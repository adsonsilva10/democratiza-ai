"use client";

import { useEffect, useState } from "react";
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { useApi } from "@/lib/hooks/useApi";

// Emoji icon helpers (avoid external icon lib for now)
const Shield = () => <span>🛡️</span>;
const Users = () => <span>👥</span>;
const AlertCircle = () => <span>⚠️</span>;
const Loader = () => <span>⏳</span>;

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

// Fallback (offline) data
const FALLBACK_PLANS: Plan[] = [
  {
    id: "pay_per_use",
    name: "Análise + Assinatura",
    description: "Análise completa com assinatura eletrônica",
    price: 24.9,
    duration_months: 0,
    max_analyses: 1,
    features: [
      "Análise completa do contrato",
      "Identificação de cláusulas abusivas",
      "Relatório detalhado em PDF",
      "Assinatura eletrônica integrada",
      "Certificado digital válido",
      "Suporte prioritário por chat",
      "Armazenamento seguro por 5 anos",
    ],
    is_active: true,
    type: "pay_per_use",
  },
  {
    id: "subscription_basic",
    name: "Plano Básico",
    description: "Para usuários que fazem algumas análises por mês",
    price: 49.9,
    duration_months: 1,
    max_analyses: 10,
    features: [
      "10 análises por mês",
      "Análise completa de contratos",
      "Identificação de riscos",
      "Relatórios em PDF",
      "Suporte prioritário",
    ],
    is_active: true,
    type: "subscription",
  },
  {
    id: "subscription_professional",
    name: "Plano Profissional",
    description: "Para advogados e consultores jurídicos",
    price: 79.9,
    duration_months: 1,
    max_analyses: 50,
    features: [
      "50 análises por mês",
      "Análise avançada com IA",
      "Consultas jurídicas por chat",
      "Assinatura eletrônica básica",
      "Relatórios personalizados",
      "Suporte prioritário por WhatsApp",
      "Histórico completo de análises",
    ],
    is_active: true,
    type: "subscription",
  },
  {
    id: "subscription_premium",
    name: "Plano Enterprise",
    description: "Para empresas e escritórios de advocacia",
    price: 149.9,
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
      "Treinamento da equipe",
    ],
    is_active: true,
    type: "subscription",
  },
];

export default function PlanosPage() {
  const { apiRequest } = useApi();
  const [plans, setPlans] = useState<Plan[]>([]);
  const [userSubscription, setUserSubscription] = useState<UserSubscription | null>(null);
  const [loadingPlans, setLoadingPlans] = useState(true);
  const [loadingSubscription, setLoadingSubscription] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [processingPayment, setProcessingPayment] = useState<string | null>(null);

  // Derived global loading
  const globalLoading = loadingPlans && loadingSubscription;

  useEffect(() => {
    (async () => {
      await Promise.all([loadPlans(), loadUserSub()]);
    })();
  }, []);

  async function loadPlans() {
    try {
      setLoadingPlans(true);
      setError(null);
      const response = await apiRequest("/api/v1/payments/plans");
      if (response.success && response.data?.plans) {
        setPlans(response.data.plans);
      } else {
        setPlans(FALLBACK_PLANS);
      }
    } catch (e) {
      console.warn("Falha ao carregar planos, usando fallback", e);
      setPlans(FALLBACK_PLANS);
      setError(null);
    } finally {
      setLoadingPlans(false);
    }
  }

  async function loadUserSub() {
    try {
      setLoadingSubscription(true);
      const response = await apiRequest("/api/v1/payments/user/subscription");
      if (response.success && response.data?.subscription) {
        setUserSubscription(response.data.subscription);
      }
    } catch (e) {
      console.warn("Falha ao obter assinatura do usuário", e);
    } finally {
      setLoadingSubscription(false);
    }
  }

  function formatPrice(price: number) {
    return new Intl.NumberFormat("pt-BR", { style: "currency", currency: "BRL" }).format(price);
  }

  function formatDate(dateString: string) {
    return new Intl.DateTimeFormat("pt-BR", { day: "2-digit", month: "2-digit", year: "numeric" }).format(new Date(dateString));
  }

  async function handlePayPerUse(planId: string) {
    try {
      setProcessingPayment("pay_per_use");
      const plan = plans.find(p => p.id === planId);
      if (plan && FALLBACK_PLANS.some(fp => fp.id === planId)) {
        alert(`Funcionalidade temporariamente indisponível.\n\nPlano: ${plan.name}\nPreço: ${formatPrice(plan.price)}`);
        return;
      }
      const response = await apiRequest("/api/v1/payments/pay-per-use", {
        method: "POST",
        body: JSON.stringify({ plan_id: planId }),
        headers: { "Content-Type": "application/json" },
      });
      if (response.success && response.data?.payment_url) {
        window.open(response.data.payment_url, "_blank");
      } else {
        throw new Error(response.error || "Erro ao criar pagamento");
      }
    } catch (e) {
      console.error(e);
      alert("Erro ao processar pagamento. Tente novamente.");
    } finally {
      setProcessingPayment(null);
    }
  }

  async function handleSubscription(planId: string) {
    try {
      setProcessingPayment(planId);
      const plan = plans.find(p => p.id === planId);
      if (plan && FALLBACK_PLANS.some(fp => fp.id === planId)) {
        alert(`Funcionalidade temporariamente indisponível.\n\nPlano: ${plan.name}\nPreço: ${formatPrice(plan.price)}/mês`);
        return;
      }
      const response = await apiRequest("/api/v1/payments/subscription", {
        method: "POST",
        body: JSON.stringify({ plan_id: planId }),
        headers: { "Content-Type": "application/json" },
      });
      if (response.success && response.data?.payment_url) {
        window.open(response.data.payment_url, "_blank");
      } else {
        throw new Error(response.error || "Erro ao criar assinatura");
      }
    } catch (e) {
      console.error(e);
      alert("Erro ao processar assinatura. Tente novamente.");
    } finally {
      setProcessingPayment(null);
    }
  }

  const payPerUsePlans = plans.filter(p => p.type === "pay_per_use");
  const subscriptionPlans = plans.filter(p => p.type === "subscription");

  // Loading skeleton page
  if (globalLoading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-gray-50 to-white">
        <Header />
        <div className="container mx-auto px-4 py-12 flex flex-col items-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mb-4" />
          <div className="flex items-center gap-2 text-gray-600">
            <Loader />
            <span>Carregando planos disponíveis...</span>
          </div>
          <p className="text-sm text-gray-500 mt-2">Verificando as melhores opções para você</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-white">
      <Header />
      <div className="container mx-auto px-4 py-6 sm:py-12">
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

        {!loadingSubscription && userSubscription?.is_active && (
          <Card className="mb-8 border-green-200 bg-green-50">
            <CardHeader>
              <div className="flex items-center gap-2">
                <Shield />
                <CardTitle className="text-green-800">Plano Ativo</CardTitle>
              </div>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <Info label="Plano Atual" value={userSubscription.plan.name} />
                <Info label="Válido até" value={formatDate(userSubscription.expires_at)} />
                <Info
                  label="Análises Restantes"
                  value={
                    userSubscription.plan.max_analyses === -1
                      ? "Ilimitado"
                      : String(userSubscription.remaining_analyses)
                  }
                />
              </div>
            </CardContent>
          </Card>
        )}

        {payPerUsePlans.length > 0 && (
          <section className="mb-12">
            <div className="bg-gradient-to-r from-amber-50 to-orange-50 border border-amber-200 rounded-xl p-4 sm:p-6">
              <div className="text-center mb-6">
                <div className="flex items-center justify-center gap-2 mb-2">
                  <span className="text-xl">💰</span>
                  <h3 className="text-lg sm:text-xl font-semibold text-gray-900">Precisa de apenas 1 análise?</h3>
                </div>
                <p className="text-gray-600 text-sm sm:text-base">Pague somente pelo que usar, sem compromisso mensal</p>
              </div>
              <div className="max-w-md mx-auto">
                {payPerUsePlans.map(plan => (
                  <div key={plan.id} className="bg-white rounded-lg p-4 sm:p-6 shadow-md border-2 border-amber-300 relative">
                    <div className="absolute -top-3 left-1/2 -translate-x-1/2">
                      <span className="bg-gradient-to-r from-amber-500 to-orange-500 text-white px-3 py-1 rounded-full text-xs font-medium">
                        🔥 Mais Completo
                      </span>
                    </div>
                    <div className="text-center mb-4">
                      <h4 className="text-lg font-semibold text-gray-900 mb-2">{plan.name}</h4>
                      <div className="text-2xl sm:text-3xl font-bold text-amber-600 mb-1">{formatPrice(plan.price)}</div>
                      <p className="text-sm text-gray-500">{plan.description}</p>
                    </div>
                    <ul className="space-y-2 mb-6">
                      {plan.features.map((f, i) => (
                        <li key={i} className="flex items-center gap-2 text-sm text-gray-700">
                          <span className="text-green-500">✓</span>
                          <span>{f}</span>
                        </li>
                      ))}
                    </ul>
                    <Button
                      onClick={() => handlePayPerUse(plan.id)}
                      disabled={processingPayment === "pay_per_use"}
                      className="w-full bg-gradient-to-r from-amber-500 to-orange-500 hover:from-amber-600 hover:to-orange-600"
                    >
                      {processingPayment === "pay_per_use" ? (
                        <div className="flex items-center gap-2">
                          <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white" />
                          Processando...
                        </div>
                      ) : (
                        <div className="flex items-center justify-center gap-2">
                          <span>✍️</span>
                          <span>Analisar + Assinar</span>
                        </div>
                      )}
                    </Button>
                  </div>
                ))}
              </div>
            </div>
          </section>
        )}

        <section className="mb-16">
          <div className="text-center mb-8 sm:mb-12">
            <div className="flex items-center justify-center gap-2 mb-4">
              <span className="text-2xl">⭐</span>
              <h2 className="text-xl sm:text-2xl font-bold text-gray-900">Planos de Assinatura</h2>
            </div>
            <p className="text-gray-600 text-sm sm:text-base max-w-lg mx-auto">Análises mensais com economia e recursos exclusivos</p>
          </div>
          {loadingPlans ? (
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-6">
              {[1, 2, 3].map(i => (
                <Card key={i} className="animate-pulse">
                  <CardHeader className="pb-4">
                    <div className="h-6 bg-gray-200 rounded mb-2" />
                    <div className="h-4 bg-gray-200 rounded" />
                  </CardHeader>
                  <CardContent className="pb-6">
                    <div className="h-12 bg-gray-200 rounded mb-4" />
                    <div className="space-y-3">
                      <div className="h-3 bg-gray-200 rounded" />
                      <div className="h-3 bg-gray-200 rounded" />
                      <div className="h-3 bg-gray-200 rounded" />
                    </div>
                  </CardContent>
                  <CardFooter>
                    <div className="h-12 bg-gray-200 rounded w-full" />
                  </CardFooter>
                </Card>
              ))}
            </div>
          ) : subscriptionPlans.length > 0 ? (
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-6 max-w-6xl mx-auto">
              {subscriptionPlans.map(plan => {
                const isPopular = plan.name.toLowerCase().includes("premium");
                const isCurrent = userSubscription?.plan.id === plan.id;
                let cardClass = "relative transition-all duration-300 hover:shadow-lg";
                let headerGradient = "bg-white";
                let badge: JSX.Element | null = null;
                if (isPopular) {
                  cardClass += " border-2 border-blue-500 shadow-xl transform lg:scale-105 z-10";
                  headerGradient = "bg-gradient-to-r from-blue-500 to-blue-600 text-white";
                  badge = (
                    <div className="absolute -top-3 left-1/2 -translate-x-1/2 z-20">
                      <Badge className="bg-gradient-to-r from-orange-500 to-red-500 text-white px-4 py-1 shadow-lg">🔥 Mais Popular</Badge>
                    </div>
                  );
                } else if (isCurrent) {
                  cardClass += " border-2 border-green-500 bg-green-50";
                  badge = (
                    <div className="absolute -top-3 left-1/2 -translate-x-1/2 z-20">
                      <Badge className="bg-green-500 text-white px-4 py-1">✅ Plano Atual</Badge>
                    </div>
                  );
                }
                return (
                  <Card key={plan.id} className={cardClass}>
                    {badge}
                    <CardHeader className={`${headerGradient} rounded-t-lg ${isPopular ? "text-white" : ""}`}>
                      <div className="text-center">
                        <CardTitle className={`text-lg sm:text-xl mb-2 ${isPopular ? "text-white" : "text-gray-900"}`}>{plan.name}</CardTitle>
                        <CardDescription className={`text-sm ${isPopular ? "text-blue-100" : "text-gray-600"}`}>{plan.description}</CardDescription>
                      </div>
                    </CardHeader>
                    <CardContent className="px-4 sm:px-6 py-6 flex-1 flex flex-col">
                      <div className="text-center mb-6">
                        <div className={`text-2xl sm:text-3xl font-bold mb-1 ${isPopular ? "text-blue-600" : "text-gray-900"}`}>{formatPrice(plan.price)}</div>
                        <p className="text-xs sm:text-sm text-gray-500">por {plan.duration_months} mês{plan.duration_months > 1 ? "es" : ""}</p>
                        <div className="mt-3 p-2 bg-gray-50 rounded-lg">
                          <div className="text-lg font-semibold text-gray-900">{plan.max_analyses === -1 ? "∞" : plan.max_analyses}</div>
                          <div className="text-xs text-gray-600">análises{plan.max_analyses === -1 ? " ilimitadas" : " incluídas"}</div>
                        </div>
                      </div>
                      <ul className="flex-1 space-y-3">
                        {plan.features.map((f, i) => (
                          <li key={i} className="flex items-start gap-3">
                            <span className="text-green-500 mt-0.5 text-sm">✓</span>
                            <span className="text-sm text-gray-700 leading-relaxed">{f}</span>
                          </li>
                        ))}
                      </ul>
                      {isPopular && (
                        <div className="mt-4 p-3 bg-gradient-to-r from-green-50 to-emerald-50 border border-green-200 rounded-lg">
                          <div className="flex items-center gap-2">
                            <span className="text-green-600">💰</span>
                            <span className="text-sm font-medium text-green-800">Economia de até 60% vs. pagamento avulso</span>
                          </div>
                        </div>
                      )}
                    </CardContent>
                    <CardFooter className="px-4 sm:px-6 pb-6">
                      <Button
                        onClick={() => handleSubscription(plan.id)}
                        disabled={processingPayment === plan.id || isCurrent}
                        className={`w-full h-12 font-medium transition-all ${
                          isPopular
                            ? "bg-gradient-to-r from-blue-500 to-blue-600 hover:from-blue-600 hover:to-blue-700 shadow-lg"
                            : isCurrent
                            ? "bg-green-100 text-green-800 border-green-300"
                            : "bg-gray-900 hover:bg-gray-800"
                        }`}
                        variant={isCurrent ? "outline" : "default"}
                      >
                        {processingPayment === plan.id ? (
                          <div className="flex items-center gap-2">
                            <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white" />
                            <span>Processando...</span>
                          </div>
                        ) : isCurrent ? (
                          <div className="flex items-center gap-2">
                            <span>✅</span>
                            <span>Plano Ativo</span>
                          </div>
                        ) : (
                          <div className="flex items-center gap-2">
                            <span>🚀</span>
                            <span>{isPopular ? "Escolher Premium" : "Assinar Agora"}</span>
                          </div>
                        )}
                      </Button>
                      {isPopular && !isCurrent && (
                        <p className="text-xs text-center text-gray-500 mt-2">⏰ Oferta por tempo limitado</p>
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
                <h3 className="text-lg font-medium text-gray-900 mb-2 mt-4">Nenhum plano de assinatura disponível</h3>
                <p className="text-gray-500">No momento não há planos de assinatura disponíveis.</p>
              </CardContent>
            </Card>
          )}
        </section>

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

        <section className="mt-12">
          <div className="bg-gradient-to-br from-gray-50 to-white border border-gray-200 rounded-xl p-4 sm:p-8">
            <div className="text-center mb-6 sm:mb-8">
              <h3 className="text-lg sm:text-xl font-semibold mb-2">Por que escolher a Democratiza AI?</h3>
              <p className="text-gray-600 text-sm">A revolução na análise jurídica chegou</p>
            </div>
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-6 text-center">
              <ValueBox icon="🛡️" title="Análise Segura" text="Seus contratos são analisados com total segurança e privacidade" />
              <ValueBox icon="⚡" title="Resultados Rápidos" text="Análise completa em segundos com IA especializada" />
              <ValueBox icon="📊" title="Relatórios Detalhados" text="Relatórios completos com riscos e recomendações práticas" />
            </div>
            <div className="mt-8 pt-6 border-t border-gray-200">
              <div className="flex flex-col sm:flex-row items-center justify-center gap-4 sm:gap-8 text-center">
                <Tag text="✅ Satisfação garantida" />
                <Tag text="💬 Suporte especializado" />
                <Tag text="🔄 Cancelamento fácil" />
              </div>
              <div className="mt-4 text-center">
                <p className="text-xs text-gray-500">Planos atualizados em: {new Date().toLocaleString("pt-BR")}</p>
                {error && <p className="text-xs text-yellow-600 mt-1">{error}</p>}
              </div>
            </div>
          </div>
        </section>
      </div>
    </div>
  );
}

// Reusable UI fragments
function Header() {
  return (
    <div className="bg-white border-b border-gray-200 px-4 md:px-6 py-4">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-xl md:text-3xl font-bold text-gray-900">💳 Escolha seu Plano</h1>
          <p className="text-sm md:text-base text-gray-600 mt-1">Democratize a análise jurídica com nossos planos flexíveis</p>
        </div>
        <div className="hidden lg:flex items-center gap-4">
          <Badge variant="secondary" className="bg-green-100 text-green-700">⚡ Análise em 45s</Badge>
          <Badge variant="secondary" className="bg-blue-100 text-blue-700">🛡️ 98.7% de precisão</Badge>
        </div>
      </div>
    </div>
  );
}

function Info({ label, value }: { label: string; value: string }) {
  return (
    <div>
      <p className="text-sm text-green-600">{label}</p>
      <p className="font-medium text-green-800">{value}</p>
    </div>
  );
}

function ValueBox({ icon, title, text }: { icon: string; title: string; text: string }) {
  return (
    <div className="group hover:bg-white hover:shadow-lg rounded-lg p-4 transition-all">
      <div className="text-3xl sm:text-4xl mb-3 group-hover:scale-110 transition-transform">{icon}</div>
      <h4 className="font-semibold text-gray-900 mb-2 text-sm sm:text-base">{title}</h4>
      <p className="text-gray-600 text-xs sm:text-sm leading-relaxed">{text}</p>
    </div>
  );
}

function Tag({ text }: { text: string }) {
  return <div className="flex items-center gap-2 text-sm text-gray-600"><span>{text}</span></div>;
}