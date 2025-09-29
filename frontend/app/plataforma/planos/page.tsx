"use client";

import { useState, useEffect } from "react";
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { useApi } from "@/lib/hooks/useApi";

// Ícones simples usando emojis enquanto lucide-react não está disponível
const Check = ({ className = "" }: { className?: string }) => <span className={className}>✓</span>;
const CreditCard = ({ className = "" }: { className?: string }) => <span className={className}>💳</span>;
const FileText = ({ className = "" }: { className?: string }) => <span className={className}>📄</span>;
const Zap = ({ className = "" }: { className?: string }) => <span className={className}>⚡</span>;
const Shield = ({ className = "" }: { className?: string }) => <span className={className}>🛡️</span>;
const Users = ({ className = "" }: { className?: string }) => <span className={className}>👥</span>;
const Clock = ({ className = "" }: { className?: string }) => <span className={className}>⏰</span>;
const AlertCircle = ({ className = "" }: { className?: string }) => <span className={className}>⚠️</span>;
const Loader = ({ className = "" }: { className?: string }) => <span className={className}>⏳</span>;

interface Plan {
  id: string;
  name: string;
  description: string;
  price: number;
  duration_months: number;
  max_analyses: number;
  features: string[];
  is_active: boolean;
  type: "pay_per_use" | "subscription";
}

interface UserSubscription {
  id: string;
  plan: Plan;
  is_active: boolean;
  expires_at: string;
  remaining_analyses: number;
}

// Dados de fallback/mock para quando a API não responder
const FALLBACK_PLANS: Plan[] = [
  {
    id: "pay_per_use_basic",
    name: "Análise Simples",
    description: "Apenas análise do contrato",
    price: 15.90,
    duration_months: 0,
    max_analyses: 1,
    features: [
      "Análise completa do contrato",
      "Identificação de cláusulas abusivas",
      "Relatório detalhado em PDF",
      "Suporte por email"
    ],
    is_active: true,
    type: "pay_per_use"
  },
  {
    id: "pay_per_use_signature",
    name: "Análise + Assinatura",
    description: "Análise completa com assinatura eletrônica",
    price: 24.90,
    duration_months: 0,
    max_analyses: 1,
    features: [
      "Análise completa do contrato",
      "Identificação de cláusulas abusivas",
      "Relatório detalhado em PDF",
      "Assinatura eletrônica integrada",
      "Certificado digital válido",
      "Suporte prioritário por chat",
      "Armazenamento seguro por 5 anos"
    ],
    is_active: true,
    type: "pay_per_use"
  },
  {
    id: "subscription_basic",
    name: "Plano Básico",
    description: "Para usuários que fazem algumas análises por mês",
    price: 49.90,
    duration_months: 1,
    max_analyses: 10,
    features: [
      "10 análises por mês",
      "Análise completa de contratos",
      "Identificação de riscos",
      "Relatórios em PDF",
      "Suporte prioritário"
    ],
    is_active: true,
    type: "subscription"
  },
  {
    id: "subscription_professional",
    name: "Plano Profissional",
    description: "Para advogados e consultores jurídicos",
    price: 79.90,
    duration_months: 1,
    max_analyses: 50,
    features: [
      "50 análises por mês",
      "Análise avançada com IA",
      "Consultas jurídicas por chat",
      "Assinatura eletrônica básica",
      "Relatórios personalizados",
      "Suporte prioritário por WhatsApp",
      "Histórico completo de análises"
    ],
    is_active: true,
    type: "subscription"
  },
  {
    id: "subscription_premium",
    name: "Plano Enterprise",
    description: "Para empresas e escritórios de advocacia",
    price: 149.90,
    duration_months: 1,
    max_analyses: -1,
    features: [
      "Análises ilimitadas",
      "IA jurídica especializada",
      "Consultoria jurídica dedicada",
      "Assinatura eletrônica avançada",
      "Dashboard executivo completo",
      "Suporte premium 24/7",
      "API de integração",
      "Relatórios de compliance",
      "Treinamento da equipe"
    ],
    is_active: true,
    type: "subscription"
  }
];

export default function PlanosPage() {
  const { apiRequest } = useApi();
  const [plans, setPlans] = useState<Plan[]>([]);
  const [userSubscription, setUserSubscription] = useState<UserSubscription | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [processingPayment, setProcessingPayment] = useState<string | null>(null);
  const [loadingPlans, setLoadingPlans] = useState(true);
  const [loadingSubscription, setLoadingSubscription] = useState(true);

  useEffect(() => {
    loadData();
  }, []);

  const loadPlans = async () => {
    try {
      setLoadingPlans(true);
      setError(null);
      
      const response = await apiRequest("/api/v1/payments/plans");
      
      if (response.success && response.data?.plans) {
        setPlans(response.data.plans);
      } else {
        // Usar dados de fallback se API falhar
        console.warn("API de planos não disponível, usando dados de fallback");
        setPlans(FALLBACK_PLANS);
      }
    } catch (error) {
      console.error("Erro ao carregar planos:", error);
      // Usar dados de fallback em caso de erro
      setPlans(FALLBACK_PLANS);
      setError("");
    } finally {
      setLoadingPlans(false);
    }
  };

  const loadUserSubscription = async () => {
    try {
      setLoadingSubscription(true);
      
      const response = await apiRequest("/api/v1/payments/user/subscription");
      
      if (response.success && response.data?.subscription) {
        setUserSubscription(response.data.subscription);
      }
    } catch (error) {
      console.error("Erro ao carregar assinatura do usuário:", error);
      // Não é crítico se não conseguir carregar a assinatura
    } finally {
      setLoadingSubscription(false);
    }
  };

  const loadData = async () => {
    await Promise.all([loadPlans(), loadUserSubscription()]);
    setLoading(false);
  };

  const handlePayPerUse = async (planId: string) => {
    try {
      setProcessingPayment("pay_per_use");

      // Verificar se é um plano de fallback
      const plan = plans.find(p => p.id === planId);
      if (plan && FALLBACK_PLANS.some(fp => fp.id === planId)) {
        alert(`Funcionalidade temporariamente indisponível.\n\nPlano: ${plan.name}\nPreço: ${formatPrice(plan.price)}\n\nTente novamente mais tarde ou entre em contato conosco.`);
        return;
      }

      const response = await apiRequest("/api/v1/payments/pay-per-use", {
        method: "POST",
        body: JSON.stringify({ plan_id: planId }),
        headers: {
          "Content-Type": "application/json",
        },
      });

      if (response.success && response.data?.payment_url) {
        // Redirecionar para Mercado Pago
        window.open(response.data.payment_url, "_blank");
      } else {
        throw new Error(response.error || "Erro ao criar pagamento");
      }
    } catch (error) {
      console.error("Erro no pagamento avulso:", error);
      alert("Erro ao processar pagamento. Verifique sua conexão e tente novamente.");
    } finally {
      setProcessingPayment(null);
    }
  };

  const handleSubscription = async (planId: string) => {
    try {
      setProcessingPayment(planId);

      // Verificar se é um plano de fallback
      const plan = plans.find(p => p.id === planId);
      if (plan && FALLBACK_PLANS.some(fp => fp.id === planId)) {
        alert(`Funcionalidade temporariamente indisponível.\n\nPlano: ${plan.name}\nPreço: ${formatPrice(plan.price)}/mês\n\nTente novamente mais tarde ou entre em contato conosco.`);
        return;
      }

      const response = await apiRequest("/api/v1/payments/subscription", {
        method: "POST",
        body: JSON.stringify({ plan_id: planId }),
        headers: {
          "Content-Type": "application/json",
        },
      });

      if (response.success && response.data?.payment_url) {
        // Redirecionar para Mercado Pago
        window.open(response.data.payment_url, "_blank");
      } else {
        throw new Error(response.error || "Erro ao criar assinatura");
      }
    } catch (error) {
      console.error("Erro na assinatura:", error);
      alert("Erro ao processar assinatura. Verifique sua conexão e tente novamente.");
    } finally {
      setProcessingPayment(null);
    }
  };

  const formatPrice = (price: number) => {
    return new Intl.NumberFormat("pt-BR", {
      style: "currency",
      currency: "BRL",
    }).format(price);
  };

  const formatDate = (dateString: string) => {
    return new Intl.DateTimeFormat("pt-BR", {
      day: "2-digit",
      month: "2-digit",
      year: "numeric",
    }).format(new Date(dateString));
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-gray-50 to-white">
        <div className="container mx-auto px-4 py-6 sm:py-12">
          <div className="text-center mb-8">
            <div className="flex items-center justify-center gap-3 mb-6">
              <div className="w-12 h-12 bg-gradient-to-r from-blue-600 to-purple-600 rounded-full flex items-center justify-center shadow-lg">
                <span className="text-white text-xl">💳</span>
              </div>
              <div className="text-left">
                <h1 className="text-2xl sm:text-4xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
                  Escolha seu Plano
                </h1>
                <p className="text-sm sm:text-base text-gray-500 font-medium">
                  Democratiza AI
                </p>
              </div>
            </div>
            <div className="max-w-3xl mx-auto">
              <p className="text-gray-600 text-base sm:text-lg leading-relaxed">
                Carregando planos disponíveis...
              </p>
            </div>
          </div>
        
          <div className="flex flex-col items-center justify-center h-64">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mb-4"></div>
            <div className="flex items-center gap-2 text-gray-600">
              <Loader />
              <span>Carregando planos disponíveis...</span>
            </div>
            <p className="text-sm text-gray-500 mt-2">
              Aguarde enquanto verificamos as melhores opções para você
            </p>
          </div>
        </div>
      </div>
    );
  }

  const payPerUsePlans = plans.filter((plan) => plan.type === "pay_per_use");
  const subscriptionPlans = plans.filter((plan) => plan.type === "subscription");

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-white">
      <div className="container mx-auto px-4 py-6 sm:py-12">
        {/* Header Mobile-First */}
        <div className="text-center mb-8 sm:mb-12">
          <div className="mb-6">
            <div className="flex items-center justify-center gap-3 mb-6">
              <div className="w-12 h-12 bg-gradient-to-r from-blue-600 to-purple-600 rounded-full flex items-center justify-center shadow-lg">
                <span className="text-white text-xl">💳</span>
              </div>
              <div className="text-left">
                <h1 className="text-2xl sm:text-4xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
                  Escolha seu Plano
                </h1>
                <p className="text-sm sm:text-base text-gray-500 font-medium">
                  Democratiza AI
                </p>
              </div>
            </div>
            <div className="max-w-3xl mx-auto">
              <p className="text-gray-600 text-base sm:text-lg leading-relaxed mb-4">
                Democratize a análise jurídica com nossos <span className="font-semibold text-blue-600">planos flexíveis</span>.
              </p>
              <p className="text-gray-500 text-sm sm:text-base">
                Pague apenas pelo que usar ou assine um plano mensal com benefícios exclusivos.
              </p>
            </div>
          </div>
        </div>

      {/* Aviso de erro se houver */}
      {error && (
        <Card className="mb-8 border-yellow-200 bg-yellow-50">
          <CardContent className="py-4">
            <div className="flex items-center gap-2 text-yellow-800">
              <AlertCircle />
              <span className="font-medium">Aviso:</span>
              <span>{error}</span>
            </div>
          </CardContent>
        </Card>
      )}

      {/* Status da Assinatura Atual */}
      {!loadingSubscription && userSubscription && userSubscription.is_active && (
        <Card className="mb-8 border-green-200 bg-green-50">
          <CardHeader>
            <div className="flex items-center gap-2">
              <Shield />
              <CardTitle className="text-green-800">Plano Ativo</CardTitle>
            </div>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div>
                <p className="text-sm text-green-600">Plano Atual</p>
                <p className="font-medium text-green-800">{userSubscription.plan.name}</p>
              </div>
              <div>
                <p className="text-sm text-green-600">Válido até</p>
                <p className="font-medium text-green-800">
                  {formatDate(userSubscription.expires_at)}
                </p>
              </div>
              <div>
                <p className="text-sm text-green-600">Análises Restantes</p>
                <p className="font-medium text-green-800">
                  {userSubscription.plan.max_analyses === -1 
                    ? "Ilimitado" 
                    : userSubscription.remaining_analyses
                  }
                </p>
              </div>
            </div>
          </CardContent>
        </Card>
      )}

      {/* Opção de Pagamento Avulso - Lado a Lado */}
      {payPerUsePlans.length > 0 && (
        <div className="mb-12">
          <div className="bg-gradient-to-r from-amber-50 to-orange-50 border border-amber-200 rounded-xl p-4 sm:p-6">
            <div className="text-center mb-6">
              <div className="flex items-center justify-center gap-2 mb-2">
                <span className="text-xl">💰</span>
                <h3 className="text-lg sm:text-xl font-semibold text-gray-900">Precisa de apenas 1 análise?</h3>
              </div>
              <p className="text-gray-600 text-sm sm:text-base">Pague somente pelo que usar, sem compromisso mensal</p>
            </div>
            
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 max-w-4xl mx-auto">
              {payPerUsePlans.map((plan) => (
                <div key={plan.id} className={`bg-white rounded-lg p-4 sm:p-6 shadow-md border-2 transition-all hover:shadow-lg ${
                  plan.id === 'pay_per_use_signature' ? 'border-amber-300 relative' : 'border-gray-200'
                }`}>
                  {plan.id === 'pay_per_use_signature' && (
                    <div className="absolute -top-3 left-1/2 transform -translate-x-1/2">
                      <span className="bg-gradient-to-r from-amber-500 to-orange-500 text-white px-3 py-1 rounded-full text-xs font-medium">
                        🔥 Mais Completo
                      </span>
                    </div>
                  )}
                  
                  <div className="text-center mb-4">
                    <h4 className="text-lg font-semibold text-gray-900 mb-2">{plan.name}</h4>
                    <div className="text-2xl sm:text-3xl font-bold text-amber-600 mb-1">
                      {formatPrice(plan.price)}
                    </div>
                    <p className="text-sm text-gray-500">{plan.description}</p>
                  </div>
                  
                  <div className="space-y-2 mb-6">
                    {plan.features.map((feature, index) => (
                      <div key={index} className="flex items-center gap-2 text-sm text-gray-700">
                        <span className="text-green-500 text-base">✓</span>
                        <span>{feature}</span>
                      </div>
                    ))}
                  </div>
                  
                  <Button
                    onClick={() => handlePayPerUse(plan.id)}
                    disabled={processingPayment === "pay_per_use"}
                    className={`w-full ${
                      plan.id === 'pay_per_use_signature'
                        ? 'bg-gradient-to-r from-amber-500 to-orange-500 hover:from-amber-600 hover:to-orange-600'
                        : 'bg-gradient-to-r from-gray-600 to-gray-700 hover:from-gray-700 hover:to-gray-800'
                    }`}
                  >
                    {processingPayment === "pay_per_use" ? (
                      <div className="flex items-center gap-2">
                        <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
                        Processando...
                      </div>
                    ) : (
                      <div className="flex items-center justify-center gap-2">
                        <span>{plan.id === 'pay_per_use_signature' ? '✍️' : '📊'}</span>
                        <span>{plan.id === 'pay_per_use_signature' ? 'Analisar + Assinar' : 'Apenas Analisar'}</span>
                      </div>
                    )}
                  </Button>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* Planos de Assinatura - Layout Mobile-First 3 Colunas */}
      <div className="mb-16">
        <div className="text-center mb-8 sm:mb-12">
          <div className="flex items-center justify-center gap-2 mb-4">
            <span className="text-2xl">⭐</span>
            <h2 className="text-xl sm:text-2xl font-bold text-gray-900">
              Planos de Assinatura
            </h2>
          </div>
          <p className="text-gray-600 text-sm sm:text-base max-w-lg mx-auto">
            Análises mensais com economia e recursos exclusivos
          </p>
        </div>
        
        {loadingPlans ? (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-6">
            {[1, 2, 3].map((i) => (
              <Card key={i} className="animate-pulse">
                <CardHeader className="pb-4">
                  <div className="h-6 bg-gray-200 rounded mb-2"></div>
                  <div className="h-4 bg-gray-200 rounded"></div>
                </CardHeader>
                <CardContent className="pb-6">
                  <div className="h-12 bg-gray-200 rounded mb-4"></div>
                  <div className="space-y-3">
                    <div className="h-3 bg-gray-200 rounded"></div>
                    <div className="h-3 bg-gray-200 rounded"></div>
                    <div className="h-3 bg-gray-200 rounded"></div>
                  </div>
                </CardContent>
                <CardFooter>
                  <div className="h-12 bg-gray-200 rounded w-full"></div>
                </CardFooter>
              </Card>
            ))}
          </div>
        ) : subscriptionPlans.length > 0 ? (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-6 max-w-6xl mx-auto">
            {subscriptionPlans.map((plan, index) => {
            const isPopular = plan.name.toLowerCase().includes("premium");
            const isBasic = plan.name.toLowerCase().includes("básico");
            const isCurrentPlan = userSubscription?.plan.id === plan.id;
            
            // Ordenar: Básico, Premium (destaque), Empresarial
            let cardClass = "relative transition-all duration-300 hover:shadow-lg";
            let headerGradient = "bg-white";
            let badgeContent = null;
            
            if (isPopular) {
              cardClass += " border-2 border-blue-500 shadow-xl transform lg:scale-105 z-10";
              headerGradient = "bg-gradient-to-r from-blue-500 to-blue-600 text-white";
              badgeContent = (
                <div className="absolute -top-3 left-1/2 transform -translate-x-1/2 z-20">
                  <Badge className="bg-gradient-to-r from-orange-500 to-red-500 text-white px-4 py-1 shadow-lg">
                    🔥 Mais Popular
                  </Badge>
                </div>
              );
            } else if (isCurrentPlan) {
              cardClass += " border-2 border-green-500 bg-green-50";
              badgeContent = (
                <div className="absolute -top-3 left-1/2 transform -translate-x-1/2 z-20">
                  <Badge className="bg-green-500 text-white px-4 py-1">
                    ✅ Plano Atual
                  </Badge>
                </div>
              );
            }

            return (
              <Card key={plan.id} className={cardClass}>
                {badgeContent}
                
                <CardHeader className={`${headerGradient} rounded-t-lg ${isPopular ? 'text-white' : ''}`}>
                  <div className="text-center">
                    <CardTitle className={`text-lg sm:text-xl mb-2 ${isPopular ? 'text-white' : 'text-gray-900'}`}>
                      {plan.name}
                    </CardTitle>
                    <CardDescription className={`text-sm ${isPopular ? 'text-blue-100' : 'text-gray-600'}`}>
                      {plan.description}
                    </CardDescription>
                  </div>
                </CardHeader>
                
                <CardContent className="px-4 sm:px-6 py-6 flex-1 flex flex-col">
                  {/* Preço Principal */}
                  <div className="text-center mb-6">
                    <div className={`text-2xl sm:text-3xl font-bold mb-1 ${isPopular ? 'text-blue-600' : 'text-gray-900'}`}>
                      {formatPrice(plan.price)}
                    </div>
                    <p className="text-xs sm:text-sm text-gray-500">
                      por {plan.duration_months} mês{plan.duration_months > 1 ? "es" : ""}
                    </p>
                    
                    {/* Análises Destacadas */}
                    <div className="mt-3 p-2 bg-gray-50 rounded-lg">
                      <div className="text-lg font-semibold text-gray-900">
                        {plan.max_analyses === -1 ? "∞" : plan.max_analyses}
                      </div>
                      <div className="text-xs text-gray-600">
                        análises{plan.max_analyses === -1 ? " ilimitadas" : " incluídas"}
                      </div>
                    </div>
                  </div>
                  
                  {/* Features Lista */}
                  <div className="flex-1">
                    <ul className="space-y-3">
                      {plan.features.map((feature, index) => (
                        <li key={index} className="flex items-start gap-3">
                          <span className="text-green-500 mt-0.5 text-sm flex-shrink-0">✓</span>
                          <span className="text-sm text-gray-700 leading-relaxed">{feature}</span>
                        </li>
                      ))}
                    </ul>
                  </div>
                  
                  {/* Economia (para plano popular) */}
                  {isPopular && (
                    <div className="mt-4 p-3 bg-gradient-to-r from-green-50 to-emerald-50 border border-green-200 rounded-lg">
                      <div className="flex items-center gap-2">
                        <span className="text-green-600">💰</span>
                        <span className="text-sm font-medium text-green-800">
                          Economia de até 60% vs. pagamento avulso
                        </span>
                      </div>
                    </div>
                  )}
                </CardContent>
                
                <CardFooter className="px-4 sm:px-6 pb-6">
                  <Button
                    onClick={() => handleSubscription(plan.id)}
                    disabled={processingPayment === plan.id || isCurrentPlan}
                    className={`w-full h-12 font-medium transition-all ${
                      isPopular 
                        ? 'bg-gradient-to-r from-blue-500 to-blue-600 hover:from-blue-600 hover:to-blue-700 shadow-lg' 
                        : isCurrentPlan
                        ? 'bg-green-100 text-green-800 border-green-300'
                        : 'bg-gray-900 hover:bg-gray-800'
                    }`}
                    variant={isCurrentPlan ? "outline" : "default"}
                  >
                    {processingPayment === plan.id ? (
                      <div className="flex items-center gap-2">
                        <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
                        <span>Processando...</span>
                      </div>
                    ) : isCurrentPlan ? (
                      <div className="flex items-center gap-2">
                        <span>✅</span>
                        <span>Plano Ativo</span>
                      </div>
                    ) : (
                      <div className="flex items-center gap-2">
                        <span>🚀</span>
                        <span>{isPopular ? 'Escolher Premium' : 'Assinar Agora'}</span>
                      </div>
                    )}
                  </Button>
                  
                  {/* CTA adicional para plano popular */}
                  {isPopular && !isCurrentPlan && (
                    <p className="text-xs text-center text-gray-500 mt-2">
                      ⏰ Oferta por tempo limitado
                    </p>
                  )}
                </CardFooter>
              </Card>
            );
            })}
          </div>
        ) : (
          <Card className="text-center py-12">
            <CardContent>
              <Users />
              <h3 className="text-lg font-medium text-gray-900 mb-2 mt-4">
                Nenhum plano de assinatura disponível
              </h3>
              <p className="text-gray-500">
                No momento não há planos de assinatura disponíveis.
              </p>
            </CardContent>
          </Card>
        )}
      </div>

      {/* Informações sobre Status */}
      {(loadingPlans || loadingSubscription) && (
        <div className="mt-8 p-4 bg-blue-50 rounded-lg">
          <div className="flex items-center gap-2 text-blue-800 mb-2">
            <Loader />
            <span className="font-medium">Carregando informações...</span>
          </div>
          <div className="text-sm text-blue-700 space-y-1">
            <p>• Planos: {loadingPlans ? "Carregando..." : "✓ Carregado"}</p>
            <p>• Assinatura atual: {loadingSubscription ? "Verificando..." : "✓ Verificado"}</p>
          </div>
        </div>
      )}

      {/* Informações de Valor - Mobile-First */}
      <div className="mt-12">
        <div className="bg-gradient-to-br from-gray-50 to-white border border-gray-200 rounded-xl p-4 sm:p-8">
          <div className="text-center mb-6 sm:mb-8">
            <h3 className="text-lg sm:text-xl font-semibold mb-2">Por que escolher a Democratiza AI?</h3>
            <p className="text-gray-600 text-sm">A revolução na análise jurídica chegou</p>
          </div>
          
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-6 text-center">
            <div className="group hover:bg-white hover:shadow-lg rounded-lg p-4 transition-all">
              <div className="text-3xl sm:text-4xl mb-3 group-hover:scale-110 transition-transform">🛡️</div>
              <h4 className="font-semibold text-gray-900 mb-2 text-sm sm:text-base">Análise Segura</h4>
              <p className="text-gray-600 text-xs sm:text-sm leading-relaxed">
                Seus contratos são analisados com total segurança e privacidade
              </p>
            </div>
            
            <div className="group hover:bg-white hover:shadow-lg rounded-lg p-4 transition-all">
              <div className="text-3xl sm:text-4xl mb-3 group-hover:scale-110 transition-transform">⚡</div>
              <h4 className="font-semibold text-gray-900 mb-2 text-sm sm:text-base">Resultados Rápidos</h4>
              <p className="text-gray-600 text-xs sm:text-sm leading-relaxed">
                Análise completa em segundos com IA especializada
              </p>
            </div>
            
            <div className="group hover:bg-white hover:shadow-lg rounded-lg p-4 transition-all">
              <div className="text-3xl sm:text-4xl mb-3 group-hover:scale-110 transition-transform">📊</div>
              <h4 className="font-semibold text-gray-900 mb-2 text-sm sm:text-base">Relatórios Detalhados</h4>
              <p className="text-gray-600 text-xs sm:text-sm leading-relaxed">
                Relatórios completos com riscos e recomendações práticas
              </p>
            </div>
          </div>
          
          {/* Garantia e Suporte */}
          <div className="mt-8 pt-6 border-t border-gray-200">
            <div className="flex flex-col sm:flex-row items-center justify-center gap-4 sm:gap-8 text-center">
              <div className="flex items-center gap-2 text-sm text-gray-600">
                <span className="text-green-500">✅</span>
                <span>Satisfação garantida</span>
              </div>
              <div className="flex items-center gap-2 text-sm text-gray-600">
                <span className="text-blue-500">💬</span>
                <span>Suporte especializado</span>
              </div>
              <div className="flex items-center gap-2 text-sm text-gray-600">
                <span className="text-purple-500">🔄</span>
                <span>Cancelamento fácil</span>
              </div>
            </div>
            
            <div className="mt-4 text-center">
              <p className="text-xs text-gray-500">
                Planos atualizados em: {new Date().toLocaleString('pt-BR')}
              </p>
              {error && (
                <p className="text-xs text-yellow-600 mt-1">
                  {error}
                </p>
              )}
            </div>
          </div>
        </div>
      </div>
      </div>
    </div>
  );
}