'use client'

import { useState, useCallback } from 'react'
import { useRouter } from 'next/navigation'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Upload, FileText, Scan, Zap, Clock, Shield, AlertCircle, Camera, FolderOpen, X } from 'lucide-react'





export default function AnalisePage() {
  const [dragActive, setDragActive] = useState(false)
  const [selectedFile, setSelectedFile] = useState<File | null>(null)
  const [isAnalyzing, setIsAnalyzing] = useState(false)
  const [showMobileModal, setShowMobileModal] = useState(false)
  // Simulando tipo de usuário - em produção viria do contexto/API
  const [userType, setUserType] = useState<'free' | 'basic' | 'premium'>('free')
  const router = useRouter()

  const handleDrag = useCallback((e: React.DragEvent) => {
    e.preventDefault()
    e.stopPropagation()
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true)
    } else if (e.type === 'dragleave') {
      setDragActive(false)
    }
  }, [])

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault()
    e.stopPropagation()
    setDragActive(false)
    
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      setSelectedFile(e.dataTransfer.files[0])
    }
  }, [])

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setSelectedFile(e.target.files[0])
    }
  }

  const handleCameraCapture = () => {
    setShowMobileModal(false)
    // Implementar captura de câmera
    const input = document.createElement('input')
    input.type = 'file'
    input.accept = 'image/*'
    input.capture = 'environment'
    input.onchange = (e) => {
      const file = (e.target as HTMLInputElement).files?.[0]
      if (file) setSelectedFile(file)
    }
    input.click()
  }

  const handleMobileFileSelect = () => {
    setShowMobileModal(false)
    document.getElementById('mobile-file-upload')?.click()
  }

  const startAnalysis = async () => {
    if (!selectedFile) return
    setIsAnalyzing(true)
    setTimeout(() => {
      router.push('/plataforma/analise/resultado')
    }, 3000)
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-blue-50">
      <div className="bg-white border-b border-gray-200 px-4 md:px-6 py-4">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-xl md:text-3xl font-bold text-gray-900">
              Nova Análise de Contrato
            </h1>
            <p className="text-sm md:text-base text-gray-600 mt-1">
              Analise contratos com IA especializada em direito brasileiro
            </p>
          </div>
          <div className="hidden lg:flex items-center gap-4">
            <Badge variant="secondary" className="bg-green-100 text-green-700">
              ⚡ Análise em 45s
            </Badge>
            <Badge variant="secondary" className="bg-blue-100 text-blue-700">
              🛡️ 98.7% de precisão
            </Badge>
          </div>
        </div>
      </div>

      <div className="container mx-auto px-6 md:px-6 py-8 md:py-8">
        <div className="max-w-2xl mx-auto space-y-8 md:space-y-6">
          {/* Progress Steps - Como Funciona */}
          <div className="relative flex justify-center">
            {/* Desktop: Horizontal layout */}
            <div className="hidden sm:flex justify-between items-center mb-8 w-full max-w-2xl">
              <div className="flex items-center flex-1">
                <div className="flex flex-col items-center relative">
                  <div className="w-12 h-12 rounded-full flex items-center justify-center text-sm font-bold transition-all duration-300 bg-gradient-to-r from-blue-600 to-blue-700 text-white shadow-lg">
                    📤
                  </div>
                  <div className="mt-2 text-center">
                    <p className="text-sm font-medium text-blue-600">
                      Upload
                    </p>
                    <p className="text-xs text-gray-400 hidden lg:block">
                      Envie arquivo
                    </p>
                  </div>
                </div>
                <div className="flex-1 h-0.5 mx-4 transition-colors duration-300 bg-blue-600" />
              </div>

              <div className="flex items-center flex-1">
                <div className="flex flex-col items-center relative">
                  <div className="w-12 h-12 rounded-full flex items-center justify-center text-sm font-bold transition-all duration-300 bg-gradient-to-r from-blue-600 to-blue-700 text-white shadow-lg">
                    🤖
                  </div>
                  <div className="mt-2 text-center">
                    <p className="text-sm font-medium text-blue-600">
                      IA Analisa
                    </p>
                    <p className="text-xs text-gray-400 hidden lg:block">
                      Claude processa
                    </p>
                  </div>
                </div>
                <div className="flex-1 h-0.5 mx-4 transition-colors duration-300 bg-blue-600" />
              </div>

              <div className="flex items-center">
                <div className="flex flex-col items-center relative">
                  <div className="w-12 h-12 rounded-full flex items-center justify-center text-sm font-bold transition-all duration-300 bg-gradient-to-r from-blue-600 to-blue-700 text-white shadow-lg">
                    📊
                  </div>
                  <div className="mt-2 text-center">
                    <p className="text-sm font-medium text-blue-600">
                      Relatório
                    </p>
                    <p className="text-xs text-gray-400 hidden lg:block">
                      Receba alertas
                    </p>
                  </div>
                </div>
              </div>
            </div>

            {/* Mobile: Compact horizontal layout */}
            <div className="flex sm:hidden justify-between items-center mb-8 px-2">
              <div className="flex flex-col items-center">
                <div className="w-12 h-12 rounded-full flex items-center justify-center text-sm font-bold transition-all duration-300 bg-gradient-to-r from-blue-600 to-blue-700 text-white">
                  📤
                </div>
                <p className="text-sm font-medium mt-2 text-blue-600">
                  Upload
                </p>
              </div>

              <div className="flex flex-col items-center">
                <div className="w-12 h-12 rounded-full flex items-center justify-center text-sm font-bold transition-all duration-300 bg-gradient-to-r from-blue-600 to-blue-700 text-white">
                  🤖
                </div>
                <p className="text-sm font-medium mt-2 text-blue-600">
                  IA Analisa
                </p>
              </div>

              <div className="flex flex-col items-center">
                <div className="w-12 h-12 rounded-full flex items-center justify-center text-sm font-bold transition-all duration-300 bg-gradient-to-r from-blue-600 to-blue-700 text-white">
                  📊
                </div>
                <p className="text-sm font-medium mt-2 text-blue-600">
                  Relatório
                </p>
              </div>
            </div>
          </div>
            
            {/* Upload Area */}
            <Card className="border-2 border-dashed border-gray-300">
              <CardContent 
                className={dragActive 
                  ? 'p-8 md:p-12 text-center bg-blue-50 border-blue-400 transition-colors duration-200' 
                  : 'p-8 md:p-12 text-center transition-colors duration-200'
                }
                onDragEnter={handleDrag}
                onDragLeave={handleDrag}
                onDragOver={handleDrag}
                onDrop={handleDrop}
              >
                {!selectedFile ? (
                  <div className="space-y-6">
                    <div className="w-20 h-20 md:w-20 md:h-20 mx-auto bg-gray-100 rounded-full flex items-center justify-center">
                      <Upload className="h-14 w-14 md:h-12 md:w-12 text-gray-400" />
                    </div>
                    <div>
                      {/* Desktop: Arraste seu contrato */}
                      <h3 className="hidden md:block text-lg font-semibold text-gray-900 mb-2">
                        Arraste seu contrato aqui
                      </h3>
                      {/* Mobile: Selecione seu contrato */}
                      <h3 className="md:hidden text-2xl font-semibold text-gray-900 mb-4">
                        Selecione seu contrato
                      </h3>
                      
                      <p className="hidden md:block text-gray-500 mb-4">
                        ou clique para selecionar um arquivo
                      </p>
                      <p className="md:hidden text-lg text-gray-600 mb-8">
                        Escolha entre câmera ou arquivo
                      </p>

                      {/* Desktop: Input direto */}
                      <div className="hidden md:block">
                        <input
                          type="file"
                          id="file-upload"
                          className="hidden"
                          accept=".pdf,.doc,.docx"
                          onChange={handleFileSelect}
                        />
                        <label htmlFor="file-upload">
                          <Button className="bg-gradient-to-r from-blue-600 to-purple-600">
                            Selecionar Arquivo
                          </Button>
                        </label>
                      </div>

                      {/* Mobile: Modal com opções */}
                      <div className="md:hidden">
                        <Button 
                          className="bg-gradient-to-r from-blue-600 to-purple-600 h-14 text-lg px-8 min-w-[200px]"
                          onClick={() => setShowMobileModal(true)}
                        >
                          Selecionar Arquivo
                        </Button>
                        <input
                          type="file"
                          id="mobile-file-upload"
                          className="hidden"
                          accept=".pdf,.doc,.docx,image/*"
                          onChange={handleFileSelect}
                        />
                      </div>
                    </div>
                    <p className="text-base md:text-xs text-gray-500 mt-3">
                      Formatos aceitos: PDF, DOC, DOCX • Máximo 10MB
                    </p>
                  </div>
                ) : (
                  <div className="space-y-6">
                    <div className="w-20 h-20 md:w-20 md:h-20 mx-auto bg-green-100 rounded-full flex items-center justify-center">
                      <FileText className="h-14 w-14 md:h-12 md:w-12 text-green-600" />
                    </div>
                    <div>
                      <h3 className="text-2xl md:text-lg font-semibold text-gray-900 break-all">
                        {selectedFile.name}
                      </h3>
                      <p className="text-lg md:text-base text-gray-600 mt-2">
                        {(selectedFile.size / 1024 / 1024).toFixed(1)} MB
                      </p>
                    </div>
                    <div className="flex flex-col sm:flex-row gap-4 justify-center">
                      <Button 
                        onClick={startAnalysis}
                        disabled={isAnalyzing}
                        className="bg-gradient-to-r from-blue-600 to-purple-600 h-14 text-lg px-8 min-w-[180px]"
                      >
                        {isAnalyzing ? (
                          <>
                            <div className="w-6 h-6 border-2 border-white border-t-transparent rounded-full animate-spin mr-3" />
                            Analisando...
                          </>
                        ) : (
                          <>
                            <Zap className="w-6 h-6 mr-3" />
                            Iniciar Análise
                          </>
                        )}
                      </Button>
                      <Button 
                        variant="outline" 
                        onClick={() => setSelectedFile(null)}
                        disabled={isAnalyzing}
                        className="h-14 text-lg px-8 min-w-[120px]"
                      >
                        Remover
                      </Button>
                    </div>
                  </div>
                )}
              </CardContent>
            </Card>
            {/* Upgrade de Planos - Apenas para usuários free/basic */}
            {(userType === 'free' || userType === 'basic') && (
              <Card className="bg-gradient-to-r from-blue-600 to-purple-600 text-white">
                <CardContent className="p-8 md:p-6 text-center">
                  <h3 className="font-bold text-2xl md:text-lg mb-4 md:mb-2">
                    {userType === 'free' ? 'Análises Ilimitadas' : 'Upgrade Premium'}
                  </h3>
                  <p className="text-lg md:text-sm opacity-90 mb-8 md:mb-4">
                    {userType === 'free' 
                      ? 'Comece com plano básico para mais funcionalidades'
                      : 'Upgrade para Premium e analise quantos contratos quiser'
                    }
                  </p>
                  <Button 
                    variant="secondary" 
                    className="w-full bg-white text-blue-600 hover:bg-gray-100 h-14 text-lg min-h-[56px]"
                    onClick={() => router.push('/plataforma/planos')}
                  >
                    Ver Planos
                  </Button>
                </CardContent>
              </Card>
            )}
        </div>
      </div>

      {/* Modal Mobile */}
      {showMobileModal && (
        <div className="md:hidden fixed inset-0 bg-black/50 z-50 flex items-end">
          <div className="bg-white w-full rounded-t-xl p-8 space-y-8">
            <div className="flex items-center justify-between">
              <h3 className="text-2xl font-semibold">Selecionar Arquivo</h3>
              <Button 
                variant="ghost" 
                className="h-12 w-12 p-0 min-h-[48px] min-w-[48px]"
                onClick={() => setShowMobileModal(false)}
              >
                <X className="h-8 w-8" />
              </Button>
            </div>
            
            <div className="space-y-6">
              <Button 
                className="w-full flex items-center gap-6 justify-start h-20 px-6"
                variant="outline"
                onClick={handleCameraCapture}
              >
                <Camera className="h-8 w-8" />
                <div className="text-left">
                  <div className="font-medium text-lg">Câmera</div>
                  <div className="text-base text-gray-500">Fotografar documento</div>
                </div>
              </Button>
              
              <Button 
                className="w-full flex items-center gap-6 justify-start h-20 px-6"
                variant="outline"
                onClick={handleMobileFileSelect}
              >
                <FolderOpen className="h-8 w-8" />
                <div className="text-left">
                  <div className="font-medium text-lg">Arquivo</div>
                  <div className="text-base text-gray-500">Escolher da galeria</div>
                </div>
              </Button>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
