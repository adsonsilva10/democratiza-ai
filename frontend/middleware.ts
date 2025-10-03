import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'

// Rotas que requerem autenticação
const protectedRoutes = ['/dashboard', '/chat', '/contracts']

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
    
    // Verificar se há token no localStorage via cookie ou header
    const authToken = request.cookies.get('sb-access-token')?.value || 
                     request.cookies.get('auth-token')?.value ||
                     request.headers.get('authorization')?.replace('Bearer ', '')

    console.log('🔍 Middleware - Rota:', pathname, 'Token:', !!authToken)

    // Verificar se a rota é protegida
    const isProtectedRoute = protectedRoutes.some(route => 
      pathname.startsWith(route)
    )
    
    // Verificar se é rota de auth
    const isAuthRoute = authRoutes.some(route => 
      pathname.startsWith(route)
    )

    // Se está tentando acessar rota protegida sem token
    if (isProtectedRoute && !authToken) {
      console.log('❌ Acesso negado - rota protegida sem token')
      const url = request.nextUrl.clone()
      url.pathname = '/login'
      url.searchParams.set('callbackUrl', pathname)
      return NextResponse.redirect(url)
    }

    // Se está tentando acessar rota de auth com token válido
    if (isAuthRoute && authToken) {
      console.log('✅ Usuário já logado - redirecionando para dashboard')
      const url = request.nextUrl.clone()
      url.pathname = '/dashboard'
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