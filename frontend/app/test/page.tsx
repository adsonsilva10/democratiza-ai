export default function TestPage() {
  return (
    <div className="min-h-screen bg-gray-50 p-8">
      <h1 className="text-2xl font-bold">Página de Teste</h1>
      <p>Se você está vendo esta página, o Next.js está funcionando!</p>
      <div className="mt-4">
        <a 
          href="/contracts" 
          className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
        >
          Ir para Contratos
        </a>
      </div>
    </div>
  )
}