'use client'

import { useState, useCallback, useEffect } from 'react'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { 
  Wand2, 
  Download, 
  Image as ImageIcon,
  Zap,
  Eye,
  Settings,
  CheckCircle,
  Clock,
  Sparkles,
  FileImage
} from 'lucide-react'
import { cn } from '../../lib/utils'
import { useImageProcessing } from '../../lib/hooks/useImageProcessing'

interface ImageFile {
  id: string
  file: File
  preview: string
  processed?: boolean
  confidenceScore?: number
  appliedFilters?: string[]
  processingTime?: number
}

interface ImageOptimizerProps {
  images: File[]
  onImagesProcessed?: (processedImages: File[]) => void
  autoProcess?: boolean
  className?: string
}

export function ImageOptimizer({ 
  images, 
  onImagesProcessed, 
  autoProcess = true,
  className 
}: ImageOptimizerProps) {
  const [imageFiles, setImageFiles] = useState<ImageFile[]>([])
  const [processingOptions, setProcessingOptions] = useState<{
    autoEnhance: boolean
    preserveColors: boolean
    outputFormat: 'PNG' | 'JPEG' | 'WEBP'
  }>({
    autoEnhance: true,
    preserveColors: false,
    outputFormat: 'PNG'
  })
  const [processedCount, setProcessedCount] = useState(0)
  const [showSettings, setShowSettings] = useState(false)

  const { 
    processImage, 
    processMultipleImages, 
    downloadEnhancedImage,
    isProcessing, 
    error 
  } = useImageProcessing()

  // Inicializar arquivos de imagem
  useEffect(() => {
    const newImageFiles: ImageFile[] = images.map(file => ({
      id: crypto.randomUUID(),
      file,
      preview: URL.createObjectURL(file),
      processed: false
    }))

    setImageFiles(newImageFiles)
    setProcessedCount(0)

    // Cleanup URLs quando componente desmonta
    return () => {
      newImageFiles.forEach(({ preview }) => URL.revokeObjectURL(preview))
    }
  }, [images])

  // Auto-processamento se habilitado
  useEffect(() => {
    if (autoProcess && imageFiles.length > 0 && !imageFiles.some(img => img.processed)) {
      handleProcessAll()
    }
  }, [imageFiles, autoProcess])

  // Processar imagem individual
  const handleProcessSingle = useCallback(async (imageFile: ImageFile) => {
    try {
      const result = await processImage(imageFile.file, processingOptions)
      
      setImageFiles(prev => prev.map(img => 
        img.id === imageFile.id 
          ? {
              ...img,
              processed: true,
              confidenceScore: result.confidenceScore,
              appliedFilters: result.appliedFilters,
              processingTime: result.processingTimeMs
            }
          : img
      ))

      setProcessedCount(prev => prev + 1)

    } catch (error) {
      console.error('Erro ao processar imagem:', error)
    }
  }, [processImage, processingOptions])

  // Processar todas as imagens
  const handleProcessAll = useCallback(async () => {
    if (imageFiles.length === 0) return

    try {
      const unprocessedImages = imageFiles.filter(img => !img.processed)
      const files = unprocessedImages.map(img => img.file)
      
      const results = await processMultipleImages(files, processingOptions)
      
      setImageFiles(prev => prev.map((img, index) => {
        const resultIndex = unprocessedImages.findIndex(unprocessed => unprocessed.id === img.id)
        if (resultIndex !== -1 && results[resultIndex]) {
          const result = results[resultIndex]
          return {
            ...img,
            processed: true,
            confidenceScore: result.confidenceScore,
            appliedFilters: result.appliedFilters,
            processingTime: result.processingTimeMs
          }
        }
        return img
      }))

      setProcessedCount(imageFiles.length)

      // Notificar componente pai
      if (onImagesProcessed) {
        onImagesProcessed(files)
      }

    } catch (error) {
      console.error('Erro ao processar imagens:', error)
    }
  }, [imageFiles, processMultipleImages, processingOptions, onImagesProcessed])

  // Download imagem otimizada
  const handleDownloadSingle = useCallback(async (imageFile: ImageFile) => {
    try {
      await downloadEnhancedImage(imageFile.file, processingOptions)
    } catch (error) {
      console.error('Erro ao fazer download:', error)
    }
  }, [downloadEnhancedImage, processingOptions])

  // Calcular estatísticas
  const stats = {
    totalImages: imageFiles.length,
    processedImages: processedCount,
    averageConfidence: imageFiles
      .filter(img => img.confidenceScore)
      .reduce((acc, img) => acc + (img.confidenceScore || 0), 0) / 
      Math.max(processedCount, 1),
    totalProcessingTime: imageFiles
      .reduce((acc, img) => acc + (img.processingTime || 0), 0)
  }

  const getQualityColor = (score?: number) => {
    if (!score) return 'gray'
    if (score >= 0.8) return 'green'
    if (score >= 0.6) return 'yellow'
    return 'red'
  }

  return (
    <div className={cn("w-full space-y-4", className)}>
      {/* Header com Estatísticas */}
      <Card>
        <CardHeader className="pb-3">
          <div className="flex items-center justify-between">
            <CardTitle className="text-lg font-semibold flex items-center gap-2">
              <Sparkles className="h-5 w-5 text-purple-600" />
              Otimização de Imagens para OCR
            </CardTitle>
            
            <div className="flex items-center gap-2">
              <Button
                onClick={() => setShowSettings(!showSettings)}
                variant="outline"
                size="sm"
              >
                <Settings className="h-4 w-4 mr-1" />
                Configurações
              </Button>
              
              <Badge variant="secondary">
                {processedCount}/{stats.totalImages} processadas
              </Badge>
            </div>
          </div>
        </CardHeader>

        {/* Configurações */}
        {showSettings && (
          <CardContent className="pt-0 border-t">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <label className="flex items-center space-x-2">
                <input
                  type="checkbox"
                  checked={processingOptions.autoEnhance}
                  onChange={(e) => setProcessingOptions(prev => ({
                    ...prev,
                    autoEnhance: e.target.checked
                  }))}
                  className="rounded"
                />
                <span className="text-sm">Otimização Automática</span>
              </label>

              <label className="flex items-center space-x-2">
                <input
                  type="checkbox"
                  checked={processingOptions.preserveColors}
                  onChange={(e) => setProcessingOptions(prev => ({
                    ...prev,
                    preserveColors: e.target.checked
                  }))}
                  className="rounded"
                />
                <span className="text-sm">Preservar Cores</span>
              </label>

              <select
                value={processingOptions.outputFormat}
                onChange={(e) => setProcessingOptions(prev => ({
                  ...prev,
                  outputFormat: e.target.value as 'PNG' | 'JPEG' | 'WEBP'
                }))}
                className="text-sm border rounded px-2 py-1"
              >
                <option value="PNG">PNG</option>
                <option value="JPEG">JPEG</option>
                <option value="WEBP">WEBP</option>
              </select>
            </div>
          </CardContent>
        )}

        {/* Estatísticas Resumidas */}
        {processedCount > 0 && (
          <CardContent className="pt-0">
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-center">
              <div className="space-y-1">
                <div className="text-2xl font-bold text-green-600">
                  {Math.round(stats.averageConfidence * 100)}%
                </div>
                <div className="text-xs text-gray-500">Confiança Média</div>
              </div>
              
              <div className="space-y-1">
                <div className="text-2xl font-bold text-blue-600">
                  {stats.totalProcessingTime}ms
                </div>
                <div className="text-xs text-gray-500">Tempo Total</div>
              </div>
              
              <div className="space-y-1">
                <div className="text-2xl font-bold text-purple-600">
                  {Math.round(stats.totalProcessingTime / Math.max(stats.processedImages, 1))}ms
                </div>
                <div className="text-xs text-gray-500">Tempo Médio</div>
              </div>
              
              <div className="space-y-1">
                <Button
                  onClick={handleProcessAll}
                  disabled={isProcessing || processedCount === stats.totalImages}
                  size="sm"
                  className="w-full"
                >
                  {isProcessing ? (
                    <>
                      <Clock className="h-4 w-4 mr-2 animate-spin" />
                      Processando...
                    </>
                  ) : (
                    <>
                      <Zap className="h-4 w-4 mr-2" />
                      Processar Todas
                    </>
                  )}
                </Button>
              </div>
            </div>
          </CardContent>
        )}
      </Card>

      {/* Lista de Imagens */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {imageFiles.map((imageFile, index) => (
          <Card key={imageFile.id} className="overflow-hidden">
            <CardHeader className="pb-2">
              <div className="flex items-center justify-between">
                <Badge variant="outline" className="text-xs">
                  Página {index + 1}
                </Badge>
                
                {imageFile.processed && (
                  <Badge 
                    variant="secondary"
                    className={cn(
                      "text-xs",
                      getQualityColor(imageFile.confidenceScore) === 'green' && "bg-green-100 text-green-800",
                      getQualityColor(imageFile.confidenceScore) === 'yellow' && "bg-yellow-100 text-yellow-800",
                      getQualityColor(imageFile.confidenceScore) === 'red' && "bg-red-100 text-red-800"
                    )}
                  >
                    {imageFile.confidenceScore ? 
                      `${Math.round(imageFile.confidenceScore * 100)}% confiança` : 
                      'Processado'
                    }
                  </Badge>
                )}
              </div>
            </CardHeader>

            <CardContent className="space-y-3">
              {/* Preview da Imagem */}
              <div className="relative">
                <img
                  src={imageFile.preview}
                  alt={`Preview ${index + 1}`}
                  className="w-full h-32 object-cover rounded border"
                />
                
                {imageFile.processed && (
                  <div className="absolute top-2 right-2">
                    <CheckCircle className="h-6 w-6 text-green-600 bg-white rounded-full" />
                  </div>
                )}
              </div>

              {/* Informações do Arquivo */}
              <div className="text-xs text-gray-600 space-y-1">
                <div className="truncate">📄 {imageFile.file.name}</div>
                <div>📏 {(imageFile.file.size / 1024 / 1024).toFixed(1)} MB</div>
                
                {imageFile.processed && imageFile.appliedFilters && (
                  <div className="flex flex-wrap gap-1 mt-2">
                    {imageFile.appliedFilters.slice(0, 3).map(filter => (
                      <Badge key={filter} variant="outline" className="text-xs px-1 py-0">
                        {filter.replace(/_/g, ' ')}
                      </Badge>
                    ))}
                    {imageFile.appliedFilters.length > 3 && (
                      <Badge variant="outline" className="text-xs px-1 py-0">
                        +{imageFile.appliedFilters.length - 3}
                      </Badge>
                    )}
                  </div>
                )}
              </div>

              {/* Ações */}
              <div className="flex gap-2">
                {!imageFile.processed ? (
                  <Button
                    onClick={() => handleProcessSingle(imageFile)}
                    disabled={isProcessing}
                    size="sm"
                    className="flex-1"
                  >
                    <Wand2 className="h-4 w-4 mr-1" />
                    Otimizar
                  </Button>
                ) : (
                  <>
                    <Button
                      onClick={() => handleDownloadSingle(imageFile)}
                      variant="outline"
                      size="sm"
                      className="flex-1"
                    >
                      <Download className="h-4 w-4 mr-1" />
                      Download
                    </Button>
                    
                    <Button
                      onClick={() => handleProcessSingle(imageFile)}
                      variant="secondary"
                      size="sm"
                      className="flex-1"
                    >
                      <Eye className="h-4 w-4 mr-1" />
                      Reprocessar
                    </Button>
                  </>
                )}
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      {/* Mensagem de Erro */}
      {error && (
        <Card className="border-red-200 bg-red-50">
          <CardContent className="pt-4">
            <div className="flex items-center gap-2 text-red-800">
              <FileImage className="h-5 w-5" />
              <span className="font-medium">Erro no processamento:</span>
            </div>
            <p className="text-sm text-red-700 mt-1">{error}</p>
          </CardContent>
        </Card>
      )}

      {/* Dicas de Otimização */}
      <Card className="bg-blue-50 border-blue-200">
        <CardContent className="pt-4">
          <div className="flex gap-3">
            <Sparkles className="h-5 w-5 text-blue-600 mt-0.5 flex-shrink-0" />
            <div className="space-y-2">
              <p className="text-sm font-medium text-blue-900">
                🎯 Como funciona a otimização:
              </p>
              <ul className="text-xs text-blue-800 space-y-1 ml-4">
                <li>• <strong>Correção de Perspectiva:</strong> Endireita documentos fotografados</li>
                <li>• <strong>Melhoria de Contraste:</strong> Realça texto e remove sombras</li>
                <li>• <strong>Redução de Ruído:</strong> Remove granulosidade e artefatos</li>
                <li>• <strong>Nitidez Adaptativa:</strong> Melhora legibilidade do texto</li>
                <li>• <strong>Binarização:</strong> Converte para preto/branco otimizado</li>
              </ul>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}