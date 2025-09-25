'use client'

import React, { useState, useEffect } from 'react'
import { useAgents, AgentInfo } from '@/lib/hooks/useApi'

interface AgentSelectorProps {
  selectedAgent: string
  onAgentChange: (agentType: string) => void
  contractText?: string
  className?: string
}

const AgentSelector: React.FC<AgentSelectorProps> = ({
  selectedAgent,
  onAgentChange,
  contractText,
  className = ""
}) => {
  const [agents, setAgents] = useState<Record<string, AgentInfo>>({})
  const [suggestedAgent, setSuggestedAgent] = useState<string | null>(null)
  const { getAvailableAgents, classifyContract, loading } = useAgents()

  useEffect(() => {
    loadAgents()
  }, [])

  useEffect(() => {
    if (contractText && contractText.trim()) {
      autoClassifyContract()
    }
  }, [contractText])

  const loadAgents = async () => {
    try {
      const availableAgents = await getAvailableAgents()
      setAgents(availableAgents)
    } catch (error) {
      console.error('Erro ao carregar agentes:', error)
    }
  }

  const autoClassifyContract = async () => {
    if (!contractText) return

    try {
      const classification = await classifyContract(contractText)
      if (classification.agent_type && classification.agent_type !== selectedAgent) {
        setSuggestedAgent(classification.agent_type)
      }
    } catch (error) {
      console.error('Erro na classificação automática:', error)
    }
  }

  const handleAgentSelect = (agentType: string) => {
    onAgentChange(agentType)
    setSuggestedAgent(null) // Limpar sugestão após seleção
  }

  const acceptSuggestion = () => {
    if (suggestedAgent) {
      handleAgentSelect(suggestedAgent)
    }
  }

  return (
    <div className={`space-y-4 ${className}`}>
      {/* Sugestão de Agente */}
      {suggestedAgent && suggestedAgent !== selectedAgent && (
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-3">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-2">
              <span className="text-blue-600">🤖</span>
              <div>
                <p className="text-sm font-medium text-blue-800">
                  Agente sugerido: {agents[suggestedAgent]?.name}
                </p>
                <p className="text-xs text-blue-600">
                  Baseado no conteúdo do contrato
                </p>
              </div>
            </div>
            <button
              onClick={acceptSuggestion}
              className="px-3 py-1 bg-blue-600 text-white text-xs rounded hover:bg-blue-700"
            >
              Aceitar
            </button>
          </div>
        </div>
      )}

      {/* Seletor de Agentes */}
      <div className="grid grid-cols-2 gap-2">
        {Object.entries(agents).map(([agentType, agentInfo]) => (
          <button
            key={agentType}
            onClick={() => handleAgentSelect(agentType)}
            className={`
              p-3 rounded-lg border-2 transition-all text-left
              ${selectedAgent === agentType
                ? `border-${agentInfo.color}-500 bg-${agentInfo.color}-50`
                : 'border-gray-200 hover:border-gray-300 bg-white'
              }
            `}
          >
            <div className="flex items-center space-x-2 mb-1">
              <span className="text-lg">{agentInfo.icon}</span>
              <span className={`font-medium text-sm ${
                selectedAgent === agentType ? `text-${agentInfo.color}-800` : 'text-gray-800'
              }`}>
                {agentInfo.name}
              </span>
            </div>
            <p className={`text-xs ${
              selectedAgent === agentType ? `text-${agentInfo.color}-600` : 'text-gray-600'
            }`}>
              {agentInfo.description}
            </p>
            <div className="flex flex-wrap gap-1 mt-2">
              {agentInfo.areas.slice(0, 3).map((area, index) => (
                <span
                  key={index}
                  className={`
                    px-1.5 py-0.5 text-xs rounded
                    ${selectedAgent === agentType
                      ? `bg-${agentInfo.color}-100 text-${agentInfo.color}-700`
                      : 'bg-gray-100 text-gray-600'
                    }
                  `}
                >
                  {area}
                </span>
              ))}
            </div>
          </button>
        ))}
      </div>

      {/* Informações do Agente Selecionado */}
      {selectedAgent && agents[selectedAgent] && (
        <div className="bg-gray-50 rounded-lg p-3">
          <div className="flex items-center space-x-2 mb-2">
            <span className="text-lg">{agents[selectedAgent].icon}</span>
            <span className="font-medium text-gray-800">
              {agents[selectedAgent].name}
            </span>
          </div>
          <p className="text-sm text-gray-600 mb-2">
            {agents[selectedAgent].description}
          </p>
          <div className="flex flex-wrap gap-1">
            <span className="text-xs text-gray-500 mr-1">Especialidades:</span>
            {agents[selectedAgent].areas.map((area, index) => (
              <span
                key={index}
                className="px-2 py-1 bg-gray-200 text-gray-700 text-xs rounded"
              >
                {area}
              </span>
            ))}
          </div>
        </div>
      )}

      {loading && (
        <div className="text-center py-2">
          <span className="text-sm text-gray-500">Carregando agentes...</span>
        </div>
      )}
    </div>
  )
}

export default AgentSelector