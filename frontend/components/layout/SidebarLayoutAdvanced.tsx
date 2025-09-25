'use client'

import Link from 'next/link'
import { useState, ReactNode, useEffect, useCallback } from 'react'

interface SidebarLayoutProps {
  children: ReactNode
  currentPage?: string
}

export default function SidebarLayoutAdvanced({ children, currentPage }: SidebarLayoutProps) {
  // Estados simplificados para evitar loops
  const [sidebarOpen, setSidebarOpen] = useState(false)
  const [isLargeScreen, setIsLargeScreen] = useState(false)
  const [mounted, setMounted] = useState(false)
  const [userClosedSidebar, setUserClosedSidebar] = useState(false)

  // Callback estável para verificar tamanho da tela
  const checkScreenSize = useCallback(() => {
    const isLarge = window.innerWidth >= 1024
    setIsLargeScreen(isLarge)
    
    // Desktop: aberto por padrão, mobile: fechado
    if (isLarge) {
      setSidebarOpen(!userClosedSidebar)
    } else {
      setSidebarOpen(false)
      // Reset userClosedSidebar apenas quando sai do desktop
      if (userClosedSidebar) {
        setUserClosedSidebar(false)
      }
    }
  }, [userClosedSidebar]) // Dependência estável

  // useEffect apenas para setup inicial
  useEffect(() => {
    setMounted(true)
    checkScreenSize()
    
    window.addEventListener('resize', checkScreenSize)
    return () => window.removeEventListener('resize', checkScreenSize)
  }, [checkScreenSize])

  // Handlers de toggle
  const handleSidebarToggle = useCallback((e: React.MouseEvent | React.TouchEvent) => {
    e.preventDefault()
    e.stopPropagation()
    
    if (isLargeScreen) {
      // Desktop: controla estado de "fechado pelo usuário"
      setUserClosedSidebar(prev => !prev)
    } else {
      // Mobile: toggle direto
      setSidebarOpen(prev => !prev)
    }
  }, [isLargeScreen])

  const closeSidebar = useCallback(() => {
    if (isLargeScreen) {
      setUserClosedSidebar(true)
    } else {
      setSidebarOpen(false)
    }
  }, [isLargeScreen])

  // Previne problemas de hidratação
  if (!mounted) {
    return (
      <div className="min-h-screen bg-gray-50">
        <div className="p-4 sm:p-6">
          {children}
        </div>
      </div>
    )
  }

  const menuItems = [
    { 
      icon: (
        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" />
        </svg>
      ), 
      label: 'Home', 
      href: '/dashboard', 
      id: 'home' 
    },
    { 
      icon: (
        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
        </svg>
      ), 
      label: 'Análise', 
      href: '/dashboard/analise', 
      id: 'analise' 
    },
    { 
      icon: (
        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
      ), 
      label: 'Histórico', 
      href: '/dashboard/historico', 
      id: 'historico' 
    },
    { 
      icon: (
        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
        </svg>
      ), 
      label: 'Chat IA', 
      href: '/dashboard/chat', 
      id: 'chat' 
    },
    { 
      icon: (
        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
        </svg>
      ), 
      label: 'Configurações', 
      href: '/dashboard/configuracoes', 
      id: 'configuracoes' 
    },
    { 
      icon: (
        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3 0 1.4-1.278 2.575-3.006 2.907-.542.104-.994.54-.994 1.093m0 3h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
      ), 
      label: 'Ajuda e Suporte', 
      href: '/dashboard/suporte', 
      id: 'suporte' 
    },
  ]

  // Determina se o sidebar deve estar visível
  const sidebarVisible = isLargeScreen ? !userClosedSidebar : sidebarOpen

  return (
    <div className="min-h-screen bg-gray-50 w-full overflow-x-hidden">
      {/* Sidebar Principal */}
      <div className={`fixed inset-y-0 left-0 z-30 bg-gradient-to-b from-blue-900 to-purple-900 transition-all duration-300 ease-in-out shadow-lg
        ${sidebarVisible ? 'w-64 translate-x-0' : 'w-0 -translate-x-full'}
      `}>
        <div className={`h-full flex flex-col ${sidebarVisible ? 'opacity-100' : 'opacity-0 pointer-events-none'} transition-opacity duration-300`}>
          {/* Sidebar Header */}
          <div className="flex items-center justify-between p-4 border-b border-white/10 flex-shrink-0">
            <div className="text-white font-bold text-lg truncate">
              Democratiza AI
            </div>
            <button
              onClick={closeSidebar}
              className="text-white hover:bg-white/10 p-2 rounded-lg transition-colors flex-shrink-0"
              title={isLargeScreen ? "Fechar sidebar" : "Fechar menu"}
            >
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>

          {/* Menu Items */}
          <nav className="mt-8 px-2 flex-1 overflow-y-auto">
            {menuItems.map((item, index) => (
              <Link
                key={index}
                href={item.href}
                className={`flex items-center px-3 py-3 mb-2 text-white rounded-lg transition-all duration-200 group relative ${
                  currentPage === item.id 
                    ? 'bg-white/20 shadow-lg' 
                    : 'hover:bg-white/10 hover:shadow-md'
                }`}
              >
                <div className="flex-shrink-0 w-5 h-5 flex items-center justify-center">
                  {item.icon}
                </div>
                <span className="ml-3 text-sm font-medium truncate">{item.label}</span>
                {currentPage === item.id && (
                  <div className="absolute right-2 w-2 h-2 bg-green-400 rounded-full flex-shrink-0 animate-pulse"></div>
                )}
              </Link>
            ))}
          </nav>

          {/* User Section */}
          <div className="absolute bottom-20 left-0 right-0 px-2">
            <div className="flex items-center px-3 py-3 text-white justify-start bg-white/5 rounded-lg backdrop-blur-sm">
              <div className="w-8 h-8 bg-gradient-to-r from-green-400 to-blue-400 rounded-full flex items-center justify-center text-sm font-bold flex-shrink-0 shadow-lg">
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                </svg>
              </div>
              <div className="ml-3 min-w-0 flex-1">
                <div className="text-sm font-medium truncate">Usuário</div>
                <div className="text-xs text-gray-300 truncate flex items-center">
                  <div className="w-2 h-2 bg-green-400 rounded-full mr-1 animate-pulse"></div>
                  Plano Free
                </div>
              </div>
            </div>
          </div>

          {/* Logout Button */}
          <div className="absolute bottom-4 left-0 right-0 px-2">
            <Link
              href="/login"
              className="flex items-center justify-center px-3 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-all duration-200 hover:shadow-lg"
            >
              <svg className="w-4 h-4 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
              </svg>
              <span className="ml-2 text-sm truncate">Sair</span>
            </Link>
          </div>
        </div>
      </div>

      {/* Overlay para mobile quando sidebar aberto */}
      {!isLargeScreen && sidebarOpen && (
        <div 
          className="fixed inset-0 bg-black bg-opacity-50 z-20"
          onClick={closeSidebar}
        />
      )}

      {/* Mobile Navigation Bar - aparece quando sidebar está fechado no mobile */}
      {!isLargeScreen && !sidebarOpen && (
        <div className="fixed left-0 top-0 bottom-0 w-16 bg-gradient-to-b from-blue-900 to-purple-900 z-30 flex flex-col shadow-lg">
          {/* Hamburger button no topo */}
          <button
            onClick={handleSidebarToggle}
            className="flex items-center justify-center h-16 text-white hover:bg-white/10 transition-colors"
            title="Abrir menu completo"
          >
            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
            </svg>
          </button>

          {/* Ícones dos menu items principais */}
          <nav className="flex-1 flex flex-col items-center py-4 space-y-2">
            {menuItems.slice(0, 4).map((item, index) => (
              <Link
                key={index}
                href={item.href}
                className={`w-12 h-12 flex items-center justify-center rounded-lg transition-all duration-200 relative ${
                  currentPage === item.id 
                    ? 'bg-white/20 text-white shadow-lg' 
                    : 'text-white/70 hover:bg-white/10 hover:text-white'
                }`}
                title={item.label}
              >
                <div className="w-5 h-5">
                  {item.icon}
                </div>
                {currentPage === item.id && (
                  <div className="absolute -right-1 top-1/2 transform -translate-y-1/2 w-1 h-6 bg-green-400 rounded-full"></div>
                )}
              </Link>
            ))}
          </nav>

          {/* Ícones inferiores: Configurações, Suporte, Usuário, Logout */}
          <div className="flex flex-col items-center space-y-2 p-2">
            {/* Configurações */}
            <Link
              href="/dashboard/configuracoes"
              className={`w-12 h-12 flex items-center justify-center rounded-lg transition-all duration-200 relative ${
                currentPage === 'configuracoes' 
                  ? 'bg-white/20 text-white shadow-lg' 
                  : 'text-white/70 hover:bg-white/10 hover:text-white'
              }`}
              title="Configurações"
            >
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
              </svg>
              {currentPage === 'configuracoes' && (
                <div className="absolute -right-1 top-1/2 transform -translate-y-1/2 w-1 h-6 bg-green-400 rounded-full"></div>
              )}
            </Link>

            {/* Ajuda e Suporte */}
            <Link
              href="/dashboard/suporte"
              className={`w-12 h-12 flex items-center justify-center rounded-lg transition-all duration-200 relative ${
                currentPage === 'suporte' 
                  ? 'bg-white/20 text-white shadow-lg' 
                  : 'text-white/70 hover:bg-white/10 hover:text-white'
              }`}
              title="Ajuda e Suporte"
            >
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3 0 1.4-1.278 2.575-3.006 2.907-.542.104-.994.54-.994 1.093m0 3h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              {currentPage === 'suporte' && (
                <div className="absolute -right-1 top-1/2 transform -translate-y-1/2 w-1 h-6 bg-green-400 rounded-full"></div>
              )}
            </Link>

            {/* Indicador de usuário */}
            <div className="w-8 h-8 bg-gradient-to-r from-green-400 to-blue-400 rounded-full flex items-center justify-center mt-2">
              <svg className="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
              </svg>
            </div>

            {/* Logout */}
            <Link
              href="/login"
              className="w-12 h-12 flex items-center justify-center rounded-lg transition-all duration-200 text-red-400 hover:bg-red-600/10 hover:text-red-300"
              title="Sair"
            >
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
              </svg>
            </Link>
          </div>
        </div>
      )}

      {/* Main Content */}
      <div className={`transition-all duration-300 min-h-screen ${
        isLargeScreen 
          ? (sidebarVisible ? 'ml-64' : 'ml-0') 
          : (sidebarOpen ? 'ml-0' : 'ml-16')
      }`}>
        {/* Top Bar */}
        <div className="bg-white border-b border-gray-200 px-4 sm:px-6 py-4 relative z-10">
          <div className="flex items-center justify-between w-full min-w-0">
            <div className="flex items-center min-w-0 flex-1">
              {/* Botão para expandir quando fechado - APENAS DESKTOP */}
              {(isLargeScreen && !sidebarVisible) && (
                <button
                  onClick={handleSidebarToggle}
                  className="mr-4 p-3 rounded-lg text-gray-500 hover:text-gray-700 hover:bg-gray-50 active:bg-gray-200 flex-shrink-0 transition-all duration-150 cursor-pointer"
                  style={{ 
                    minWidth: '48px', 
                    minHeight: '48px', 
                    touchAction: 'manipulation',
                  }}
                  title="Expandir sidebar"
                  type="button"
                >
                  {/* Ícone para expandir sidebar no desktop */}
                  <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 5l7 7-7 7M5 5l7 7-7 7" />
                  </svg>
                </button>
              )}
              
              <div>
                <h1 className="text-lg sm:text-xl font-semibold text-gray-800 truncate">
                  {menuItems.find(item => item.id === currentPage)?.label || 'Dashboard'}
                </h1>
              </div>
            </div>
            
            <div className="flex items-center gap-4 flex-shrink-0">
              <span className="text-sm text-gray-600 hidden sm:block truncate">
                Protegendo contratos desde 2024
              </span>
              <div className="w-8 h-8 bg-gradient-to-r from-blue-500 to-purple-500 rounded-full flex-shrink-0"></div>
            </div>
          </div>
        </div>

        {/* Page Content */}
        <main className="p-4 sm:p-6 relative z-0">
          {children}
        </main>
      </div>
    </div>
  )
}