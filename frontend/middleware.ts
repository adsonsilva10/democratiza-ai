import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'

// Rotas que requerem autenticação
const protectedRoutes = ['/plataforma', '/dashboard', '/chat', '/contracts']

// Rotas de auth (redirecionam se já autenticado) 
const authRoutes = ['/login', '/register']

// Rotas públicas (sempre acessíveis)
const publicRoutes = ['/', '/auth/callback']

export async function middleware(request: NextRequest) {
  try {
    const { pathname } = request.nextUrl
    
    // Permitir acesso às rotas públicas sempre
    if (publicRoutes.includes(pathname)) {
      return NextResponse.next()
    }

    // Criar cliente Supabase para middleware
    const res = NextResponse.next()
    
    // Verificar tokens de autenticação (Supabase + Demo)
    const supabaseAccessToken = request.cookies.get('sb-access-token')?.value
    const supabaseRefreshToken = request.cookies.get('sb-refresh-token')?.value
    const demoToken = request.cookies.get('auth-token')?.value
    const authHeader = request.headers.get('authorization')?.replace('Bearer ', '')
    
    // Considerar autenticado se tiver qualquer token válido
    const hasSupabaseAuth = !!(supabaseAccessToken || supabaseRefreshToken)
    const hasDemoAuth = !!demoToken
    const hasHeaderAuth = !!authHeader
    const isAuthenticated = hasSupabaseAuth || hasDemoAuth || hasHeaderAuth

    console.log('🔍 Middleware - Rota:', pathname)
    console.log('🔍 Supabase Auth:', hasSupabaseAuth, 'Demo Auth:', hasDemoAuth, 'Header Auth:', hasHeaderAuth)
    console.log('🔍 Resultado:', isAuthenticated ? 'AUTENTICADO' : 'NÃO AUTENTICADO')

    // Verificar se a rota é protegida
    const isProtectedRoute = protectedRoutes.some(route => 
      pathname.startsWith(route)
    )
    
    // Verificar se é rota de auth
    const isAuthRoute = authRoutes.some(route => 
      pathname.startsWith(route)
    )

    // Se está tentando acessar rota protegida sem token
    if (isProtectedRoute && !isAuthenticated) {
      console.log('❌ Acesso negado - rota protegida sem token')
      const url = request.nextUrl.clone()
      url.pathname = '/login'
      url.searchParams.set('callbackUrl', pathname)
      console.log('🔄 Redirecionando para login com callback:', pathname)
      return NextResponse.redirect(url)
    }

    // Se está tentando acessar rota de auth com token válido
    if (isAuthRoute && isAuthenticated) {
      console.log('✅ Usuário já logado - redirecionando para plataforma')
      const url = request.nextUrl.clone()
      url.pathname = '/plataforma'
      return NextResponse.redirect(url)
    }

    console.log('✅ Middleware - acesso permitido')
    return res

  } catch (error) {
    console.error('❌ Erro no middleware:', error)
    
    // Em caso de erro, permitir acesso para não quebrar a aplicação
    return NextResponse.next()
  }
}

export const config = {
  matcher: [
    '/((?!api|_next/static|_next/image|favicon.ico).*)',
  ],
}