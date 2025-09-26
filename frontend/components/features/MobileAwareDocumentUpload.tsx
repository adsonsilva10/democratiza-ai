'use client'

import { useState, useCallback } from 'react'
import { useDropzone } from 'react-dropzone'
import { Button } from '@/components/ui/button'
import { Card, CardContent } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { 
  Camera, 
  Upload, 
  File, 
  X, 
  Image as ImageIcon,
  Smartphone,
  Monitor
} from 'lucide-react'
import { cn } from '@/lib/utils'
import { useDeviceDetection } from '@/lib/hooks/useDeviceDetection'
import { MobileCameraCapture } from './MobileCameraCapture'

interface UploadedFile {
  id: string
  file: File
  preview?: string
  type: 'image' | 'pdf' | 'document'
}

interface MobileAwareDocumentUploadProps {
  onFilesUploaded: (files: File[]) => void
  maxFiles?: number
  maxFileSize?: number // in MB
  acceptedTypes?: string[]
  className?: string
}

export function MobileAwareDocumentUpload({
  onFilesUploaded,
  maxFiles = 10,
  maxFileSize = 10,
  acceptedTypes = ['image/*', '.pdf', '.doc', '.docx'],
  className
}: MobileAwareDocumentUploadProps) {
  const [uploadedFiles, setUploadedFiles] = useState<UploadedFile[]>([])
  const [showCamera, setShowCamera] = useState(false)
  const [uploadMode, setUploadMode] = useState<'files' | 'camera'>('files')
  
  const { isMobile, hasCamera, isIOS, isAndroid } = useDeviceDetection()

  // Processar arquivos selecionados
  const processFiles = useCallback((files: File[]) => {
    const newFiles: UploadedFile[] = files.map(file => {
      const fileType = file.type.startsWith('image/') ? 'image' : 
                      file.type === 'application/pdf' ? 'pdf' : 'document'
      
      return {
        id: crypto.randomUUID(),
        file,
        type: fileType,
        preview: fileType === 'image' ? URL.createObjectURL(file) : undefined
      }
    })

    setUploadedFiles(prev => [...prev, ...newFiles])
    onFilesUploaded(files)
  }, [onFilesUploaded])

  // Configurar dropzone
  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    accept: acceptedTypes.reduce((acc, type) => {
      acc[type] = []
      return acc
    }, {} as Record<string, string[]>),
    maxFiles,
    maxSize: maxFileSize * 1024 * 1024,
    onDrop: processFiles,
    disabled: showCamera
  })

  // Remover arquivo
  const removeFile = useCallback((fileId: string) => {
    setUploadedFiles(prev => {
      const updated = prev.filter(f => f.id !== fileId)
      const remainingFiles = updated.map(f => f.file)
      onFilesUploaded(remainingFiles)
      return updated
    })
  }, [onFilesUploaded])

  // Lidar com captura da câmera
  const handleCameraCapture = useCallback((files: File[]) => {
    processFiles(files)
    setShowCamera(false)
  }, [processFiles])

  // Cancelar câmera
  const handleCameraCancel = useCallback(() => {
    setShowCamera(false)
  }, [])

  // Iniciar captura
  const startCamera = useCallback(() => {
    setShowCamera(true)
  }, [])

  // Renderizar modo câmera
  if (showCamera) {
    return (
      <MobileCameraCapture
        onImagesCapture={handleCameraCapture}
        onCancel={handleCameraCancel}
        maxImages={maxFiles}
        className={className}
      />
    )
  }

  return (
    <div className={cn("w-full space-y-4", className)}>
      {/* Device Type Indicator */}
      {isMobile && (
        <div className="flex items-center gap-2 text-sm text-gray-600 mb-2">
          <Smartphone className="h-4 w-4" />
          <span>Modo Mobile {isIOS ? '(iOS)' : isAndroid ? '(Android)' : ''}</span>
          {hasCamera && (
            <Badge variant="secondary" className="text-xs">
              Câmera Disponível
            </Badge>
          )}
        </div>
      )}

      {/* Upload Options */}
      <div className="flex gap-2 mb-4">
        <Button
          onClick={() => setUploadMode('files')}
          variant={uploadMode === 'files' ? 'default' : 'outline'}
          size="sm"
          className="flex-1"
        >
          <Upload className="h-4 w-4 mr-2" />
          Arquivos
        </Button>
        
        {isMobile && hasCamera && (
          <Button
            onClick={() => setUploadMode('camera')}
            variant={uploadMode === 'camera' ? 'default' : 'outline'}
            size="sm"
            className="flex-1"
          >
            <Camera className="h-4 w-4 mr-2" />
            Câmera
          </Button>
        )}
      </div>

      {/* Upload Area */}
      {uploadMode === 'files' && (
        <Card>
          <CardContent className="p-6">
            <div
              {...getRootProps()}
              className={cn(
                "border-2 border-dashed rounded-lg p-8 text-center cursor-pointer transition-colors",
                isDragActive ? "border-blue-500 bg-blue-50" : "border-gray-300 hover:border-gray-400",
                isMobile ? "py-6" : "py-8"
              )}
            >
              <input {...getInputProps()} />
              
              <div className="flex flex-col items-center gap-3">
                {isMobile ? (
                  <Smartphone className="h-8 w-8 text-gray-400" />
                ) : (
                  <Upload className="h-8 w-8 text-gray-400" />
                )}
                
                <div className="space-y-1">
                  <p className={cn("font-medium", isMobile ? "text-sm" : "text-base")}>
                    {isMobile ? "Toque para selecionar arquivos" : "Arraste arquivos aqui ou clique para selecionar"}
                  </p>
                  <p className={cn("text-gray-500", isMobile ? "text-xs" : "text-sm")}>
                    PDF, DOC, DOCX, PNG, JPG até {maxFileSize}MB
                  </p>
                </div>
                
                {isMobile && (
                  <div className="text-xs text-gray-400 text-center">
                    Máximo {maxFiles} arquivo{maxFiles > 1 ? 's' : ''}
                  </div>
                )}
              </div>
            </div>
          </CardContent>
        </Card>
      )}

      {/* Camera Mode */}
      {uploadMode === 'camera' && isMobile && hasCamera && (
        <Card>
          <CardContent className="p-6 text-center space-y-4">
            <Camera className="h-12 w-12 text-gray-400 mx-auto" />
            <div className="space-y-2">
              <p className="font-medium">Capturar com Câmera</p>
              <p className="text-sm text-gray-600">
                Tire fotos de cada página do seu contrato
              </p>
            </div>
            <Button onClick={startCamera} className="w-full">
              <Camera className="h-4 w-4 mr-2" />
              Abrir Câmera
            </Button>
          </CardContent>
        </Card>
      )}

      {/* Files Preview */}
      {uploadedFiles.length > 0 && (
        <Card>
          <CardContent className="p-4">
            <div className="flex items-center justify-between mb-3">
              <h4 className="font-medium text-sm">
                Arquivos Selecionados ({uploadedFiles.length})
              </h4>
              <Badge variant="outline" className="text-xs">
                {uploadedFiles.length}/{maxFiles}
              </Badge>
            </div>
            
            <div className="space-y-2">
              {uploadedFiles.map((uploadedFile) => (
                <div 
                  key={uploadedFile.id} 
                  className="flex items-center gap-3 p-2 border rounded-lg"
                >
                  {uploadedFile.type === 'image' && uploadedFile.preview ? (
                    <img
                      src={uploadedFile.preview}
                      alt="Preview"
                      className="w-10 h-10 object-cover rounded"
                    />
                  ) : (
                    <div className="w-10 h-10 bg-gray-100 rounded flex items-center justify-center">
                      {uploadedFile.type === 'pdf' ? (
                        <File className="h-5 w-5 text-red-600" />
                      ) : (
                        <File className="h-5 w-5 text-gray-600" />
                      )}
                    </div>
                  )}
                  
                  <div className="flex-1 min-w-0">
                    <p className="text-sm font-medium truncate">
                      {uploadedFile.file.name}
                    </p>
                    <p className="text-xs text-gray-500">
                      {(uploadedFile.file.size / 1024 / 1024).toFixed(1)} MB
                    </p>
                  </div>
                  
                  <Button
                    onClick={() => removeFile(uploadedFile.id)}
                    variant="ghost"
                    size="sm"
                    className="h-8 w-8 p-0 text-gray-400 hover:text-red-600"
                  >
                    <X className="h-4 w-4" />
                  </Button>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      )}

      {/* Tips for mobile users */}
      {isMobile && (
        <Card className="bg-blue-50 border-blue-200">
          <CardContent className="p-4">
            <div className="flex gap-3">
              <Camera className="h-5 w-5 text-blue-600 mt-0.5 flex-shrink-0" />
              <div className="space-y-1">
                <p className="text-sm font-medium text-blue-900">
                  Dicas para melhor captura:
                </p>
                <ul className="text-xs text-blue-800 space-y-1">
                  <li>• Use boa iluminação natural</li>
                  <li>• Mantenha o documento plano</li>
                  <li>• Capture cada página separadamente</li>
                  <li>• Evite sombras e reflexos</li>
                </ul>
              </div>
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  )
}