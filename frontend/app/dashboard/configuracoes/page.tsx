'use client'

import { useState } from 'react'

export default function ConfiguracoesPage() {
  const [activeTab, setActiveTab] = useState('perfil')
  const [formData, setFormData] = useState({
    nome: 'João Silva',
    email: 'joao.silva@email.com',
    telefone: '(11) 99999-9999',
    notificacoes: {
      email: true,
      sms: false,
      push: true
    },
    analise: {
      autoAnalise: true,
      nivelDetalhe: 'completo',
      alertasRisco: true
    }
  })

  const tabs = [
    { id: 'perfil', label: 'Perfil', icon: '👤' },
    { id: 'notificacoes', label: 'Notificações', icon: '🔔' },
    { id: 'analise', label: 'Análise', icon: '🔍' },
    { id: 'seguranca', label: 'Segurança', icon: '🔒' }
  ]

  const handleInputChange = (field: string, value: any) => {
    setFormData(prev => ({
      ...prev,
      [field]: value
    }))
  }

  const handleNestedChange = (section: string, field: string, value: any) => {
    setFormData(prev => ({
      ...prev,
      [section]: {
        ...prev[section as keyof typeof prev] as any,
        [field]: value
      }
    }))
  }

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold text-gray-900 mb-6">Configurações</h1>

      <div className="flex flex-col lg:flex-row gap-8">
        {/* Sidebar de navegação */}
        <div className="lg:w-64">
          <nav className="space-y-2">
            {tabs.map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`w-full flex items-center gap-3 px-4 py-3 text-left rounded-lg transition-colors ${
                  activeTab === tab.id
                    ? 'bg-blue-100 text-blue-700 font-medium'
                    : 'text-gray-700 hover:bg-gray-100'
                }`}
              >
                <span className="text-lg">{tab.icon}</span>
                {tab.label}
              </button>
            ))}
          </nav>
        </div>

        {/* Conteúdo das configurações */}
        <div className="flex-1">
          <div className="bg-white rounded-lg shadow">
            
            {/* Aba Perfil */}
            {activeTab === 'perfil' && (
              <div className="p-6">
                <h2 className="text-lg font-semibold text-gray-900 mb-6">Informações do Perfil</h2>
                
                <div className="space-y-6">
                  <div className="flex items-center gap-6">
                    <div className="w-20 h-20 bg-blue-100 rounded-full flex items-center justify-center">
                      <span className="text-2xl text-blue-600">👤</span>
                    </div>
                    <div>
                      <button className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors">
                        Alterar Foto
                      </button>
                      <p className="text-sm text-gray-500 mt-1">JPG, PNG até 2MB</p>
                    </div>
                  </div>

                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        Nome Completo
                      </label>
                      <input
                        type="text"
                        value={formData.nome}
                        onChange={(e) => handleInputChange('nome', e.target.value)}
                        className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                      />
                    </div>

                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        Email
                      </label>
                      <input
                        type="email"
                        value={formData.email}
                        onChange={(e) => handleInputChange('email', e.target.value)}
                        className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                      />
                    </div>

                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        Telefone
                      </label>
                      <input
                        type="tel"
                        value={formData.telefone}
                        onChange={(e) => handleInputChange('telefone', e.target.value)}
                        className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                      />
                    </div>
                  </div>

                  <div className="flex justify-end gap-4 pt-4">
                    <button className="px-4 py-2 text-gray-600 hover:text-gray-800">
                      Cancelar
                    </button>
                    <button className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors">
                      Salvar Alterações
                    </button>
                  </div>
                </div>
              </div>
            )}

            {/* Aba Notificações */}
            {activeTab === 'notificacoes' && (
              <div className="p-6">
                <h2 className="text-lg font-semibold text-gray-900 mb-6">Preferências de Notificação</h2>
                
                <div className="space-y-6">
                  <div className="flex items-center justify-between">
                    <div>
                      <h3 className="font-medium text-gray-900">Notificações por Email</h3>
                      <p className="text-sm text-gray-500">Receba updates sobre suas análises por email</p>
                    </div>
                    <button
                      onClick={() => handleNestedChange('notificacoes', 'email', !formData.notificacoes.email)}
                      className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${
                        formData.notificacoes.email ? 'bg-blue-600' : 'bg-gray-200'
                      }`}
                    >
                      <span className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
                        formData.notificacoes.email ? 'translate-x-6' : 'translate-x-1'
                      }`} />
                    </button>
                  </div>

                  <div className="flex items-center justify-between">
                    <div>
                      <h3 className="font-medium text-gray-900">SMS</h3>
                      <p className="text-sm text-gray-500">Alertas importantes via SMS</p>
                    </div>
                    <button
                      onClick={() => handleNestedChange('notificacoes', 'sms', !formData.notificacoes.sms)}
                      className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${
                        formData.notificacoes.sms ? 'bg-blue-600' : 'bg-gray-200'
                      }`}
                    >
                      <span className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
                        formData.notificacoes.sms ? 'translate-x-6' : 'translate-x-1'
                      }`} />
                    </button>
                  </div>

                  <div className="flex items-center justify-between">
                    <div>
                      <h3 className="font-medium text-gray-900">Notificações Push</h3>
                      <p className="text-sm text-gray-500">Notificações instantâneas no navegador</p>
                    </div>
                    <button
                      onClick={() => handleNestedChange('notificacoes', 'push', !formData.notificacoes.push)}
                      className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${
                        formData.notificacoes.push ? 'bg-blue-600' : 'bg-gray-200'
                      }`}
                    >
                      <span className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
                        formData.notificacoes.push ? 'translate-x-6' : 'translate-x-1'
                      }`} />
                    </button>
                  </div>
                </div>
              </div>
            )}

            {/* Aba Análise */}
            {activeTab === 'analise' && (
              <div className="p-6">
                <h2 className="text-lg font-semibold text-gray-900 mb-6">Configurações de Análise</h2>
                
                <div className="space-y-6">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-3">
                      Nível de Detalhamento
                    </label>
                    <div className="space-y-2">
                      {['basico', 'completo', 'avancado'].map((nivel) => (
                        <label key={nivel} className="flex items-center">
                          <input
                            type="radio"
                            name="nivelDetalhe"
                            value={nivel}
                            checked={formData.analise.nivelDetalhe === nivel}
                            onChange={(e) => handleNestedChange('analise', 'nivelDetalhe', e.target.value)}
                            className="mr-3 text-blue-600"
                          />
                          <span className="capitalize">{nivel}</span>
                        </label>
                      ))}
                    </div>
                  </div>

                  <div className="flex items-center justify-between">
                    <div>
                      <h3 className="font-medium text-gray-900">Análise Automática</h3>
                      <p className="text-sm text-gray-500">Iniciar análise automaticamente após upload</p>
                    </div>
                    <button
                      onClick={() => handleNestedChange('analise', 'autoAnalise', !formData.analise.autoAnalise)}
                      className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${
                        formData.analise.autoAnalise ? 'bg-blue-600' : 'bg-gray-200'
                      }`}
                    >
                      <span className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
                        formData.analise.autoAnalise ? 'translate-x-6' : 'translate-x-1'
                      }`} />
                    </button>
                  </div>
                </div>
              </div>
            )}

            {/* Aba Segurança */}
            {activeTab === 'seguranca' && (
              <div className="p-6">
                <h2 className="text-lg font-semibold text-gray-900 mb-6">Segurança</h2>
                
                <div className="space-y-6">
                  <div>
                    <h3 className="font-medium text-gray-900 mb-4">Alterar Senha</h3>
                    <div className="space-y-4">
                      <input
                        type="password"
                        placeholder="Senha atual"
                        className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                      />
                      <input
                        type="password"
                        placeholder="Nova senha"
                        className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                      />
                      <input
                        type="password"
                        placeholder="Confirmar nova senha"
                        className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                      />
                      <button className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700">
                        Atualizar Senha
                      </button>
                    </div>
                  </div>

                  <div className="border-t pt-6">
                    <h3 className="font-medium text-gray-900 mb-4">Sessões Ativas</h3>
                    <div className="space-y-3">
                      <div className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                        <div>
                          <p className="font-medium">Chrome - Windows</p>
                          <p className="text-sm text-gray-500">São Paulo, Brasil - Agora</p>
                        </div>
                        <span className="text-green-600 text-sm">Atual</span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}