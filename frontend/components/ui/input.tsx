/**
 * Input Component - Design System Base
 * Componente fundamental para entrada de dados
 */

import React from 'react';
import { cva, type VariantProps } from 'class-variance-authority';
import { cn } from '../../lib/utils';

// Variantes do Input
const inputVariants = cva(
  "flex w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50",
  {
    variants: {
      variant: {
        default: "border-neutral-300 focus-visible:ring-primary",
        destructive: "border-danger focus-visible:ring-danger",
        success: "border-success focus-visible:ring-success",
      },
      size: {
        default: "h-10 px-3 py-2",
        sm: "h-9 px-3 text-sm",
        lg: "h-11 px-4 text-base",
      },
    },
    defaultVariants: {
      variant: "default",
      size: "default",
    },
  }
);

export interface InputProps
  extends Omit<React.InputHTMLAttributes<HTMLInputElement>, 'size'>,
    VariantProps<typeof inputVariants> {
  label?: string;
  error?: string;
  helper?: string;
  leftIcon?: React.ReactNode;
  rightIcon?: React.ReactNode;
  onRightIconClick?: () => void;
}

const Input = React.forwardRef<HTMLInputElement, InputProps>(
  ({ 
    className, 
    variant, 
    size, 
    type, 
    label,
    error,
    helper,
    leftIcon,
    rightIcon,
    onRightIconClick,
    id,
    ...props 
  }, ref) => {
    const inputId = id || `input-${Math.random().toString(36).substr(2, 9)}`;
    const hasError = !!error;
    const effectiveVariant = hasError ? 'destructive' : variant;

    return (
      <div className="w-full">
        {label && (
          <label 
            htmlFor={inputId}
            className="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70 mb-2 block"
          >
            {label}
          </label>
        )}
        
        <div className="relative">
          {leftIcon && (
            <div className="absolute left-3 top-1/2 -translate-y-1/2 text-muted-foreground">
              {leftIcon}
            </div>
          )}
          
          <input
            type={type}
            className={cn(
              inputVariants({ variant: effectiveVariant, size }),
              leftIcon && "pl-10",
              rightIcon && "pr-10",
              className
            )}
            ref={ref}
            id={inputId}
            {...props}
          />
          
          {rightIcon && (
            <div 
              className={cn(
                "absolute right-3 top-1/2 -translate-y-1/2 text-muted-foreground",
                onRightIconClick && "cursor-pointer hover:text-foreground"
              )}
              onClick={onRightIconClick}
            >
              {rightIcon}
            </div>
          )}
        </div>
        
        {(error || helper) && (
          <p className={cn(
            "text-sm mt-1",
            error ? "text-danger" : "text-muted-foreground"
          )}>
            {error || helper}
          </p>
        )}
      </div>
    );
  }
);

Input.displayName = "Input";

// Textarea Component
export interface TextareaProps
  extends React.TextareaHTMLAttributes<HTMLTextAreaElement>,
    VariantProps<typeof inputVariants> {
  label?: string;
  error?: string;
  helper?: string;
}

const Textarea = React.forwardRef<HTMLTextAreaElement, TextareaProps>(
  ({ 
    className, 
    variant, 
    label,
    error,
    helper,
    id,
    ...props 
  }, ref) => {
    const textareaId = id || `textarea-${Math.random().toString(36).substr(2, 9)}`;
    const hasError = !!error;
    const effectiveVariant = hasError ? 'destructive' : variant;

    return (
      <div className="w-full">
        {label && (
          <label 
            htmlFor={textareaId}
            className="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70 mb-2 block"
          >
            {label}
          </label>
        )}
        
        <textarea
          className={cn(
            "flex min-h-[80px] w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50",
            effectiveVariant === 'destructive' && "border-danger focus-visible:ring-danger",
            effectiveVariant === 'success' && "border-success focus-visible:ring-success",
            className
          )}
          ref={ref}
          id={textareaId}
          {...props}
        />
        
        {(error || helper) && (
          <p className={cn(
            "text-sm mt-1",
            error ? "text-danger" : "text-muted-foreground"
          )}>
            {error || helper}
          </p>
        )}
      </div>
    );
  }
);

Textarea.displayName = "Textarea";

// Componentes especializados para o contexto jurídico
export interface CPFInputProps extends Omit<InputProps, 'type' | 'placeholder'> {
  onValidCPF?: (cpf: string) => void;
}

const CPFInput = React.forwardRef<HTMLInputElement, CPFInputProps>(
  ({ onValidCPF, onChange, ...props }, ref) => {
    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
      let value = e.target.value.replace(/\D/g, '');
      
      // Aplicar máscara CPF
      if (value.length >= 11) {
        value = value.substring(0, 11);
      }
      
      // Formatar
      if (value.length > 9) {
        value = value.replace(/(\d{3})(\d{3})(\d{3})(\d{2})/, '$1.$2.$3-$4');
      } else if (value.length > 6) {
        value = value.replace(/(\d{3})(\d{3})(\d{3})/, '$1.$2.$3');
      } else if (value.length > 3) {
        value = value.replace(/(\d{3})(\d{3})/, '$1.$2');
      }
      
      e.target.value = value;
      
      // Validar CPF completo
      if (value.length === 14) {
        // Implementar validação de CPF aqui
        onValidCPF?.(value);
      }
      
      onChange?.(e);
    };

    return (
      <Input
        ref={ref}
        type="text"
        placeholder="000.000.000-00"
        label="CPF"
        maxLength={14}
        onChange={handleChange}
        {...props}
      />
    );
  }
);

CPFInput.displayName = "CPFInput";

export { Input, Textarea, CPFInput, inputVariants };