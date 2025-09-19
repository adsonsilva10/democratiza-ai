# Democratiza AI - Frontend

## 🎯 Visão Geral

Frontend da plataforma **Democratiza AI**, uma solução completa para análise de contratos com inteligência artificial. O projeto democratiza a compreensão jurídica no Brasil, permitindo que qualquer pessoa entenda o que está assinando.

## 🚀 Funcionalidades Implementadas

### ✅ Sistema de Upload
- **Componente**: `SimpleUploadManager.tsx`
- **Funcionalidades**:
  - Drag & drop de arquivos PDF e DOC
  - Validação de tipo e tamanho
  - Barra de progresso de upload
  - Preview de arquivo selecionado
  - Integração com API de upload

### ✅ Sistema de Autenticação  
- **Rotas**: `app/(auth)/login` e `app/(auth)/register`
- **Funcionalidades**:
  - Formulários de login e registro
  - Validação de campos
  - Integração com JWT
  - Context API para estado global
  - Middleware de proteção de rotas

### ✅ Interface de Chat com IA
- **Componente**: `SimpleChat.tsx`
- **Funcionalidades**:
  - Chat em tempo real com agentes especializados
  - Seleção de tipo de agente (locação, telecom, financeiro)
  - Simulação de resposta de IA
  - Interface intuitiva com indicador de digitação

### ✅ Dashboard Completo
- **Área**: `app/(dashboard)`
- **Funcionalidades**:
  - Sidebar de navegação
  - Cards de estatísticas
  - Lista de contratos recentes
  - Página completa de gestão de contratos
  - Filtros por tipo, risco e status
  - Ordenação e busca

## 🏗️ Arquitetura

### Stack Tecnológico
- **Framework**: Next.js 14.1.0 (App Router)
- **UI**: React 18 + TypeScript
- **Styling**: Tailwind CSS 3.4.0 + PostCSS
- **Componentes**: Shadcn/UI
- **Estado**: React Context + Custom Hooks
- **HTTP Client**: Fetch API nativo

### Estrutura de Diretórios
```
frontend/
├── app/
│   ├── (auth)/             # Grupo de rotas de autenticação
│   │   ├── login/page.tsx  # Página de login
│   │   └── register/page.tsx # Página de registro
│   ├── (dashboard)/        # Grupo de rotas protegidas
│   │   ├── layout.tsx      # Layout com sidebar
│   │   ├── page.tsx        # Dashboard principal
│   │   └── contracts/page.tsx # Gestão de contratos
│   ├── chat/page.tsx       # Interface de chat
│   ├── layout.tsx          # Layout root
│   └── page.tsx            # Homepage
├── components/
│   ├── features/           # Componentes específicos
│   │   ├── ChatWithAgent.tsx
│   │   ├── SimpleChat.tsx
│   │   └── SimpleUploadManager.tsx
│   └── ui/                 # Componentes base Shadcn/UI
├── lib/
│   ├── api.ts              # Client HTTP para backend
│   ├── hooks/useApi.ts     # Hooks customizados
│   └── providers.tsx       # Context providers
└── middleware.ts           # Proteção de rotas
```

## 🔧 Configuração e Instalação

### Pré-requisitos
- Node.js 18+
- npm ou yarn

### Instalação
```bash
cd frontend
npm install
npm run dev
```

### Variáveis de Ambiente
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## 🔌 Integração com Backend

### API Client (`lib/api.ts`)
Client HTTP completo com:
- Autenticação JWT
- Endpoints para contratos, chat e usuários
- Tratamento de erros
- TypeScript interfaces

### Endpoints Implementados
- **Auth**: Login, registro, logout, perfil
- **Contratos**: Upload, listagem, análise, exclusão
- **Chat**: Sessões, mensagens, agentes
- **Pagamentos**: Integração Mercado Pago

### Hooks Customizados (`lib/hooks/useApi.ts`)
- `useAuth()`: Gerenciamento de autenticação
- `useContracts()`: Estado dos contratos
- `useChat()`: Gerenciamento de chat
- `useIsAuthenticated()`: Verificação de auth

## 🎨 Design System

### Componentes Base
- Todas as funcionalidades usam componentes Shadcn/UI
- Design system consistente com Tailwind CSS
- Responsivo para mobile e desktop
- Temas e variáveis CSS customizáveis

### Padrões de UX
- **Loading States**: Indicadores de carregamento
- **Error Handling**: Tratamento de erros amigável
- **Form Validation**: Validação em tempo real
- **Toast Notifications**: Feedback para usuário

## 🔒 Segurança e Autenticação

### Proteção de Rotas
- Middleware Next.js para proteção automática
- Redirecionamento para login se não autenticado
- Context para estado global de autenticação

### Gerenciamento de Tokens
- JWT armazenado em localStorage
- Refresh automático de tokens
- Logout em caso de token inválido

## 📱 Responsividade

### Breakpoints
- **Mobile**: 640px e abaixo
- **Tablet**: 768px - 1024px  
- **Desktop**: 1024px e acima

### Componentes Adaptativos
- Layout fluido com CSS Grid/Flexbox
- Sidebar colapsável em mobile
- Cards responsivos no dashboard
- Forms otimizados para touch

## 🧪 Testing Strategy

### Componentes Testáveis
- Upload com simulação de arquivos
- Forms com validação
- Chat com mock de respostas
- Dashboard com dados de demonstração

### Dados Mock
Todos os componentes funcionam com dados simulados para demonstração:
- Contratos de exemplo
- Usuários fictícios
- Respostas de IA simuladas

## 🚀 Deploy e Produção

### Build
```bash
npm run build
npm start
```

### Variáveis de Produção
```env
NEXT_PUBLIC_API_URL=https://api.democratiza-ai.com
NODE_ENV=production
```

### Checklist de Deploy
- [ ] Configurar variáveis de ambiente
- [ ] Testar integração com backend real
- [ ] Configurar domínio personalizado
- [ ] Otimizar imagens e assets
- [ ] Configurar monitoring

## 🔄 Próximos Passos

### Melhorias Técnicas
- [ ] Implementar React Query para cache
- [ ] Adicionar testes automatizados
- [ ] Configurar Storybook para componentes
- [ ] Otimizar performance com lazy loading

### Novas Funcionalidades
- [ ] Sistema de notificações
- [ ] Análise de contratos em batch
- [ ] Integração com assinatura eletrônica
- [ ] Dashboard de analytics avançado

## 📄 Licença

Este projeto faz parte da plataforma Democratiza AI.

---

**Status**: ✅ Frontend completo e funcional  
**Última atualização**: 19/09/2024  
**Desenvolvido com**: Next.js + TypeScript + Tailwind CSS