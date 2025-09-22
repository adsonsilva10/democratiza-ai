'use client'

import SimpleUploadManager from '@/components/features/SimpleUploadManager'
import Link from 'next/link'

export default function HomePage() {
  const handleFileSelect = (file: File) => {
    console.log('Arquivo selecionado:', file.name)
  }

  const handleUploadComplete = (result: any) => {
    console.log('Upload completo:', result)
    // Aqui você pode redirecionar para página de resultados ou mostrar o chat
  }
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      {/* Header */}
      <header className="container mx-auto px-4 py-6">
        <div className="flex justify-between items-center">
          <div className="text-xl font-bold text-gray-900">
            Contrato Seguro
          </div>
          <div className="space-x-4">
            <Link 
              href="/login"
              className="text-blue-600 hover:text-blue-700 font-medium"
            >
              Entrar
            </Link>
            <Link 
              href="/register"
              className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg font-medium transition-colors"
            >
              Criar conta
            </Link>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <div className="container mx-auto px-4 py-16">
        <div className="text-center mb-16">
          <h1 className="text-5xl font-bold text-gray-900 mb-6">
            Contrato Seguro
          </h1>
          <p className="text-xl text-gray-600 mb-8 max-w-3xl mx-auto">
            Democratizando a compreensão jurídica no Brasil. Analise seus contratos 
            com IA especializada e tome decisões mais seguras.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <button className="bg-blue-600 hover:bg-blue-700 text-white px-8 py-3 rounded-lg font-semibold transition-colors">
              📄 Analisar Contrato
            </button>
            <Link 
              href="/chat"
              className="border border-blue-600 text-blue-600 hover:bg-blue-50 px-8 py-3 rounded-lg font-semibold transition-colors text-center"
            >
              � Chat com IA
            </Link>
          </div>
        </div>

        {/* Features Grid */}
        <div className="grid md:grid-cols-3 gap-8 mb-16">
          <div className="bg-white p-6 rounded-lg shadow-md">
            <div className="text-3xl mb-4">🤖</div>
            <h3 className="text-xl font-semibold mb-3">Análise por IA</h3>
            <p className="text-gray-600">
              Nossa IA especializada identifica cláusulas abusivas e riscos 
              em contratos de locação, telecomunicações e financeiros.
            </p>
          </div>
          
          <div className="bg-white p-6 rounded-lg shadow-md">
            <div className="text-3xl mb-4">⚡</div>
            <h3 className="text-xl font-semibold mb-3">Análise Rápida</h3>
            <p className="text-gray-600">
              Receba um relatório completo em minutos, com classificação 
              de riscos e recomendações personalizadas.
            </p>
          </div>
          
          <div className="bg-white p-6 rounded-lg shadow-md">
            <div className="text-3xl mb-4">🔒</div>
            <h3 className="text-xl font-semibold mb-3">Seguro e Privado</h3>
            <p className="text-gray-600">
              Seus documentos são processados com máxima segurança e 
              confidencialidade, seguindo a LGPD.
            </p>
          </div>
        </div>

        {/* Upload Section */}
        <div className="bg-white rounded-lg shadow-lg p-8 max-w-2xl mx-auto">
          <h2 className="text-2xl font-bold text-center mb-6">
            📎 Envie seu contrato para análise
          </h2>
          
          <SimpleUploadManager 
            onFileSelect={handleFileSelect}
            onUploadComplete={handleUploadComplete}
          />
        </div>

        {/* Stats Section */}
        <div className="mt-16 grid grid-cols-2 md:grid-cols-4 gap-8 text-center">
          <div>
            <div className="text-3xl font-bold text-blue-600">1,000+</div>
            <div className="text-gray-600">Contratos Analisados</div>
          </div>
          <div>
            <div className="text-3xl font-bold text-blue-600">95%</div>
            <div className="text-gray-600">Precisão da IA</div>
          </div>
          <div>
            <div className="text-3xl font-bold text-blue-600">3min</div>
            <div className="text-gray-600">Tempo Médio</div>
          </div>
          <div>
            <div className="text-3xl font-bold text-blue-600">24/7</div>
            <div className="text-gray-600">Disponibilidade</div>
          </div>
        </div>
      </div>
    </div>
  )
}
