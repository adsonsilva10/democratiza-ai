'use client'

import React, { useState, useEffect } from 'react'

interface ChatSession {
  id: string
  contract_id?: string
  messages: Array<{
    id: string
    content: string
    role: 'user' | 'assistant'
    timestamp: string
    agent_type?: string
  }>
  created_at: string
  updated_at: string
  title?: string
  agent_type?: string
}

interface ChatHistoryProps {
  onSessionLoad: (session: ChatSession) => void
  currentSessionId?: string
  onNewSession: () => void
  className?: string
}

const ChatHistory: React.FC<ChatHistoryProps> = ({
  onSessionLoad,
  currentSessionId,
  onNewSession,
  className = ""
}) => {
  const [sessions, setSessions] = useState<ChatSession[]>([])
  const [filteredSessions, setFilteredSessions] = useState<ChatSession[]>([])
  const [searchQuery, setSearchQuery] = useState('')
  const [filterAgent, setFilterAgent] = useState('all')
  const [sortOrder, setSortOrder] = useState<'newest' | 'oldest'>('newest')
  const [showDetails, setShowDetails] = useState<string | null>(null)

  useEffect(() => {
    loadSessions()
  }, [])

  useEffect(() => {
    applyFilters()
  }, [sessions, searchQuery, filterAgent, sortOrder])

  const loadSessions = () => {
    try {
      const sessionList = JSON.parse(localStorage.getItem('user_chat_sessions') || '[]')
      const fullSessions: ChatSession[] = []

      for (const sessionMeta of sessionList) {
        const fullSession = localStorage.getItem(`chat_session_${sessionMeta.id}`)
        if (fullSession) {
          const session = JSON.parse(fullSession)
          // Adicionar título automático se não tiver
          if (!session.title && session.messages && session.messages.length > 0) {
            const firstUserMessage = session.messages.find((m: any) => m.role === 'user')
            session.title = firstUserMessage 
              ? firstUserMessage.content.slice(0, 50) + (firstUserMessage.content.length > 50 ? '...' : '')
              : 'Nova conversa'
          }
          fullSessions.push(session)
        }
      }

      setSessions(fullSessions)
    } catch (error) {
      console.error('Erro ao carregar sessões:', error)
      setSessions([])
    }
  }

  const applyFilters = () => {
    let filtered = [...sessions]

    // Filtro por busca
    if (searchQuery.trim()) {
      filtered = filtered.filter(session =>
        session.title?.toLowerCase().includes(searchQuery.toLowerCase()) ||
        session.messages.some(msg => 
          msg.content.toLowerCase().includes(searchQuery.toLowerCase())
        )
      )
    }

    // Filtro por agente
    if (filterAgent !== 'all') {
      filtered = filtered.filter(session =>
        session.agent_type === filterAgent ||
        session.messages.some(msg => msg.agent_type === filterAgent)
      )
    }

    // Ordenação
    filtered.sort((a, b) => {
      const dateA = new Date(a.updated_at)
      const dateB = new Date(b.updated_at)
      return sortOrder === 'newest' ? dateB.getTime() - dateA.getTime() : dateA.getTime() - dateB.getTime()
    })

    setFilteredSessions(filtered)
  }

  const deleteSession = (sessionId: string) => {
    if (confirm('Tem certeza que deseja excluir esta conversa?')) {
      try {
        // Remover sessão do localStorage
        localStorage.removeItem(`chat_session_${sessionId}`)
        
        // Atualizar lista de sessões
        const sessionList = JSON.parse(localStorage.getItem('user_chat_sessions') || '[]')
        const updatedList = sessionList.filter((s: any) => s.id !== sessionId)
        localStorage.setItem('user_chat_sessions', JSON.stringify(updatedList))
        
        loadSessions()
      } catch (error) {
        console.error('Erro ao excluir sessão:', error)
      }
    }
  }

  const exportSession = (session: ChatSession) => {
    const exportData = {
      title: session.title,
      created_at: session.created_at,
      messages: session.messages,
      agent_type: session.agent_type
    }
    
    const blob = new Blob([JSON.stringify(exportData, null, 2)], { type: 'application/json' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `chat-${session.title?.replace(/[^a-z0-9]/gi, '_')}-${new Date().toISOString().split('T')[0]}.json`
    a.click()
    URL.revokeObjectURL(url)
  }

  const formatDate = (dateString: string) => {
    const date = new Date(dateString)
    const now = new Date()
    const diff = now.getTime() - date.getTime()
    const days = Math.floor(diff / (1000 * 60 * 60 * 24))
    
    if (days === 0) {
      return date.toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit' })
    } else if (days === 1) {
      return 'Ontem'
    } else if (days < 7) {
      return `${days} dias atrás`
    } else {
      return date.toLocaleDateString('pt-BR')
    }
  }

  const getAgentIcon = (agentType?: string) => {
    switch (agentType) {
      case 'rental': return '🏠'
      case 'financial': return '💰'
      case 'telecom': return '📱'
      default: return '🤖'
    }
  }

  const getAgentName = (agentType?: string) => {
    switch (agentType) {
      case 'rental': return 'Locação'
      case 'financial': return 'Financeiro'
      case 'telecom': return 'Telecom'
      default: return 'Geral'
    }
  }

  return (
    <div className={`flex flex-col h-full bg-white ${className}`}>
      {/* Header */}
      <div className="p-4 border-b border-gray-200">
        <div className="flex items-center justify-between mb-3">
          <h3 className="text-lg font-semibold text-gray-800">Histórico de Conversas</h3>
          <button
            onClick={onNewSession}
            className="px-3 py-1 bg-blue-500 text-white text-sm rounded hover:bg-blue-600"
          >
            + Nova
          </button>
        </div>

        {/* Busca */}
        <div className="mb-3">
          <input
            type="text"
            placeholder="Buscar conversas..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 rounded text-sm focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
          />
        </div>

        {/* Filtros */}
        <div className="flex space-x-2">
          <select
            value={filterAgent}
            onChange={(e) => setFilterAgent(e.target.value)}
            className="flex-1 px-2 py-1 border border-gray-300 rounded text-sm"
          >
            <option value="all">Todos os agentes</option>
            <option value="general">🤖 Geral</option>
            <option value="rental">🏠 Locação</option>
            <option value="financial">💰 Financeiro</option>
            <option value="telecom">📱 Telecom</option>
          </select>

          <select
            value={sortOrder}
            onChange={(e) => setSortOrder(e.target.value as 'newest' | 'oldest')}
            className="flex-1 px-2 py-1 border border-gray-300 rounded text-sm"
          >
            <option value="newest">Mais recentes</option>
            <option value="oldest">Mais antigas</option>
          </select>
        </div>
      </div>

      {/* Lista de Sessões */}
      <div className="flex-1 overflow-y-auto">
        {filteredSessions.length === 0 ? (
          <div className="p-4 text-center text-gray-500">
            {sessions.length === 0 ? (
              <div>
                <p>Nenhuma conversa ainda.</p>
                <p className="text-sm">Inicie uma nova conversa para começar!</p>
              </div>
            ) : (
              <p>Nenhuma conversa encontrada com os filtros aplicados.</p>
            )}
          </div>
        ) : (
          <div className="space-y-1 p-2">
            {filteredSessions.map((session) => (
              <div
                key={session.id}
                className={`relative group border border-gray-200 rounded-lg hover:border-gray-300 transition-colors ${
                  currentSessionId === session.id ? 'bg-blue-50 border-blue-300' : 'bg-white'
                }`}
              >
                <div
                  onClick={() => onSessionLoad(session)}
                  className="p-3 cursor-pointer"
                >
                  <div className="flex items-start justify-between">
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center space-x-2 mb-1">
                        <span className="text-sm">
                          {getAgentIcon(session.agent_type || session.messages[session.messages.length - 1]?.agent_type)}
                        </span>
                        <span className="text-xs text-gray-500">
                          {getAgentName(session.agent_type || session.messages[session.messages.length - 1]?.agent_type)}
                        </span>
                      </div>
                      <p className="text-sm font-medium text-gray-800 truncate">
                        {session.title || 'Conversa sem título'}
                      </p>
                      <div className="flex items-center justify-between text-xs text-gray-500 mt-1">
                        <span>{session.messages.length} mensagens</span>
                        <span>{formatDate(session.updated_at)}</span>
                      </div>
                    </div>
                  </div>
                </div>

                {/* Ações da sessão */}
                <div className="absolute top-2 right-2 opacity-0 group-hover:opacity-100 transition-opacity">
                  <div className="flex space-x-1">
                    <button
                      onClick={(e) => {
                        e.stopPropagation()
                        setShowDetails(showDetails === session.id ? null : session.id)
                      }}
                      className="p-1 text-gray-400 hover:text-gray-600 text-xs"
                      title="Detalhes"
                    >
                      ℹ️
                    </button>
                    <button
                      onClick={(e) => {
                        e.stopPropagation()
                        exportSession(session)
                      }}
                      className="p-1 text-gray-400 hover:text-gray-600 text-xs"
                      title="Exportar"
                    >
                      📥
                    </button>
                    <button
                      onClick={(e) => {
                        e.stopPropagation()
                        deleteSession(session.id)
                      }}
                      className="p-1 text-gray-400 hover:text-red-500 text-xs"
                      title="Excluir"
                    >
                      🗑️
                    </button>
                  </div>
                </div>

                {/* Detalhes expandidos */}
                {showDetails === session.id && (
                  <div className="border-t border-gray-200 p-3 bg-gray-50 text-xs">
                    <div className="space-y-1">
                      <p><strong>Criado:</strong> {new Date(session.created_at).toLocaleString('pt-BR')}</p>
                      <p><strong>Atualizado:</strong> {new Date(session.updated_at).toLocaleString('pt-BR')}</p>
                      {session.contract_id && <p><strong>Contrato:</strong> {session.contract_id}</p>}
                      <p><strong>Primeira mensagem:</strong> 
                        <span className="ml-1 text-gray-600">
                          {session.messages.find(m => m.role === 'user')?.content.slice(0, 100) || 'N/A'}...
                        </span>
                      </p>
                    </div>
                  </div>
                )}
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Footer com estatísticas */}
      <div className="p-3 border-t border-gray-200 bg-gray-50 text-xs text-gray-600">
        <div className="flex justify-between">
          <span>{filteredSessions.length} de {sessions.length} conversas</span>
          <span>
            {sessions.reduce((acc, session) => acc + session.messages.length, 0)} mensagens total
          </span>
        </div>
      </div>
    </div>
  )
}

export default ChatHistory