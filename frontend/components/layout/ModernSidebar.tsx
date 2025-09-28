'use client'

import Link from 'next/link'
import { useState, ReactNode, useEffect } from 'react'

interface ModernSidebarProps {
  children: ReactNode
  currentPage?: string
}

export default function ModernSidebar({ children, currentPage }: ModernSidebarProps) {
  const [sidebarOpen, setSidebarOpen] = useState(false)
  const [mounted, setMounted] = useState(false)

  useEffect(() => {
    setMounted(true)
  }, [])

  if (!mounted) {
    return (
      <div className="min-h-screen bg-gray-50">
        <div className="p-4 sm:p-6">
          {children}
        </div>
      </div>
    )
  }

  const toggleSidebar = () => {
    setSidebarOpen(!sidebarOpen)
  }

  const menuSections = [
    {
      title: "Análise de Contratos",
      items: [
        { icon: '🏠', label: 'Visão Geral', href: '/dashboard', id: 'dashboard' },
        { icon: '🔍', label: 'Nova Análise', href: '/dashboard/analise', id: 'analise' },
        { icon: '📜', label: 'Histórico', href: '/dashboard/historico', id: 'historico' },
      ]
    },
    {
      title: "Ferramentas",
      items: [
        { icon: '✍️', label: 'Assinatura', href: '/dashboard/assinatura', id: 'assinatura' },
        { icon: '🤖', label: 'Assistente IA', href: '/dashboard/assistente', id: 'assistente' },
      ]
    },
    {
      title: "Conta",
      items: [
        { icon: '💳', label: 'Planos', href: '/dashboard/planos', id: 'planos' },
        { icon: '⚙️', label: 'Configurações', href: '/dashboard/configuracoes', id: 'configuracoes' },
      ]
    }
  ]

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Mobile menu button */}
      <div className="lg:hidden fixed top-4 left-4 z-50">
        <button
          onClick={toggleSidebar}
          className="p-2 bg-white rounded-md shadow-md text-gray-600 hover:text-gray-900"
        >
          <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
          </svg>
        </button>
      </div>

      {/* Sidebar */}
      <div className={`fixed inset-y-0 left-0 z-40 w-64 bg-white shadow-lg transform transition-transform duration-300 ease-in-out lg:translate-x-0 ${sidebarOpen ? 'translate-x-0' : '-translate-x-full'}`}>
        {/* Sidebar header */}
        <div className="flex items-center gap-3 px-6 py-6 border-b border-gray-200">
          <div className="w-10 h-10 bg-gradient-to-br from-blue-500 to-purple-600 rounded-lg flex items-center justify-center text-white text-xl font-bold">
            ⚖️
          </div>
          <div>
            <h2 className="text-xl font-bold text-gray-900">Democratiza AI</h2>
            <p className="text-sm text-gray-500">Contratos Seguros</p>
          </div>
        </div>

        {/* Menu sections */}
        <nav className="mt-6 px-4 space-y-6">
          {menuSections.map((section, sectionIndex) => (
            <div key={sectionIndex}>
              <h3 className="text-xs font-semibold text-gray-500 uppercase tracking-wide px-2 mb-3">
                {section.title}
              </h3>
              <div className="space-y-1">
                {section.items.map((item) => (
                  <Link
                    key={item.id}
                    href={item.href}
                    className={`flex items-center gap-3 px-3 py-2 rounded-lg text-sm font-medium transition-colors ${
                      currentPage === item.id
                        ? 'bg-blue-50 text-blue-700 border-r-2 border-blue-700'
                        : 'text-gray-600 hover:bg-gray-50 hover:text-gray-900'
                    }`}
                  >
                    <span className="text-lg">{item.icon}</span>
                    {item.label}
                  </Link>
                ))}
              </div>
            </div>
          ))}
        </nav>

        {/* User section */}
        <div className="absolute bottom-0 left-0 right-0 p-4 border-t border-gray-200 bg-white">
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 bg-gray-300 rounded-full flex items-center justify-center text-sm font-medium text-gray-600">
              U
            </div>
            <div className="flex-1 min-w-0">
              <p className="text-sm font-medium text-gray-900 truncate">Usuário</p>
              <p className="text-xs text-gray-500">usuario@email.com</p>
            </div>
          </div>
        </div>
      </div>

      {/* Main content */}
      <div className="lg:pl-64">
        <main className="p-6">
          {children}
        </main>
      </div>

      {/* Mobile overlay */}
      {sidebarOpen && (
        <div
          className="fixed inset-0 bg-black bg-opacity-50 z-30 lg:hidden"
          onClick={toggleSidebar}
        />
      )}
    </div>
  )
}