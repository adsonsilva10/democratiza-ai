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

      <div className="container mx-auto px-4 md:px-6 py-6 md:py-8">
        <div className="max-w-2xl mx-auto space-y-6">
            
            {/* Upload Area */}
            <Card className="border-2 border-dashed border-gray-300">
              <CardContent 
                className={dragActive 
                  ? 'p-6 md:p-12 text-center bg-blue-50 border-blue-400 transition-colors duration-200' 
                  : 'p-6 md:p-12 text-center transition-colors duration-200'
                }
                onDragEnter={handleDrag}
                onDragLeave={handleDrag}
                onDragOver={handleDrag}
                onDrop={handleDrop}
              >
                {!selectedFile ? (
                  <div className="space-y-4">
                    <div className="w-16 h-16 mx-auto bg-gray-100 rounded-full flex items-center justify-center">
                      <Upload className="h-8 w-8 text-gray-400" />
                    </div>
                    <div>
                      {/* Desktop: Arraste seu contrato */}
                      <h3 className="hidden md:block text-lg font-semibold text-gray-900 mb-2">
                        Arraste seu contrato aqui
                      </h3>
                      {/* Mobile: Selecione seu contrato */}
                      <h3 className="md:hidden text-lg font-semibold text-gray-900 mb-2">
                        Selecione seu contrato
                      </h3>
                      
                      <p className="hidden md:block text-gray-500 mb-4">
                        ou clique para selecionar um arquivo
                      </p>
                      <p className="md:hidden text-gray-500 mb-4">
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
                          className="bg-gradient-to-r from-blue-600 to-purple-600"
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
                    <p className="text-xs text-gray-400">
                      Formatos aceitos: PDF, DOC, DOCX • Máximo 10MB
                    </p>
                  </div>
                ) : (
                  <div className="space-y-4">
                    <div className="w-16 h-16 mx-auto bg-green-100 rounded-full flex items-center justify-center">
                      <FileText className="h-8 w-8 text-green-600" />
                    </div>
                    <div>
                      <h3 className="text-lg font-semibold text-gray-900">
                        {selectedFile.name}
                      </h3>
                      <p className="text-gray-500">
                        {(selectedFile.size / 1024 / 1024).toFixed(1)} MB
                      </p>
                    </div>
                    <div className="flex flex-col sm:flex-row gap-3 justify-center">
                      <Button 
                        onClick={startAnalysis}
                        disabled={isAnalyzing}
                        className="bg-gradient-to-r from-blue-600 to-purple-600"
                      >
                        {isAnalyzing ? (
                          <>
                            <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin mr-2" />
                            Analisando...
                          </>
                        ) : (
                          <>
                            <Zap className="w-4 h-4 mr-2" />
                            Iniciar Análise
                          </>
                        )}
                      </Button>
                      <Button 
                        variant="outline" 
                        onClick={() => setSelectedFile(null)}
                        disabled={isAnalyzing}
                      >
                        Remover
                      </Button>
                    </div>
                  </div>
                )}
              </CardContent>
            </Card>
            {/* Como Funciona */}
            <Card>
              <CardHeader>
                <CardTitle className="text-lg text-center">Como Funciona</CardTitle>
              </CardHeader>
              <CardContent className="px-4 md:px-6">
                {/* Mobile: Layout vertical compacto */}
                <div className="md:hidden space-y-3">
                  <div className="flex items-center gap-3">
                    <div className="w-8 h-8 bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-full flex items-center justify-center text-xs flex-shrink-0">
                      📤
                    </div>
                    <div className="flex-1">
                      <h4 className="font-semibold text-sm text-gray-900">Upload</h4>
                      <p className="text-xs text-gray-500">Envie seu arquivo</p>
                    </div>
                  </div>
                  
                  <div className="flex items-center gap-3">
                    <div className="w-8 h-8 bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-full flex items-center justify-center text-xs flex-shrink-0">
                      🤖
                    </div>
                    <div className="flex-1">
                      <h4 className="font-semibold text-sm text-gray-900">IA Analisa</h4>
                      <p className="text-xs text-gray-500">Claude processa</p>
                    </div>
                  </div>
                  
                  <div className="flex items-center gap-3">
                    <div className="w-8 h-8 bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-full flex items-center justify-center text-xs flex-shrink-0">
                      �
                    </div>
                    <div className="flex-1">
                      <h4 className="font-semibold text-sm text-gray-900">Relatório</h4>
                      <p className="text-xs text-gray-500">Receba alertas</p>
                    </div>
                  </div>
                </div>

                {/* Desktop: Layout horizontal */}
                <div className="hidden md:block">
                  <div className="flex items-center justify-center">
                    {/* Passo 1 */}
                    <div className="flex-1 text-center">
                      <div className="w-12 h-12 mx-auto bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-full flex items-center justify-center font-bold text-sm mb-2">
                        📤
                      </div>
                      <h4 className="font-semibold text-sm text-gray-900">Upload</h4>
                      <p className="text-xs text-gray-500 mt-0.5">Envie arquivo</p>
                    </div>

                    {/* Seta 1 */}
                    <div className="flex-shrink-0 px-4">
                      <div className="w-8 h-0.5 bg-gray-300"></div>
                    </div>

                    {/* Passo 2 */}
                    <div className="flex-1 text-center">
                      <div className="w-12 h-12 mx-auto bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-full flex items-center justify-center font-bold text-sm mb-2">
                        🤖
                      </div>
                      <h4 className="font-semibold text-sm text-gray-900">IA Analisa</h4>
                      <p className="text-xs text-gray-500 mt-0.5">Claude processa</p>
                    </div>

                    {/* Seta 2 */}
                    <div className="flex-shrink-0 px-4">
                      <div className="w-8 h-0.5 bg-gray-300"></div>
                    </div>

                    {/* Passo 3 */}
                    <div className="flex-1 text-center">
                      <div className="w-12 h-12 mx-auto bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-full flex items-center justify-center font-bold text-sm mb-2">
                        📊
                      </div>
                      <h4 className="font-semibold text-sm text-gray-900">Relatório</h4>
                      <p className="text-xs text-gray-500 mt-0.5">Receba alertas</p>
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Upgrade de Planos - Apenas para usuários free/basic */}
            {(userType === 'free' || userType === 'basic') && (
              <Card className="bg-gradient-to-r from-blue-600 to-purple-600 text-white">
                <CardContent className="p-6 text-center">
                  <h3 className="font-bold text-lg mb-2">
                    {userType === 'free' ? 'Análises Ilimitadas' : 'Upgrade Premium'}
                  </h3>
                  <p className="text-sm opacity-90 mb-4">
                    {userType === 'free' 
                      ? 'Comece com plano básico para mais funcionalidades'
                      : 'Upgrade para Premium e analise quantos contratos quiser'
                    }
                  </p>
                  <Button 
                    variant="secondary" 
                    className="w-full bg-white text-blue-600 hover:bg-gray-100"
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
          <div className="bg-white w-full rounded-t-xl p-6 space-y-4">
            <div className="flex items-center justify-between">
              <h3 className="text-lg font-semibold">Selecionar Arquivo</h3>
              <Button 
                variant="ghost" 
                size="sm"
                onClick={() => setShowMobileModal(false)}
              >
                <X className="h-4 w-4" />
              </Button>
            </div>
            
            <div className="space-y-3">
              <Button 
                className="w-full flex items-center gap-3 justify-start h-12"
                variant="outline"
                onClick={handleCameraCapture}
              >
                <Camera className="h-5 w-5" />
                <div className="text-left">
                  <div className="font-medium">Câmera</div>
                  <div className="text-xs text-gray-500">Fotografar documento</div>
                </div>
              </Button>
              
              <Button 
                className="w-full flex items-center gap-3 justify-start h-12"
                variant="outline"
                onClick={handleMobileFileSelect}
              >
                <FolderOpen className="h-5 w-5" />
                <div className="text-left">
                  <div className="font-medium">Arquivo</div>
                  <div className="text-xs text-gray-500">Escolher da galeria</div>
                </div>
              </Button>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
