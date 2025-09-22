import SimpleChat from '@/components/features/SimpleChat'
import Link from 'next/link'

export default function ChatPage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 w-full overflow-x-hidden">
      {/* Header */}
      <header className="container mx-auto px-4 py-6 w-full">
        <div className="flex flex-col sm:flex-row sm:justify-between sm:items-center gap-4 w-full">
          <Link href="/" className="text-lg sm:text-xl font-bold text-gray-900 truncate">
            ← Contrato Seguro
          </Link>
          <div className="flex gap-4 justify-start sm:justify-end">
            <Link 
              href="/login"
              className="text-blue-600 hover:text-blue-700 font-medium"
            >
              Entrar
            </Link>
            <Link 
              href="/register"
              className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg font-medium transition-colors whitespace-nowrap"
            >
              Criar conta
            </Link>
          </div>
        </div>
      </header>

      {/* Chat Section */}
      <div className="container mx-auto px-4 py-8 w-full">
        <div className="max-w-4xl mx-auto w-full">
          <div className="text-center mb-8">
            <h1 className="text-2xl sm:text-3xl font-bold text-gray-900 mb-4">
              Chat com Agente IA
            </h1>
            <p className="text-gray-600 mb-6 text-sm sm:text-base px-2">
              Converse com nossos agentes especializados para esclarecer dúvidas sobre contratos
            </p>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 sm:gap-8 w-full">
            {/* Chat de Locação */}
            <div className="w-full">
              <h3 className="text-lg font-semibold mb-4 truncate">🏠 Agente de Locação</h3>
              <SimpleChat agentType="rental" className="w-full" />
            </div>

            {/* Chat de Telecomunicações */}
            <div className="w-full">
              <h3 className="text-lg font-semibold mb-4 truncate">📱 Agente de Telecomunicações</h3>
              <SimpleChat agentType="telecom" className="w-full" />
            </div>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 sm:gap-8 mt-6 sm:mt-8 w-full">
            {/* Chat Financeiro */}
            <div className="w-full">
              <h3 className="text-lg font-semibold mb-4 truncate">💰 Agente Financeiro</h3>
              <SimpleChat agentType="financial" className="w-full" />
            </div>

            {/* Chat Classificador */}
            <div className="w-full">
              <h3 className="text-lg font-semibold mb-4 truncate">🤖 Agente Classificador</h3>
              <SimpleChat agentType="classifier" className="w-full" />
            </div>
          </div>

          {/* Informações */}
          <div className="mt-8 sm:mt-12 bg-white rounded-lg shadow-lg p-4 sm:p-8 w-full">
            <h2 className="text-xl sm:text-2xl font-bold text-center mb-6">
              Como Funciona
            </h2>
            
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 w-full">
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