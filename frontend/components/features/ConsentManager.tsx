"use client";

import React, { useState, useEffect } from 'react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card';
import { Checkbox } from '@/components/ui/checkbox';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Badge } from '@/components/ui/badge';
import { Separator } from '@/components/ui/separator';
import { ScrollArea } from '@/components/ui/scroll-area';
import { Shield, AlertTriangle, FileText, User } from 'lucide-react';

interface ConsentPurpose {
  id: string;
  name: string;
  description: string;
  required: boolean;
  category: 'essential' | 'functional' | 'analytics' | 'marketing';
}

interface ConsentManagerProps {
  userType: 'CPF' | 'CNPJ';
  onConsentGranted: (purposes: string[]) => void;
  onConsentDeclined: () => void;
  isLoading?: boolean;
  preAnalysisWarning?: string;
}

const CONSENT_PURPOSES: ConsentPurpose[] = [
  {
    id: 'contract_analysis',
    name: 'Análise de Contratos',
    description: 'Processamento do conteúdo de contratos para análise jurídica e identificação de riscos.',
    required: true,
    category: 'essential'
  },
  {
    id: 'service_provision',
    name: 'Prestação de Serviços',
    description: 'Operação da plataforma e fornecimento dos serviços de análise contratual.',
    required: true,
    category: 'essential'
  },
  {
    id: 'security',
    name: 'Segurança da Plataforma',
    description: 'Proteção contra fraudes, monitoramento de segurança e prevenção de uso indevido.',
    required: false,
    category: 'functional'
  },
  {
    id: 'improvement',
    name: 'Melhoria dos Serviços',
    description: 'Análise de uso para melhorar a qualidade e precisão das análises contratuais.',
    required: false,
    category: 'analytics'
  }
];

const CategoryIcons = {
  essential: Shield,
  functional: FileText,
  analytics: User,
  marketing: AlertTriangle
};

const CategoryColors = {
  essential: 'bg-green-100 text-green-800',
  functional: 'bg-blue-100 text-blue-800',
  analytics: 'bg-yellow-100 text-yellow-800',
  marketing: 'bg-red-100 text-red-800'
};

const CategoryLabels = {
  essential: 'Essencial',
  functional: 'Funcional',
  analytics: 'Análise',
  marketing: 'Marketing'
};

export default function ConsentManager({ 
  userType, 
  onConsentGranted, 
  onConsentDeclined, 
  isLoading = false,
  preAnalysisWarning 
}: ConsentManagerProps) {
  const [selectedPurposes, setSelectedPurposes] = useState<string[]>([]);
  const [hasReadTerms, setHasReadTerms] = useState(false);
  const [showDetails, setShowDetails] = useState(false);

  // Auto-seleciona propósitos obrigatórios
  useEffect(() => {
    const requiredPurposes = CONSENT_PURPOSES
      .filter(purpose => purpose.required)
      .map(purpose => purpose.id);
    setSelectedPurposes(requiredPurposes);
  }, []);

  const handlePurposeToggle = (purposeId: string, required: boolean) => {
    if (required) return; // Não permite desmarcar obrigatórios

    setSelectedPurposes(prev => 
      prev.includes(purposeId)
        ? prev.filter(id => id !== purposeId)
        : [...prev, purposeId]
    );
  };

  const handleGrantConsent = () => {
    if (!hasReadTerms) return;
    
    const requiredPurposes = CONSENT_PURPOSES
      .filter(p => p.required)
      .map(p => p.id);
    
    // Garante que todos os obrigatórios estão incluídos
    const finalPurposes = Array.from(new Set([...selectedPurposes, ...requiredPurposes]));
    
    onConsentGranted(finalPurposes);
  };

  const canGrantConsent = hasReadTerms && selectedPurposes.length > 0;
  const requiredCount = CONSENT_PURPOSES.filter(p => p.required).length;
  const selectedRequired = selectedPurposes.filter(id => 
    CONSENT_PURPOSES.find(p => p.id === id)?.required
  ).length;

  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center p-4">
      <Card className="w-full max-w-4xl">
        <CardHeader className="text-center space-y-4">
          <div className="flex items-center justify-center">
            <Shield className="h-12 w-12 text-blue-600" />
          </div>
          <CardTitle className="text-2xl font-bold">
            Consentimento para Tratamento de Dados
          </CardTitle>
          <CardDescription className="text-lg">
            Conforme Lei Geral de Proteção de Dados (LGPD)
          </CardDescription>
          
          {/* Badge do tipo de usuário */}
          <Badge variant={userType === 'CPF' ? 'default' : 'secondary'} className="mx-auto">
            {userType === 'CPF' ? '👤 Pessoa Física' : '🏢 Pessoa Jurídica'}
          </Badge>
        </CardHeader>

        <CardContent className="space-y-6">
          {/* Aviso pré-análise */}
          {preAnalysisWarning && (
            <Alert className="border-amber-200 bg-amber-50">
              <AlertTriangle className="h-4 w-4 text-amber-600" />
              <AlertDescription className="text-amber-800 whitespace-pre-line">
                {preAnalysisWarning}
              </AlertDescription>
            </Alert>
          )}

          {/* Explicação sobre consentimento */}
          <div className="bg-blue-50 p-4 rounded-lg border border-blue-200">
            <h3 className="font-semibold text-blue-900 mb-2">
              📋 Por que precisamos do seu consentimento?
            </h3>
            <p className="text-blue-800 text-sm leading-relaxed">
              Para analisar seus contratos, precisamos processar dados pessoais como documentos e 
              informações de uso. A LGPD exige seu consentimento explícito para cada finalidade 
              específica do tratamento desses dados.
            </p>
          </div>

          {/* Finalidades de tratamento */}
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <h3 className="text-lg font-semibold">Finalidades do Tratamento</h3>
              <Button
                variant="outline"
                size="sm"
                onClick={() => setShowDetails(!showDetails)}
              >
                {showDetails ? 'Ocultar' : 'Ver'} Detalhes
              </Button>
            </div>

            <div className="grid gap-3">
              {CONSENT_PURPOSES.map(purpose => {
                const IconComponent = CategoryIcons[purpose.category];
                const isSelected = selectedPurposes.includes(purpose.id);
                
                return (
                  <div
                    key={purpose.id}
                    className={`border rounded-lg p-4 transition-all ${
                      isSelected ? 'border-blue-500 bg-blue-50' : 'border-gray-200'
                    } ${purpose.required ? 'bg-green-50 border-green-300' : ''}`}
                  >
                    <div className="flex items-start space-x-3">
                      <Checkbox
                        checked={isSelected}
                        onCheckedChange={() => handlePurposeToggle(purpose.id, purpose.required)}
                        disabled={purpose.required}
                        className="mt-0.5"
                      />
                      
                      <div className="flex-1 space-y-2">
                        <div className="flex items-center justify-between">
                          <div className="flex items-center space-x-2">
                            <IconComponent className="h-4 w-4 text-gray-600" />
                            <span className="font-medium">{purpose.name}</span>
                            {purpose.required && (
                              <Badge variant="secondary" className="text-xs">
                                Obrigatório
                              </Badge>
                            )}
                          </div>
                          
                          <Badge 
                            variant="outline" 
                            className={`text-xs ${CategoryColors[purpose.category]}`}
                          >
                            {CategoryLabels[purpose.category]}
                          </Badge>
                        </div>
                        
                        {showDetails && (
                          <p className="text-sm text-gray-600 leading-relaxed">
                            {purpose.description}
                          </p>
                        )}
                      </div>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>

          <Separator />

          {/* Informações sobre direitos do titular */}
          <div className="bg-gray-50 p-4 rounded-lg">
            <h4 className="font-semibold mb-3 text-gray-900">
              ⚖️ Seus direitos como titular de dados:
            </h4>
            <div className="grid md:grid-cols-2 gap-3 text-sm text-gray-700">
              <div>• Acesso aos seus dados</div>
              <div>• Correção de dados incorretos</div>
              <div>• Portabilidade dos dados</div>
              <div>• Eliminação dos dados</div>
              <div>• Revogação do consentimento</div>
              <div>• Informações sobre compartilhamento</div>
            </div>
            <p className="text-xs text-gray-600 mt-3">
              Para exercer seus direitos, entre em contato através do nosso canal de privacidade.
            </p>
          </div>

          {/* Termos de serviço */}
          <div className="space-y-3">
            <div className="flex items-center space-x-2">
              <Checkbox
                checked={hasReadTerms}
                onCheckedChange={(checked) => setHasReadTerms(checked === true)}
              />
              <label className="text-sm font-medium">
                Li e concordo com os{' '}
                <button className="text-blue-600 underline hover:text-blue-800">
                  Termos de Serviço
                </button>{' '}
                e{' '}
                <button className="text-blue-600 underline hover:text-blue-800">
                  Política de Privacidade
                </button>
              </label>
            </div>
            
            <div className="text-xs text-gray-600 bg-gray-50 p-3 rounded">
              <strong>IMPORTANTE:</strong> Este serviço tem caráter informativo e NÃO substitui 
              consultoria jurídica profissional. Para decisões importantes, consulte sempre 
              um advogado qualificado.
            </div>
          </div>

          {/* Resumo da seleção */}
          <Alert>
            <FileText className="h-4 w-4" />
            <AlertDescription>
              <strong>Resumo:</strong> {selectedRequired} de {requiredCount} finalidades 
              obrigatórias selecionadas, {selectedPurposes.length - selectedRequired} opcionais.
              {!canGrantConsent && (
                <span className="text-red-600 block mt-1">
                  É necessário ler os termos para continuar.
                </span>
              )}
            </AlertDescription>
          </Alert>
        </CardContent>

        <CardFooter className="flex justify-between pt-6">
          <Button 
            variant="outline" 
            onClick={onConsentDeclined}
            disabled={isLoading}
          >
            Não Concordo
          </Button>
          
          <Button 
            onClick={handleGrantConsent}
            disabled={!canGrantConsent || isLoading}
            className="bg-green-600 hover:bg-green-700"
          >
            {isLoading ? 'Processando...' : 'Concordo e Prosseguir'}
          </Button>
        </CardFooter>
      </Card>
    </div>
  );
}