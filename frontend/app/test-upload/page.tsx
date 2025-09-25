'use client'

import React, { useState } from 'react'
import MockOCRUploader from '@/components/features/MockOCRUploader'
import { ContractAnalysis } from '@/lib/hooks/useApi'

interface UploadResult {
  file: File
  extractedText: string
  analysis?: ContractAnalysis
}

export default function TestUploadPage() {
  const [uploadResults, setUploadResults] = useState<UploadResult[]>([])

  const handleAnalysisComplete = (result: UploadResult) => {
    setUploadResults(prev => [result, ...prev])
  }

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="bg-white rounded-lg shadow-sm p-8">
          <div className="text-center mb-8">
            <h1 className="text-3xl font-bold text-gray-900 mb-2">
              🚀 Teste de Upload + OCR + Análise
            </h1>
            <p className="text-gray-600 max-w-2xl mx-auto">
              Sistema completo de upload de documentos com extração de texto simulada (Mock OCR) 
              e análise automática de contratos usando IA. Suporta PDF, DOC, DOCX, TXT e imagens.
            </p>
          </div>

          {/* Componente de Upload */}
          <div className="mb-8">
            <MockOCRUploader 
              onAnalysisComplete={handleAnalysisComplete}
              className="max-w-2xl mx-auto"
            />
          </div>

          {/* Histórico de Resultados */}
          {uploadResults.length > 0 && (
            <div className="border-t pt-8">
              <h2 className="text-xl font-semibold text-gray-900 mb-6">
                📋 Histórico de Análises ({uploadResults.length})
              </h2>
              
              <div className="space-y-6">
                {uploadResults.map((result, index) => (
                  <div key={index} className="bg-gray-50 rounded-lg p-6">
                    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                      {/* Informações do Arquivo */}
                      <div>
                        <h3 className="text-lg font-medium text-gray-900 mb-4">
                          📄 Documento
                        </h3>
                        <div className="space-y-2 text-sm">
                          <p><strong>Nome:</strong> {result.file.name}</p>
                          <p><strong>Tamanho:</strong> {(result.file.size / 1024).toFixed(1)} KB</p>
                          <p><strong>Tipo:</strong> {result.file.type || 'Não identificado'}</p>
                        </div>
                        
                        <div className="mt-4">
                          <p className="text-sm font-medium text-gray-900 mb-2">Texto extraído:</p>
                          <div className="bg-white p-3 rounded border text-xs text-gray-700 max-h-40 overflow-y-auto">
                            {result.extractedText}
                          </div>
                        </div>
                      </div>

                      {/* Análise do Contrato */}
                      <div>
                        <h3 className="text-lg font-medium text-gray-900 mb-4">
                          🤖 Análise IA
                        </h3>
                        
                        {result.analysis ? (
                          <div className="space-y-4">
                            {/* Tipo e Risco */}
                            <div className="grid grid-cols-2 gap-4">
                              <div>
                                <p className="text-sm font-medium text-gray-600">Tipo de Contrato</p>
                                <p className="text-sm bg-blue-100 text-blue-800 px-2 py-1 rounded">
                                  {result.analysis.contract_type}
                                </p>
                              </div>
                              <div>
                                <p className="text-sm font-medium text-gray-600">Nível de Risco</p>
                                <span className={`text-sm px-2 py-1 rounded font-medium ${
                                  result.analysis.risk_assessment.overall_risk === 'ALTO_RISCO' 
                                    ? 'bg-red-100 text-red-800'
                                    : result.analysis.risk_assessment.overall_risk === 'MEDIO_RISCO'
                                    ? 'bg-yellow-100 text-yellow-800'
                                    : 'bg-green-100 text-green-800'
                                }`}>
                                  {result.analysis.risk_assessment.overall_risk}
                                </span>
                              </div>
                            </div>

                            {/* Score de Risco */}
                            <div>
                              <p className="text-sm font-medium text-gray-600 mb-2">Score de Risco</p>
                              <div className="bg-gray-200 rounded-full h-2">
                                <div 
                                  className={`h-2 rounded-full ${
                                    result.analysis.risk_assessment.risk_score >= 70 
                                      ? 'bg-red-500' 
                                      : result.analysis.risk_assessment.risk_score >= 40
                                      ? 'bg-yellow-500'
                                      : 'bg-green-500'
                                  }`}
                                  style={{ width: `${result.analysis.risk_assessment.risk_score}%` }}
                                ></div>
                              </div>
                              <p className="text-xs text-gray-500 mt-1">
                                {result.analysis.risk_assessment.risk_score}/100
                              </p>
                            </div>

                            {/* Cláusulas Problemáticas */}
                            {result.analysis.problematic_clauses.length > 0 && (
                              <div>
                                <p className="text-sm font-medium text-gray-600 mb-2">
                                  ⚠️ Cláusulas Problemáticas ({result.analysis.problematic_clauses.length})
                                </p>
                                <div className="space-y-2 max-h-32 overflow-y-auto">
                                  {result.analysis.problematic_clauses.map((clause, idx) => (
                                    <div key={idx} className="bg-red-50 border border-red-200 rounded p-2">
                                      <p className="text-xs font-medium text-red-800">
                                        {clause.issue_type}
                                      </p>
                                      <p className="text-xs text-red-600">
                                        {clause.explanation.substring(0, 100)}...
                                      </p>
                                    </div>
                                  ))}
                                </div>
                              </div>
                            )}

                            {/* Resumo */}
                            <div>
                              <p className="text-sm font-medium text-gray-600 mb-2">Resumo</p>
                              <p className="text-xs text-gray-700 bg-white p-2 rounded border">
                                {result.analysis.summary.substring(0, 200)}...
                              </p>
                            </div>
                          </div>
                        ) : (
                          <p className="text-sm text-gray-500 italic">
                            Análise não disponível
                          </p>
                        )}
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Instruções */}
          <div className="mt-8 bg-blue-50 border border-blue-200 rounded-lg p-6">
            <h3 className="text-lg font-medium text-blue-900 mb-3">
              💡 Como funciona este teste
            </h3>
            <div className="text-sm text-blue-800 space-y-2">
              <p>1. <strong>Upload:</strong> Arraste um arquivo ou clique para selecionar</p>
              <p>2. <strong>OCR Mock:</strong> O sistema simula extração de texto baseada no tipo de arquivo</p>
              <p>3. <strong>Análise IA:</strong> O texto é enviado para o backend que simula análise com IA</p>
              <p>4. <strong>Resultado:</strong> Você recebe análise completa com riscos e recomendações</p>
            </div>
            
            <div className="mt-4 text-xs text-blue-600">
              <p><strong>Tipos suportados:</strong> PDF (telecom), DOC/DOCX (locação), TXT (bancário), outros (genérico)</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}