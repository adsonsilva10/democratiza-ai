'use client'

import { useState } from 'react'

export default function ConfiguracoesPage() {
  const [notificacoes, setNotificacoes] = useState({
    email: true,
    push: false,
    sms: false,
    analiseCompleta: true,
    riscosAltos: true,
    novoContrato: false
  })

  const [preferencias, setPreferencias] = useState({
    idioma: 'pt-BR',
    tema: 'light',
    moeda: 'BRL',
    precisaoAnalise: 'alta',
    tipoRelatorio: 'completo'
  })

  const [privacidade, setPrivacidade] = useState({
    compartilharDados: false,
    melhoriaServico: true,
    cookiesNecessarios: true,
    cookiesAnalise: false,
    cookiesMarketing: false
  })

  const [perfil, setPerfil] = useState({
    nome: 'João Silva',
    email: 'joao.silva@email.com',
    telefone: '(11) 99999-9999',
    empresa: 'Minha Empresa LTDA',
    cargo: 'Gerente Jurídico'
  })

  return (
    <div className="w-full max-w-4xl mx-auto">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-2xl sm:text-3xl lg:text-4xl font-bold text-gray-900 mb-4">
          ⚙️ Configurações
        </h1>
        <p className="text-gray-600 text-base sm:text-lg">
          Personalize sua experiência na plataforma
        </p>
      </div>

      <div className="space-y-8">
        
        {/* Perfil do Usuário */}
        <div className="bg-white p-6 rounded-xl shadow-lg">
          <h2 className="text-xl font-bold text-gray-900 mb-6 flex items-center">
            👤 Perfil do Usuário
          </h2>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Nome Completo
              </label>
              <input
                type="text"
                value={perfil.nome}
                onChange={(e) => setPerfil({...perfil, nome: e.target.value})}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                E-mail
              </label>
              <input
                type="email"
                value={perfil.email}
                onChange={(e) => setPerfil({...perfil, email: e.target.value})}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Telefone
              </label>
              <input
                type="tel"
                value={perfil.telefone}
                onChange={(e) => setPerfil({...perfil, telefone: e.target.value})}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Empresa
              </label>
              <input
                type="text"
                value={perfil.empresa}
                onChange={(e) => setPerfil({...perfil, empresa: e.target.value})}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              />
            </div>

            <div className="md:col-span-2">
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Cargo/Função
              </label>
              <input
                type="text"
                value={perfil.cargo}
                onChange={(e) => setPerfil({...perfil, cargo: e.target.value})}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              />
            </div>
          </div>

          <div className="mt-6 flex justify-end">
            <button className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors">
              Salvar Perfil
            </button>
          </div>
        </div>

        {/* Preferências de Análise */}
        <div className="bg-white p-6 rounded-xl shadow-lg">
          <h2 className="text-xl font-bold text-gray-900 mb-6 flex items-center">
            🎯 Preferências de Análise
          </h2>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Precisão da Análise
              </label>
              <select
                value={preferencias.precisaoAnalise}
                onChange={(e) => setPreferencias({...preferencias, precisaoAnalise: e.target.value})}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              >
                <option value="rapida">Análise Rápida (menos detalhada)</option>
                <option value="media">Análise Padrão (equilibrada)</option>
                <option value="alta">Análise Detalhada (mais precisa)</option>
              </select>
              <p className="text-xs text-gray-500 mt-1">
                Análises mais detalhadas podem levar mais tempo para processar
              </p>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Tipo de Relatório
              </label>
              <select
                value={preferencias.tipoRelatorio}
                onChange={(e) => setPreferencias({...preferencias, tipoRelatorio: e.target.value})}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              >
                <option value="resumido">Resumo Executivo</option>
                <option value="completo">Relatório Completo</option>
                <option value="tecnico">Análise Técnica Detalhada</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Idioma
              </label>
              <select
                value={preferencias.idioma}
                onChange={(e) => setPreferencias({...preferencias, idioma: e.target.value})}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              >
                <option value="pt-BR">Português (Brasil)</option>
                <option value="en-US">English (US)</option>
                <option value="es-ES">Español</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Moeda Padrão
              </label>
              <select
                value={preferencias.moeda}
                onChange={(e) => setPreferencias({...preferencias, moeda: e.target.value})}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              >
                <option value="BRL">Real Brasileiro (R$)</option>
                <option value="USD">Dólar Americano ($)</option>
                <option value="EUR">Euro (€)</option>
              </select>
            </div>
          </div>
        </div>

        {/* Notificações */}
        <div className="bg-white p-6 rounded-xl shadow-lg">
          <h2 className="text-xl font-bold text-gray-900 mb-6 flex items-center">
            🔔 Notificações
          </h2>
          
          <div className="space-y-6">
            <div>
              <h3 className="font-semibold text-gray-900 mb-4">Meios de Comunicação</h3>
              <div className="space-y-3">
                <label className="flex items-center">
                  <input
                    type="checkbox"
                    checked={notificacoes.email}
                    onChange={(e) => setNotificacoes({...notificacoes, email: e.target.checked})}
                    className="mr-3 h-4 w-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
                  />
                  <span className="text-gray-700">E-mail</span>
                </label>
                
                <label className="flex items-center">
                  <input
                    type="checkbox"
                    checked={notificacoes.push}
                    onChange={(e) => setNotificacoes({...notificacoes, push: e.target.checked})}
                    className="mr-3 h-4 w-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
                  />
                  <span className="text-gray-700">Notificações Push (navegador)</span>
                </label>
                
                <label className="flex items-center">
                  <input
                    type="checkbox"
                    checked={notificacoes.sms}
                    onChange={(e) => setNotificacoes({...notificacoes, sms: e.target.checked})}
                    className="mr-3 h-4 w-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
                  />
                  <span className="text-gray-700">SMS (apenas emergências)</span>
                </label>
              </div>
            </div>

            <div>
              <h3 className="font-semibold text-gray-900 mb-4">Tipos de Alerta</h3>
              <div className="space-y-3">
                <label className="flex items-center">
                  <input
                    type="checkbox"
                    checked={notificacoes.analiseCompleta}
                    onChange={(e) => setNotificacoes({...notificacoes, analiseCompleta: e.target.checked})}
                    className="mr-3 h-4 w-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
                  />
                  <span className="text-gray-700">Análise de contrato concluída</span>
                </label>
                
                <label className="flex items-center">
                  <input
                    type="checkbox"
                    checked={notificacoes.riscosAltos}
                    onChange={(e) => setNotificacoes({...notificacoes, riscosAltos: e.target.checked})}
                    className="mr-3 h-4 w-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
                  />
                  <span className="text-gray-700">Riscos altos detectados</span>
                </label>
                
                <label className="flex items-center">
                  <input
                    type="checkbox"
                    checked={notificacoes.novoContrato}
                    onChange={(e) => setNotificacoes({...notificacoes, novoContrato: e.target.checked})}
                    className="mr-3 h-4 w-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
                  />
                  <span className="text-gray-700">Lembretes de novos contratos</span>
                </label>
              </div>
            </div>
          </div>
        </div>

        {/* Privacidade e Segurança */}
        <div className="bg-white p-6 rounded-xl shadow-lg">
          <h2 className="text-xl font-bold text-gray-900 mb-6 flex items-center">
            🔒 Privacidade e Segurança
          </h2>
          
          <div className="space-y-6">
            <div>
              <h3 className="font-semibold text-gray-900 mb-4">Compartilhamento de Dados</h3>
              <div className="space-y-3">
                <label className="flex items-start">
                  <input
                    type="checkbox"
                    checked={privacidade.compartilharDados}
                    onChange={(e) => setPrivacidade({...privacidade, compartilharDados: e.target.checked})}
                    className="mr-3 h-4 w-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500 mt-1"
                  />
                  <div>
                    <span className="text-gray-700 font-medium">Compartilhar dados anonimizados</span>
                    <p className="text-sm text-gray-500 mt-1">
                      Ajuda a melhorar nossa IA, mantendo sua privacidade protegida
                    </p>
                  </div>
                </label>
                
                <label className="flex items-start">
                  <input
                    type="checkbox"
                    checked={privacidade.melhoriaServico}
                    onChange={(e) => setPrivacidade({...privacidade, melhoriaServico: e.target.checked})}
                    className="mr-3 h-4 w-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500 mt-1"
                  />
                  <div>
                    <span className="text-gray-700 font-medium">Dados para melhoria do serviço</span>
                    <p className="text-sm text-gray-500 mt-1">
                      Permite análises internas para aprimorar a plataforma
                    </p>
                  </div>
                </label>
              </div>
            </div>

            <div>
              <h3 className="font-semibold text-gray-900 mb-4">Cookies e Rastreamento</h3>
              <div className="space-y-3">
                <label className="flex items-start">
                  <input
                    type="checkbox"
                    checked={privacidade.cookiesNecessarios}
                    disabled
                    className="mr-3 h-4 w-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500 mt-1 opacity-50"
                  />
                  <div>
                    <span className="text-gray-700 font-medium">Cookies necessários</span>
                    <p className="text-sm text-gray-500 mt-1">
                      Essenciais para o funcionamento da plataforma (não pode ser desabilitado)
                    </p>
                  </div>
                </label>
                
                <label className="flex items-start">
                  <input
                    type="checkbox"
                    checked={privacidade.cookiesAnalise}
                    onChange={(e) => setPrivacidade({...privacidade, cookiesAnalise: e.target.checked})}
                    className="mr-3 h-4 w-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500 mt-1"
                  />
                  <div>
                    <span className="text-gray-700 font-medium">Cookies de análise</span>
                    <p className="text-sm text-gray-500 mt-1">
                      Para entender como você usa a plataforma e melhorar a experiência
                    </p>
                  </div>
                </label>
                
                <label className="flex items-start">
                  <input
                    type="checkbox"
                    checked={privacidade.cookiesMarketing}
                    onChange={(e) => setPrivacidade({...privacidade, cookiesMarketing: e.target.checked})}
                    className="mr-3 h-4 w-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500 mt-1"
                  />
                  <div>
                    <span className="text-gray-700 font-medium">Cookies de marketing</span>
                    <p className="text-sm text-gray-500 mt-1">
                      Para personalizar ofertas e conteúdo relevante
                    </p>
                  </div>
                </label>
              </div>
            </div>

            <div className="pt-4 border-t border-gray-200">
              <div className="flex flex-col sm:flex-row gap-3">
                <button className="px-4 py-2 text-blue-600 border border-blue-600 rounded-lg hover:bg-blue-50 transition-colors">
                  Alterar Senha
                </button>
                <button className="px-4 py-2 text-red-600 border border-red-600 rounded-lg hover:bg-red-50 transition-colors">
                  Excluir Conta
                </button>
                <button className="px-4 py-2 text-gray-600 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors">
                  Baixar Meus Dados
                </button>
              </div>
            </div>
          </div>
        </div>

        {/* Botões de Ação */}
        <div className="flex justify-end space-x-4">
          <button className="px-6 py-3 text-gray-700 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors">
            Cancelar
          </button>
          <button className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors">
            Salvar Todas as Configurações
          </button>
        </div>
      </div>
    </div>
  )
}