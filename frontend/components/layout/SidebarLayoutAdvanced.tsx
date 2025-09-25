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
  const [profileDropdownOpen, setProfileDropdownOpen] = useState(false)

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

  const handleProfileToggle = useCallback((e: React.MouseEvent) => {
    e.preventDefault()
    e.stopPropagation()
    setProfileDropdownOpen(prev => !prev)
  }, [])

  // Fechar dropdown quando clicar fora
  const handleClickOutside = useCallback((e: MouseEvent) => {
    const target = e.target as Element
    if (!target.closest('[data-profile-dropdown]')) {
      setProfileDropdownOpen(false)
    }
  }, [])

  useEffect(() => {
    if (profileDropdownOpen) {
      document.addEventListener('click', handleClickOutside)
      return () => document.removeEventListener('click', handleClickOutside)
    }
  }, [profileDropdownOpen, handleClickOutside])

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

  // Menu organizado por categoria com emojis modernos
  const menuSections = [
    {
      title: "Análise de Contratos",
      items: [
        { 
          icon: '🏠', 
          label: 'Visão Geral', 
          href: '/dashboard', 
          id: 'home',
          description: 'Painel principal'
        },
        { 
          icon: '🔍', 
          label: 'Nova Análise', 
          href: '/dashboard/analise', 
          id: 'analise',
          description: 'Analisar novo contrato'
        },
        { 
          icon: '📜', 
          label: 'Histórico', 
          href: '/dashboard/historico', 
          id: 'historico',
          description: 'Contratos analisados'
        },
      ]
    },
    {
      title: "Assinatura Digital",
      items: [
        { 
          icon: '✍️', 
          label: 'Assinatura', 
          href: '/dashboard/assinatura', 
          id: 'assinatura',
          description: 'Gerenciar assinaturas'
        },
      ]
    },
    {
      title: "Planos e Assistência",
      items: [
        { 
          icon: '💳', 
          label: 'Planos', 
          href: '/dashboard/planos', 
          id: 'planos',
          description: 'Gerenciar assinatura'
        },
        { 
          icon: '🤖', 
          label: 'Chat IA', 
          href: '/dashboard/chat', 
          id: 'chat',
          description: 'Assistente jurídico'
        },
      ]
    },
    {
      title: "Conta",
      items: [
        { 
          icon: '⚙️', 
          label: 'Configurações', 
          href: '/dashboard/configuracoes', 
          id: 'configuracoes',
          description: 'Configurações da conta'
        },
        { 
          icon: '💬', 
          label: 'Suporte', 
          href: '/dashboard/suporte', 
          id: 'suporte',
          description: 'Ajuda e suporte'
        },
      ]
    }
  ]

  // Lista plana para compatibilidade com código existente
  const menuItems = menuSections.flatMap(section => section.items)

  // Determina se o sidebar deve estar visível
  const sidebarVisible = isLargeScreen ? !userClosedSidebar : sidebarOpen

  return (
    <div className="min-h-screen bg-gray-50 w-full overflow-x-hidden">
      {/* Sidebar Principal */}
      <div className={`fixed inset-y-0 left-0 z-30 bg-gradient-to-b from-blue-900 to-purple-900 transition-all duration-300 ease-in-out shadow-lg
        ${sidebarVisible ? 'w-64 translate-x-0' : 'w-0 -translate-x-full'}
      `}>
        <div className={`h-full flex flex-col ${sidebarVisible ? 'opacity-100' : 'opacity-0 pointer-events-none'} transition-opacity duration-300`}>
          {/* Sidebar Header - Design Elegante */}
          <div className="flex items-center justify-between px-4 py-4 border-b border-white/20 flex-shrink-0">
            <div className="flex items-center gap-3 min-w-0 flex-1">
              <div className="w-10 h-10 bg-gradient-to-br from-emerald-400 via-cyan-400 to-blue-400 rounded-lg flex items-center justify-center text-xl font-bold shadow-lg">
                ⚖️
              </div>
              <div className="min-w-0">
                <div className="text-white font-bold text-lg truncate">
                  Democratiza AI
                </div>
                <div className="text-white/70 text-xs truncate">
                  Análise Jurídica Inteligente
                </div>
              </div>
            </div>
            <button
              onClick={closeSidebar}
              className="text-white/60 hover:text-white hover:bg-white/20 p-2 rounded-lg transition-all flex-shrink-0 backdrop-blur-sm"
              title={isLargeScreen ? "Minimizar sidebar" : "Fechar menu"}
            >
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>

          {/* Menu Items - Design Otimizado */}
          <nav className="flex-1 px-3 py-4">
            <div className="space-y-4">
              {menuSections.map((section, sectionIndex) => (
                <div key={sectionIndex}>
                  {/* Section Title - Compacto */}
                  <div className="mb-2">
                    <h3 className="text-xs font-semibold text-white/70 uppercase tracking-wider px-2">
                      {section.title}
                    </h3>
                    <div className="mt-1 h-px bg-gradient-to-r from-white/20 to-transparent"></div>
                  </div>
                  
                  {/* Section Items - Otimizado */}
                  <div className="space-y-1">
                    {section.items.map((item, itemIndex) => (
                      <Link
                        key={itemIndex}
                        href={item.href}
                        className={`flex items-center px-3 py-3 text-white rounded-lg transition-all duration-200 group relative ${
                          currentPage === item.id 
                            ? 'bg-white/25 shadow-lg border border-white/30' 
                            : 'hover:bg-white/15 hover:shadow-md'
                        }`}
                      >
                        <div className="flex-shrink-0 text-xl mr-3">
                          {item.icon}
                        </div>
                        <div className="flex-1 min-w-0">
                          <div className="text-sm font-semibold truncate">{item.label}</div>
                          <div className="text-xs text-white/60 truncate">{item.description}</div>
                        </div>
                        {currentPage === item.id && (
                          <div className="flex-shrink-0">
                            <div className="w-2 h-2 bg-emerald-400 rounded-full shadow-sm animate-pulse"></div>
                          </div>
                        )}
                      </Link>
                    ))}
                  </div>
                </div>
              ))}
            </div>
          </nav>

          {/* Footer Section com Logout */}
          <div className="px-3 pb-3">
            {/* Logout Button */}
            <Link
              href="/login"
              className="flex items-center justify-center px-3 py-2.5 bg-gradient-to-r from-red-600/90 to-red-700/90 text-white rounded-lg hover:from-red-600 hover:to-red-700 transition-all duration-200 w-full group shadow-md"
            >
              <span className="text-base mr-2 group-hover:animate-pulse">🚪</span>
              <span className="text-sm font-medium">Sair da Conta</span>
            </Link>
            
            <div className="text-center text-xs text-white/60 mt-2 py-1">
              Democratiza AI © 2024
            </div>
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
        <div className="fixed left-0 top-0 bottom-0 w-16 bg-gradient-to-b from-blue-900 to-purple-900 z-30 flex flex-col shadow-xl">
          {/* Logo compacto no topo */}
          <div className="flex items-center justify-center h-16 border-b border-white/10">
            <span className="text-2xl">⚖️</span>
          </div>
          
          {/* Menu button */}
          <button
            onClick={handleSidebarToggle}
            className="flex items-center justify-center h-12 text-white/60 hover:text-white hover:bg-white/10 transition-colors mx-2 my-2 rounded-lg"
            title="Abrir menu completo"
          >
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
            </svg>
          </button>

          {/* Ícones dos menu items principais */}
          <nav className="flex-1 flex flex-col items-center py-2 space-y-1">
            {menuItems.slice(0, 5).map((item, index) => (
              <Link
                key={index}
                href={item.href}
                className={`w-12 h-12 flex items-center justify-center rounded-xl transition-all duration-200 relative text-xl ${
                  currentPage === item.id 
                    ? 'bg-white/20 text-white shadow-lg scale-110' 
                    : 'text-white/70 hover:bg-white/10 hover:text-white hover:scale-105'
                }`}
                title={item.label}
              >
                {item.icon}
                {currentPage === item.id && (
                  <div className="absolute -right-1 top-1/2 transform -translate-y-1/2 w-1 h-6 bg-emerald-400 rounded-full"></div>
                )}
              </Link>
            ))}
          </nav>

          {/* Ícones inferiores: Configurações, Suporte, Usuário, Logout */}
          <div className="flex flex-col items-center space-y-2 p-2 border-t border-white/10">
            {/* Configurações */}
            <Link
              href="/dashboard/configuracoes"
              className={`w-12 h-12 flex items-center justify-center rounded-xl transition-all duration-200 relative text-lg ${
                currentPage === 'configuracoes' 
                  ? 'bg-white/20 text-white shadow-lg scale-110' 
                  : 'text-white/70 hover:bg-white/10 hover:text-white hover:scale-105'
              }`}
              title="Configurações"
            >
              ⚙️
              {currentPage === 'configuracoes' && (
                <div className="absolute -right-1 top-1/2 transform -translate-y-1/2 w-1 h-6 bg-emerald-400 rounded-full"></div>
              )}
            </Link>

            {/* Ajuda e Suporte */}
            <Link
              href="/dashboard/suporte"
              className={`w-12 h-12 flex items-center justify-center rounded-xl transition-all duration-200 relative text-lg ${
                currentPage === 'suporte' 
                  ? 'bg-white/20 text-white shadow-lg scale-110' 
                  : 'text-white/70 hover:bg-white/10 hover:text-white hover:scale-105'
              }`}
              title="Ajuda e Suporte"
            >
              💬
              {currentPage === 'suporte' && (
                <div className="absolute -right-1 top-1/2 transform -translate-y-1/2 w-1 h-6 bg-emerald-400 rounded-full"></div>
              )}
            </Link>

            {/* Logout */}
            <Link
              href="/login"
              className="w-12 h-12 flex items-center justify-center rounded-xl transition-all duration-200 text-red-400 hover:bg-red-600/20 hover:text-red-300 hover:scale-105 text-lg"
              title="Sair da Conta"
            >
              🚪
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
                  {menuItems.find(item => item.id === currentPage)?.label || 'Visão Geral'}
                </h1>
              </div>
            </div>
            
            <div className="flex items-center gap-3 flex-shrink-0">
              {/* Perfil do usuário */}
              <div className="relative" data-profile-dropdown>
                <button 
                  onClick={handleProfileToggle}
                  className="flex items-center gap-3 hover:bg-gray-50 rounded-lg p-2 transition-colors"
                >
                  <div className="hidden sm:flex flex-col items-end">
                    <span className="text-sm font-medium text-gray-700">Adson Silva</span>
                    <span className="text-xs text-gray-500">Plano Premium</span>
                  </div>
                  <div className="relative">
                    <div className="w-10 h-10 bg-gradient-to-r from-emerald-500 to-cyan-500 rounded-full flex items-center justify-center shadow-lg">
                      <span className="text-white font-semibold text-lg">👤</span>
                    </div>
                    <div className="absolute -bottom-1 -right-1 w-4 h-4 bg-green-500 border-2 border-white rounded-full"></div>
                  </div>
                  <svg className={`w-4 h-4 text-gray-400 transition-transform ${profileDropdownOpen ? 'rotate-180' : ''}`} fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                  </svg>
                </button>

                {/* Dropdown Menu */}
                {profileDropdownOpen && (
                  <div className="absolute right-0 mt-2 w-80 sm:w-80 w-72 bg-white rounded-xl shadow-xl border border-gray-200 z-50 overflow-hidden">
                    {/* Header do Perfil */}
                    <div className="bg-gradient-to-r from-emerald-500 to-cyan-500 p-4 text-white">
                      <div className="flex items-center gap-3">
                        <div className="w-12 h-12 bg-white/20 rounded-full flex items-center justify-center text-xl font-bold">
                          👤
                        </div>
                        <div>
                          <h3 className="font-semibold text-lg">Adson Silva</h3>
                          <div className="flex items-center gap-2">
                            <div className="w-2 h-2 bg-green-300 rounded-full"></div>
                            <span className="text-sm text-emerald-100">Plano Premium</span>
                          </div>
                        </div>
                      </div>
                    </div>

                    {/* Estatísticas */}
                    <div className="p-4 border-b border-gray-200">
                      <h4 className="text-sm font-medium text-gray-700 mb-3">Estatísticas</h4>
                      <div className="grid grid-cols-3 gap-4">
                        <div className="text-center">
                          <div className="text-lg font-bold text-blue-600">5</div>
                          <div className="text-xs text-gray-500">📊 Análises</div>
                        </div>
                        <div className="text-center">
                          <div className="text-lg font-bold text-green-600">2</div>
                          <div className="text-xs text-gray-500">✍️ Assinaturas</div>
                        </div>
                        <div className="text-center">
                          <div className="text-lg font-bold text-emerald-600">85%</div>
                          <div className="text-xs text-gray-500">💰 Economia</div>
                        </div>
                      </div>
                    </div>

                    {/* Menu Items */}
                    <div className="py-2">
                      <Link href="/dashboard/configuracoes" className="flex items-center gap-3 px-4 py-3 text-gray-700 hover:bg-gray-50 transition-colors">
                        <span className="text-lg">⚙️</span>
                        <span className="text-sm font-medium">Configurações</span>
                      </Link>
                      <Link href="/dashboard/suporte" className="flex items-center gap-3 px-4 py-3 text-gray-700 hover:bg-gray-50 transition-colors">
                        <span className="text-lg">💬</span>
                        <span className="text-sm font-medium">Suporte</span>
                      </Link>
                      <Link href="/dashboard/gerenciar-plano" className="flex items-center gap-3 px-4 py-3 text-gray-700 hover:bg-gray-50 transition-colors">
                        <span className="text-lg">💳</span>
                        <span className="text-sm font-medium">Gerenciar Plano</span>
                      </Link>
                      <hr className="my-2" />
                      <Link href="/login" className="flex items-center gap-3 px-4 py-3 text-red-600 hover:bg-red-50 transition-colors">
                        <span className="text-lg">🚪</span>
                        <span className="text-sm font-medium">Sair da Conta</span>
                      </Link>
                    </div>
                  </div>
                )}
              </div>
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