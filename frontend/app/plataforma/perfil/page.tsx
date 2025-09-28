'use client'

import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'

export default function PerfilPage() {
  return (
    <div className="p-6 max-w-4xl mx-auto">
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-gray-900 mb-2">Meu Perfil</h1>
        <p className="text-gray-600">Gerencie suas informações pessoais e preferências da conta</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Perfil Principal */}
        <div className="lg:col-span-2 space-y-6">
          {/* Informações Pessoais */}
          <Card>
            <CardHeader>
              <CardTitle>Informações Pessoais</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="flex items-center gap-6">
                <div className="w-20 h-20 bg-gradient-to-r from-blue-600 to-purple-600 rounded-full flex items-center justify-center text-white text-2xl font-bold">
                  AS
                </div>
                <div>
                  <h3 className="text-lg font-semibold text-gray-900">Adson Silva</h3>
                  <p className="text-gray-600">adson@democratiza.ai</p>
                  <Badge className="mt-1 bg-gradient-to-r from-blue-600 to-purple-600 text-white">
                    Premium ⭐
                  </Badge>
                </div>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Nome Completo</label>
                  <div className="p-3 bg-gray-50 rounded-lg text-gray-900">Adson Silva</div>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Email</label>
                  <div className="p-3 bg-gray-50 rounded-lg text-gray-900">adson@democratiza.ai</div>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Telefone</label>
                  <div className="p-3 bg-gray-50 rounded-lg text-gray-900">+55 (11) 99999-9999</div>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Membro desde</label>
                  <div className="p-3 bg-gray-50 rounded-lg text-gray-900">Janeiro 2025</div>
                </div>
              </div>

              <div className="flex gap-3">
                <Button className="bg-gradient-to-r from-blue-600 to-purple-600">
                  Editar Perfil
                </Button>
                <Button variant="outline">
                  Alterar Senha
                </Button>
              </div>
            </CardContent>
          </Card>

          {/* Estatísticas de Uso */}
          <Card>
            <CardHeader>
              <CardTitle>Estatísticas de Uso</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-3 gap-4">
                <div className="text-center p-4 bg-blue-50 rounded-lg">
                  <div className="text-2xl font-bold text-blue-600">23</div>
                  <div className="text-sm text-gray-600">Análises Realizadas</div>
                </div>
                <div className="text-center p-4 bg-green-50 rounded-lg">
                  <div className="text-2xl font-bold text-green-600">12</div>
                  <div className="text-sm text-gray-600">Assinaturas</div>
                </div>
                <div className="text-center p-4 bg-purple-50 rounded-lg">
                  <div className="text-2xl font-bold text-purple-600">15</div>
                  <div className="text-sm text-gray-600">Riscos Evitados</div>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Sidebar */}
        <div className="space-y-6">
          {/* Plano Atual */}
          <Card>
            <CardHeader>
              <CardTitle>Plano Atual</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-center">
                <div className="w-16 h-16 mx-auto mb-3 bg-gradient-to-r from-blue-600 to-purple-600 rounded-full flex items-center justify-center text-white text-2xl">
                  ⭐
                </div>
                <h3 className="font-bold text-lg text-gray-900">Premium</h3>
                <p className="text-gray-600 text-sm mb-4">Análises ilimitadas</p>
                <Button variant="outline" className="w-full">
                  Gerenciar Plano
                </Button>
              </div>
            </CardContent>
          </Card>

          {/* Ações Rápidas */}
          <Card>
            <CardHeader>
              <CardTitle>Ações Rápidas</CardTitle>
            </CardHeader>
            <CardContent className="space-y-3">
              <Button variant="outline" className="w-full justify-start gap-2">
                <span>⚙️</span>
                Configurações
              </Button>
              <Button variant="outline" className="w-full justify-start gap-2">
                <span>❓</span>
                Central de Ajuda
              </Button>
              <Button variant="outline" className="w-full justify-start gap-2 text-red-600 hover:text-red-700 hover:bg-red-50">
                <span>🚪</span>
                Sair da Conta
              </Button>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  )
}