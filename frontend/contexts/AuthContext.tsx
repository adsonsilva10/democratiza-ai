'use client'

import { createContext, useContext, useEffect, useState, useCallback, ReactNode } from 'react'
import { User, Session } from '@supabase/supabase-js'
import { supabase, getCurrentSession, getCurrentUser, onAuthStateChange, signOut as supabaseSignOut } from '@/lib/supabase'
import { SessionTimeoutWarning } from '@/components/auth/SessionTimeoutWarning'

interface AuthContextType {
  user: User | null
  session: Session | null
  loading: boolean
  isAuthenticated: boolean
  signOut: () => Promise<void>
  refreshUser: () => Promise<void>
  resetActivityTimeout: () => void
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

interface AuthProviderProps {
  children: ReactNode
}

// Configurações de timeout (em milissegundos)
const SESSION_TIMEOUT = 2 * 60 * 60 * 1000 // 2 horas
const WARNING_BEFORE_TIMEOUT = 5 * 60 * 1000 // 5 minutos de aviso antes do timeout
const CHECK_INTERVAL = 60 * 1000 // Verificar a cada 1 minuto

export function AuthProvider({ children }: AuthProviderProps) {
  const [user, setUser] = useState<User | null>(null)
  const [session, setSession] = useState<Session | null>(null)
  const [loading, setLoading] = useState(true)
  const [lastActivity, setLastActivity] = useState<number>(Date.now())
  const [showTimeoutWarning, setShowTimeoutWarning] = useState(false)

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

  // Função para resetar o timeout de atividade
  const resetActivityTimeout = useCallback(() => {
    setLastActivity(Date.now())
    setShowTimeoutWarning(false)
  }, [])

  // Função para fazer logout automático
  const autoSignOut = useCallback(async () => {
    console.log('⏰ Sessão expirada por inatividade - fazendo logout automático')
    try {
      await supabaseSignOut()
      setUser(null)
      setSession(null)
      
      localStorage.removeItem('auth-token')
      localStorage.removeItem('user-email')
      localStorage.removeItem('last-activity')
      document.cookie = 'auth-token=; path=/; expires=Thu, 01 Jan 1970 00:00:00 GMT'
      
      window.location.href = '/login?timeout=true'
    } catch (error) {
      console.error('❌ Erro no logout automático:', error)
    }
  }, [])

  // Função para fazer logout
  const signOut = async () => {
    try {
      await supabaseSignOut()
      setUser(null)
      setSession(null)
      
      // Limpar localStorage e cookies
      localStorage.removeItem('auth-token')
      localStorage.removeItem('user-email')
      localStorage.removeItem('last-activity')
      document.cookie = 'auth-token=; path=/; expires=Thu, 01 Jan 1970 00:00:00 GMT'
      
      // Redirecionar para login
      window.location.href = '/login'
    } catch (error) {
      console.error('❌ Erro no logout:', error)
    }
  }

  // Effect para verificar timeout de inatividade
  useEffect(() => {
    if (!isAuthenticated) return

    const checkTimeout = () => {
      const now = Date.now()
      const timeSinceLastActivity = now - lastActivity
      const timeUntilTimeout = SESSION_TIMEOUT - timeSinceLastActivity

      // Se passou do tempo, fazer logout
      if (timeSinceLastActivity >= SESSION_TIMEOUT) {
        autoSignOut()
        return
      }

      // Se está próximo do timeout, mostrar aviso
      if (timeUntilTimeout <= WARNING_BEFORE_TIMEOUT && !showTimeoutWarning) {
        console.log('⚠️ Sessão expirando em breve - mostrando aviso')
        setShowTimeoutWarning(true)
      }
    }

    // Verificar timeout periodicamente
    const intervalId = setInterval(checkTimeout, CHECK_INTERVAL)

    // Verificar imediatamente
    checkTimeout()

    return () => clearInterval(intervalId)
  }, [isAuthenticated, lastActivity, showTimeoutWarning, autoSignOut])

  // Effect para rastrear atividade do usuário
  useEffect(() => {
    if (!isAuthenticated) return

    const handleActivity = () => {
      resetActivityTimeout()
    }

    // Eventos que indicam atividade do usuário
    const events = ['mousedown', 'keydown', 'scroll', 'touchstart', 'click']
    
    events.forEach(event => {
      window.addEventListener(event, handleActivity)
    })

    // Restaurar última atividade do localStorage (caso a página tenha sido recarregada)
    const storedLastActivity = localStorage.getItem('last-activity')
    if (storedLastActivity) {
      const lastActivityTime = parseInt(storedLastActivity, 10)
      if (Date.now() - lastActivityTime < SESSION_TIMEOUT) {
        setLastActivity(lastActivityTime)
      } else {
        // Sessão expirou durante recarga
        autoSignOut()
      }
    }

    return () => {
      events.forEach(event => {
        window.removeEventListener(event, handleActivity)
      })
    }
  }, [isAuthenticated, resetActivityTimeout, autoSignOut])

  // Effect para salvar última atividade no localStorage
  useEffect(() => {
    if (isAuthenticated) {
      localStorage.setItem('last-activity', lastActivity.toString())
    }
  }, [lastActivity, isAuthenticated])

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
        
        // Sincronizar com localStorage e cookies para compatibilidade
        if (session?.user) {
          localStorage.setItem('auth-token', session.access_token)
          localStorage.setItem('user-email', session.user.email || '')
          
          // Salvar também como cookie para o middleware detectar
          document.cookie = `auth-token=${session.access_token}; path=/; max-age=${60 * 60 * 24 * 7}` // 7 dias
        } else {
          localStorage.removeItem('auth-token')
          localStorage.removeItem('user-email')
          
          // Remover cookie também
          document.cookie = 'auth-token=; path=/; expires=Thu, 01 Jan 1970 00:00:00 GMT'
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
    refreshUser,
    resetActivityTimeout
  }

  return (
    <AuthContext.Provider value={value}>
      {children}
      {showTimeoutWarning && isAuthenticated && (
        <SessionTimeoutWarning
          onStayLoggedIn={resetActivityTimeout}
          onLogout={signOut}
          timeRemaining={Math.max(0, SESSION_TIMEOUT - (Date.now() - lastActivity))}
        />
      )}
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