/**
 * RiskShield-BFSI-X — Frontend Mock Data
 * Complete seed data mirroring the backend SQLite database.
 * Used when backend is not deployed. All API calls are intercepted by mockClient.js
 */

// ===== TRANSACTIONS =====
export const MOCK_TRANSACTIONS = [
  { id: 1, customer_id: 'CUST1000', email: 'arjun.mehta@hdfc.com', transaction_id: 'TXN10000', transaction_amount: 84500, transaction_datetime: '2026-07-16T03:12:00', prediction_score: 0.82, is_fraud: 1, rules_triggered: ['HIGH_VALUE', 'NEW_BENEFICIARY'], combined_score: 0.82 },
  { id: 2, customer_id: 'CUST1001', email: 'priya.sharma@icici.com', transaction_id: 'TXN10001', transaction_amount: 12300, transaction_datetime: '2026-07-16T04:45:00', prediction_score: 0.55, is_fraud: 0, rules_triggered: ['ODD_HOUR'], combined_score: 0.55 },
  { id: 3, customer_id: 'CUST1002', email: 'rohit.verma@sbi.com', transaction_id: 'TXN10002', transaction_amount: 215000, transaction_datetime: '2026-07-16T06:20:00', prediction_score: 0.91, is_fraud: 1, rules_triggered: ['HIGH_VALUE', 'NEW_BENEFICIARY', 'RAPID_SUCCESSION'], combined_score: 0.91 },
  { id: 4, customer_id: 'CUST1003', email: 'sneha.patel@axis.com', transaction_id: 'TXN10003', transaction_amount: 5800, transaction_datetime: '2026-07-16T07:10:00', prediction_score: 0.38, is_fraud: 0, rules_triggered: [], combined_score: 0.38 },
  { id: 5, customer_id: 'CUST1004', email: 'vikram.iyer@kotak.com', transaction_id: 'TXN10004', transaction_amount: 67200, transaction_datetime: '2026-07-16T08:33:00', prediction_score: 0.74, is_fraud: 1, rules_triggered: ['HIGH_VALUE', 'GEO_MISMATCH'], combined_score: 0.74 },
  { id: 6, customer_id: 'CUST1005', email: 'anita.reddy@yes.com', transaction_id: 'TXN10005', transaction_amount: 3200, transaction_datetime: '2026-07-16T09:55:00', prediction_score: 0.22, is_fraud: 0, rules_triggered: [], combined_score: 0.22 },
  { id: 7, customer_id: 'CUST1006', email: 'deepak.nair@pnb.com', transaction_id: 'TXN10006', transaction_amount: 142000, transaction_datetime: '2026-07-16T10:14:00', prediction_score: 0.88, is_fraud: 1, rules_triggered: ['HIGH_VALUE', 'RAPID_SUCCESSION', 'NEW_BENEFICIARY'], combined_score: 0.88 },
  { id: 8, customer_id: 'CUST1007', email: 'kavya.singh@bob.com', transaction_id: 'TXN10007', transaction_amount: 29000, transaction_datetime: '2026-07-16T11:02:00', prediction_score: 0.61, is_fraud: 0, rules_triggered: ['ODD_HOUR'], combined_score: 0.61 },
];

// ===== SECURITY EVENTS =====
export const MOCK_SECURITY_EVENTS = [
  { id: 1, customer_id: 'CUST1000', email: 'arjun.mehta@hdfc.com', event_type: 'failed_login', device_fingerprint: 'DEV-A4F2C8', ip_address: '185.220.101.47', geo_location: 'Moscow, Russia', hard_flags: ['new_device', 'impossible_travel'], iso_anomaly_flag: 1, security_trap_score: 3.2, event_timestamp: '2026-07-16T03:05:00' },
  { id: 2, customer_id: 'CUST1001', email: 'priya.sharma@icici.com', event_type: 'login', device_fingerprint: 'DEV-B7E1D3', ip_address: '103.21.58.120', geo_location: 'Bengaluru, India', hard_flags: ['multiple_failed_attempts'], iso_anomaly_flag: 0, security_trap_score: 1.4, event_timestamp: '2026-07-16T04:39:00' },
  { id: 3, customer_id: 'CUST1002', email: 'rohit.verma@sbi.com', event_type: 'session_start', device_fingerprint: 'DEV-C9G5H1', ip_address: '91.108.56.200', geo_location: 'Kyiv, Ukraine', hard_flags: ['new_device', 'impossible_travel', 'tor_exit_node'], iso_anomaly_flag: 1, security_trap_score: 4.1, event_timestamp: '2026-07-16T06:12:00' },
  { id: 4, customer_id: 'CUST1003', email: 'sneha.patel@axis.com', event_type: 'login', device_fingerprint: 'DEV-D2K8L6', ip_address: '49.36.200.15', geo_location: 'Mumbai, India', hard_flags: [], iso_anomaly_flag: 0, security_trap_score: 0.6, event_timestamp: '2026-07-16T07:08:00' },
  { id: 5, customer_id: 'CUST1004', email: 'vikram.iyer@kotak.com', event_type: 'failed_login', device_fingerprint: 'DEV-E5M3N9', ip_address: '194.165.16.77', geo_location: 'Amsterdam, Netherlands', hard_flags: ['new_device', 'geo_mismatch'], iso_anomaly_flag: 1, security_trap_score: 2.8, event_timestamp: '2026-07-16T08:27:00' },
  { id: 6, customer_id: 'CUST1005', email: 'anita.reddy@yes.com', event_type: 'session_start', device_fingerprint: 'DEV-F8P4Q2', ip_address: '122.160.97.34', geo_location: 'Hyderabad, India', hard_flags: [], iso_anomaly_flag: 0, security_trap_score: 0.3, event_timestamp: '2026-07-16T09:51:00' },
  { id: 7, customer_id: 'CUST1006', email: 'deepak.nair@pnb.com', event_type: 'failed_login', device_fingerprint: 'DEV-G1R7S5', ip_address: '45.155.205.90', geo_location: 'Frankfurt, Germany', hard_flags: ['new_device', 'impossible_travel', 'multiple_failed_attempts'], iso_anomaly_flag: 1, security_trap_score: 3.9, event_timestamp: '2026-07-16T10:07:00' },
  { id: 8, customer_id: 'CUST1007', email: 'kavya.singh@bob.com', event_type: 'login', device_fingerprint: 'DEV-H4T2U8', ip_address: '203.110.83.44', geo_location: 'Delhi, India', hard_flags: ['odd_hour_login'], iso_anomaly_flag: 0, security_trap_score: 1.1, event_timestamp: '2026-07-16T10:58:00' },
];

// ===== CORRELATED ALERTS (with nested transaction + security_event) =====
export const MOCK_ALERTS = [
  {
    id: 1, customer_id: 'CUST1000', transaction_id: 1, security_event_id: 1,
    correlation_window_sec: 420, correlated_score: 0.91, risk_level: 'Critical', status: 'open',
    created_at: '2026-07-16T03:15:00',
    explanation: `CRITICAL CORRELATION DETECTED\n\nCustomer CUST1000 (arjun.mehta@hdfc.com) triggered a high-value transaction of ₹84,500 to a new beneficiary at 03:12 UTC.\n\nWithin 7 minutes prior, a failed login was detected from IP 185.220.101.47 (Moscow, Russia) — a geographic impossibility given the customer's registered address in Mumbai.\n\nThe device fingerprint DEV-A4F2C8 has never been seen before on this account. IsolationForest flagged this session as a statistical outlier (score: 3.2).\n\nRule triggers: HIGH_VALUE + NEW_BENEFICIARY on transaction stream. new_device + impossible_travel + IsolationForest on identity stream.\n\nRecommendation: FREEZE account and escalate to L2 fraud operations immediately.`,
    transaction: MOCK_TRANSACTIONS[0],
    security_event: MOCK_SECURITY_EVENTS[0],
  },
  {
    id: 2, customer_id: 'CUST1002', transaction_id: 3, security_event_id: 3,
    correlation_window_sec: 480, correlated_score: 0.95, risk_level: 'Critical', status: 'investigating',
    created_at: '2026-07-16T06:22:00',
    explanation: `CRITICAL CORRELATION DETECTED\n\nCustomer CUST1002 (rohit.verma@sbi.com) executed a wire transfer of ₹2,15,000 — the largest single transaction in their 4-year account history.\n\nExactly 8 minutes before the transfer, a session was initiated from a Tor exit node (IP 91.108.56.200, Kyiv Ukraine). The device DEV-C9G5H1 is unrecognized.\n\nIsolationForest anomaly score of 4.1 — top 0.1% statistical outlier across entire customer base.\n\nRule triggers: HIGH_VALUE + NEW_BENEFICIARY + RAPID_SUCCESSION on transaction. new_device + impossible_travel + tor_exit_node + IsolationForest on identity.\n\nRecommendation: Transaction flagged for reversal review. Customer verification required via registered mobile OTP.`,
    transaction: MOCK_TRANSACTIONS[2],
    security_event: MOCK_SECURITY_EVENTS[2],
  },
  {
    id: 3, customer_id: 'CUST1004', transaction_id: 5, security_event_id: 5,
    correlation_window_sec: 360, correlated_score: 0.78, risk_level: 'High', status: 'open',
    created_at: '2026-07-16T08:35:00',
    explanation: `HIGH RISK CORRELATION\n\nCustomer CUST1004 (vikram.iyer@kotak.com) transferred ₹67,200 at 08:33 UTC. The transaction ML score of 0.74 indicates elevated fraud probability.\n\nA failed login attempt was detected 6 minutes earlier from Amsterdam (IP 194.165.16.77) — inconsistent with customer's usual access from Chennai.\n\nNew device fingerprint DEV-E5M3N9 detected. IsolationForest confirms anomalous session behaviour.\n\nRule triggers: HIGH_VALUE + GEO_MISMATCH on transaction. new_device + geo_mismatch + IsolationForest on identity.\n\nRecommendation: Place soft block on account. Contact customer for verification before processing further transactions.`,
    transaction: MOCK_TRANSACTIONS[4],
    security_event: MOCK_SECURITY_EVENTS[4],
  },
  {
    id: 4, customer_id: 'CUST1006', transaction_id: 7, security_event_id: 7,
    correlation_window_sec: 420, correlated_score: 0.86, risk_level: 'Critical', status: 'open',
    created_at: '2026-07-16T10:16:00',
    explanation: `CRITICAL CORRELATION DETECTED\n\nCustomer CUST1006 (deepak.nair@pnb.com) initiated a transfer of ₹1,42,000 with RAPID_SUCCESSION flag — this is the 3rd transaction in 90 minutes.\n\n7 minutes before this transaction, 4 consecutive failed login attempts were recorded from Frankfurt Germany (IP 45.155.205.90). Device DEV-G1R7S5 is new to this account.\n\nIsolationForest score 3.9 — strong anomaly signal. Pattern consistent with credential stuffing attack followed by account takeover.\n\nRule triggers: HIGH_VALUE + RAPID_SUCCESSION + NEW_BENEFICIARY on transaction. new_device + impossible_travel + multiple_failed_attempts + IsolationForest on identity.\n\nRecommendation: IMMEDIATE account freeze. Escalate to cybersecurity incident response team.`,
    transaction: MOCK_TRANSACTIONS[6],
    security_event: MOCK_SECURITY_EVENTS[6],
  },
  {
    id: 5, customer_id: 'CUST1001', transaction_id: 2, security_event_id: 2,
    correlation_window_sec: 360, correlated_score: 0.58, risk_level: 'Medium', status: 'open',
    created_at: '2026-07-16T04:47:00',
    explanation: `MEDIUM RISK CORRELATION\n\nCustomer CUST1001 (priya.sharma@icici.com) made a ₹12,300 transaction at an unusual hour (04:45 UTC).\n\nA login was recorded 6 minutes earlier from Bengaluru — consistent with customer location, but multiple failed attempts preceded the successful login.\n\nNo new device or impossible travel detected. IsolationForest did not flag this session.\n\nRule triggers: ODD_HOUR on transaction. multiple_failed_attempts on identity.\n\nRecommendation: Monitor for 24 hours. Send SMS alert to customer. No immediate block required.`,
    transaction: MOCK_TRANSACTIONS[1],
    security_event: MOCK_SECURITY_EVENTS[1],
  },
  {
    id: 6, customer_id: 'CUST1007', transaction_id: 8, security_event_id: 8,
    correlation_window_sec: 240, correlated_score: 0.52, risk_level: 'Medium', status: 'resolved',
    created_at: '2026-07-16T11:04:00',
    explanation: `MEDIUM RISK CORRELATION\n\nCustomer CUST1007 (kavya.singh@bob.com) transferred ₹29,000 at 11:02 UTC with an ODD_HOUR flag.\n\nA login was detected 4 minutes earlier from Delhi — customer's registered city. Device DEV-H4T2U8 is known.\n\nMinor anomaly: odd_hour_login flag on identity stream. IsolationForest did not flag.\n\nRule triggers: ODD_HOUR on transaction. odd_hour_login on identity.\n\nRecommendation: Low priority. Alert auto-resolved after customer confirmed via mobile app. No action required.`,
    transaction: MOCK_TRANSACTIONS[7],
    security_event: MOCK_SECURITY_EVENTS[7],
  },
  {
    id: 7, customer_id: 'CUST1003', transaction_id: 4, security_event_id: 4,
    correlation_window_sec: 120, correlated_score: 0.31, risk_level: 'Low', status: 'false_positive',
    created_at: '2026-07-16T07:12:00',
    explanation: `LOW RISK CORRELATION\n\nCustomer CUST1003 (sneha.patel@axis.com) transacted ₹5,800 with a low ML fraud score of 0.38.\n\nLogin detected 2 minutes before from Mumbai — consistent with customer's registered location. Known device DEV-D2K8L6.\n\nNo flags on either stream. Correlation detected purely due to temporal proximity.\n\nRule triggers: None on transaction. None on identity.\n\nRecommendation: False positive. Correlation window produced no meaningful signal. Mark as resolved.`,
    transaction: MOCK_TRANSACTIONS[3],
    security_event: MOCK_SECURITY_EVENTS[3],
  },
  {
    id: 8, customer_id: 'CUST1005', transaction_id: 6, security_event_id: 6,
    correlation_window_sec: 240, correlated_score: 0.28, risk_level: 'Low', status: 'resolved',
    created_at: '2026-07-16T09:57:00',
    explanation: `LOW RISK CORRELATION\n\nCustomer CUST1005 (anita.reddy@yes.com) transacted ₹3,200 — a routine amount well within normal behaviour.\n\nSession started from Hyderabad 4 minutes prior. Known device, no geographic anomaly detected.\n\nIsolationForest score well within normal range. No rules triggered on either stream.\n\nRecommendation: No action required. System auto-resolved.`,
    transaction: MOCK_TRANSACTIONS[5],
    security_event: MOCK_SECURITY_EVENTS[5],
  },
];

// ===== ANALYTICS =====
export const MOCK_ANALYTICS = {
  total_alerts: 8,
  critical_alerts: 3,
  high_alerts: 1,
  avg_correlated_score: 0.65,
  average_risk_score: 0.65,
  system_status: 'healthy',
  alerts_trend: [
    { date: 'Jul 10', count: 2 },
    { date: 'Jul 11', count: 5 },
    { date: 'Jul 12', count: 3 },
    { date: 'Jul 13', count: 7 },
    { date: 'Jul 14', count: 4 },
    { date: 'Jul 15', count: 6 },
    { date: 'Jul 16', count: 8 },
  ],
  risk_distribution: [
    { name: 'Critical', value: 3 },
    { name: 'High', value: 1 },
    { name: 'Medium', value: 2 },
    { name: 'Low', value: 2 },
  ],
  top_risk_customers: [
    { customer_id: 'CUST1002', count: 1, avg_score: 0.95, max_risk: 'Critical' },
    { customer_id: 'CUST1006', count: 1, avg_score: 0.86, max_risk: 'Critical' },
    { customer_id: 'CUST1000', count: 1, avg_score: 0.91, max_risk: 'Critical' },
    { customer_id: 'CUST1004', count: 1, avg_score: 0.78, max_risk: 'High' },
    { customer_id: 'CUST1001', count: 1, avg_score: 0.58, max_risk: 'Medium' },
  ],
};

// ===== GRAPH DATA per alert id =====
export const MOCK_GRAPHS = {
  1: {
    nodes: [
      { id: 'cust_CUST1000', label: 'CUST1000', type: 'customer', value: 30, details: 'arjun.mehta@hdfc.com' },
      { id: 'tx_1', label: 'TXN10000', type: 'transaction', value: 25, details: 'Amount: ₹84,500 | Score: 0.82' },
      { id: 'event_1', label: 'failed_login', type: 'security_event', value: 25, details: 'Trap Score: 3.2' },
      { id: 'dev_DEV-A4F2C8', label: 'DEV-A4F2C8', type: 'device', value: 15, details: 'Unknown device' },
      { id: 'ip_185.220.101.47', label: '185.220.101.47', type: 'ip', value: 15, details: 'Moscow, Russia' },
    ],
    edges: [
      { source: 'cust_CUST1000', target: 'tx_1', type: 'transact' },
      { source: 'cust_CUST1000', target: 'event_1', type: 'correlation' },
      { source: 'event_1', target: 'dev_DEV-A4F2C8', type: 'used_device' },
      { source: 'event_1', target: 'ip_185.220.101.47', type: 'login_from' },
    ],
  },
  2: {
    nodes: [
      { id: 'cust_CUST1002', label: 'CUST1002', type: 'customer', value: 30, details: 'rohit.verma@sbi.com' },
      { id: 'tx_3', label: 'TXN10002', type: 'transaction', value: 25, details: 'Amount: ₹2,15,000 | Score: 0.91' },
      { id: 'event_3', label: 'session_start', type: 'security_event', value: 25, details: 'Trap Score: 4.1' },
      { id: 'dev_DEV-C9G5H1', label: 'DEV-C9G5H1', type: 'device', value: 15, details: 'Tor exit node device' },
      { id: 'ip_91.108.56.200', label: '91.108.56.200', type: 'ip', value: 15, details: 'Kyiv, Ukraine' },
    ],
    edges: [
      { source: 'cust_CUST1002', target: 'tx_3', type: 'transact' },
      { source: 'cust_CUST1002', target: 'event_3', type: 'correlation' },
      { source: 'event_3', target: 'dev_DEV-C9G5H1', type: 'used_device' },
      { source: 'event_3', target: 'ip_91.108.56.200', type: 'login_from' },
    ],
  },
  3: {
    nodes: [
      { id: 'cust_CUST1004', label: 'CUST1004', type: 'customer', value: 30, details: 'vikram.iyer@kotak.com' },
      { id: 'tx_5', label: 'TXN10004', type: 'transaction', value: 25, details: 'Amount: ₹67,200 | Score: 0.74' },
      { id: 'event_5', label: 'failed_login', type: 'security_event', value: 25, details: 'Trap Score: 2.8' },
      { id: 'dev_DEV-E5M3N9', label: 'DEV-E5M3N9', type: 'device', value: 15, details: 'New device' },
      { id: 'ip_194.165.16.77', label: '194.165.16.77', type: 'ip', value: 15, details: 'Amsterdam, Netherlands' },
    ],
    edges: [
      { source: 'cust_CUST1004', target: 'tx_5', type: 'transact' },
      { source: 'cust_CUST1004', target: 'event_5', type: 'correlation' },
      { source: 'event_5', target: 'dev_DEV-E5M3N9', type: 'used_device' },
      { source: 'event_5', target: 'ip_194.165.16.77', type: 'login_from' },
    ],
  },
  4: {
    nodes: [
      { id: 'cust_CUST1006', label: 'CUST1006', type: 'customer', value: 30, details: 'deepak.nair@pnb.com' },
      { id: 'tx_7', label: 'TXN10006', type: 'transaction', value: 25, details: 'Amount: ₹1,42,000 | Score: 0.88' },
      { id: 'event_7', label: 'failed_login', type: 'security_event', value: 25, details: 'Trap Score: 3.9' },
      { id: 'dev_DEV-G1R7S5', label: 'DEV-G1R7S5', type: 'device', value: 15, details: 'New device' },
      { id: 'ip_45.155.205.90', label: '45.155.205.90', type: 'ip', value: 15, details: 'Frankfurt, Germany' },
    ],
    edges: [
      { source: 'cust_CUST1006', target: 'tx_7', type: 'transact' },
      { source: 'cust_CUST1006', target: 'event_7', type: 'correlation' },
      { source: 'event_7', target: 'dev_DEV-G1R7S5', type: 'used_device' },
      { source: 'event_7', target: 'ip_45.155.205.90', type: 'login_from' },
    ],
  },
  5: {
    nodes: [
      { id: 'cust_CUST1001', label: 'CUST1001', type: 'customer', value: 30, details: 'priya.sharma@icici.com' },
      { id: 'tx_2', label: 'TXN10001', type: 'transaction', value: 25, details: 'Amount: ₹12,300 | Score: 0.55' },
      { id: 'event_2', label: 'login', type: 'security_event', value: 25, details: 'Trap Score: 1.4' },
      { id: 'dev_DEV-B7E1D3', label: 'DEV-B7E1D3', type: 'device', value: 15, details: 'Known device' },
      { id: 'ip_103.21.58.120', label: '103.21.58.120', type: 'ip', value: 15, details: 'Bengaluru, India' },
    ],
    edges: [
      { source: 'cust_CUST1001', target: 'tx_2', type: 'transact' },
      { source: 'cust_CUST1001', target: 'event_2', type: 'correlation' },
      { source: 'event_2', target: 'dev_DEV-B7E1D3', type: 'used_device' },
      { source: 'event_2', target: 'ip_103.21.58.120', type: 'login_from' },
    ],
  },
  6: {
    nodes: [
      { id: 'cust_CUST1007', label: 'CUST1007', type: 'customer', value: 30, details: 'kavya.singh@bob.com' },
      { id: 'tx_8', label: 'TXN10007', type: 'transaction', value: 25, details: 'Amount: ₹29,000 | Score: 0.61' },
      { id: 'event_8', label: 'login', type: 'security_event', value: 25, details: 'Trap Score: 1.1' },
      { id: 'dev_DEV-H4T2U8', label: 'DEV-H4T2U8', type: 'device', value: 15, details: 'Known device' },
      { id: 'ip_203.110.83.44', label: '203.110.83.44', type: 'ip', value: 15, details: 'Delhi, India' },
    ],
    edges: [
      { source: 'cust_CUST1007', target: 'tx_8', type: 'transact' },
      { source: 'cust_CUST1007', target: 'event_8', type: 'correlation' },
      { source: 'event_8', target: 'dev_DEV-H4T2U8', type: 'used_device' },
      { source: 'event_8', target: 'ip_203.110.83.44', type: 'login_from' },
    ],
  },
  7: {
    nodes: [
      { id: 'cust_CUST1003', label: 'CUST1003', type: 'customer', value: 30, details: 'sneha.patel@axis.com' },
      { id: 'tx_4', label: 'TXN10003', type: 'transaction', value: 25, details: 'Amount: ₹5,800 | Score: 0.38' },
      { id: 'event_4', label: 'login', type: 'security_event', value: 25, details: 'Trap Score: 0.6' },
      { id: 'dev_DEV-D2K8L6', label: 'DEV-D2K8L6', type: 'device', value: 15, details: 'Known device' },
      { id: 'ip_49.36.200.15', label: '49.36.200.15', type: 'ip', value: 15, details: 'Mumbai, India' },
    ],
    edges: [
      { source: 'cust_CUST1003', target: 'tx_4', type: 'transact' },
      { source: 'cust_CUST1003', target: 'event_4', type: 'correlation' },
      { source: 'event_4', target: 'dev_DEV-D2K8L6', type: 'used_device' },
      { source: 'event_4', target: 'ip_49.36.200.15', type: 'login_from' },
    ],
  },
  8: {
    nodes: [
      { id: 'cust_CUST1005', label: 'CUST1005', type: 'customer', value: 30, details: 'anita.reddy@yes.com' },
      { id: 'tx_6', label: 'TXN10005', type: 'transaction', value: 25, details: 'Amount: ₹3,200 | Score: 0.22' },
      { id: 'event_6', label: 'session_start', type: 'security_event', value: 25, details: 'Trap Score: 0.3' },
      { id: 'dev_DEV-F8P4Q2', label: 'DEV-F8P4Q2', type: 'device', value: 15, details: 'Known device' },
      { id: 'ip_122.160.97.34', label: '122.160.97.34', type: 'ip', value: 15, details: 'Hyderabad, India' },
    ],
    edges: [
      { source: 'cust_CUST1005', target: 'tx_6', type: 'transact' },
      { source: 'cust_CUST1005', target: 'event_6', type: 'correlation' },
      { source: 'event_6', target: 'dev_DEV-F8P4Q2', type: 'used_device' },
      { source: 'event_6', target: 'ip_122.160.97.34', type: 'login_from' },
    ],
  },
};
