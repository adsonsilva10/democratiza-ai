// Real API client for backend connection
export interface Contract {
  id: string
  title: string
  name?: string
  type?: string
  status: 'uploaded' | 'processing' | 'completed' | 'error'
  created_at?: string
  analysis?: any
}

class ApiClient {
  private baseURL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1'

  private async request(endpoint: string, options: RequestInit = {}) {
    const url = `${this.baseURL}${endpoint}`
    
    // Get token from localStorage
    const token = typeof window !== 'undefined' ? localStorage.getItem('auth-token') : null
    
    const headers: Record<string, string> = {
      'Content-Type': 'application/json',
      ...(options.headers as Record<string, string>),
    }
    
    if (token) {
      headers['Authorization'] = `Bearer ${token}`
    }
    
    const response = await fetch(url, {
      ...options,
      headers,
    })
    
    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: 'Request failed' }))
      throw new Error(error.detail || `HTTP ${response.status}`)
    }
    
    return response.json()
  }

  async uploadContract(file: File, title?: string): Promise<{ data: Contract }> {
    const formData = new FormData()
    formData.append('file', file)
    if (title) formData.append('title', title)
    
    const response = await this.request('/contracts', {
      method: 'POST',
      headers: {}, // FormData sets its own Content-Type
      body: formData,
    })
    
    return { data: response }
  }

  async getContract(contractId: string): Promise<{ data: Contract }> {
    const response = await this.request(`/contracts/${contractId}`)
    return { data: response }
  }

  async listContracts(): Promise<{ data: Contract[] }> {
    const response = await this.request('/contracts')
    return { data: response }
  }

  async analyzeContract(contractId: string): Promise<{ data: any }> {
    const response = await this.request(`/contracts/${contractId}/analyze`, {
      method: 'POST',
    })
    return { data: response }
  }

  async deleteContract(contractId: string): Promise<void> {
    await this.request(`/contracts/${contractId}`, {
      method: 'DELETE',
    })
  }
}

const apiClient = new ApiClient()
export default apiClient