'use client'

import Link from 'next/link'
import { useState, ReactNode } from 'react'

interface SidebarLayoutProps {
  children: ReactNode
  currentPage?: string
}

export default function SidebarLayout({ children, currentPage }: SidebarLayoutProps) {
  const [sidebarOpen, setSidebarOpen] = useState(true)

  const menuItems = [
    { 
      icon: '🏠', 
      label: 'Início', 
      href: '/', 
      id: 'home' 
    },
    { 
      icon: '📄', 
      label: 'Análise', 
      href: '/dashboard', 
      id: 'dashboard' 
    },
    { 
      icon: '💬', 
      label: 'Chat IA', 
      href: '/chat', 
      id: 'chat' 
    },
    { 
      icon: '📋', 
      label: 'Contratos', 
      href: '/contracts', 
      id: 'contracts' 
    },
    { 
      icon: '📊', 
      label: 'Performance', 
      href: '/performance', 
      id: 'performance' 
    },
  ]

  return (
    <div className="min-h-screen bg-gray-50 flex">
      {/* Sidebar Simples */}
      <div className={`bg-blue-900 text-white transition-all duration-300 ${sidebarOpen ? 'w-64' : 'w-16'}`}>
        <div className="p-4">
          <h1 className={`font-bold ${sidebarOpen ? 'text-lg' : 'text-xs'}`}>
            {sidebarOpen ? 'Democratiza AI' : 'DA'}
          </h1>
        </div>
        
        <nav className="mt-8">
          {menuItems.map((item, index) => (
            <Link
              key={index}
              href={item.href}
              className={`flex items-center px-4 py-3 text-white hover:bg-white/10 ${
                currentPage === item.id ? 'bg-white/20' : ''
              }`}
            >
              <span className="text-xl">{item.icon}</span>
              {sidebarOpen && <span className="ml-3">{item.label}</span>}
            </Link>
          ))}
        </nav>
        
        <div className="absolute bottom-4 left-4">
          <button
            onClick={() => setSidebarOpen(!sidebarOpen)}
            className="text-white hover:bg-white/10 p-2 rounded"
          >
            {sidebarOpen ? '◀' : '▶'}
          </button>
        </div>
      </div>

      {/* Main Content */}
      <div className="flex-1">
        <div className="bg-white border-b p-4">
          <h1 className="text-xl font-semibold">
            {menuItems.find(item => item.id === currentPage)?.label || 'Dashboard'}
          </h1>
        </div>
        
        <main className="p-6">
          {children}
        </main>
      </div>
    </div>
  )
}