"use client"

import React from 'react'
import { CheckCircle, X, ArrowRight, User } from 'lucide-react'

interface SuccessModalProps {
  isOpen: boolean
  onClose: () => void
  title: string
  message: string
  userEmail?: string
  actionText?: string
  onAction?: () => void
}

export function SuccessModal({
  isOpen,
  onClose,
  title,
  message,
  userEmail,
  actionText = "Continuar",
  onAction
}: SuccessModalProps) {
  if (!isOpen) return null

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
      <div className="bg-white rounded-2xl p-8 max-w-md w-full relative animate-in fade-in-0 zoom-in-95 duration-300">
        {/* Close Button */}
        <button
          onClick={onClose}
          className="absolute top-4 right-4 text-gray-400 hover:text-gray-600 transition-colors"
        >
          <X className="h-5 w-5" />
        </button>

        {/* Success Icon */}
        <div className="flex justify-center mb-6">
          <div className="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center">
            <CheckCircle className="h-8 w-8 text-green-600" />
          </div>
        </div>

        {/* Content */}
        <div className="text-center">
          <h3 className="text-xl font-bold text-gray-900 mb-3">
            {title}
          </h3>
          
          <p className="text-gray-600 mb-6 leading-relaxed">
            {message}
          </p>

          {/* User Info */}
          {userEmail && (
            <div className="bg-gray-50 rounded-lg p-4 mb-6">
              <div className="flex items-center justify-center gap-2 text-sm text-gray-600">
                <User className="h-4 w-4" />
                <span>{userEmail}</span>
              </div>
            </div>
          )}

          {/* Action Button */}
          <button
            onClick={onAction || onClose}
            className="w-full flex items-center justify-center gap-2 py-3 px-4 bg-gradient-to-r from-green-500 to-emerald-500 text-white font-semibold rounded-xl shadow-lg hover:shadow-xl transition-all duration-300 transform hover:scale-[1.02]"
          >
            <span>{actionText}</span>
            <ArrowRight className="w-5 h-5" />
          </button>
        </div>
      </div>
    </div>
  )
}

// Modal específica para sucesso no cadastro
interface RegisterSuccessModalProps {
  isOpen: boolean
  onClose: () => void
  userEmail: string
  needsConfirmation?: boolean
  onGoToLogin: () => void
}

export function RegisterSuccessModal({
  isOpen,
  onClose,
  userEmail,
  needsConfirmation = false,
  onGoToLogin
}: RegisterSuccessModalProps) {
  return (
    <SuccessModal
      isOpen={isOpen}
      onClose={onClose}
      title={needsConfirmation ? "Conta criada!" : "Bem-vindo!"}
      message={
        needsConfirmation
          ? "Sua conta foi criada com sucesso! Verifique seu email para ativar a conta e fazer o primeiro login."
          : "Sua conta foi criada com sucesso! Você já pode fazer login e começar a usar a plataforma."
      }
      userEmail={userEmail}
      actionText="Fazer Login"
      onAction={onGoToLogin}
    />
  )
}