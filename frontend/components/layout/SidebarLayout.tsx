'use client'

import Link from 'next/link'
import { useState, ReactNode } from 'react'

interface SidebarLayoutProps {
  children: ReactNode
  currentPage?: string
}

export default function SidebarLayout({ children, currentPage }: SidebarLayoutProps) {
  const [sidebarOpen, setSidebarOpen] = useState(false)

  const menuItems = [
    { icon: '🏠', label: 'Início', href: '/', id: 'home' },
    { icon: '📄', label: 'Análise', href: '/dashboard', id: 'dashboard' },
    { icon: '💬', label: 'Chat IA', href: '/chat', id: 'chat' },
    { icon: '📋', label: 'Contratos', href: '/contracts', id: 'contracts' },
    { icon: '👤', label: 'Perfil', href: '/profile', id: 'profile' },
    { icon: '⚙️', label: 'Configurações', href: '/settings', id: 'settings' },
  ]

  return (
    <div className="min-h-screen bg-gray-50 w-full overflow-x-hidden">
      {/* Sidebar Mobile-First */}
      <div className={`fixed inset-y-0 left-0 z-50 ${sidebarOpen ? 'w-64' : 'w-16'} bg-gradient-to-b from-blue-900 to-purple-900 transition-all duration-300 ease-in-out shadow-lg`}>
        {/* Sidebar Header */}
        <div className="flex items-center justify-between p-4 border-b border-white/10">
          {sidebarOpen && (
            <div className="text-white font-bold text-lg truncate">
              Democratiza AI
            </div>
          )}
          <button
            onClick={() => setSidebarOpen(!sidebarOpen)}
            className="text-white hover:bg-white/10 p-2 rounded-lg transition-colors flex-shrink-0"
          >
            {sidebarOpen ? (
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            ) : (
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
              </svg>
            )}
          </button>
        </div>

        {/* Menu Items */}
        <nav className="mt-8 px-2">
          {menuItems.map((item, index) => (
            <Link
              key={index}
              href={item.href}
              className={`flex items-center px-3 py-3 mb-2 text-white rounded-lg transition-colors group relative ${
                currentPage === item.id ? 'bg-white/20' : 'hover:bg-white/10'
              }`}
            >
              <span className="text-xl flex-shrink-0">{item.icon}</span>
              {sidebarOpen && (
                <span className="ml-3 text-sm font-medium truncate">{item.label}</span>
              )}
              {!sidebarOpen && (
                <div className="absolute left-16 bg-gray-900 text-white px-2 py-1 rounded text-xs opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none whitespace-nowrap z-10">
                  {item.label}
                </div>
              )}
              {currentPage === item.id && (
                <div className="absolute right-2 w-2 h-2 bg-green-400 rounded-full flex-shrink-0"></div>
              )}
            </Link>
          ))}
        </nav>

        {/* User Section */}
        <div className="absolute bottom-20 left-0 right-0 px-2">
          <div className={`flex items-center px-3 py-3 text-white ${sidebarOpen ? 'justify-start' : 'justify-center'}`}>
            <div className="w-8 h-8 bg-gradient-to-r from-green-400 to-blue-400 rounded-full flex items-center justify-center text-sm font-bold flex-shrink-0">
              U
            </div>
            {sidebarOpen && (
              <div className="ml-3 min-w-0 flex-1">
                <div className="text-sm font-medium truncate">Usuário</div>
                <div className="text-xs text-gray-300 truncate">Plano Free</div>
              </div>
            )}
          </div>
        </div>

        {/* Logout Button */}
        <div className="absolute bottom-4 left-0 right-0 px-2">
          <Link
            href="/login"
            className={`flex items-center justify-center px-3 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors ${!sidebarOpen ? 'text-xs' : ''}`}
          >
            {sidebarOpen ? (
              <>
                <span className="text-sm flex-shrink-0">🔐</span>
                <span className="ml-2 text-sm truncate">Sair</span>
              </>
            ) : (
              <span className="text-lg">🔐</span>
            )}
          </Link>
        </div>
      </div>

      {/* Overlay for mobile when sidebar is open */}
      {sidebarOpen && (
        <div 
          className="fixed inset-0 bg-black bg-opacity-50 z-40 lg:hidden"
          onClick={() => setSidebarOpen(false)}
        />
      )}

      {/* Main Content */}
      <div className={`transition-all duration-300 ${sidebarOpen ? 'ml-64' : 'ml-16'} w-full`}>
        {/* Top Bar */}
        <div className="bg-white border-b border-gray-200 px-4 sm:px-6 py-4 w-full">
          <div className="flex items-center justify-between w-full min-w-0">
            <div className="flex items-center min-w-0 flex-1">
              <button
                onClick={() => setSidebarOpen(!sidebarOpen)}
                className="lg:hidden mr-4 p-2 rounded-md text-gray-400 hover:text-gray-500 hover:bg-gray-100 flex-shrink-0"
              >
                <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
                </svg>
              </button>
              <h1 className="text-lg sm:text-xl font-semibold text-gray-800 truncate">
                {menuItems.find(item => item.id === currentPage)?.label || 'Dashboard'}
              </h1>
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
        <main className="p-4 sm:p-6 w-full">
          {children}
        </main>
      </div>
    </div>
  )
}