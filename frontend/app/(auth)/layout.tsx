import Link from 'next/link'

export default function AuthLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 via-white to-blue-50 flex items-center justify-center py-8 px-4">
      <div className="max-w-md w-full space-y-6">
        {/* Logo/Brand */}
        <div className="text-center">
          <Link href="/" className="inline-block">
            <div className="bg-gradient-to-r from-red-500 to-orange-500 bg-clip-text text-transparent text-3xl font-bold mb-2">
              Democratiza AI
            </div>
          </Link>
          <p className="text-gray-600 text-sm">
            Protegendo seus direitos com inteligência artificial
          </p>
        </div>
        
        {/* Form Container */}
        <div className="bg-white/90 backdrop-blur-sm rounded-3xl shadow-2xl p-8 border border-white/20">
          {children}
        </div>
        
        {/* Footer */}
        <div className="text-center">
          <p className="text-xs text-gray-500">
            🔒 Protegido por criptografia de ponta a ponta
          </p>
          <Link href="/" className="text-xs text-blue-600 hover:text-blue-700 mt-2 inline-block">
            ← Voltar para a página inicial
          </Link>
        </div>
      </div>
    </div>
  )
}
