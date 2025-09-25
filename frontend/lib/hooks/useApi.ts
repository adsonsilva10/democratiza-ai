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
