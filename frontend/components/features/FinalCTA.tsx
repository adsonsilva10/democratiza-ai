'use client'

import Link from 'next/link'

export default function FinalCTA() {
  return (
    <section className="px-4 sm:px-6 lg:px-8 py-12 sm:py-16 lg:py-20 w-full overflow-hidden">
      <div className="mx-auto max-w-4xl w-full">
        {/* Main CTA Card */}
        <div className="bg-gradient-to-r from-blue-600 via-purple-600 to-blue-800 rounded-2xl sm:rounded-3xl p-6 sm:p-8 lg:p-12 xl:p-16 text-white relative overflow-hidden w-full">
          {/* Background Pattern */}
          <div className="absolute inset-0 bg-gradient-to-br from-white/10 to-transparent"></div>
          <div className="absolute top-0 right-0 w-24 h-24 sm:w-32 sm:h-32 lg:w-48 lg:h-48 xl:w-64 xl:h-64 bg-white/5 rounded-full -translate-y-12 sm:-translate-y-16 lg:-translate-y-24 xl:-translate-y-32 translate-x-12 sm:translate-x-16 lg:translate-x-24 xl:translate-x-32"></div>
          <div className="absolute bottom-0 left-0 w-16 h-16 sm:w-24 sm:h-24 lg:w-36 lg:h-36 xl:w-48 xl:h-48 bg-white/5 rounded-full translate-y-8 sm:translate-y-12 lg:translate-y-18 xl:translate-y-24 -translate-x-8 sm:-translate-x-12 lg:-translate-x-18 xl:-translate-x-24"></div>
          
          <div className="relative z-10 text-center w-full">
            {/* Headline */}
            <h2 className="text-2xl sm:text-3xl lg:text-4xl xl:text-5xl font-bold mb-4 sm:mb-6 leading-tight w-full">
              Pronto para proteger 
              <span className="block">seu negócio?</span>
            </h2>
            
            {/* Description */}
            <p className="text-lg sm:text-xl lg:text-2xl mb-6 sm:mb-8 opacity-90 max-w-3xl mx-auto leading-relaxed px-2 w-full">
              Junte-se a milhares de profissionais que nunca mais assinam um contrato arriscado. 
              <span className="block mt-2 font-semibold">
                Comece com uma análise gratuita agora.
              </span>
            </p>
            
            {/* Action Buttons */}
            <div className="flex flex-col sm:flex-row gap-3 sm:gap-4 justify-center max-w-lg mx-auto mb-6 sm:mb-8 px-2 w-full">
              <Link
                href="/dashboard"
                className="bg-white text-blue-600 hover:bg-gray-100 px-6 sm:px-8 py-3 sm:py-4 rounded-xl font-semibold text-base sm:text-lg transition-all transform hover:scale-105 shadow-lg flex items-center justify-center gap-2 w-full sm:w-auto"
              >
                <span className="text-lg sm:text-xl">🚀</span>
                Começar Teste Grátis
              </Link>
              <Link 
                href="/chat" 
                className="border-2 border-white/30 text-white hover:bg-white/10 px-6 sm:px-8 py-3 sm:py-4 rounded-xl font-semibold text-base sm:text-lg transition-all text-center flex items-center justify-center gap-2 w-full sm:w-auto"
              >
                <span className="text-lg sm:text-xl">💬</span>
                Falar com IA
              </Link>
            </div>
            
            {/* Trust Indicators */}
            <div className="flex flex-wrap justify-center gap-3 sm:gap-4 lg:gap-6 text-xs sm:text-sm opacity-80 px-2 w-full">
              <div className="flex items-center gap-1.5 sm:gap-2">
                <span className="text-sm sm:text-base lg:text-lg">✓</span>
                <span>30 dias grátis</span>
              </div>
              <div className="flex items-center gap-1.5 sm:gap-2">
                <span className="text-sm sm:text-base lg:text-lg">✓</span>
                <span>Sem cartão</span>
              </div>
              <div className="flex items-center gap-1.5 sm:gap-2">
                <span className="text-sm sm:text-base lg:text-lg">✓</span>
                <span>Suporte 24/7</span>
              </div>
              <div className="flex items-center gap-1.5 sm:gap-2">
                <span className="text-sm sm:text-base lg:text-lg">✓</span>
                <span>Cancele quando quiser</span>
              </div>
            </div>
          </div>
        </div>
        
        {/* Secondary CTAs */}
        <div className="grid gap-4 sm:gap-6 md:grid-cols-3 mt-8 sm:mt-12 w-full">
          <div className="text-center p-4 sm:p-6 bg-gradient-to-br from-green-50 to-emerald-50 rounded-xl border border-green-200 w-full">
            <div className="text-3xl sm:text-4xl mb-3 sm:mb-4">⚡</div>
            <h3 className="font-bold text-green-800 mb-2 text-sm sm:text-base w-full">Análise Instantânea</h3>
            <p className="text-green-700 text-xs sm:text-sm w-full">Resultados em 3 segundos garantidos</p>
          </div>
          
          <div className="text-center p-4 sm:p-6 bg-gradient-to-br from-blue-50 to-cyan-50 rounded-xl border border-blue-200 w-full">
            <div className="text-3xl sm:text-4xl mb-3 sm:mb-4">🎯</div>
            <h3 className="font-bold text-blue-800 mb-2 text-sm sm:text-base w-full">IA Avançada</h3>
            <p className="text-blue-700 text-xs sm:text-sm w-full">Tecnologia de última geração</p>
          </div>
          
          <div className="text-center p-4 sm:p-6 bg-gradient-to-br from-purple-50 to-pink-50 rounded-xl border border-purple-200 w-full">
            <div className="text-3xl sm:text-4xl mb-3 sm:mb-4">🔒</div>
            <h3 className="font-bold text-purple-800 mb-2 text-sm sm:text-base w-full">100% Seguro</h3>
            <p className="text-purple-700 text-xs sm:text-sm w-full">Seus dados protegidos e privados</p>
          </div>
        </div>
      </div>
    </section>
  )
}