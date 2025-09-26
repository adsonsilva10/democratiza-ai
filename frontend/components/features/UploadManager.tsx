'use client'

import { useState, useRef } from 'react'
import apiClient from '../../lib/api'
import { MobileAwareDocumentUpload } from './MobileAwareDocumentUpload'
import { useDeviceDetection } from '@/lib/hooks/useDeviceDetection'

interface UploadManagerProps {
  onContractUploaded?: (contractId: string) => void
  maxFiles?: number
  maxFileSize?: number
}

export default function UploadManager({ 
  onContractUploaded, 
  maxFiles = 5, 
  maxFileSize = 10
}: UploadManagerProps) {
  const [uploading, setUploading] = useState(false)
  const [uploadProgress, setUploadProgress] = useState(0)
  const [uploadedFiles, setUploadedFiles] = useState<Array<{
    file: File
    contractId?: string
    status: 'uploading' | 'processing' | 'completed' | 'error'
    error?: string
  }>>([])
  const [contractTitle, setContractTitle] = useState('')
  const [isDragOver, setIsDragOver] = useState(false)
  const fileInputRef = useRef<HTMLInputElement>(null)
  const { isMobile } = useDeviceDetection()

  const handleFileSelect = async (files: FileList | null) => {
    if (!files || !contractTitle.trim()) {
      if (!contractTitle.trim()) {
        alert('Por favor, informe um título para o contrato')
      }
      return
    }

    setUploading(true)

    for (const file of Array.from(files).slice(0, maxFiles)) {
      const fileUpload = {
        file,
        status: 'uploading' as const
      }

      setUploadedFiles(prev => [...prev, fileUpload])

      if (file.size > maxFileSize) {
        setUploadedFiles(prev =>
          prev.map(f =>
            f.file === file
              ? { ...f, status: 'error' as const, error: 'Arquivo muito grande (máximo 10MB)' }
              : f
          )
        )
        continue
      }

      try {
        const contract = await apiClient.uploadContract(file)

        setUploadedFiles(prev =>
          prev.map(f =>
            f.file === file
              ? { ...f, contractId: contract.data.id, status: 'processing' as const }
              : f
          )
        )

        // Poll for completion
        pollContractStatus(contract.data.id, file)

        if (onContractUploaded) {
          onContractUploaded(contract.data.id)
        }
      } catch (error) {
        console.error('Upload error:', error)
        setUploadedFiles(prev =>
          prev.map(f =>
            f.file === file
              ? { ...f, status: 'error' as const, error: 'Erro no upload' }
              : f
          )
        )
      }
    }

    setUploading(false)
    setUploadProgress(0)
  }

  const pollContractStatus = async (contractId: string, file: File) => {
    const maxAttempts = 60 // 5 minutes with 5-second intervals
    let attempts = 0

    const checkStatus = async () => {
      try {
        const contract = await apiClient.getContract(contractId)

        if (contract.data.status === 'completed') {
          setUploadedFiles(prev =>
            prev.map(f =>
              f.file === file
                ? { ...f, status: 'completed' as const }
                : f
            )
          )
          return
        }

        if (contract.data.status === 'error') {
          setUploadedFiles(prev =>
            prev.map(f =>
              f.file === file
                ? { ...f, status: 'error' as const, error: 'Erro no processamento' }
                : f
            )
          )
          return
        }

        attempts++
        if (attempts < maxAttempts) {
          setTimeout(checkStatus, 5000)
        } else {
          setUploadedFiles(prev =>
            prev.map(f =>
              f.file === file
                ? { ...f, status: 'error' as const, error: 'Timeout no processamento' }
                : f
            )
          )
        }
      } catch (error) {
        console.error('Status check error:', error)
        setUploadedFiles(prev =>
          prev.map(f =>
            f.file === file
              ? { ...f, status: 'error' as const, error: 'Erro ao verificar status' }
              : f
          )
        )
      }
    }

    setTimeout(checkStatus, 2000)
  }

  const removeFile = (file: File) => {
    setUploadedFiles(prev => prev.filter(f => f.file !== file))
  }

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault()
    setIsDragOver(true)
  }

  const handleDragLeave = (e: React.DragEvent) => {
    e.preventDefault()
    setIsDragOver(false)
  }

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault()
    setIsDragOver(false)
    handleFileSelect(e.dataTransfer.files)
  }

  const handleFileInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    handleFileSelect(e.target.files)
  }

  const formatFileSize = (bytes: number) => {
    if (bytes === 0) return '0 Bytes'
    const k = 1024
    const sizes = ['Bytes', 'KB', 'MB', 'GB']
    const i = Math.floor(Math.log(bytes) / Math.log(k))
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
  }

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'uploading':
      case 'processing':
        return '🔄'
      case 'completed':
        return '✅'
      case 'error':
        return '❌'
      default:
        return '📄'
    }
  }

  const getStatusText = (status: string) => {
    switch (status) {
      case 'uploading':
        return 'Enviando...'
      case 'processing':
        return 'Analisando...'
      case 'completed':
        return 'Análise concluída'
      case 'error':
        return 'Erro'
      default:
        return ''
    }
  }

  return (
    <div className="max-w-4xl mx-auto bg-white rounded-lg shadow-sm border p-6">
      {/* Header */}
      <div className="mb-6">
        <h2 className="text-2xl font-bold text-gray-900 mb-2">📄 Upload de Contrato</h2>
        <p className="text-gray-600">
          Faça upload do seu contrato para análise por IA. Formatos suportados: PDF, DOC, DOCX
        </p>
      </div>

      {/* Contract Title Input */}
      <div className="mb-6">
        <label htmlFor="contractTitle" className="block text-sm font-medium text-gray-700 mb-2">
          Título do Contrato *
        </label>
        <input
          type="text"
          id="contractTitle"
          value={contractTitle}
          onChange={(e) => setContractTitle(e.target.value)}
          placeholder="Ex: Contrato de Locação - Apartamento Centro"
          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          disabled={uploading}
        />
      </div>

      {/* Mobile-Aware Upload Area */}
      <MobileAwareDocumentUpload
        onFilesUploaded={(files) => handleFileSelect({ 
          ...files, 
          length: files.length,
          item: (index: number) => files[index]
        } as FileList)}
        maxFiles={maxFiles}
        maxFileSize={maxFileSize}
        acceptedTypes={['.pdf', '.doc', '.docx', '.txt', 'image/*']}
      />

      {/* Upload Progress */}
      {uploading && (
        <div className="mt-6">
          <div className="flex items-center justify-between mb-2">
            <span className="text-sm text-gray-600">Enviando arquivos...</span>
            <span className="text-sm text-gray-600">{uploadProgress}%</span>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-2">
            <div
              className="bg-blue-600 h-2 rounded-full transition-all duration-300"
              style={{ width: `${uploadProgress}%` }}
            />
          </div>
        </div>
      )}

      {/* File List */}
      {uploadedFiles.length > 0 && (
        <div className="mt-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Arquivos</h3>
          <div className="space-y-3">
            {uploadedFiles.map((fileUpload, index) => (
              <div key={index} className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                <div className="flex items-center space-x-3">
                  <div className="text-2xl">📄</div>
                  <div>
                    <p className="font-medium text-gray-900">{fileUpload.file.name}</p>
                    <p className="text-sm text-gray-500">
                      {formatFileSize(fileUpload.file.size)}
                    </p>
                  </div>
                </div>

                <div className="flex items-center space-x-3">
                  <div className="flex items-center space-x-2">
                    <span className="text-xl">{getStatusIcon(fileUpload.status)}</span>
                    <span className="text-sm text-gray-600">
                      {getStatusText(fileUpload.status)}
                    </span>
                  </div>

                  {fileUpload.status === 'error' && (
                    <button
                      onClick={() => removeFile(fileUpload.file)}
                      className="text-red-600 hover:text-red-800 text-sm"
                    >
                      Remover
                    </button>
                  )}

                  {fileUpload.status === 'completed' && fileUpload.contractId && (
                    <button
                      onClick={() => onContractUploaded?.(fileUpload.contractId!)}
                      className="text-blue-600 hover:text-blue-800 text-sm font-medium"
                    >
                      Ver Análise
                    </button>
                  )}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Error Messages */}
      {uploadedFiles.some(f => f.status === 'error') && (
        <div className="mt-4 p-4 bg-red-50 border border-red-200 rounded-md">
          <div className="flex items-center space-x-2">
            <span className="text-red-600">⚠️</span>
            <p className="text-red-700 font-medium">Alguns arquivos apresentaram erros:</p>
          </div>
          <ul className="mt-2 space-y-1">
            {uploadedFiles
              .filter(f => f.status === 'error')
              .map((f, index) => (
                <li key={index} className="text-red-600 text-sm">
                  • {f.file.name}: {f.error}
                </li>
              ))}
          </ul>
        </div>
      )}
    </div>
  )
}