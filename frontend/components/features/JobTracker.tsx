'use client'

import { useState, useEffect, useCallback } from 'react'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { 
  Clock, 
  CheckCircle, 
  XCircle, 
  Loader2,
  Pause,
  Play,
  Download,
  Eye,
  Trash2,
  WifiOff,
  Wifi,
  Activity,
  TrendingUp,
  FileText,
  Image as ImageIcon,
  Brain
} from 'lucide-react'
import { cn } from '../../lib/utils'
import { useAsyncJobs, ContractJob } from '../../lib/hooks/useAsyncJobs'

interface JobTrackerProps {
  userId?: string
  autoRefresh?: boolean
  showOnlyActive?: boolean
  className?: string
}

export function JobTracker({ 
  userId = 'demo_user', 
  autoRefresh = true,
  showOnlyActive = false,
  className 
}: JobTrackerProps) {
  const [selectedJob, setSelectedJob] = useState<string | null>(null)
  const [showCompleted, setShowCompleted] = useState(!showOnlyActive)
  
  const {
    jobs,
    isConnected,
    connectionError,
    getUserJobs,
    cancelJob,
    getJobResult,
    subscribeToJob,
    connect,
    disconnect
  } = useAsyncJobs(userId)

  const jobsList = Object.values(jobs)
  const activeJobs = jobsList.filter(job => 
    job.status === 'pending' || job.status === 'processing'
  )
  const completedJobs = jobsList.filter(job => 
    job.status === 'completed' || job.status === 'failed' || job.status === 'cancelled'
  )

  // Auto refresh jobs periodically
  useEffect(() => {
    if (autoRefresh) {
      const interval = setInterval(() => {
        getUserJobs()
      }, 30000) // Refresh every 30 seconds

      return () => clearInterval(interval)
    }
  }, [autoRefresh, getUserJobs])

  // Load initial jobs
  useEffect(() => {
    getUserJobs()
  }, [getUserJobs])

  const handleCancelJob = useCallback(async (jobId: string) => {
    const success = await cancelJob(jobId)
    if (success) {
      console.log(`Job ${jobId} cancelado`)
    }
  }, [cancelJob])

  const handleViewResult = useCallback(async (jobId: string) => {
    try {
      const result = await getJobResult(jobId)
      console.log('Resultado do job:', result)
      // Aqui você pode abrir um modal ou navegar para página de resultado
    } catch (error) {
      console.error('Erro ao obter resultado:', error)
    }
  }, [getJobResult])

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'pending':
        return <Clock className="h-4 w-4 text-yellow-500" />
      case 'processing':
        return <Loader2 className="h-4 w-4 text-blue-500 animate-spin" />
      case 'completed':
        return <CheckCircle className="h-4 w-4 text-green-500" />
      case 'failed':
        return <XCircle className="h-4 w-4 text-red-500" />
      case 'cancelled':
        return <Pause className="h-4 w-4 text-gray-500" />
      default:
        return <Clock className="h-4 w-4 text-gray-400" />
    }
  }

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'pending':
        return 'bg-yellow-100 text-yellow-800'
      case 'processing':
        return 'bg-blue-100 text-blue-800'
      case 'completed':
        return 'bg-green-100 text-green-800'
      case 'failed':
        return 'bg-red-100 text-red-800'
      case 'cancelled':
        return 'bg-gray-100 text-gray-800'
      default:
        return 'bg-gray-100 text-gray-600'
    }
  }

  const getJobTypeIcon = (jobType: string) => {
    switch (jobType) {
      case 'contract_analysis':
        return <FileText className="h-4 w-4" />
      case 'image_processing':
        return <ImageIcon className="h-4 w-4" />
      case 'full_pipeline':
        return <Brain className="h-4 w-4" />
      default:
        return <Activity className="h-4 w-4" />
    }
  }

  const formatDuration = (startTime: string) => {
    const start = new Date(startTime)
    const now = new Date()
    const diffMs = now.getTime() - start.getTime()
    const diffMins = Math.floor(diffMs / 60000)
    const diffSecs = Math.floor((diffMs % 60000) / 1000)
    
    if (diffMins > 0) {
      return `${diffMins}m ${diffSecs}s`
    }
    return `${diffSecs}s`
  }

  const formatProgress = (progress?: number) => {
    if (progress === undefined) return 'N/A'
    return `${Math.round(progress * 100)}%`
  }

  return (
    <div className={cn("w-full space-y-4", className)}>
      {/* Header com Status de Conexão */}
      <Card>
        <CardHeader className="pb-3">
          <div className="flex items-center justify-between">
            <CardTitle className="text-lg font-semibold flex items-center gap-2">
              <Activity className="h-5 w-5 text-blue-600" />
              Processamento de Contratos
            </CardTitle>
            
            <div className="flex items-center gap-2">
              {/* Status de Conexão */}
              <Badge 
                variant="outline" 
                className={cn(
                  "flex items-center gap-1",
                  isConnected ? "border-green-500 text-green-700" : "border-red-500 text-red-700"
                )}
              >
                {isConnected ? (
                  <>
                    <Wifi className="h-3 w-3" />
                    Online
                  </>
                ) : (
                  <>
                    <WifiOff className="h-3 w-3" />
                    Offline
                  </>
                )}
              </Badge>

              {/* Controles de Conexão */}
              {!isConnected && (
                <Button onClick={connect} size="sm" variant="outline">
                  Reconectar
                </Button>
              )}
            </div>
          </div>

          {connectionError && (
            <div className="text-sm text-red-600 bg-red-50 p-2 rounded">
              {connectionError}
            </div>
          )}
        </CardHeader>

        <CardContent className="pt-0">
          {/* Estatísticas Rápidas */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-4">
            <div className="text-center">
              <div className="text-2xl font-bold text-blue-600">{activeJobs.length}</div>
              <div className="text-xs text-gray-500">Em Andamento</div>
            </div>
            
            <div className="text-center">
              <div className="text-2xl font-bold text-green-600">
                {completedJobs.filter(j => j.status === 'completed').length}
              </div>
              <div className="text-xs text-gray-500">Concluídos</div>
            </div>
            
            <div className="text-center">
              <div className="text-2xl font-bold text-red-600">
                {completedJobs.filter(j => j.status === 'failed').length}
              </div>
              <div className="text-xs text-gray-500">Falharam</div>
            </div>
            
            <div className="text-center">
              <div className="text-2xl font-bold text-gray-600">{jobsList.length}</div>
              <div className="text-xs text-gray-500">Total</div>
            </div>
          </div>

          {/* Toggle para mostrar concluídos */}
          <div className="flex items-center gap-2">
            <label className="flex items-center space-x-2 text-sm">
              <input
                type="checkbox"
                checked={showCompleted}
                onChange={(e) => setShowCompleted(e.target.checked)}
                className="rounded"
              />
              <span>Mostrar jobs concluídos</span>
            </label>
          </div>
        </CardContent>
      </Card>

      {/* Jobs Ativos */}
      {activeJobs.length > 0 && (
        <Card>
          <CardHeader className="pb-3">
            <CardTitle className="text-base font-medium flex items-center gap-2">
              <TrendingUp className="h-4 w-4 text-blue-500" />
              Jobs em Andamento ({activeJobs.length})
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-3">
            {activeJobs.map((job) => (
              <JobCard
                key={job.job_id}
                job={job}
                isSelected={selectedJob === job.job_id}
                onSelect={() => setSelectedJob(job.job_id)}
                onCancel={() => handleCancelJob(job.job_id)}
                onViewResult={() => handleViewResult(job.job_id)}
                getStatusIcon={getStatusIcon}
                getStatusColor={getStatusColor}
                getJobTypeIcon={getJobTypeIcon}
                formatDuration={formatDuration}
                formatProgress={formatProgress}
              />
            ))}
          </CardContent>
        </Card>
      )}

      {/* Jobs Concluídos */}
      {showCompleted && completedJobs.length > 0 && (
        <Card>
          <CardHeader className="pb-3">
            <CardTitle className="text-base font-medium flex items-center gap-2">
              <CheckCircle className="h-4 w-4 text-green-500" />
              Jobs Concluídos ({completedJobs.length})
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-3">
            {completedJobs.slice(-10).reverse().map((job) => (
              <JobCard
                key={job.job_id}
                job={job}
                isSelected={selectedJob === job.job_id}
                onSelect={() => setSelectedJob(job.job_id)}
                onCancel={() => handleCancelJob(job.job_id)}
                onViewResult={() => handleViewResult(job.job_id)}
                getStatusIcon={getStatusIcon}
                getStatusColor={getStatusColor}
                getJobTypeIcon={getJobTypeIcon}
                formatDuration={formatDuration}
                formatProgress={formatProgress}
                isCompleted={true}
              />
            ))}
          </CardContent>
        </Card>
      )}

      {/* Empty State */}
      {jobsList.length === 0 && (
        <Card>
          <CardContent className="pt-6 text-center">
            <Activity className="h-12 w-12 text-gray-400 mx-auto mb-4" />
            <h3 className="text-lg font-semibold text-gray-900 mb-2">
              Nenhum job encontrado
            </h3>
            <p className="text-gray-600">
              Faça upload de um contrato para começar o processamento
            </p>
          </CardContent>
        </Card>
      )}
    </div>
  )
}

// Componente separado para cada job
interface JobCardProps {
  job: ContractJob
  isSelected: boolean
  isCompleted?: boolean
  onSelect: () => void
  onCancel: () => void
  onViewResult: () => void
  getStatusIcon: (status: string) => React.ReactNode
  getStatusColor: (status: string) => string
  getJobTypeIcon: (jobType: string) => React.ReactNode
  formatDuration: (startTime: string) => string
  formatProgress: (progress?: number) => string
}

function JobCard({ 
  job, 
  isSelected, 
  isCompleted = false,
  onSelect, 
  onCancel, 
  onViewResult,
  getStatusIcon,
  getStatusColor,
  getJobTypeIcon,
  formatDuration,
  formatProgress
}: JobCardProps) {
  return (
    <div
      className={cn(
        "border rounded-lg p-3 cursor-pointer transition-all",
        isSelected ? "border-blue-500 bg-blue-50" : "border-gray-200 hover:border-gray-300"
      )}
      onClick={onSelect}
    >
      <div className="flex items-center justify-between mb-2">
        <div className="flex items-center gap-2">
          {getJobTypeIcon(job.job_type)}
          <span className="font-medium text-sm truncate max-w-[200px]">
            {job.contract_title}
          </span>
        </div>
        
        <div className="flex items-center gap-2">
          <Badge className={cn("text-xs", getStatusColor(job.status))}>
            {getStatusIcon(job.status)}
            {job.status}
          </Badge>
        </div>
      </div>

      {/* Progress Bar para jobs ativos */}
      {job.status === 'processing' && job.progress !== undefined && (
        <div className="mb-2">
          <div className="flex items-center justify-between mb-1">
            <span className="text-xs text-gray-600">{job.current_stage}</span>
            <span className="text-xs text-gray-500">{formatProgress(job.progress)}</span>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-1.5">
            <div
              className="bg-blue-600 h-1.5 rounded-full transition-all duration-300"
              style={{ width: `${(job.progress || 0) * 100}%` }}
            />
          </div>
        </div>
      )}

      <div className="flex items-center justify-between text-xs text-gray-500">
        <div className="flex items-center gap-3">
          <span>ID: {job.job_id.slice(0, 8)}...</span>
          <span>{formatDuration(job.created_at)}</span>
          {job.estimated_completion && (
            <span>ETA: {new Date(job.estimated_completion).toLocaleTimeString()}</span>
          )}
        </div>
        
        <div className="flex items-center gap-1">
          {job.status === 'completed' && (
            <Button
              onClick={(e) => { e.stopPropagation(); onViewResult() }}
              size="sm"
              variant="ghost"
              className="h-6 w-6 p-0"
            >
              <Eye className="h-3 w-3" />
            </Button>
          )}
          
          {(job.status === 'pending' || job.status === 'processing') && (
            <Button
              onClick={(e) => { e.stopPropagation(); onCancel() }}
              size="sm"
              variant="ghost"
              className="h-6 w-6 p-0 text-red-500 hover:text-red-700"
            >
              <Trash2 className="h-3 w-3" />
            </Button>
          )}
        </div>
      </div>

      {/* Mensagem de progresso ou erro */}
      {job.message && (
        <div className="mt-2 text-xs text-gray-600 bg-gray-50 p-2 rounded">
          {job.message}
        </div>
      )}

      {job.error_message && (
        <div className="mt-2 text-xs text-red-600 bg-red-50 p-2 rounded">
          ❌ {job.error_message}
        </div>
      )}
    </div>
  )
}