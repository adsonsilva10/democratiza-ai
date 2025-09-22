import './globals.css'

export const metadata = {
  title: 'Contrato Seguro - Análise Inteligente de Contratos',
  description: 'Democratizando a compreensão jurídica no Brasil. Analise seus contratos com IA especializada e tome decisões mais seguras.',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="pt-BR">
      <body className="overflow-x-hidden">
        {children}
      </body>
    </html>
  )
}
