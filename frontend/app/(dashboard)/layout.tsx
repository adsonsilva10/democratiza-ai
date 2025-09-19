import Link from 'next/link'

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <div className="min-h-screen bg-gray-50">
      {/* Sidebar */}
      <div className="fixed inset-y-0 left-0 z-50 w-64 bg-white shadow-lg">
        <div className="flex flex-col h-full">
          {/* Logo */}
          <div className="flex items-center h-16 px-6 border-b">
            <Link href="/" className="text-xl font-bold text-gray-900">
              Contrato Seguro
            </Link>
          </div>
          
          {/* Navigation */}
          <nav className="flex-1 px-4 py-6 space-y-2">
            <Link 
              href="/dashboard"
              className="flex items-center px-3 py-2 text-gray-700 rounded-lg hover:bg-gray-100"
            >
              📊 Dashboard
            </Link>
            <Link 
              href="/dashboard/contracts"
              className="flex items-center px-3 py-2 text-gray-700 rounded-lg hover:bg-gray-100"
            >
              📄 Meus Contratos
            </Link>
            <Link 
              href="/dashboard/upload"
              className="flex items-center px-3 py-2 text-gray-700 rounded-lg hover:bg-gray-100"
            >
              📤 Novo Upload
            </Link>
            <Link 
              href="/dashboard/chat"
              className="flex items-center px-3 py-2 text-gray-700 rounded-lg hover:bg-gray-100"
            >
              💬 Chat IA
            </Link>
            <Link 
              href="/dashboard/settings"
              className="flex items-center px-3 py-2 text-gray-700 rounded-lg hover:bg-gray-100"
            >
              ⚙️ Configurações
            </Link>
          </nav>
          
          {/* User Menu */}
          <div className="p-4 border-t">
            <div className="flex items-center space-x-3">
              <div className="w-8 h-8 bg-blue-600 rounded-full flex items-center justify-center">
                <span className="text-white text-sm font-medium">U</span>
              </div>
              <div className="flex-1">
                <p className="text-sm font-medium text-gray-900">Usuário</p>
                <p className="text-xs text-gray-500">usuario@email.com</p>
              </div>
            </div>
            <button className="w-full mt-3 px-3 py-2 text-sm text-gray-600 hover:text-gray-900 text-left">
              🚪 Sair
            </button>
          </div>
        </div>
      </div>
      
      {/* Main Content */}
      <div className="pl-64">
        {/* Top Header */}
        <header className="bg-white shadow-sm border-b h-16 flex items-center justify-between px-6">
          <h1 className="text-2xl font-semibold text-gray-900">Dashboard</h1>
          <div className="flex items-center space-x-4">
            <button className="p-2 text-gray-400 hover:text-gray-600">
              🔔
            </button>
            <button className="p-2 text-gray-400 hover:text-gray-600">
              ❓
            </button>
          </div>
        </header>
        
        {/* Page Content */}
        <main className="p-6">
          {children}
        </main>
      </div>
    </div>
  )
}