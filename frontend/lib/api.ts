// API Client
interface ApiResponse<T> {
  data: T;
  message?: string;
  error?: string;
}

interface LoginRequest {
  email: string;
  password: string;
}

interface RegisterRequest {
  email: string;
  password: string;
  name: string;
}

interface AuthResponse {
  token: string;
  user: {
    id: string;
    email: string;
    name: string;
  };
}

interface Contract {
  id: string;
  name: string;
  type: string;
  status: string;
  analysis?: {
    summary: string;
    risks: Array<{
      level: 'high' | 'medium' | 'low';
      description: string;
      clause?: string;
    }>;
    clauses: Array<{
      type: string;
      content: string;
      risk_level: 'high' | 'medium' | 'low';
    }>;
    recommendations: string[];
  };
  created_at: string;
  updated_at: string;
}

interface ChatMessage {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: string;
}

interface ChatSession {
  id: string;
  contract_id: string;
  messages: ChatMessage[];
  created_at: string;
  updated_at: string;
}

class ApiClient {
  private baseURL: string;
  private token: string | null = null;

  constructor() {
    this.baseURL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
    this.token = typeof window !== 'undefined' ? localStorage.getItem('token') : null;
  }

  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<ApiResponse<T>> {
    const url = `${this.baseURL}${endpoint}`;
    
    const headers: Record<string, string> = {
      'Content-Type': 'application/json',
    };

    if (options.headers) {
      Object.assign(headers, options.headers);
    }

    if (this.token) {
      headers.Authorization = `Bearer ${this.token}`;
    }

    try {
      const response = await fetch(url, {
        ...options,
        headers,
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.message || `HTTP error! status: ${response.status}`);
      }

      return data;
    } catch (error) {
      console.error('API request failed:', error);
      throw error;
    }
  }

  setToken(token: string) {
    this.token = token;
    if (typeof window !== 'undefined') {
      localStorage.setItem('token', token);
    }
  }

  clearToken() {
    this.token = null;
    if (typeof window !== 'undefined') {
      localStorage.removeItem('token');
    }
  }

  // Auth endpoints
  async login(credentials: LoginRequest): Promise<ApiResponse<AuthResponse>> {
    // FastAPI OAuth2 expects form data for token endpoint
    const formData = new FormData();
    formData.append('username', credentials.email);
    formData.append('password', credentials.password);

    const response = await fetch(`${this.baseURL}/api/v1/auth/token`, {
      method: 'POST',
      body: formData,
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.detail || `HTTP error! status: ${response.status}`);
    }

    // Set token after successful login
    this.setToken(data.access_token);

    return {
      data: {
        token: data.access_token,
        user: data.user || { id: '', email: credentials.email, name: '' }
      }
    };
  }

  async register(userData: RegisterRequest): Promise<ApiResponse<AuthResponse>> {
    return this.request<AuthResponse>('/api/v1/auth/register', {
      method: 'POST',
      body: JSON.stringify(userData),
    });
  }

  async logout(): Promise<ApiResponse<{}>> {
    const response = await this.request<{}>('/api/v1/auth/logout', {
      method: 'POST',
    });
    this.clearToken();
    return response;
  }

  async getCurrentUser(): Promise<ApiResponse<AuthResponse['user']>> {
    return this.request<AuthResponse['user']>('/api/v1/auth/me');
  }

  // Contract endpoints
  async getContracts(): Promise<ApiResponse<Contract[]>> {
    return this.request<Contract[]>('/api/v1/contracts');
  }

  async getContract(id: string): Promise<ApiResponse<Contract>> {
    return this.request<Contract>(`/api/v1/contracts/${id}`);
  }

  async uploadContract(file: File): Promise<ApiResponse<Contract>> {
    const formData = new FormData();
    formData.append('file', file);

    const headers: Record<string, string> = {};
    if (this.token) {
      headers.Authorization = `Bearer ${this.token}`;
    }

    try {
      const response = await fetch(`${this.baseURL}/api/v1/contracts/upload`, {
        method: 'POST',
        headers,
        body: formData,
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.message || `HTTP error! status: ${response.status}`);
      }

      return data;
    } catch (error) {
      console.error('Contract upload failed:', error);
      throw error;
    }
  }

  async analyzeContract(contractId: string): Promise<ApiResponse<Contract>> {
    return this.request<Contract>(`/api/v1/contracts/${contractId}/analyze`, {
      method: 'POST',
    });
  }

  async deleteContract(id: string): Promise<ApiResponse<{}>> {
    return this.request<{}>(`/api/v1/contracts/${id}`, {
      method: 'DELETE',
    });
  }

  // Chat endpoints
  async getChatSessions(contractId: string): Promise<ApiResponse<ChatSession[]>> {
    return this.request<ChatSession[]>(`/api/v1/chat/sessions?contract_id=${contractId}`);
  }

  async createChatSession(contractId: string): Promise<ApiResponse<ChatSession>> {
    return this.request<ChatSession>('/api/v1/chat/sessions', {
      method: 'POST',
      body: JSON.stringify({ contract_id: contractId }),
    });
  }

  async sendMessage(
    sessionId: string,
    message: string
  ): Promise<ApiResponse<ChatMessage>> {
    return this.request<ChatMessage>(`/api/v1/chat/sessions/${sessionId}/messages`, {
      method: 'POST',
      body: JSON.stringify({ content: message }),
    });
  }

  async getChatMessages(sessionId: string): Promise<ApiResponse<ChatMessage[]>> {
    return this.request<ChatMessage[]>(`/api/v1/chat/sessions/${sessionId}/messages`);
  }

  // Payment endpoints
  async createPaymentIntent(amount: number): Promise<ApiResponse<{ client_secret: string }>> {
    return this.request<{ client_secret: string }>('/api/v1/payments/create-intent', {
      method: 'POST',
      body: JSON.stringify({ amount }),
    });
  }

  async confirmPayment(paymentIntentId: string): Promise<ApiResponse<{}>> {
    return this.request<{}>('/api/v1/payments/confirm', {
      method: 'POST',
      body: JSON.stringify({ payment_intent_id: paymentIntentId }),
    });
  }
}

// Create and export singleton instance
const apiClient = new ApiClient();
export default apiClient;

// Export types for use in components
export type {
  ApiResponse,
  LoginRequest,
  RegisterRequest,
  AuthResponse,
  Contract,
  ChatMessage,
  ChatSession,
};
