"""
OCR Service - Extração de texto de documentos
Usa Google Cloud Vision API para extrair texto de PDFs e imagens
"""

import io
import base64
from typing import Optional, List, Dict, Any
from pathlib import Path
import asyncio
import httpx
from PIL import Image
import fitz  # PyMuPDF para PDFs

from app.core.config import settings

class OCRService:
    """
    Serviço de OCR usando Google Cloud Vision API
    Extrai texto de PDFs, imagens e documentos escaneados
    """
    
    def __init__(self):
        self.api_key = settings.GOOGLE_API_KEY
        self.base_url = "https://vision.googleapis.com/v1/images:annotate"
        
    async def extract_text_from_pdf(self, pdf_content: bytes, max_pages: int = 10) -> Dict[str, Any]:
        """
        Extrai texto de PDF convertendo páginas em imagens
        
        Args:
            pdf_content: Conteúdo binário do PDF
            max_pages: Máximo de páginas para processar
            
        Returns:
            Dict com texto extraído, número de páginas e metadados
        """
        
        try:
            # Abrir PDF com PyMuPDF
            pdf_document = fitz.open(stream=pdf_content, filetype="pdf")
            total_pages = len(pdf_document)
            
            # Limitar páginas processadas
            pages_to_process = min(total_pages, max_pages)
            
            extracted_texts = []
            page_metadata = []
            
            print(f"📄 Processando PDF: {pages_to_process} páginas de {total_pages}")
            
            for page_num in range(pages_to_process):
                page = pdf_document[page_num]
                
                # Tentar extrair texto diretamente (se for PDF com texto)
                direct_text = page.get_text()
                
                if direct_text.strip() and len(direct_text.strip()) > 50:
                    # PDF tem texto extraível
                    print(f"✅ Página {page_num + 1}: Texto direto extraído")
                    extracted_texts.append(direct_text)
                    page_metadata.append({
                        'page': page_num + 1,
                        'method': 'direct_text',
                        'char_count': len(direct_text)
                    })
                    
                else:
                    # PDF escaneado, usar OCR
                    print(f"🔍 Página {page_num + 1}: Usando OCR...")
                    
                    # Converter página para imagem
                    pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))  # 2x zoom para melhor qualidade
                    img_data = pix.tobytes("png")
                    
                    # Extrair texto via OCR
                    ocr_text = await self.extract_text_from_image(img_data)
                    
                    extracted_texts.append(ocr_text)
                    page_metadata.append({
                        'page': page_num + 1,
                        'method': 'ocr',
                        'char_count': len(ocr_text)
                    })
            
            pdf_document.close()
            
            # Combinar todo o texto
            full_text = "\n\n".join(extracted_texts)
            
            return {
                'text': full_text,
                'total_pages': total_pages,
                'processed_pages': pages_to_process,
                'page_metadata': page_metadata,
                'total_chars': len(full_text),
                'success': True
            }
            
        except Exception as e:
            print(f"❌ Erro processando PDF: {e}")
            return {
                'text': '',
                'error': str(e),
                'success': False
            }
    
    async def extract_text_from_image(self, image_content: bytes) -> str:
        """
        Extrai texto de imagem usando Google Cloud Vision
        
        Args:
            image_content: Conteúdo binário da imagem
            
        Returns:
            Texto extraído da imagem
        """
        
        if not self.api_key:
            raise ValueError("Google API Key não configurada")
        
        try:
            # Converter imagem para base64
            image_base64 = base64.b64encode(image_content).decode('utf-8')
            
            # Preparar payload para Vision API
            payload = {
                "requests": [{
                    "image": {
                        "content": image_base64
                    },
                    "features": [{
                        "type": "TEXT_DETECTION",
                        "maxResults": 1
                    }]
                }]
            }
            
            # Fazer requisição para Vision API
            url = f"{self.base_url}?key={self.api_key}"
            
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(url, json=payload)
                
                if response.status_code == 200:
                    result = response.json()
                    
                    if 'responses' in result and result['responses']:
                        text_annotations = result['responses'][0].get('textAnnotations', [])
                        
                        if text_annotations:
                            # Primeiro resultado contém todo o texto
                            extracted_text = text_annotations[0]['description']
                            return extracted_text.strip()
                        else:
                            print("⚠️ Nenhum texto encontrado na imagem")
                            return ""
                    else:
                        print(f"❌ Resposta inválida da Vision API: {result}")
                        return ""
                else:
                    print(f"❌ Erro Vision API: {response.status_code} - {response.text}")
                    return ""
                    
        except Exception as e:
            print(f"❌ Erro extraindo texto de imagem: {e}")
            return ""
    
    async def extract_text_from_file(self, file_path: str) -> Dict[str, Any]:
        """
        Extrai texto de arquivo (PDF ou imagem)
        
        Args:
            file_path: Caminho para o arquivo
            
        Returns:
            Dict com resultado da extração
        """
        
        file_path = Path(file_path)
        
        if not file_path.exists():
            return {
                'text': '',
                'error': 'Arquivo não encontrado',
                'success': False
            }
        
        # Ler conteúdo do arquivo
        with open(file_path, 'rb') as f:
            file_content = f.read()
        
        # Determinar tipo do arquivo pela extensão
        file_extension = file_path.suffix.lower()
        
        if file_extension == '.pdf':
            return await self.extract_text_from_pdf(file_content)
            
        elif file_extension in ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp']:
            text = await self.extract_text_from_image(file_content)
            return {
                'text': text,
                'file_type': 'image',
                'total_chars': len(text),
                'success': True
            }
            
        else:
            return {
                'text': '',
                'error': f'Tipo de arquivo não suportado: {file_extension}',
                'success': False
            }
    
    async def process_contract_document(self, file_content: bytes, filename: str) -> Dict[str, Any]:
        """
        Processa documento de contrato especificamente
        Otimizado para extração de texto jurídico
        
        Args:
            file_content: Conteúdo binário do arquivo
            filename: Nome do arquivo original
            
        Returns:
            Dict com texto processado e metadados
        """
        
        print(f"📋 Processando contrato: {filename}")
        
        # Determinar tipo do arquivo
        file_extension = Path(filename).suffix.lower()
        
        start_time = asyncio.get_event_loop().time()
        
        if file_extension == '.pdf':
            result = await self.extract_text_from_pdf(file_content, max_pages=20)  # Máximo 20 páginas para contratos
        elif file_extension in ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp']:
            text = await self.extract_text_from_image(file_content)
            result = {
                'text': text,
                'file_type': 'image',
                'total_chars': len(text),
                'success': True
            }
        else:
            result = {
                'text': '',
                'error': f'Tipo de arquivo não suportado para contratos: {file_extension}',
                'success': False
            }
        
        processing_time = asyncio.get_event_loop().time() - start_time
        
        if result.get('success'):
            # Adicionar metadados específicos para contratos
            result.update({
                'filename': filename,
                'file_type': file_extension[1:],  # Remove o ponto
                'processing_time_seconds': round(processing_time, 2),
                'estimated_tokens': len(result['text']) // 4,  # Estimativa rough de tokens
                'suitable_for_analysis': len(result['text']) > 100,  # Mínimo de texto para análise
            })
            
            print(f"✅ Processamento concluído: {result['total_chars']} caracteres em {processing_time:.2f}s")
        else:
            print(f"❌ Falha no processamento: {result.get('error')}")
        
        return result

# Função utilitária para teste
async def test_ocr_service():
    """Testa o serviço de OCR com um exemplo"""
    
    service = OCRService()
    
    # Criar uma imagem de teste simples com texto
    from PIL import Image, ImageDraw, ImageFont
    
    # Criar imagem com texto de contrato
    img = Image.new('RGB', (800, 600), color='white')
    draw = ImageDraw.Draw(img)
    
    contract_text = """
    CONTRATO DE PRESTAÇÃO DE SERVIÇOS
    
    Entre as partes:
    
    CONTRATANTE: João Silva, CPF 123.456.789-00
    CONTRATADO: Empresa XYZ LTDA, CNPJ 12.345.678/0001-90
    
    CLÁUSULA 1ª - DO OBJETO
    O presente contrato tem por objeto a prestação de serviços
    de consultoria empresarial pelo período de 12 meses.
    
    CLÁUSULA 2ª - DO VALOR
    O valor total do contrato é de R$ 120.000,00 (cento e
    vinte mil reais), a ser pago em 12 parcelas mensais.
    """
    
    # Tentar usar uma fonte
    try:
        font = ImageFont.truetype("arial.ttf", 16)
    except:
        font = ImageFont.load_default()
    
    # Desenhar texto na imagem
    y_offset = 50
    for line in contract_text.strip().split('\n'):
        draw.text((50, y_offset), line.strip(), fill='black', font=font)
        y_offset += 25
    
    # Salvar como bytes
    img_buffer = io.BytesIO()
    img.save(img_buffer, format='PNG')
    img_bytes = img_buffer.getvalue()
    
    # Testar OCR
    print("🧪 Testando OCR Service...")
    
    try:
        result = await service.process_contract_document(img_bytes, "contrato_teste.png")
        
        print(f"✅ Resultado: {result['success']}")
        if result['success']:
            print(f"📝 Texto extraído ({result['total_chars']} chars):")
            print(result['text'][:200] + "..." if len(result['text']) > 200 else result['text'])
        else:
            print(f"❌ Erro: {result['error']}")
            
    except Exception as e:
        print(f"❌ Erro no teste: {e}")

if __name__ == "__main__":
    asyncio.run(test_ocr_service())