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
      push: true
    }
  })

  const tabs = [
    { id: 'perfil', label: 'Perfil', icon: '👤' },
    { id: 'notificacoes', label: 'Notificações', icon: '🔔' },
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
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-white">
      {/* Header moderno com breadcrumb */}
      <div className="bg-white border-b border-gray-200 px-4 md:px-6 py-4 md:py-6">
        <div className="flex flex-col gap-2">
          <nav className="text-sm text-gray-500">
            <span>Plataforma</span> <span className="mx-2">›</span> <span className="text-gray-900">Configurações</span>
          </nav>
          <div className="flex items-center gap-3">
            <div className="p-2 bg-blue-100 rounded-lg">
              <span className="text-xl text-blue-600">⚙️</span>
            </div>
            <div>
              <h1 className="text-xl md:text-2xl font-bold text-gray-900">Configurações</h1>
              <p className="text-sm text-gray-600">Gerencie suas preferências e configurações da conta</p>
            </div>
          </div>
        </div>
      </div>

      <div className="p-4 md:p-6">
        <div className="flex flex-col lg:flex-row gap-6 lg:gap-8 max-w-7xl mx-auto">
          {/* Navegação melhorada */}
          <div className="lg:w-72">
            {/* Mobile: Cards horizontais com scroll */}
            <div className="lg:hidden mb-6">
              <div className="flex gap-2 overflow-x-auto pb-2 scrollbar-hide">
                {tabs.map((tab) => (
                  <button
                    key={tab.id}
                    onClick={() => setActiveTab(tab.id)}
                    className={`flex-shrink-0 flex items-center gap-2 px-4 py-3 rounded-xl transition-all font-medium text-sm ${
                      activeTab === tab.id
                        ? 'bg-blue-600 text-white shadow-lg shadow-blue-200'
                        : 'bg-white text-gray-600 border border-gray-200 hover:bg-gray-50'
                    }`}
                  >
                    <span className="text-lg">{tab.icon}</span>
                    <span>{tab.label}</span>
                  </button>
                ))}
              </div>
            </div>
            
            {/* Desktop: Navegação sidebar aprimorada */}
            <nav className="hidden lg:block">
              <div className="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden">
                {tabs.map((tab, index) => (
                  <button
                    key={tab.id}
                    onClick={() => setActiveTab(tab.id)}
                    className={`w-full flex items-center gap-4 px-6 py-4 text-left transition-all border-b border-gray-50 last:border-0 ${
                      activeTab === tab.id
                        ? 'bg-gradient-to-r from-blue-50 to-indigo-50 text-blue-700 border-l-4 border-l-blue-500'
                        : 'text-gray-700 hover:bg-gray-50'
                    }`}
                  >
                    <div className={`p-2 rounded-lg ${
                      activeTab === tab.id 
                        ? 'bg-blue-100 text-blue-600' 
                        : 'bg-gray-100 text-gray-600'
                    }`}>
                      <span className="text-lg">{tab.icon}</span>
                    </div>
                    <div className="flex-1">
                      <span className="font-medium">{tab.label}</span>
                      <div className={`text-xs mt-0.5 ${
                        activeTab === tab.id ? 'text-blue-600' : 'text-gray-500'
                      }`}>
                        {index === 0 && 'Informações pessoais'}
                        {index === 1 && 'Alertas e comunicação'}
                        {index === 2 && 'Senha e privacidade'}
                      </div>
                    </div>
                  </button>
                ))}
              </div>
            </nav>
          </div>

          {/* Conteúdo das configurações */}
          <div className="flex-1">
            <div className="bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden">
              
              {/* Aba Perfil */}
              {activeTab === 'perfil' && (
                <div className="p-6 md:p-8">
                  <div className="flex items-center gap-3 mb-8">
                    <div className="p-2 bg-blue-100 rounded-lg">
                      <span className="text-xl text-blue-600">👤</span>
                    </div>
                    <div>
                      <h2 className="text-xl font-semibold text-gray-900">Informações do Perfil</h2>
                      <p className="text-sm text-gray-600">Gerencie suas informações pessoais e de contato</p>
                    </div>
                  </div>
                  
                  <div className="space-y-8">
                    {/* Seção Foto de Perfil */}
                    <div className="bg-gradient-to-br from-gray-50 to-white rounded-xl p-6 border border-gray-100">
                      <h3 className="text-lg font-medium text-gray-900 mb-4">Foto de Perfil</h3>
                      <div className="flex flex-col sm:flex-row items-center gap-6">
                        <div className="relative">
                          <div className="w-20 h-20 md:w-24 md:h-24 bg-gradient-to-br from-blue-100 to-blue-200 rounded-full flex items-center justify-center shadow-lg">
                            <span className="text-2xl md:text-3xl text-blue-600">👤</span>
                          </div>
                          <div className="absolute -bottom-1 -right-1 w-8 h-8 bg-green-500 rounded-full flex items-center justify-center shadow-md">
                            <span className="text-white text-sm">✓</span>
                          </div>
                        </div>
                        <div className="text-center sm:text-left">
                          <div className="space-y-2 mb-4">
                            <button className="bg-gradient-to-r from-blue-500 to-blue-600 text-white px-6 py-3 rounded-xl hover:from-blue-600 hover:to-blue-700 transition-all shadow-md hover:shadow-lg text-sm font-medium">
                              📸 Alterar Foto
                            </button>
                            <button className="block text-sm text-gray-500 hover:text-gray-700 underline">
                              Remover foto atual
                            </button>
                          </div>
                          <div className="text-xs text-gray-500 space-y-1">
                            <p>• Formatos aceitos: JPG, PNG, GIF</p>
                            <p>• Tamanho máximo: 2MB</p>
                            <p>• Resolução recomendada: 400x400px</p>
                          </div>
                        </div>
                      </div>
                    </div>

                    {/* Seção Informações Pessoais */}
                    <div className="bg-gradient-to-br from-gray-50 to-white rounded-xl p-6 border border-gray-100">
                      <h3 className="text-lg font-medium text-gray-900 mb-6">Informações Pessoais</h3>
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                        <div className="space-y-2">
                          <label className="flex items-center gap-2 text-sm font-medium text-gray-700">
                            <span>👨‍💼</span> Nome Completo
                          </label>
                          <input
                            type="text"
                            value={formData.nome}
                            onChange={(e) => handleInputChange('nome', e.target.value)}
                            className="w-full px-4 py-3 border border-gray-200 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all text-sm bg-white shadow-sm"
                            placeholder="Digite seu nome completo"
                          />
                        </div>

                        <div className="space-y-2">
                          <label className="flex items-center gap-2 text-sm font-medium text-gray-700">
                            <span>📧</span> Email
                          </label>
                          <input
                            type="email"
                            value={formData.email}
                            onChange={(e) => handleInputChange('email', e.target.value)}
                            className="w-full px-4 py-3 border border-gray-200 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all text-sm bg-white shadow-sm"
                            placeholder="seu@email.com"
                          />
                        </div>

                        <div className="space-y-2 md:col-span-1">
                          <label className="flex items-center gap-2 text-sm font-medium text-gray-700">
                            <span>📱</span> Telefone
                          </label>
                          <input
                            type="tel"
                            value={formData.telefone}
                            onChange={(e) => handleInputChange('telefone', e.target.value)}
                            className="w-full px-4 py-3 border border-gray-200 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all text-sm bg-white shadow-sm"
                            placeholder="(11) 99999-9999"
                          />
                        </div>

                        <div className="space-y-2">
                          <label className="flex items-center gap-2 text-sm font-medium text-gray-700">
                            <span>🌍</span> Localização
                          </label>
                          <select className="w-full px-4 py-3 border border-gray-200 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all text-sm bg-white shadow-sm">
                            <option>São Paulo, SP</option>
                            <option>Rio de Janeiro, RJ</option>
                            <option>Belo Horizonte, MG</option>
                          </select>
                        </div>
                      </div>
                    </div>

                    {/* Botões de Ação */}
                    <div className="flex flex-col sm:flex-row gap-4 justify-end pt-6 border-t border-gray-100">
                      <button className="px-6 py-3 text-gray-600 hover:text-gray-800 hover:bg-gray-50 rounded-xl transition-all text-sm font-medium">
                        ↶ Cancelar Alterações
                      </button>
                      <button className="px-8 py-3 bg-gradient-to-r from-green-500 to-green-600 text-white rounded-xl hover:from-green-600 hover:to-green-700 transition-all shadow-lg hover:shadow-xl text-sm font-medium">
                        ✅ Salvar Alterações
                      </button>
                    </div>
                  </div>
                </div>
              )}

              {/* Aba Notificações */}
              {activeTab === 'notificacoes' && (
                <div className="p-6 md:p-8">
                  <div className="flex items-center gap-3 mb-8">
                    <div className="p-2 bg-amber-100 rounded-lg">
                      <span className="text-xl text-amber-600">🔔</span>
                    </div>
                    <div>
                      <h2 className="text-xl font-semibold text-gray-900">Preferências de Notificação</h2>
                      <p className="text-sm text-gray-600">Configure como deseja receber informações importantes</p>
                    </div>
                  </div>
                  
                  <div className="space-y-6">
                    {/* Email Notifications */}
                    <div className="bg-gradient-to-br from-blue-50 to-indigo-50 rounded-xl p-6 border border-blue-100">
                      <div className="flex items-start justify-between gap-4">
                        <div className="flex-1">
                          <div className="flex items-center gap-3 mb-2">
                            <div className="w-10 h-10 bg-blue-100 rounded-lg flex items-center justify-center">
                              <span className="text-lg text-blue-600">📧</span>
                            </div>
                            <div>
                              <h3 className="font-semibold text-gray-900">Notificações por Email</h3>
                              <p className="text-sm text-gray-600">Receba updates sobre suas análises e relatórios</p>
                            </div>
                          </div>
                          <div className="ml-13 space-y-1 text-xs text-blue-600">
                            <p>• Relatórios de análise concluídos</p>
                            <p>• Alertas de vencimento de contratos</p>
                            <p>• Novidades da plataforma</p>
                          </div>
                        </div>
                        <div className="flex-shrink-0">
                          <button
                            onClick={() => handleNestedChange('notificacoes', 'email', !formData.notificacoes.email)}
                            className={`relative inline-flex h-7 w-12 items-center rounded-full transition-all shadow-sm ${
                              formData.notificacoes.email 
                                ? 'bg-gradient-to-r from-blue-500 to-blue-600 shadow-blue-200' 
                                : 'bg-gray-200 hover:bg-gray-300'
                            }`}
                          >
                            <span className={`inline-block h-5 w-5 transform rounded-full bg-white transition-transform shadow-sm ${
                              formData.notificacoes.email ? 'translate-x-6' : 'translate-x-1'
                            }`} />
                          </button>
                          <p className="text-xs text-center mt-1 font-medium">
                            {formData.notificacoes.email ? 'Ativo' : 'Inativo'}
                          </p>
                        </div>
                      </div>
                    </div>

                    {/* Push Notifications */}
                    <div className="bg-gradient-to-br from-purple-50 to-pink-50 rounded-xl p-6 border border-purple-100">
                      <div className="flex items-start justify-between gap-4">
                        <div className="flex-1">
                          <div className="flex items-center gap-3 mb-2">
                            <div className="w-10 h-10 bg-purple-100 rounded-lg flex items-center justify-center">
                              <span className="text-lg text-purple-600">🔔</span>
                            </div>
                            <div>
                              <h3 className="font-semibold text-gray-900">Notificações Push</h3>
                              <p className="text-sm text-gray-600">Alertas instantâneos no navegador</p>
                            </div>
                          </div>
                          <div className="ml-13 space-y-1 text-xs text-purple-600">
                            <p>• Progresso de análises em tempo real</p>
                            <p>• Mensagens do chat com agentes</p>
                            <p>• Lembretes de ações pendentes</p>
                          </div>
                        </div>
                        <div className="flex-shrink-0">
                          <button
                            onClick={() => handleNestedChange('notificacoes', 'push', !formData.notificacoes.push)}
                            className={`relative inline-flex h-7 w-12 items-center rounded-full transition-all shadow-sm ${
                              formData.notificacoes.push 
                                ? 'bg-gradient-to-r from-purple-500 to-purple-600 shadow-purple-200' 
                                : 'bg-gray-200 hover:bg-gray-300'
                            }`}
                          >
                            <span className={`inline-block h-5 w-5 transform rounded-full bg-white transition-transform shadow-sm ${
                              formData.notificacoes.push ? 'translate-x-6' : 'translate-x-1'
                            }`} />
                          </button>
                          <p className="text-xs text-center mt-1 font-medium">
                            {formData.notificacoes.push ? 'Ativo' : 'Inativo'}
                          </p>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              )}

              {/* Aba Segurança */}
              {activeTab === 'seguranca' && (
                <div className="p-6 md:p-8">
                  <div className="flex items-center gap-3 mb-8">
                    <div className="p-2 bg-red-100 rounded-lg">
                      <span className="text-xl text-red-600">🔒</span>
                    </div>
                    <div>
                      <h2 className="text-xl font-semibold text-gray-900">Segurança</h2>
                      <p className="text-sm text-gray-600">Mantenha sua conta protegida e segura</p>
                    </div>
                  </div>
                  
                  <div className="space-y-8">
                    {/* Alterar Senha */}
                    <div className="bg-gradient-to-br from-gray-50 to-white rounded-xl p-6 border border-gray-100">
                      <div className="flex items-center gap-3 mb-6">
                        <span className="text-2xl">🔑</span>
                        <div>
                          <h3 className="text-lg font-semibold text-gray-900">Alterar Senha</h3>
                          <p className="text-sm text-gray-600">Atualize sua senha para manter a segurança</p>
                        </div>
                      </div>
                      
                      <div className="space-y-4">
                        <div>
                          <label className="block text-sm font-medium text-gray-700 mb-2">Senha Atual</label>
                          <input
                            type="password"
                            placeholder="Digite sua senha atual"
                            className="w-full px-4 py-3 border border-gray-200 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all text-sm bg-white"
                          />
                        </div>
                        <div>
                          <label className="block text-sm font-medium text-gray-700 mb-2">Nova Senha</label>
                          <input
                            type="password"
                            placeholder="Digite sua nova senha"
                            className="w-full px-4 py-3 border border-gray-200 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all text-sm bg-white"
                          />
                          <div className="mt-2 space-y-1 text-xs">
                            <div className="flex items-center gap-2 text-gray-500">
                              <span className="w-2 h-2 rounded-full bg-gray-300"></span>
                              <span>Mínimo 8 caracteres</span>
                            </div>
                            <div className="flex items-center gap-2 text-gray-500">
                              <span className="w-2 h-2 rounded-full bg-gray-300"></span>
                              <span>Pelo menos uma letra maiúscula</span>
                            </div>
                            <div className="flex items-center gap-2 text-gray-500">
                              <span className="w-2 h-2 rounded-full bg-gray-300"></span>
                              <span>Pelo menos um número</span>
                            </div>
                          </div>
                        </div>
                        <div>
                          <label className="block text-sm font-medium text-gray-700 mb-2">Confirmar Nova Senha</label>
                          <input
                            type="password"
                            placeholder="Confirme sua nova senha"
                            className="w-full px-4 py-3 border border-gray-200 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all text-sm bg-white"
                          />
                        </div>
                        <button className="w-full bg-gradient-to-r from-blue-500 to-blue-600 text-white px-6 py-3 rounded-xl hover:from-blue-600 hover:to-blue-700 transition-all shadow-md hover:shadow-lg text-sm font-medium mt-4">
                          🔄 Atualizar Senha
                        </button>
                      </div>
                    </div>

                    {/* Sessões Ativas */}
                    <div className="bg-gradient-to-br from-gray-50 to-white rounded-xl p-6 border border-gray-100">
                      <div className="flex items-center gap-3 mb-6">
                        <span className="text-2xl">💻</span>
                        <div>
                          <h3 className="text-lg font-semibold text-gray-900">Sessões Ativas</h3>
                          <p className="text-sm text-gray-600">Gerencie os dispositivos conectados à sua conta</p>
                        </div>
                      </div>
                      
                      <div className="space-y-4">
                        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 p-4 bg-green-50 border border-green-200 rounded-xl">
                          <div className="flex items-center gap-3">
                            <div className="w-10 h-10 bg-green-100 rounded-lg flex items-center justify-center">
                              <span className="text-lg text-green-600">🖥️</span>
                            </div>
                            <div>
                              <p className="font-semibold text-gray-900">Chrome - Windows</p>
                              <p className="text-sm text-gray-600">São Paulo, Brasil • Agora</p>
                              <p className="text-xs text-green-600 font-medium">✓ Sessão atual</p>
                            </div>
                          </div>
                          <span className="bg-green-100 text-green-700 px-3 py-1 rounded-full text-xs font-medium self-start sm:self-center">Ativa</span>
                        </div>
                      </div>
                    </div>

                    {/* Verificação em Duas Etapas */}
                    <div className="bg-gradient-to-br from-blue-50 to-indigo-50 rounded-xl p-6 border border-blue-100">
                      <div className="flex items-center gap-3 mb-4">
                        <span className="text-2xl">🛡️</span>
                        <div>
                          <h3 className="text-lg font-semibold text-gray-900">Verificação em Duas Etapas</h3>
                          <p className="text-sm text-gray-600">Adicione uma camada extra de segurança</p>
                        </div>
                      </div>
                      
                      <div className="bg-white rounded-lg p-4 border border-blue-200">
                        <div className="flex items-center justify-between">
                          <div>
                            <p className="font-medium text-gray-900">Autenticação por SMS</p>
                            <p className="text-sm text-gray-600">Receba códigos via mensagem</p>
                          </div>
                          <button className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 text-sm font-medium">
                            Configurar
                          </button>
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
    </div>
  )
}