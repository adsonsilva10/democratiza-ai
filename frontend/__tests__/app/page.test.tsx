import { render, screen } from '@testing-library/react'
import HomePage from '@/app/page'

// Mock Next.js modules
jest.mock('next/link', () => {
  return function MockLink({ children, ...props }: any) {
    return <a {...props}>{children}</a>
  }
})

jest.mock('@/components/features/SimpleUploadManager', () => {
  return function MockUploadManager() {
    return <div data-testid="upload-manager">Upload Manager Mock</div>
  }
})

jest.mock('@/components/features/ProcessSteps', () => {
  return function MockProcessSteps() {
    return <div data-testid="process-steps">Process Steps Mock</div>
  }
})

jest.mock('@/components/features/SocialProof', () => {
  return function MockSocialProof() {
    return <div data-testid="social-proof">Social Proof Mock</div>
  }
})

jest.mock('@/components/features/FinalCTA', () => {
  return function MockFinalCTA() {
    return <div data-testid="final-cta">Final CTA Mock</div>
  }
})

describe('HomePage', () => {
  it('renders the main heading', () => {
    render(<HomePage />)
    
    const heading = screen.getByRole('heading', { level: 1 })
    expect(heading).toBeInTheDocument()
    expect(heading).toHaveTextContent(/Nunca Assine Um/i)
  })

  it('renders the hero section with trust badge', () => {
    render(<HomePage />)
    
    expect(screen.getByText(/Confiado por milhares de brasileiros/i)).toBeInTheDocument()
    expect(screen.getByText(/Contrato Arriscado/i)).toBeInTheDocument()
  })

  it('renders CTA buttons', () => {
    render(<HomePage />)
    
    const analyzeButton = screen.getByRole('link', { name: /Analise Grátis Agora/i })
    const chatButton = screen.getByRole('link', { name: /Conversar com IA/i })
    
    expect(analyzeButton).toBeInTheDocument()
    expect(chatButton).toBeInTheDocument()
    
    expect(analyzeButton).toHaveAttribute('href', '/dashboard')
    expect(chatButton).toHaveAttribute('href', '/chat')
  })

  it('renders upload manager component', () => {
    render(<HomePage />)
    
    expect(screen.getAllByTestId('upload-manager')).toHaveLength(2)
  })

  it('renders process steps component', () => {
    render(<HomePage />)
    
    expect(screen.getByTestId('process-steps')).toBeInTheDocument()
  })

  it('renders social proof component', () => {
    render(<HomePage />)
    
    expect(screen.getByTestId('social-proof')).toBeInTheDocument()
  })

  it('renders final CTA component', () => {
    render(<HomePage />)
    
    expect(screen.getByTestId('final-cta')).toBeInTheDocument()
  })

  it('displays trust indicators', () => {
    render(<HomePage />)
    
    expect(screen.getByText(/30 dias grátis/i)).toBeInTheDocument()
    expect(screen.getByText(/Sem cartão/i)).toBeInTheDocument()
    expect(screen.getByText(/Cancele quando quiser/i)).toBeInTheDocument()
  })

  it('shows the warning about contract risks', () => {
    render(<HomePage />)
    
    expect(screen.getByText(/maioria dos brasileiros assina contratos/i)).toBeInTheDocument()
    expect(screen.getAllByText(/Cláusulas abusivas/i)).toHaveLength(5)
  })
})