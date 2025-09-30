'use client'

import { useState, useEffect } from 'react'
import Link from 'next/link'
import { Button } from '@/components/ui/button'
import { Card, CardContent } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { ArrowRight, CheckCircle, Shield, Zap, Users, FileText, MessageSquare, PenTool, Star, Menu, X, Play, AlertTriangle, Heart, Brain } from 'lucide-react'

export default function HomePage() {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false)
  const [activeTestimonial, setActiveTestimonial] = useState(0)

  // Auto-rotate testimonials
  useEffect(() => {
    const interval = setInterval(() => {
      setActiveTestimonial((prev) => (prev + 1) % testimonials.length)
    }, 5000)
    return () => clearInterval(interval)
  }, [])

  const painPoints = [
    {
      icon: "😰",
      title: "Medo de Assinar",
      description: "Você hesita antes de assinar qualquer documento porque já foi enganado antes"
    },
    {
      icon: "💸",
      title: "Prejuízos Financeiros", 
      description: "Perdeu dinheiro por não entender cláusulas abusivas escondidas no contrato"
    },
    {
      icon: "⚖️",
      title: "Direitos Ignorados",
      description: "Suas reclamações foram ignoradas porque você não conhecia seus direitos"
    },
    {
      icon: "🤝",
      title: "Confiança Quebrada",
      description: "Se sente vulnerável em negociações por não ter conhecimento jurídico"
    }
  ]

  const realStories = [
    {
      name: "Ailton Silva",
      avatar: "👨‍💼",
      profession: "Aposentado",
      title: "Advogado me cobrou mesmo sem resultado",
      story: "Fui enganado pelo meu advogado. Contratei ele para conseguir minha aposentadoria especial, porém no meio do processo eu consegui me aposentar por idade. Mesmo não sendo algo acordado com antecedência, ele me cobrou os honorários da mesma forma.",
      pain: "Falta de transparência nos contratos",
      gradient: "from-red-50 to-orange-50", 
      borderColor: "border-red-200"
    },
    {
      name: "Adson Patrique",
      avatar: "🏠",
      profession: "Inquilino",
      title: "Prejuízo com contrato de aluguel",
      story: "Aluguei um apartamento e 3 meses depois acabou o gás da geladeira. O proprietário se recusou a dar assistência pois afirmou que o contrato sinalizava que tudo era responsabilidade do inquilino. Nessa eu tive prejuízo pois não consegui identificar os perigos subliminares no contrato.",
      pain: "Cláusulas abusivas escondidas",
      gradient: "from-blue-50 to-indigo-50",
      borderColor: "border-blue-200"
    }
  ]

  const features = [
    {
      icon: <Brain className="h-8 w-8" />,
      title: "IA que Entende Por Você",
      description: "Nossa inteligência artificial lê e explica cada palavra do seu contrato em linguagem simples",
      gradient: "from-blue-500 to-cyan-500",
      bgGradient: "from-blue-50 to-cyan-50", 
      benefit: "Nunca mais seja pego de surpresa"
    },
    {
      icon: <Shield className="h-8 w-8" />,
      title: "Proteção Contra Abusos",
      description: "Identificamos cláusulas abusivas e te mostramos exatamente quais são seus direitos",
      gradient: "from-red-500 to-orange-500",
      bgGradient: "from-red-50 to-orange-50",
      benefit: "Defenda-se antes de ser prejudicado"
    },
    {
      icon: <PenTool className="h-8 w-8" />,
      title: "Assinatura Segura", 
      description: "Assine apenas quando tiver certeza absoluta, com nossa validação jurídica completa",
      gradient: "from-green-500 to-emerald-500",
      bgGradient: "from-green-50 to-emerald-50",
      benefit: "Segurança total em suas decisões"
    },
    {
      icon: <MessageSquare className="h-8 w-8" />,
      title: "Advogado Virtual 24/7",
      description: "Tire suas dúvidas a qualquer hora com nosso assistente jurídico especializado",
      gradient: "from-purple-500 to-violet-500",
      bgGradient: "from-purple-50 to-violet-50",
      benefit: "Conhecimento jurídico na palma da mão"
    }
  ]

  const testimonials = [
    {
      name: "Carla Santos",
      role: "Empreendedora", 
      company: "Salão de Beleza",
      content: "Descobri que meu contrato de aluguel tinha uma cláusula que me permitia reduzir o valor em 40% durante a pandemia. Economizei R$ 18.000! Nunca mais vou assinar algo sem analisar aqui primeiro.",
      rating: 5,
      avatar: "💇‍♀️",
      savings: "R$ 18.000 economizados"
    },
    {
      name: "Roberto Lima",
      role: "Aposentado",
      company: "Construção Civil",
      content: "Quase assinei um contrato de empréstimo com juros abusivos. A plataforma me alertou e me ajudou a negociar condições 60% melhores. Me sinto protegido agora.",
      rating: 5,
      avatar: "👷‍♂️", 
      savings: "60% menos juros"
    },
    {
      name: "Ana Beatriz",
      role: "Mãe e Freelancer",
      company: "Designer Gráfica",
      content: "Sempre tive medo de contratos porque já fui enganada. Agora entendo exatamente o que estou assinando e posso negociar de igual para igual. Mudou minha vida!",
      rating: 5,
      avatar: "👩‍💻",
      savings: "Confiança recuperada"
    }
  ]

  const stats = [
    { value: "R$ 2.3M+", label: "Economizados pelos usuários", icon: "💰" },
    { value: "94%", label: "Identificam cláusulas abusivas", icon: "🎯" },
    { value: "45s", label: "Para entender seu contrato", icon: "⚡" },
    { value: "Zero", label: "Surpresas desagradáveis", icon: "✅" }
  ]

  const transformationSteps = [
    {
      step: "1",
      title: "Você Envia",
      description: "Foto, PDF, ou digite seu contrato. Qualquer formato serve.",
      icon: "📤",
      color: "blue"
    },
    {
      step: "2",
      title: "IA Traduz", 
      description: "Transformamos juridiquês em português claro que você entende.",
      icon: "🤖",
      color: "purple"
    },
    {
      step: "3",
      title: "Você Decide",
      description: "Com conhecimento total, você assina ou negocia com confiança.",
      icon: "✅",
      color: "green"
    }
  ]

  const fears = [
    "Medo de ser enganado novamente",
    "Não entender termos jurídicos", 
    "Assinar algo prejudicial",
    "Não saber seus direitos",
    "Ser tratado como inferior",
    "Perder dinheiro por ignorância"
  ]
  
  return (
    <div className="min-h-screen bg-white">
      {/* Header Navigation */}
      <header className="sticky top-0 z-50 bg-white/95 backdrop-blur-md border-b border-gray-100">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16 lg:h-20">
            {/* Logo */}
            <div className="flex items-center gap-3">
              <div className="w-8 h-8 lg:w-10 lg:h-10 bg-gradient-to-br from-blue-600 to-purple-600 rounded-xl flex items-center justify-center shadow-lg">
                <span className="text-white font-bold text-sm lg:text-base">⚖️</span>
              </div>
              <div>
                <h1 className="font-bold text-lg lg:text-xl text-gray-900">Democratiza AI</h1>
                <p className="text-xs text-gray-600 hidden sm:block">Seus direitos protegidos</p>
              </div>
            </div>

            {/* Desktop Navigation */}
            <nav className="hidden lg:flex items-center gap-8">
              <a href="#como-funciona" className="text-gray-600 hover:text-gray-900 transition-colors font-medium">Como Funciona</a>
              <a href="#protecao" className="text-gray-600 hover:text-gray-900 transition-colors font-medium">Proteção</a>
              <a href="#historias-reais" className="text-gray-600 hover:text-gray-900 transition-colors font-medium">Histórias Reais</a>
              <div className="flex items-center gap-3">
                <Link href="/plataforma">
                  <Button variant="ghost" className="font-medium">Entrar</Button>
                </Link>
                <Link href="/plataforma/analise">
                  <Button className="bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 shadow-lg">
                    Proteger Agora
                  </Button>
                </Link>
              </div>
            </nav>

            {/* Mobile Menu Button */}
            <button
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              className="lg:hidden p-2 text-gray-600 hover:text-gray-900 transition-colors"
            >
              {mobileMenuOpen ? <X className="h-6 w-6" /> : <Menu className="h-6 w-6" />}
            </button>
          </div>

          {/* Mobile Menu */}
          {mobileMenuOpen && (
            <div className="lg:hidden absolute top-16 left-0 right-0 bg-white border-b border-gray-100 shadow-lg">
              <nav className="px-4 py-6 space-y-4">
                <a href="#como-funciona" className="block text-gray-600 hover:text-gray-900 transition-colors font-medium py-2">Como Funciona</a>
                <a href="#protecao" className="block text-gray-600 hover:text-gray-900 transition-colors font-medium py-2">Proteção</a>
                <a href="#historias-reais" className="block text-gray-600 hover:text-gray-900 transition-colors font-medium py-2">Histórias Reais</a>
                <div className="pt-4 border-t border-gray-100 space-y-3">
                  <Link href="/plataforma" className="block">
                    <Button variant="ghost" className="w-full justify-center font-medium">Entrar</Button>
                  </Link>
                  <Link href="/plataforma/analise" className="block">
                    <Button className="w-full justify-center bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 shadow-lg">
                      Proteger Agora
                    </Button>
                  </Link>
                </div>
              </nav>
            </div>
          )}
        </div>
      </header>

      {/* Hero Section - Mobile First Design */}
      <div className="container mx-auto px-4 py-8 sm:py-16">
        <div className="text-center mb-12 sm:mb-16">
          {/* Trust Badge */}
          <div className="inline-flex items-center gap-2 bg-green-100 text-green-800 px-4 py-2 rounded-full text-sm font-medium mb-6">
            <span className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></span>
            Confiado por 10.000+ brasileiros
          </div>
          
          <h1 className="text-4xl sm:text-6xl font-bold text-gray-900 mb-6 leading-tight">
            Nunca Assine um<br />
            <span className="bg-gradient-to-r from-red-500 to-orange-500 bg-clip-text text-transparent">
              Contrato Arriscado
            </span>
          </h1>
          
          <p className="text-lg sm:text-xl text-gray-600 mb-8 max-w-3xl mx-auto leading-relaxed">
            IA especializada analisa seus contratos em <strong className="text-blue-600">3 segundos</strong>. 
            Identifica riscos, cláusulas abusivas e protege seus direitos.
          </p>
          
          {/* Key Benefits */}
          <div className="flex flex-wrap justify-center gap-4 mb-8">
            <div className="flex items-center gap-2 bg-white/70 backdrop-blur-sm px-4 py-2 rounded-full shadow-sm">
              <span className="text-blue-500">⚡</span>
              <span className="text-sm font-medium text-gray-700">3 segundos</span>
            </div>
            <div className="flex items-center gap-2 bg-white/70 backdrop-blur-sm px-4 py-2 rounded-full shadow-sm">
              <span className="text-green-500">🔒</span>
              <span className="text-sm font-medium text-gray-700">100% seguro</span>
            </div>
            <div className="flex items-center gap-2 bg-white/70 backdrop-blur-sm px-4 py-2 rounded-full shadow-sm">
              <span className="text-purple-500">🎯</span>
              <span className="text-sm font-medium text-gray-700">97% precisão</span>
            </div>
          </div>
          
          <div className="flex flex-col sm:flex-row gap-4 justify-center max-w-md mx-auto">
            <button className="bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white px-8 py-4 rounded-xl font-semibold transition-all transform hover:scale-105 shadow-lg flex items-center justify-center gap-2">
              <span className="text-xl">📄</span>
              Analisar Grátis
            </button>
            <Link 
              href="/chat"
              className="border-2 border-blue-200 text-blue-700 hover:bg-blue-50 hover:border-blue-300 px-8 py-4 rounded-xl font-semibold transition-all text-center flex items-center justify-center gap-2"
            >
              <span className="text-xl">💬</span>
              Conversar com IA
            </Link>
          </div>
        </div>

        {/* Process Steps - Visual Storytelling */}
        <div className="mb-16">
          <h2 className="text-3xl sm:text-4xl font-bold text-center mb-4">
            Análise em 3 passos simples
          </h2>
          <p className="text-gray-600 text-center mb-12 max-w-2xl mx-auto">
            Do upload aos insights em menos de 5 segundos. Nenhuma expertise jurídica necessária.
          </p>
          
          <div className="grid md:grid-cols-3 gap-8 max-w-5xl mx-auto">
            {/* Step 1 */}
            <div className="relative">
              <div className="bg-white rounded-2xl shadow-lg p-8 h-full hover:shadow-xl transition-all duration-300 hover:-translate-y-2">
                <div className="flex items-center justify-center w-16 h-16 bg-gradient-to-r from-blue-500 to-purple-500 rounded-full text-white text-2xl font-bold mb-6 mx-auto">
                  1
                </div>
                <div className="text-6xl text-center mb-4">📄</div>
                <h3 className="text-xl font-bold mb-4 text-center">Envie seu contrato</h3>
                <p className="text-gray-600 text-center leading-relaxed">
                  Arraste e solte seu contrato ou cole o texto diretamente. 
                  Suportamos PDF, Word e texto com segurança enterprise.
                </p>
                <div className="flex flex-wrap gap-2 justify-center mt-4">
                  <span className="bg-blue-100 text-blue-800 px-3 py-1 rounded-full text-sm">PDF</span>
                  <span className="bg-green-100 text-green-800 px-3 py-1 rounded-full text-sm">DOCX</span>
                  <span className="bg-purple-100 text-purple-800 px-3 py-1 rounded-full text-sm">TXT</span>
                </div>
              </div>
              {/* Connector Arrow */}
              <div className="hidden md:block absolute top-1/2 -right-4 w-8 h-8 text-gray-300">
                <svg fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clipRule="evenodd" />
                </svg>
              </div>
            </div>

            {/* Step 2 */}
            <div className="relative">
              <div className="bg-white rounded-2xl shadow-lg p-8 h-full hover:shadow-xl transition-all duration-300 hover:-translate-y-2">
                <div className="flex items-center justify-center w-16 h-16 bg-gradient-to-r from-purple-500 to-pink-500 rounded-full text-white text-2xl font-bold mb-6 mx-auto">
                  2
                </div>
                <div className="text-6xl text-center mb-4">🤖</div>
                <h3 className="text-xl font-bold mb-4 text-center">IA analisa cada cláusula</h3>
                <p className="text-gray-600 text-center leading-relaxed">
                  Nossa IA avançada escaneia linha por linha, identificando riscos potenciais, 
                  linguagem tendenciosa e termos injustos usando machine learning.
                </p>
                <div className="flex flex-wrap gap-2 justify-center mt-4">
                  <span className="bg-orange-100 text-orange-800 px-3 py-1 rounded-full text-sm">500+ categorias</span>
                  <span className="bg-red-100 text-red-800 px-3 py-1 rounded-full text-sm">Detecção de viés</span>
                </div>
              </div>
              {/* Connector Arrow */}
              <div className="hidden md:block absolute top-1/2 -right-4 w-8 h-8 text-gray-300">
                <svg fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clipRule="evenodd" />
                </svg>
              </div>
            </div>

            {/* Step 3 */}
            <div className="bg-white rounded-2xl shadow-lg p-8 h-full hover:shadow-xl transition-all duration-300 hover:-translate-y-2">
              <div className="flex items-center justify-center w-16 h-16 bg-gradient-to-r from-green-500 to-emerald-500 rounded-full text-white text-2xl font-bold mb-6 mx-auto">
                3
              </div>
              <div className="text-6xl text-center mb-4">📊</div>
              <h3 className="text-xl font-bold mb-4 text-center">Receba insights acionáveis</h3>
              <p className="text-gray-600 text-center leading-relaxed">
                Relatório completo com níveis de risco, explicações em linguagem simples 
                e recomendações específicas para negociação.
              </p>
              <div className="flex flex-wrap gap-2 justify-center mt-4">
                <span className="bg-green-100 text-green-800 px-3 py-1 rounded-full text-sm">Score de risco</span>
                <span className="bg-blue-100 text-blue-800 px-3 py-1 rounded-full text-sm">Sugestões</span>
              </div>
            </div>
          </div>
        </div>

        {/* Features Grid - Enhanced */}
        <div className="grid md:grid-cols-3 gap-8 mb-16">
          <div className="bg-white/80 backdrop-blur-sm p-8 rounded-2xl shadow-lg hover:shadow-xl transition-all duration-300 hover:-translate-y-2 border border-white/20">
            <div className="text-5xl mb-6 text-center">🧠</div>
            <h3 className="text-xl font-semibold mb-4 text-center">IA Avançada</h3>
            <p className="text-gray-600 text-center leading-relaxed mb-4">
              Modelos de machine learning treinados em milhões de contratos brasileiros 
              identificam riscos que revisores humanos frequentemente perdem.
            </p>
            <div className="text-center">
              <span className="bg-blue-100 text-blue-800 px-3 py-1 rounded-full text-sm font-medium">
                97% precisão
              </span>
            </div>
          </div>
          
          <div className="bg-white/80 backdrop-blur-sm p-8 rounded-2xl shadow-lg hover:shadow-xl transition-all duration-300 hover:-translate-y-2 border border-white/20">
            <div className="text-5xl mb-6 text-center">⚡</div>
            <h3 className="text-xl font-semibold mb-4 text-center">Resultados Instantâneos</h3>
            <p className="text-gray-600 text-center leading-relaxed mb-4">
              Análise completa de contratos em menos de 5 segundos. 
              Sem mais esperar dias por revisão jurídica.
            </p>
            <div className="text-center">
              <span className="bg-green-100 text-green-800 px-3 py-1 rounded-full text-sm font-medium">
                3 segundos
              </span>
            </div>
          </div>
          
          <div className="bg-white/80 backdrop-blur-sm p-8 rounded-2xl shadow-lg hover:shadow-xl transition-all duration-300 hover:-translate-y-2 border border-white/20">
            <div className="text-5xl mb-6 text-center">🛡️</div>
            <h3 className="text-xl font-semibold mb-4 text-center">Detecção de Riscos</h3>
            <p className="text-gray-600 text-center leading-relaxed mb-4">
              Identifica automaticamente linguagem tendenciosa, taxas ocultas, 
              cláusulas de rescisão injustas e problemas de propriedade intelectual.
            </p>
            <div className="text-center">
              <span className="bg-purple-100 text-purple-800 px-3 py-1 rounded-full text-sm font-medium">
                50+ categorias
              </span>
            </div>
          </div>
        </div>

        {/* Upload Section - Enhanced */}
        <div className="bg-white/90 backdrop-blur-sm rounded-3xl shadow-2xl p-8 sm:p-12 max-w-4xl mx-auto border border-white/20">
          <div className="text-center mb-8">
            <h2 className="text-2xl sm:text-3xl font-bold mb-4">
              🚀 Comece agora - Análise gratuita
            </h2>
            <p className="text-gray-600 max-w-2xl mx-auto">
              Faça upload do seu contrato e receba um relatório detalhado em segundos. 
              Sem cadastro necessário para o primeiro teste.
            </p>
          </div>
          
          <SimpleUploadManager 
            onFileSelect={handleFileSelect}
            onUploadComplete={handleUploadComplete}
          />
          
          {/* Trust Indicators */}
          <div className="flex flex-wrap justify-center gap-6 mt-8 pt-8 border-t border-gray-200">
            <div className="flex items-center gap-2 text-sm text-gray-600">
              <span className="text-green-500">🔒</span>
              <span>Criptografia end-to-end</span>
            </div>
            <div className="flex items-center gap-2 text-sm text-gray-600">
              <span className="text-blue-500">📋</span>
              <span>Conforme LGPD</span>
            </div>
            <div className="flex items-center gap-2 text-sm text-gray-600">
              <span className="text-purple-500">🗑️</span>
              <span>Dados excluídos após análise</span>
            </div>
          </div>
        </div>

        {/* Social Proof Section */}
        <div className="mt-20">
          <div className="text-center mb-12">
            <h2 className="text-3xl sm:text-4xl font-bold mb-4">
              Confiado por profissionais em todo o Brasil
            </h2>
            <p className="text-gray-600 max-w-2xl mx-auto">
              Junte-se a milhares de empresas e freelancers que protegem seus interesses 
              com cada contrato assinado.
            </p>
          </div>

          {/* Stats */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8 mb-16">
            <div className="text-center">
              <div className="text-4xl sm:text-5xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent mb-2">
                10.000+
              </div>
              <div className="text-gray-600 font-medium">Contratos Analisados</div>
            </div>
            <div className="text-center">
              <div className="text-4xl sm:text-5xl font-bold bg-gradient-to-r from-green-600 to-emerald-600 bg-clip-text text-transparent mb-2">
                97%
              </div>
              <div className="text-gray-600 font-medium">Precisão da IA</div>
            </div>
            <div className="text-center">
              <div className="text-4xl sm:text-5xl font-bold bg-gradient-to-r from-orange-600 to-red-600 bg-clip-text text-transparent mb-2">
                3s
              </div>
              <div className="text-gray-600 font-medium">Tempo Médio</div>
            </div>
            <div className="text-center">
              <div className="text-4xl sm:text-5xl font-bold bg-gradient-to-r from-purple-600 to-pink-600 bg-clip-text text-transparent mb-2">
                R$ 2.4M
              </div>
              <div className="text-gray-600 font-medium">Riscos Evitados</div>
            </div>
          </div>

          {/* Testimonials */}
          <div className="grid md:grid-cols-3 gap-8">
            <div className="bg-white/80 backdrop-blur-sm p-6 rounded-2xl shadow-lg border border-white/20">
              <div className="flex items-center gap-1 mb-4">
                {[...Array(5)].map((_, i) => (
                  <span key={i} className="text-yellow-400">⭐</span>
                ))}
                <span className="text-sm text-gray-600 ml-2">5.0</span>
              </div>
              <p className="text-gray-700 mb-4 italic">
                "Contrato Seguro salvou nossa startup R$ 50.000 ao identificar uma cláusula 
                de responsabilidade em nosso contrato com fornecedor que nossa equipe jurídica não viu."
              </p>
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 bg-gradient-to-r from-blue-500 to-purple-500 rounded-full flex items-center justify-center text-white font-bold">
                  YP
                </div>
                <div>
                  <div className="font-medium">Yogesh Patel</div>
                  <div className="text-sm text-gray-600">Gerente de Marketing Digital</div>
                </div>
              </div>
            </div>

            <div className="bg-white/80 backdrop-blur-sm p-6 rounded-2xl shadow-lg border border-white/20">
              <div className="flex items-center gap-1 mb-4">
                {[...Array(5)].map((_, i) => (
                  <span key={i} className="text-yellow-400">⭐</span>
                ))}
                <span className="text-sm text-gray-600 ml-2">5.0</span>
              </div>
              <p className="text-gray-700 mb-4 italic">
                "Como desenvolvedor freelancer, estava perdendo dinheiro com contratos ruins. 
                Agora tenho confiança para negociar melhores termos e proteger minha propriedade intelectual."
              </p>
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 bg-gradient-to-r from-green-500 to-emerald-500 rounded-full flex items-center justify-center text-white font-bold">
                  MR
                </div>
                <div>
                  <div className="font-medium">Marcus Rodriguez</div>
                  <div className="text-sm text-gray-600">Desenvolvedor Senior</div>
                </div>
              </div>
            </div>

            <div className="bg-white/80 backdrop-blur-sm p-6 rounded-2xl shadow-lg border border-white/20">
              <div className="flex items-center gap-1 mb-4">
                {[...Array(5)].map((_, i) => (
                  <span key={i} className="text-yellow-400">⭐</span>
                ))}
                <span className="text-sm text-gray-600 ml-2">5.0</span>
              </div>
              <p className="text-gray-700 mb-4 italic">
                "A velocidade é incrível. O que costumava levar dias para nossa equipe jurídica 
                agora acontece em segundos. Transformou completamente nosso processo de revisão."
              </p>
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 bg-gradient-to-r from-purple-500 to-pink-500 rounded-full flex items-center justify-center text-white font-bold">
                  ZK
                </div>
                <div>
                  <div className="font-medium">Zara Khan</div>
                  <div className="text-sm text-gray-600">Consultora Jurídica</div>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* CTA Section */}
        <div className="mt-20 text-center">
          <div className="bg-gradient-to-r from-blue-600 to-purple-600 rounded-3xl p-8 sm:p-12 text-white">
            <h2 className="text-3xl sm:text-4xl font-bold mb-4">
              Pronto para proteger seu negócio?
            </h2>
            <p className="text-xl mb-8 opacity-90 max-w-2xl mx-auto">
              Junte-se a milhares de profissionais que nunca mais assinam um contrato arriscado. 
              Comece com uma análise gratuita.
            </p>
            
            <div className="flex flex-col sm:flex-row gap-4 justify-center max-w-md mx-auto mb-8">
              <button className="bg-white text-blue-600 hover:bg-gray-100 px-8 py-4 rounded-xl font-semibold transition-all transform hover:scale-105 shadow-lg flex items-center justify-center gap-2">
                <span className="text-xl">🚀</span>
                Começar Grátis
              </button>
              <Link 
                href="/chat"
                className="border-2 border-white/30 text-white hover:bg-white/10 px-8 py-4 rounded-xl font-semibold transition-all text-center flex items-center justify-center gap-2"
              >
                <span className="text-xl">💬</span>
                Falar com IA
              </Link>
            </div>
            
            <div className="flex flex-wrap justify-center gap-6 text-sm opacity-80">
              <div className="flex items-center gap-2">
                <span>✓</span>
                <span>30 dias grátis</span>
              </div>
              <div className="flex items-center gap-2">
                <span>✓</span>
                <span>Cancele quando quiser</span>
              </div>
              <div className="flex items-center gap-2">
                <span>✓</span>
                <span>Suporte 24/7</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}