"""
Democratiza AI - Serviço de OCR com Google Cloud Vision API
Processa PDFs e imagens para extração de texto inteligente
"""

import os
import json
import logging
from typing import Optional, Dict, Any, List
from pathlib import Path
import io
import asyncio

try:
    from google.cloud import vision
    from google.oauth2 import service_account
    GOOGLE_VISION_AVAILABLE = True
except ImportError:
    GOOGLE_VISION_AVAILABLE = False
    logging.warning("Google Cloud Vision não instalado. Use: pip install google-cloud-vision")

try:
    import fitz  # PyMuPDF
    PYMUPDF_AVAILABLE = True
except ImportError:
    PYMUPDF_AVAILABLE = False
    logging.warning("PyMuPDF não instalado. Use: pip install PyMuPDF")

try:
    from PIL import Image
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False
    logging.warning("Pillow não instalado. Use: pip install Pillow")

from ..core.config import settings

logger = logging.getLogger(__name__)

class OCRService:
    """
    Serviço de OCR inteligente com múltiplas estratégias:
    1. Extração direta de texto (PDFs nativos)
    2. Google Cloud Vision OCR (PDFs escaneados/imagens)
    3. Fallback simples (quando OCR não disponível)
    """
    
    def __init__(self):
        self.client = None
        self.available = False
        self._initialize_client()
    
    def _initialize_client(self):
        """Inicializa cliente Google Cloud Vision de forma segura"""
        
        if not GOOGLE_VISION_AVAILABLE:
            logger.warning("⚠️ Google Cloud Vision não disponível - instale as dependências")
            return
        
        try:
            # Tentar carregar credenciais do arquivo JSON
            credentials_path = Path(__file__).parent.parent.parent / "credentials" / "google-cloud-credentials.json"
            
            if credentials_path.exists():
                logger.info(f"📁 Carregando credenciais: {credentials_path}")
                
                # Verificar se arquivo JSON está válido
                with open(credentials_path, 'r') as f:
                    credentials_data = json.load(f)
                
                if credentials_data.get('type') != 'service_account':
                    raise ValueError("Arquivo de credenciais inválido - não é service_account")
                
                credentials = service_account.Credentials.from_service_account_file(
                    str(credentials_path),
                    scopes=['https://www.googleapis.com/auth/cloud-platform']
                )
                
                self.client = vision.ImageAnnotatorClient(credentials=credentials)
                self.available = True
                logger.info("✅ Google Cloud Vision inicializado com sucesso")
                
            elif os.getenv('GOOGLE_APPLICATION_CREDENTIALS'):
                # Fallback para variável de ambiente
                logger.info("🔄 Tentando credenciais via variável de ambiente")
                self.client = vision.ImageAnnotatorClient()
                self.available = True
                logger.info("✅ Google Cloud Vision inicializado via env var")
                
            else:
                logger.warning("⚠️ Credenciais Google Cloud Vision não encontradas")
                
        except Exception as e:
            logger.error(f"❌ Erro ao inicializar Google Cloud Vision: {e}")
            self.client = None
            self.available = False
    
    async def extract_text_from_file(self, file_content: bytes, filename: str = "documento") -> Dict[str, Any]:
        """
        Extrai texto de arquivo (PDF ou imagem) usando estratégia inteligente
        """
        
        file_ext = Path(filename).suffix.lower()
        
        if file_ext == '.pdf':
            return await self.extract_text_from_pdf(file_content)
        elif file_ext in ['.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff']:
            return await self.extract_text_from_image(file_content)
        else:
            return {
                "text": f"Tipo de arquivo não suportado: {file_ext}",
                "method": "unsupported",
                "confidence": 0.0,
                "error": f"Extensão {file_ext} não suportada"
            }
    
    async def extract_text_from_pdf(self, file_content: bytes) -> Dict[str, Any]:
        """
        Extrai texto de PDF usando estratégia híbrida:
        1. PyMuPDF para PDFs com texto nativo (rápido)
        2. Google Vision OCR para PDFs escaneados (preciso)
        """
        
        try:
            # Estratégia 1: Tentativa de extração direta
            if PYMUPDF_AVAILABLE:
                direct_result = self._extract_text_directly_pdf(file_content)
                
                if direct_result and len(direct_result.strip()) > 100:
                    logger.info("✅ Texto extraído diretamente do PDF (nativo)")
                    return {
                        "text": direct_result,
                        "method": "direct_extraction",
                        "confidence": 0.98,
                        "pages": self._count_pdf_pages(file_content),
                        "processing_time": "< 1s"
                    }
            
            # Estratégia 2: OCR via Google Vision
            if self.available:
                logger.info("🔄 PDF parece escaneado, usando OCR...")
                ocr_result = await self._extract_pdf_via_ocr(file_content)
                return ocr_result
            
            # Estratégia 3: Fallback limitado
            logger.warning("⚠️ OCR não disponível, usando extração limitada")
            fallback_text = direct_result if 'direct_result' in locals() else "Texto não disponível para extração automática."
            
            return {
                "text": fallback_text,
                "method": "limited_fallback",
                "confidence": 0.3,
                "pages": 1,
                "warning": "OCR não configurado - apenas texto nativo extraído"
            }
            
        except Exception as e:
            logger.error(f"❌ Erro na extração de PDF: {e}")
            return {
                "text": f"Erro na extração: {str(e)}",
                "method": "error",
                "confidence": 0.0,
                "error": str(e)
            }
    
    def _extract_text_directly_pdf(self, file_content: bytes) -> str:
        """Extração direta usando PyMuPDF"""
        if not PYMUPDF_AVAILABLE:
            return ""
        
        try:
            doc = fitz.open(stream=file_content, filetype="pdf")
            text_parts = []
            
            for page_num in range(doc.page_count):
                page = doc[page_num]
                text = page.get_text()
                if text.strip():
                    text_parts.append(f"=== Página {page_num + 1} ===\n{text.strip()}")
            
            doc.close()
            return "\n\n".join(text_parts)
            
        except Exception as e:
            logger.warning(f"Extração direta PyMuPDF falhou: {e}")
            return ""
    
    def _count_pdf_pages(self, file_content: bytes) -> int:
        """Conta páginas do PDF"""
        if not PYMUPDF_AVAILABLE:
            return 1
        
        try:
            doc = fitz.open(stream=file_content, filetype="pdf")
            page_count = doc.page_count
            doc.close()
            return page_count
        except:
            return 1
    
    async def _extract_pdf_via_ocr(self, file_content: bytes) -> Dict[str, Any]:
        """Extração via Google Cloud Vision OCR"""
        
        if not self.available:
            raise Exception("Google Cloud Vision não está disponível")
        
        try:
            # Converter PDF para imagens
            images = await self._pdf_to_images(file_content)
            
            if not images:
                raise Exception("Não foi possível converter PDF para imagens")
            
            all_text = []
            confidences = []
            
            for i, image_bytes in enumerate(images):
                logger.info(f"📄 Processando página {i + 1}/{len(images)}...")
                
                # OCR da imagem
                vision_image = vision.Image(content=image_bytes)
                response = self.client.text_detection(image=vision_image)
                
                if response.error.message:
                    logger.error(f"Erro OCR página {i+1}: {response.error.message}")
                    continue
                
                if response.full_text_annotation:
                    page_text = response.full_text_annotation.text
                    confidence = self._calculate_confidence(response.full_text_annotation)
                    
                    all_text.append(f"=== Página {i + 1} ===\n{page_text.strip()}")
                    confidences.append(confidence)
                else:
                    all_text.append(f"=== Página {i + 1} ===\n[Nenhum texto detectado]")
                    confidences.append(0.0)
            
            final_text = "\n\n".join(all_text)
            avg_confidence = sum(confidences) / len(confidences) if confidences else 0.0
            
            return {
                "text": final_text,
                "method": "google_vision_ocr",
                "confidence": avg_confidence,
                "pages": len(images),
                "processing_time": f"~{len(images) * 2}s"
            }
            
        except Exception as e:
            logger.error(f"OCR via Google Vision falhou: {e}")
            raise Exception(f"Erro no OCR: {str(e)}")
    
    async def _pdf_to_images(self, file_content: bytes) -> List[bytes]:
        """Converte PDF para lista de imagens"""
        
        try:
            # Usar pdf2image se disponível
            try:
                import pdf2image
                images = pdf2image.convert_from_bytes(file_content, dpi=200)
                
                image_bytes_list = []
                for image in images:
                    img_byte_arr = io.BytesIO()
                    image.save(img_byte_arr, format='PNG', quality=95)
                    image_bytes_list.append(img_byte_arr.getvalue())
                
                return image_bytes_list
                
            except ImportError:
                # Fallback usando PyMuPDF para renderizar páginas
                if not PYMUPDF_AVAILABLE:
                    raise Exception("pdf2image e PyMuPDF não disponíveis para conversão PDF->imagem")
                
                doc = fitz.open(stream=file_content, filetype="pdf")
                image_bytes_list = []
                
                for page_num in range(doc.page_count):
                    page = doc[page_num]
                    # Renderizar página como imagem
                    pix = page.get_pixmap(matrix=fitz.Matrix(2.0, 2.0))  # 2x zoom para melhor qualidade
                    img_data = pix.tobytes("png")
                    image_bytes_list.append(img_data)
                
                doc.close()
                return image_bytes_list
                
        except Exception as e:
            logger.error(f"Erro na conversão PDF->imagem: {e}")
            return []
    
    async def extract_text_from_image(self, image_content: bytes) -> Dict[str, Any]:
        """Extrai texto de imagem usando Google Cloud Vision"""
        
        if not self.available:
            return {
                "text": "OCR não disponível - configure Google Cloud Vision",
                "method": "unavailable",
                "confidence": 0.0,
                "error": "Google Cloud Vision não configurado"
            }
        
        try:
            # Validar se é uma imagem válida
            if PIL_AVAILABLE:
                try:
                    img = Image.open(io.BytesIO(image_content))
                    img.verify()  # Verificar se imagem é válida
                except Exception:
                    return {
                        "text": "Arquivo de imagem inválido ou corrompido",
                        "method": "error",
                        "confidence": 0.0,
                        "error": "Imagem inválida"
                    }
            
            # Fazer OCR
            image = vision.Image(content=image_content)
            response = self.client.text_detection(image=image)
            
            if response.error.message:
                raise Exception(f"Erro OCR: {response.error.message}")
            
            if response.full_text_annotation:
                text = response.full_text_annotation.text
                confidence = self._calculate_confidence(response.full_text_annotation)
                
                return {
                    "text": text.strip(),
                    "method": "google_vision_ocr",
                    "confidence": confidence,
                    "pages": 1,
                    "processing_time": "~2s"
                }
            else:
                return {
                    "text": "Nenhum texto foi encontrado na imagem",
                    "method": "google_vision_ocr",
                    "confidence": 0.0,
                    "pages": 1,
                    "warning": "Imagem sem texto detectável"
                }
                
        except Exception as e:
            logger.error(f"Erro no OCR de imagem: {e}")
            return {
                "text": f"Erro na análise da imagem: {str(e)}",
                "method": "error",
                "confidence": 0.0,
                "error": str(e)
            }
    
    def _calculate_confidence(self, annotation) -> float:
        """Calcula confiança média da detecção de texto"""
        if not annotation.pages:
            return 0.0
        
        confidences = []
        for page in annotation.pages:
            for block in page.blocks:
                if hasattr(block, 'confidence') and block.confidence > 0:
                    confidences.append(block.confidence)
        
        return sum(confidences) / len(confidences) if confidences else 0.0
    
    def is_available(self) -> bool:
        """Verifica se o serviço OCR está disponível"""
        return self.available and self.client is not None
    
    def get_status(self) -> Dict[str, Any]:
        """Retorna status detalhado do serviço OCR"""
        credentials_path = Path(__file__).parent.parent.parent / "credentials" / "google-cloud-credentials.json"
        
        return {
            "available": self.available,
            "google_vision_installed": GOOGLE_VISION_AVAILABLE,
            "pymupdf_available": PYMUPDF_AVAILABLE,
            "pil_available": PIL_AVAILABLE,
            "credentials_found": credentials_path.exists(),
            "service_account": getattr(settings, 'GOOGLE_CLOUD_SERVICE_ACCOUNT_EMAIL', None),
            "project_id": getattr(settings, 'GOOGLE_CLOUD_PROJECT_ID', None)
        }

# Instância global do serviço
ocr_service = OCRService()


# Função de teste segura
async def test_ocr_basic():
    """Teste básico do OCR sem expor credenciais"""
    
    service = OCRService()
    status = service.get_status()
    
    print("🔍 STATUS OCR SERVICE")
    print("=" * 40)
    for key, value in status.items():
        print(f"{key}: {value}")
    
    print(f"\n✅ OCR Disponível: {service.is_available()}")
    
    if service.is_available():
        print("🎉 Google Cloud Vision configurado com sucesso!")
    else:
        print("⚠️ OCR não disponível - verifique configurações")

if __name__ == "__main__":
    asyncio.run(test_ocr_basic())