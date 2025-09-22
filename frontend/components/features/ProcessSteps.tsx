'use client'

export default function ProcessSteps() {
  const steps = [
    {
      number: '01',
      icon: '📄',
      title: 'Envie seu contrato',
      description: 'Arraste e solte seu contrato ou cole o texto diretamente. Suportamos PDF, Word e texto com segurança enterprise.',
      badges: ['PDF', 'DOCX', 'TXT'],
      bgColor: 'from-blue-500 to-purple-500'
    },
    {
      number: '02', 
      icon: '🤖',
      title: 'IA analisa cada cláusula',
      description: 'Nossa IA avançada escaneia linha por linha, identificando riscos potenciais, linguagem tendenciosa e termos injustos.',
      badges: ['500+ categorias', 'Detecção de viés'],
      bgColor: 'from-purple-500 to-pink-500'
    },
    {
      number: '03',
      icon: '📊', 
      title: 'Receba insights acionáveis',
      description: 'Relatório completo com níveis de risco, explicações em linguagem simples e recomendações específicas.',
      badges: ['Score de risco', 'Sugestões'],
      bgColor: 'from-green-500 to-emerald-500'
    }
  ]

  return (
    <section className="px-4 sm:px-6 lg:px-8 py-8 sm:py-12 lg:py-16 bg-gradient-to-br from-gray-50 to-blue-50 w-full overflow-hidden">
      <div className="mx-auto max-w-6xl w-full">
        {/* Header */}
        <div className="text-center mb-8 sm:mb-12 lg:mb-16 w-full">
          <h2 className="text-2xl sm:text-3xl lg:text-4xl xl:text-5xl font-bold text-gray-900 mb-3 sm:mb-4 w-full">
            Análise em 3 passos simples
          </h2>
          <p className="text-base sm:text-lg lg:text-xl text-gray-600 max-w-3xl mx-auto px-4 sm:px-0 w-full">
            Do upload aos insights em menos de 5 segundos. Nenhuma expertise jurídica necessária.
          </p>
        </div>

        {/* Steps Grid */}
        <div className="grid gap-6 sm:gap-8 md:grid-cols-3 lg:gap-12 w-full">
          {steps.map((step, index) => (
            <div key={index} className="relative w-full">
              {/* Step Card */}
              <div className="bg-white rounded-2xl shadow-lg p-6 sm:p-8 h-full hover:shadow-xl transition-all duration-300 hover:-translate-y-2 border border-white/20 w-full">
                {/* Step Number */}
                <div className={`flex items-center justify-center w-12 h-12 sm:w-16 sm:h-16 bg-gradient-to-r ${step.bgColor} rounded-full text-white text-lg sm:text-2xl font-bold mb-4 sm:mb-6 mx-auto`}>
                  {step.number}
                </div>
                
                {/* Icon */}
                <div className="text-4xl sm:text-5xl lg:text-6xl text-center mb-4 sm:mb-6">{step.icon}</div>
                
                {/* Content */}
                <h3 className="text-lg sm:text-xl font-bold mb-3 sm:mb-4 text-center text-gray-900 w-full">
                  {step.title}
                </h3>
                <p className="text-sm sm:text-base text-gray-600 text-center leading-relaxed mb-4 sm:mb-6 w-full">
                  {step.description}
                </p>
                
                {/* Badges */}
                <div className="flex flex-wrap gap-2 justify-center w-full">
                  {step.badges.map((badge, badgeIndex) => (
                    <span
                      key={badgeIndex}
                      className="bg-gray-100 text-gray-800 px-2.5 sm:px-3 py-1 rounded-full text-xs sm:text-sm font-medium whitespace-nowrap"
                    >
                      {badge}
                    </span>
                  ))}
                </div>
              </div>

              {/* Connector Arrow - Hidden on mobile, shown on desktop */}
              {index < steps.length - 1 && (
                <div className="hidden md:block absolute top-1/2 -right-6 lg:-right-8 w-8 h-8 text-gray-300 transform -translate-y-1/2">
                  <svg fill="currentColor" viewBox="0 0 20 20" className="w-full h-full">
                    <path 
                      fillRule="evenodd" 
                      d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" 
                      clipRule="evenodd" 
                    />
                  </svg>
                </div>
              )}
            </div>
          ))}
        </div>

        {/* Call to Action */}
        <div className="text-center mt-8 sm:mt-12">
          <button className="bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white px-6 sm:px-8 py-3 sm:py-4 rounded-xl font-semibold text-base sm:text-lg transition-all transform hover:scale-105 shadow-lg">
            Comece Agora - É Grátis
          </button>
          <p className="text-xs sm:text-sm text-gray-500 mt-2 sm:mt-3 px-4">
            ✓ Teste grátis por 30 dias • ✓ Sem cartão de crédito • ✓ Suporte 24/7
          </p>
        </div>
      </div>
    </section>
  )
}