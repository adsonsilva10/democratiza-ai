"use client";

import { useState, useEffect } from "react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { useApi } from "@/lib/hooks/useApi";

// Ícones simples usando emojis
const Upload = () => <span>📤</span>;
const Users = () => <span>👥</span>;
const FileText = () => <span>📄</span>;
const CheckCircle = () => <span>✅</span>;
const Clock = () => <span>⏰</span>;
const X = () => <span>❌</span>;
const Download = () => <span>⬇️</span>;
const Plus = () => <span>➕</span>;
const Trash = () => <span>🗑️</span>;

interface Signer {
  name: string;
  email: string;
  document: string;
  phone: string;
}

interface SignatureRequest {
  id: string;
  document_name: string;
  status: string;
  signers_completed: number;
  signers_total: number;
  progress_percentage: number;
  created_at: string;
  completed_at?: string;
  expires_at?: string;
}

const statusColors = {
  draft: "bg-gray-100 text-gray-800",
  sent: "bg-blue-100 text-blue-800",
  signed: "bg-green-100 text-green-800",
  cancelled: "bg-red-100 text-red-800",
  expired: "bg-orange-100 text-orange-800",
};

const statusLabels = {
  draft: "Rascunho",
  sent: "Enviado",
  signed: "Assinado",
  cancelled: "Cancelado", 
  expired: "Expirado",
};

export default function AssinaturaPage() {
  const { apiRequest } = useApi();
  const [activeStep, setActiveStep] = useState<'upload' | 'signers' | 'send' | 'status'>('upload');
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [signers, setSigners] = useState<Signer[]>([
    { name: "", email: "", document: "", phone: "" }
  ]);
  const [signatureRequests, setSignatureRequests] = useState<SignatureRequest[]>([]);
  const [loading, setLoading] = useState(false);
  const [creatingRequest, setCreatingRequest] = useState(false);

  useEffect(() => {
    loadSignatureRequests();
  }, []);

  const loadSignatureRequests = async () => {
    try {
      const response = await apiRequest("/api/v1/signatures/user/requests");
      
      if (response.success) {
        setSignatureRequests(response.data.data || []);
      }
    } catch (error) {
      console.error("Erro ao carregar solicitações:", error);
    }
  };

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file && file.type === "application/pdf") {
      setSelectedFile(file);
      setActiveStep('signers');
    } else {
      alert("Por favor, selecione um arquivo PDF válido.");
    }
  };

  const addSigner = () => {
    setSigners([...signers, { name: "", email: "", document: "", phone: "" }]);
  };

  const removeSigner = (index: number) => {
    if (signers.length > 1) {
      setSigners(signers.filter((_, i) => i !== index));
    }
  };

  const updateSigner = (index: number, field: keyof Signer, value: string) => {
    const updatedSigners = signers.map((signer, i) => 
      i === index ? { ...signer, [field]: value } : signer
    );
    setSigners(updatedSigners);
  };

  const validateCPF = (cpf: string) => {
    const cleanCPF = cpf.replace(/\D/g, '');
    return cleanCPF.length === 11;
  };

  const formatCPF = (value: string) => {
    const numbers = value.replace(/\D/g, '');
    return numbers.replace(/(\d{3})(\d{3})(\d{3})(\d{2})/, '$1.$2.$3-$4');
  };

  const formatPhone = (value: string) => {
    const numbers = value.replace(/\D/g, '');
    return numbers.replace(/(\d{2})(\d{4,5})(\d{4})/, '($1) $2-$3');
  };

  const canProceedToSend = () => {
    return signers.every(signer => 
      signer.name.trim() && 
      signer.email.trim() && 
      signer.email.includes('@') &&
      validateCPF(signer.document)
    );
  };

  const createSignatureRequest = async () => {
    if (!selectedFile || !canProceedToSend()) {
      alert("Verifique se todos os campos obrigatórios estão preenchidos.");
      return;
    }

    try {
      setCreatingRequest(true);

      const formData = new FormData();
      formData.append('document', selectedFile);
      formData.append('signers_json', JSON.stringify(signers));

      const response = await fetch('/api/v1/signatures/create', {
        method: 'POST',
        body: formData,
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`,
        },
      });

      const result = await response.json();

      if (result.status === 'success') {
        alert("Solicitação de assinatura criada com sucesso!");
        setActiveStep('status');
        loadSignatureRequests();
        
        // Reset form
        setSelectedFile(null);
        setSigners([{ name: "", email: "", document: "", phone: "" }]);
        setActiveStep('upload');
      } else {
        throw new Error(result.detail || "Erro ao criar solicitação");
      }
    } catch (error) {
      console.error("Erro ao criar solicitação:", error);
      alert("Erro ao criar solicitação de assinatura. Tente novamente.");
    } finally {
      setCreatingRequest(false);
    }
  };

  const downloadSignedDocument = async (requestId: string) => {
    try {
      const response = await fetch(`/api/v1/signatures/${requestId}/download`, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`,
        },
      });

      if (response.ok) {
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.style.display = 'none';
        a.href = url;
        a.download = `documento_assinado_${requestId}.pdf`;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
      } else {
        alert("Erro ao baixar documento assinado.");
      }
    } catch (error) {
      console.error("Erro ao baixar documento:", error);
      alert("Erro ao baixar documento assinado.");
    }
  };

  const cancelSignatureRequest = async (requestId: string) => {
    if (confirm("Tem certeza que deseja cancelar esta solicitação?")) {
      try {
        const response = await apiRequest(`/api/v1/signatures/${requestId}/cancel`, {
          method: 'POST',
        });

        if (response.success) {
          alert("Solicitação cancelada com sucesso.");
          loadSignatureRequests();
        } else {
          alert("Erro ao cancelar solicitação.");
        }
      } catch (error) {
        console.error("Erro ao cancelar:", error);
        alert("Erro ao cancelar solicitação.");
      }
    }
  };

  const formatDate = (dateString: string) => {
    return new Intl.DateTimeFormat("pt-BR", {
      day: "2-digit",
      month: "2-digit", 
      year: "numeric",
      hour: "2-digit",
      minute: "2-digit",
    }).format(new Date(dateString));
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-white">
      <div className="container mx-auto px-4 py-6 sm:py-8">
        {/* Header Mobile-First */}
        <div className="mb-6 sm:mb-8">
          <div className="flex items-center gap-2 mb-4">
            <span className="text-2xl">✍️</span>
            <h1 className="text-xl sm:text-3xl font-bold text-gray-900">
              Assinatura Eletrônica
            </h1>
          </div>
          <p className="text-gray-600 text-sm sm:text-base">
            Envie documentos para assinatura eletrônica segura e juridicamente válida
          </p>
        </div>

        {/* Navigation Steps - Mobile-First */}
        <div className="mb-6 sm:mb-8">
          {/* Mobile: Dropdown Navigation */}
          <div className="sm:hidden">
            <select
              value={activeStep}
              onChange={(e) => setActiveStep(e.target.value as any)}
              className="w-full p-3 border border-gray-300 rounded-lg bg-white focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            >
              <option value="upload">📤 1. Enviar Documento</option>
              <option value="signers">👥 2. Definir Signatários</option>
              <option value="send">📄 3. Enviar para Assinatura</option>
              <option value="status">✅ 4. Acompanhar Status</option>
            </select>
          </div>

          {/* Desktop: Horizontal Navigation */}
          <nav className="hidden sm:flex space-x-8" aria-label="Progress">
            {[
              { id: 'upload', name: 'Enviar Documento', icon: <Upload />, step: 1 },
              { id: 'signers', name: 'Definir Signatários', icon: <Users />, step: 2 },
              { id: 'send', name: 'Enviar para Assinatura', icon: <FileText />, step: 3 },
              { id: 'status', name: 'Acompanhar Status', icon: <CheckCircle />, step: 4 },
            ].map((step, index) => (
              <button
                key={step.id}
                onClick={() => setActiveStep(step.id as any)}
                className={`flex items-center space-x-2 py-3 px-4 border-b-2 font-medium text-sm transition-colors ${
                  activeStep === step.id
                    ? 'border-blue-500 text-blue-600 bg-blue-50 rounded-t-lg'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                <span className="hidden lg:inline">{step.step}.</span>
                {step.icon}
                <span className="hidden md:inline">{step.name}</span>
              </button>
            ))}
          </nav>
        </div>

      {/* Step Content */}
      <div className="space-y-8">
        
        {/* Step 1: Upload Document - Mobile Optimized */}
        {activeStep === 'upload' && (
          <Card className="shadow-lg">
            <CardHeader className="pb-4">
              <CardTitle className="flex items-center gap-2 text-lg sm:text-xl">
                <Upload />
                Enviar Documento para Assinatura
              </CardTitle>
              <CardDescription className="text-sm">
                Selecione o arquivo PDF que será enviado para assinatura
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="border-2 border-dashed border-gray-300 rounded-lg p-6 sm:p-8 text-center hover:border-blue-400 hover:bg-blue-50/30 transition-colors">
                <input
                  type="file"
                  id="file-upload"
                  accept=".pdf"
                  onChange={handleFileChange}
                  className="hidden"
                />
                <label
                  htmlFor="file-upload"
                  className="cursor-pointer flex flex-col items-center"
                >
                  <div className="text-4xl sm:text-5xl mb-4 text-blue-500">
                    <FileText />
                  </div>
                  <p className="text-base sm:text-lg font-medium text-gray-900 mb-2">
                    Clique para enviar seu arquivo
                  </p>
                  <p className="text-xs sm:text-sm text-gray-500 mb-4">
                    Apenas arquivos PDF são aceitos (máx. 50MB)
                  </p>
                  
                  {/* Mobile: Additional visual cues */}
                  <div className="sm:hidden">
                    <div className="flex items-center gap-2 text-xs text-gray-400 mb-2">
                      <span>📱</span>
                      <span>Toque para selecionar do seu dispositivo</span>
                    </div>
                  </div>
                  
                  <Button 
                    type="button" 
                    variant="outline" 
                    className="mt-2 pointer-events-none"
                    size="sm"
                  >
                    📂 Selecionar Arquivo PDF
                  </Button>
                </label>
                
                {selectedFile && (
                  <div className="mt-6 p-4 bg-gradient-to-r from-green-50 to-emerald-50 border border-green-200 rounded-lg">
                    <div className="flex items-start gap-3">
                      <div className="text-2xl">✅</div>
                      <div className="text-left flex-1">
                        <p className="text-green-800 font-medium text-sm sm:text-base break-all">
                          {selectedFile.name}
                        </p>
                        <p className="text-green-600 text-xs sm:text-sm mt-1">
                          Tamanho: {(selectedFile.size / 1024 / 1024).toFixed(2)} MB
                        </p>
                        <p className="text-green-600 text-xs mt-1">
                          ✓ Arquivo válido para assinatura eletrônica
                        </p>
                      </div>
                    </div>
                    
                    <div className="mt-4 pt-4 border-t border-green-200">
                      <Button 
                        onClick={() => setActiveStep('signers')} 
                        className="w-full bg-green-600 hover:bg-green-700"
                      >
                        Próximo: Definir Signatários →
                      </Button>
                    </div>
                  </div>
                )}
              </div>
              
              {/* Help Section - Mobile */}
              <div className="mt-6 p-4 bg-gray-50 rounded-lg">
                <h4 className="font-medium text-gray-900 mb-2 text-sm">💡 Dicas importantes:</h4>
                <ul className="text-xs sm:text-sm text-gray-600 space-y-1">
                  <li>• Certifique-se que o documento está completo</li>
                  <li>• O arquivo deve estar em formato PDF</li>
                  <li>• Tamanho máximo permitido: 50MB</li>
                  <li>• O documento será enviado com segurança</li>
                </ul>
              </div>
            </CardContent>
          </Card>
        )}

        {/* Step 2: Define Signers - Mobile Optimized */}
        {activeStep === 'signers' && (
          <Card className="shadow-lg">
            <CardHeader className="pb-4">
              <CardTitle className="flex items-center gap-2 text-lg sm:text-xl">
                <Users />
                Definir Signatários
              </CardTitle>
              <CardDescription className="text-sm">
                Adicione as informações das pessoas que devem assinar o documento
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4 sm:space-y-6">
              {signers.map((signer, index) => (
                <div key={index} className="p-3 sm:p-4 border-2 border-gray-100 rounded-lg space-y-4 bg-gray-50">
                  <div className="flex justify-between items-center">
                    <div className="flex items-center gap-2">
                      <span className="w-6 h-6 bg-blue-500 text-white rounded-full flex items-center justify-center text-xs font-bold">
                        {index + 1}
                      </span>
                      <h3 className="font-medium text-gray-900 text-sm sm:text-base">
                        Signatário {index + 1}
                      </h3>
                    </div>
                    {signers.length > 1 && (
                      <Button
                        onClick={() => removeSigner(index)}
                        variant="outline"
                        size="sm"
                        className="h-8 w-8 p-0 hover:bg-red-50 hover:border-red-200"
                      >
                        <Trash />
                      </Button>
                    )}
                  </div>
                  
                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 sm:gap-4">
                    <div className="sm:col-span-2">
                      <label className="block text-xs sm:text-sm font-medium text-gray-700 mb-1 sm:mb-2">
                        Nome Completo *
                      </label>
                      <input
                        type="text"
                        value={signer.name}
                        onChange={(e) => updateSigner(index, 'name', e.target.value)}
                        className="w-full px-3 py-2 sm:py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-sm"
                        placeholder="Nome completo do signatário"
                      />
                    </div>
                    
                    <div className="sm:col-span-2">
                      <label className="block text-xs sm:text-sm font-medium text-gray-700 mb-1 sm:mb-2">
                        E-mail *
                      </label>
                      <input
                        type="email"
                        value={signer.email}
                        onChange={(e) => updateSigner(index, 'email', e.target.value)}
                        className="w-full px-3 py-2 sm:py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-sm"
                        placeholder="email@exemplo.com"
                      />
                    </div>
                    
                    <div>
                      <label className="block text-xs sm:text-sm font-medium text-gray-700 mb-1 sm:mb-2">
                        CPF *
                      </label>
                      <input
                        type="text"
                        value={signer.document}
                        onChange={(e) => updateSigner(index, 'document', formatCPF(e.target.value))}
                        className="w-full px-3 py-2 sm:py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-sm"
                        placeholder="000.000.000-00"
                        maxLength={14}
                      />
                    </div>
                    
                    <div>
                      <label className="block text-xs sm:text-sm font-medium text-gray-700 mb-1 sm:mb-2">
                        Telefone (opcional)
                      </label>
                      <input
                        type="text"
                        value={signer.phone}
                        onChange={(e) => updateSigner(index, 'phone', formatPhone(e.target.value))}
                        className="w-full px-3 py-2 sm:py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-sm"
                        placeholder="(11) 99999-9999"
                        maxLength={15}
                      />
                    </div>
                  </div>
                </div>
              ))}
              
              {/* Action Buttons - Mobile Optimized */}
              <div className="flex flex-col sm:flex-row justify-between gap-3 sm:gap-4 pt-4">
                <Button 
                  onClick={addSigner} 
                  variant="outline"
                  className="w-full sm:w-auto order-2 sm:order-1"
                >
                  <Plus /> <span className="ml-1">Adicionar Signatário</span>
                </Button>
                
                <Button 
                  onClick={() => setActiveStep('send')}
                  disabled={!canProceedToSend()}
                  className="w-full sm:w-auto order-1 sm:order-2 bg-blue-600 hover:bg-blue-700"
                >
                  Continuar para Envio →
                </Button>
              </div>
            </CardContent>
          </Card>
        )}

        {/* Step 3: Send for Signature - Mobile Optimized */}
        {activeStep === 'send' && (
          <Card className="shadow-lg">
            <CardHeader className="pb-4">
              <CardTitle className="flex items-center gap-2 text-lg sm:text-xl">
                <FileText />
                Revisar e Enviar
              </CardTitle>
              <CardDescription className="text-sm">
                Revise as informações antes de enviar o documento para assinatura
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4 sm:space-y-6">
              {/* Document Review */}
              {selectedFile && (
                <div className="p-4 bg-gradient-to-r from-blue-50 to-cyan-50 border border-blue-200 rounded-lg">
                  <div className="flex items-center gap-3">
                    <div className="text-2xl">📄</div>
                    <div className="flex-1 min-w-0">
                      <h3 className="font-medium text-blue-900 text-sm sm:text-base">Documento</h3>
                      <p className="text-blue-800 text-sm break-all">{selectedFile.name}</p>
                      <p className="text-blue-600 text-xs">
                        {(selectedFile.size / 1024 / 1024).toFixed(2)} MB
                      </p>
                    </div>
                    <div className="text-green-500 text-lg">✅</div>
                  </div>
                </div>
              )}
              
              {/* Signers Review */}
              <div className="space-y-3">
                <div className="flex items-center gap-2">
                  <h3 className="font-medium text-gray-900 text-sm sm:text-base">
                    Signatários ({signers.length})
                  </h3>
                  <Badge variant="outline" className="text-xs">
                    {signers.length} pessoa{signers.length > 1 ? 's' : ''}
                  </Badge>
                </div>
                
                <div className="space-y-3">
                  {signers.map((signer, index) => (
                    <div key={index} className="p-3 sm:p-4 border-2 border-gray-100 rounded-lg bg-gray-50">
                      <div className="flex items-start gap-3">
                        <div className="w-6 h-6 bg-blue-500 text-white rounded-full flex items-center justify-center text-xs font-bold flex-shrink-0 mt-1">
                          {index + 1}
                        </div>
                        <div className="flex-1 min-w-0">
                          <p className="font-medium text-gray-900 text-sm break-words">{signer.name}</p>
                          <p className="text-xs sm:text-sm text-gray-600 break-all">{signer.email}</p>
                          <p className="text-xs sm:text-sm text-gray-600">CPF: {signer.document}</p>
                          {signer.phone && (
                            <p className="text-xs sm:text-sm text-gray-600">Tel: {signer.phone}</p>
                          )}
                        </div>
                        <div className="text-green-500 text-lg">
                          <CheckCircle />
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
              
              {/* Info Box */}
              <div className="p-4 bg-yellow-50 border border-yellow-200 rounded-lg">
                <div className="flex gap-2">
                  <span className="text-yellow-600">ℹ️</span>
                  <div className="text-xs sm:text-sm text-yellow-800">
                    <p className="font-medium mb-1">O que acontecerá após o envio:</p>
                    <ul className="space-y-1 text-xs">
                      <li>• Cada signatário receberá um e-mail com o link para assinatura</li>
                      <li>• Você receberá notificações sobre o progresso</li>
                      <li>• O documento final será disponibilizado quando todas as assinaturas forem coletadas</li>
                    </ul>
                  </div>
                </div>
              </div>
              
              {/* Action Buttons - Mobile Optimized */}
              <div className="flex flex-col sm:flex-row justify-between gap-3 sm:gap-4 pt-4">
                <Button 
                  onClick={() => setActiveStep('signers')} 
                  variant="outline"
                  className="w-full sm:w-auto order-2 sm:order-1"
                >
                  ← Voltar
                </Button>
                
                <Button 
                  onClick={createSignatureRequest}
                  disabled={creatingRequest}
                  className="w-full sm:w-auto order-1 sm:order-2 bg-green-600 hover:bg-green-700"
                >
                  {creatingRequest ? (
                    <div className="flex items-center gap-2">
                      <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
                      <span>Enviando...</span>
                    </div>
                  ) : (
                    <div className="flex items-center gap-2">
                      <span>🚀</span>
                      <span>Enviar para Assinatura</span>
                    </div>
                  )}
                </Button>
              </div>
            </CardContent>
          </Card>
        )}

        {/* Step 4: Status Tracking */}
        {activeStep === 'status' && (
          <div className="space-y-6">
            <div className="flex justify-between items-center">
              <div>
                <h2 className="text-xl font-bold text-gray-900">Solicitações de Assinatura</h2>
                <p className="text-gray-600">Acompanhe o status dos seus documentos</p>
              </div>
              
              <Button onClick={() => setActiveStep('upload')}>
                <Plus /> Nova Solicitação
              </Button>
            </div>

            {signatureRequests.length === 0 ? (
              <Card>
                <CardContent className="py-12 text-center">
                  <FileText />
                  <h3 className="text-lg font-medium text-gray-900 mb-2 mt-4">
                    Nenhuma solicitação encontrada
                  </h3>
                  <p className="text-gray-500 mb-4">
                    Você ainda não criou nenhuma solicitação de assinatura.
                  </p>
                  <Button onClick={() => setActiveStep('upload')}>
                    <Plus /> Criar Nova Solicitação
                  </Button>
                </CardContent>
              </Card>
            ) : (
              <div className="space-y-4">
                {signatureRequests.map((request) => (
                  <Card key={request.id}>
                    <CardHeader>
                      <div className="flex justify-between items-start">
                        <div>
                          <CardTitle className="text-lg">
                            {request.document_name}
                          </CardTitle>
                          <CardDescription>
                            Criado em {formatDate(request.created_at)}
                            {request.expires_at && (
                              <span> • Expira em {formatDate(request.expires_at)}</span>
                            )}
                          </CardDescription>
                        </div>
                        
                        <Badge 
                          className={statusColors[request.status as keyof typeof statusColors]}
                        >
                          {statusLabels[request.status as keyof typeof statusLabels] || request.status}
                        </Badge>
                      </div>
                    </CardHeader>
                    
                    <CardContent>
                      <div className="space-y-4">
                        <div className="flex items-center justify-between">
                          <div className="flex items-center gap-4">
                            <div>
                              <p className="text-sm text-gray-500">Progresso</p>
                              <p className="font-medium">
                                {request.signers_completed} de {request.signers_total} assinaturas
                              </p>
                            </div>
                            <div className="flex-1 max-w-xs">
                              <div className="w-full bg-gray-200 rounded-full h-2">
                                <div 
                                  className="bg-blue-600 h-2 rounded-full transition-all duration-300"
                                  style={{ width: `${request.progress_percentage}%` }}
                                ></div>
                              </div>
                              <p className="text-xs text-gray-500 mt-1">
                                {request.progress_percentage}% concluído
                              </p>
                            </div>
                          </div>
                          
                          <div className="flex gap-2">
                            {request.status === 'signed' && (
                              <Button
                                onClick={() => downloadSignedDocument(request.id)}
                                size="sm"
                              >
                                <Download /> Baixar
                              </Button>
                            )}
                            
                            {['draft', 'sent'].includes(request.status) && (
                              <Button
                                onClick={() => cancelSignatureRequest(request.id)}
                                variant="outline"
                                size="sm"
                              >
                                <X /> Cancelar
                              </Button>
                            )}
                          </div>
                        </div>
                        
                        {request.completed_at && (
                          <div className="p-3 bg-green-50 rounded-lg">
                            <p className="text-green-800 font-medium">
                              <CheckCircle /> Documento assinado em {formatDate(request.completed_at)}
                            </p>
                          </div>
                        )}
                      </div>
                    </CardContent>
                  </Card>
                ))}
              </div>
            )}
          </div>
        )}
      </div>
      </div>
    </div>
  );
}