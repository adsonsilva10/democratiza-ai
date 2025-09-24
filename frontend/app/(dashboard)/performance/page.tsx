import PerformanceDashboard from '@/components/features/PerformanceDashboard'

export default function PerformancePage() {
  return (
    <div className="w-full max-w-7xl mx-auto">
      {/* Header da página */}
      <div className="mb-8">
        <h1 className="text-2xl sm:text-3xl lg:text-4xl font-bold text-gray-900 mb-4">
          📊 Performance & Analytics
        </h1>
        <p className="text-gray-600 text-base sm:text-lg">
          Monitor de performance da aplicação, métricas web vitais e análises de uso
        </p>
      </div>

      {/* Componente de dashboard */}
      <PerformanceDashboard />
    </div>
  )
}