import { theme } from './lib/design-tokens';

/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: ["class"],
  content: [
    './pages/**/*.{ts,tsx}',
    './components/**/*.{ts,tsx}',
    './app/**/*.{ts,tsx}',
    './src/**/*.{ts,tsx}',
  ],
  theme: {
    container: {
      center: true,
      padding: "2rem",
      screens: {
        "2xl": "1400px",
      },
    },
    extend: {
      // Design System Colors - Integrando com tokens existentes
      colors: {
        // Mantendo compatibilidade com Shadcn/UI
        border: "hsl(var(--border))",
        input: "hsl(var(--input))",
        ring: "hsl(var(--ring))",
        background: "hsl(var(--background))",
        foreground: "hsl(var(--foreground))",
        
        // Design System - Cores Principais
        primary: {
          ...theme.colors.primary,
          DEFAULT: theme.colors.primary[500],
          foreground: "hsl(var(--primary-foreground))",
        },
        secondary: {
          ...theme.colors.secondary,
          DEFAULT: theme.colors.secondary[500],
          foreground: "hsl(var(--secondary-foreground))",
        },
        
        // Design System - Status Colors
        destructive: {
          ...theme.colors.danger,
          DEFAULT: theme.colors.danger[500],
          foreground: "hsl(var(--destructive-foreground))",
        },
        success: {
          ...theme.colors.success,
          DEFAULT: theme.colors.success[500],
          foreground: theme.colors.success[50],
        },
        warning: {
          ...theme.colors.warning,
          DEFAULT: theme.colors.warning[500],
          foreground: theme.colors.warning[50],
        },
        danger: {
          ...theme.colors.danger,
          DEFAULT: theme.colors.danger[500],
          foreground: theme.colors.danger[50],
        },
        
        // Cores do Design System
        neutral: theme.colors.neutral,
        
        // Mantendo cores Shadcn/UI
        muted: {
          DEFAULT: "hsl(var(--muted))",
          foreground: "hsl(var(--muted-foreground))",
        },
        accent: {
          DEFAULT: "hsl(var(--accent))",
          foreground: "hsl(var(--accent-foreground))",
        },
        popover: {
          DEFAULT: "hsl(var(--popover))",
          foreground: "hsl(var(--popover-foreground))",
        },
        card: {
          DEFAULT: "hsl(var(--card))",
          foreground: "hsl(var(--card-foreground))",
        },
      },
      
      // Design System - Typography
      fontFamily: theme.typography.fontFamily,
      fontSize: theme.typography.fontSize,
      fontWeight: theme.typography.fontWeight,
      
      // Design System - Spacing & Layout
      spacing: theme.spacing,
      screens: theme.breakpoints,
      boxShadow: theme.shadows,
      
      // Design System - Border Radius
      borderRadius: {
        ...theme.borderRadius,
        lg: "var(--radius)",
        md: "calc(var(--radius) - 2px)",
        sm: "calc(var(--radius) - 4px)",
      },
      
      // Design System - Animations + Existing
      keyframes: {
        "accordion-down": {
          from: { height: 0 },
          to: { height: "var(--radix-accordion-content-height)" },
        },
        "accordion-up": {
          from: { height: "var(--radix-accordion-content-height)" },
          to: { height: 0 },
        },
        "fade-in": {
          from: { opacity: 0 },
          to: { opacity: 1 },
        },
        "slide-in": {
          from: { transform: "translateY(100%)" },
          to: { transform: "translateY(0)" },
        },
        // Novas animações do Design System
        "pulse-glow": {
          "0%, 100%": { 
            opacity: 1,
            boxShadow: `0 0 20px ${theme.colors.primary[400]}`
          },
          "50%": { 
            opacity: 0.8,
            boxShadow: `0 0 40px ${theme.colors.primary[500]}`
          },
        },
        "bounce-subtle": {
          "0%, 100%": { transform: "translateY(0)" },
          "50%": { transform: "translateY(-4px)" },
        },
      },
      animation: {
        "accordion-down": "accordion-down 0.2s ease-out",
        "accordion-up": "accordion-up 0.2s ease-out",
        "fade-in": "fade-in 0.3s ease-out",
        "slide-in": "slide-in 0.3s ease-out",
        "pulse-glow": "pulse-glow 2s ease-in-out infinite",
        "bounce-subtle": "bounce-subtle 1s ease-in-out infinite",
      },
      
      // Design System - Z-Index
      zIndex: theme.zIndex,
      
      // Design System - Transition
      transitionDuration: theme.animations.duration,
      transitionTimingFunction: theme.animations.ease,
    },
  },
  plugins: [],
}
