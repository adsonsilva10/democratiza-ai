'use client'

import React, { useState } from 'react'
import Link from 'next/link'
import { useRouter } from 'next/navigation'
import { User, Mail, Lock, Eye, EyeOff, ArrowRight, Check } from 'lucide-react'
import { signUpWithEmail } from '@/lib/supabase'

interface FormData {
  name: string
  email: string
  password: string
  confirmPassword: string
}

export default function Register() {
  const router = useRouter()
  const [formData, setFormData] = useState<FormData>({
    name: '',
    email: '',
    password: '',
    confirmPassword: '',
  })
  const [showPassword, setShowPassword] = useState(false)
  const [showConfirmPassword, setShowConfirmPassword] = useState(false)
  const [isLoading, setIsLoading] = useState(false)
  const [errors, setErrors] = useState<string[]>([])
  const [successMessage, setSuccessMessage] = useState('')

  function handleChange(e: React.ChangeEvent<HTMLInputElement>) {
    const { id, value } = e.target
    setFormData(prev => ({ ...prev, [id]: value }))
    setErrors([]) // Clear errors when user types
  }

  function validateForm(): string[] {
    const newErrors: string[] = []
    
    if (formData.name.length < 2) {
      newErrors.push('Nome deve ter pelo menos 2 caracteres')
    }
    
    if (!formData.email.includes('@')) {
      newErrors.push('Email deve ser válido')
    }
    
    if (formData.password.length < 6) {
      newErrors.push('Senha deve ter pelo menos 6 caracteres')
    }
    
    if (formData.password !== formData.confirmPassword) {
      newErrors.push('Senhas não coincidem')
    }
    
    return newErrors
  }

  async function handleSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault()
    
    const validationErrors = validateForm()
    if (validationErrors.length > 0) {
      setErrors(validationErrors)
      return
    }
    
    setIsLoading(true)
    setErrors([])
    setSuccessMessage('')
    
    try {
      console.log('🔄 Tentando criar conta no Supabase...')
      
      const result = await signUpWithEmail(
        formData.email.trim(),
        formData.password,
        formData.name.trim()
      )

      if (result.user) {
        console.log('✅ Conta criada com sucesso:', result.user)
        
        // Verificar se precisa de confirmação de email
        if (result.user.email_confirmed_at || process.env.NODE_ENV === 'development') {
          setSuccessMessage('Conta criada com sucesso! Você já pode fazer login.')
          setTimeout(() => {
            router.push('/login?message=Conta criada com sucesso! Faça seu login')
          }, 2000)
        } else {
          setSuccessMessage('Conta criada com sucesso! Verifique seu email para confirmar.')
          setTimeout(() => {
            router.push('/login?message=Verifique seu email para ativar a conta')
          }, 2000)
        }
      } else {
        console.warn('⚠️ Usuário não retornado, mas sem erro')
        setErrors(['Erro inesperado ao criar conta. Tente novamente.'])
      }
      
    } catch (error: any) {
      console.error('❌ Erro ao criar conta:', error)
      
      // Tratamento de erros específicos do Supabase
      if (error.message?.includes('User already registered')) {
        setErrors(['Este email já está registrado. Tente fazer login ou use outro email.'])
      } else if (error.message?.includes('Password')) {
        setErrors(['Senha deve ter pelo menos 6 caracteres.'])
      } else if (error.message?.includes('Email')) {
        setErrors(['Email inválido. Verifique o formato.'])
      } else {
        setErrors([error.message || 'Erro ao criar conta. Verifique sua conexão e tente novamente.'])
      }
    } finally {
      setIsLoading(false)
    }
  }

  const passwordStrength = {
    length: formData.password.length >= 6,
    match: formData.password === formData.confirmPassword && formData.confirmPassword.length > 0
  }

  return (
    <div className="w-full">
      <div className="text-center mb-8">
        <h2 className="text-2xl font-bold text-gray-900 mb-2">Crie sua conta grátis</h2>
        <p className="text-gray-600 text-sm">
          Já tem uma conta?{' '}
          <Link href="/login" className="text-red-500 hover:text-red-600 font-medium">
            Faça login
          </Link>
        </p>
      </div>

      <form onSubmit={handleSubmit} className="space-y-6">
        {/* Name Field */}
        <div>
          <label htmlFor="name" className="block text-sm font-semibold text-gray-700 mb-2">
            Nome completo
          </label>
          <div className="relative">
            <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              <User className="h-5 w-5 text-gray-400" />
            </div>
            <input 
              id="name" 
              type="text" 
              value={formData.name} 
              onChange={handleChange} 
              required 
              className="block w-full pl-10 pr-3 py-3 border border-gray-200 rounded-xl shadow-sm focus:outline-none focus:ring-2 focus:ring-red-500 focus:border-red-500 transition-colors bg-gray-50 focus:bg-white"
              placeholder="Seu nome completo"
            />
          </div>
        </div>

        {/* Email Field */}
        <div>
          <label htmlFor="email" className="block text-sm font-semibold text-gray-700 mb-2">
            Email
          </label>
          <div className="relative">
            <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              <Mail className="h-5 w-5 text-gray-400" />
            </div>
            <input 
              id="email" 
              type="email" 
              value={formData.email} 
              onChange={handleChange} 
              required 
              className="block w-full pl-10 pr-3 py-3 border border-gray-200 rounded-xl shadow-sm focus:outline-none focus:ring-2 focus:ring-red-500 focus:border-red-500 transition-colors bg-gray-50 focus:bg-white"
              placeholder="seu@email.com"
            />
          </div>
        </div>

        {/* Password Field */}
        <div>
          <label htmlFor="password" className="block text-sm font-semibold text-gray-700 mb-2">
            Senha
          </label>
          <div className="relative">
            <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              <Lock className="h-5 w-5 text-gray-400" />
            </div>
            <input 
              id="password" 
              type={showPassword ? 'text' : 'password'} 
              value={formData.password} 
              onChange={handleChange} 
              required 
              className="block w-full pl-10 pr-10 py-3 border border-gray-200 rounded-xl shadow-sm focus:outline-none focus:ring-2 focus:ring-red-500 focus:border-red-500 transition-colors bg-gray-50 focus:bg-white"
              placeholder="Crie uma senha segura"
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
          {/* Password strength indicator */}
          {formData.password && (
            <div className="mt-2 flex items-center gap-2 text-xs">
              <div className={`flex items-center gap-1 ${passwordStrength.length ? 'text-green-600' : 'text-gray-400'}`}>
                <Check className="w-3 h-3" />
                <span>Mínimo 6 caracteres</span>
              </div>
            </div>
          )}
        </div>

        {/* Confirm Password Field */}
        <div>
          <label htmlFor="confirmPassword" className="block text-sm font-semibold text-gray-700 mb-2">
            Confirmar senha
          </label>
          <div className="relative">
            <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              <Lock className="h-5 w-5 text-gray-400" />
            </div>
            <input 
              id="confirmPassword" 
              type={showConfirmPassword ? 'text' : 'password'} 
              value={formData.confirmPassword} 
              onChange={handleChange} 
              required 
              className="block w-full pl-10 pr-10 py-3 border border-gray-200 rounded-xl shadow-sm focus:outline-none focus:ring-2 focus:ring-red-500 focus:border-red-500 transition-colors bg-gray-50 focus:bg-white"
              placeholder="Confirme sua senha"
            />
            <button
              type="button"
              className="absolute inset-y-0 right-0 pr-3 flex items-center"
              onClick={() => setShowConfirmPassword(!showConfirmPassword)}
            >
              {showConfirmPassword ? (
                <EyeOff className="h-5 w-5 text-gray-400 hover:text-gray-600" />
              ) : (
                <Eye className="h-5 w-5 text-gray-400 hover:text-gray-600" />
              )}
            </button>
          </div>
          {/* Password match indicator */}
          {formData.confirmPassword && (
            <div className="mt-2 flex items-center gap-2 text-xs">
              <div className={`flex items-center gap-1 ${passwordStrength.match ? 'text-green-600' : 'text-red-500'}`}>
                <Check className="w-3 h-3" />
                <span>{passwordStrength.match ? 'Senhas coincidem' : 'Senhas não coincidem'}</span>
              </div>
            </div>
          )}
        </div>

        {/* Terms */}
        <div className="flex items-start gap-3">
          <input
            id="terms"
            name="terms"
            type="checkbox"
            required
            className="h-4 w-4 text-red-500 focus:ring-red-500 border-gray-300 rounded mt-0.5"
          />
          <label htmlFor="terms" className="text-sm text-gray-700">
            Eu concordo com os{' '}
            <Link href="#" className="text-red-500 hover:text-red-600 font-medium">
              Termos de Uso
            </Link>{' '}
            e{' '}
            <Link href="#" className="text-red-500 hover:text-red-600 font-medium">
              Política de Privacidade
            </Link>
          </label>
        </div>

        {/* Success Message */}
        {successMessage && (
          <div className="p-4 bg-green-50 border border-green-200 rounded-xl">
            <div className="flex items-start">
              <div className="w-6 h-6 bg-green-100 rounded-full flex items-center justify-center mr-3 mt-0.5">
                <span className="text-green-600 text-sm">✅</span>
              </div>
              <div>
                <h4 className="text-green-800 font-medium text-sm mb-1">Sucesso!</h4>
                <p className="text-green-700 text-sm">{successMessage}</p>
              </div>
            </div>
          </div>
        )}

        {/* Error Messages */}
        {errors.length > 0 && (
          <div className="p-4 bg-red-50 border border-red-200 rounded-xl">
            <div className="flex items-start">
              <div className="w-6 h-6 bg-red-100 rounded-full flex items-center justify-center mr-3 mt-0.5">
                <span className="text-red-600 text-sm">⚠️</span>
              </div>
              <div>
                <h4 className="text-red-800 font-medium text-sm mb-1">Corrija os seguintes erros:</h4>
                <ul className="text-red-700 text-sm space-y-1">
                  {errors.map((error, index) => (
                    <li key={index}>• {error}</li>
                  ))}
                </ul>
              </div>
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
              <span>Criando conta...</span>
            </>
          ) : (
            <>
              <span>Criar minha conta grátis</span>
              <ArrowRight className="w-5 h-5" />
            </>
          )}
        </button>
      </form>
    </div>
  )
}