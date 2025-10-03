// Utilitários para gerenciar redirecionamentos de autenticação

/**
 * Obtém a URL de callback dos parâmetros da URL ou retorna o padrão
 */
export function getCallbackUrl(searchParams?: URLSearchParams, defaultUrl = '/plataforma'): string {
  if (typeof window === 'undefined') return defaultUrl
  
  // Tentar obter dos search params primeiro
  if (searchParams) {
    const callbackUrl = searchParams.get('callbackUrl')
    if (callbackUrl) return callbackUrl
  }
  
  // Tentar obter da URL atual
  const urlParams = new URLSearchParams(window.location.search)
  const callbackUrl = urlParams.get('callbackUrl')
  if (callbackUrl) return callbackUrl
  
  return defaultUrl
}

/**
 * Salva a URL de callback para uso após OAuth
 */
export function saveCallbackUrl(url: string): void {
  if (typeof window !== 'undefined') {
    sessionStorage.setItem('oauth-callback-url', url)
  }
}

/**
 * Obtém e remove a URL de callback salva
 */
export function getAndClearCallbackUrl(defaultUrl = '/plataforma'): string {
  if (typeof window === 'undefined') return defaultUrl
  
  const savedUrl = sessionStorage.getItem('oauth-callback-url')
  if (savedUrl) {
    sessionStorage.removeItem('oauth-callback-url')
    return savedUrl
  }
  
  return defaultUrl
}

/**
 * Redireciona para a URL de callback apropriada
 */
export function redirectToCallback(router: any, searchParams?: URLSearchParams): void {
  const callbackUrl = getCallbackUrl(searchParams)
  console.log('🔄 Redirecionando para:', callbackUrl)
  router.push(callbackUrl)
}

/**
 * Cria URL de login com callback
 */
export function createLoginUrl(returnTo?: string): string {
  const loginUrl = '/login'
  if (returnTo) {
    return `${loginUrl}?callbackUrl=${encodeURIComponent(returnTo)}`
  }
  return loginUrl
}