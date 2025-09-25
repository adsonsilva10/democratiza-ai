'use client';

import React, { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';

// Tipos de usuário
type UserType = 'subscriber' | 'ex-subscriber' | 'pay-per-use'

interface UserProfile {
  id: string
  email: string
  name: string
  userType: UserType
  subscription?: SubscriptionData
  credits?: CreditBalance
}

interface SubscriptionData {
  id: string
  planType: string
  planName: string
  monthlyPrice: number
  status: 'active' | 'cancelled' | 'expired'
  billingStart: string
  billingEnd: string
  contractsAnalyzed: number
  contractsLimit: number
  signaturesUsed: number
  signaturesLimit: number
  includedFeatures: string[]
  nextPayment: string
  autoRenewal: boolean
}

interface CreditBalance {
  total: number
  used: number
  remaining: number
  expiryDate?: string
}

export default function ManagePlanPage() {
  const [userProfile, setUserProfile] = useState<UserProfile | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const router = useRouter();

  // Função para determinar o tipo de usuário
  const determineUserType = (profile: any): UserType => {
    // Se tem assinatura ativa
    if (profile.subscription?.status === 'active') {
      return 'subscriber';
    }
    
    // Se tinha assinatura mas cancelou/expirou
    if (profile.subscription && ['cancelled', 'expired'].includes(profile.subscription.status)) {
      return 'ex-subscriber';
    }
    
    // Se nunca teve assinatura ou só usa créditos
    return 'pay-per-use';
  };

  useEffect(() => {
    // Simular carregamento de dados da API
    const loadUserProfile = async () => {
      try {
        setIsLoading(true);
        
        // Aqui você faria a chamada real para a API
        // const response = await fetch('/api/user/profile');
        // const data = await response.json();
        
        // Dados mockados para demonstração - altere para testar diferentes cenários
        const mockProfile = {
          id: 'user_123',
          email: 'usuario@exemplo.com',
          name: 'João Silva',
          
          // === CENÁRIOS DE TESTE ===
          // Descomente apenas UM dos cenários abaixo para testar:

          // Cenário 1: Usuário com assinatura ativa
          /*
          subscription: {
            id: 'sub_123',
            planType: 'professional',
            planName: 'Plano Profissional',
            monthlyPrice: 79.90,
            status: 'active' as const,
            billingStart: '2025-01-01',
            billingEnd: '2025-02-01',
            contractsAnalyzed: 23,
            contractsLimit: 50,
            signaturesUsed: 12,
            signaturesLimit: 50,
            includedFeatures: [
              '50 análises mensais',
              'IA especializada por setor',
              'Consultoria jurídica via chat',
              'Assinatura eletrônica certificada',
              'Relatórios personalizáveis',
              'Suporte WhatsApp prioritário'
            ],
            nextPayment: '2025-02-01',
            autoRenewal: true
          },
          */
          
          // Cenário 2: Ex-assinante (assinatura cancelada/expirada)
          /*
          subscription: {
            id: 'sub_123',
            planType: 'professional',
            planName: 'Plano Profissional',
            monthlyPrice: 79.90,
            status: 'expired' as const,
            billingStart: '2024-12-01',
            billingEnd: '2025-01-01',
            contractsAnalyzed: 47,
            contractsLimit: 50,
            signaturesUsed: 23,
            signaturesLimit: 50,
            includedFeatures: [
              '50 análises mensais',
              'IA especializada por setor',
              'Consultoria jurídica via chat',
              'Assinatura eletrônica certificada',
              'Relatórios personalizáveis',
              'Suporte WhatsApp prioritário'
            ],
            nextPayment: '',
            autoRenewal: false
          },
          */
          
          // Cenário 3: Usuário pay-per-use (ATIVO)
          credits: {
            total: 50,
            used: 32,
            remaining: 18,
            expiryDate: "2025-12-31"
          }
        };

        const userType = determineUserType(mockProfile);
        
        setUserProfile({
          ...mockProfile,
          userType
        });

        setIsLoading(false);
      } catch (error) {
        console.error('Erro ao carregar perfil do usuário:', error);
        setIsLoading(false);
      }
    };

    loadUserProfile();
  }, []);

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-50 to-blue-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Carregando informações da conta...</p>
        </div>
      </div>
    );
  }

  if (!userProfile) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-50 to-blue-50 flex items-center justify-center">
        <div className="text-center">
          <p className="text-red-600">Erro ao carregar informações do usuário.</p>
        </div>
      </div>
    );
  }

  // Renderizar baseado no tipo de usuário
  if (userProfile.userType === 'subscriber' || userProfile.userType === 'ex-subscriber') {
    // Renderizar componente de gestão de assinatura
    return <SubscriptionManagerComponent userProfile={userProfile} />;
  } else {
    // Renderizar componente de gestão de créditos
    return <CreditManagerComponent userProfile={userProfile} />;
  }
}

// Componente para gestão de assinatura
function SubscriptionManagerComponent({ userProfile }: { userProfile: UserProfile }) {
  const router = useRouter();

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-blue-50 p-4 sm:p-6">
      <div className="max-w-7xl mx-auto space-y-6">
        {/* Header */}
        <div className="text-center space-y-2">
          <h1 className="text-3xl sm:text-4xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
            Gerenciar Assinatura
          </h1>
          <p className="text-gray-600 text-sm sm:text-base">
            Controle sua assinatura, uso e configurações
          </p>
        </div>

        {/* Status da Assinatura */}
        <div className="bg-white rounded-lg shadow-lg p-6">
          <h2 className="text-xl font-semibold mb-4">Status da Assinatura</h2>
          {userProfile.subscription && (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <p className="text-gray-600">Plano Atual</p>
                <p className="text-2xl font-bold text-blue-600">{userProfile.subscription.planName}</p>
                <p className="text-gray-500">R$ {userProfile.subscription.monthlyPrice.toFixed(2).replace('.', ',')}/mês</p>
              </div>
              <div>
                <p className="text-gray-600">Status</p>
                <span className={`inline-flex px-3 py-1 rounded-full text-sm font-medium ${
                  userProfile.subscription.status === 'active' ? 'bg-green-100 text-green-800' :
                  userProfile.subscription.status === 'cancelled' ? 'bg-yellow-100 text-yellow-800' :
                  'bg-red-100 text-red-800'
                }`}>
                  {userProfile.subscription.status === 'active' ? 'Ativa' :
                   userProfile.subscription.status === 'cancelled' ? 'Cancelada' : 'Expirada'}
                </span>
              </div>
            </div>
          )}
        </div>

        {/* Botão Conhecer Planos para ex-assinantes */}
        {userProfile.userType === 'ex-subscriber' && (
          <div className="bg-blue-50 border border-blue-200 rounded-lg p-6 text-center">
            <h3 className="text-lg font-semibold text-blue-800 mb-2">
              Reative sua assinatura
            </h3>
            <p className="text-blue-600 mb-4">
              Volte a ter acesso completo aos nossos serviços
            </p>
            <button
              onClick={() => router.push('/dashboard/planos')}
              className="bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 transition-colors"
            >
              Conhecer Planos de Assinatura
            </button>
          </div>
        )}
      </div>
    </div>
  );
}

// Componente para gestão de créditos
function CreditManagerComponent({ userProfile }: { userProfile: UserProfile }) {
  const router = useRouter();

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-blue-50 p-4 sm:p-6">
      <div className="max-w-7xl mx-auto space-y-6">
        {/* Header */}
        <div className="text-center space-y-2">
          <h1 className="text-3xl sm:text-4xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
            Gerenciar Créditos
          </h1>
          <p className="text-gray-600 text-sm sm:text-base">
            Acompanhe seu saldo e histórico de uso dos serviços avulsos
          </p>
        </div>

        {/* Saldo de Créditos */}
        {userProfile.credits && (
          <div className="bg-gradient-to-r from-blue-500 to-purple-600 text-white rounded-lg shadow-lg p-6">
            <h2 className="text-xl font-semibold mb-4">Saldo de Créditos</h2>
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
              <div>
                <p className="text-blue-100 text-sm">Total de Créditos</p>
                <p className="text-2xl font-bold">{userProfile.credits.total}</p>
              </div>
              <div>
                <p className="text-blue-100 text-sm">Utilizados</p>
                <p className="text-2xl font-bold">{userProfile.credits.used}</p>
              </div>
              <div>
                <p className="text-blue-100 text-sm">Disponíveis</p>
                <p className="text-2xl font-bold text-green-300">{userProfile.credits.remaining}</p>
              </div>
            </div>
          </div>
        )}

        {/* Call to Action para Assinatura */}
        <div className="bg-gradient-to-r from-green-50 to-blue-50 border border-green-200 rounded-lg p-6 text-center">
          <h3 className="text-lg font-semibold text-green-800 mb-2">
            🚀 Que tal uma assinatura?
          </h3>
          <p className="text-green-600 mb-4">
            Com nossos planos mensais você tem muito mais vantagens e economia!
          </p>
          <div className="flex flex-col sm:flex-row gap-3 justify-center">
            <button
              onClick={() => router.push('/dashboard/planos')}
              className="bg-green-600 text-white px-6 py-3 rounded-lg hover:bg-green-700 transition-colors"
            >
              Conhecer Planos de Assinatura
            </button>
            <button className="bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 transition-colors">
              Comprar Mais Créditos
            </button>
          </div>
        </div>

        {/* Ações Rápidas */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          <div className="bg-white rounded-lg shadow-md p-6 text-center hover:shadow-lg transition-shadow cursor-pointer">
            <div className="w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-3">
              <span className="text-2xl">📄</span>
            </div>
            <h3 className="font-semibold text-gray-800">Analisar Contrato</h3>
            <p className="text-xs text-gray-600 mt-1">2 créditos por análise</p>
          </div>

          <div className="bg-white rounded-lg shadow-md p-6 text-center hover:shadow-lg transition-shadow cursor-pointer">
            <div className="w-12 h-12 bg-purple-100 rounded-full flex items-center justify-center mx-auto mb-3">
              <span className="text-2xl">✍️</span>
            </div>
            <h3 className="font-semibold text-gray-800">Assinatura Digital</h3>
            <p className="text-xs text-gray-600 mt-1">3 créditos por assinatura</p>
          </div>

          <div className="bg-white rounded-lg shadow-md p-6 text-center hover:shadow-lg transition-shadow cursor-pointer">
            <div className="w-12 h-12 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-3">
              <span className="text-2xl">📊</span>
            </div>
            <h3 className="font-semibold text-gray-800">Histórico</h3>
            <p className="text-xs text-gray-600 mt-1">Ver uso detalhado</p>
          </div>
        </div>
      </div>
    </div>
  );
}