'use client'

import { useState } from 'react'
import Link from 'next/link'

export default function RegisterPage() {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    password: '',
    confirmPassword: ''
  })
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setIsLoading(true)
    setError(null)

    // Validações
    if (formData.password !== formData.confirmPassword) {
      setError('As senhas não coincidem')
      setIsLoading(false)
      return
    }

    if (formData.password.length < 6) {
      setError('A senha deve ter pelo menos 6 caracteres')
      setIsLoading(false)
      return
    }

    try {
      // Simular registro
      await new Promise(resolve => setTimeout(resolve, 1000))
      
      // Aqui você faria a chamada para a API
      // const response = await fetch('/api/v1/auth/register', {
      //   method: 'POST',
      //   headers: { 'Content-Type': 'application/json' },
      //   body: JSON.stringify({
      //     name: formData.name,
      //     email: formData.email,
      //     password: formData.password
      //   })
      // })

      // Simular sucesso
      alert('Conta criada com sucesso! Faça login para continuar.')
      window.location.href = '/login'
      
    } catch (err) {
      setError('Erro ao criar conta. Tente novamente.')
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
        <h2 className="text-xl sm:text-2xl font-bold text-gray-900 truncate">Criar nova conta</h2>
        <p className="mt-2 text-sm text-gray-600">
          Já tem uma conta?{' '}
          <Link href="/login" className="text-blue-600 hover:text-blue-500">
            Faça login
          </Link>
        </p>
      </div>

      <form onSubmit={handleSubmit} className="space-y-6 w-full">
        <div className="w-full">
          <label htmlFor="name" className="block text-sm font-medium text-gray-700">
            Nome completo
          </label>
          <input
            id="name"
            name="name"
            type="text"
            required
            value={formData.name}
            onChange={handleChange}
            className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 min-w-0"
            placeholder="Seu nome completo"
          />
        </div>

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
          <p className="mt-1 text-sm text-gray-500">Mínimo 6 caracteres</p>
        </div>

        <div className="w-full">
          <label htmlFor="confirmPassword" className="block text-sm font-medium text-gray-700">
            Confirmar senha
          </label>
          <input
            id="confirmPassword"
            name="confirmPassword"
            type="password"
            required
            value={formData.confirmPassword}
            onChange={handleChange}
            className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 min-w-0"
            placeholder="••••••••"
          />
        </div>

        <div className="flex items-start w-full">
          <input
            id="terms"
            name="terms"
            type="checkbox"
            required
            className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded flex-shrink-0 mt-0.5"
          />
          <label htmlFor="terms" className="ml-2 block text-sm text-gray-900 min-w-0">
            Aceito os{' '}
            <a href="#" className="text-blue-600 hover:text-blue-500">
              termos de uso
            </a>{' '}
            e{' '}
            <a href="#" className="text-blue-600 hover:text-blue-500">
              política de privacidade
            </a>
          </label>
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
          {isLoading ? '🔄 Criando conta...' : '🚀 Criar conta'}
        </button>
      </form>

      <div className="mt-6 w-full">
        <div className="relative">
          <div className="absolute inset-0 flex items-center">
            <div className="w-full border-t border-gray-300" />
          </div>
          <div className="relative flex justify-center text-sm">
            <span className="px-2 bg-white text-gray-500">Ou registre-se com</span>
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