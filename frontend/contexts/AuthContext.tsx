'use client'

import { createContext, useContext, useEffect, useState, ReactNode } from 'react'
import { User, Session } from '@supabase/supabase-js'
import { supabase, getCurrentSession, getCurrentUser, onAuthStateChange, signOut as supabaseSignOut } from '@/lib/supabase'

interface AuthContextType {
  user: User | null
  session: Session | null
  loading: boolean
  isAuthenticated: boolean
  signOut: () => Promise<void>
  refreshUser: () => Promise<void>
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

interface AuthProviderProps {
  children: ReactNode
}

export function AuthProvider({ children }: AuthProviderProps) {
  const [user, setUser] = useState<User | null>(null)
  const [session, setSession] = useState<Session | null>(null)
  const [loading, setLoading] = useState(true)

  const isAuthenticated = !!user && !!session

  // Função para atualizar dados do usuário
  const refreshUser = async () => {
    try {
      const currentUser = await getCurrentUser()
      const currentSession = await getCurrentSession()
      
      setUser(currentUser)
      setSession(currentSession)
    } catch (error) {
      console.error('❌ Erro ao atualizar usuário:', error)
      setUser(null)
      setSession(null)
    }
  }

  // Função para fazer logout
  const signOut = async () => {
    try {
      await supabaseSignOut()
      setUser(null)
      setSession(null)
      
      // Redirecionar para login
      window.location.href = '/login'
    } catch (error) {
      console.error('❌ Erro no logout:', error)
    }
  }

  useEffect(() => {
    let mounted = true

    // Função para inicializar autenticação
    const initializeAuth = async () => {
      try {
        console.log('🔄 Inicializando autenticação...')
        
        const currentSession = await getCurrentSession()
        const currentUser = await getCurrentUser()

        if (mounted) {
          setSession(currentSession)
          setUser(currentUser)
          
          console.log('✅ Auth inicializada:', {
            user: currentUser?.email,
            authenticated: !!currentUser
          })
        }
      } catch (error) {
        console.error('❌ Erro na inicialização da auth:', error)
        if (mounted) {
          setUser(null)
          setSession(null)
        }
      } finally {
        if (mounted) {
          setLoading(false)
        }
      }
    }

    // Inicializar
    initializeAuth()

    // Listener para mudanças no estado de autenticação
    const { data: { subscription } } = onAuthStateChange((event, session) => {
      if (mounted) {
        console.log('🔄 Auth state changed:', event, session?.user?.email)
        
        setSession(session)
        setUser(session?.user || null)
        
        // Sincronizar com localStorage para compatibilidade
        if (session?.user) {
          localStorage.setItem('auth-token', session.access_token)
          localStorage.setItem('user-email', session.user.email || '')
        } else {
          localStorage.removeItem('auth-token')
          localStorage.removeItem('user-email')
        }
        
        setLoading(false)
      }
    })

    // Cleanup
    return () => {
      mounted = false
      subscription?.unsubscribe()
    }
  }, [])

  const value: AuthContextType = {
    user,
    session,
    loading,
    isAuthenticated,
    signOut,
    refreshUser
  }

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  )
}

// Hook para usar o contexto de autenticação
export function useAuth(): AuthContextType {
  const context = useContext(AuthContext)
  
  if (context === undefined) {
    throw new Error('useAuth deve ser usado dentro de um AuthProvider')
  }
  
  return context
}

// Hook para verificar se usuário está logado
export function useAuthRequired(): AuthContextType {
  const auth = useAuth()
  
  useEffect(() => {
    if (!auth.loading && !auth.isAuthenticated) {
      console.log('❌ Usuário não autenticado - redirecionando para login')
      window.location.href = '/login'
    }
  }, [auth.loading, auth.isAuthenticated])
  
  return auth
}