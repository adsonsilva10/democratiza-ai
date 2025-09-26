'use client'

import { useState, useRef, useCallback, useEffect } from 'react'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Camera, RotateCcw, Check, X, Plus, Trash2 } from 'lucide-react'
import { cn } from '@/lib/utils'

interface CapturedImage {
  id: string
  dataUrl: string
  timestamp: Date
  file: File
}

interface MobileCameraCaptureProps {
  onImagesCapture: (files: File[]) => void
  onCancel: () => void
  maxImages?: number
  className?: string
}

export function MobileCameraCapture({ 
  onImagesCapture, 
  onCancel, 
  maxImages = 10,
  className 
}: MobileCameraCaptureProps) {
  const [stream, setStream] = useState<MediaStream | null>(null)
  const [isCapturing, setIsCapturing] = useState(false)
  const [capturedImages, setCapturedImages] = useState<CapturedImage[]>([])
  const [facingMode, setFacingMode] = useState<'user' | 'environment'>('environment')
  const [error, setError] = useState<string | null>(null)
  
  const videoRef = useRef<HTMLVideoElement>(null)
  const canvasRef = useRef<HTMLCanvasElement>(null)

  // Inicializar câmera
  const initializeCamera = useCallback(async () => {
    try {
      setError(null)
      
      if (stream) {
        stream.getTracks().forEach(track => track.stop())
      }

      const constraints = {
        video: {
          facingMode,
          width: { ideal: 1920, max: 2560 },
          height: { ideal: 1080, max: 1440 }
        }
      }

      const mediaStream = await navigator.mediaDevices.getUserMedia(constraints)
      setStream(mediaStream)
      
      if (videoRef.current) {
        videoRef.current.srcObject = mediaStream
      }
    } catch (err) {
      console.error('Erro ao acessar câmera:', err)
      setError('Não foi possível acessar a câmera. Verifique as permissões.')
    }
  }, [facingMode, stream])

  // Cleanup stream
  const cleanupStream = useCallback(() => {
    if (stream) {
      stream.getTracks().forEach(track => track.stop())
      setStream(null)
    }
  }, [stream])

  // Alternar câmera (frontal/traseira)
  const toggleCamera = useCallback(() => {
    setFacingMode(prev => prev === 'user' ? 'environment' : 'user')
  }, [])

  // Capturar foto
  const capturePhoto = useCallback(() => {
    if (!videoRef.current || !canvasRef.current) return

    const video = videoRef.current
    const canvas = canvasRef.current
    const context = canvas.getContext('2d')

    if (!context) return

    // Configurar canvas com dimensões do vídeo
    canvas.width = video.videoWidth
    canvas.height = video.videoHeight

    // Desenhar frame atual do vídeo no canvas
    context.drawImage(video, 0, 0, canvas.width, canvas.height)

    // Converter para blob e criar File
    canvas.toBlob((blob) => {
      if (!blob) return

      const timestamp = new Date()
      const fileName = `contract-page-${capturedImages.length + 1}-${timestamp.getTime()}.jpg`
      const file = new File([blob], fileName, { type: 'image/jpeg' })
      
      const dataUrl = canvas.toDataURL('image/jpeg', 0.9)
      
      const newImage: CapturedImage = {
        id: crypto.randomUUID(),
        dataUrl,
        timestamp,
        file
      }

      setCapturedImages(prev => [...prev, newImage])
    }, 'image/jpeg', 0.9)
  }, [capturedImages.length])

  // Remover imagem
  const removeImage = useCallback((imageId: string) => {
    setCapturedImages(prev => prev.filter(img => img.id !== imageId))
  }, [])

  // Finalizar captura
  const finishCapture = useCallback(() => {
    if (capturedImages.length === 0) return
    
    const files = capturedImages.map(img => img.file)
    onImagesCapture(files)
    cleanupStream()
  }, [capturedImages, onImagesCapture, cleanupStream])

  // Cancelar captura
  const handleCancel = useCallback(() => {
    cleanupStream()
    onCancel()
  }, [cleanupStream, onCancel])

  // Inicializar câmera ao montar componente
  useEffect(() => {
    initializeCamera()
    return cleanupStream
  }, [initializeCamera, cleanupStream])

  // Re-inicializar quando mudar modo da câmera
  useEffect(() => {
    if (stream) {
      initializeCamera()
    }
  }, [facingMode, initializeCamera, stream])

  if (error) {
    return (
      <Card className={cn("w-full max-w-md mx-auto", className)}>
        <CardHeader>
          <CardTitle className="text-center text-red-600">Erro na Câmera</CardTitle>
        </CardHeader>
        <CardContent className="text-center space-y-4">
          <p className="text-sm text-gray-600">{error}</p>
          <div className="flex gap-2 justify-center">
            <Button onClick={initializeCamera} variant="outline" size="sm">
              Tentar Novamente
            </Button>
            <Button onClick={handleCancel} variant="secondary" size="sm">
              Cancelar
            </Button>
          </div>
        </CardContent>
      </Card>
    )
  }

  return (
    <div className={cn("w-full max-w-md mx-auto space-y-4", className)}>
      {/* Camera Preview */}
      <Card>
        <CardHeader className="pb-2">
          <div className="flex items-center justify-between">
            <CardTitle className="text-sm font-medium">
              Capturar Contrato
            </CardTitle>
            <Badge variant="secondary" className="text-xs">
              {capturedImages.length}/{maxImages}
            </Badge>
          </div>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="relative rounded-lg overflow-hidden bg-black aspect-[4/3]">
            <video
              ref={videoRef}
              autoPlay
              playsInline
              muted
              className="w-full h-full object-cover"
            />
            
            {/* Overlay Guide */}
            <div className="absolute inset-4 border-2 border-white border-dashed rounded-lg opacity-50" />
            
            {/* Camera Controls */}
            <div className="absolute bottom-4 left-1/2 transform -translate-x-1/2 flex items-center gap-4">
              <Button
                onClick={toggleCamera}
                variant="secondary"
                size="sm"
                className="bg-black/50 hover:bg-black/70 text-white border-white/20"
              >
                <RotateCcw className="h-4 w-4" />
              </Button>
              
              <Button
                onClick={capturePhoto}
                disabled={capturedImages.length >= maxImages}
                className="bg-white hover:bg-gray-100 text-black rounded-full w-14 h-14 p-0"
              >
                <Camera className="h-6 w-6" />
              </Button>
              
              <div className="w-8" /> {/* Spacer for symmetry */}
            </div>
          </div>

          <p className="text-xs text-gray-500 text-center">
            Posicione o documento dentro da área tracejada e toque no botão de câmera
          </p>
        </CardContent>
      </Card>

      {/* Captured Images Preview */}
      {capturedImages.length > 0 && (
        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium">
              Páginas Capturadas ({capturedImages.length})
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-3 gap-2 mb-4">
              {capturedImages.map((image, index) => (
                <div key={image.id} className="relative group">
                  <img
                    src={image.dataUrl}
                    alt={`Página ${index + 1}`}
                    className="w-full aspect-[3/4] object-cover rounded border"
                  />
                  <div className="absolute inset-0 bg-black/50 opacity-0 group-hover:opacity-100 transition-opacity rounded flex items-center justify-center">
                    <Button
                      onClick={() => removeImage(image.id)}
                      variant="destructive"
                      size="sm"
                      className="w-8 h-8 p-0"
                    >
                      <Trash2 className="h-4 w-4" />
                    </Button>
                  </div>
                  <Badge className="absolute top-1 left-1 text-xs">
                    {index + 1}
                  </Badge>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      )}

      {/* Action Buttons */}
      <div className="flex gap-2">
        <Button
          onClick={handleCancel}
          variant="outline"
          className="flex-1"
        >
          <X className="h-4 w-4 mr-2" />
          Cancelar
        </Button>
        
        {capturedImages.length < maxImages && (
          <Button
            onClick={capturePhoto}
            variant="secondary"
            className="flex-1"
          >
            <Plus className="h-4 w-4 mr-2" />
            Mais Páginas
          </Button>
        )}
        
        <Button
          onClick={finishCapture}
          disabled={capturedImages.length === 0}
          className="flex-1"
        >
          <Check className="h-4 w-4 mr-2" />
          Concluir ({capturedImages.length})
        </Button>
      </div>

      {/* Hidden canvas for image capture */}
      <canvas ref={canvasRef} className="hidden" />
    </div>
  )
}