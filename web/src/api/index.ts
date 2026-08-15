import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || '/api/v1';
const IS_DEMO = import.meta.env.VITE_DEMO_MODE === 'true';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
});

export type Envelope<T> = {
  success: boolean;
  data: T;
  meta: {
    request_id: string;
    timestamp: string;
  };
  error: null | {
    code: string;
    message: string;
    details: any;
  };
};

export type Farm = {
  id: string;
  user_id: string;
  name: string;
  crop: string | null;
  sowing_date: string | null;
  area_m2: number;
  status: 'PENDING' | 'VERIFIED' | 'UNAVAILABLE';
};

export type Claim = {
  id: string;
  policy_id: string;
  incident_date: string;
  event_type: string;
  description: string;
  status: 'SUBMITTED' | 'AI_ASSESSED' | 'UNDER_REVIEW' | 'APPROVED' | 'REJECTED';
  damage_pct: number | null;
  ai_confidence: number | null;
};

// Mock Data
const MOCK_FARMS: Farm[] = [
  { id: '1', user_id: '1', name: 'North Field', crop: 'Wheat', sowing_date: '2026-06-01', area_m2: 25000, status: 'VERIFIED' },
  { id: '2', user_id: '1', name: 'East Plot', crop: 'Corn', sowing_date: '2026-05-15', area_m2: 12000, status: 'PENDING' },
];

const MOCK_CLAIMS: Claim[] = [
  { id: '1', policy_id: 'p1', incident_date: '2026-08-10', event_type: 'flood', description: 'Heavy rains flooded the north field', status: 'AI_ASSESSED', damage_pct: 85, ai_confidence: 0.92 },
  { id: '2', policy_id: 'p2', incident_date: '2026-08-12', event_type: 'pest', description: 'Locust swarm', status: 'SUBMITTED', damage_pct: null, ai_confidence: null },
];

export type Policy = {
  id: string;
  farm_id: string;
  premium_amount: number;
  coverage_amount: number;
  status: 'ACTIVE' | 'EXPIRED' | 'PENDING';
  start_date: string;
  end_date: string;
};

export type PolicyVerification = {
  is_verified: boolean;
  blockchain_hash: string;
  timestamp: string;
  network: string;
};

const MOCK_POLICIES: Policy[] = [
  { id: 'p1', farm_id: '1', premium_amount: 1500, coverage_amount: 25000, status: 'ACTIVE', start_date: '2026-01-01', end_date: '2026-12-31' },
  { id: 'p2', farm_id: '2', premium_amount: 800, coverage_amount: 12000, status: 'PENDING', start_date: '2026-06-01', end_date: '2027-05-31' },
];

function createMockResponse<T>(data: T): Envelope<T> {
  return {
    success: true,
    data,
    meta: { request_id: 'mock-uuid', timestamp: new Date().toISOString() },
    error: null,
  };
}

export type User = {
  id: string;
  email: string;
  name: string;
  role: 'ADMIN' | 'INSURER' | 'FARMER';
};

export type Notification = {
  id: string;
  user_id: string;
  title: string;
  message: string;
  is_read: boolean;
  created_at: string;
};

export const api = {
  login: async (credentials: any): Promise<Envelope<{ access_token: string; refresh_token: string }>> => {
    if (IS_DEMO) return createMockResponse({ access_token: 'mock-token', refresh_token: 'mock-refresh' });
    const res = await apiClient.post('/auth/login', credentials);
    return res.data;
  },
  register: async (userData: any): Promise<Envelope<{ user: User; access_token: string }>> => {
    if (IS_DEMO) return createMockResponse({ user: { id: '1', email: userData.email, name: userData.name, role: 'ADMIN' }, access_token: 'mock-token' });
    const res = await apiClient.post('/auth/register', userData);
    return res.data;
  },
  getMe: async (): Promise<Envelope<User>> => {
    if (IS_DEMO) return createMockResponse({ id: '1', email: 'admin@agrishield.com', name: 'Admin User', role: 'ADMIN' });
    const res = await apiClient.get('/auth/me');
    return res.data;
  },
  getNotifications: async (): Promise<Envelope<Notification[]>> => {
    if (IS_DEMO) return createMockResponse([
      { id: '1', user_id: '1', title: 'New Claim Filed', message: 'Farm #1 filed a flood claim.', is_read: false, created_at: new Date().toISOString() }
    ]);
    const res = await apiClient.get('/notifications');
    return res.data;
  },
  getFarms: async (): Promise<Envelope<Farm[]>> => {
    if (IS_DEMO) return createMockResponse(MOCK_FARMS);
    const res = await apiClient.get('/farms');
    return res.data;
  },
  getClaims: async (): Promise<Envelope<Claim[]>> => {
    if (IS_DEMO) return createMockResponse(MOCK_CLAIMS);
    const res = await apiClient.get('/claims');
    return res.data;
  },
  reviewClaim: async (id: string, action: 'APPROVE' | 'REJECT'): Promise<Envelope<Claim>> => {
    if (IS_DEMO) {
      const claim = MOCK_CLAIMS.find(c => c.id === id);
      if (!claim) throw new Error('Claim not found');
      const updated: Claim = { ...claim, status: action === 'APPROVE' ? 'APPROVED' : 'REJECTED' };
      return createMockResponse(updated);
    }
    const res = await apiClient.post(`/claims/${id}/review`, { action });
    return res.data;
  },
  getPolicies: async (): Promise<Envelope<Policy[]>> => {
    if (IS_DEMO) return createMockResponse(MOCK_POLICIES);
    const res = await apiClient.get('/insurance/policies');
    return res.data;
  },
  verifyPolicy: async (id: string): Promise<Envelope<PolicyVerification>> => {
    if (IS_DEMO) {
      return createMockResponse({
        is_verified: true,
        blockchain_hash: `0x${Math.random().toString(16).substring(2, 15).padEnd(64, '0')}`,
        timestamp: new Date().toISOString(),
        network: 'Polygon Mumbai'
      });
    }
    const res = await apiClient.get(`/insurance/policies/${id}/verification`);
    return res.data;
  }
};
