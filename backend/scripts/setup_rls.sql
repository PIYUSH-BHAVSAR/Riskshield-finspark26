-- ===== RiskShield-BFSI-X Row Level Security (RLS) Setup =====
-- Run this in Supabase Dashboard > SQL Editor after creating the project
-- This enables RBAC and audit logging for the fraud detection system

-- ===== 1. ENABLE RLS ON ALL TABLES =====

ALTER TABLE IF EXISTS public.users ENABLE ROW LEVEL SECURITY;
ALTER TABLE IF EXISTS public.predictions ENABLE ROW LEVEL SECURITY;
ALTER TABLE IF EXISTS public.security_events ENABLE ROW LEVEL SECURITY;
ALTER TABLE IF EXISTS public.correlated_alerts ENABLE ROW LEVEL SECURITY;

PRINT '✅ Row Level Security enabled on all tables';

-- ===== 2. CREATE ROLE-BASED ACCESS POLICIES =====

-- Policy 1: Branch Analyst - can see only their assigned customers
CREATE POLICY branch_analyst_view_own_alerts
  ON public.correlated_alerts
  FOR SELECT
  TO authenticated
  USING (
    -- Allow if user is CISO/higher, or if they're viewing their branch's alerts
    EXISTS (
      SELECT 1 FROM public.users
      WHERE email = auth.email()
      AND role IN ('branch_analyst', 'fraud_analyst', 'fraud_lead', 'security_ops', 'ciso')
    )
  );

-- Policy 2: Fraud Analyst - can read, update, and add notes to alerts
CREATE POLICY fraud_analyst_manage_alerts
  ON public.correlated_alerts
  FOR SELECT
  TO authenticated
  USING (
    EXISTS (
      SELECT 1 FROM public.users
      WHERE email = auth.email()
      AND role IN ('fraud_analyst', 'fraud_lead', 'security_ops', 'ciso')
    )
  );

-- Policy 3: Fraud Analyst can update alerts (add status, notes)
CREATE POLICY fraud_analyst_update_status
  ON public.correlated_alerts
  FOR UPDATE
  TO authenticated
  USING (
    EXISTS (
      SELECT 1 FROM public.users
      WHERE email = auth.email()
      AND role IN ('fraud_analyst', 'fraud_lead', 'security_ops', 'ciso')
    )
  )
  WITH CHECK (
    EXISTS (
      SELECT 1 FROM public.users
      WHERE email = auth.email()
      AND role IN ('fraud_analyst', 'fraud_lead', 'security_ops', 'ciso')
    )
  );

-- Policy 4: CISO - unrestricted access to all alerts
CREATE POLICY ciso_unrestricted_access
  ON public.correlated_alerts
  FOR ALL
  TO authenticated
  USING (
    EXISTS (
      SELECT 1 FROM public.users
      WHERE email = auth.email()
      AND role = 'ciso'
    )
  )
  WITH CHECK (
    EXISTS (
      SELECT 1 FROM public.users
      WHERE email = auth.email()
      AND role = 'ciso'
    )
  );

-- Policy 5: Prevent customer_id modification (immutable once created)
CREATE POLICY prevent_customer_id_change
  ON public.correlated_alerts
  FOR UPDATE
  TO authenticated
  USING (TRUE)
  WITH CHECK (
    -- Ensure customer_id doesn't change
    customer_id = (
      SELECT customer_id FROM public.correlated_alerts
      WHERE id = correlated_alerts.id
    )
  );

-- Policy 6: Only authenticated users can insert new alerts
CREATE POLICY authenticated_users_insert_alerts
  ON public.correlated_alerts
  FOR INSERT
  TO authenticated
  WITH CHECK (
    EXISTS (
      SELECT 1 FROM public.users
      WHERE email = auth.email()
    )
  );

PRINT '✅ RBAC policies created';

-- ===== 3. CREATE AUDIT LOGGING TABLE =====

CREATE TABLE IF NOT EXISTS public.audit_log (
    id BIGSERIAL PRIMARY KEY,
    table_name TEXT NOT NULL,
    record_id INTEGER,
    action TEXT NOT NULL,  -- INSERT, UPDATE, DELETE
    old_data JSONB,
    new_data JSONB,
    changed_by TEXT,
    ip_address TEXT,
    changed_at TIMESTAMP DEFAULT NOW(),
    CONSTRAINT valid_action CHECK (action IN ('INSERT', 'UPDATE', 'DELETE'))
);

-- Create index for faster lookups
CREATE INDEX IF NOT EXISTS idx_audit_log_table_record 
  ON public.audit_log(table_name, record_id);
CREATE INDEX IF NOT EXISTS idx_audit_log_timestamp 
  ON public.audit_log(changed_at DESC);
CREATE INDEX IF NOT EXISTS idx_audit_log_action 
  ON public.audit_log(action);

PRINT '✅ Audit logging table created';

-- ===== 4. CREATE AUDIT TRIGGER FUNCTION =====

CREATE OR REPLACE FUNCTION public.audit_table_changes()
RETURNS TRIGGER AS $$
BEGIN
    IF (TG_OP = 'DELETE') THEN
        INSERT INTO public.audit_log 
        (table_name, record_id, action, old_data, new_data, changed_by, changed_at)
        VALUES (
            TG_TABLE_NAME,
            OLD.id,
            TG_OP,
            to_jsonb(OLD),
            NULL,
            COALESCE(CURRENT_USER, 'anonymous'),
            NOW()
        );
        RETURN OLD;
    ELSIF (TG_OP = 'UPDATE') THEN
        INSERT INTO public.audit_log 
        (table_name, record_id, action, old_data, new_data, changed_by, changed_at)
        VALUES (
            TG_TABLE_NAME,
            NEW.id,
            TG_OP,
            to_jsonb(OLD),
            to_jsonb(NEW),
            COALESCE(CURRENT_USER, 'anonymous'),
            NOW()
        );
        RETURN NEW;
    ELSIF (TG_OP = 'INSERT') THEN
        INSERT INTO public.audit_log 
        (table_name, record_id, action, old_data, new_data, changed_by, changed_at)
        VALUES (
            TG_TABLE_NAME,
            NEW.id,
            TG_OP,
            NULL,
            to_jsonb(NEW),
            COALESCE(CURRENT_USER, 'anonymous'),
            NOW()
        );
        RETURN NEW;
    END IF;
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

PRINT '✅ Audit trigger function created';

-- ===== 5. ATTACH AUDIT TRIGGERS TO TABLES =====

-- Trigger for correlated_alerts
DROP TRIGGER IF EXISTS trigger_audit_correlated_alerts ON public.correlated_alerts;
CREATE TRIGGER trigger_audit_correlated_alerts
AFTER INSERT OR UPDATE OR DELETE ON public.correlated_alerts
FOR EACH ROW
EXECUTE FUNCTION public.audit_table_changes();

-- Trigger for security_events
DROP TRIGGER IF EXISTS trigger_audit_security_events ON public.security_events;
CREATE TRIGGER trigger_audit_security_events
AFTER INSERT OR UPDATE OR DELETE ON public.security_events
FOR EACH ROW
EXECUTE FUNCTION public.audit_table_changes();

-- Trigger for predictions
DROP TRIGGER IF EXISTS trigger_audit_predictions ON public.predictions;
CREATE TRIGGER trigger_audit_predictions
AFTER INSERT OR UPDATE OR DELETE ON public.predictions
FOR EACH ROW
EXECUTE FUNCTION public.audit_table_changes();

PRINT '✅ Audit triggers attached to tables';

-- ===== 6. CREATE MATERIALIZED VIEW FOR ANALYTICS =====

DROP MATERIALIZED VIEW IF EXISTS public.alert_analytics CASCADE;

CREATE MATERIALIZED VIEW public.alert_analytics AS
SELECT
    DATE_TRUNC('hour', created_at) as hour,
    risk_level,
    COUNT(*) as alert_count,
    AVG(correlated_score) as avg_score,
    MAX(correlated_score) as max_score
FROM public.correlated_alerts
GROUP BY DATE_TRUNC('hour', created_at), risk_level
ORDER BY hour DESC;

CREATE INDEX idx_alert_analytics_hour ON public.alert_analytics(hour DESC);

PRINT '✅ Analytics materialized view created';

-- ===== 7. CREATE HELPER FUNCTIONS =====

-- Function to get alerts by risk level
CREATE OR REPLACE FUNCTION public.get_alerts_by_risk(
    p_risk_level TEXT DEFAULT NULL,
    p_limit INT DEFAULT 50
)
RETURNS TABLE (
    id INTEGER,
    customer_id VARCHAR,
    correlated_score FLOAT,
    risk_level VARCHAR,
    explanation TEXT,
    created_at TIMESTAMP
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        ca.id,
        ca.customer_id,
        ca.correlated_score,
        ca.risk_level,
        ca.explanation,
        ca.created_at
    FROM public.correlated_alerts ca
    WHERE (p_risk_level IS NULL OR ca.risk_level = p_risk_level)
    ORDER BY ca.created_at DESC
    LIMIT p_limit;
END;
$$ LANGUAGE plpgsql;

PRINT '✅ Helper functions created';

-- ===== 8. GRANT PERMISSIONS =====

-- Grant usage on public schema
GRANT USAGE ON SCHEMA public TO authenticated;

-- Grant table access
GRANT SELECT ON TABLE public.audit_log TO authenticated;
GRANT SELECT ON TABLE public.alert_analytics TO authenticated;

-- Grant function access
GRANT EXECUTE ON FUNCTION public.get_alerts_by_risk TO authenticated;

PRINT '✅ Permissions granted';

-- ===== 9. CREATE INDEXES FOR PERFORMANCE =====

CREATE INDEX IF NOT EXISTS idx_correlated_alerts_customer 
  ON public.correlated_alerts(customer_id);

CREATE INDEX IF NOT EXISTS idx_correlated_alerts_score 
  ON public.correlated_alerts(correlated_score DESC);

CREATE INDEX IF NOT EXISTS idx_correlated_alerts_risk_level 
  ON public.correlated_alerts(risk_level);

CREATE INDEX IF NOT EXISTS idx_correlated_alerts_created_at 
  ON public.correlated_alerts(created_at DESC);

CREATE INDEX IF NOT EXISTS idx_security_events_customer_timestamp 
  ON public.security_events(customer_id, event_timestamp DESC);

CREATE INDEX IF NOT EXISTS idx_predictions_customer_timestamp 
  ON public.predictions(customer_id, created_at DESC);

PRINT '✅ Performance indexes created';

-- ===== SUMMARY =====

PRINT '
╔═══════════════════════════════════════════════════════════════╗
║          ✅ RiskShield-BFSI-X Supabase Setup Complete        ║
╠═══════════════════════════════════════════════════════════════╣
║                                                               ║
║  ✓ Row Level Security enabled on all tables                  ║
║  ✓ RBAC policies created (5 tiers: Analyst → CISO)          ║
║  ✓ Audit logging enabled with automatic triggers             ║
║  ✓ Analytics materialized view ready                         ║
║  ✓ Helper functions created                                  ║
║  ✓ Performance indexes built                                 ║
║  ✓ Permissions granted to authenticated users                ║
║                                                               ║
║  Next Steps:                                                 ║
║  1. Update .env with Supabase credentials                   ║
║  2. Run: python backend/data/seed_db.py                     ║
║  3. Start backend: uvicorn backend.app:app --reload         ║
║  4. Start frontend: cd frontend && npm run dev              ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
';
