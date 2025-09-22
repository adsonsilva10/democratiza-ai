/**
 * Design System Components - Index
 * Exportações centralizadas de todos os componentes do sistema
 */

// Base Components
export { Button, buttonVariants } from './button';
export type { ButtonProps } from './button';

export { 
  Card, 
  CardHeader, 
  CardFooter, 
  CardTitle, 
  CardDescription, 
  CardContent,
  cardVariants 
} from './card';
export type { CardProps } from './card';

export { 
  Badge, 
  RiskBadge, 
  ContractTypeBadge, 
  badgeVariants 
} from './badge';
export type { BadgeProps, RiskBadgeProps, ContractTypeBadgeProps } from './badge';

export { 
  Alert, 
  AlertTitle, 
  AlertDescription, 
  ContractAlert,
  AlertIcons,
  alertVariants 
} from './alert';
export type { AlertProps, ContractAlertProps } from './alert';

export { 
  Input, 
  Textarea, 
  CPFInput, 
  inputVariants 
} from './input';
export type { InputProps, TextareaProps, CPFInputProps } from './input';

// Toaster (mantendo compatibilidade)
export { Toaster } from './toaster';