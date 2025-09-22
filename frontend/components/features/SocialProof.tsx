'use client'

export default function SocialProof() {
  return (
    <section className="px-4 sm:px-6 lg:px-8 py-16 sm:py-20 bg-white">
      <div className="mx-auto max-w-7xl">
        {/* Header */}
        <div className="text-center mb-16">
          <h2 className="text-3xl sm:text-4xl lg:text-5xl font-bold text-gray-900 mb-6">
            Proteja seus contratos com tecnologia avançada
          </h2>
          <p className="text-lg sm:text-xl text-gray-600 max-w-3xl mx-auto">
            Nossa plataforma utiliza inteligência artificial de última geração para analisar 
            cada cláusula e identificar potenciais riscos antes da assinatura.
          </p>
        </div>

        {/* Trust Badges */}
        <div className="mt-16 flex flex-wrap justify-center gap-8 items-center opacity-60">
          <div className="flex items-center gap-2 text-sm text-gray-600">
            <span className="text-green-500 text-lg">🔒</span>
            <span>Criptografia end-to-end</span>
          </div>
          <div className="flex items-center gap-2 text-sm text-gray-600">
            <span className="text-blue-500 text-lg">📋</span>
            <span>Conforme LGPD</span>
          </div>
          <div className="flex items-center gap-2 text-sm text-gray-600">
            <span className="text-purple-500 text-lg">🗑️</span>
            <span>Dados excluídos após análise</span>
          </div>
          <div className="flex items-center gap-2 text-sm text-gray-600">
            <span className="text-yellow-500 text-lg">⚡</span>
            <span>Disponível 24/7</span>
          </div>
        </div>
      </div>
    </section>
  )
}