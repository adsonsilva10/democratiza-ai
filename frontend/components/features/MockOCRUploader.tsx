import React, { useState, useCallback, useRef } from 'react'
import { useContractAnalysis, ContractAnalysis } from '@/lib/hooks/useApi'

interface UploadResult {
  file: File
  extractedText: string
  analysis?: ContractAnalysis
}

interface MockOCRUploaderProps {
  onAnalysisComplete?: (result: UploadResult) => void
  className?: string
}

const MockOCRUploader: React.FC<MockOCRUploaderProps> = ({
  onAnalysisComplete,
  className = ""
}) => {
  const [isDragging, setIsDragging] = useState(false)
  const [uploadResult, setUploadResult] = useState<UploadResult | null>(null)
  const [isProcessing, setIsProcessing] = useState(false)
  const fileInputRef = useRef<HTMLInputElement>(null)
  
  const { analyzeContract, loading: analysisLoading } = useContractAnalysis()

  // Simulação de OCR - extrai texto de diferentes tipos de arquivo
  const mockOCRExtraction = useCallback(async (file: File): Promise<string> => {
    return new Promise((resolve) => {
      setTimeout(() => {
        const fileExtension = file.name.split('.').pop()?.toLowerCase()
        
        let extractedText = ''
        
        switch (fileExtension) {
          case 'pdf':
            extractedText = `
CONTRATO DE PRESTAÇÃO DE SERVIÇOS DE TELECOMUNICAÇÕES

Pelo presente instrumento particular, as partes:

CONTRATANTE: [Nome do cliente extraído via OCR]
CONTRATADA: Telecom XYZ Ltda.

CLÁUSULA 1ª - DO OBJETO
A CONTRATADA compromete-se a prestar serviços de internet banda larga com velocidade de até 100 Mbps.

CLÁUSULA 2ª - DA PERMANÊNCIA  
O presente contrato tem prazo de permanência mínima de 24 (vinte e quatro) meses.

CLÁUSULA 3ª - DA RESCISÃO
Em caso de rescisão antecipada pelo CONTRATANTE, será devida multa compensatória no valor de R$ 2.000,00 (dois mil reais).

CLÁUSULA 4ª - DAS RESPONSABILIDADES
A CONTRATADA não se responsabiliza por instabilidades na conexão decorrentes de fatores externos.

CLÁUSULA 5ª - DO REAJUSTE
Os preços serão reajustados anualmente pelo IGP-M, sem limitação.

Local e Data: São Paulo, ${new Date().toLocaleDateString('pt-BR')}
            `.trim()
            break
            
          case 'docx':
          case 'doc':
            extractedText = `
CONTRATO DE LOCAÇÃO RESIDENCIAL

LOCADOR: Imobiliária ABC Ltda.
LOCATÁRIO: [Nome extraído via OCR do documento]

CLÁUSULA 1ª: O prazo de locação é de 30 meses, improrrogável.

CLÁUSULA 2ª: O valor do aluguel é de R$ 3.500,00 mensais, reajustável anualmente pelo IGPM.

CLÁUSULA 3ª: É exigido depósito caução no valor de 3 aluguéis.

CLÁUSULA 4ª: O locatário se responsabiliza por todas as despesas de condomínio, IPTU e manutenção.

CLÁUSULA 5ª: É vedada a sublocação total ou parcial do imóvel.

CLÁUSULA 6ª: O locatário não poderá fazer alterações estruturais sem autorização.
            `.trim()
            break
            
          case 'txt':
            extractedText = `
CONTRATO DE ABERTURA DE CONTA CORRENTE

BANCO: Banco Fictício S.A.
CLIENTE: [Dados extraídos do documento]

CONDIÇÕES GERAIS:

1. Taxa de manutenção mensal: R$ 45,00
2. Limite de cheque especial pré-aprovado: R$ 5.000,00
3. Juros do cheque especial: 8,99% ao mês
4. Tarifa por TED: R$ 25,00
5. Saldo mínimo exigido: R$ 500,00

CLÁUSULAS ESPECIAIS:
- Em caso de saldo negativo por mais de 60 dias, o banco poderá encerrar a conta automaticamente
- O cliente autoriza débito automático de todas as taxas e tarifas
- Foro de eleição: Comarca da Capital/SP
            `.trim()
            break
            
          default:
            extractedText = `
DOCUMENTO GENÉRICO EXTRAÍDO VIA OCR

[Texto simulado extraído de ${file.name}]

Este é um exemplo de texto que seria extraído de um documento através de tecnologia OCR (Optical Character Recognition).

O sistema conseguiu identificar este documento como um contrato e extraiu o seguinte conteúdo para análise:

- Partes envolvidas identificadas
- Cláusulas contratuais detectadas  
- Valores monetários reconhecidos
- Prazos e condições específicas

Qualidade de extração: 95% (simulado)
Confiança no reconhecimento: Alta
            `.trim()
        }
        
        resolve(extractedText)
      }, 1500) // Simula tempo de processamento OCR
    })
  }, [])

  const handleFiles = useCallback(async (files: FileList | File[]) => {
    const fileArray = Array.from(files)
    if (fileArray.length === 0) return

    const file = fileArray[0] // Processa apenas o primeiro arquivo
    setIsProcessing(true)

    try {
      // 1. Simular OCR
      console.log(`📄 Iniciando OCR para: ${file.name}`)
      const extractedText = await mockOCRExtraction(file)
      
      // 2. Criar resultado inicial
      const result: UploadResult = {
        file,
        extractedText
      }
      
      // 3. Analisar com IA
      console.log(`🤖 Iniciando análise de IA...`)
      try {
        const analysisResult = await analyzeContract(extractedText)
        result.analysis = analysisResult
      } catch (error) {
        console.error('Erro na análise:', error)
        result.analysis = {
          contract_type: 'Erro',
          risk_assessment: {
            overall_risk: 'ALTO_RISCO',
            risk_score: 0
          },
          problematic_clauses: [],
          recommendations: ['Erro ao processar análise. Tente novamente.'],
          summary: 'Não foi possível analisar o contrato devido a um erro.'
        }
      }
      
      setUploadResult(result)
      onAnalysisComplete?.(result)
      
    } catch (error) {
      console.error('Erro no processamento:', error)
    } finally {
      setIsProcessing(false)
    }
  }, [mockOCRExtraction, analyzeContract, onAnalysisComplete])

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault()
    setIsDragging(false)
    
    const files = e.dataTransfer.files
    handleFiles(files)
  }, [handleFiles])

  const handleFileInput = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files
    if (files) {
      handleFiles(files)
    }
  }, [handleFiles])

  const isLoading = isProcessing || analysisLoading

  return (
    <div className={`space-y-6 ${className}`}>
      {/* Área de Upload */}
      <div
        className={`
          relative border-2 border-dashed rounded-lg p-8 text-center transition-all duration-200
          ${isDragging ? 'border-blue-500 bg-blue-50' : 'border-gray-300 hover:border-gray-400'}
          ${isLoading ? 'opacity-50 pointer-events-none' : 'cursor-pointer'}
        `}
        onDragOver={(e) => {
          e.preventDefault()
          setIsDragging(true)
        }}
        onDragLeave={() => setIsDragging(false)}
        onDrop={handleDrop}
        onClick={() => !isLoading && fileInputRef.current?.click()}
      >
        <input
          ref={fileInputRef}
          type="file"
          className="hidden"
          accept=".pdf,.doc,.docx,.txt,.jpg,.jpeg,.png"
          onChange={handleFileInput}
          disabled={isLoading}
        />
        
        {isLoading ? (
          <div className="space-y-4">
            <div className="animate-spin mx-auto w-12 h-12 border-4 border-blue-500 border-t-transparent rounded-full"></div>
            <div className="space-y-2">
              <p className="text-lg font-medium text-gray-900">
                {isProcessing ? 'Extraindo texto do documento...' : 'Analisando contrato...'}
              </p>
              <p className="text-sm text-gray-500">
                {isProcessing ? 'OCR em andamento' : 'Análise jurídica com IA'}
              </p>
            </div>
          </div>
        ) : (
          <div className="space-y-4">
            <div className="mx-auto w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center">
              <svg className="w-8 h-8 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
              </svg>
            </div>
            <div>
              <p className="text-lg font-medium text-gray-900">
                Arraste seu contrato aqui ou clique para selecionar
              </p>
              <p className="text-sm text-gray-500 mt-1">
                Suporta: PDF, DOC, DOCX, TXT, JPG, PNG • Máx. 10MB
              </p>
            </div>
          </div>
        )}
      </div>

      {/* Resultado do Upload */}
      {uploadResult && (
        <div className="bg-green-50 border border-green-200 rounded-lg p-6">
          <div className="flex items-start space-x-4">
            <div className="flex-shrink-0">
              <svg className="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <div className="flex-1 min-w-0">
              <h3 className="text-lg font-medium text-green-900 mb-2">
                ✅ Documento processado com sucesso!
              </h3>
              
              <div className="space-y-3">
                <div>
                  <p className="text-sm font-medium text-green-800">Arquivo:</p>
                  <p className="text-sm text-green-700">{uploadResult.file.name}</p>
                </div>
                
                <div>
                  <p className="text-sm font-medium text-green-800">Texto extraído:</p>
                  <p className="text-sm text-green-700 bg-white p-3 rounded border max-h-32 overflow-y-auto">
                    {uploadResult.extractedText.substring(0, 200)}...
                  </p>
                </div>
                
                {uploadResult.analysis && (
                  <div>
                    <p className="text-sm font-medium text-green-800">Análise:</p>
                    <div className="text-sm bg-white p-3 rounded border">
                      <p><strong>Tipo:</strong> {uploadResult.analysis.contract_type}</p>
                      <p><strong>Risco:</strong> 
                        <span className={`ml-1 px-2 py-1 rounded text-xs font-medium ${
                          uploadResult.analysis.risk_assessment.overall_risk === 'ALTO_RISCO' 
                            ? 'bg-red-100 text-red-800'
                            : uploadResult.analysis.risk_assessment.overall_risk === 'MEDIO_RISCO'
                            ? 'bg-yellow-100 text-yellow-800'
                            : 'bg-green-100 text-green-800'
                        }`}>
                          {uploadResult.analysis.risk_assessment.overall_risk}
                        </span>
                      </p>
                      <p><strong>Problemas encontrados:</strong> {uploadResult.analysis.problematic_clauses.length}</p>
                    </div>
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

export default MockOCRUploader