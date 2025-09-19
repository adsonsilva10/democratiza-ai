// Report Viewer Component
'use client'

import { useState } from 'react'
import apiClient, { Contract } from '@/lib/api'

interface ReportViewerProps {
  contract: Contract
}

export default function ReportViewer({ contract }: ReportViewerProps) {
  const [activeTab, setActiveTab] = useState<'overview' | 'risks' | 'clauses' | 'recommendations'>('overview')

  const analysis = contract.analysis

  const getRiskLevelColor = (level: string) => {
    switch (level) {
      case 'high':
        return 'bg-red-100 text-red-800 border-red-200'
      case 'medium':
        return 'bg-yellow-100 text-yellow-800 border-yellow-200'
      case 'low':
        return 'bg-green-100 text-green-800 border-green-200'
      default:
        return 'bg-gray-100 text-gray-800 border-gray-200'
    }
  }

  const getRiskIcon = (level: string) => {
    switch (level) {
      case 'high':
        return '🔴'
      case 'medium':
        return '🟡'
      case 'low':
        return '🟢'
      default:
        return '⚪'
    }
  }

  const TabButton = ({ tab, label }: { tab: typeof activeTab; label: string }) => (
    <button
      onClick={() => setActiveTab(tab)}
      className={`px-4 py-2 rounded-lg font-medium transition-colors ${
        activeTab === tab
          ? 'bg-blue-500 text-white'
          : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
      }`}
    >
      {label}
    </button>
  )

  const OverviewTab = () => (
    <div className="space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="bg-gray-50 p-4 rounded-lg">
          <h3 className="text-lg font-semibold text-gray-900 mb-2">Tipo de Contrato</h3>
          <p className="font-semibold text-gray-900">{contract.type}</p>
        </div>
        
        <div className="bg-gray-50 p-4 rounded-lg">
          <h3 className="text-lg font-semibold text-gray-900 mb-2">Status</h3>
          <p className="font-semibold text-gray-900">{contract.status}</p>
        </div>
      </div>

      {analysis && (
        <div className="bg-blue-50 p-6 rounded-lg">
          <h3 className="text-xl font-bold text-blue-900 mb-4">Resumo da Análise</h3>
          <p className="text-blue-800 leading-relaxed">{analysis.summary}</p>
        </div>
      )}

      {!analysis && (
        <div className="bg-yellow-50 p-6 rounded-lg text-center">
          <h3 className="text-lg font-semibold text-yellow-800 mb-2">Análise Pendente</h3>
          <p className="text-yellow-700 mb-4">Este contrato ainda não foi analisado pela IA.</p>
        </div>
      )}
    </div>
  )

  const RisksTab = () => (
    <div className="space-y-4">
      {analysis?.risks?.map((risk: any, index: number) => (
        <div key={index} className={`p-4 border rounded-lg ${getRiskLevelColor(risk.level)}`}>
          <div className="flex items-start space-x-3">
            <span className="text-lg mt-1">{getRiskIcon(risk.level)}</span>
            <div className="flex-1">
              <div className="flex items-center space-x-2 mb-2">
                <span className="px-2 py-1 text-xs font-semibold rounded uppercase tracking-wide">
                  {risk.level === 'high' ? 'Alto Risco' : 
                   risk.level === 'medium' ? 'Médio Risco' : 'Baixo Risco'}
                </span>
              </div>
              <p className="font-medium mb-2">{risk.description}</p>
              {risk.clause && (
                <div className="mt-2 p-2 bg-white bg-opacity-50 rounded">
                  <p className="text-sm font-medium mb-1">Cláusula relacionada:</p>
                  <p className="text-sm italic">{risk.clause}</p>
                </div>
              )}
            </div>
          </div>
        </div>
      ))}
      
      {!analysis?.risks?.length && (
        <div className="text-center py-8">
          <span className="text-4xl mb-4 block">🔍</span>
          <p className="text-gray-500">Nenhum risco identificado ou análise ainda não realizada.</p>
        </div>
      )}
    </div>
  )

  const ClausesTab = () => (
    <div className="space-y-4">
      {analysis?.clauses?.map((clause: any, index: number) => (
        <div key={index} className={`p-4 border rounded-lg ${getRiskLevelColor(clause.risk_level)}`}>
          <div className="flex items-start space-x-3">
            <span className="text-lg mt-1">{getRiskIcon(clause.risk_level)}</span>
            <div className="flex-1">
              <div className="flex items-center space-x-2 mb-2">
                <h4 className="font-semibold text-gray-900">{clause.type}</h4>
                <span className="px-2 py-1 text-xs font-semibold rounded uppercase tracking-wide">
                  {clause.risk_level === 'high' ? 'Alto Risco' : 
                   clause.risk_level === 'medium' ? 'Médio Risco' : 'Baixo Risco'}
                </span>
              </div>
              <p className="text-gray-700 leading-relaxed">{clause.content}</p>
            </div>
          </div>
        </div>
      ))}
      
      {!analysis?.clauses?.length && (
        <div className="text-center py-8">
          <span className="text-4xl mb-4 block">📄</span>
          <p className="text-gray-500">Nenhuma cláusula analisada ainda.</p>
        </div>
      )}
    </div>
  )

  const RecommendationsTab = () => (
    <div className="space-y-4">
      {analysis?.recommendations?.map((recommendation: string, index: number) => (
        <div key={index} className="p-4 bg-green-50 border border-green-200 rounded-lg">
          <div className="flex items-start space-x-3">
            <span className="text-lg mt-1">💡</span>
            <div className="flex-1">
              <p className="text-green-800 leading-relaxed">{recommendation}</p>
            </div>
          </div>
        </div>
      ))}
      
      {!analysis?.recommendations?.length && (
        <div className="text-center py-8">
          <span className="text-4xl mb-4 block">💡</span>
          <p className="text-gray-500">Nenhuma recomendação disponível ainda.</p>
        </div>
      )}
    </div>
  )

  return (
    <div className="max-w-4xl mx-auto p-6 bg-white min-h-screen">
      <div className="mb-8">
        <div className="flex items-center space-x-2 text-sm text-gray-500 mb-2">
          <span>📄</span>
          <span>Relatório de Análise</span>
        </div>
        <h1 className="text-2xl font-bold text-gray-900">{contract.name}</h1>
        <p className="text-gray-600 mt-2">
          Criado em {new Date(contract.created_at).toLocaleDateString('pt-BR')}
        </p>
      </div>

      <div className="mb-6">
        <div className="flex space-x-2 overflow-x-auto pb-2">
          <TabButton tab="overview" label="📊 Visão Geral" />
          <TabButton tab="risks" label="⚠️ Riscos" />
          <TabButton tab="clauses" label="📋 Cláusulas" />
          <TabButton tab="recommendations" label="💡 Recomendações" />
        </div>
      </div>

      <div className="bg-white rounded-lg border border-gray-200 p-6">
        {activeTab === 'overview' && <OverviewTab />}
        {activeTab === 'risks' && <RisksTab />}
        {activeTab === 'clauses' && <ClausesTab />}
        {activeTab === 'recommendations' && <RecommendationsTab />}
      </div>
    </div>
  )
}
