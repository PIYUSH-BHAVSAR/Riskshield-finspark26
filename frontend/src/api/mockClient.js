/**
 * RiskShield-BFSI-X — Mock API Client
 * Intercepts all API calls and returns mock data with simulated network delay.
 * Drop-in replacement for client.js — no backend needed.
 */

import {
  MOCK_ANALYTICS,
  MOCK_ALERTS,
  MOCK_GRAPHS,
} from './mockData';

// In-memory mutable state so status updates persist during the session
let alertsState = MOCK_ALERTS.map(a => ({ ...a }));

// Simulated network delay (ms)
const delay = (ms = 400) => new Promise(resolve => setTimeout(resolve, ms));

// Wrap response to match axios shape: { data: ... }
const ok = (data) => ({ data });

// ===== ROUTE MATCHER =====
const mockClient = {

  get: async (url, config = {}) => {
    await delay();

    // GET /api/analytics
    if (url === '/api/analytics') {
      return ok(MOCK_ANALYTICS);
    }

    // GET /api/alerts
    if (url === '/api/alerts') {
      const params = config?.params || {};
      let filtered = [...alertsState];

      if (params.risk_level && params.risk_level !== 'All') {
        filtered = filtered.filter(a => a.risk_level === params.risk_level);
      }
      if (params.status) {
        filtered = filtered.filter(a => a.status === params.status);
      }

      return ok({ alerts: filtered, total: filtered.length, limit: 50 });
    }

    // GET /api/alerts/:id/graph
    const graphMatch = url.match(/^\/api\/alerts\/(\d+)\/graph$/);
    if (graphMatch) {
      const id = parseInt(graphMatch[1]);
      const graph = MOCK_GRAPHS[id] || { nodes: [], edges: [], alert_id: id };
      return ok(graph);
    }

    // GET /api/health
    if (url === '/api/health') {
      return ok({ status: 'healthy', service: 'RiskShield-BFSI-X', version: '1.0.0', database: 'connected', environment: 'mock' });
    }

    console.warn(`[mockClient] Unhandled GET: ${url}`);
    return ok({});
  },

  post: async (url, data) => {
    await delay(600);

    // POST /api/auth/login
    if (url === '/api/auth/login') {
      // data is URLSearchParams in Login.jsx
      const username = typeof data?.get === 'function' ? data.get('username') : data?.username;
      const password = typeof data?.get === 'function' ? data.get('password') : data?.password;

      if (username === 'admin@riskshield.com' && password === 'admin123') {
        return ok({
          access_token: 'mock-token-riskshield-bfsi-x',
          token_type: 'bearer',
          user: { email: 'admin@riskshield.com', role: 'analyst' },
        });
      }
      // Simulate 401
      const err = new Error('Invalid email or password');
      err.response = { status: 401, data: { detail: 'Invalid email or password' } };
      throw err;
    }

    // POST /api/run-correlation
    if (url === '/api/run-correlation') {
      // Simulate finding 2 new alerts
      return ok({ new_alerts_created: 2, correlation_window_sec: 900, status: 'completed' });
    }

    // POST /api/seed-data
    if (url === '/api/seed-data') {
      return ok({ transactions_created: 15, security_events_created: 10, alerts_created: 8, message: 'Test data seeded (mock)' });
    }

    console.warn(`[mockClient] Unhandled POST: ${url}`);
    return ok({});
  },

  patch: async (url, data) => {
    await delay(300);

    // PATCH /api/alerts/:id
    const alertMatch = url.match(/^\/api\/alerts\/(\d+)$/);
    if (alertMatch) {
      const id = parseInt(alertMatch[1]);
      const newStatus = data?.status_update;

      const idx = alertsState.findIndex(a => a.id === id);
      if (idx !== -1 && newStatus) {
        alertsState[idx] = { ...alertsState[idx], status: newStatus };
        return ok({ id, status: newStatus, message: 'Alert status updated' });
      }
      const err = new Error('Alert not found');
      err.response = { status: 404, data: { detail: 'Alert not found' } };
      throw err;
    }

    console.warn(`[mockClient] Unhandled PATCH: ${url}`);
    return ok({});
  },
};

export default mockClient;
