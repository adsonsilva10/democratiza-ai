'use client'

import { useState, useEffect } from 'react'
import { useRouter, usePathname } from 'next/navigation'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import Link from 'next/link'

// Ícones usando emojis para compatibilidade
interface SidebarItem {
  id: string
  label: string
  icon: string
  href: string
  badge?: string
  category?: string
}

const sidebarItems: SidebarItem[] = [
  {
    id: 'dashboard',
    label: 'Visão Geral',
    icon: '🏠',
    href: '/plataforma',
    category: 'main'
  },
  {
    id: 'analise',
    label: 'Nova Análise',
    icon: '📄',
    href: '/plataforma/analise',
    category: 'contracts'
  },
  {
    id: 'historico',
    label: 'Histórico',
    icon: '📋',
    href: '/plataforma/historico',
    category: 'contracts'
  },
  {
    id: 'assinatura',
    label: 'Assinatura Digital',
    icon: '✍️',
    href: '/plataforma/assinatura',
    category: 'tools'
  },
  {
    id: 'chat',
    label: 'Assistente IA',
    icon: '🤖',
    href: '/chat',
    category: 'tools'
  },
  {
    id: 'planos',
    label: 'Planos',
    icon: '💳',
    href: '/plataforma/planos',
    category: 'account'
  },
  {
    id: 'configuracoes',
    label: 'Configurações',
    icon: '⚙️',
    href: '/plataforma/configuracoes',
    category: 'account'
  },
  {
    id: 'suporte',
    label: 'Suporte',
    icon: '❓',
    href: '/plataforma/suporte',
    category: 'account'
  },
  {
    id: 'perfil',
    label: 'Meu Perfil',
    icon: '👤',
    href: '/plataforma/perfil',
    category: 'account'
  }
]

interface CleanSidebarLayoutProps {
  children: React.ReactNode
}

export default function CleanSidebarLayout({ children }: CleanSidebarLayoutProps) {
  const [isCollapsed, setIsCollapsed] = useState(false)
  const [isMobileOpen, setIsMobileOpen] = useState(false)
  const [isMobile, setIsMobile] = useState(false)
  const router = useRouter()
  const pathname = usePathname()

  // Detectar se é mobile
  useEffect(() => {
    const checkIsMobile = () => {
      setIsMobile(window.innerWidth < 1024)
      if (window.innerWidth < 1024) {
        setIsCollapsed(false)
      }
    }

    checkIsMobile()
    window.addEventListener('resize', checkIsMobile)
    return () => window.removeEventListener('resize', checkIsMobile)
  }, [])

  // Auto-colapsar em telas médias (1024-1280px)
  useEffect(() => {
    const handleResize = () => {
      if (window.innerWidth >= 1024 && window.innerWidth < 1280) {
        setIsCollapsed(true)
      } else if (window.innerWidth >= 1280) {
        setIsCollapsed(false)
      }
    }

    handleResize()
    window.addEventListener('resize', handleResize)
    return () => window.removeEventListener('resize', handleResize)
  }, [])

  const handleNavigation = (href: string) => {
    router.push(href)
    if (isMobile) {
      setIsMobileOpen(false)
    }
  }

  const handleLogout = () => {
    // Implementar logout
    router.push('/login')
  }

  // Sidebar Content Component
  const SidebarContent = ({ mobile = false }: { mobile?: boolean }) => (
    <div className="flex flex-col h-full">
      {/* Header com botões de controle no mobile */}
      {mobile && (
        <div className="flex items-center justify-between p-4 border-b border-gray-200">
          {/* Hamburger funcional */}
          <Button
            variant="ghost"
            className="w-10 h-10 p-0 flex items-center justify-center hover:bg-gray-100"
            onClick={() => setIsMobileOpen(false)}
          >
            <span className="text-lg">☰</span>
          </Button>
          
          {/* Botão X para fechar */}
          <Button
            variant="ghost"
            className="w-8 h-8 p-0 flex items-center justify-center hover:bg-gray-100 rounded-full"
            onClick={() => setIsMobileOpen(false)}
          >
            <span className="text-sm font-bold text-gray-600">✕</span>
          </Button>
        </div>
      )}

      {/* Header */}
      <div className={`flex items-center p-4 border-b border-gray-200 ${mobile ? 'justify-center' : 'justify-between'}`}>
        {(!isCollapsed || mobile) && (
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 bg-gradient-to-r from-blue-600 to-purple-600 rounded-lg flex items-center justify-center text-white font-bold text-sm">
              ⚖️
            </div>
            <div>
              <h1 className="font-bold text-gray-900 text-sm">Democratiza AI</h1>
              <p className="text-xs text-gray-500">Contrato Seguro</p>
            </div>
          </div>
        )}
        
        {!mobile && (
          <Button
            variant="ghost"
            size="sm"
            onClick={() => setIsCollapsed(!isCollapsed)}
            className="p-2 hover:bg-gray-100"
          >
            {isCollapsed ? (
              <span className="text-sm">→</span>
            ) : (
              <span className="text-sm">←</span>
            )}
          </Button>
        )}
      </div>      {/* Navigation */}
      <div className="flex-1 overflow-y-auto py-4">
        <nav className="space-y-1 px-3">
          {sidebarItems.map((item) => {
            const isActive = pathname === item.href
            
            return (
              <div key={item.id} className="relative group">
                <Button
                  variant={isActive ? "secondary" : "ghost"}
                  className={`
                    w-full justify-start gap-3 h-10 px-3
                    ${isActive 
                      ? 'bg-gradient-to-r from-blue-50 to-purple-50 text-blue-700 border-l-2 border-blue-600' 
                      : 'text-gray-700 hover:bg-gray-50 hover:text-gray-900'
                    }
                    ${isCollapsed && !mobile ? 'justify-center px-2' : ''}
                  `}
                  onClick={() => handleNavigation(item.href)}
                >
                  <span className={`text-lg flex-shrink-0 ${isActive ? 'filter brightness-75' : ''}`}>
                    {item.icon}
                  </span>
                  {(!isCollapsed || mobile) && (
                    <span className="text-sm font-medium truncate">
                      {item.label}
                    </span>
                  )}
                  {item.badge && (!isCollapsed || mobile) && (
                    <Badge className="ml-auto bg-blue-100 text-blue-600 text-xs">
                      {item.badge}
                    </Badge>
                  )}
                </Button>
                
                {/* Tooltip manual para modo colapsado */}
                {isCollapsed && !mobile && (
                  <div className="absolute left-full top-1/2 transform -translate-y-1/2 ml-2 px-2 py-1 bg-gray-900 text-white text-xs rounded opacity-0 group-hover:opacity-100 transition-opacity duration-200 pointer-events-none whitespace-nowrap z-50">
                    {item.label}
                  </div>
                )}
              </div>
            )
          })}
        </nav>
      </div>

      {/* Avatar Simples - sem funcionalidade complexa */}
      <div className="border-t border-gray-200 p-3">
        <div className="flex items-center gap-3">
          <div className="h-8 w-8 flex-shrink-0 bg-gradient-to-r from-blue-600 to-purple-600 rounded-full flex items-center justify-center text-white text-sm font-bold">
            AS
          </div>
          {(!isCollapsed || mobile) && (
            <div className="flex-1 text-left">
              <div className="text-sm font-medium text-gray-900">Adson Silva</div>
              <div className="text-xs text-gray-500">Premium ⭐</div>
            </div>
          )}
        </div>
      </div>
    </div>
  )

  return (
    <div className="min-h-screen bg-gray-50 flex">
      {/* Desktop Sidebar */}
      {!isMobile && (
        <div className={`
          bg-white border-r border-gray-200 flex-shrink-0 transition-all duration-300
          ${isCollapsed ? 'w-16' : 'w-64'}
        `}>
          <SidebarContent />
        </div>
      )}

      {/* Mobile Sidebar Fixa com Ícones - só aparece quando menu não está aberto */}
      {isMobile && !isMobileOpen && (
        <div className="fixed left-0 top-0 bottom-0 w-16 bg-white border-r border-gray-200 z-30 flex flex-col">
          {/* Menu Hamburger - Primeiro item no topo */}
          <div className="p-2 border-b border-gray-200">
            <Button
              variant="ghost"
              className="w-12 h-12 p-0 flex items-center justify-center hover:bg-gray-100"
              onClick={() => setIsMobileOpen(!isMobileOpen)}
            >
              <span className="text-lg">☰</span>
            </Button>
          </div>

          {/* Logo - Agora em segundo lugar */}
          <div className="flex items-center justify-center p-3 border-b border-gray-200">
            <div className="w-8 h-8 bg-gradient-to-r from-blue-600 to-purple-600 rounded-lg flex items-center justify-center text-white text-sm">
              ⚖️
            </div>
          </div>
          
          {/* Navigation Icons */}
          <div className="flex-1 overflow-y-auto py-2">
            <nav className="space-y-1 px-2">
              {sidebarItems.map((item) => {
                const isActive = pathname === item.href
                return (
                  <Button
                    key={item.id}
                    variant={isActive ? "secondary" : "ghost"}
                    className={`
                      w-12 h-12 p-0 flex items-center justify-center
                      ${isActive 
                        ? 'bg-gradient-to-r from-blue-50 to-purple-50 text-blue-700' 
                        : 'text-gray-700 hover:bg-gray-50'
                      }
                    `}
                    onClick={() => handleNavigation(item.href)}
                  >
                    <span className={`text-lg ${isActive ? 'filter brightness-75' : ''}`}>
                      {item.icon}
                    </span>
                  </Button>
                )
              })}
            </nav>
          </div>

          {/* Avatar Simples - sem dropdown */}
          <div className="border-t border-gray-200 p-2">
            <div className="flex items-center justify-center">
              <div className="h-8 w-8 bg-gradient-to-r from-blue-600 to-purple-600 rounded-full flex items-center justify-center text-white text-xs font-bold">
                AS
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Mobile Sidebar Retrátil - Menu Completo (sobrepõe) */}
      {isMobile && isMobileOpen && (
        <>
          {/* Overlay para fechar clicando fora */}
          <div 
            className="fixed inset-0 bg-black bg-opacity-30 z-35"
            onClick={() => setIsMobileOpen(false)}
          />
          <div className="fixed left-0 top-0 bottom-0 w-80 bg-white border-r border-gray-200 z-40 transform transition-all duration-300 ease-in-out">
            <SidebarContent mobile />
          </div>
        </>
      )}



      {/* Main Content */}
      <div className={`flex-1 flex flex-col min-h-screen ${
        isMobile && !isMobileOpen
          ? 'ml-16' // Apenas menu fixo empurra (64px)
          : '' // Menu completo sobrepõe, desktop sem margin
      }`}>
        {/* Page Content */}
        <main className="flex-1 p-6">
          {children}
        </main>
      </div>
    </div>
  )
}