'use client'

import { useState } from 'react'
import ChatWithAgent from '@/components/features/ChatWithAgent'

export default function ChatPage() {
  return (
    <div className="flex flex-col h-full -m-6">
      <div className="bg-white border-b border-gray-200 px-4 py-3 flex-shrink-0">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-xl md:text-3xl font-bold text-gray-900">
              🤖 Assistente IA
            </h1>
            <p className="text-sm md:text-base text-gray-600 mt-1">
              Converse com agentes especializados sobre seus contratos
            </p>
          </div>
        </div>
      </div>

      <div className="flex-1 px-2 py-2 flex flex-col min-h-0">
        <div className="flex-1 flex flex-col min-h-0">
          {/* Chat Interface */}
          <div className="bg-white rounded-xl border border-gray-200 shadow-lg overflow-hidden flex-1 flex flex-col min-h-0">
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