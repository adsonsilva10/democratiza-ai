// React hooks para integração com API
import { useState, useCallback } from 'react'
import apiClient, { Contract, ChatSession, ChatMessage } from '../api'

export const useAuth = () => {
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const login = useCallback(async (email: string, password: string) => {
    setIsLoading(true)
    setError(null)
    
    try {
      const response = await apiClient.login({ email, password })
      return response.data
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Erro no login'
      setError(errorMessage)
      throw err
    } finally {
      setIsLoading(false)
    }
  }, [])

  const register = useCallback(async (name: string, email: string, password: string) => {
    setIsLoading(true)
    setError(null)
    
    try {
      const response = await apiClient.register({ email, password, name })
      return response.data
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Erro no registro'
      setError(errorMessage)
      throw err
    } finally {
      setIsLoading(false)
    }
  }, [])

  const logout = useCallback(async () => {
    try {
      await apiClient.logout()
      apiClient.clearToken()
    } catch (err) {
      console.error('Erro no logout:', err)
    }
  }, [])

  return {
    login,
    register,
    logout,
    isLoading,
    error,
    clearError: () => setError(null)
  }
}

export const useContracts = () => {
  const [contracts, setContracts] = useState<Contract[]>([])
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const fetchContracts = useCallback(async () => {
    setIsLoading(true)
    setError(null)
    
    try {
      const response = await apiClient.getContracts()
      setContracts(response.data)
      return response.data
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Erro ao carregar contratos'
      setError(errorMessage)
      throw err
    } finally {
      setIsLoading(false)
    }
  }, [])

  const uploadContract = useCallback(async (file: File) => {
    setIsLoading(true)
    setError(null)
    
    try {
      const response = await apiClient.uploadContract(file)
      // Atualizar lista local
      setContracts(prev => [...prev, response.data])
      return response.data
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Erro no upload'
      setError(errorMessage)
      throw err
    } finally {
      setIsLoading(false)
    }
  }, [])

  const deleteContract = useCallback(async (contractId: string) => {
    try {
      await apiClient.deleteContract(contractId)
      // Remover da lista local
      setContracts(prev => prev.filter(c => c.id !== contractId))
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Erro ao deletar contrato'
      setError(errorMessage)
      throw err
    }
  }, [])

  const analyzeContract = useCallback(async (contractId: string) => {
    setIsLoading(true)
    setError(null)
    
    try {
      const response = await apiClient.analyzeContract(contractId)
      // Atualizar contrato na lista local
      setContracts(prev => 
        prev.map(c => c.id === contractId ? response.data : c)
      )
      return response.data
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Erro na análise'
      setError(errorMessage)
      throw err
    } finally {
      setIsLoading(false)
    }
  }, [])

  return {
    contracts,
    fetchContracts,
    uploadContract,
    deleteContract,
    analyzeContract,
    isLoading,
    error,
    clearError: () => setError(null)
  }
}

export const useChat = () => {
  const [chatSessions, setChatSessions] = useState<ChatSession[]>([])
  const [currentSession, setCurrentSession] = useState<ChatSession | null>(null)
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const createChatSession = useCallback(async (contractId: string) => {
    setIsLoading(true)
    setError(null)
    
    try {
      const response = await apiClient.createChatSession(contractId)
      const newSession = response.data
      setChatSessions(prev => [...prev, newSession])
      setCurrentSession(newSession)
      return newSession
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Erro ao criar sessão'
      setError(errorMessage)
      throw err
    } finally {
      setIsLoading(false)
    }
  }, [])

  const sendMessage = useCallback(async (sessionId: string, content: string) => {
    if (!currentSession || currentSession.id !== sessionId) return

    setIsLoading(true)
    setError(null)
    
    try {
      const response = await apiClient.sendMessage(sessionId, content)
      const newMessage = response.data
      
      // Atualizar sessão atual com nova mensagem
      setCurrentSession(prev => prev ? {
        ...prev,
        messages: [...prev.messages, newMessage]
      } : null)
      
      return newMessage
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Erro ao enviar mensagem'
      setError(errorMessage)
      throw err
    } finally {
      setIsLoading(false)
    }
  }, [currentSession])

  const getChatSessions = useCallback(async (contractId: string) => {
    setIsLoading(true)
    setError(null)
    
    try {
      const response = await apiClient.getChatSessions(contractId)
      setChatSessions(response.data)
      return response.data
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Erro ao carregar sessões'
      setError(errorMessage)
      throw err
    } finally {
      setIsLoading(false)
    }
  }, [])

  return {
    chatSessions,
    currentSession,
    createChatSession,
    sendMessage,
    getChatSessions,
    setCurrentSession,
    isLoading,
    error,
    clearError: () => setError(null)
  }
}

// Hook para verificar autenticação
export const useIsAuthenticated = () => {
  const [isAuthenticated, setIsAuthenticated] = useState(false)
  
  const checkAuth = useCallback(async () => {
    try {
      await apiClient.getCurrentUser()
      setIsAuthenticated(true)
    } catch {
      setIsAuthenticated(false)
      apiClient.clearToken()
    }
  }, [])

  return {
    isAuthenticated,
    checkAuth
  }
}