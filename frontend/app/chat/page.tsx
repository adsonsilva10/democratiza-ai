import SimpleChat from '@/components/features/SimpleChat'
import Link from 'next/link'

export default function ChatPage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      {/* Header */}
      <header className="container mx-auto px-4 py-6">
        <div className="flex justify-between items-center">
          <Link href="/" className="text-xl font-bold text-gray-900">
            ← Contrato Seguro
          </Link>
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

      {/* Chat Section */}
      <div className="container mx-auto px-4 py-8">
        <div className="max-w-4xl mx-auto">
          <div className="text-center mb-8">
            <h1 className="text-3xl font-bold text-gray-900 mb-4">
              Chat com Agente IA
            </h1>
            <p className="text-gray-600 mb-6">
              Converse com nossos agentes especializados para esclarecer dúvidas sobre contratos
            </p>
          </div>

          <div className="grid md:grid-cols-2 gap-8">
            {/* Chat de Locação */}
            <div>
              <h3 className="text-lg font-semibold mb-4">🏠 Agente de Locação</h3>
              <SimpleChat agentType="rental" />
            </div>

            {/* Chat de Telecomunicações */}
            <div>
              <h3 className="text-lg font-semibold mb-4">📱 Agente de Telecomunicações</h3>
              <SimpleChat agentType="telecom" />
            </div>
          </div>

          <div className="grid md:grid-cols-2 gap-8 mt-8">
            {/* Chat Financeiro */}
            <div>
              <h3 className="text-lg font-semibold mb-4">💰 Agente Financeiro</h3>
              <SimpleChat agentType="financial" />
            </div>

            {/* Chat Classificador */}
            <div>
              <h3 className="text-lg font-semibold mb-4">🤖 Agente Classificador</h3>
              <SimpleChat agentType="classifier" />
            </div>
          </div>

          {/* Informações */}
          <div className="mt-12 bg-white rounded-lg shadow-lg p-8">
            <h2 className="text-2xl font-bold text-center mb-6">
              Como Funciona
            </h2>
            
            <div className="grid md:grid-cols-4 gap-6">
              <div className="text-center">
                <div className="text-3xl mb-3">📄</div>
                <h3 className="font-semibold mb-2">1. Upload</h3>
                <p className="text-sm text-gray-600">Envie seu contrato em PDF, DOC ou DOCX</p>
              </div>
              
              <div className="text-center">
                <div className="text-3xl mb-3">🤖</div>
                <h3 className="font-semibold mb-2">2. Análise IA</h3>
                <p className="text-sm text-gray-600">Nossa IA analisa e classifica o contrato</p>
              </div>
              
              <div className="text-center">
                <div className="text-3xl mb-3">💬</div>
                <h3 className="font-semibold mb-2">3. Chat</h3>
                <p className="text-sm text-gray-600">Converse com o agente especializado</p>
              </div>
              
              <div className="text-center">
                <div className="text-3xl mb-3">📊</div>
                <h3 className="font-semibold mb-2">4. Relatório</h3>
                <p className="text-sm text-gray-600">Receba um relatório detalhado</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}