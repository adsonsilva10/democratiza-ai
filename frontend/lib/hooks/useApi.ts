import { useState, useCallback } from 'react';

export interface ContractAnalysis {
  contract_type: string;
  risk_assessment: {
    overall_risk: 'ALTO_RISCO' | 'MEDIO_RISCO' | 'BAIXO_RISCO';
    risk_score: number;
  };
  problematic_clauses: Array<{
    clause_text: string;
    issue_type: string;
    severity: string;
    explanation: string;
    recommendation: string;
  }>;
  recommendations: string[];
  summary: string;
}

export const useApi = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const apiRequest = useCallback(async (url: string, options: RequestInit = {}) => {
    setLoading(true);
    setError(null);

    // Mock responses for development mode
    if (process.env.NODE_ENV === 'development') {
      await new Promise(resolve => setTimeout(resolve, 500)); // Simulate network delay
      
      // Mock subscription data
      if (url.includes('/api/v1/payments/user/subscription')) {
        setLoading(false);
        return {
          success: true,
          data: {
            subscription: {
              id: 'sub_mock_123',
              plan: 'premium',
              status: 'active',
              current_period_start: '2024-01-01T00:00:00Z',
              current_period_end: '2024-12-31T23:59:59Z',
              cancel_at_period_end: false
            }
          }
        };
      }

      // Mock other payment endpoints
      if (url.includes('/api/v1/payments/')) {
        setLoading(false);
        return {
          success: true,
          data: {
            message: 'Mock payment response'
          }
        };
      }

      // Mock contract endpoints  
      if (url.includes('/api/v1/contracts/')) {
        setLoading(false);
        return {
          success: true,
          data: {
            id: 'contract_mock_123',
            status: 'completed',
            analysis: { riskLevel: 'medium', summary: 'Mock analysis' }
          }
        };
      }

      // Default mock response
      setLoading(false);
      return {
        success: true,
        data: { message: 'Mock response' }
      };
    }

    try {
      const headers = {
        'Content-Type': 'application/json',
        ...options.headers,
      };

      const response = await fetch(url, {
        ...options,
        headers,
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || `Erro HTTP: ${response.status}`);
      }

      setLoading(false);
      return data;
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'Erro desconhecido';
      setError(errorMessage);
      setLoading(false);
      throw { error: errorMessage };
    }
  }, []);

  return { apiRequest, loading, error };
};

export const useContractAnalysis = () => {
  const { apiRequest, loading, error } = useApi();

  const analyzeContract = useCallback(async (text: string): Promise<ContractAnalysis> => {
    const response = await apiRequest('/api/v1/demo/analyze-text', {
      method: 'POST',
      body: JSON.stringify({ text }),
    });
    return response;
  }, [apiRequest]);

  return { analyzeContract, loading, error };
};

export const useChat = () => {
  const { apiRequest, loading, error } = useApi();

  const sendMessage = useCallback(async (
    message: string, 
    agentType: string = 'general', 
    contractId?: string
  ) => {
    const params = new URLSearchParams({
      question: message,
      agent_type: agentType
    });
    
    if (contractId) {
      params.append('contract_id', contractId);
    }
    
    const response = await apiRequest(`/api/v1/demo/chat?${params}`, {
      method: 'GET',
    });
    return response;
  }, [apiRequest]);

  return { sendMessage, loading, error };
};

export interface AgentInfo {
  name: string;
  icon: string;
  description: string;
  areas: string[];
  color: string;
}

export const useAgents = () => {
  const { apiRequest, loading, error } = useApi();

  const getAvailableAgents = useCallback(async (): Promise<Record<string, AgentInfo>> => {
    const response = await apiRequest('/api/v1/demo/agents', {
      method: 'GET',
    });
    return response.agents;
  }, [apiRequest]);

  const classifyContract = useCallback(async (text: string, contractType?: string) => {
    const params = new URLSearchParams();
    if (text) params.append('text', text);
    if (contractType) params.append('contract_type', contractType);
    
    const response = await apiRequest(`/api/v1/demo/classify-contract?${params}`, {
      method: 'GET',
    });
    return response;
  }, [apiRequest]);

  return { getAvailableAgents, classifyContract, loading, error };
};
