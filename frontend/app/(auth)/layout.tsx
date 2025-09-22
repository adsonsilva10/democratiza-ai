export default function AuthLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8 w-full overflow-x-hidden">
      <div className="max-w-md w-full space-y-8 min-w-0">
        <div className="text-center">
          <h1 className="text-2xl sm:text-3xl font-bold text-gray-900 mb-2 truncate">
            Contrato Seguro
          </h1>
          <p className="text-gray-600 text-sm sm:text-base px-2">
            Democratizando a compreensão jurídica no Brasil
          </p>
        </div>
        
        <div className="bg-white rounded-lg shadow-lg p-4 sm:p-8 w-full">
          {children}
        </div>
        
        <div className="text-center px-2">
          <p className="text-xs sm:text-sm text-gray-500">
            🔒 Seus dados são protegidos com segurança total
          </p>
        </div>
      </div>
    </div>
  )
}
