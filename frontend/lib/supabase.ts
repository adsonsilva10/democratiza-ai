// lib/supabase.ts
import { createClient } from '@supabase/supabase-js'
import type { Database } from '@/types/supabase'

// Configuração do Supabase seguindo as Democratiza AI Copilot Instructions
const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL || 'https://brrehdlpiimawxiiswzq.supabase.co'
const supabaseAnonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY || 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImJycmVoZGxwaWltYXd4aWlzd3pxIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTkzNDUwMzAsImV4cCI6MjA3NDkyMTAzMH0.YBxqUB9AXUWq1dptUWgGBB4nIvDLES50Vs8l8A4o_4E'

export const supabase = createClient(supabaseUrl, supabaseAnonKey, {
  auth: {
    autoRefreshToken: true,
    persistSession: true,
    detectSessionInUrl: true,
    flowType: 'pkce'
  },
  // Configuração para desenvolvimento - desabilita confirmação de email
  global: {
    headers: {
      'apikey': supabaseAnonKey
    }
  }
})

// Função para login social com Google
export const signInWithGoogle = async () => {
  try {
    console.log('🔗 Iniciando login com Google...')
    
    const { data, error } = await supabase.auth.signInWithOAuth({
      provider: 'google',
      options: {
        redirectTo: `${window.location.origin}/auth/callback`,
        queryParams: {
          access_type: 'offline',
          prompt: 'consent',
        },
      },
    })

    if (error) {
      console.error('❌ Erro no login com Google:', error.message)
      throw new Error(`Erro no login: ${error.message}`)
    }

    console.log('✅ Redirecionamento para Google iniciado')
    return data
    
  } catch (error) {
    console.error('❌ Falha no login social:', error)
    throw error
  }
}

// Função para login com email/senha (com suporte a desenvolvimento)
export const signInWithEmail = async (email: string, password: string) => {
  try {
    console.log('🔐 Fazendo login com email:', email)
    
    const { data, error } = await supabase.auth.signInWithPassword({
      email,
      password,
    })

    // Em desenvolvimento, se erro for "email not confirmed", dar mensagem mais clara
    if (error && error.message.includes('Email not confirmed')) {
      if (process.env.NODE_ENV === 'development' || window.location.hostname === 'localhost') {
        console.log('🔧 Modo desenvolvimento: email não confirmado')
        throw new Error('Conta criada com sucesso! Para desenvolvimento, acesse o painel do Supabase e confirme o usuário manualmente, ou configure SMTP.')
      }
    }

    if (error) {
      console.error('❌ Erro no login:', error.message)
      throw new Error(error.message)
    }

    console.log('✅ Login realizado com sucesso')
    return data
    
  } catch (error) {
    console.error('❌ Falha no login:', error)
    throw error
  }
}

// Função para registro com email/senha (otimizada para desenvolvimento)
export const signUpWithEmail = async (email: string, password: string, fullName: string) => {
  try {
    console.log('👤 Registrando usuário:', email)
    
    const { data, error } = await supabase.auth.signUp({
      email,
      password,
      options: {
        data: {
          full_name: fullName,
        },
        // Para desenvolvimento: desabilitar confirmação de email
        emailRedirectTo: undefined
      }
    })

    if (error) {
      console.error('❌ Erro no registro:', error.message)
      throw new Error(error.message)
    }

    console.log('✅ Registro realizado com sucesso')
    
    // Em desenvolvimento, retornar dados que simulam usuário confirmado
    if (process.env.NODE_ENV === 'development' || window.location.hostname === 'localhost') {
      console.log('🔧 Modo desenvolvimento: simulando confirmação automática')
      return {
        ...data,
        user: data.user ? {
          ...data.user,
          email_confirmed_at: new Date().toISOString(), // Simular confirmação
          user_metadata: {
            ...data.user.user_metadata,
            email_verified: true
          }
        } : null
      }
    }
    
    return data
    
  } catch (error) {
    console.error('❌ Falha no registro:', error)
    throw error
  }
}

// Função para logout
export const signOut = async () => {
  try {
    console.log('🚪 Fazendo logout...')
    
    const { error } = await supabase.auth.signOut()
    
    if (error) {
      console.error('❌ Erro no logout:', error.message)
      throw new Error(error.message)
    }

    // Limpar storage local
    if (typeof window !== 'undefined') {
      localStorage.removeItem('auth-token')
      localStorage.removeItem('user-email')
    }

    console.log('✅ Logout realizado com sucesso')
    
  } catch (error) {
    console.error('❌ Falha no logout:', error)
    throw error
  }
}

// Função para obter sessão atual
export const getCurrentSession = async () => {
  try {
    const { data: { session }, error } = await supabase.auth.getSession()
    
    if (error) {
      console.error('❌ Erro ao obter sessão:', error.message)
      return null
    }
    
    return session
    
  } catch (error) {
    console.error('❌ Falha ao obter sessão:', error)
    return null
  }
}

// Função para obter usuário atual
export const getCurrentUser = async () => {
  try {
    const { data: { user }, error } = await supabase.auth.getUser()
    
    if (error) {
      console.error('❌ Erro ao obter usuário:', error.message)
      return null
    }
    
    return user
    
  } catch (error) {
    console.error('❌ Falha ao obter usuário:', error)
    return null
  }
}

// Listener para mudanças no estado de autenticação
export const onAuthStateChange = (callback: (event: string, session: any) => void) => {
  return supabase.auth.onAuthStateChange((event, session) => {
    console.log('🔄 Estado de auth mudou:', event, session?.user?.email)
    callback(event, session)
  })
}