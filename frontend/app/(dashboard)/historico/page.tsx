"use client";

import { useState, useEffect } from "react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { useApi } from "@/lib/hooks/useApi";
import Link from 'next/link';

// Ícones simples usando emojis
const Calendar = () => <span>📅</span>;
const CreditCard = () => <span>💳</span>;
const RefreshCw = () => <span>🔄</span>;
const Download = () => <span>⬇️</span>;
const FileText = () => <span>📄</span>;

interface Transaction {
  id: string;
  amount: number;
  status: string;
  payment_method: string;
  description: string;
  created_at: string;
  updated_at: string;
  mercado_pago_payment_url?: string;
  plan?: {
    name: string;
    type: string;
  };
}

interface Contract {
  id: number;
  title: string;
  type: string;
  riskLevel: string;
  uploadDate: string;
  status: string;
  summary: string;
  keyPoints: string[];
  riskScore: number;
}

const statusColors = {
  pending: "bg-yellow-100 text-yellow-800",
  approved: "bg-green-100 text-green-800", 
  cancelled: "bg-red-100 text-red-800",
  rejected: "bg-red-100 text-red-800",
};

const statusLabels = {
  pending: "Pendente",
  approved: "Aprovado",
  cancelled: "Cancelado", 
  rejected: "Rejeitado",
};

// TODO: Buscar contratos reais da API
const allContracts: Contract[] = []

const typeEmojis = {
  rental: '🏠',
  telecom: '📱',
  financial: '💰',
  insurance: '🛡️',
  health: '🏥'
}

const typeLabels = {
  rental: 'Locação',
  telecom: 'Telecom',
  financial: 'Financeiro',
  insurance: 'Seguro',
  health: 'Saúde'
}

const riskColors = {
  low: 'bg-green-100 text-green-800 border-green-300',
  medium: 'bg-yellow-100 text-yellow-800 border-yellow-300',
  high: 'bg-red-100 text-red-800 border-red-300'
}

const riskLabels = {
  low: 'Baixo Risco',
  medium: 'Médio Risco',
  high: 'Alto Risco'
}

export default function HistoricoPage() {
  const { apiRequest } = useApi();
  const [activeTab, setActiveTab] = useState<'contracts' | 'transactions'>('contracts');
  const [transactions, setTransactions] = useState<Transaction[]>([]);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  
  // Estados para filtros de contratos
  const [filterType, setFilterType] = useState('all');
  const [filterRisk, setFilterRisk] = useState('all');
  const [sortBy, setSortBy] = useState('date');
  const [searchTerm, setSearchTerm] = useState('');

  useEffect(() => {
    if (activeTab === 'transactions') {
      loadTransactions();
    } else {
      setLoading(false);
    }
  }, [activeTab]);

  const loadTransactions = async () => {
    try {
      setLoading(true);
      const response = await apiRequest("/api/v1/payments/user/transactions");
      
      if (response.success) {
        setTransactions(response.data.transactions || []);
      }
    } catch (error) {
      console.error("Erro ao carregar transações:", error);
    } finally {
      setLoading(false);
    }
  };

  const refreshTransactions = async () => {
    setRefreshing(true);
    await loadTransactions();
    setRefreshing(false);
  };

  const formatPrice = (price: number) => {
    return new Intl.NumberFormat("pt-BR", {
      style: "currency",
      currency: "BRL",
    }).format(price);
  };

  const formatDate = (dateString: string) => {
    return new Intl.DateTimeFormat("pt-BR", {
      day: "2-digit",
      month: "2-digit",
      year: "numeric",
      hour: "2-digit",
      minute: "2-digit",
    }).format(new Date(dateString));
  };

  // Filtrar contratos
  const filteredContracts = allContracts
    .filter(contract => {
      if (filterType !== 'all' && contract.type !== filterType) return false
      if (filterRisk !== 'all' && contract.riskLevel !== filterRisk) return false
      if (searchTerm && !contract.title.toLowerCase().includes(searchTerm.toLowerCase())) return false
      return true
    })
    .sort((a, b) => {
      switch (sortBy) {
        case 'date':
          return new Date(b.uploadDate).getTime() - new Date(a.uploadDate).getTime()
        case 'risk':
          return b.riskScore - a.riskScore
        case 'name':
          return a.title.localeCompare(b.title)
        default:
          return 0
      }
    })

  const getRiskScoreColor = (score: number) => {
    if (score <= 40) return 'text-green-600'
    if (score <= 70) return 'text-yellow-600'
    return 'text-red-600'
  }

  return (
    <div className="w-full max-w-7xl mx-auto">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-2xl sm:text-3xl lg:text-4xl font-bold text-gray-900 mb-4">
          📚 Histórico
        </h1>
        <p className="text-gray-600 text-base sm:text-lg">
          Visualize seus contratos analisados e transações realizadas
        </p>
      </div>

      {/* Navigation Tabs */}
      <div className="mb-8">
        <nav className="flex space-x-8" aria-label="Tabs">
          <button
            onClick={() => setActiveTab('contracts')}
            className={`whitespace-nowrap py-2 px-1 border-b-2 font-medium text-sm ${
              activeTab === 'contracts'
                ? 'border-blue-500 text-blue-600'
                : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
            }`}
          >
            <FileText /> Contratos Analisados
          </button>
          <button
            onClick={() => setActiveTab('transactions')}
            className={`whitespace-nowrap py-2 px-1 border-b-2 font-medium text-sm ${
              activeTab === 'transactions'
                ? 'border-blue-500 text-blue-600'
                : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
            }`}
          >
            <CreditCard /> Transações de Pagamento
          </button>
        </nav>
      </div>

      {/* Conteúdo das Abas */}
      {activeTab === 'contracts' ? (
        <>
          {/* Filtros e Busca */}
          <div className="bg-white p-6 rounded-xl shadow-lg mb-8">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          {/* Busca */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Buscar contrato
            </label>
            <input
              type="text"
              placeholder="Digite o nome do contrato..."
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
            />
          </div>

          {/* Filtro por Tipo */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Tipo de contrato
            </label>
            <select
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              value={filterType}
              onChange={(e) => setFilterType(e.target.value)}
            >
              <option value="all">Todos os tipos</option>
              <option value="rental">Locação</option>
              <option value="telecom">Telecom</option>
              <option value="financial">Financeiro</option>
              <option value="insurance">Seguro</option>
              <option value="health">Saúde</option>
            </select>
          </div>

          {/* Filtro por Risco */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Nível de risco
            </label>
            <select
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              value={filterRisk}
              onChange={(e) => setFilterRisk(e.target.value)}
            >
              <option value="all">Todos os níveis</option>
              <option value="low">Baixo risco</option>
              <option value="medium">Médio risco</option>
              <option value="high">Alto risco</option>
            </select>
          </div>

          {/* Ordenação */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Ordenar por
            </label>
            <select
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              value={sortBy}
              onChange={(e) => setSortBy(e.target.value)}
            >
              <option value="date">Data mais recente</option>
              <option value="risk">Maior risco</option>
              <option value="name">Nome A-Z</option>
            </select>
          </div>
        </div>
      </div>

      {/* Estatísticas Rápidas */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
        <div className="bg-blue-50 p-4 rounded-lg border border-blue-200">
          <div className="text-2xl font-bold text-blue-600">{filteredContracts.length}</div>
          <div className="text-sm text-blue-700">Contratos encontrados</div>
        </div>
        <div className="bg-red-50 p-4 rounded-lg border border-red-200">
          <div className="text-2xl font-bold text-red-600">
            {filteredContracts.filter(c => c.riskLevel === 'high').length}
          </div>
          <div className="text-sm text-red-700">Alto risco</div>
        </div>
        <div className="bg-yellow-50 p-4 rounded-lg border border-yellow-200">
          <div className="text-2xl font-bold text-yellow-600">
            {filteredContracts.filter(c => c.riskLevel === 'medium').length}
          </div>
          <div className="text-sm text-yellow-700">Médio risco</div>
        </div>
        <div className="bg-green-50 p-4 rounded-lg border border-green-200">
          <div className="text-2xl font-bold text-green-600">
            {filteredContracts.filter(c => c.riskLevel === 'low').length}
          </div>
          <div className="text-sm text-green-700">Baixo risco</div>
        </div>
      </div>

      {/* Lista de Contratos */}
      <div className="space-y-6">
        {filteredContracts.map((contract) => (
          <div key={contract.id} className="bg-white p-6 rounded-xl shadow-lg hover:shadow-xl transition-shadow duration-200">
            <div className="flex flex-col lg:flex-row lg:items-start lg:justify-between gap-6">
              
              {/* Informações Principais */}
              <div className="flex-1">
                <div className="flex items-start justify-between mb-4">
                  <div className="flex items-center space-x-3">
                    <span className="text-2xl">{typeEmojis[contract.type as keyof typeof typeEmojis]}</span>
                    <div>
                      <h3 className="text-lg font-semibold text-gray-900 mb-1">
                        {contract.title}
                      </h3>
                      <div className="flex items-center space-x-3">
                        <span className="text-sm text-gray-600">
                          {typeLabels[contract.type as keyof typeof typeLabels]}
                        </span>
                        <span className="text-sm text-gray-400">•</span>
                        <span className="text-sm text-gray-600">
                          {new Date(contract.uploadDate).toLocaleDateString('pt-BR')}
                        </span>
                      </div>
                    </div>
                  </div>
                  
                  <div className="flex items-center space-x-3">
                    <span className={`px-3 py-1 rounded-full text-sm font-medium border ${
                      riskColors[contract.riskLevel as keyof typeof riskColors]
                    }`}>
                      {riskLabels[contract.riskLevel as keyof typeof riskLabels]}
                    </span>
                    <div className={`text-lg font-bold ${getRiskScoreColor(contract.riskScore)}`}>
                      {contract.riskScore}%
                    </div>
                  </div>
                </div>

                <p className="text-gray-700 mb-4 leading-relaxed">
                  {contract.summary}
                </p>

                <div>
                  <h4 className="font-medium text-gray-900 mb-2">Principais pontos identificados:</h4>
                  <ul className="space-y-1">
                    {contract.keyPoints.map((point, index) => (
                      <li key={index} className="text-sm text-gray-600 flex items-start">
                        <span className="text-blue-500 mr-2 mt-1">•</span>
                        {point}
                      </li>
                    ))}
                  </ul>
                </div>
              </div>

              {/* Ações */}
              <div className="flex flex-col space-y-3 lg:min-w-[200px]">
                <button className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors">
                  Ver Análise Completa
                </button>
                <Link 
                  href={`/dashboard/chat?contract=${contract.id}`}
                  className="px-4 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors text-center"
                >
                  💬 Chat sobre este contrato
                </Link>
                <button className="px-4 py-2 text-gray-600 hover:text-gray-800 transition-colors text-sm">
                  📥 Baixar PDF
                </button>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Mensagem quando não há resultados */}
      {filteredContracts.length === 0 && (
        <div className="text-center py-12">
          <div className="text-6xl mb-4">📭</div>
          <h3 className="text-xl font-semibold text-gray-900 mb-2">
            Nenhum contrato encontrado
          </h3>
          <p className="text-gray-600 mb-6">
            Tente ajustar os filtros ou faça uma nova busca
          </p>
          <Link 
            href="/dashboard/analise"
            className="inline-flex items-center px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
          >
            📤 Analisar novo contrato
          </Link>
        </div>
      )}
        </>
      ) : (
        /* Aba de Transações */
        <div className="space-y-6">
          <div className="flex justify-between items-center">
            <div>
              <h2 className="text-xl font-bold text-gray-900">Histórico de Pagamentos</h2>
              <p className="text-gray-600">Visualize todas as suas transações</p>
            </div>
            
            <Button 
              onClick={refreshTransactions}
              disabled={refreshing}
            >
              <RefreshCw /> {refreshing ? "Atualizando..." : "Atualizar"}
            </Button>
          </div>

          {loading ? (
            <div className="flex items-center justify-center h-32">
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
            </div>
          ) : transactions.length === 0 ? (
            <Card>
              <CardContent className="py-12 text-center">
                <CreditCard />
                <h3 className="text-lg font-medium text-gray-900 mb-2 mt-4">
                  Nenhuma transação encontrada
                </h3>
                <p className="text-gray-500 mb-4">
                  Você ainda não realizou nenhum pagamento na plataforma.
                </p>
                <Button onClick={() => window.location.href = "/dashboard/planos"}>
                  Ver Planos Disponíveis
                </Button>
              </CardContent>
            </Card>
          ) : (
            <>
              {transactions.map((transaction) => (
                <Card key={transaction.id}>
                  <CardHeader className="pb-3">
                    <div className="flex justify-between items-start">
                      <div>
                        <CardTitle className="text-lg">
                          {transaction.description || `Transação #${transaction.id.slice(0, 8)}`}
                        </CardTitle>
                        <CardDescription>
                          {transaction.plan && (
                            <span className="mr-2">
                              {transaction.plan.name} • {transaction.plan.type === "subscription" ? "Assinatura" : "Avulso"}
                            </span>
                          )}
                          <Calendar /> {formatDate(transaction.created_at)}
                        </CardDescription>
                      </div>
                      
                      <div className="text-right">
                        <div className="text-2xl font-bold text-primary mb-1">
                          {formatPrice(transaction.amount)}
                        </div>
                        <Badge 
                          className={statusColors[transaction.status as keyof typeof statusColors] || "bg-gray-100 text-gray-800"}
                        >
                          {statusLabels[transaction.status as keyof typeof statusLabels] || transaction.status}
                        </Badge>
                      </div>
                    </div>
                  </CardHeader>
                  
                  <CardContent>
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
                      <div>
                        <p className="text-gray-500">Método de Pagamento</p>
                        <p className="font-medium">{transaction.payment_method || "Mercado Pago"}</p>
                      </div>
                      
                      <div>
                        <p className="text-gray-500">Status</p>
                        <p className="font-medium">
                          {statusLabels[transaction.status as keyof typeof statusLabels] || transaction.status}
                        </p>
                      </div>
                      
                      <div>
                        <p className="text-gray-500">Última Atualização</p>
                        <p className="font-medium">{formatDate(transaction.updated_at)}</p>
                      </div>
                    </div>
                    
                    {transaction.status === "pending" && transaction.mercado_pago_payment_url && (
                      <div className="mt-4 pt-4 border-t">
                        <Button 
                          onClick={() => window.open(transaction.mercado_pago_payment_url, "_blank")}
                          className="w-full sm:w-auto"
                        >
                          <CreditCard /> Finalizar Pagamento
                        </Button>
                      </div>
                    )}
                  </CardContent>
                </Card>
              ))}
              
              {/* Resumo das Transações */}
              <Card className="mt-8">
                <CardHeader>
                  <CardTitle>Resumo</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                    <div className="text-center p-4 bg-blue-50 rounded-lg">
                      <div className="text-2xl font-bold text-blue-600">
                        {transactions.length}
                      </div>
                      <p className="text-sm text-blue-600">Total de Transações</p>
                    </div>
                    
                    <div className="text-center p-4 bg-green-50 rounded-lg">
                      <div className="text-2xl font-bold text-green-600">
                        {transactions.filter(t => t.status === "approved").length}
                      </div>
                      <p className="text-sm text-green-600">Pagamentos Aprovados</p>
                    </div>
                    
                    <div className="text-center p-4 bg-yellow-50 rounded-lg">
                      <div className="text-2xl font-bold text-yellow-600">
                        {transactions.filter(t => t.status === "pending").length}
                      </div>
                      <p className="text-sm text-yellow-600">Pagamentos Pendentes</p>
                    </div>
                    
                    <div className="text-center p-4 bg-purple-50 rounded-lg">
                      <div className="text-2xl font-bold text-purple-600">
                        {formatPrice(
                          transactions
                            .filter(t => t.status === "approved")
                            .reduce((sum, t) => sum + t.amount, 0)
                        )}
                      </div>
                      <p className="text-sm text-purple-600">Total Pago</p>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </>
          )}
        </div>
      )}
    </div>
  )
}