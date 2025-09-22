/**
 * Alert Component - Design System Base
 * Componente para alertas, notificações e feedbacks
 */

import React from 'react';
import { cva, type VariantProps } from 'class-variance-authority';
import { cn } from '../../lib/utils';

// Variantes do Alert
const alertVariants = cva(
  "relative w-full rounded-lg border p-4 [&>svg~*]:pl-7 [&>svg+div]:translate-y-[-3px] [&>svg]:absolute [&>svg]:left-4 [&>svg]:top-4 [&>svg]:text-foreground",
  {
    variants: {
      variant: {
        default: "bg-background text-foreground border-neutral-200",
        destructive: "border-danger/50 text-danger-foreground bg-danger/10 [&>svg]:text-danger",
        success: "border-success/50 text-success-foreground bg-success/10 [&>svg]:text-success",
        warning: "border-warning/50 text-warning-foreground bg-warning/10 [&>svg]:text-warning",
        info: "border-primary/50 text-primary-foreground bg-primary/10 [&>svg]:text-primary",
      },
    },
    defaultVariants: {
      variant: "default",
    },
  }
);

export interface AlertProps
  extends React.HTMLAttributes<HTMLDivElement>,
    VariantProps<typeof alertVariants> {
  dismissible?: boolean;
  onDismiss?: () => void;
}

const Alert = React.forwardRef<HTMLDivElement, AlertProps>(
  ({ className, variant, dismissible, onDismiss, children, ...props }, ref) => (
    <div
      ref={ref}
      role="alert"
      className={cn(alertVariants({ variant }), className)}
      {...props}
    >
      {children}
      {dismissible && onDismiss && (
        <button
          type="button"
          className="absolute right-4 top-4 rounded-sm opacity-70 ring-offset-background transition-opacity hover:opacity-100 focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2"
          onClick={onDismiss}
          aria-label="Fechar alerta"
        >
          <svg 
            className="h-4 w-4" 
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
  )
);
Alert.displayName = "Alert";

const AlertTitle = React.forwardRef<
  HTMLParagraphElement,
  React.HTMLAttributes<HTMLHeadingElement>
>(({ className, ...props }, ref) => (
  <h5
    ref={ref}
    className={cn("mb-1 font-medium leading-none tracking-tight", className)}
    {...props}
  />
));
AlertTitle.displayName = "AlertTitle";

const AlertDescription = React.forwardRef<
  HTMLParagraphElement,
  React.HTMLAttributes<HTMLParagraphElement>
>(({ className, ...props }, ref) => (
  <div
    ref={ref}
    className={cn("text-sm [&_p]:leading-relaxed", className)}
    {...props}
  />
));
AlertDescription.displayName = "AlertDescription";

// Ícones para diferentes tipos de alerta
const AlertIcons = {
  success: (
    <svg className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
    </svg>
  ),
  warning: (
    <svg className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z" />
    </svg>
  ),
  destructive: (
    <svg className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
    </svg>
  ),
  info: (
    <svg className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
    </svg>
  ),
};

// Componentes especializados para contexto jurídico
export interface ContractAlertProps extends Omit<AlertProps, 'variant'> {
  type: 'clausula-abusiva' | 'prazo-vencimento' | 'valor-alto' | 'condicoes-favoraveis';
  title: string;
  description: string;
}

const ContractAlert = React.forwardRef<HTMLDivElement, ContractAlertProps>(
  ({ type, title, description, ...props }, ref) => {
    const alertConfig = {
      'clausula-abusiva': { variant: 'destructive' as const, icon: AlertIcons.destructive },
      'prazo-vencimento': { variant: 'warning' as const, icon: AlertIcons.warning },
      'valor-alto': { variant: 'warning' as const, icon: AlertIcons.warning },
      'condicoes-favoraveis': { variant: 'success' as const, icon: AlertIcons.success },
    };

    const config = alertConfig[type];

    return (
      <Alert
        ref={ref}
        variant={config.variant}
        {...props}
      >
        {config.icon}
        <AlertTitle>{title}</AlertTitle>
        <AlertDescription>{description}</AlertDescription>
      </Alert>
    );
  }
);

ContractAlert.displayName = "ContractAlert";

export { 
  Alert, 
  AlertTitle, 
  AlertDescription, 
  ContractAlert,
  AlertIcons,
  alertVariants 
};