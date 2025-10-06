'use client'

import { useEffect, useState } from 'react'
import { Button } from '@/components/ui/button'
import { Card } from '@/components/ui/card'
import { AlertTriangle, Clock } from 'lucide-react'

interface SessionTimeoutWarningProps {
  onStayLoggedIn: () => void
  onLogout: () => Promise<void>
  timeRemaining: number
}

export function SessionTimeoutWarning({
  onStayLoggedIn,
  onLogout,
  timeRemaining: initialTimeRemaining,
}: SessionTimeoutWarningProps) {
  const [timeRemaining, setTimeRemaining] = useState(initialTimeRemaining)

  useEffect(() => {
    // Atualizar contador a cada segundo
    const interval = setInterval(() => {
      setTimeRemaining((prev) => Math.max(0, prev - 1000))
    }, 1000)

    return () => clearInterval(interval)
  }, [])

  // Auto-logout quando tempo acabar
  useEffect(() => {
    if (timeRemaining <= 0) {
      onLogout()
    }
  }, [timeRemaining, onLogout])

  const formatTime = (ms: number) => {
    const minutes = Math.floor(ms / 1000 / 60)
    const seconds = Math.floor((ms / 1000) % 60)
    return `${minutes}:${seconds.toString().padStart(2, '0')}`
  }

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-sm">
      <Card className="w-full max-w-md mx-4 p-6 shadow-2xl animate-in fade-in-0 zoom-in-95">
        <div className="flex items-center gap-3 mb-4">
          <div className="rounded-full bg-yellow-100 p-2">
            <AlertTriangle className="h-6 w-6 text-yellow-600" />
          </div>
          <h2 className="text-xl font-semibold">Sessão Expirando</h2>
        </div>

        <p className="text-gray-600 mb-6">
          Sua sessão está prestes a expirar por inatividade. Você será desconectado automaticamente em:
        </p>

        <div className="flex justify-center py-6 mb-6">
          <div className="flex items-center gap-3 rounded-lg bg-gray-100 px-8 py-4">
            <Clock className="h-6 w-6 text-gray-600" />
            <span className="text-3xl font-bold text-gray-900">
              {formatTime(timeRemaining)}
            </span>
          </div>
        </div>

        <div className="flex gap-3">
          <Button
            variant="outline"
            onClick={onLogout}
            className="flex-1"
          >
            Sair Agora
          </Button>
          <Button
            onClick={onStayLoggedIn}
            className="flex-1 bg-primary hover:bg-primary/90"
          >
            Continuar Conectado
          </Button>
        </div>
      </Card>
    </div>
  )
}
