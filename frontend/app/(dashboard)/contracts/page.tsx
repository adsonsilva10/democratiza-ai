'use client'

import { useState } from 'react'
import UploadManager from '@/components/features/UploadManager'

export default function ContractsPage() {
  const [selectedContractId, setSelectedContractId] = useState<string | null>(null)

  const handleContractUploaded = (contractId: string) => {
    console.log('Contract uploaded:', contractId)
    setSelectedContractId(contractId)
  }

  return (
    <div className="container mx-auto py-8 px-4">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">
          📋 Análise de Contratos
        </h1>
        <p className="text-lg text-gray-600">
          Faça upload e analise seus contratos com IA especializada
        </p>
      </div>

      <UploadManager 
        onContractUploaded={handleContractUploaded}
        maxFiles={5}
        maxFileSize={10}
      />

      {selectedContractId && (
        <div className="mt-8 p-4 bg-green-50 border border-green-200 rounded-lg">
          <h3 className="font-semibold text-green-800 mb-2">
            ✅ Upload Realizado com Sucesso!
          </h3>
          <p className="text-green-700 text-sm">
            Contrato ID: {selectedContractId} - A análise está em andamento.
          </p>
        </div>
      )}
    </div>
  )
}