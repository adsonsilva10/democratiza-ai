'use client'

import { useState } from 'react'
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Badge } from '@/components/ui/badge'
import { Upload, Users, Send, FileCheck, CheckCircle2, Trash2, Eye, Plus, ArrowLeft, ArrowRight, FileText, User, Mail, IdCard, AlertCircle } from 'lucide-react'

export default function AssinaturaPage() {
  const [activeStep, setActiveStep] = useState<'upload' | 'signers' | 'review' | 'status'>('upload')
  const [selectedFile, setSelectedFile] = useState<File | null>(null)
  const [signers, setSigners] = useState([
    { name: '', email: '', document: '' }
  ])

  const addSigner = () => {
    if (signers.length < 5) {
      setSigners([...signers, { name: '', email: '', document: '' }])
    }
  }

  const removeSigner = (index: number) => {
    if (signers.length > 1) {
      setSigners(signers.filter((_, i) => i !== index))
    }
  }

  const updateSigner = (index: number, field: string, value: string) => {
    const newSigners = [...signers]
    newSigners[index] = { ...newSigners[index], [field]: value }
    setSigners(newSigners)
  }

  const formatCPF = (value: string) => {
    const numbers = value.replace(/\D/g, '')
    return numbers.replace(/(\d{3})(\d{3})(\d{3})(\d{2})/, '$1.$2.$3-$4')
  }

  const handleFileUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0]
    if (file && file.type === 'application/pdf') {
      setSelectedFile(file)
    }
  }

  const steps = [
    { id: 'upload', title: 'Upload', icon: Upload, description: 'Enviar documento' },
    { id: 'signers', title: 'Signatários', icon: Users, description: 'Definir assinantes' },
    { id: 'review', title: 'Revisar', icon: Eye, description: 'Revisar envio' },
    { id: 'status', title: 'Status', icon: FileCheck, description: 'Acompanhar' }
  ]

  const currentStepIndex = steps.findIndex(step => step.id === activeStep)

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-blue-50">
      {/* Header moderno com breadcrumb */}
      <div className="bg-white border-b border-gray-200 px-4 md:px-6 py-4 md:py-6">
        <div className="flex flex-col gap-2">
          <nav className="text-sm text-gray-500">
            <span>Plataforma</span> <span className="mx-2">›</span> <span className="text-gray-900">Assinatura Digital</span>
          </nav>
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="p-2 bg-purple-100 rounded-lg">
                <span className="text-xl text-purple-600">✍️</span>
              </div>
              <div>
                <h1 className="text-xl md:text-2xl font-bold text-gray-900">
                  Assinatura Digital
                </h1>
                <p className="text-sm text-gray-600">
                  Envie documentos para assinatura eletrônica com validade jurídica
                </p>
              </div>
            </div>
            <div className="hidden lg:flex items-center gap-4">
              <Badge variant="secondary" className="bg-green-100 text-green-700">
                ⚡ Assinatura em 2min
              </Badge>
              <Badge variant="secondary" className="bg-blue-100 text-blue-700">
                🛡️ Validade jurídica
              </Badge>
            </div>
          </div>
        </div>
      </div>

      <div className="container mx-auto px-6 md:px-6 py-8 md:py-8">
        <div className="max-w-2xl mx-auto space-y-8 md:space-y-6">
          {/* Progress Steps - Responsivo */}
          <div className="relative flex justify-center">
            {/* Desktop: Horizontal layout */}
            <div className="hidden sm:flex justify-between items-center mb-8 w-full max-w-2xl">
              {steps.map((step, index) => (
                <div key={step.id} className="flex items-center flex-1">
                  <div className="flex flex-col items-center relative">
                    <div className={`w-12 h-12 rounded-full flex items-center justify-center text-sm font-bold transition-all duration-300 ${
                      currentStepIndex >= index 
                        ? 'bg-gradient-to-r from-blue-600 to-blue-700 text-white shadow-lg' 
                        : 'bg-gray-200 text-gray-500'
                    }`}>
                      {currentStepIndex > index ? (
                        <CheckCircle2 className="h-6 w-6" />
                      ) : (
                        <step.icon className="h-5 w-5" />
                      )}
                    </div>
                    <div className="mt-2 text-center">
                      <p className={`text-sm font-medium ${
                        currentStepIndex >= index ? 'text-blue-600' : 'text-gray-500'
                      }`}>
                        {step.title}
                      </p>
                      <p className="text-xs text-gray-400 hidden lg:block">
                        {step.description}
                      </p>
                    </div>
                  </div>
                  {index < steps.length - 1 && (
                    <div className={`flex-1 h-0.5 mx-4 transition-colors duration-300 ${
                      currentStepIndex > index ? 'bg-blue-600' : 'bg-gray-200'
                    }`} />
                  )}
                </div>
              ))}
            </div>

            {/* Mobile: Compact horizontal layout */}
            <div className="flex sm:hidden justify-between items-center mb-8 px-2">
              {steps.map((step, index) => (
                <div key={step.id} className="flex flex-col items-center">
                  <div className={`w-12 h-12 rounded-full flex items-center justify-center text-sm font-bold transition-all duration-300 ${
                    currentStepIndex >= index 
                      ? 'bg-gradient-to-r from-blue-600 to-blue-700 text-white' 
                      : 'bg-gray-200 text-gray-500'
                  }`}>
                    {currentStepIndex > index ? (
                      <CheckCircle2 className="h-5 w-5" />
                    ) : (
                      index + 1
                    )}
                  </div>
                  <p className={`text-sm font-medium mt-2 ${
                    currentStepIndex >= index ? 'text-blue-600' : 'text-gray-500'
                  }`}>
                    {step.title}
                  </p>
                </div>
              ))}
            </div>
          </div>

        {/* Upload Step com área de upload unificada */}
        {activeStep === 'upload' && (
          <Card className="border-2 border-dashed border-gray-300">
            <CardContent 
              className="p-8 md:p-12 text-center transition-colors duration-200"
            >
              {!selectedFile ? (
                <div className="space-y-6">
                  <div className="w-20 h-20 md:w-20 md:h-20 mx-auto bg-gray-100 rounded-full flex items-center justify-center">
                    <Upload className="h-14 w-14 md:h-12 md:w-12 text-gray-400" />
                  </div>
                  <div>
                    {/* Desktop: Arraste seu documento */}
                    <h3 className="hidden md:block text-lg font-semibold text-gray-900 mb-2">
                      Arraste seu documento aqui
                    </h3>
                    {/* Mobile: Selecione seu documento */}
                    <h3 className="md:hidden text-2xl font-semibold text-gray-900 mb-4">
                      Selecione seu documento
                    </h3>
                    
                    <p className="hidden md:block text-gray-500 mb-4">
                      ou clique para selecionar um arquivo
                    </p>
                    <p className="md:hidden text-lg text-gray-600 mb-8">
                      Escolha o PDF para assinatura
                    </p>

                    {/* Desktop: Input direto */}
                    <div className="hidden md:block">
                      <input
                        type="file"
                        id="file-upload"
                        className="hidden"
                        accept=".pdf"
                        onChange={handleFileUpload}
                      />
                      <label htmlFor="file-upload">
                        <Button className="bg-gradient-to-r from-blue-600 to-purple-600">
                          Selecionar Arquivo
                        </Button>
                      </label>
                    </div>

                    {/* Mobile: Botão direto */}
                    <div className="md:hidden">
                      <Button 
                        className="bg-gradient-to-r from-blue-600 to-purple-600 h-14 text-lg px-8 min-w-[200px]"
                        onClick={() => document.getElementById('mobile-file-upload')?.click()}
                      >
                        Selecionar Arquivo
                      </Button>
                      <input
                        type="file"
                        id="mobile-file-upload"
                        className="hidden"
                        accept=".pdf"
                        onChange={handleFileUpload}
                      />
                    </div>
                  </div>
                  <p className="text-base md:text-xs text-gray-500 mt-3">
                    Formatos aceitos: PDF • Máximo 50MB
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
                      onClick={() => setActiveStep('signers')}
                      className="bg-gradient-to-r from-blue-600 to-purple-600 h-14 text-lg px-8 min-w-[180px]"
                    >
                      <Users className="w-6 h-6 mr-3" />
                      Definir Signatários
                    </Button>
                    <Button 
                      variant="outline" 
                      onClick={() => setSelectedFile(null)}
                      className="h-14 text-lg px-8 min-w-[120px]"
                    >
                      Remover Arquivo
                    </Button>
                  </div>
                </div>
              )}
            </CardContent>
          </Card>
        )}

        {/* Upload Guidelines */}
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 mt-6">
          <div className="p-4 bg-blue-50 border border-blue-200 rounded-lg">
            <h4 className="font-medium text-blue-900 mb-2 text-sm flex items-center gap-2">
              📝 Requisitos do arquivo
            </h4>
            <ul className="text-xs text-blue-800 space-y-1">
              <li>• Formato: Apenas PDF</li>
              <li>• Tamanho máximo: 50MB</li>
              <li>• Conteúdo completo e final</li>
            </ul>
          </div>
          
          <div className="p-4 bg-yellow-50 border border-yellow-200 rounded-lg">
            <h4 className="font-medium text-yellow-900 mb-2 text-sm flex items-center gap-2">
              🔒 Segurança
            </h4>
            <ul className="text-xs text-yellow-800 space-y-1">
              <li>• Criptografia de ponta a ponta</li>
              <li>• Validade jurídica garantida</li>
              <li>• Certificado digital ICP-Brasil</li>
            </ul>
          </div>
        </div>

        {/* Signers Step */}
        {activeStep === 'signers' && (
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Users className="h-5 w-5" />
                Definir Signatários
              </CardTitle>
              <CardDescription>
                Adicione as pessoas que precisam assinar o documento
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              {signers.map((signer, index) => (
                <div key={index} className="p-4 border border-gray-200 rounded-lg space-y-4">
                  <div className="flex items-center justify-between">
                    <h4 className="font-medium text-gray-900">
                      Signatário {index + 1}
                    </h4>
                    {signers.length > 1 && (
                      <Button
                        variant="ghost"
                        size="sm"
                        onClick={() => removeSigner(index)}
                        className="text-red-600 hover:text-red-700"
                      >
                        <Trash2 className="h-4 w-4" />
                      </Button>
                    )}
                  </div>
                  
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">
                        Nome Completo
                      </label>
                      <Input
                        placeholder="Digite o nome completo"
                        value={signer.name}
                        onChange={(e) => updateSigner(index, 'name', e.target.value)}
                      />
                    </div>
                    
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">
                        E-mail
                      </label>
                      <Input
                        type="email"
                        placeholder="email@exemplo.com"
                        value={signer.email}
                        onChange={(e) => updateSigner(index, 'email', e.target.value)}
                      />
                    </div>
                  </div>
                  
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      CPF
                    </label>
                    <Input
                      placeholder="000.000.000-00"
                      value={signer.document}
                      onChange={(e) => updateSigner(index, 'document', formatCPF(e.target.value))}
                      maxLength={14}
                    />
                  </div>
                </div>
              ))}
              
              {signers.length < 5 && (
                <Button
                  variant="outline"
                  onClick={addSigner}
                  className="w-full"
                >
                  <Plus className="h-4 w-4 mr-2" />
                  Adicionar Signatário
                </Button>
              )}
              
              <div className="flex gap-4 pt-4">
                <Button
                  variant="outline"
                  onClick={() => setActiveStep('upload')}
                  className="flex-1"
                >
                  <ArrowLeft className="h-4 w-4 mr-2" />
                  Voltar
                </Button>
                <Button
                  onClick={() => setActiveStep('review')}
                  className="flex-1 bg-gradient-to-r from-blue-600 to-purple-600"
                  disabled={signers.some(s => !s.name || !s.email || !s.document)}
                >
                  Continuar
                  <ArrowRight className="h-4 w-4 ml-2" />
                </Button>
              </div>
            </CardContent>
          </Card>
        )}

        {/* Review Step */}
        {activeStep === 'review' && (
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Eye className="h-5 w-5" />
                Revisar Envio
              </CardTitle>
              <CardDescription>
                Confirme os dados antes de enviar para assinatura
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              <div className="p-4 bg-gray-50 rounded-lg">
                <h4 className="font-medium text-gray-900 mb-2">Documento</h4>
                <p className="text-gray-600">{selectedFile?.name}</p>
                <p className="text-sm text-gray-500">
                  {(selectedFile!.size / 1024 / 1024).toFixed(1)} MB
                </p>
              </div>
              
              <div className="space-y-4">
                <h4 className="font-medium text-gray-900">Signatários</h4>
                {signers.map((signer, index) => (
                  <div key={index} className="p-4 border border-gray-200 rounded-lg">
                    <div className="flex items-center gap-2 mb-2">
                      <User className="h-4 w-4 text-gray-500" />
                      <span className="font-medium">{signer.name}</span>
                    </div>
                    <div className="flex items-center gap-2 text-sm text-gray-600">
                      <Mail className="h-4 w-4" />
                      {signer.email}
                    </div>
                    <div className="flex items-center gap-2 text-sm text-gray-600 mt-1">
                      <IdCard className="h-4 w-4" />
                      {signer.document}
                    </div>
                  </div>
                ))}
              </div>
              
              <div className="p-4 bg-yellow-50 border border-yellow-200 rounded-lg">
                <div className="flex items-start gap-2">
                  <AlertCircle className="h-5 w-5 text-yellow-600 mt-0.5" />
                  <div>
                    <h4 className="font-medium text-yellow-900">Importante</h4>
                    <p className="text-sm text-yellow-800 mt-1">
                      Após o envio, todos os signatários receberão um e-mail com o link para assinatura.
                      O processo só será concluído quando todas as assinaturas forem coletadas.
                    </p>
                  </div>
                </div>
              </div>
              
              <div className="flex gap-4">
                <Button
                  variant="outline"
                  onClick={() => setActiveStep('signers')}
                  className="flex-1"
                >
                  <ArrowLeft className="h-4 w-4 mr-2" />
                  Voltar
                </Button>
                <Button
                  onClick={() => setActiveStep('status')}
                  className="flex-1 bg-gradient-to-r from-green-600 to-blue-600"
                >
                  <Send className="h-4 w-4 mr-2" />
                  Enviar para Assinatura
                </Button>
              </div>
            </CardContent>
          </Card>
        )}

        {/* Status Step */}
        {activeStep === 'status' && (
          <Card>
            <CardHeader className="text-center">
              <div className="w-16 h-16 mx-auto bg-green-100 rounded-full flex items-center justify-center mb-4">
                <CheckCircle2 className="h-8 w-8 text-green-600" />
              </div>
              <CardTitle className="text-green-900">Documento Enviado!</CardTitle>
              <CardDescription>
                Seu documento foi enviado para assinatura com sucesso
              </CardDescription>
            </CardHeader>
            <CardContent className="text-center space-y-4">
              <div className="p-4 bg-green-50 border border-green-200 rounded-lg">
                <p className="text-green-800">
                  Todos os signatários receberão um e-mail com instruções para assinar o documento.
                  Você será notificado quando todas as assinaturas forem coletadas.
                </p>
              </div>
              
              <div className="space-y-2">
                <p className="text-sm text-gray-600">ID do Processo:</p>
                <p className="font-mono text-lg font-bold text-gray-900">
                  ASS-{Date.now().toString().slice(-8)}
                </p>
              </div>
              
              <Button
                onClick={() => {
                  setActiveStep('upload')
                  setSelectedFile(null)
                  setSigners([{ name: '', email: '', document: '' }])
                }}
                className="w-full bg-gradient-to-r from-blue-600 to-purple-600"
              >
                Enviar Novo Documento
              </Button>
            </CardContent>
          </Card>
        )}
        </div>
      </div>
    </div>
  )
}