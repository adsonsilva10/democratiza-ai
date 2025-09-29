// Mock API client for development
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

  async uploadContract(file: File, title?: string): Promise<{ data: Contract }> {
    // Simulate upload with delay
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    const contractId = Math.random().toString(36).substr(2, 9)
    
    return {
      data: {
        id: contractId,
        title: title || file.name,
        status: 'processing'
      }
    }
  }

  async getContract(contractId: string): Promise<{ data: Contract }> {
    // Simulate API delay
    await new Promise(resolve => setTimeout(resolve, 500))
    
    // Simulate processing completion after some time
    const isCompleted = Math.random() > 0.3
    
    return {
      data: {
        id: contractId,
        title: 'Contract Title',
        status: isCompleted ? 'completed' : 'processing',
        analysis: isCompleted ? {
          riskLevel: 'medium',
          summary: 'Análise concluída com sucesso'
        } : undefined
      }
    }
  }

  async analyzeContract(contractId: string): Promise<{ data: any }> {
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    return {
      data: {
        riskLevel: 'medium',
        clauses: [],
        summary: 'Análise mock'
      }
    }
  }
}

const apiClient = new ApiClient()
export default apiClient