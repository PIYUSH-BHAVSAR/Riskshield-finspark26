import React, { useState, useEffect } from 'react';
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, BarChart, Bar, Cell } from 'recharts';
import client from '../api/client';

const Dashboard = () => {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [triggering, setTriggering] = useState(false);
  const [triggerSuccess, setTriggerSuccess] = useState('');

  const fetchStats = async () => {
    try {
      setError('');
      const response = await client.get('/api/analytics');
      setStats(response.data);
    } catch (err) {
      console.error(err);
      setError('Failed to fetch system analytics dashboard.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchStats();
    // Poll stats every 15 seconds
    const interval = setInterval(fetchStats, 15000);
    return () => clearInterval(interval);
  }, []);

  const handleRunCorrelation = async () => {
    setTriggering(true);
    setTriggerSuccess('');
    try {
      const response = await client.post('/api/run-correlation');
      const count = response.data.new_alerts_created;
      setTriggerSuccess(`Correlation engine ran successfully. Detected ${count} new threat vectors.`);
      fetchStats();
      setTimeout(() => setTriggerSuccess(''), 5000);
    } catch (err) {
      console.error(err);
      setError('Failed to trigger database correlation engine.');
    } finally {
      setTriggering(false);
    }
  };

  if (loading) {
    return (
      <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '80vh', color: '#94a3b8' }}>
        <h3>Loading System Telemetry & KPIs...</h3>
      </div>
    );
  }

  const COLORS = ['#ef4444', '#f97316', '#eab308', '#22c55e']; // Critical, High, Medium, Low

  return (
    <div>
      <div className="header-row">
        <div>
          <h1 className="page-title">Executive Dashboard</h1>
          <p className="page-subtitle">Unified Cyber Threat & Transaction Correlation Operations Center</p>
        </div>
        <div style={{ display: 'flex', gap: '1rem', alignItems: 'center' }}>
          {triggerSuccess && (
            <span style={{ fontSize: '0.875rem', color: '#34d399', fontWeight: 500 }}>
              {triggerSuccess}
            </span>
          )}
          <button 
            className="btn btn-primary" 
            onClick={handleRunCorrelation}
            disabled={triggering}
          >
            🔄 {triggering ? 'Running Correlation...' : 'Scan Correlation'}
          </button>
        </div>
      </div>

      {error && (
        <div style={{ padding: '0.75rem 1rem', background: 'rgba(239, 68, 68, 0.15)', border: '1px solid rgba(239, 68, 68, 0.3)', borderRadius: '8px', color: '#f87171', marginBottom: '1.5rem' }}>
          {error}
        </div>
      )}

      {/* KPI Cards Grid */}
      <div className="grid-stats">
        <div className="glass-panel stat-card">
          <span className="stat-label">Total Correlated Alerts</span>
          <span className="stat-value">{stats?.total_alerts}</span>
          <span className="stat-trend" style={{ color: '#22c55e' }}>Active Monitoring</span>
        </div>
        
        <div className="glass-panel stat-card" style={{ borderLeft: '4px solid #ef4444' }}>
          <span className="stat-label">Critical Threat Vectors</span>
          <span className="stat-value" style={{ color: '#ef4444' }}>{stats?.critical_alerts}</span>
          <span className="stat-trend" style={{ color: stats?.critical_alerts > 0 ? '#ef4444' : '#64748b' }}>
            {stats?.critical_alerts > 0 ? '⚠️ Immediate Action Required' : 'No Critical Incidents'}
          </span>
        </div>

        <div className="glass-panel stat-card" style={{ borderLeft: '4px solid #f97316' }}>
          <span className="stat-label">High Severity Scopes</span>
          <span className="stat-value" style={{ color: '#f97316' }}>{stats?.high_alerts}</span>
          <span className="stat-trend" style={{ color: '#f97316' }}>Needs Investigation</span>
        </div>

        <div className="glass-panel stat-card">
          <span className="stat-label">Average Risk Index</span>
          <span className="stat-value">{(stats?.average_risk_score * 100).toFixed(1)}%</span>
          <span className="stat-trend" style={{ color: stats?.average_risk_score > 0.6 ? '#f97316' : '#22c55e' }}>
            {stats?.average_risk_score > 0.6 ? 'High Mean Exposure' : 'Exposure Controlled'}
          </span>
        </div>
      </div>

      {/* Charts Grid */}
      <div className="charts-grid">
        <div className="glass-panel" style={{ height: '380px' }}>
          <div className="chart-header">
            <span>7-Day Correlation Incident Trend</span>
            <span style={{ fontSize: '0.8rem', color: '#64748b' }}>Frequency / Day</span>
          </div>
          <div style={{ width: '100%', height: '300px' }}>
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={stats?.alerts_trend} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                <defs>
                  <linearGradient id="colorCount" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#6366f1" stopOpacity={0.4}/>
                    <stop offset="95%" stopColor="#6366f1" stopOpacity={0.0}/>
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" />
                <XAxis dataKey="date" stroke="#64748b" fontSize={11} tickLine={false} />
                <YAxis stroke="#64748b" fontSize={11} tickLine={false} />
                <Tooltip 
                  contentStyle={{ backgroundColor: '#1e293b', border: '1px solid rgba(255,255,255,0.1)', borderRadius: '8px' }}
                  labelStyle={{ color: '#ffffff', fontWeight: 600 }}
                />
                <Area type="monotone" dataKey="count" stroke="#6366f1" strokeWidth={2} fillOpacity={1} fill="url(#colorCount)" name="Correlations" />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="glass-panel" style={{ height: '380px' }}>
          <div className="chart-header">
            <span>Threat Severity Profiles</span>
          </div>
          <div style={{ width: '100%', height: '300px' }}>
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={stats?.risk_distribution} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" />
                <XAxis dataKey="name" stroke="#64748b" fontSize={11} tickLine={false} />
                <YAxis stroke="#64748b" fontSize={11} tickLine={false} />
                <Tooltip 
                  contentStyle={{ backgroundColor: '#1e293b', border: '1px solid rgba(255,255,255,0.1)', borderRadius: '8px' }}
                  labelStyle={{ color: '#ffffff', fontWeight: 600 }}
                  cursor={{ fill: 'rgba(255,255,255,0.02)' }}
                />
                <Bar dataKey="value" name="Threats" radius={[4, 4, 0, 0]}>
                  {stats?.risk_distribution.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>

      {/* Systems Status Summary */}
      <div className="glass-panel" style={{ marginTop: '2rem' }}>
        <h3 style={{ color: 'white', marginBottom: '1rem', fontSize: '1.2rem' }}>Audit & Telemetry Environment Details</h3>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '2rem' }}>
          <div>
            <span style={{ fontSize: '0.85rem', color: '#64748b', display: 'block' }}>Operational Health</span>
            <div className="status-indicator" style={{ marginTop: '0.5rem', color: 'white', fontSize: '1rem' }}>
              <span className={`status-dot ${stats?.system_status || 'healthy'}`}></span>
              {stats?.system_status === 'healthy' ? 'System Fully Operational' : (stats?.system_status === 'warning' ? 'Exposure Warning' : 'System Degraded')}
            </div>
          </div>
          <div>
            <span style={{ fontSize: '0.85rem', color: '#64748b', display: 'block' }}>Database Provider</span>
            <span style={{ color: 'white', display: 'block', marginTop: '0.5rem', fontWeight: 600 }}>SQLAlchemy (PostgreSQL / SQLite)</span>
          </div>
          <div>
            <span style={{ fontSize: '0.85rem', color: '#64748b', display: 'block' }}>ML Analytics Stream</span>
            <span style={{ color: 'white', display: 'block', marginTop: '0.5rem', fontWeight: 600 }}>CatBoost + IsolationForest</span>
          </div>
          <div>
            <span style={{ fontSize: '0.85rem', color: '#64748b', display: 'block' }}>Temporal Scanning Rule</span>
            <span style={{ color: 'white', display: 'block', marginTop: '0.5rem', fontWeight: 600 }}>15 Minute Sliding Correlation</span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
