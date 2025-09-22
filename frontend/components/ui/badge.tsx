/**
 * Badge Component - Design System Base
 * Componente para indicadores de status, tags e labels
 */

import React from 'react';
import { cva, type VariantProps } from 'class-variance-authority';
import { cn } from '../../lib/utils';

// Variantes do Badge
const badgeVariants = cva(
  "inline-flex items-center rounded-full border px-2.5 py-0.5 text-xs font-semibold transition-colors focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2",
  {
    variants: {
      variant: {
        // Default neutral
        default: "border-transparent bg-neutral-100 text-neutral-900 hover:bg-neutral-200",
        
        // Primary brand
        primary: "border-transparent bg-primary text-white",
        
        // Secondary brand
        secondary: "border-transparent bg-secondary text-white",
        
        // Success - Baixo risco
        success: "border-transparent bg-success text-white",
        
        // Warning - Médio risco  
        warning: "border-transparent bg-warning text-white",
        
        // Danger - Alto risco
        danger: "border-transparent bg-danger text-white",
        
        // Outline variants
        outline: "text-neutral-700 border-neutral-300",
        "outline-primary": "text-primary border-primary-300",
        "outline-success": "text-success border-success-300", 
        "outline-warning": "text-warning border-warning-300",
        "outline-danger": "text-danger border-danger-300",
        
        // Subtle variants
        subtle: "bg-neutral-50 text-neutral-600 border-neutral-200",
        "subtle-primary": "bg-primary-50 text-primary-700 border-primary-200",
        "subtle-success": "bg-success-50 text-success-700 border-success-200",
        "subtle-warning": "bg-warning-50 text-warning-700 border-warning-200", 
        "subtle-danger": "bg-danger-50 text-danger-700 border-danger-200",
      },
      size: {
        sm: "px-2 py-1 text-xs",
        default: "px-2.5 py-0.5 text-xs",
        lg: "px-3 py-1 text-sm",
      },
    },
    defaultVariants: {
      variant: "default",
      size: "default",
    },
  }
);

export interface BadgeProps
  extends React.HTMLAttributes<HTMLDivElement>,
    VariantProps<typeof badgeVariants> {
  icon?: React.ReactNode;
  removable?: boolean;
  onRemove?: () => void;
}

const Badge = React.forwardRef<HTMLDivElement, BadgeProps>(
  ({ className, variant, size, icon, removable, onRemove, children, ...props }, ref) => {
    return (
      <div
        ref={ref}
        className={cn(badgeVariants({ variant, size }), className)}
        {...props}
      >
        {icon && (
          <span className="mr-1 flex-shrink-0">
            {icon}
          </span>
        )}
        
        <span className="truncate">
          {children}
        </span>
        
        {removable && onRemove && (
          <button
            type="button"
            className="ml-1 flex-shrink-0 rounded-full p-0.5 hover:bg-black/10 focus:outline-none focus:ring-1 focus:ring-white"
            onClick={onRemove}
            aria-label="Remover"
          >
            <svg 
              className="h-3 w-3" 
              fill="none" 
              viewBox="0 0 24 24" 
              stroke="currentColor"
            >
              <path 
                strokeLinecap="round" 
                strokeLinejoin="round" 
                strokeWidth={2} 
                d="M6 18L18 6M6 6l12 12" 
              />
            </svg>
          </button>
        )}
      </div>
    );
  }
);

Badge.displayName = "Badge";

// Componentes especializados para o contexto jurídico
export interface RiskBadgeProps extends Omit<BadgeProps, 'variant'> {
  risk: 'baixo' | 'medio' | 'alto';
}

const RiskBadge = React.forwardRef<HTMLDivElement, RiskBadgeProps>(
  ({ risk, ...props }, ref) => {
    const riskConfig = {
      baixo: { variant: 'success' as const, label: 'Baixo Risco' },
      medio: { variant: 'warning' as const, label: 'Médio Risco' },
      alto: { variant: 'danger' as const, label: 'Alto Risco' },
    };

    const config = riskConfig[risk];

    return (
      <Badge
        ref={ref}
        variant={config.variant}
        {...props}
      >
        {config.label}
      </Badge>
    );
  }
);

RiskBadge.displayName = "RiskBadge";

export interface ContractTypeBadgeProps extends Omit<BadgeProps, 'variant'> {
  type: 'locacao' | 'telecom' | 'financeiro' | 'outros';
}

const ContractTypeBadge = React.forwardRef<HTMLDivElement, ContractTypeBadgeProps>(
  ({ type, ...props }, ref) => {
    const typeConfig = {
      locacao: { variant: 'primary' as const, label: 'Locação' },
      telecom: { variant: 'secondary' as const, label: 'Telecom' },
      financeiro: { variant: 'outline-primary' as const, label: 'Financeiro' },
      outros: { variant: 'outline' as const, label: 'Outros' },
    };

    const config = typeConfig[type];

    return (
      <Badge
        ref={ref}
        variant={config.variant}
        {...props}
      >
        {config.label}
      </Badge>
    );
  }
);

ContractTypeBadge.displayName = "ContractTypeBadge";

export { Badge, RiskBadge, ContractTypeBadge, badgeVariants };