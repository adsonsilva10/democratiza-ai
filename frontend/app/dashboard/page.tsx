'use client'

export default function DashboardPage() {
  // Simulando dados do usuário - em produção viria de uma API
  const totalContratos = 0 // Mude para 42 para testar com contratos
  const hasAnalyzedContracts = totalContratos > 0

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold text-gray-900 mb-6">Dashboard</h1>
      
      {/* Se não analisou nenhum contrato, mostra o botão primeiro */}
      {!hasAnalyzedContracts && (
        <div className="mb-8">
          <div className="bg-gradient-to-r from-blue-600 to-purple-600 rounded-lg p-8 text-white text-center">
            <h2 className="text-2xl font-bold mb-3">Bem-vindo ao Democratiza AI!</h2>
            <p className="text-blue-100 mb-6 text-lg">Comece analisando seu primeiro contrato e descubra os riscos ocultos</p>
            <button className="bg-white text-blue-600 px-8 py-4 rounded-lg font-semibold hover:bg-gray-50 transition-colors text-lg">
              🚀 Analisar Meu Primeiro Contrato
            </button>
          </div>
        </div>
      )}

      {/* Só mostra estatísticas se já analisou contratos */}
      {hasAnalyzedContracts && (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <div className="bg-white p-6 rounded-lg shadow">
            <h3 className="text-sm font-medium text-gray-500">Total de Contratos</h3>
            <p className="text-2xl font-bold text-gray-900">{totalContratos}</p>
          </div>
          
          <div className="bg-white p-6 rounded-lg shadow">
            <h3 className="text-sm font-medium text-gray-500">Análises Concluídas</h3>
            <p className="text-2xl font-bold text-gray-900">38</p>
          </div>
          
          <div className="bg-white p-6 rounded-lg shadow">
            <h3 className="text-sm font-medium text-gray-500">Riscos Identificados</h3>
            <p className="text-2xl font-bold text-red-600">27</p>
          </div>
        </div>
      )}

      {/* Se já analisou contratos, mostra o botão menor depois das estatísticas */}
      {hasAnalyzedContracts && (
        <div className="mb-8">
          <div className="bg-gradient-to-r from-blue-600 to-purple-600 rounded-lg p-6 text-white">
            <h2 className="text-xl font-bold mb-2">Pronto para analisar outro contrato?</h2>
            <p className="text-blue-100 mb-4">Faça upload do seu documento e receba uma análise completa em minutos</p>
            <button className="bg-white text-blue-600 px-6 py-3 rounded-lg font-semibold hover:bg-gray-50 transition-colors">
              📄 Analisar Contrato
            </button>
          </div>
        </div>
      )}

      {/* Seção de contratos recentes */}
      <div className="bg-white rounded-lg shadow">
        <div className="p-6 border-b">
          <h2 className="text-lg font-medium text-gray-900">
            {hasAnalyzedContracts ? 'Contratos Recentes' : 'Seus Contratos Aparecerão Aqui'}
          </h2>
        </div>
        <div className="p-6">
          {hasAnalyzedContracts ? (
            <div className="space-y-4">
              <div className="flex items-center justify-between p-4 border rounded-lg">
                <div>
                  <h3 className="font-medium">Contrato de Locação - Apto 101</h3>
                  <p className="text-sm text-gray-500">Analisado em 20/09/2025</p>
                </div>
                <span className="px-3 py-1 bg-red-100 text-red-800 rounded-full text-sm">Alto Risco</span>
              </div>
              <div className="flex items-center justify-between p-4 border rounded-lg">
                <div>
                  <h3 className="font-medium">Contrato de Internet - Fibra</h3>
                  <p className="text-sm text-gray-500">Analisado em 18/09/2025</p>
                </div>
                <span className="px-3 py-1 bg-yellow-100 text-yellow-800 rounded-full text-sm">Médio Risco</span>
              </div>
            </div>
          ) : (
            <div className="text-center py-8">
              <div className="text-gray-400 mb-4">
                <svg className="w-16 h-16 mx-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
              </div>
              <p className="text-gray-500 mb-2">Nenhum contrato analisado ainda</p>
              <p className="text-sm text-gray-400">Seus contratos analisados aparecerão aqui com seus respectivos níveis de risco</p>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}