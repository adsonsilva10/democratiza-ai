/**
 * Button Component - Design System Base
 * Componente fundamental com variantes, tamanhos e estados
 */

import React from 'react';
import { cva, type VariantProps } from 'class-variance-authority';
import { cn } from '../../lib/utils';

// Definindo variantes usando CVA (Class Variance Authority)
const buttonVariants = cva(
  // Base classes - sempre aplicadas
  "inline-flex items-center justify-center whitespace-nowrap rounded-md text-sm font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50",
  {
    variants: {
      variant: {
        // Primary - Ação principal (azul)
        default: "bg-primary text-white hover:bg-primary-600 active:bg-primary-700",
        
        // Secondary - Ação secundária (dourado)
        secondary: "bg-secondary text-white hover:bg-secondary-600 active:bg-secondary-700",
        
        // Destructive - Ações de risco (vermelho)
        destructive: "bg-danger text-white hover:bg-danger-600 active:bg-danger-700",
        
        // Outline - Botão com borda
        outline: "border border-neutral-200 bg-background hover:bg-neutral-50 hover:text-neutral-900",
        
        // Ghost - Botão transparente
        ghost: "hover:bg-neutral-100 hover:text-neutral-900",
        
        // Link - Aparência de link
        link: "text-primary underline-offset-4 hover:underline",
        
        // Success - Para confirmações
        success: "bg-success text-white hover:bg-success-600 active:bg-success-700",
        
        // Warning - Para alertas
        warning: "bg-warning text-white hover:bg-warning-600 active:bg-warning-700",
      },
      size: {
        default: "h-10 px-4 py-2",
        sm: "h-9 rounded-md px-3",
        lg: "h-11 rounded-md px-8",
        xl: "h-12 rounded-lg px-10 text-base",
        icon: "h-10 w-10",
      },
      fullWidth: {
        true: "w-full",
        false: "w-auto",
      },
    },
    defaultVariants: {
      variant: "default",
      size: "default",
      fullWidth: false,
    },
  }
);

export interface ButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement>,
    VariantProps<typeof buttonVariants> {
  asChild?: boolean;
  loading?: boolean;
  leftIcon?: React.ReactNode;
  rightIcon?: React.ReactNode;
}

const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ 
    className, 
    variant, 
    size, 
    fullWidth,
    asChild = false, 
    loading = false,
    leftIcon,
    rightIcon,
    children,
    disabled,
    ...props 
  }, ref) => {
    
    const isDisabled = disabled || loading;
    
    return (
      <button
        className={cn(buttonVariants({ variant, size, fullWidth }), className)}
        ref={ref}
        disabled={isDisabled}
        {...props}
      >
        {loading && (
          <svg
            className="mr-2 h-4 w-4 animate-spin"
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
          >
            <circle
              className="opacity-25"
              cx="12"
              cy="12"
              r="10"
              stroke="currentColor"
              strokeWidth="4"
            />
            <path
              className="opacity-75"
              fill="currentColor"
              d="m4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
            />
          </svg>
        )}
        
        {!loading && leftIcon && (
          <span className="mr-2 flex-shrink-0">
            {leftIcon}
          </span>
        )}
        
        <span className="truncate">
          {children}
        </span>
        
        {!loading && rightIcon && (
          <span className="ml-2 flex-shrink-0">
            {rightIcon}
          </span>
        )}
      </button>
    );
  }
);

Button.displayName = "Button";

export { Button, buttonVariants };