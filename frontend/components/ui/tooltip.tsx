"use client"

import * as React from "react"
import { cn } from "@/lib/utils"

// Implementação simplificada do Tooltip sem Radix UI
interface TooltipProviderProps {
  children: React.ReactNode
  delayDuration?: number
}

const TooltipProvider = ({ children }: TooltipProviderProps) => {
  return <div>{children}</div>
}

interface TooltipProps {
  children: React.ReactNode
}

const Tooltip = ({ children }: TooltipProps) => {
  const [isVisible, setIsVisible] = React.useState(false)
  
  return (
    <div className="relative inline-block">
      {React.Children.map(children, (child) => {
        if (React.isValidElement(child)) {
          if (child.type === TooltipTrigger) {
            return React.cloneElement(child as React.ReactElement<any>, {
              onMouseEnter: () => setIsVisible(true),
              onMouseLeave: () => setIsVisible(false),
              onFocus: () => setIsVisible(true),
              onBlur: () => setIsVisible(false)
            })
          }
          if (child.type === TooltipContent && isVisible) {
            return child
          }
        }
        return child
      })}
    </div>
  )
}

interface TooltipTriggerProps {
  children: React.ReactNode
  asChild?: boolean
  onMouseEnter?: () => void
  onMouseLeave?: () => void
  onFocus?: () => void
  onBlur?: () => void
}

const TooltipTrigger = React.forwardRef<
  HTMLDivElement,
  TooltipTriggerProps
>(({ children, asChild, onMouseEnter, onMouseLeave, onFocus, onBlur }, ref) => {
  if (asChild) {
    return React.Children.map(children, child => {
      if (React.isValidElement(child)) {
        return React.cloneElement(child as React.ReactElement<any>, {
          onMouseEnter,
          onMouseLeave,
          onFocus,
          onBlur,
          ref
        })
      }
      return child
    })
  }

  return (
    <div
      ref={ref}
      onMouseEnter={onMouseEnter}
      onMouseLeave={onMouseLeave}
      onFocus={onFocus}
      onBlur={onBlur}
    >
      {children}
    </div>
  )
})
TooltipTrigger.displayName = "TooltipTrigger"

interface TooltipContentProps extends React.HTMLAttributes<HTMLDivElement> {
  side?: "top" | "right" | "bottom" | "left"
  sideOffset?: number
}

const TooltipContent = React.forwardRef<
  HTMLDivElement,
  TooltipContentProps
>(({ className, side = "top", sideOffset = 4, ...props }, ref) => {
  const getPositionClasses = () => {
    switch (side) {
      case "top":
        return "bottom-full mb-1 left-1/2 -translate-x-1/2"
      case "bottom":
        return "top-full mt-1 left-1/2 -translate-x-1/2"
      case "left":
        return "right-full mr-1 top-1/2 -translate-y-1/2"
      case "right":
        return "left-full ml-1 top-1/2 -translate-y-1/2"
      default:
        return "bottom-full mb-1 left-1/2 -translate-x-1/2"
    }
  }

  return (
    <div
      ref={ref}
      className={cn(
        "absolute z-50 overflow-hidden rounded-md border bg-gray-900 px-3 py-1.5 text-xs text-white shadow-md animate-in fade-in-0 zoom-in-95",
        getPositionClasses(),
        className
      )}
      {...props}
    />
  )
})
TooltipContent.displayName = "TooltipContent"

export { Tooltip, TooltipTrigger, TooltipContent, TooltipProvider }