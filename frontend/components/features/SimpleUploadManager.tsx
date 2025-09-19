'use client'

import { useState, useRef } from 'react'

interface SimpleUploadManagerProps {
  onFileSelect?: (file: File) => void
  onUploadComplete?: (result: any) => void
  className?: string
}

const ACCEPTED_FILE_TYPES = [
  'application/pdf',
  'application/msword',
  'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
]

const MAX_FILE_SIZE = 10 * 1024 * 1024 // 10MB

export default function SimpleUploadManager({ 
  onFileSelect, 
  onUploadComplete, 
  className = '' 
}: SimpleUploadManagerProps) {
  const [isDragOver, setIsDragOver] = useState(false)
  const [isUploading, setIsUploading] = useState(false)
  const [uploadProgress, setUploadProgress] = useState(0)
  const [error, setError] = useState<string | null>(null)
  const [selectedFile, setSelectedFile] = useState<File | null>(null)
  const [success, setSuccess] = useState<string | null>(null)
  const fileInputRef = useRef<HTMLInputElement>(null)

  const validateFile = (file: File): string | null => {
    if (!ACCEPTED_FILE_TYPES.includes(file.type)) {
      return 'Tipo de arquivo não suportado. Use PDF, DOC ou DOCX.'
    }
    
    if (file.size > MAX_FILE_SIZE) {
      return 'Arquivo muito grande. Tamanho máximo: 10MB.'
    }
    
    return null
  }

  const handleFileSelect = (file: File) => {
    const validationError = validateFile(file)
    if (validationError) {
      setError(validationError)
      return
    }

    setError(null)
    setSuccess(null)
    setSelectedFile(file)
    onFileSelect?.(file)
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
    
    const files = Array.from(e.dataTransfer.files)
    if (files.length > 0) {
      handleFileSelect(files[0])
    }
  }

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files
    if (files && files.length > 0) {
      handleFileSelect(files[0])
    }
  }

  const handleUpload = async () => {
    if (!selectedFile) return

    setIsUploading(true)
    setUploadProgress(0)
    setError(null)
    setSuccess(null)

    try {
      // Simular progresso de upload
      const progressInterval = setInterval(() => {
        setUploadProgress(prev => {
          if (prev >= 90) {
            clearInterval(progressInterval)
            return 90
          }
          return prev + 10
        })
      }, 200)

      // Aqui você faria a chamada real para a API
      // const formData = new FormData()
      // formData.append('file', selectedFile)
      // const response = await fetch('/api/v1/contracts/upload', {
      //   method: 'POST',
      //   body: formData
      // })

      // Simular delay de upload
      await new Promise(resolve => setTimeout(resolve, 2000))
      
      clearInterval(progressInterval)
      setUploadProgress(100)
      
      // Simular resposta da API
      const mockResult = {
        success: true,
        fileId: 'mock-file-id-' + Date.now(),
        fileName: selectedFile.name,
        message: 'Arquivo enviado com sucesso!',
        analysis: {
          contractType: 'Contrato de Locação',
          riskLevel: 'Médio',
          issues: ['Cláusula de reajuste abusiva', 'Multa excessiva'],
          recommendations: ['Negociar taxa de reajuste', 'Solicitar redução da multa']
        }
      }

      setSuccess('✅ Arquivo enviado e analisado com sucesso!')
      onUploadComplete?.(mockResult)
      
      // Reset após sucesso
      setTimeout(() => {
        setIsUploading(false)
        setUploadProgress(0)
      }, 1000)
      
    } catch (err) {
      setError('Erro ao enviar arquivo. Tente novamente.')
      setIsUploading(false)
      setUploadProgress(0)
    }
  }

  const handleReset = () => {
    setSelectedFile(null)
    setError(null)
    setSuccess(null)
    setUploadProgress(0)
    setIsUploading(false)
    if (fileInputRef.current) {
      fileInputRef.current.value = ''
    }
  }

  const formatFileSize = (bytes: number): string => {
    if (bytes === 0) return '0 Bytes'
    const k = 1024
    const sizes = ['Bytes', 'KB', 'MB', 'GB']
    const i = Math.floor(Math.log(bytes) / Math.log(k))
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
  }

  return (
    <div className={`w-full max-w-2xl mx-auto ${className}`}>
      {/* Área de Drop */}
      <div
        className={`
          border-2 border-dashed rounded-lg p-8 text-center transition-all duration-200
          ${isDragOver 
            ? 'border-blue-400 bg-blue-50' 
            : 'border-gray-300 hover:border-blue-400'
          }
          ${error ? 'border-red-300 bg-red-50' : ''}
          ${success ? 'border-green-300 bg-green-50' : ''}
        `}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
      >
        <div className="text-4xl mb-4">
          {isUploading ? '⏳' : success ? '✅' : '📄'}
        </div>
        
        {!selectedFile ? (
          <>
            <p className="text-lg mb-2 text-gray-700">
              Arraste seu contrato aqui ou clique para selecionar
            </p>
            <p className="text-sm text-gray-500 mb-4">
              Formatos aceitos: PDF, DOC, DOCX (máx. 10MB)
            </p>
            
            <button
              onClick={() => fileInputRef.current?.click()}
              disabled={isUploading}
              className="bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400 text-white px-6 py-2 rounded-lg transition-colors"
            >
              Selecionar Arquivo
            </button>
          </>
        ) : (
          <div className="space-y-4">
            <div className="bg-white p-4 rounded-lg border">
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-3">
                  <span className="text-2xl">📄</span>
                  <div className="text-left">
                    <p className="font-medium text-gray-900">{selectedFile.name}</p>
                    <p className="text-sm text-gray-500">{formatFileSize(selectedFile.size)}</p>
                  </div>
                </div>
                
                {!isUploading && !success && (
                  <button
                    onClick={handleReset}
                    className="text-red-500 hover:text-red-700 text-xl"
                  >
                    ❌
                  </button>
                )}
              </div>
              
              {isUploading && (
                <div className="mt-3">
                  <div className="w-full bg-gray-200 rounded-full h-2">
                    <div 
                      className="bg-blue-600 h-2 rounded-full transition-all duration-300"
                      style={{ width: `${uploadProgress}%` }}
                    ></div>
                  </div>
                  <p className="text-sm text-gray-600 mt-1">
                    {uploadProgress < 100 ? `Enviando... ${uploadProgress}%` : 'Analisando contrato...'}
                  </p>
                </div>
              )}
            </div>
            
            {!isUploading && !success && (
              <button
                onClick={handleUpload}
                className="bg-green-600 hover:bg-green-700 text-white px-8 py-3 rounded-lg font-semibold transition-colors"
              >
                🚀 Analisar Contrato
              </button>
            )}

            {success && (
              <div className="space-y-3">
                <p className="text-green-700 font-medium">{success}</p>
                <div className="flex space-x-3">
                  <button
                    onClick={handleReset}
                    className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-2 rounded-lg transition-colors"
                  >
                    📄 Analisar Outro
                  </button>
                  <button
                    onClick={() => alert('Funcionalidade em desenvolvimento!')}
                    className="bg-gray-600 hover:bg-gray-700 text-white px-6 py-2 rounded-lg transition-colors"
                  >
                    📊 Ver Relatório
                  </button>
                </div>
              </div>
            )}
          </div>
        )}
      </div>

      {/* Input oculto */}
      <input
        ref={fileInputRef}
        type="file"
        accept=".pdf,.doc,.docx"
        onChange={handleInputChange}
        className="hidden"
      />

      {/* Mensagem de erro */}
      {error && (
        <div className="mt-4 p-4 bg-red-100 border border-red-300 rounded-lg">
          <p className="text-red-700">❌ {error}</p>
        </div>
      )}

      {/* Informações de segurança */}
      <div className="mt-6 text-center">
        <p className="text-sm text-gray-500">
          🔒 Seus documentos são processados com segurança total e confidencialidade
        </p>
      </div>
    </div>
  )
}