export default function DashboardTestPage() {
  return (
    <div className="p-8 bg-white min-h-screen">
      <div className="max-w-4xl mx-auto">
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">
            🎉 Dashboard Funcionando!
          </h1>
          <p className="text-gray-600 text-lg">
            Se você está vendo esta mensagem, a rota /dashboard está funcionando corretamente.
          </p>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <div className="bg-blue-50 p-6 rounded-xl border border-blue-200">
            <div className="text-3xl mb-3">📊</div>
            <h3 className="font-bold text-blue-900">Análises Realizadas</h3>
            <div className="text-2xl font-bold text-blue-600 mt-2">127</div>
          </div>
          
          <div className="bg-green-50 p-6 rounded-xl border border-green-200">
            <div className="text-3xl mb-3">✅</div>
            <h3 className="font-bold text-green-900">Contratos Seguros</h3>
            <div className="text-2xl font-bold text-green-600 mt-2">89</div>
          </div>
          
          <div className="bg-red-50 p-6 rounded-xl border border-red-200">
            <div className="text-3xl mb-3">⚠️</div>
            <h3 className="font-bold text-red-900">Riscos Identificados</h3>
            <div className="text-2xl font-bold text-red-600 mt-2">38</div>
          </div>
        </div>
        
        <div className="bg-gray-50 p-6 rounded-xl">
          <h2 className="text-2xl font-bold text-gray-900 mb-4">
            🚀 Próximos Passos
          </h2>
          <div className="space-y-3">
            <p className="flex items-center gap-3">
              <span className="w-2 h-2 bg-blue-500 rounded-full"></span>
              A rota está funcionando perfeitamente
            </p>
            <p className="flex items-center gap-3">
              <span className="w-2 h-2 bg-green-500 rounded-full"></span>
              Layout do dashboard carregado com sucesso
            </p>
            <p className="flex items-center gap-3">
              <span className="w-2 h-2 bg-purple-500 rounded-full"></span>
              Pronto para implementar o dashboard completo
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}