'use client'

import { useState, useEffect, useRef } from 'react'
import { useRouter, usePathname } from 'next/navigation'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'

interface SidebarItem {
  id: string
  label: string
  icon: string
  href: string
  priority: number // Para determinar ordem de importância
}

const sidebarItems: SidebarItem[] = [
  { id: 'dashboard', label: 'Visão Geral', icon: '🏠', href: '/plataforma', priority: 1 },
  { id: 'analise', label: 'Nova Análise', icon: '📄', href: '/plataforma/analise', priority: 2 },
  { id: 'historico', label: 'Histórico', icon: '📋', href: '/plataforma/historico', priority: 3 },
  { id: 'assinatura', label: 'Assinatura Digital', icon: '✍️', href: '/plataforma/assinatura', priority: 4 },
  { id: 'chat', label: 'Assistente IA', icon: '🤖', href: '/plataforma/chat', priority: 5 },
  { id: 'planos', label: 'Planos', icon: '💳', href: '/plataforma/planos', priority: 6 },
  { id: 'configuracoes', label: 'Configurações', icon: '⚙️', href: '/plataforma/configuracoes', priority: 7 },
  { id: 'suporte', label: 'Suporte', icon: '❓', href: '/plataforma/suporte', priority: 8 }
]

interface AdaptiveSidebarProps {
  children: React.ReactNode
}

export default function CleanSidebarLayoutAdaptive({ children }: AdaptiveSidebarProps) {
  const [isCollapsed, setIsCollapsed] = useState(false)
  const [isMobileOpen, setIsMobileOpen] = useState(false)
  const [isMobile, setIsMobile] = useState(false)
  const [isProfileOpen, setIsProfileOpen] = useState(false)
  const [menuDimensions, setMenuDimensions] = useState({
    itemHeight: 44,
    itemSpacing: 4,
    fontSize: 'text-sm',
    iconSize: 'text-lg',
    compact: false
  })
  
  const sidebarRef = useRef<HTMLDivElement>(null)
  const headerRef = useRef<HTMLDivElement>(null)
  const footerRef = useRef<HTMLDivElement>(null)
  const router = useRouter()
  const pathname = usePathname()

  // Fechar dropdown ao clicar fora
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (isProfileOpen && footerRef.current && !footerRef.current.contains(event.target as Node)) {
        setIsProfileOpen(false)
      }
    }

    document.addEventListener('mousedown', handleClickOutside)
    return () => document.removeEventListener('mousedown', handleClickOutside)
  }, [isProfileOpen])

  // Calcular dimensões adaptativas baseado na altura da tela
  useEffect(() => {
    const calculateAdaptiveDimensions = () => {
      const isMobileView = window.innerWidth < 1024
      setIsMobile(isMobileView)
      
      if (!isMobileView) {
        const viewportHeight = window.innerHeight
        const headerHeight = 80 // Altura estimada do header
        const footerHeight = 80 // Altura estimada do footer
        const padding = 24 // Padding total
        
        const availableHeight = viewportHeight - headerHeight - footerHeight - padding
        const totalItems = sidebarItems.length
        
        // Usar espaçamento padrão fixo - como estava originalmente
        let itemHeight, itemSpacing, fontSize, iconSize, compact
        
        // Espaçamento padrão fixo
        itemHeight = 44
        itemSpacing = 1
        fontSize = 'text-sm'
        iconSize = 'text-lg'
        compact = false
        
        setMenuDimensions({
          itemHeight,
          itemSpacing,
          fontSize,
          iconSize,
          compact
        })
        
        // Auto-collapse baseado na largura
        if (window.innerWidth >= 1024 && window.innerWidth < 1280) {
          setIsCollapsed(true)
        } else if (window.innerWidth >= 1280) {
          setIsCollapsed(false)
        }
      }
    }

    calculateAdaptiveDimensions()
    window.addEventListener('resize', calculateAdaptiveDimensions)
    return () => window.removeEventListener('resize', calculateAdaptiveDimensions)
  }, [])

  const handleNavigation = (href: string) => {
    router.push(href)
    if (isMobile) setIsMobileOpen(false)
  }

  const toggleSidebar = () => {
    if (isMobile) {
      setIsMobileOpen(!isMobileOpen)
    } else {
      setIsCollapsed(!isCollapsed)
    }
  }

  // Desktop Sidebar Component
  const DesktopSidebar = () => (
    <div className={`
      bg-white border-r border-gray-200 flex-shrink-0 transition-all duration-300
      ${isCollapsed ? 'w-16' : 'w-72'}
    `}>
      <div 
        ref={sidebarRef}
        className="flex flex-col h-screen"
      >
        {/* Header Fixo */}
        <div 
          ref={headerRef}
          className={`
            flex items-center justify-between border-b border-gray-100 flex-shrink-0
            ${menuDimensions.compact ? 'p-3' : 'p-4'}
          `}
        >
          {!isCollapsed && (
            <div className="flex items-center gap-3">
              <div className={`
                bg-gradient-to-r from-blue-600 to-purple-600 rounded-xl flex items-center justify-center text-white font-bold
                ${menuDimensions.compact ? 'w-8 h-8 text-sm' : 'w-10 h-10 text-base'}
              `}>
                ⚖️
              </div>
              <div>
                <h1 className={`font-bold text-gray-900 ${menuDimensions.compact ? 'text-base' : 'text-lg'}`}>
                  Democratiza AI
                </h1>
                <p className={`text-gray-500 ${menuDimensions.compact ? 'text-xs' : 'text-sm'}`}>
                  Contrato Seguro
                </p>
              </div>
            </div>
          )}
          
          <Button
            variant="ghost"
            size="sm"
            onClick={toggleSidebar}
            className="p-2 hover:bg-gray-100 rounded-lg"
          >
            {isCollapsed ? '→' : '←'}
          </Button>
        </div>

        {/* Área de Navegação - Mais compacta */}
        <div className="flex-1 py-3">
          <nav className="space-y-1 px-3">
            {sidebarItems.map((item) => {
              const isActive = pathname === item.href
              
              return (
                <div key={item.id} className="relative group">
                  <Button
                    variant={isActive ? "secondary" : "ghost"}
                    className={`
                      w-full transition-all duration-200
                      ${isCollapsed ? 'justify-center px-0' : 'justify-start gap-3 px-3'}
                      ${isActive 
                        ? 'bg-gradient-to-r from-blue-50 to-purple-50 text-blue-700 border-l-2 border-blue-600 shadow-sm' 
                        : 'text-gray-700 hover:bg-gray-50 hover:text-gray-900'
                      }
                    `}
                    style={{ height: `${menuDimensions.itemHeight}px` }}
                    onClick={() => handleNavigation(item.href)}
                  >
                    <span className={`${menuDimensions.iconSize} flex-shrink-0`}>
                      {item.icon}
                    </span>
                    {!isCollapsed && (
                      <span className={`${menuDimensions.fontSize} font-medium truncate flex-1 text-left`}>
                        {item.label}
                      </span>
                    )}
                  </Button>
                  
                  {/* Tooltip Manual para Modo Colapsado */}
                  {isCollapsed && (
                    <div className="absolute left-full top-0 ml-2 opacity-0 group-hover:opacity-100 transition-opacity duration-200 pointer-events-none z-50">
                      <div className="bg-gray-900 text-white text-sm px-3 py-2 rounded-lg shadow-lg whitespace-nowrap">
                        {item.label}
                        <div className="absolute top-1/2 left-0 transform -translate-y-1/2 -translate-x-full">
                          <div className="w-0 h-0 border-t-4 border-b-4 border-r-4 border-transparent border-r-gray-900"></div>
                        </div>
                      </div>
                    </div>
                  )}
                </div>
              )
            })}
            
            {/* Seção do Perfil integrada na navegação */}
            <div className="relative group">
              <Button
                variant="ghost"
                className={`
                  w-full transition-all duration-200 border-t border-gray-200 mt-2 pt-2
                  ${isCollapsed ? 'justify-center px-0' : 'justify-start gap-3 px-3'}
                  text-gray-700 hover:bg-gray-50 hover:text-gray-900
                `}
                style={{ height: `${menuDimensions.itemHeight}px` }}
                onClick={() => setIsProfileOpen(!isProfileOpen)}
              >
                <span className={`${menuDimensions.iconSize} flex-shrink-0`}>
                  <div className="w-6 h-6 bg-gradient-to-r from-blue-600 to-purple-600 rounded-full flex items-center justify-center text-white text-xs font-bold">
                    AS
                  </div>
                </span>
                {!isCollapsed && (
                  <>
                    <span className={`${menuDimensions.fontSize} font-medium truncate flex-1 text-left`}>
                      Adson Silva
                    </span>
                    <span className={`text-gray-400 transition-transform ${isProfileOpen ? 'rotate-180' : ''}`}>
                      ▼
                    </span>
                  </>
                )}
              </Button>
              
              {/* Tooltip para modo colapsado */}
              {isCollapsed && (
                <div className="absolute left-full top-0 ml-2 opacity-0 group-hover:opacity-100 transition-opacity duration-200 pointer-events-none z-50">
                  <div className="bg-gray-900 text-white text-sm px-3 py-2 rounded-lg shadow-lg whitespace-nowrap">
                    Adson Silva (Premium)
                    <div className="absolute top-1/2 left-0 transform -translate-y-1/2 -translate-x-full">
                      <div className="w-0 h-0 border-t-4 border-b-4 border-r-4 border-transparent border-r-gray-900"></div>
                    </div>
                  </div>
                </div>
              )}
              
              {/* Dropdown do Perfil na navegação */}
              {isProfileOpen && (
                <div className={`
                  ${isCollapsed ? 'absolute left-full top-0 ml-2 w-64' : 'mt-1'}
                  bg-white border border-gray-200 rounded-lg shadow-xl z-50
                `}>
                  <div className="p-3">
                    {!isCollapsed && (
                      <div className="flex items-center gap-3 pb-3 border-b border-gray-100">
                        <div className="w-10 h-10 bg-gradient-to-r from-blue-600 to-purple-600 rounded-full flex items-center justify-center text-white font-semibold text-sm">
                          AS
                        </div>
                        <div>
                          <div className="font-semibold text-gray-900 text-sm">Adson Silva</div>
                          <div className="text-xs text-gray-500">adson@email.com</div>
                          <div className="mt-1">
                            <Badge className="bg-gradient-to-r from-blue-600 to-purple-600 text-white text-xs">
                              Premium ⭐
                            </Badge>
                          </div>
                        </div>
                      </div>
                    )}
                    
                    <div className={`space-y-1 ${!isCollapsed ? 'mt-3' : ''}`}>
                      <Button
                        variant="ghost"
                        className="w-full justify-start text-sm h-9"
                        onClick={() => {
                          handleNavigation('/plataforma/perfil')
                          setIsProfileOpen(false)
                        }}
                      >
                        👤 Meu Perfil
                      </Button>
                      <Button
                        variant="ghost"
                        className="w-full justify-start text-sm h-9"
                        onClick={() => {
                          handleNavigation('/plataforma/configuracoes')
                          setIsProfileOpen(false)
                        }}
                      >
                        ⚙️ Configurações
                      </Button>
                      <Button
                        variant="ghost"
                        className="w-full justify-start text-sm h-9"
                        onClick={() => {
                          handleNavigation('/plataforma/planos')
                          setIsProfileOpen(false)
                        }}
                      >
                        💳 Planos
                      </Button>
                      <div className="border-t border-gray-100 my-2"></div>
                      <Button
                        variant="ghost"
                        className="w-full justify-start text-sm h-9 text-red-600 hover:text-red-700 hover:bg-red-50"
                        onClick={() => {
                          router.push('/login')
                          setIsProfileOpen(false)
                        }}
                      >
                        🚪 Sair
                      </Button>
                    </div>
                  </div>
                </div>
              )}
            </div>
          </nav>
        </div>
        

      </div>
    </div>
  )

  // Mobile Components - Menu Lateral Corrigido
  const MobileSidebar = () => (
    <>
      {/* Barra Fixa Mobile - só aparece quando menu não está aberto */}
      {!isMobileOpen && (
        <div className="fixed left-0 top-0 bottom-0 w-16 bg-white border-r border-gray-200 z-30 flex flex-col">
          {/* Hamburger Menu */}
          <div className="p-2 border-b border-gray-200">
            <Button
              variant="ghost"
              className="w-12 h-12 p-0 flex items-center justify-center hover:bg-gray-100"
              onClick={() => setIsMobileOpen(true)}
            >
              <span className="text-lg">☰</span>
            </Button>
          </div>

          {/* Logo */}
          <div className="flex items-center justify-center p-3 border-b border-gray-200">
            <div className="w-8 h-8 bg-gradient-to-r from-blue-600 to-purple-600 rounded-lg flex items-center justify-center text-white text-sm">
              ⚖️
            </div>
          </div>

          {/* Ícones de Navegação */}
          <div className="flex-1 py-2">
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

          {/* Avatar do Perfil na Barra Fixa */}
          <div className="mt-auto p-2 border-t border-gray-200 relative">
            <Button
              variant="ghost"
              className="w-12 h-12 p-0 flex items-center justify-center hover:bg-gray-100"
              onClick={() => setIsProfileOpen(!isProfileOpen)}
            >
              <div className="w-8 h-8 bg-gradient-to-r from-blue-600 to-purple-600 rounded-full flex items-center justify-center text-white text-xs font-bold">
                AS
              </div>
            </Button>

            {/* Dropup do Avatar Mobile Barra Fixa */}
            {isProfileOpen && (
              <>
                {/* Overlay para fechar */}
                <div 
                  className="fixed inset-0 bg-black bg-opacity-30 z-[55]"
                  onClick={() => setIsProfileOpen(false)}
                />
                {/* Dropup - Menu que abre PARA CIMA */}
                <div 
                  className="fixed left-16 w-64 bg-white border border-gray-200 rounded-lg shadow-xl z-[60]"
                  style={{ 
                    bottom: 'calc(100vh - (100vh - 80px))', // 80px do bottom da tela
                    transform: 'translateY(-100%)' // Move 100% para cima
                  }}
                >
                  <div className="p-3">
                    <div className="flex items-center gap-3 pb-3 border-b border-gray-100">
                      <div className="w-10 h-10 bg-gradient-to-r from-blue-600 to-purple-600 rounded-full flex items-center justify-center text-white font-semibold text-sm">
                        AS
                      </div>
                      <div>
                        <div className="font-semibold text-gray-900 text-sm">Adson Silva</div>
                        <div className="text-xs text-gray-500">adson@email.com</div>
                        <div className="mt-1">
                          <Badge className="bg-gradient-to-r from-blue-600 to-purple-600 text-white text-xs">
                            Premium ⭐
                          </Badge>
                        </div>
                      </div>
                    </div>
                    
                    <div className="mt-3 space-y-1">
                      <Button
                        variant="ghost"
                        className="w-full justify-start text-sm h-9"
                        onClick={() => {
                          handleNavigation('/plataforma/perfil')
                          setIsProfileOpen(false)
                        }}
                      >
                        👤 Meu Perfil
                      </Button>
                      <Button
                        variant="ghost"
                        className="w-full justify-start text-sm h-9"
                        onClick={() => {
                          handleNavigation('/plataforma/configuracoes')
                          setIsProfileOpen(false)
                        }}
                      >
                        ⚙️ Configurações
                      </Button>
                      <Button
                        variant="ghost"
                        className="w-full justify-start text-sm h-9"
                        onClick={() => {
                          handleNavigation('/plataforma/planos')
                          setIsProfileOpen(false)
                        }}
                      >
                        💳 Planos
                      </Button>
                      <div className="border-t border-gray-100 my-2"></div>
                      <Button
                        variant="ghost"
                        className="w-full justify-start text-sm h-9 text-red-600 hover:text-red-700 hover:bg-red-50"
                        onClick={() => {
                          router.push('/login')
                          setIsProfileOpen(false)
                        }}
                      >
                        🚪 Sair
                      </Button>
                    </div>
                  </div>
                </div>
              </>
            )}
          </div>

        </div>
      )}

      {/* Menu Completo Mobile Lateral - sobrepõe tudo */}
      {isMobileOpen && (
        <>
          {/* Overlay para fechar clicando fora */}
          <div 
            className="fixed inset-0 bg-black bg-opacity-30 z-35"
            onClick={() => setIsMobileOpen(false)}
          />
          <div className="fixed left-0 top-0 bottom-0 w-80 bg-white border-r border-gray-200 z-40 transform transition-all duration-300 ease-in-out">
            <div className="flex flex-col h-full">
              {/* Header com controles */}
              <div className="flex items-center justify-between p-4 border-b border-gray-200">
                {/* Hamburger funcional */}
                <Button
                  variant="ghost"
                  className="w-10 h-10 p-0 flex items-center justify-center hover:bg-gray-100"
                  onClick={() => setIsMobileOpen(false)}
                >
                  <span className="text-lg">☰</span>
                </Button>
                
                {/* Logo e título */}
                <div className="flex items-center gap-3">
                  <div className="w-8 h-8 bg-gradient-to-r from-blue-600 to-purple-600 rounded-lg flex items-center justify-center text-white font-bold text-sm">
                    ⚖️
                  </div>
                  <div>
                    <h1 className="font-bold text-gray-900 text-sm">Democratiza AI</h1>
                    <p className="text-xs text-gray-500">Contrato Seguro</p>
                  </div>
                </div>
                
                {/* Botão X para fechar */}
                <Button
                  variant="ghost"
                  className="w-8 h-8 p-0 flex items-center justify-center hover:bg-gray-100 rounded-full"
                  onClick={() => setIsMobileOpen(false)}
                >
                  <span className="text-sm font-bold text-gray-600">✕</span>
                </Button>
              </div>

              {/* Navegação */}
              <div className="flex-1 py-4">
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
                          `}
                          onClick={() => handleNavigation(item.href)}
                        >
                          <span className={`text-lg flex-shrink-0 ${isActive ? 'filter brightness-75' : ''}`}>
                            {item.icon}
                          </span>
                          <span className="text-sm font-medium truncate">
                            {item.label}
                          </span>
                        </Button>
                      </div>
                    )
                  })}
                  
                  
                  {/* Seção do Perfil integrada no mobile - após Suporte */}
                  <div className="border-t border-gray-200 mt-4 pt-4">
                    <Button
                      variant="ghost"
                      className="w-full justify-start gap-3 h-10 px-3 text-gray-700 hover:bg-gray-50 hover:text-gray-900"
                      onClick={() => setIsProfileOpen(!isProfileOpen)}
                    >
                      <span className="text-lg flex-shrink-0">
                        <div className="w-6 h-6 bg-gradient-to-r from-blue-600 to-purple-600 rounded-full flex items-center justify-center text-white text-xs font-bold">
                          AS
                        </div>
                      </span>
                      <span className="text-sm font-medium truncate flex-1 text-left">
                        Adson Silva
                      </span>
                      <span className={`text-gray-400 transition-transform ${isProfileOpen ? 'rotate-180' : ''}`}>
                        ▼
                      </span>
                    </Button>
                    
                    {/* Dropdown Mobile Menu Completo */}
                    {isProfileOpen && (
                      <div className="mt-2 bg-gray-50 border border-gray-200 rounded-lg">
                        <div className="p-3">
                          <div className="flex items-center gap-3 pb-3 border-b border-gray-200">
                            <div className="w-10 h-10 bg-gradient-to-r from-blue-600 to-purple-600 rounded-full flex items-center justify-center text-white font-semibold text-sm">
                              AS
                            </div>
                            <div>
                              <div className="font-semibold text-gray-900 text-sm">Adson Silva</div>
                              <div className="text-xs text-gray-500">adson@email.com</div>
                              <div className="mt-1">
                                <Badge className="bg-gradient-to-r from-blue-600 to-purple-600 text-white text-xs">
                                  Premium ⭐
                                </Badge>
                              </div>
                            </div>
                          </div>
                          
                          <div className="mt-3 space-y-1">
                            <Button
                              variant="ghost"
                              className="w-full justify-start text-sm h-9"
                              onClick={() => {
                                handleNavigation('/plataforma/perfil')
                                setIsProfileOpen(false)
                                setIsMobileOpen(false)
                              }}
                            >
                              👤 Meu Perfil
                            </Button>
                            <Button
                              variant="ghost"
                              className="w-full justify-start text-sm h-9"
                              onClick={() => {
                                handleNavigation('/plataforma/configuracoes')
                                setIsProfileOpen(false)
                                setIsMobileOpen(false)
                              }}
                            >
                              ⚙️ Configurações
                            </Button>
                            <Button
                              variant="ghost"
                              className="w-full justify-start text-sm h-9"
                              onClick={() => {
                                handleNavigation('/plataforma/planos')
                                setIsProfileOpen(false)
                                setIsMobileOpen(false)
                              }}
                            >
                              💳 Planos
                            </Button>
                            <div className="border-t border-gray-100 my-2"></div>
                            <Button
                              variant="ghost"
                              className="w-full justify-start text-sm h-9 text-red-600 hover:text-red-700 hover:bg-red-50"
                              onClick={() => {
                                router.push('/login')
                                setIsProfileOpen(false)
                                setIsMobileOpen(false)
                              }}
                            >
                              🚪 Sair
                            </Button>
                          </div>
                        </div>
                      </div>
                    )}
                  </div>
                </nav>
              </div>


            </div>
          </div>
        </>
      )}
    </>
  )

  return (
    <div className="min-h-screen bg-gray-50 flex">
      {/* Sidebar */}
      {isMobile ? <MobileSidebar /> : <DesktopSidebar />}

      {/* Main Content */}
      <div className={`flex-1 flex flex-col ${isMobile ? 'ml-16' : ''}`}>
        {/* Page Content */}
        <main className="flex-1 p-6">
          {children}
        </main>
      </div>
    </div>
  )
}