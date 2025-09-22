'use client'

import SimpleUploadManager from '@/components/features/SimpleUploadManager'
import Link from 'next/link'
import { useState } from 'react'

export default function HomePage() {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false)

  const handleFileSelect = (file: File) => {
    console.log('Arquivo selecionado:', file.name)
  }

  const handleUploadComplete = (result: any) => {
    console.log('Upload completo:', result)
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50">
      {/* Navigation */}
      <nav className="bg-white/80 backdrop-blur-md shadow-sm sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            {/* Logo */}
            <div className="flex-shrink-0">
              <Link href="/" className="text-xl font-bold text-gray-900">
                <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-600 to-purple-600">
                  Democratiza AI
                </span>
              </Link>
            </div>

            {/* Desktop Navigation */}
            <div className="hidden md:block">
              <div className="ml-10 flex items-baseline space-x-8">
                <Link href="/dashboard" className="text-gray-900 hover:text-blue-600 px-3 py-2 text-sm font-medium transition-colors">
                  Análise de Contratos
                </Link>
                <Link href="/chat" className="text-gray-900 hover:text-blue-600 px-3 py-2 text-sm font-medium transition-colors">
                  Chat com IA
                </Link>
                <Link href="/contracts" className="text-gray-900 hover:text-blue-600 px-3 py-2 text-sm font-medium transition-colors">
                  Meus Contratos
                </Link>
                <Link href="/login" className="text-gray-900 hover:text-blue-600 px-3 py-2 text-sm font-medium transition-colors">
                  Entrar
                </Link>
                <Link 
                  href="/register" 
                  className="bg-gradient-to-r from-blue-600 to-purple-600 text-white px-4 py-2 rounded-lg text-sm font-medium hover:shadow-lg transition-all duration-200"
                >
                  Cadastrar
                </Link>
              </div>
            </div>

            {/* Mobile menu button */}
            <div className="md:hidden">
              <button
                onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
                className="inline-flex items-center justify-center p-2 rounded-md text-gray-400 hover:text-gray-500 hover:bg-gray-100"
              >
                <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
                </svg>
              </button>
            </div>
          </div>

          {/* Mobile Navigation */}
          {mobileMenuOpen && (
            <div className="md:hidden">
              <div className="px-2 pt-2 pb-3 space-y-1 sm:px-3 bg-white rounded-lg shadow-lg mt-2">
                <Link href="/dashboard" className="text-gray-900 hover:text-blue-600 block px-3 py-2 text-base font-medium">
                  Análise de Contratos
                </Link>
                <Link href="/chat" className="text-gray-900 hover:text-blue-600 block px-3 py-2 text-base font-medium">
                  Chat com IA
                </Link>
                <Link href="/contracts" className="text-gray-900 hover:text-blue-600 block px-3 py-2 text-base font-medium">
                  Meus Contratos
                </Link>
                <Link href="/login" className="text-gray-900 hover:text-blue-600 block px-3 py-2 text-base font-medium">
                  Entrar
                </Link>
                <Link 
                  href="/register" 
                  className="bg-gradient-to-r from-blue-600 to-purple-600 text-white block px-3 py-2 rounded-lg text-base font-medium text-center"
                >
                  Cadastrar
                </Link>
              </div>
            </div>
          )}
        </div>
      </nav>

      {/* Hero Section - Mobile First */}
      <section className="relative px-4 sm:px-6 lg:px-8 py-12 sm:py-16 lg:py-24">
        <div className="mx-auto max-w-4xl">
          <div className="text-center">
            {/* Headline principal - Mobile First */}
            <h1 className="text-3xl sm:text-4xl md:text-5xl lg:text-6xl font-bold tracking-tight text-gray-900">
              Nunca Assine Um
              <span className="block text-transparent bg-clip-text bg-gradient-to-r from-blue-600 to-purple-600 mt-2">
                Contrato Arriscado
              </span>
            </h1>
            
            {/* Subtítulo - Mobile First */}
            <p className="mt-6 text-lg sm:text-xl lg:text-2xl leading-relaxed text-gray-600 max-w-3xl mx-auto">
              Análise de contratos com IA que protege brasileiros de acordos arriscados. 
              <span className="block mt-2 font-semibold text-blue-600">
                Democratizando a compreensão jurídica no Brasil.
              </span>
            </p>

            {/* Proposta de valor real */}
            <div className="mt-8 grid grid-cols-1 sm:grid-cols-3 gap-4 max-w-2xl mx-auto">
              <div className="flex flex-col items-center p-4 bg-white/60 rounded-lg backdrop-blur-sm">
                <svg className="w-8 h-8 text-green-500 mb-2" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                </svg>
                <span className="text-sm font-medium text-gray-700 text-center">Análise Instantânea</span>
              </div>
              <div className="flex flex-col items-center p-4 bg-white/60 rounded-lg backdrop-blur-sm">
                <svg className="w-8 h-8 text-blue-500 mb-2" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M3 4a1 1 0 011-1h12a1 1 0 011 1v2a1 1 0 01-1 1H4a1 1 0 01-1-1V4zM3 10a1 1 0 011-1h6a1 1 0 011 1v6a1 1 0 01-1 1H4a1 1 0 01-1-1v-6zM14 9a1 1 0 00-1 1v6a1 1 0 001 1h2a1 1 0 001-1v-6a1 1 0 00-1-1h-2z" clipRule="evenodd" />
                </svg>
                <span className="text-sm font-medium text-gray-700 text-center">Upload Seguro</span>
              </div>
              <div className="flex flex-col items-center p-4 bg-white/60 rounded-lg backdrop-blur-sm">
                <svg className="w-8 h-8 text-purple-500 mb-2" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clipRule="evenodd" />
                </svg>
                <span className="text-sm font-medium text-gray-700 text-center">Linguagem Clara</span>
              </div>
            </div>

            {/* CTAs - Mobile First */}
            <div className="mt-10 flex flex-col sm:flex-row items-center justify-center gap-4">
              <Link
                href="/dashboard"
                className="w-full sm:w-auto rounded-xl bg-gradient-to-r from-blue-600 to-purple-600 px-8 py-4 text-lg font-semibold text-white shadow-lg hover:shadow-xl transition-all duration-200 hover:scale-105 text-center"
              >
                Analise Seu Contrato Grátis
              </Link>
              <Link 
                href="/chat" 
                className="w-full sm:w-auto rounded-xl border-2 border-gray-300 px-8 py-4 text-lg font-semibold text-gray-700 hover:border-blue-600 hover:text-blue-600 transition-colors text-center"
              >
                Fale com a IA
              </Link>
            </div>

            {/* Explicação do problema que resolvemos */}
            <div className="mt-12 p-6 bg-yellow-50 rounded-xl border border-yellow-200">
              <h3 className="text-lg font-semibold text-yellow-800 mb-2">
                🚨 Você sabia que 73% dos brasileiros já assinaram contratos sem entender completamente?
              </h3>
              <p className="text-yellow-700">
                Cláusulas abusivas, multas escondidas e armadilhas jurídicas podem custar caro. 
                Nossa IA identifica esses riscos em segundos, usando linguagem simples que qualquer pessoa entende.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Como Funciona - Mobile First */}
      <section className="relative px-4 sm:px-6 lg:px-8 py-12 sm:py-16 bg-white">
        <div className="mx-auto max-w-4xl">
          <div className="text-center mb-8 sm:mb-12">
            <h2 className="text-2xl sm:text-3xl lg:text-4xl font-bold text-gray-900">
              Como Funciona Nossa Análise
            </h2>
            <p className="mt-4 text-base sm:text-lg text-gray-600">
              Transformamos jargão jurídico em insights claros que qualquer pessoa entende.
            </p>
          </div>

          {/* Processo Visual - Mobile First */}
          <div className="bg-gray-50 rounded-2xl p-4 sm:p-6 lg:p-8">
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 lg:gap-8 items-center">
              {/* Upload Area */}
              <div>
                <div className="mb-4">
                  <span className="inline-flex items-center rounded-full bg-blue-100 px-3 py-1 text-sm font-medium text-blue-800">
                    01 Envie seu contrato
                  </span>
                </div>
                <SimpleUploadManager
                  onFileSelect={handleFileSelect}
                  onUploadComplete={handleUploadComplete}
                  className="max-w-none"
                />
                <div className="mt-4 grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-1 xl:grid-cols-2 gap-3 text-sm text-gray-500">
                  <div className="flex items-center gap-2">
                    <svg className="w-4 h-4 text-green-500" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                    </svg>
                    <span>PDF, DOCX, TXT</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <svg className="w-4 h-4 text-green-500" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                    </svg>
                    <span>Upload criptografado</span>
                  </div>
                </div>
              </div>

              {/* Preview do resultado - Mobile Optimized */}
              <div className="bg-white rounded-xl p-4 sm:p-6 shadow-lg">
                <div className="mb-4">
                  <span className="inline-flex items-center rounded-full bg-green-100 px-3 py-1 text-sm font-medium text-green-800">
                    02 IA analisa cada cláusula
                  </span>
                </div>
                
                <div className="space-y-4">
                  <div className="border-l-4 border-red-500 pl-4">
                    <div className="flex items-center gap-2 mb-2">
                      <span className="w-2 h-2 bg-red-500 rounded-full"></span>
                      <span className="font-semibold text-red-700 text-sm">🚨 Alto Risco</span>
                    </div>
                    <p className="text-sm text-gray-600">
                      Cláusula de rescisão unilateral sem prazo adequado
                    </p>
                  </div>
                  
                  <div className="border-l-4 border-yellow-500 pl-4">
                    <div className="flex items-center gap-2 mb-2">
                      <span className="w-2 h-2 bg-yellow-500 rounded-full"></span>
                      <span className="font-semibold text-yellow-700 text-sm">⚠️ Atenção</span>
                    </div>
                    <p className="text-sm text-gray-600">
                      Multa por atraso superior ao permitido por lei
                    </p>
                  </div>
                  
                  <div className="border-l-4 border-green-500 pl-4">
                    <div className="flex items-center gap-2 mb-2">
                      <span className="w-2 h-2 bg-green-500 rounded-full"></span>
                      <span className="font-semibold text-green-700 text-sm">✅ Adequado</span>
                    </div>
                    <p className="text-sm text-gray-600">
                      Termos de pagamento claros e justos
                    </p>
                  </div>
                </div>
                
                <div className="mt-6 pt-4 border-t border-gray-200">
                  <span className="inline-flex items-center rounded-full bg-purple-100 px-3 py-1 text-sm font-medium text-purple-800">
                    03 Receba orientações práticas
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Por que Escolher Democratiza AI - Mobile First */}
      <section className="px-4 sm:px-6 lg:px-8 py-12 sm:py-16 bg-gray-50">
        <div className="mx-auto max-w-6xl">
          <div className="text-center mb-8 sm:mb-12">
            <h2 className="text-2xl sm:text-3xl lg:text-4xl font-bold text-gray-900">
              Por que Democratiza AI?
            </h2>
            <p className="mt-4 text-base sm:text-lg text-gray-600 max-w-3xl mx-auto">
              Criamos uma plataforma que coloca o poder da análise jurídica nas mãos de todo brasileiro, 
              independente do conhecimento legal.
            </p>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 sm:gap-8">
            <div className="text-center bg-white p-6 rounded-xl shadow-sm">
              <div className="w-12 h-12 sm:w-16 sm:h-16 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <svg className="w-6 h-6 sm:w-8 sm:h-8 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <h3 className="text-base sm:text-lg font-semibold text-gray-900 mb-2">IA Especializada</h3>
              <p className="text-sm sm:text-base text-gray-600">
                Treinada especificamente em contratos brasileiros, nossa IA entende as nuances da legislação nacional
              </p>
            </div>

            <div className="text-center bg-white p-6 rounded-xl shadow-sm">
              <div className="w-12 h-12 sm:w-16 sm:h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <svg className="w-6 h-6 sm:w-8 sm:h-8 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                </svg>
              </div>
              <h3 className="text-base sm:text-lg font-semibold text-gray-900 mb-2">Análise Instantânea</h3>
              <p className="text-sm sm:text-base text-gray-600">
                Receba insights detalhados em segundos, não em dias ou semanas de análise tradicional
              </p>
            </div>

            <div className="text-center bg-white p-6 rounded-xl shadow-sm">
              <div className="w-12 h-12 sm:w-16 sm:h-16 bg-red-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <svg className="w-6 h-6 sm:w-8 sm:h-8 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L4.082 15.5c-.77.833.192 2.5 1.732 2.5z" />
                </svg>
              </div>
              <h3 className="text-base sm:text-lg font-semibold text-gray-900 mb-2">Detecção de Armadilhas</h3>
              <p className="text-sm sm:text-base text-gray-600">
                Identifica cláusulas abusivas, multas excessivas e termos prejudiciais automaticamente
              </p>
            </div>

            <div className="text-center bg-white p-6 rounded-xl shadow-sm">
              <div className="w-12 h-12 sm:w-16 sm:h-16 bg-purple-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <svg className="w-6 h-6 sm:w-8 sm:h-8 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
                </svg>
              </div>
              <h3 className="text-base sm:text-lg font-semibold text-gray-900 mb-2">Linguagem Simples</h3>
              <p className="text-sm sm:text-base text-gray-600">
                Traduzimos complexidade jurídica em orientações práticas que qualquer pessoa entende
              </p>
            </div>
          </div>

          {/* Problemas que resolvemos */}
          <div className="mt-12 sm:mt-16">
            <div className="text-center mb-8">
              <h3 className="text-xl sm:text-2xl font-bold text-gray-900">
                Protegemos você de contratos arriscados
              </h3>
            </div>
            
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-6">
              <div className="bg-red-50 border border-red-200 p-4 rounded-lg">
                <div className="flex items-start gap-3">
                  <span className="text-red-500 text-lg">❌</span>
                  <div>
                    <h4 className="font-semibold text-red-800 text-sm">Cláusulas Abusivas</h4>
                    <p className="text-red-700 text-sm mt-1">Multas excessivas, rescisão unilateral, transferência inadequada de responsabilidades</p>
                  </div>
                </div>
              </div>
              
              <div className="bg-red-50 border border-red-200 p-4 rounded-lg">
                <div className="flex items-start gap-3">
                  <span className="text-red-500 text-lg">❌</span>
                  <div>
                    <h4 className="font-semibold text-red-800 text-sm">Taxas Ocultas</h4>
                    <p className="text-red-700 text-sm mt-1">Custos escondidos, juros abusivos, correções monetárias inadequadas</p>
                  </div>
                </div>
              </div>
              
              <div className="bg-red-50 border border-red-200 p-4 rounded-lg">
                <div className="flex items-start gap-3">
                  <span className="text-red-500 text-lg">❌</span>
                  <div>
                    <h4 className="font-semibold text-red-800 text-sm">Prazos Prejudiciais</h4>
                    <p className="text-red-700 text-sm mt-1">Avisos insuficientes, renovações automáticas, bloqueios de rescisão</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Final - Mobile First */}
      <section className="px-4 sm:px-6 lg:px-8 py-12 sm:py-16 bg-white">
        <div className="mx-auto max-w-4xl text-center">
          <h2 className="text-2xl sm:text-3xl lg:text-4xl font-bold text-gray-900 mb-4 sm:mb-6">
            Nunca mais assine um contrato sem saber o que está fazendo
          </h2>
          <p className="text-base sm:text-lg text-gray-600 mb-6 sm:mb-8 max-w-2xl mx-auto">
            Proteja-se de cláusulas abusivas e armadilhas contratuais. 
            Nossa IA analisa cada detalhe para que você tome decisões informadas.
          </p>
          
          <div className="flex flex-col sm:flex-row gap-4 justify-center mb-8">
            <Link
              href="/dashboard"
              className="w-full sm:w-auto rounded-xl bg-gradient-to-r from-blue-600 to-purple-600 px-6 sm:px-8 py-3 sm:py-4 text-base sm:text-lg font-semibold text-white shadow-lg hover:shadow-xl transition-all duration-200 hover:scale-105 text-center"
            >
              Analisar Meu Contrato Grátis
            </Link>
            <Link
              href="/chat"
              className="w-full sm:w-auto rounded-xl border-2 border-blue-600 px-6 sm:px-8 py-3 sm:py-4 text-base sm:text-lg font-semibold text-blue-600 hover:bg-blue-50 transition-colors text-center"
            >
              Conversar com a IA
            </Link>
          </div>

          {/* Garantias e benefícios */}
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 sm:gap-6 text-sm sm:text-base">
            <div className="flex flex-col sm:flex-row lg:flex-col items-center gap-2 text-gray-600">
              <svg className="w-5 h-5 text-green-500 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
              </svg>
              <span className="text-center sm:text-left lg:text-center">100% Gratuito para começar</span>
            </div>
            <div className="flex flex-col sm:flex-row lg:flex-col items-center gap-2 text-gray-600">
              <svg className="w-5 h-5 text-green-500 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
              </svg>
              <span className="text-center sm:text-left lg:text-center">Análise em segundos</span>
            </div>
            <div className="flex flex-col sm:flex-row lg:flex-col items-center gap-2 text-gray-600">
              <svg className="w-5 h-5 text-green-500 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
              </svg>
              <span className="text-center sm:text-left lg:text-center">Dados 100% seguros</span>
            </div>
            <div className="flex flex-col sm:flex-row lg:flex-col items-center gap-2 text-gray-600">
              <svg className="w-5 h-5 text-green-500 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
              </svg>
              <span className="text-center sm:text-left lg:text-center">Sem conhecimento jurídico necessário</span>
            </div>
          </div>

          {/* Call to action adicional */}
          <div className="mt-8 sm:mt-12 p-4 sm:p-6 bg-blue-50 rounded-xl border border-blue-200">
            <h3 className="text-lg sm:text-xl font-semibold text-blue-800 mb-2">
              💡 Comece agora mesmo
            </h3>
            <p className="text-blue-700 text-sm sm:text-base">
              Faça upload do seu contrato e receba uma análise detalhada em segundos. 
              Identifique riscos antes que se tornem problemas.
            </p>
          </div>
        </div>
      </section>
    </div>
  )
}