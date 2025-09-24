'use client'

import { useState } from 'react'
import Link from 'next/link'

export default function LoginPage() {
  const [formData, setFormData] = useState({
    email: '',
    password: ''
  })
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setIsLoading(true)
    setError(null)

    try {
      // Simular delay de autenticação
      await new Promise(resolve => setTimeout(resolve, 1000))
      
      // Credenciais de demonstração
      const validCredentials = [
        { email: 'demo@democratiza.ai', password: 'demo123' },
        { email: 'admin@democratiza.ai', password: 'admin123' },
        { email: 'user@test.com', password: '123456' }
      ]

      const isValid = validCredentials.some(
        cred => cred.email === formData.email && cred.password === formData.password
      )

      if (isValid) {
        // Salvar token fictício no localStorage
        localStorage.setItem('auth-token', 'demo-token-' + Date.now())
        localStorage.setItem('user-email', formData.email)
        
        alert('Login realizado com sucesso!')
        window.location.href = '/dashboard'
      } else {
        setError('Email ou senha incorretos. Tente: demo@democratiza.ai / demo123')
      }
      
    } catch (err) {
      setError('Erro ao fazer login. Tente novamente.')
    } finally {
      setIsLoading(false)
    }
  }

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData(prev => ({
      ...prev,
      [e.target.name]: e.target.value
    }))
  }

  return (
    <div className="w-full">
      <div className="text-center mb-6">
        <h2 className="text-xl sm:text-2xl font-bold text-gray-900 truncate">Entrar na sua conta</h2>
        <p className="mt-2 text-sm text-gray-600">
          Ou{' '}
          <Link href="/register" className="text-blue-600 hover:text-blue-500">
            crie uma nova conta
          </Link>
        </p>
      </div>

      {/* Credenciais de demonstração */}
      <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 mb-6">
        <h3 className="text-sm font-medium text-blue-900 mb-2">🔑 Credenciais de Demonstração</h3>
        <div className="space-y-2 text-sm">
          <div className="bg-white rounded p-2 border">
            <p className="font-mono text-blue-800">📧 demo@democratiza.ai</p>
            <p className="font-mono text-blue-800">🔒 demo123</p>
          </div>
          <div className="bg-white rounded p-2 border">
            <p className="font-mono text-blue-800">📧 admin@democratiza.ai</p>
            <p className="font-mono text-blue-800">🔒 admin123</p>
          </div>
          <div className="bg-white rounded p-2 border">
            <p className="font-mono text-blue-800">📧 user@test.com</p>
            <p className="font-mono text-blue-800">🔒 123456</p>
          </div>
        </div>
        <p className="text-xs text-blue-600 mt-2">
          💡 Use qualquer uma dessas credenciais para acessar o sistema
        </p>
      </div>

      <form onSubmit={handleSubmit} className="space-y-6 w-full">
        <div className="w-full">
          <label htmlFor="email" className="block text-sm font-medium text-gray-700">
            Email
          </label>
          <input
            id="email"
            name="email"
            type="email"
            required
            value={formData.email}
            onChange={handleChange}
            className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 min-w-0"
            placeholder="seu@email.com"
          />
        </div>

        <div className="w-full">
          <label htmlFor="password" className="block text-sm font-medium text-gray-700">
            Senha
          </label>
          <input
            id="password"
            name="password"
            type="password"
            required
            value={formData.password}
            onChange={handleChange}
            className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 min-w-0"
            placeholder="••••••••"
          />
        </div>

        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3 w-full">
          <div className="flex items-center flex-shrink-0">
            <input
              id="remember-me"
              name="remember-me"
              type="checkbox"
              className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
            />
            <label htmlFor="remember-me" className="ml-2 block text-sm text-gray-900 truncate">
              Lembrar de mim
            </label>
          </div>

          <div className="text-sm flex-shrink-0">
            <a href="#" className="text-blue-600 hover:text-blue-500 truncate">
              Esqueceu a senha?
            </a>
          </div>
        </div>

        {error && (
          <div className="p-3 bg-red-100 border border-red-300 rounded-md w-full">
            <p className="text-red-700 text-sm break-words">❌ {error}</p>
          </div>
        )}

        <button
          type="submit"
          disabled={isLoading}
          className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:bg-gray-400"
        >
          {isLoading ? '🔄 Entrando...' : '🔑 Entrar'}
        </button>

        {/* Botões de acesso rápido */}
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-2 mt-4">
          <button
            type="button"
            onClick={() => setFormData({email: 'demo@democratiza.ai', password: 'demo123'})}
            className="text-xs px-3 py-1 bg-green-100 text-green-700 rounded hover:bg-green-200 transition-colors"
          >
            🚀 Demo
          </button>
          <button
            type="button"
            onClick={() => setFormData({email: 'admin@democratiza.ai', password: 'admin123'})}
            className="text-xs px-3 py-1 bg-purple-100 text-purple-700 rounded hover:bg-purple-200 transition-colors"
          >
            👑 Admin
          </button>
          <button
            type="button"
            onClick={() => setFormData({email: 'user@test.com', password: '123456'})}
            className="text-xs px-3 py-1 bg-blue-100 text-blue-700 rounded hover:bg-blue-200 transition-colors"
          >
            👤 User
          </button>
        </div>
      </form>

      <div className="mt-6 w-full">
        <div className="relative">
          <div className="absolute inset-0 flex items-center">
            <div className="w-full border-t border-gray-300" />
          </div>
          <div className="relative flex justify-center text-sm">
            <span className="px-2 bg-white text-gray-500">Ou continue com</span>
          </div>
        </div>

        <div className="mt-6 grid grid-cols-1 sm:grid-cols-2 gap-3 w-full">
          <button className="w-full inline-flex justify-center py-2 px-4 border border-gray-300 rounded-md shadow-sm bg-white text-sm font-medium text-gray-500 hover:bg-gray-50 min-w-0">
            <span className="truncate">📧 Google</span>
          </button>
          <button className="w-full inline-flex justify-center py-2 px-4 border border-gray-300 rounded-md shadow-sm bg-white text-sm font-medium text-gray-500 hover:bg-gray-50 min-w-0">
            <span className="truncate">📘 Facebook</span>
          </button>
        </div>
      </div>
    </div>
  )
}
