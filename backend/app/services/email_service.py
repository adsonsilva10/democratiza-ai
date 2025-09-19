from typing import List, Dict, Any, Optional
import sendgrid
from sendgrid.helpers.mail import Mail, Email, To, Content
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

class EmailService:
    """Service for sending transactional emails via SendGrid"""
    
    def __init__(self):
        self.sg = sendgrid.SendGridAPIClient(api_key=settings.SENDGRID_API_KEY)
        self.from_email = Email("noreply@contratoseguro.com.br", "Contrato Seguro")
    
    async def send_welcome_email(self, user_email: str, user_name: str) -> bool:
        """Send welcome email to new users"""
        
        subject = "Bem-vindo ao Contrato Seguro!"
        
        html_content = f"""
        <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
            <h1 style="color: #2563eb;">Bem-vindo ao Contrato Seguro, {user_name}!</h1>
            
            <p>Parabéns por dar o primeiro passo para tornar seus contratos mais seguros!</p>
            
            <p>Com o Contrato Seguro, você pode:</p>
            <ul>
                <li>✅ Analisar contratos com IA especializada em legislação brasileira</li>
                <li>✅ Identificar cláusulas abusivas e riscos</li>
                <li>✅ Conversar com nossa IA para esclarecer dúvidas</li>
                <li>✅ Receber relatórios detalhados e recomendações</li>
            </ul>
            
            <div style="text-align: center; margin: 30px 0;">
                <a href="https://contratoseguro.com.br/dashboard" 
                   style="background-color: #2563eb; color: white; padding: 15px 30px; text-decoration: none; border-radius: 8px; display: inline-block;">
                    Começar a Analisar Contratos
                </a>
            </div>
            
            <p>Se tiver dúvidas, nossa equipe está aqui para ajudar!</p>
            
            <p>Atenciosamente,<br>Equipe Contrato Seguro</p>
            
            <hr style="margin: 30px 0; border: none; border-top: 1px solid #e5e7eb;">
            <p style="font-size: 12px; color: #6b7280;">
                Este email foi enviado porque você criou uma conta no Contrato Seguro.
            </p>
        </div>
        """
        
        return await self._send_email(user_email, subject, html_content)
    
    async def send_analysis_complete_email(
        self, 
        user_email: str, 
        user_name: str, 
        contract_title: str,
        risk_level: str,
        contract_id: str
    ) -> bool:
        """Send email when contract analysis is complete"""
        
        subject = f"Análise completa: {contract_title}"
        
        risk_color = {
            "Alto Risco": "#dc2626",
            "Médio Risco": "#d97706", 
            "Baixo Risco": "#16a34a"
        }.get(risk_level, "#6b7280")
        
        html_content = f"""
        <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
            <h1 style="color: #2563eb;">Análise Concluída!</h1>
            
            <p>Olá {user_name},</p>
            
            <p>A análise do seu contrato foi concluída com sucesso!</p>
            
            <div style="background-color: #f8fafc; padding: 20px; border-radius: 8px; margin: 20px 0;">
                <h3 style="margin: 0 0 10px 0; color: #374151;">📄 {contract_title}</h3>
                <p style="margin: 0;">
                    <strong>Nível de Risco:</strong> 
                    <span style="color: {risk_color}; font-weight: bold;">{risk_level}</span>
                </p>
            </div>
            
            <div style="text-align: center; margin: 30px 0;">
                <a href="https://contratoseguro.com.br/contracts/{contract_id}" 
                   style="background-color: #2563eb; color: white; padding: 15px 30px; text-decoration: none; border-radius: 8px; display: inline-block;">
                    Ver Análise Completa
                </a>
            </div>
            
            <p>A análise inclui:</p>
            <ul>
                <li>Identificação de cláusulas potencialmente abusivas</li>
                <li>Avaliação de riscos por categoria</li>
                <li>Recomendações específicas</li>
                <li>Base legal para cada ponto identificado</li>
            </ul>
            
            <p>Atenciosamente,<br>Equipe Contrato Seguro</p>
        </div>
        """
        
        return await self._send_email(user_email, subject, html_content)
    
    async def send_subscription_confirmation_email(
        self,
        user_email: str,
        user_name: str,
        subscription_type: str,
        expiration_date: str
    ) -> bool:
        """Send subscription confirmation email"""
        
        subject = "Assinatura confirmada - Contrato Seguro"
        
        features = {
            "basic": [
                "Análise de até 10 contratos por mês",
                "Chat com IA especializada",
                "Relatórios de risco básicos",
                "Suporte por email"
            ],
            "premium": [
                "Análise ilimitada de contratos",
                "Chat com IA especializada",
                "Relatórios detalhados de risco",
                "Assinatura eletrônica D4Sign",
                "Suporte prioritário",
                "Histórico completo"
            ]
        }
        
        feature_list = "".join([f"<li>✅ {feature}</li>" for feature in features.get(subscription_type, [])])
        
        html_content = f"""
        <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
            <h1 style="color: #2563eb;">Assinatura Confirmada! 🎉</h1>
            
            <p>Olá {user_name},</p>
            
            <p>Sua assinatura <strong>{subscription_type.title()}</strong> foi confirmada com sucesso!</p>
            
            <div style="background-color: #f0f9ff; padding: 20px; border-radius: 8px; margin: 20px 0; border-left: 4px solid #2563eb;">
                <h3 style="margin: 0 0 15px 0; color: #1e40af;">Seus Benefícios:</h3>
                <ul style="margin: 0; padding-left: 20px;">
                    {feature_list}
                </ul>
            </div>
            
            <p><strong>Válida até:</strong> {expiration_date}</p>
            
            <div style="text-align: center; margin: 30px 0;">
                <a href="https://contratoseguro.com.br/dashboard" 
                   style="background-color: #2563eb; color: white; padding: 15px 30px; text-decoration: none; border-radius: 8px; display: inline-block;">
                    Acessar Dashboard
                </a>
            </div>
            
            <p>Agora você pode aproveitar todos os recursos da sua assinatura!</p>
            
            <p>Atenciosamente,<br>Equipe Contrato Seguro</p>
        </div>
        """
        
        return await self._send_email(user_email, subject, html_content)
    
    async def send_password_reset_email(
        self,
        user_email: str,
        user_name: str,
        reset_token: str
    ) -> bool:
        """Send password reset email"""
        
        subject = "Redefinir senha - Contrato Seguro"
        reset_url = f"https://contratoseguro.com.br/auth/reset-password?token={reset_token}"
        
        html_content = f"""
        <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
            <h1 style="color: #2563eb;">Redefinir Senha</h1>
            
            <p>Olá {user_name},</p>
            
            <p>Recebemos uma solicitação para redefinir a senha da sua conta.</p>
            
            <div style="text-align: center; margin: 30px 0;">
                <a href="{reset_url}" 
                   style="background-color: #2563eb; color: white; padding: 15px 30px; text-decoration: none; border-radius: 8px; display: inline-block;">
                    Redefinir Senha
                </a>
            </div>
            
            <p>Este link é válido por 1 hora por motivos de segurança.</p>
            
            <p>Se você não solicitou esta redefinição, pode ignorar este email.</p>
            
            <p>Atenciosamente,<br>Equipe Contrato Seguro</p>
        </div>
        """
        
        return await self._send_email(user_email, subject, html_content)
    
    async def _send_email(self, to_email: str, subject: str, html_content: str) -> bool:
        """Internal method to send email via SendGrid"""
        
        try:
            mail = Mail(
                from_email=self.from_email,
                to_emails=To(to_email),
                subject=subject,
                html_content=Content("text/html", html_content)
            )
            
            response = self.sg.send(mail)
            
            if response.status_code in [200, 201, 202]:
                logger.info(f"Email sent successfully to {to_email}")
                return True
            else:
                logger.error(f"Failed to send email to {to_email}. Status: {response.status_code}")
                return False
                
        except Exception as e:
            logger.error(f"Error sending email to {to_email}: {str(e)}")
            return False

# Global email service instance
email_service = EmailService()
