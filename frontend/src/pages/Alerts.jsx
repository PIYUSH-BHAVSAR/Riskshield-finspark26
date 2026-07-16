import React, { useState, useEffect } from 'react';
import client from '../api/client';
import RiskBadge from '../components/RiskBadge';
import NetworkGraph from '../components/NetworkGraph';

const Alerts = () => {
  const [alerts, setAlerts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [selectedAlert, setSelectedAlert] = useState(null);
  const [graphData, setGraphData] = useState(null);
  const [loadingGraph, setLoadingGraph] = useState(false);
  
  // Filters
  const [statusFilter, setStatusFilter] = useState('');
  const [riskFilter, setRiskFilter] = useState('');

  const fetchAlerts = async () => {
    try {
      setError('');
      let url = '/api/alerts';
      const params = {};
      if (statusFilter) params.status = statusFilter;
      if (riskFilter) params.risk_level = riskFilter;
      
      const response = await client.get(url, { params });
      // API returns { alerts: [...], total: N, limit: N }
      const alertsData = response.data.alerts || [];
      setAlerts(alertsData);
      
      // Auto-select the first alert if none is selected
      if (alertsData.length > 0 && !selectedAlert) {
        handleSelectAlert(alertsData[0]);
      }
    } catch (err) {
      console.error(err);
      setError('Failed to fetch correlation alerts list.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchAlerts();
  }, [statusFilter, riskFilter]);

  const handleSelectAlert = async (alert) => {
    setSelectedAlert(alert);
    setLoadingGraph(true);
    try {
      const response = await client.get(`/api/alerts/${alert.id}/graph`);
      setGraphData(response.data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoadingGraph(false);
    }
  };

  const handleStatusChange = async (alertId, newStatus) => {
    try {
      const response = await client.patch(`/api/alerts/${alertId}`, {
        status_update: newStatus
      });
      
      // Update alerts local state
      setAlerts(prev => prev.map(a => a.id === alertId ? { ...a, status: response.data.status } : a));
      
      // Update selected alert if it's the one being modified
      if (selectedAlert && selectedAlert.id === alertId) {
        setSelectedAlert(prev => ({ ...prev, status: response.data.status }));
      }
    } catch (err) {
      console.error(err);
      alert('Failed to update alert status.');
    }
  };

  const formatWindowTime = (seconds) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return mins > 0 ? `${mins}m ${secs}s` : `${secs}s`;
  };

  return (
    <div>
      <div className="header-row">
        <div>
          <h1 className="page-title">Correlation Alerts</h1>
          <p className="page-subtitle">Inspect correlated anomalies across identity access logs and transaction pipelines</p>
        </div>
        
        {/* Filters Panel */}
        <div style={{ display: 'flex', gap: '1rem' }}>
          <div>
            <select 
              className="form-input" 
              style={{ padding: '0.5rem 1rem', fontSize: '0.9rem', width: '160px' }}
              value={statusFilter} 
              onChange={e => setStatusFilter(e.target.value)}
            >
              <option value="">All Statuses</option>
              <option value="open">Open</option>
              <option value="investigating">Investigating</option>
              <option value="resolved">Resolved</option>
              <option value="false_positive">False Positive</option>
            </select>
          </div>
          <div>
            <select 
              className="form-input" 
              style={{ padding: '0.5rem 1rem', fontSize: '0.9rem', width: '160px' }}
              value={riskFilter} 
              onChange={e => setRiskFilter(e.target.value)}
            >
              <option value="">All Risk Levels</option>
              <option value="Critical">Critical</option>
              <option value="High">High</option>
              <option value="Medium">Medium</option>
              <option value="Low">Low</option>
            </select>
          </div>
        </div>
      </div>

      {error && (
        <div style={{ padding: '0.75rem 1rem', background: 'rgba(239, 68, 68, 0.15)', border: '1px solid rgba(239, 68, 68, 0.3)', borderRadius: '8px', color: '#f87171', marginBottom: '1.5rem' }}>
          {error}
        </div>
      )}

      {loading ? (
        <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '40vh', color: '#94a3b8' }}>
          <h3>Fetching correlation database records...</h3>
        </div>
      ) : (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '2rem' }}>
          
          {/* Alerts Table */}
          <div className="glass-panel table-container" style={{ padding: '0' }}>
            {alerts.length === 0 ? (
              <div style={{ padding: '3rem', textAlign: 'center', color: '#64748b' }}>
                <h4>No correlated alerts found matching filter criteria.</h4>
              </div>
            ) : (
              <table className="custom-table">
                <thead>
                  <tr>
                    <th>Alert ID</th>
                    <th>Customer ID</th>
                    <th>Risk Level</th>
                    <th>Risk Score</th>
                    <th>Correlation Gap</th>
                    <th>Status</th>
                    <th>Time Flagged</th>
                  </tr>
                </thead>
                <tbody>
                  {alerts.map((alert) => (
                    <tr 
                      key={alert.id} 
                      onClick={() => handleSelectAlert(alert)}
                      style={{ 
                        cursor: 'pointer',
                        background: selectedAlert && selectedAlert.id === alert.id ? 'rgba(99, 102, 241, 0.08)' : 'none',
                        borderLeft: selectedAlert && selectedAlert.id === alert.id ? '4px solid #6366f1' : '4px solid transparent'
                      }}
                    >
                      <td style={{ fontWeight: 600 }}>#AL-{alert.id}</td>
                      <td>{alert.customer_id}</td>
                      <td><RiskBadge level={alert.risk_level} /></td>
                      <td style={{ fontWeight: 600 }}>{(alert.correlated_score * 100).toFixed(0)}%</td>
                      <td>{formatWindowTime(alert.correlation_window_sec)}</td>
                      <td onClick={(e) => e.stopPropagation()}>
                        <select 
                          className="form-input"
                          style={{ 
                            padding: '0.25rem 0.5rem', 
                            fontSize: '0.85rem', 
                            width: '130px', 
                            backgroundColor: 'rgba(15, 23, 42, 0.8)',
                            borderColor: alert.status === 'open' ? 'rgba(239, 68, 68, 0.4)' : 'rgba(255,255,255,0.06)'
                          }}
                          value={alert.status} 
                          onChange={(e) => handleStatusChange(alert.id, e.target.value)}
                        >
                          <option value="open">🔴 Open</option>
                          <option value="investigating">🟡 Investigating</option>
                          <option value="resolved">🟢 Resolved</option>
                          <option value="false_positive">⚪ False Positive</option>
                        </select>
                      </td>
                      <td style={{ fontSize: '0.85rem', color: '#64748b' }}>
                        {new Date(alert.created_at || alert.transaction?.transaction_datetime).toLocaleString()}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            )}
          </div>

          {/* Selected Alert Detailed Panel */}
          {selectedAlert && (
            <div className="alert-detail-layout">
              
              {/* Explanatory Details */}
              <div className="glass-panel" style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', borderBottom: '1px solid var(--border-color)', paddingBottom: '1rem' }}>
                  <h3 style={{ color: 'white', fontSize: '1.25rem' }}>Incidence Inspector — Alert #AL-{selectedAlert.id}</h3>
                  <RiskBadge level={selectedAlert.risk_level} />
                </div>
                
                <div>
                  <h4 style={{ color: '#94a3b8', fontSize: '0.9rem', textTransform: 'uppercase', marginBottom: '0.5rem', letterSpacing: '0.5px' }}>Correlated Explanations</h4>
                  <div className="alert-explanation glass-panel" style={{ background: '#07090e', padding: '1rem' }}>
                    {selectedAlert.explanation}
                  </div>
                </div>

                <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1.5rem' }}>
                  {/* Transaction info */}
                  {selectedAlert.transaction && (
                    <div className="glass-panel" style={{ background: '#090d16', padding: '1rem' }}>
                      <h4 style={{ color: '#f97316', fontSize: '0.85rem', textTransform: 'uppercase', marginBottom: '0.75rem' }}>Transaction Stream</h4>
                      <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem', fontSize: '0.85rem' }}>
                        <div><span style={{ color: '#64748b' }}>Tx ID:</span> <span style={{ color: 'white', fontWeight: 600 }}>{selectedAlert.transaction.transaction_id}</span></div>
                        <div><span style={{ color: '#64748b' }}>Amount:</span> <span style={{ color: 'white', fontWeight: 600 }}>₹{selectedAlert.transaction.transaction_amount.toLocaleString()}</span></div>
                        <div><span style={{ color: '#64748b' }}>ML Score:</span> <span style={{ color: '#f97316', fontWeight: 600 }}>{(selectedAlert.transaction.prediction_score * 100).toFixed(1)}%</span></div>
                        <div>
                          <span style={{ color: '#64748b' }}>Rules:</span>{' '}
                          {selectedAlert.transaction.rules_triggered.map(rule => (
                            <span key={rule} style={{ padding: '1px 5px', background: 'rgba(249, 115, 22, 0.1)', color: '#f97316', border: '1px solid rgba(249, 115, 22, 0.2)', borderRadius: '4px', fontSize: '0.7rem', marginRight: '4px' }}>
                              {rule}
                            </span>
                          ))}
                        </div>
                      </div>
                    </div>
                  )}

                  {/* Security Telemetry info */}
                  {selectedAlert.security_event && (
                    <div className="glass-panel" style={{ background: '#090d16', padding: '1rem' }}>
                      <h4 style={{ color: '#eab308', fontSize: '0.85rem', textTransform: 'uppercase', marginBottom: '0.75rem' }}>Identity Telemetry</h4>
                      <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem', fontSize: '0.85rem' }}>
                        <div><span style={{ color: '#64748b' }}>Event:</span> <span style={{ color: 'white', fontWeight: 600 }}>{selectedAlert.security_event.event_type}</span></div>
                        <div><span style={{ color: '#64748b' }}>IP:</span> <span style={{ color: 'white', fontWeight: 600 }}>{selectedAlert.security_event.ip_address}</span></div>
                        <div><span style={{ color: '#64748b' }}>Location:</span> <span style={{ color: 'white', fontWeight: 600 }}>{selectedAlert.security_event.geo_location}</span></div>
                        <div><span style={{ color: '#64748b' }}>Trap Score:</span> <span style={{ color: '#eab308', fontWeight: 600 }}>{selectedAlert.security_event.security_trap_score.toFixed(1)}</span></div>
                        <div>
                          <span style={{ color: '#64748b' }}>Flags:</span>{' '}
                          {selectedAlert.security_event.hard_flags.map(flag => (
                            <span key={flag} style={{ padding: '1px 5px', background: 'rgba(234, 179, 8, 0.1)', color: '#eab308', border: '1px solid rgba(234, 179, 8, 0.2)', borderRadius: '4px', fontSize: '0.7rem', marginRight: '4px' }}>
                              {flag}
                            </span>
                          ))}
                          {selectedAlert.security_event.iso_anomaly_flag === 1 && (
                            <span style={{ padding: '1px 5px', background: 'rgba(168, 85, 247, 0.1)', color: '#a855f7', border: '1px solid rgba(168, 85, 247, 0.2)', borderRadius: '4px', fontSize: '0.7rem' }}>
                              ISOLATION_FOREST
                            </span>
                          )}
                        </div>
                      </div>
                    </div>
                  )}
                </div>
              </div>

              {/* D3 Network Graph */}
              <div className="glass-panel" style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
                <h3 style={{ color: 'white', fontSize: '1.25rem', borderBottom: '1px solid var(--border-color)', paddingBottom: '1rem' }}>Interactive Identity Link Graph</h3>
                {loadingGraph ? (
                  <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '400px', color: '#94a3b8' }}>
                    <h4>Generating Graph Force Matrix...</h4>
                  </div>
                ) : (
                  graphData && <NetworkGraph graphData={graphData} />
                )}
                <div style={{ display: 'flex', flexWrap: 'wrap', gap: '1rem', fontSize: '0.8rem', color: '#64748b', justifyContent: 'center' }}>
                  <div><span style={{ display: 'inline-block', width: '10px', height: '10px', borderRadius: '50%', backgroundColor: '#6366f1', marginRight: '4px' }}></span>Customer</div>
                  <div><span style={{ display: 'inline-block', width: '10px', height: '10px', borderRadius: '50%', backgroundColor: '#f97316', marginRight: '4px' }}></span>Transaction</div>
                  <div><span style={{ display: 'inline-block', width: '10px', height: '10px', borderRadius: '50%', backgroundColor: '#eab308', marginRight: '4px' }}></span>Telemetry Event</div>
                  <div><span style={{ display: 'inline-block', width: '10px', height: '10px', borderRadius: '50%', backgroundColor: '#ec4899', marginRight: '4px' }}></span>Device</div>
                  <div><span style={{ display: 'inline-block', width: '10px', height: '10px', borderRadius: '50%', backgroundColor: '#06b6d4', marginRight: '4px' }}></span>IP Address</div>
                  <div><span style={{ display: 'inline-block', width: '10px', height: '10px', borderRadius: '50%', backgroundColor: '#a855f7', marginRight: '4px' }}></span>Geo Location</div>
                </div>
              </div>

            </div>
          )}

        </div>
      )}
    </div>
  );
};

export default Alerts;
