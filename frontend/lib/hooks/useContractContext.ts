'use client'

import { useState, useCallback } from 'react'
import { useApi, ContractAnalysis } from './useApi'

export interface ContractContext {
  id: string
  text: string
  analysis?: ContractAnalysis
  fileName?: string
  uploadDate: string
}

export const useContractContext = () => {
  const [contracts, setContracts] = useState<ContractContext[]>([])
  const [selectedContract, setSelectedContract] = useState<ContractContext | null>(null)
  const { apiRequest, loading, error } = useApi()

  // Carregar contratos do localStorage
  const loadContracts = useCallback(() => {
    try {
      const savedContracts = JSON.parse(localStorage.getItem('analyzed_contracts') || '[]')
      setContracts(savedContracts)
      return savedContracts
    } catch (error) {
      console.error('Erro ao carregar contratos:', error)
      return []
    }
  }, [])

  // Salvar contratos no localStorage
  const saveContracts = useCallback((contractList: ContractContext[]) => {
    try {
      localStorage.setItem('analyzed_contracts', JSON.stringify(contractList))
      setContracts(contractList)
    } catch (error) {
      console.error('Erro ao salvar contratos:', error)
    }
  }, [])

  // Adicionar novo contrato
  const addContract = useCallback((text: string, fileName?: string) => {
    const newContract: ContractContext = {
      id: `contract-${Date.now()}`,
      text,
      fileName,
      uploadDate: new Date().toISOString()
    }

    const updatedContracts = [...contracts, newContract]
    saveContracts(updatedContracts)
    return newContract
  }, [contracts, saveContracts])

  // Analisar contrato
  const analyzeContract = useCallback(async (contractId: string): Promise<ContractAnalysis | null> => {
    try {
      const contract = contracts.find(c => c.id === contractId)
      if (!contract) {
        throw new Error('Contrato não encontrado')
      }

      const analysis = await apiRequest('/api/v1/demo/analyze-text', {
        method: 'POST',
        body: JSON.stringify({ text: contract.text }),
      }) as ContractAnalysis

      // Atualizar contrato com análise
      const updatedContracts = contracts.map(c => 
        c.id === contractId ? { ...c, analysis } : c
      )
      saveContracts(updatedContracts)

      return analysis
    } catch (error) {
      console.error('Erro na análise:', error)
      return null
    }
  }, [contracts, apiRequest, saveContracts])

  // Selecionar contrato para contexto
  const selectContract = useCallback((contractId: string | null) => {
    if (contractId) {
      const contract = contracts.find(c => c.id === contractId)
      setSelectedContract(contract || null)
    } else {
      setSelectedContract(null)
    }
  }, [contracts])

  // Gerar contexto para chat
  const getContextForChat = useCallback((contractId?: string) => {
    const targetContract = contractId 
      ? contracts.find(c => c.id === contractId)
      : selectedContract

    if (!targetContract) {
      return null
    }

    return {
      contract_id: targetContract.id,
      contract_text: targetContract.text,
      file_name: targetContract.fileName,
      analysis: targetContract.analysis,
      upload_date: targetContract.uploadDate
    }
  }, [contracts, selectedContract])

  // Buscar contratos por texto
  const searchContracts = useCallback((query: string) => {
    if (!query.trim()) return contracts

    return contracts.filter(contract => 
      contract.text.toLowerCase().includes(query.toLowerCase()) ||
      contract.fileName?.toLowerCase().includes(query.toLowerCase()) ||
      contract.analysis?.summary.toLowerCase().includes(query.toLowerCase())
    )
  }, [contracts])

  // Remover contrato
  const removeContract = useCallback((contractId: string) => {
    const updatedContracts = contracts.filter(c => c.id !== contractId)
    saveContracts(updatedContracts)
    
    if (selectedContract?.id === contractId) {
      setSelectedContract(null)
    }
  }, [contracts, selectedContract, saveContracts])

  return {
    contracts,
    selectedContract,
    loading,
    error,
    loadContracts,
    addContract,
    analyzeContract,
    selectContract,
    getContextForChat,
    searchContracts,
    removeContract
  }
}