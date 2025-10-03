'use client'

import { useEffect, useState } from 'react'
import { supabase } from '@/lib/supabase'
import { Loader2, CheckCircle2, XCircle } from 'lucide-react'

export default function AuthCallback() {
  const [status, setStatus] = useState<'loading' | 'success' | 'error'>('loading')
  const [message, setMessage] = useState('Processando login...')

  useEffect(() => {
    const handleAuthCallback = async () => {
      try {
        console.log('🔄 Processando callback de autenticação...')
        
        // Pega os parâmetros da URL
        const { data, error } = await supabase.auth.getSession()
        
        if (error) {
          console.error('❌ Erro no callback:', error.message)
          setStatus('error')
          setMessage(`Erro na autenticação: ${error.message}`)
          return
        }

        if (data.session) {
          console.log('✅ Login realizado com sucesso!')
          console.log('👤 Usuário:', data.session.user.email)
          
          // Salvar dados no localStorage para compatibilidade
          localStorage.setItem('auth-token', data.session.access_token)
          localStorage.setItem('user-email', data.session.user.email || '')
          
          setStatus('success')
          setMessage('Login realizado com sucesso!')
          
          // Redirecionar após 2 segundos
          setTimeout(() => {
            window.location.href = '/dashboard'
          }, 2000)
          
        } else {
          console.log('ℹ️ Nenhuma sessão encontrada no callback')
          setStatus('error')
          setMessage('Nenhuma sessão de autenticação encontrada.')
        }
        
      } catch (error: any) {
        console.error('❌ Erro no processamento do callback:', error)
        setStatus('error')
        setMessage(`Erro inesperado: ${error.message}`)
      }
    }

    handleAuthCallback()
  }, [])

  const handleReturnToLogin = () => {
    window.location.href = '/login'
  }

  const handleGoToDashboard = () => {
    window.location.href = '/dashboard'
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-red-50 via-orange-50 to-yellow-50 flex items-center justify-center p-4">
      <div className="max-w-md w-full">
        <div className="bg-white rounded-2xl shadow-xl p-8 text-center">
          
          {/* Header */}
          <div className="mb-6">
            <div className="w-16 h-16 bg-gradient-to-r from-red-500 to-orange-500 rounded-full flex items-center justify-center mx-auto mb-4">
              <span className="text-white text-2xl font-bold">D</span>
            </div>
            <h1 className="text-2xl font-bold text-gray-900 mb-2">
              Democratiza AI
            </h1>
          </div>

          {/* Status Content */}
          {status === 'loading' && (
            <div className="space-y-4">
              <div className="flex items-center justify-center">
                <Loader2 className="w-8 h-8 text-blue-600 animate-spin" />
              </div>
              <h2 className="text-xl font-semibold text-gray-900">
                Processando login...
              </h2>
              <p className="text-gray-600">
                Aguarde enquanto validamos sua autenticação.
              </p>
            </div>
          )}

          {status === 'success' && (
            <div className="space-y-4">
              <div className="flex items-center justify-center">
                <CheckCircle2 className="w-12 h-12 text-green-600" />
              </div>
              <h2 className="text-xl font-semibold text-green-900">
                Login realizado com sucesso!
              </h2>
              <p className="text-gray-600">
                Redirecionando para o dashboard...
              </p>
              <button
                onClick={handleGoToDashboard}
                className="w-full mt-4 bg-gradient-to-r from-green-500 to-emerald-500 text-white font-semibold py-3 px-6 rounded-xl hover:shadow-lg transition-all duration-300"
              >
                Ir para Dashboard
              </button>
            </div>
          )}

          {status === 'error' && (
            <div className="space-y-4">
              <div className="flex items-center justify-center">
                <XCircle className="w-12 h-12 text-red-600" />
              </div>
              <h2 className="text-xl font-semibold text-red-900">
                Erro na autenticação
              </h2>
              <p className="text-gray-600 text-sm">
                {message}
              </p>
              <div className="space-y-3 mt-6">
                <button
                  onClick={handleReturnToLogin}
                  className="w-full bg-gradient-to-r from-red-500 to-orange-500 text-white font-semibold py-3 px-6 rounded-xl hover:shadow-lg transition-all duration-300"
                >
                  Voltar ao Login
                </button>
                <button
                  onClick={() => window.location.reload()}
                  className="w-full bg-gray-100 text-gray-700 font-semibold py-3 px-6 rounded-xl hover:bg-gray-200 transition-all duration-300"
                >
                  Tentar Novamente
                </button>
              </div>
            </div>
          )}

          {/* Footer */}
          <div className="mt-8 pt-6 border-t border-gray-100">
            <p className="text-xs text-gray-500">
              Plataforma de análise inteligente de contratos
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}