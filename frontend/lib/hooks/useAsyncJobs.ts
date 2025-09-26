'use client'

import { useState, useEffect, useCallback, useRef } from 'react'

export interface JobProgress {
  stage: string
  progress: number // 0.0 to 1.0
  message: string
  timestamp: string
  details?: Record<string, any>
}

export interface ContractJob {
  job_id: string
  status: 'pending' | 'processing' | 'completed' | 'failed' | 'cancelled'
  created_at: string
  current_stage: string
  progress?: number
  message?: string
  estimated_completion?: string
  error_message?: string
  result?: Record<string, any>
  job_type: string
  contract_title: string
}

export interface WebSocketMessage {
  type: 'connection_established' | 'job_progress' | 'job_status_changed' | 'job_completed' | 'error' | 'pong' | 'active_jobs' | 'job_subscribed'
  job_id?: string
  job?: ContractJob
  jobs?: ContractJob[]
  stage?: string
  progress?: number
  message?: string
  status?: string
  error?: string
  estimated_completion?: string
  result?: Record<string, any>
  user_id?: string
  timestamp?: string
}

interface CreateJobRequest {
  job_type: 'contract_analysis' | 'image_processing' | 'document_ocr' | 'full_pipeline'
  files: string[]
  contract_title: string
  user_email: string
  options?: Record<string, any>
}

interface UseAsyncJobsReturn {
  // Job Management
  createJob: (request: CreateJobRequest) => Promise<string>
  getJob: (jobId: string) => Promise<ContractJob | null>
  getUserJobs: () => Promise<ContractJob[]>
  cancelJob: (jobId: string) => Promise<boolean>
  getJobResult: (jobId: string) => Promise<any>
  
  // Real-time tracking
  jobs: Record<string, ContractJob>
  isConnected: boolean
  connectionError: string | null
  
  // WebSocket controls
  connect: () => void
  disconnect: () => void
  subscribeToJob: (jobId: string) => void
  
  // State
  isCreatingJob: boolean
  error: string | null
}

export function useAsyncJobs(userId: string = 'demo_user'): UseAsyncJobsReturn {
  const [jobs, setJobs] = useState<Record<string, ContractJob>>({})
  const [isConnected, setIsConnected] = useState(false)
  const [connectionError, setConnectionError] = useState<string | null>(null)
  const [isCreatingJob, setIsCreatingJob] = useState(false)
  const [error, setError] = useState<string | null>(null)
  
  const wsRef = useRef<WebSocket | null>(null)
  const reconnectTimeoutRef = useRef<NodeJS.Timeout | null>(null)
  const heartbeatIntervalRef = useRef<NodeJS.Timeout | null>(null)

  const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1'
  const wsUrl = apiUrl.replace('http', 'ws').replace('/api/v1', '/api/v1/async')

  // WebSocket connection management
  const connect = useCallback(() => {
    if (wsRef.current?.readyState === WebSocket.OPEN) {
      return
    }

    try {
      const ws = new WebSocket(`${wsUrl}/ws/${userId}`)
      wsRef.current = ws

      ws.onopen = () => {
        console.log('WebSocket conectado')
        setIsConnected(true)
        setConnectionError(null)
        
        // Iniciar heartbeat
        heartbeatIntervalRef.current = setInterval(() => {
          if (ws.readyState === WebSocket.OPEN) {
            ws.send(JSON.stringify({ type: 'ping' }))
          }
        }, 30000) // Ping a cada 30 segundos

        // Solicitar jobs ativos
        ws.send(JSON.stringify({ type: 'get_active_jobs' }))
      }

      ws.onmessage = (event) => {
        try {
          const message: WebSocketMessage = JSON.parse(event.data)
          handleWebSocketMessage(message)
        } catch (error) {
          console.error('Erro ao parsear mensagem WebSocket:', error)
        }
      }

      ws.onclose = (event) => {
        console.log('WebSocket desconectado:', event.code, event.reason)
        setIsConnected(false)
        
        // Cleanup heartbeat
        if (heartbeatIntervalRef.current) {
          clearInterval(heartbeatIntervalRef.current)
          heartbeatIntervalRef.current = null
        }

        // Tentar reconectar em 5 segundos se não foi fechamento intencional
        if (event.code !== 1000) {
          setConnectionError('Conexão perdida. Tentando reconectar...')
          reconnectTimeoutRef.current = setTimeout(() => {
            connect()
          }, 5000)
        }
      }

      ws.onerror = (error) => {
        console.error('Erro WebSocket:', error)
        setConnectionError('Erro na conexão WebSocket')
      }

    } catch (error) {
      console.error('Erro ao conectar WebSocket:', error)
      setConnectionError('Falha ao estabelecer conexão')
    }
  }, [userId, wsUrl])

  const disconnect = useCallback(() => {
    if (reconnectTimeoutRef.current) {
      clearTimeout(reconnectTimeoutRef.current)
      reconnectTimeoutRef.current = null
    }

    if (heartbeatIntervalRef.current) {
      clearInterval(heartbeatIntervalRef.current)
      heartbeatIntervalRef.current = null
    }

    if (wsRef.current) {
      wsRef.current.close(1000, 'Desconexão intencional')
      wsRef.current = null
    }

    setIsConnected(false)
    setConnectionError(null)
  }, [])

  // Handle WebSocket messages
  const handleWebSocketMessage = useCallback((message: WebSocketMessage) => {
    switch (message.type) {
      case 'connection_established':
        console.log('Conexão WebSocket estabelecida:', message.user_id)
        break

      case 'job_progress':
        if (message.job_id) {
          setJobs(prev => ({
            ...prev,
            [message.job_id!]: {
              ...prev[message.job_id!],
              current_stage: message.stage || prev[message.job_id!]?.current_stage,
              progress: message.progress,
              message: message.message,
              estimated_completion: message.estimated_completion
            }
          }))
        }
        break

      case 'job_status_changed':
        if (message.job_id && message.status) {
          setJobs(prev => ({
            ...prev,
            [message.job_id!]: {
              ...prev[message.job_id!],
              status: message.status as ContractJob['status'],
              error_message: message.error
            }
          }))
        }
        break

      case 'job_completed':
        if (message.job_id && message.result) {
          setJobs(prev => ({
            ...prev,
            [message.job_id!]: {
              ...prev[message.job_id!],
              status: 'completed',
              result: message.result
            }
          }))
        }
        break

      case 'active_jobs':
        if (message.jobs) {
          const jobsMap = message.jobs.reduce((acc, job) => {
            acc[job.job_id] = job
            return acc
          }, {} as Record<string, ContractJob>)
          setJobs(jobsMap)
        }
        break

      case 'job_subscribed':
        if (message.job_id && message.job) {
          setJobs(prev => ({
            ...prev,
            [message.job_id!]: message.job!
          }))
        }
        break

      case 'error':
        console.error('Erro WebSocket:', message.message)
        setError(message.message || 'Erro desconhecido')
        break

      case 'pong':
        // Heartbeat response - connection is alive
        break

      default:
        console.log('Mensagem WebSocket não tratada:', message.type)
    }
  }, [])

  // Job management methods
  const createJob = useCallback(async (request: CreateJobRequest): Promise<string> => {
    setIsCreatingJob(true)
    setError(null)

    try {
      const response = await fetch(`${apiUrl}/async/jobs`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(request),
      })

      if (!response.ok) {
        const errorData = await response.json()
        throw new Error(errorData.detail || 'Erro ao criar job')
      }

      const data = await response.json()
      const jobId = data.job_id

      // Adicionar job ao state local
      setJobs(prev => ({
        ...prev,
        [jobId]: {
          job_id: jobId,
          status: 'pending',
          created_at: new Date().toISOString(),
          current_stage: 'initialization',
          job_type: request.job_type,
          contract_title: request.contract_title
        }
      }))

      // Se conectado, subscrever ao job
      if (isConnected && wsRef.current) {
        wsRef.current.send(JSON.stringify({
          type: 'subscribe_job',
          job_id: jobId
        }))
      }

      return jobId

    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'Erro desconhecido'
      setError(errorMessage)
      throw new Error(errorMessage)
    } finally {
      setIsCreatingJob(false)
    }
  }, [apiUrl, isConnected])

  const getJob = useCallback(async (jobId: string): Promise<ContractJob | null> => {
    try {
      const response = await fetch(`${apiUrl}/async/jobs/${jobId}`)
      
      if (!response.ok) {
        if (response.status === 404) {
          return null
        }
        throw new Error('Erro ao buscar job')
      }

      return await response.json()
    } catch (error) {
      console.error('Erro ao buscar job:', error)
      return null
    }
  }, [apiUrl])

  const getUserJobs = useCallback(async (): Promise<ContractJob[]> => {
    try {
      const response = await fetch(`${apiUrl}/async/jobs`)
      
      if (!response.ok) {
        throw new Error('Erro ao buscar jobs do usuário')
      }

      const jobsArray = await response.json()
      
      // Atualizar state local
      const jobsMap = jobsArray.reduce((acc: Record<string, ContractJob>, job: ContractJob) => {
        acc[job.job_id] = job
        return acc
      }, {})
      
      setJobs(jobsMap)
      return jobsArray
    } catch (error) {
      console.error('Erro ao buscar jobs:', error)
      return []
    }
  }, [apiUrl])

  const cancelJob = useCallback(async (jobId: string): Promise<boolean> => {
    try {
      const response = await fetch(`${apiUrl}/async/jobs/${jobId}`, {
        method: 'DELETE',
      })

      if (response.ok) {
        setJobs(prev => ({
          ...prev,
          [jobId]: {
            ...prev[jobId],
            status: 'cancelled'
          }
        }))
        return true
      }
      
      return false
    } catch (error) {
      console.error('Erro ao cancelar job:', error)
      return false
    }
  }, [apiUrl])

  const getJobResult = useCallback(async (jobId: string): Promise<any> => {
    try {
      const response = await fetch(`${apiUrl}/async/jobs/${jobId}/result`)
      
      if (!response.ok) {
        throw new Error('Erro ao buscar resultado do job')
      }

      return await response.json()
    } catch (error) {
      console.error('Erro ao buscar resultado:', error)
      throw error
    }
  }, [apiUrl])

  const subscribeToJob = useCallback((jobId: string) => {
    if (isConnected && wsRef.current) {
      wsRef.current.send(JSON.stringify({
        type: 'subscribe_job',
        job_id: jobId
      }))
    }
  }, [isConnected])

  // Auto-connect on mount
  useEffect(() => {
    connect()
    
    return () => {
      disconnect()
    }
  }, [connect, disconnect])

  // Cleanup on unmount
  useEffect(() => {
    return () => {
      disconnect()
    }
  }, [disconnect])

  return {
    createJob,
    getJob,
    getUserJobs,
    cancelJob,
    getJobResult,
    jobs,
    isConnected,
    connectionError,
    connect,
    disconnect,
    subscribeToJob,
    isCreatingJob,
    error
  }
}