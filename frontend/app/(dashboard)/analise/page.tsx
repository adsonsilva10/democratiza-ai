'use client'

import { useState } from 'react'
import Link from 'next/link'

export default function AnalisePage() {
  const [isDragging, setIsDragging] = useState(false)
  const [uploadedFiles, setUploadedFiles] = useState<File[]>([])
  const [analysisStep, setAnalysisStep] = useState('upload') // 'upload', 'processing', 'completed'

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault()
    setIsDragging(true)
  }

  const handleDragLeave = (e: React.DragEvent) => {
    e.preventDefault()
    setIsDragging(false)
  }

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault()
    setIsDragging(false)
    
    const files = Array.from(e.dataTransfer.files)
    setUploadedFiles(files)
    
    // Simular processamento
    setAnalysisStep('processing')
    setTimeout(() => setAnalysisStep('completed'), 3000)
  }

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = Array.from(e.target.files || [])
    setUploadedFiles(files)
    
    // Simular processamento
    setAnalysisStep('processing')
    setTimeout(() => setAnalysisStep('completed'), 3000)
  }

  return (
    <div className="w-full max-w-5xl mx-auto">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-2xl sm:text-3xl lg:text-4xl font-bold text-gray-900 mb-4">
          📊 Análise de Contratos
        </h1>
        <p className="text-gray-600 text-base sm:text-lg">
          Envie seus contratos e receba uma análise jurídica detalhada em minutos
        </p>
      </div>

      {analysisStep === 'upload' && (
        <div className="space-y-8">
          {/* Área de Upload Principal */}
          <div className="bg-white rounded-xl shadow-lg p-8">
            <div
              onDragOver={handleDragOver}
              onDragLeave={handleDragLeave}
              onDrop={handleDrop}
              className={`border-2 border-dashed rounded-xl p-12 text-center transition-all duration-200 ${
                isDragging
                  ? 'border-blue-500 bg-blue-50'
                  : 'border-gray-300 hover:border-gray-400 hover:bg-gray-50'
              }`}
            >
              <div className="text-6xl mb-6">📄</div>
              <h3 className="text-xl font-bold text-gray-900 mb-4">
                Arraste e solte seu contrato aqui
              </h3>
              <p className="text-gray-600 mb-8 max-w-md mx-auto">
                Ou clique no botão abaixo para selecionar arquivos do seu computador
              </p>
              
              <div className="space-y-4">
                <label className="inline-block">
                  <input
                    type="file"
                    multiple
                    accept=".pdf,.doc,.docx,.jpg,.jpeg,.png"
                    onChange={handleFileSelect}
                    className="hidden"
                  />
                  <span className="bg-blue-600 text-white px-8 py-4 rounded-xl font-semibold hover:bg-blue-700 cursor-pointer transition-colors inline-flex items-center gap-3">
                    <span className="text-xl">📁</span>
                    Selecionar arquivos
                  </span>
                </label>
                
                <p className="text-sm text-gray-500">
                  Formatos aceitos: PDF, DOC, DOCX, JPG, PNG (máx. 10MB por arquivo)
                </p>
              </div>
            </div>
          </div>

          {/* Recursos e Benefícios */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="bg-white p-6 rounded-xl shadow-lg">
              <div className="text-3xl mb-4">🤖</div>
              <h3 className="font-semibold text-gray-900 mb-2">IA Especializada</h3>
              <p className="text-gray-600 text-sm">
                Nossa inteligência artificial é treinada especificamente em contratos brasileiros
              </p>
            </div>
            
            <div className="bg-white p-6 rounded-xl shadow-lg">
              <div className="text-3xl mb-4">⚡</div>
              <h3 className="font-semibold text-gray-900 mb-2">Análise Rápida</h3>
              <p className="text-gray-600 text-sm">
                Receba um relatório completo em menos de 5 minutos
              </p>
            </div>
            
            <div className="bg-white p-6 rounded-xl shadow-lg">
              <div className="text-3xl mb-4">🔒</div>
              <h3 className="font-semibold text-gray-900 mb-2">100% Seguro</h3>
              <p className="text-gray-600 text-sm">
                Seus documentos são criptografados e podem ser excluídos a qualquer momento
              </p>
            </div>
          </div>

          {/* Como Funciona */}
          <div className="bg-white rounded-xl shadow-lg p-8">
            <h2 className="text-2xl font-bold text-gray-900 mb-8 text-center">
              Como funciona a análise?
            </h2>
            
            <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
              <div className="text-center">
                <div className="bg-blue-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
                  <span className="text-2xl">📤</span>
                </div>
                <h3 className="font-semibold text-gray-900 mb-2">1. Upload</h3>
                <p className="text-gray-600 text-sm">
                  Envie seu contrato em PDF, Word ou imagem
                </p>
              </div>
              
              <div className="text-center">
                <div className="bg-green-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
                  <span className="text-2xl">🔍</span>
                </div>
                <h3 className="font-semibold text-gray-900 mb-2">2. Análise</h3>
                <p className="text-gray-600 text-sm">
                  IA examina cada cláusula identificando riscos
                </p>
              </div>
              
              <div className="text-center">
                <div className="bg-yellow-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
                  <span className="text-2xl">📊</span>
                </div>
                <h3 className="font-semibold text-gray-900 mb-2">3. Relatório</h3>
                <p className="text-gray-600 text-sm">
                  Receba análise detalhada com classificação de riscos
                </p>
              </div>
              
              <div className="text-center">
                <div className="bg-purple-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
                  <span className="text-2xl">💬</span>
                </div>
                <h3 className="font-semibold text-gray-900 mb-2">4. Chat</h3>
                <p className="text-gray-600 text-sm">
                  Tire dúvidas com nossa IA jurídica especializada
                </p>
              </div>
            </div>
          </div>
        </div>
      )}

      {analysisStep === 'processing' && (
        <div className="bg-white rounded-xl shadow-lg p-12 text-center">
          <div className="text-6xl mb-6 animate-pulse">🤖</div>
          <h3 className="text-2xl font-bold text-gray-900 mb-4">
            Analisando seu contrato...
          </h3>
          <p className="text-gray-600 mb-8">
            Nossa IA está examinando cada cláusula. Isso deve levar alguns minutos.
          </p>
          
          <div className="flex items-center justify-center space-x-2 mb-8">
            <div className="w-3 h-3 bg-blue-600 rounded-full animate-pulse"></div>
            <div className="w-3 h-3 bg-blue-600 rounded-full animate-pulse delay-75"></div>
            <div className="w-3 h-3 bg-blue-600 rounded-full animate-pulse delay-150"></div>
          </div>
          
          <div className="space-y-3 text-sm text-gray-500">
            <p>✅ Documento recebido e validado</p>
            <p>🔍 Identificando tipo de contrato...</p>
            <p>⚡ Analisando cláusulas e riscos...</p>
          </div>
        </div>
      )}

      {analysisStep === 'completed' && (
        <div className="space-y-8">
          <div className="bg-white rounded-xl shadow-lg p-8">
            <div className="text-center mb-8">
              <div className="text-6xl mb-4">✅</div>
              <h3 className="text-2xl font-bold text-gray-900 mb-4">
                Análise Concluída!
              </h3>
              <p className="text-gray-600">
                Seu contrato foi analisado com sucesso. Confira os resultados abaixo.
              </p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
              <div className="bg-red-50 p-6 rounded-lg border border-red-200">
                <h4 className="font-semibold text-red-800 mb-2">Alto Risco</h4>
                <div className="text-3xl font-bold text-red-600">3</div>
                <p className="text-red-700 text-sm">Cláusulas identificadas</p>
              </div>
              
              <div className="bg-yellow-50 p-6 rounded-lg border border-yellow-200">
                <h4 className="font-semibold text-yellow-800 mb-2">Médio Risco</h4>
                <div className="text-3xl font-bold text-yellow-600">2</div>
                <p className="text-yellow-700 text-sm">Pontos de atenção</p>
              </div>
              
              <div className="bg-green-50 p-6 rounded-lg border border-green-200">
                <h4 className="font-semibold text-green-800 mb-2">Score Geral</h4>
                <div className="text-3xl font-bold text-green-600">65%</div>
                <p className="text-green-700 text-sm">Índice de confiança</p>
              </div>
            </div>

            <div className="flex flex-col sm:flex-row gap-4">
              <button className="flex-1 bg-blue-600 text-white px-6 py-3 rounded-xl font-semibold hover:bg-blue-700 transition-colors">
                Ver Relatório Completo
              </button>
              <Link 
                href="/dashboard/chat"
                className="flex-1 border border-gray-300 text-gray-700 px-6 py-3 rounded-xl font-semibold hover:bg-gray-50 transition-colors text-center"
              >
                💬 Tirar dúvidas no Chat IA
              </Link>
              <button 
                onClick={() => setAnalysisStep('upload')}
                className="flex-1 border border-blue-600 text-blue-600 px-6 py-3 rounded-xl font-semibold hover:bg-blue-50 transition-colors"
              >
                Analisar outro contrato
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}