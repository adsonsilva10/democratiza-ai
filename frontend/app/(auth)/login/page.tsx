'use client'

import { useState } from 'react'
import Link from 'next/link'
import { Eye, EyeOff, Mail, Lock, ArrowRight } from 'lucide-react'
import { signInWithGoogle, signInWithEmail } from '@/lib/supabase'

export default function LoginPage() {
  const [formData, setFormData] = useState({
    email: '',
    password: ''
  })
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [showPassword, setShowPassword] = useState(false)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setIsLoading(true)
    setError(null)

    try {
      // Tentar login real com Supabase primeiro
      await signInWithEmail(formData.email, formData.password)
      
      // Se chegou até aqui, login foi bem-sucedido
      window.location.href = '/dashboard'
      
    } catch (supabaseError) {
      console.log('Login Supabase falhou, tentando credenciais demo...', supabaseError)
      
      try {
        // Fallback para credenciais de demonstração
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
          
          console.log('✅ Login demo realizado com sucesso!')
          window.location.href = '/dashboard'
        } else {
          setError('Email ou senha incorretos.')
        }
      } catch (err) {
        setError('Erro ao fazer login. Tente novamente.')
      }
    } finally {
      setIsLoading(false)
    }
  }

  const handleGoogleLogin = async () => {
    try {
      setIsLoading(true)
      setError(null)
      
      console.log('🚀 Iniciando login com Google...')
      await signInWithGoogle()
      
      // O redirecionamento será automático via Supabase
      
    } catch (error: any) {
      console.error('❌ Erro no login com Google:', error)
      setError(error.message || 'Erro ao fazer login com Google. Tente novamente.')
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
      <div className="text-center mb-8">
        <h2 className="text-2xl font-bold text-gray-900 mb-2">Bem-vindo de volta!</h2>
        <p className="text-gray-600 text-sm">
          Não tem uma conta?{' '}
          <Link href="/register" className="text-red-500 hover:text-red-600 font-medium">
            Cadastre-se grátis
          </Link>
        </p>
      </div>

      <form onSubmit={handleSubmit} className="space-y-6 w-full">
        {/* Email Field */}
        <div className="w-full">
          <label htmlFor="email" className="block text-sm font-semibold text-gray-700 mb-2">
            Email
          </label>
          <div className="relative">
            <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              <Mail className="h-5 w-5 text-gray-400" />
            </div>
            <input
              id="email"
              name="email"
              type="email"
              required
              value={formData.email}
              onChange={handleChange}
              className="block w-full pl-10 pr-3 py-3 border border-gray-200 rounded-xl shadow-sm focus:outline-none focus:ring-2 focus:ring-red-500 focus:border-red-500 transition-colors bg-gray-50 focus:bg-white"
              placeholder="seu@email.com"
            />
          </div>
        </div>

        {/* Password Field */}
        <div className="w-full">
          <label htmlFor="password" className="block text-sm font-semibold text-gray-700 mb-2">
            Senha
          </label>
          <div className="relative">
            <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              <Lock className="h-5 w-5 text-gray-400" />
            </div>
            <input
              id="password"
              name="password"
              type={showPassword ? 'text' : 'password'}
              required
              value={formData.password}
              onChange={handleChange}
              className="block w-full pl-10 pr-10 py-3 border border-gray-200 rounded-xl shadow-sm focus:outline-none focus:ring-2 focus:ring-red-500 focus:border-red-500 transition-colors bg-gray-50 focus:bg-white"
              placeholder="Digite sua senha"
            />
            <button
              type="button"
              className="absolute inset-y-0 right-0 pr-3 flex items-center"
              onClick={() => setShowPassword(!showPassword)}
            >
              {showPassword ? (
                <EyeOff className="h-5 w-5 text-gray-400 hover:text-gray-600" />
              ) : (
                <Eye className="h-5 w-5 text-gray-400 hover:text-gray-600" />
              )}
            </button>
          </div>
        </div>

        {/* Remember Me & Forgot Password */}
        <div className="flex items-center justify-between">
          <div className="flex items-center">
            <input
              id="remember-me"
              name="remember-me"
              type="checkbox"
              className="h-4 w-4 text-red-500 focus:ring-red-500 border-gray-300 rounded"
            />
            <label htmlFor="remember-me" className="ml-2 block text-sm text-gray-700">
              Lembrar de mim
            </label>
          </div>
          <Link href="#" className="text-sm text-red-500 hover:text-red-600 font-medium">
            Esqueceu a senha?
          </Link>
        </div>

        {/* Error Message */}
        {error && (
          <div className="p-4 bg-red-50 border border-red-200 rounded-xl">
            <div className="flex items-center">
              <div className="w-6 h-6 bg-red-100 rounded-full flex items-center justify-center mr-3">
                <span className="text-red-600 text-sm">⚠️</span>
              </div>
              <p className="text-red-700 text-sm">{error}</p>
            </div>
          </div>
        )}

        {/* Submit Button */}
        <button
          type="submit"
          disabled={isLoading}
          className="w-full flex items-center justify-center gap-2 py-3 px-4 bg-gradient-to-r from-red-500 to-orange-500 text-white font-semibold rounded-xl shadow-lg hover:shadow-xl transition-all duration-300 transform hover:scale-[1.02] disabled:opacity-50 disabled:transform-none"
        >
          {isLoading ? (
            <>
              <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin" />
              <span>Entrando...</span>
            </>
          ) : (
            <>
              <span>Entrar na minha conta</span>
              <ArrowRight className="w-5 h-5" />
            </>
          )}
        </button>
      </form>

      {/* Social Login */}
      <div className="mt-8">
        <div className="relative">
          <div className="absolute inset-0 flex items-center">
            <div className="w-full border-t border-gray-200" />
          </div>
          <div className="relative flex justify-center text-sm">
            <span className="px-4 bg-white text-gray-500">ou continue com</span>
          </div>
        </div>

        <div className="mt-6">
          <button 
            type="button"
            onClick={handleGoogleLogin}
            disabled={isLoading}
            className="w-full inline-flex items-center justify-center gap-3 py-3 px-4 border border-gray-200 rounded-xl shadow-sm bg-white text-sm font-medium text-gray-700 hover:bg-gray-50 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {isLoading ? (
              <div className="w-5 h-5 border-2 border-gray-400 border-t-transparent rounded-full animate-spin" />
            ) : (
              <div className="w-5 h-5 bg-red-500 rounded text-white text-xs flex items-center justify-center font-bold">G</div>
            )}
            <span>Continuar com Google</span>
          </button>
        </div>
      </div>
    </div>
  )
}
