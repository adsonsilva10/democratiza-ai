'use client'

import { useState, useCallback } from 'react'

interface ImageProcessingResult {
  success: boolean
  confidenceScore: number
  appliedFilters: string[]
  originalSize: [number, number]
  enhancedSize: [number, number]
  processingTimeMs: number
}

interface ProcessingOptions {
  autoEnhance?: boolean
  preserveColors?: boolean
  outputFormat?: 'PNG' | 'JPEG' | 'WEBP'
}

interface UseImageProcessingReturn {
  processImage: (file: File, options?: ProcessingOptions) => Promise<ImageProcessingResult>
  processMultipleImages: (files: File[], options?: ProcessingOptions) => Promise<ImageProcessingResult[]>
  downloadEnhancedImage: (file: File, options?: ProcessingOptions) => Promise<void>
  isProcessing: boolean
  error: string | null
}

export function useImageProcessing(): UseImageProcessingReturn {
  const [isProcessing, setIsProcessing] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1'

  const processImage = useCallback(async (
    file: File, 
    options: ProcessingOptions = {}
  ): Promise<ImageProcessingResult> => {
    setIsProcessing(true)
    setError(null)

    try {
      const formData = new FormData()
      formData.append('file', file)
      formData.append('auto_enhance', String(options.autoEnhance ?? true))
      formData.append('preserve_colors', String(options.preserveColors ?? false))

      const response = await fetch(`${apiUrl}/image-processing/enhance-single`, {
        method: 'POST',
        body: formData,
      })

      if (!response.ok) {
        const errorData = await response.json()
        throw new Error(errorData.detail || 'Erro no processamento da imagem')
      }

      const result = await response.json()
      return result

    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Erro desconhecido'
      setError(errorMessage)
      throw new Error(errorMessage)
    } finally {
      setIsProcessing(false)
    }
  }, [apiUrl])

  const processMultipleImages = useCallback(async (
    files: File[], 
    options: ProcessingOptions = {}
  ): Promise<ImageProcessingResult[]> => {
    if (files.length === 0) {
      throw new Error('Nenhum arquivo fornecido')
    }

    if (files.length > 20) {
      throw new Error('Máximo 20 arquivos por vez')
    }

    setIsProcessing(true)
    setError(null)

    try {
      const formData = new FormData()
      
      files.forEach(file => {
        formData.append('files', file)
      })
      
      formData.append('auto_enhance', String(options.autoEnhance ?? true))
      formData.append('preserve_colors', String(options.preserveColors ?? false))

      const response = await fetch(`${apiUrl}/image-processing/enhance-multiple`, {
        method: 'POST',
        body: formData,
      })

      if (!response.ok) {
        const errorData = await response.json()
        throw new Error(errorData.detail || 'Erro no processamento múltiplo')
      }

      const results = await response.json()
      return results

    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Erro desconhecido'
      setError(errorMessage)
      throw new Error(errorMessage)
    } finally {
      setIsProcessing(false)
    }
  }, [apiUrl])

  const downloadEnhancedImage = useCallback(async (
    file: File, 
    options: ProcessingOptions = {}
  ): Promise<void> => {
    setIsProcessing(true)
    setError(null)

    try {
      const formData = new FormData()
      formData.append('file', file)
      formData.append('auto_enhance', String(options.autoEnhance ?? true))
      formData.append('preserve_colors', String(options.preserveColors ?? false))
      formData.append('output_format', options.outputFormat || 'PNG')

      const response = await fetch(`${apiUrl}/image-processing/enhance-and-download`, {
        method: 'POST',
        body: formData,
      })

      if (!response.ok) {
        const errorData = await response.text()
        throw new Error(errorData || 'Erro no download da imagem')
      }

      // Extrair informações dos headers
      const confidenceScore = response.headers.get('X-Confidence-Score')
      const appliedFilters = response.headers.get('X-Applied-Filters')

      // Criar blob para download
      const blob = await response.blob()
      const url = window.URL.createObjectURL(blob)
      
      // Extrair nome do arquivo do Content-Disposition ou usar default
      const contentDisposition = response.headers.get('Content-Disposition')
      let filename = `enhanced_${file.name}`
      
      if (contentDisposition) {
        const matches = /filename=([^;]+)/.exec(contentDisposition)
        if (matches && matches[1]) {
          filename = matches[1].replace(/"/g, '')
        }
      }

      // Criar link de download
      const link = document.createElement('a')
      link.href = url
      link.download = filename
      document.body.appendChild(link)
      link.click()

      // Cleanup
      document.body.removeChild(link)
      window.URL.revokeObjectURL(url)

      // Log informações de qualidade
      if (confidenceScore) {
        console.log(`Confiança da imagem otimizada: ${confidenceScore}`)
      }
      if (appliedFilters) {
        console.log(`Filtros aplicados: ${appliedFilters}`)
      }

    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Erro no download'
      setError(errorMessage)
      throw new Error(errorMessage)
    } finally {
      setIsProcessing(false)
    }
  }, [apiUrl])

  return {
    processImage,
    processMultipleImages,
    downloadEnhancedImage,
    isProcessing,
    error
  }
}

// Hook adicional para métricas de qualidade
export function useImageQualityMetrics() {
  const [metrics, setMetrics] = useState(null)
  const [loading, setLoading] = useState(false)

  const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1'

  const fetchMetrics = useCallback(async () => {
    setLoading(true)
    try {
      const response = await fetch(`${apiUrl}/image-processing/quality-metrics`)
      if (response.ok) {
        const data = await response.json()
        setMetrics(data)
      }
    } catch (error) {
      console.error('Erro ao buscar métricas:', error)
    } finally {
      setLoading(false)
    }
  }, [apiUrl])

  return { metrics, loading, fetchMetrics }
}