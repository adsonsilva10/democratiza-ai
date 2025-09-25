'use client'

import React, { useState, useEffect } from 'react'
import { useContractContext, ContractContext } from '@/lib/hooks/useContractContext'

interface ContractSelectorProps {
  selectedContractId?: string
  onContractSelect: (contractId: string | null) => void
  onUploadContract?: (text: string, fileName?: string) => void
  className?: string
}

const ContractSelector: React.FC<ContractSelectorProps> = ({
  selectedContractId,
  onContractSelect,
  onUploadContract,
  className = ""
}) => {
  const {
    contracts,
    loading,
    loadContracts,
    searchContracts,
    analyzeContract,
    removeContract
  } = useContractContext()

  const [searchQuery, setSearchQuery] = useState('')
  const [showUpload, setShowUpload] = useState(false)
  const [uploadText, setUploadText] = useState('')
  const [uploadFileName, setUploadFileName] = useState('')
  const [filteredContracts, setFilteredContracts] = useState<ContractContext[]>([])

  useEffect(() => {
    loadContracts()
  }, [loadContracts])

  useEffect(() => {
    setFilteredContracts(searchContracts(searchQuery))
  }, [contracts, searchQuery, searchContracts])

  const handleUploadSubmit = () => {
    if (uploadText.trim() && onUploadContract) {
      onUploadContract(uploadText, uploadFileName || undefined)
      setUploadText('')
      setUploadFileName('')
      setShowUpload(false)
    }
  }

  const handleAnalyze = async (contractId: string) => {
    try {
      await analyzeContract(contractId)
    } catch (error) {
      console.error('Erro na análise:', error)
    }
  }

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('pt-BR', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric'
    })
  }

  const getRiskColor = (riskLevel?: string) => {
    switch (riskLevel) {
      case 'ALTO_RISCO': return 'text-red-600 bg-red-50'
      case 'MEDIO_RISCO': return 'text-yellow-600 bg-yellow-50'
      case 'BAIXO_RISCO': return 'text-green-600 bg-green-50'
      default: return 'text-gray-600 bg-gray-50'
    }
  }

  const getRiskIcon = (riskLevel?: string) => {
    switch (riskLevel) {
      case 'ALTO_RISCO': return '🔴'
      case 'MEDIO_RISCO': return '🟡'
      case 'BAIXO_RISCO': return '🟢'
      default: return '⚪'
    }
  }

  return (
    <div className={`bg-white border border-gray-200 rounded-lg ${className}`}>
      {/* Header */}
      <div className="p-4 border-b border-gray-200">
        <div className="flex items-center justify-between mb-3">
          <h3 className="font-semibold text-gray-800">Contratos para Contexto</h3>
          <button
            onClick={() => setShowUpload(!showUpload)}
            className="px-3 py-1 bg-blue-500 text-white text-sm rounded hover:bg-blue-600"
          >
            {showUpload ? 'Cancelar' : '+ Adicionar'}
          </button>
        </div>

        {/* Busca */}
        <input
          type="text"
          placeholder="Buscar contratos..."
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          className="w-full px-3 py-2 border border-gray-300 rounded text-sm focus:ring-2 focus:ring-blue-500"
        />
      </div>

      {/* Upload de novo contrato */}
      {showUpload && (
        <div className="p-4 bg-blue-50 border-b border-gray-200">
          <div className="space-y-3">
            <input
              type="text"
              placeholder="Nome do arquivo (opcional)"
              value={uploadFileName}
              onChange={(e) => setUploadFileName(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded text-sm focus:ring-2 focus:ring-blue-500"
            />
            <textarea
              placeholder="Cole o texto do contrato aqui..."
              value={uploadText}
              onChange={(e) => setUploadText(e.target.value)}
              rows={4}
              className="w-full px-3 py-2 border border-gray-300 rounded text-sm focus:ring-2 focus:ring-blue-500 resize-none"
            />
            <div className="flex gap-2">
              <button
                onClick={handleUploadSubmit}
                disabled={!uploadText.trim()}
                className="px-4 py-2 bg-blue-500 text-white text-sm rounded hover:bg-blue-600 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                Adicionar Contrato
              </button>
              <button
                onClick={() => setShowUpload(false)}
                className="px-4 py-2 bg-gray-500 text-white text-sm rounded hover:bg-gray-600"
              >
                Cancelar
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Lista de contratos */}
      <div className="max-h-96 overflow-y-auto">
        {loading ? (
          <div className="p-4 text-center text-gray-500">
            <span>Carregando contratos...</span>
          </div>
        ) : filteredContracts.length === 0 ? (
          <div className="p-4 text-center text-gray-500">
            {contracts.length === 0 ? (
              <div>
                <p>Nenhum contrato adicionado ainda.</p>
                <p className="text-sm">Adicione um contrato para começar a conversar com contexto!</p>
              </div>
            ) : (
              <p>Nenhum contrato encontrado com a busca atual.</p>
            )}
          </div>
        ) : (
          <div className="space-y-1 p-2">
            {/* Opção "Sem contexto" */}
            <button
              onClick={() => onContractSelect(null)}
              className={`w-full p-3 text-left border border-gray-200 rounded hover:border-gray-300 transition-colors ${
                !selectedContractId ? 'bg-blue-50 border-blue-300' : 'bg-white'
              }`}
            >
              <div className="flex items-center space-x-2">
                <span className="text-lg">🤖</span>
                <div>
                  <p className="font-medium text-gray-800">Chat Geral</p>
                  <p className="text-xs text-gray-500">Conversar sem contexto específico de contrato</p>
                </div>
              </div>
            </button>

            {/* Contratos disponíveis */}
            {filteredContracts.map((contract) => (
              <div
                key={contract.id}
                className={`border border-gray-200 rounded hover:border-gray-300 transition-colors ${
                  selectedContractId === contract.id ? 'bg-blue-50 border-blue-300' : 'bg-white'
                }`}
              >
                <button
                  onClick={() => onContractSelect(contract.id)}
                  className="w-full p-3 text-left"
                >
                  <div className="flex items-start justify-between">
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center space-x-2 mb-1">
                        <span className="text-lg">📄</span>
                        <span className="font-medium text-gray-800 truncate">
                          {contract.fileName || `Contrato ${contract.id.slice(-8)}`}
                        </span>
                        {contract.analysis && (
                          <span className={`px-2 py-1 text-xs rounded ${getRiskColor(contract.analysis.risk_assessment.overall_risk)}`}>
                            {getRiskIcon(contract.analysis.risk_assessment.overall_risk)}
                            {contract.analysis.risk_assessment.overall_risk.replace('_', ' ')}
                          </span>
                        )}
                      </div>
                      <p className="text-xs text-gray-500 mb-1">
                        Adicionado em {formatDate(contract.uploadDate)}
                      </p>
                      <p className="text-xs text-gray-600 line-clamp-2">
                        {contract.analysis?.summary || contract.text.slice(0, 100) + '...'}
                      </p>
                    </div>
                  </div>
                </button>

                {/* Ações do contrato */}
                <div className="px-3 pb-2 flex space-x-2">
                  {!contract.analysis && (
                    <button
                      onClick={() => handleAnalyze(contract.id)}
                      className="px-2 py-1 bg-green-500 text-white text-xs rounded hover:bg-green-600"
                    >
                      Analisar
                    </button>
                  )}
                  <button
                    onClick={() => removeContract(contract.id)}
                    className="px-2 py-1 bg-red-500 text-white text-xs rounded hover:bg-red-600"
                  >
                    Remover
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Footer */}
      {contracts.length > 0 && (
        <div className="p-3 border-t border-gray-200 bg-gray-50 text-xs text-gray-600">
          <div className="flex justify-between">
            <span>{filteredContracts.length} de {contracts.length} contratos</span>
            <span>
              {contracts.filter(c => c.analysis).length} analisados
            </span>
          </div>
        </div>
      )}
    </div>
  )
}

export default ContractSelector