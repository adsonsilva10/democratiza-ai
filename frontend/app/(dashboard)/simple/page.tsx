export default function DashboardSimple() {
  return (
    <div className="p-8">
      <h1 className="text-3xl font-bold text-gray-900 mb-8">
        🏠 Dashboard - Contrato Seguro
      </h1>
      
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
        <div className="bg-white p-6 rounded-xl shadow-lg">
          <h3 className="text-sm font-medium text-gray-500 uppercase tracking-wide mb-2">
            Contratos Analisados
          </h3>
          <div className="text-3xl font-bold text-blue-600">24</div>
        </div>
        
        <div className="bg-white p-6 rounded-xl shadow-lg">
          <h3 className="text-sm font-medium text-gray-500 uppercase tracking-wide mb-2">
            Alto Risco
          </h3>
          <div className="text-3xl font-bold text-red-600">8</div>
        </div>
        
        <div className="bg-white p-6 rounded-xl shadow-lg">
          <h3 className="text-sm font-medium text-gray-500 uppercase tracking-wide mb-2">
            Médio Risco
          </h3>
          <div className="text-3xl font-bold text-yellow-600">12</div>
        </div>
        
        <div className="bg-white p-6 rounded-xl shadow-lg">
          <h3 className="text-sm font-medium text-gray-500 uppercase tracking-wide mb-2">
            Baixo Risco
          </h3>
          <div className="text-3xl font-bold text-green-600">4</div>
        </div>
      </div>
      
      <div className="bg-white rounded-xl shadow-lg p-8">
        <h2 className="text-2xl font-bold text-gray-900 mb-6">
          Contratos Recentes
        </h2>
        <div className="space-y-4">
          <div className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
            <div className="flex items-center gap-3">
              <span className="text-2xl">🏠</span>
              <div>
                <h3 className="font-semibold">Contrato de Locação</h3>
                <p className="text-sm text-gray-600">Analisado hoje</p>
              </div>
            </div>
            <span className="px-3 py-1 bg-red-100 text-red-800 rounded-full text-sm font-medium">
              Alto Risco
            </span>
          </div>
          
          <div className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
            <div className="flex items-center gap-3">
              <span className="text-2xl">📱</span>
              <div>
                <h3 className="font-semibold">Plano de Celular</h3>
                <p className="text-sm text-gray-600">Analisado ontem</p>
              </div>
            </div>
            <span className="px-3 py-1 bg-yellow-100 text-yellow-800 rounded-full text-sm font-medium">
              Médio Risco
            </span>
          </div>
        </div>
      </div>
    </div>
  )
}