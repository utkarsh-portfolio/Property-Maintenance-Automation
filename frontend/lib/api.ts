/**
 * API client for Property Maintenance Automation backend
 */

const API_URL = process.env.API_URL || "http://localhost:8000/api/v1";

// Types
export interface Customer {
  id: number;
  first_name: string;
  last_name: string;
  email: string;
  phone: string;
  address: string;
  city: string;
  state: string;
  zip_code: string;
  property_type: string;
  preferred_contact: string;
  is_active: boolean;
  created_at: string;
}

export interface Lead {
  id: number;
  customer_id: number;
  service_type: string;
  description: string;
  urgency: string;
  status: string;
  source: string;
  estimated_value: number | null;
  actual_value: number | null;
  follow_up_count: number;
  created_at: string;
}

export interface Appointment {
  id: number;
  customer_id: number;
  lead_id: number | null;
  scheduled_start: string;
  scheduled_end: string;
  service_type: string;
  status: string;
  technician_name: string | null;
  customer_confirmed: boolean;
  created_at: string;
}

export interface LeadStats {
  total_leads: number;
  new_leads: number;
  qualified_leads: number;
  won_leads: number;
  lost_leads: number;
  conversion_rate: number;
  total_value: number;
}

export interface ChatResponse {
  conversation_id: number;
  response: string;
  intent: string | null;
  suggested_actions: string[];
}

// API Functions
async function fetchAPI<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  const response = await fetch(`${API_URL}${endpoint}`, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...options.headers,
    },
  });

  if (!response.ok) {
    throw new Error(`API error: ${response.status}`);
  }

  return response.json();
}

// Customers
export const customersAPI = {
  list: (params?: { page?: number; search?: string }) =>
    fetchAPI<{ items: Customer[]; total: number }>(
      `/customers?${new URLSearchParams(params as Record<string, string>)}`
    ),
  get: (id: number) => fetchAPI<Customer>(`/customers/${id}`),
  create: (data: Partial<Customer>) =>
    fetchAPI<Customer>("/customers", {
      method: "POST",
      body: JSON.stringify(data),
    }),
  update: (id: number, data: Partial<Customer>) =>
    fetchAPI<Customer>(`/customers/${id}`, {
      method: "PATCH",
      body: JSON.stringify(data),
    }),
};

// Leads
export const leadsAPI = {
  list: (params?: { page?: number; status?: string }) =>
    fetchAPI<{ items: Lead[]; total: number }>(
      `/leads?${new URLSearchParams(params as Record<string, string>)}`
    ),
  get: (id: number) => fetchAPI<Lead>(`/leads/${id}`),
  stats: () => fetchAPI<LeadStats>("/leads/stats"),
  create: (data: Partial<Lead>) =>
    fetchAPI<Lead>("/leads", {
      method: "POST",
      body: JSON.stringify(data),
    }),
  update: (id: number, data: Partial<Lead>) =>
    fetchAPI<Lead>(`/leads/${id}`, {
      method: "PATCH",
      body: JSON.stringify(data),
    }),
};

// Appointments
export const appointmentsAPI = {
  list: (params?: { page?: number; status?: string; date_from?: string }) =>
    fetchAPI<{ items: Appointment[]; total: number }>(
      `/appointments?${new URLSearchParams(params as Record<string, string>)}`
    ),
  today: () => fetchAPI<Appointment[]>("/appointments/today"),
  get: (id: number) => fetchAPI<Appointment>(`/appointments/${id}`),
  create: (data: Partial<Appointment>) =>
    fetchAPI<Appointment>("/appointments", {
      method: "POST",
      body: JSON.stringify(data),
    }),
  confirm: (id: number) =>
    fetchAPI<Appointment>(`/appointments/${id}/confirm`, { method: "POST" }),
  cancel: (id: number) =>
    fetchAPI<Appointment>(`/appointments/${id}/cancel`, { method: "POST" }),
};

// Chat
export const chatAPI = {
  send: (message: string, conversationId?: number) =>
    fetchAPI<ChatResponse>("/conversations/chat", {
      method: "POST",
      body: JSON.stringify({
        message,
        conversation_id: conversationId,
        channel: "web_chat",
      }),
    }),
};
