'use client'

import { useState, useEffect } from 'react'
import { useRouter, usePathname } from 'next/navigation'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu'
import {
  Tooltip,
  TooltipContent,
  TooltipProvider,
  TooltipTrigger,
} from '@/components/ui/tooltip'
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar'
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
      {/* Header */}
      <div className="flex items-center justify-between p-4 border-b border-gray-200">
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

        {mobile && (
          <Button
            variant="ghost"
            size="sm"
            onClick={() => setIsMobileOpen(false)}
            className="p-2"
          >
            <span className="text-sm">✕</span>
          </Button>
        )}
      </div>

      {/* Navigation */}
      <div className="flex-1 overflow-y-auto py-4">
        <nav className="space-y-1 px-3">
          {sidebarItems.map((item) => {
            const isActive = pathname === item.href
            
            return (
              <TooltipProvider key={item.id}>
                <Tooltip>
                  <TooltipTrigger asChild>
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
                        <span className="ml-auto bg-blue-100 text-blue-600 text-xs px-2 py-1 rounded-full">
                          {item.badge}
                        </span>
                      )}
                    </Button>
                  </TooltipTrigger>
                  {isCollapsed && !mobile && (
                    <TooltipContent side="right" sideOffset={10}>
                      <p>{item.label}</p>
                    </TooltipContent>
                  )}
                </Tooltip>
              </TooltipProvider>
            )
          })}
        </nav>
      </div>

      {/* User Profile */}
      <div className="border-t border-gray-200 p-3">
        <DropdownMenu>
          <DropdownMenuTrigger asChild>
            <Button
              variant="ghost"
              className={`
                w-full gap-3 h-12 px-3
                ${isCollapsed && !mobile ? 'justify-center px-2' : 'justify-start'}
              `}
            >
              <Avatar className="h-8 w-8 flex-shrink-0">
                <AvatarImage src="/placeholder-avatar.jpg" />
                <AvatarFallback className="bg-gradient-to-r from-blue-600 to-purple-600 text-white text-sm">
                  AS
                </AvatarFallback>
              </Avatar>
              {(!isCollapsed || mobile) && (
                <div className="flex-1 text-left">
                  <div className="text-sm font-medium text-gray-900">Adson Silva</div>
                  <div className="text-xs text-gray-500">Plano Premium</div>
                </div>
              )}
            </Button>
          </DropdownMenuTrigger>
          <DropdownMenuContent 
            align="end" 
            className="w-72 p-0"
            side={isCollapsed && !mobile ? "right" : "top"}
            sideOffset={isCollapsed && !mobile ? 10 : 5}
          >
            {/* Profile Header */}
            <div className="p-4 bg-gradient-to-r from-blue-50 to-purple-50">
              <div className="flex items-center gap-3">
                <Avatar className="h-12 w-12">
                  <AvatarImage src="/placeholder-avatar.jpg" />
                  <AvatarFallback className="bg-gradient-to-r from-blue-600 to-purple-600 text-white">
                    AS
                  </AvatarFallback>
                </Avatar>
                <div>
                  <div className="font-semibold text-gray-900">Adson Silva</div>
                  <div className="text-sm text-gray-600">adson@democratiza.ai</div>
                  <div className="flex items-center gap-1 mt-1">
                    <span className="text-xs bg-gradient-to-r from-blue-600 to-purple-600 text-white px-2 py-1 rounded-full">
                      Premium ⭐
                    </span>
                  </div>
                </div>
              </div>
            </div>

            {/* Stats */}
            <div className="grid grid-cols-3 gap-4 p-4 bg-white border-b border-gray-100">
              <div className="text-center">
                <div className="text-lg font-bold text-blue-600">23</div>
                <div className="text-xs text-gray-500">Análises</div>
              </div>
              <div className="text-center">
                <div className="text-lg font-bold text-green-600">12</div>
                <div className="text-xs text-gray-500">Assinaturas</div>
              </div>
              <div className="text-center">
                <div className="text-lg font-bold text-purple-600">15</div>
                <div className="text-xs text-gray-500">Riscos Evitados</div>
              </div>
            </div>

            {/* Menu Items */}
            <div className="p-2">
              <DropdownMenuItem className="cursor-pointer">
                <span className="mr-2">⚙️</span>
                Configurações
              </DropdownMenuItem>
              <DropdownMenuItem className="cursor-pointer">
                <span className="mr-2">💳</span>
                Gerenciar Plano
              </DropdownMenuItem>
              <DropdownMenuItem className="cursor-pointer">
                <span className="mr-2">❓</span>
                Central de Ajuda
              </DropdownMenuItem>
              <DropdownMenuSeparator />
              <DropdownMenuItem 
                className="cursor-pointer text-red-600 hover:text-red-700 hover:bg-red-50"
                onClick={handleLogout}
              >
                <span className="mr-2">🚪</span>
                Sair da Conta
              </DropdownMenuItem>
            </div>
          </DropdownMenuContent>
        </DropdownMenu>
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

      {/* Mobile Menu Button */}
      {isMobile && (
        <div className="fixed top-4 left-4 z-50 lg:hidden">
          <Button
            variant="outline"
            size="sm"
            onClick={() => setIsMobileOpen(true)}
            className="bg-white shadow-md"
          >
            <span className="text-sm">☰</span>
          </Button>
        </div>
      )}

      {/* Mobile Sidebar Overlay */}
      {isMobile && isMobileOpen && (
        <>
          <div 
            className="fixed inset-0 bg-black bg-opacity-50 z-40 lg:hidden"
            onClick={() => setIsMobileOpen(false)}
          />
          <div className="fixed left-0 top-0 bottom-0 w-80 bg-white z-50 lg:hidden">
            <SidebarContent mobile />
          </div>
        </>
      )}

      {/* Main Content */}
      <div className="flex-1 flex flex-col min-h-screen">
        {/* Header */}
        <header className="bg-white border-b border-gray-200 px-6 py-4">
          <div className="flex items-center justify-between">
            <div className={`${isMobile ? 'ml-12' : ''}`}>
              <h1 className="text-2xl font-bold text-gray-900">
                Visão Geral da Plataforma
              </h1>
              <p className="text-gray-600 mt-1">
                Bem-vindo de volta, Adson! Gerencie seus contratos com segurança.
              </p>
            </div>
            
            <div className="hidden md:flex items-center gap-4">
              <Link href="/plataforma/analise">
                <Button className="bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700">
                  <span className="mr-2">📄</span>
                  Nova Análise
                </Button>
              </Link>
            </div>
          </div>
        </header>

        {/* Page Content */}
        <main className="flex-1 p-6">
          {children}
        </main>
      </div>
    </div>
  )
}