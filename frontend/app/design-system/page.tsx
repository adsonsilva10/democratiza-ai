/**
 * Design System Showcase - Página de demonstração
 * Mostra todos os componentes do design system em ação
 */

'use client';

import React, { useState } from 'react';
import { Button } from '../components/ui/button';
import { Card, CardHeader, CardTitle, CardContent } from '../components/ui/card';
import { Badge, RiskBadge, ContractTypeBadge } from '../components/ui/badge';
import { Alert, AlertTitle, AlertDescription, ContractAlert } from '../components/ui/alert';
import { Input, Textarea, CPFInput } from '../components/ui/input';

export default function DesignSystemPage() {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    cpf: '',
    message: ''
  });

  const [alerts, setAlerts] = useState([
    { id: 1, type: 'clausula-abusiva' as const, visible: true },
    { id: 2, type: 'condicoes-favoraveis' as const, visible: true },
  ]);

  const dismissAlert = (id: number) => {
    setAlerts(alerts.map(alert => 
      alert.id === id ? { ...alert, visible: false } : alert
    ));
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-neutral-50 to-neutral-100 p-4">
      <div className="max-w-6xl mx-auto space-y-8">
        
        {/* Header */}
        <div className="text-center py-8">
          <h1 className="text-4xl font-bold text-neutral-900 mb-4">
            Design System Democratiza AI
          </h1>
          <p className="text-lg text-neutral-600 max-w-2xl mx-auto">
            Sistema de design robusto e consistente para a plataforma de análise de contratos mais confiável do Brasil.
          </p>
        </div>

        {/* Buttons Section */}
        <Card>
          <CardHeader>
            <CardTitle>Botões e Ações</CardTitle>
          </CardHeader>
          <CardContent className="space-y-6">
            
            {/* Primary Actions */}
            <div>
              <h3 className="font-semibold mb-3">Ações Principais</h3>
              <div className="flex flex-wrap gap-3">
                <Button>Analisar Contrato</Button>
                <Button variant="secondary">Baixar Relatório</Button>
                <Button variant="success">Aprovar</Button>
                <Button variant="warning">Revisar</Button>
                <Button variant="destructive">Rejeitar</Button>
              </div>
            </div>

            {/* Button Sizes */}
            <div>
              <h3 className="font-semibold mb-3">Tamanhos</h3>
              <div className="flex flex-wrap items-center gap-3">
                <Button size="sm">Pequeno</Button>
                <Button size="default">Padrão</Button>
                <Button size="lg">Grande</Button>
                <Button size="xl">Extra Grande</Button>
              </div>
            </div>

            {/* Button States */}
            <div>
              <h3 className="font-semibold mb-3">Estados</h3>
              <div className="flex flex-wrap gap-3">
                <Button variant="outline">Outline</Button>
                <Button variant="ghost">Ghost</Button>
                <Button variant="link">Link</Button>
                <Button loading>Carregando...</Button>
                <Button disabled>Desabilitado</Button>
              </div>
            </div>

            {/* Full Width */}
            <div>
              <h3 className="font-semibold mb-3">Largura Completa</h3>
              <Button fullWidth size="lg">
                Começar Análise Gratuita
              </Button>
            </div>

          </CardContent>
        </Card>

        {/* Badges Section */}
        <Card>
          <CardHeader>
            <CardTitle>Badges e Indicadores</CardTitle>
          </CardHeader>
          <CardContent className="space-y-6">
            
            {/* Risk Badges */}
            <div>
              <h3 className="font-semibold mb-3">Indicadores de Risco</h3>
              <div className="flex flex-wrap gap-3">
                <RiskBadge risk="baixo" />
                <RiskBadge risk="medio" />
                <RiskBadge risk="alto" />
              </div>
            </div>

            {/* Contract Type Badges */}
            <div>
              <h3 className="font-semibold mb-3">Tipos de Contrato</h3>
              <div className="flex flex-wrap gap-3">
                <ContractTypeBadge type="locacao" />
                <ContractTypeBadge type="telecom" />
                <ContractTypeBadge type="financeiro" />
                <ContractTypeBadge type="outros" />
              </div>
            </div>

            {/* Badge Variants */}
            <div>
              <h3 className="font-semibold mb-3">Variações</h3>
              <div className="flex flex-wrap gap-3">
                <Badge>Padrão</Badge>
                <Badge variant="primary">Primário</Badge>
                <Badge variant="outline">Outline</Badge>
                <Badge variant="subtle-success">Sutil Sucesso</Badge>
                <Badge variant="outline-danger">Outline Perigo</Badge>
              </div>
            </div>

          </CardContent>
        </Card>

        {/* Alerts Section */}
        <Card>
          <CardHeader>
            <CardTitle>Alertas e Notificações</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            
            {/* Contract Specific Alerts */}
            {alerts
              .filter(alert => alert.visible)
              .map(alert => (
                <ContractAlert
                  key={alert.id}
                  type={alert.type}
                  title={
                    alert.type === 'clausula-abusiva' 
                      ? "⚠️ Cláusula Abusiva Detectada" 
                      : "✅ Condições Favoráveis"
                  }
                  description={
                    alert.type === 'clausula-abusiva'
                      ? "Encontramos uma cláusula que pode ser prejudicial aos seus direitos. Cláusula 5.2 - Taxa de cancelamento desproporcional."
                      : "Este contrato apresenta condições favoráveis para você. Política de cancelamento flexível com 30 dias de prazo."
                  }
                  dismissible
                  onDismiss={() => dismissAlert(alert.id)}
                />
              ))
            }

            {/* Standard Alerts */}
            <Alert variant="info">
              <AlertTitle>Informação</AlertTitle>
              <AlertDescription>
                Análise concluída com sucesso. Relatório disponível para download.
              </AlertDescription>
            </Alert>

            <Alert variant="warning">
              <AlertTitle>Atenção</AlertTitle>
              <AlertDescription>
                Alguns pontos do contrato necessitam revisão antes da assinatura.
              </AlertDescription>
            </Alert>

          </CardContent>
        </Card>

        {/* Forms Section */}
        <Card>
          <CardHeader>
            <CardTitle>Formulários e Entradas</CardTitle>
          </CardHeader>
          <CardContent className="space-y-6">
            
            <div className="grid md:grid-cols-2 gap-6">
              
              {/* Text Inputs */}
              <div className="space-y-4">
                <Input
                  label="Nome Completo"
                  placeholder="Digite seu nome"
                  value={formData.name}
                  onChange={(e) => setFormData(prev => ({...prev, name: e.target.value}))}
                />
                
                <Input
                  label="E-mail"
                  type="email"
                  placeholder="seu@email.com"
                  value={formData.email}
                  onChange={(e) => setFormData(prev => ({...prev, email: e.target.value}))}
                  helper="Usaremos seu e-mail para enviar o relatório de análise"
                />

                <CPFInput
                  value={formData.cpf}
                  onChange={(e) => setFormData(prev => ({...prev, cpf: e.target.value}))}
                  onValidCPF={(cpf) => console.log('CPF válido:', cpf)}
                />
              </div>

              {/* Textarea */}
              <div>
                <Textarea
                  label="Observações"
                  placeholder="Conte-nos mais sobre o contrato que você quer analisar..."
                  value={formData.message}
                  onChange={(e) => setFormData(prev => ({...prev, message: e.target.value}))}
                  className="min-h-[160px]"
                />
              </div>
            </div>

            {/* Form Actions */}
            <div className="flex gap-3 pt-4 border-t">
              <Button variant="outline">Cancelar</Button>
              <Button>Solicitar Análise</Button>
            </div>

          </CardContent>
        </Card>

        {/* Card Variants */}
        <div className="grid md:grid-cols-3 gap-6">
          
          <Card variant="default">
            <CardHeader>
              <CardTitle>Card Padrão</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-muted-foreground">
                Estilo básico para conteúdo geral.
              </p>
            </CardContent>
          </Card>

          <Card variant="elevated">
            <CardHeader>
              <CardTitle>Card Elevado</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-muted-foreground">
                Destaque visual com sombra mais pronunciada.
              </p>
            </CardContent>
          </Card>

          <Card variant="outlined">
            <CardHeader>
              <CardTitle>Card Outlined</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-muted-foreground">
                Borda mais espessa para ênfase.
              </p>
            </CardContent>
          </Card>

        </div>

        {/* Footer */}
        <div className="text-center py-8 text-neutral-600">
          <p>Design System Democratiza AI - Versão 1.0</p>
          <p className="text-sm mt-2">
            Democratizando a compreensão jurídica no Brasil 🇧🇷
          </p>
        </div>

      </div>
    </div>
  );
}