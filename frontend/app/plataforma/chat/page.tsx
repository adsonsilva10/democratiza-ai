'use client'

import { useState } from 'react'
import ChatWithAgent from '@/components/features/ChatWithAgent'

export default function ChatPage() {
  return (
    <div className="h-screen flex flex-col bg-gradient-to-br from-gray-50 to-white">
      {/* Header moderno com breadcrumb */}
      <div className="bg-white border-b border-gray-200 px-4 md:px-6 py-4 md:py-6 flex-shrink-0">
        <div className="flex flex-col gap-2">
          <nav className="text-sm text-gray-500">
            <span>Plataforma</span> <span className="mx-2">›</span> <span className="text-gray-900">Chat</span>
          </nav>
          <div className="flex items-center gap-3">
            <div className="p-2 bg-cyan-100 rounded-lg">
              <span className="text-xl text-cyan-600">💬</span>
            </div>
            <div>
              <h1 className="text-xl md:text-2xl font-bold text-gray-900">Assistente Jurídico</h1>
              <p className="text-sm text-gray-600">Converse com nossos especialistas em IA jurídica</p>
            </div>
          </div>
        </div>
      </div>
      
      {/* Chat Container - Ocupa o restante da tela */}
      <div className="flex-1 px-4 md:px-6 py-4 pb-6 overflow-hidden">
        <div className="h-[calc(100%-0.5rem)] max-w-6xl mx-auto">
          {/* Chat Interface */}
          <div className="bg-white rounded-xl border border-gray-200 shadow-lg h-full overflow-hidden">
            {/* Chat Area */}
            <ChatWithAgent
              initialAgent="general"
            />
          </div>
        </div>
      </div>
    </div>
  )
}