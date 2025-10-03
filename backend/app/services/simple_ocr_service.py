"""
OCR Service Simplificado - Para desenvolvimento
Extrai texto de PDFs diretamente, simula OCR para imagens
"""

import io
from typing import Dict, Any
from pathlib import Path
import asyncio
import fitz  # PyMuPDF para PDFs
from PIL import Image, ImageDraw, ImageFont

from app.core.config import settings

class SimpleOCRService:
    """
    Serviço OCR simplificado para desenvolvimento
    - Extrai texto de PDFs diretamente
    - Simula OCR para imagens (placeholder)
    """
    
    def __init__(self):
        pass
        
    async def extract_text_from_pdf(self, pdf_content: bytes, max_pages: int = 10) -> Dict[str, Any]:
        """Extrai texto de PDF usando PyMuPDF"""
        
        try:
            pdf_document = fitz.open(stream=pdf_content, filetype="pdf")
            total_pages = len(pdf_document)
            pages_to_process = min(total_pages, max_pages)
            
            extracted_texts = []
            page_metadata = []
            
            print(f"📄 Processando PDF: {pages_to_process} páginas de {total_pages}")
            
            for page_num in range(pages_to_process):
                page = pdf_document[page_num]
                text = page.get_text()
                
                if text.strip():
                    extracted_texts.append(text)
                    page_metadata.append({
                        'page': page_num + 1,
                        'method': 'direct_text',
                        'char_count': len(text)
                    })
                    print(f"✅ Página {page_num + 1}: {len(text)} caracteres extraídos")
                else:
                    # PDF escaneado - placeholder para OCR futuro
                    placeholder_text = f"[Página {page_num + 1} - PDF escaneado. OCR será implementado com Google Cloud Vision API]"
                    extracted_texts.append(placeholder_text)
                    page_metadata.append({
                        'page': page_num + 1,
                        'method': 'placeholder',
                        'char_count': len(placeholder_text)
                    })
                    print(f"⚠️ Página {page_num + 1}: PDF escaneado (placeholder)")
            
            pdf_document.close()
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
        """Placeholder para OCR de imagem"""
        
        # Simular análise da imagem
        try:
            img = Image.open(io.BytesIO(image_content))
            width, height = img.size
            
            # Placeholder text baseado no tamanho da imagem
            placeholder_text = f"""[SIMULAÇÃO DE OCR - Google Cloud Vision API será implementada]

CONTRATO DE PRESTAÇÃO DE SERVIÇOS

Documento detectado: {width}x{height} pixels
Texto simulado para desenvolvimento:

CONTRATANTE: [Nome a ser extraído via OCR]
CONTRATADO: [Nome a ser extraído via OCR]

CLÁUSULA 1ª - Este texto será extraído automaticamente
quando a Google Cloud Vision API estiver configurada.

VALOR: R$ [Valor a ser extraído via OCR]

Para ativar OCR real:
1. Configurar projeto no Google Cloud Console
2. Habilitar Cloud Vision API
3. Configurar credenciais de serviço"""

            print(f"🖼️ Imagem processada: {width}x{height} (simulação)")
            return placeholder_text
            
        except Exception as e:
            return f"[Erro processando imagem: {e}]"
    
    async def process_contract_document(self, file_content: bytes, filename: str) -> Dict[str, Any]:
        """Processa documento de contrato"""
        
        print(f"📋 Processando contrato: {filename}")
        
        file_extension = Path(filename).suffix.lower()
        start_time = asyncio.get_event_loop().time()
        
        if file_extension == '.pdf':
            result = await self.extract_text_from_pdf(file_content, max_pages=20)
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
                'error': f'Tipo de arquivo não suportado: {file_extension}',
                'success': False
            }
        
        processing_time = asyncio.get_event_loop().time() - start_time
        
        if result.get('success'):
            result.update({
                'filename': filename,
                'file_type': file_extension[1:],
                'processing_time_seconds': round(processing_time, 2),
                'estimated_tokens': len(result['text']) // 4,
                'suitable_for_analysis': len(result['text']) > 100,
                'ocr_mode': 'development_simulation'  # Indica que é simulação
            })
            
            print(f"✅ Processamento concluído: {result['total_chars']} caracteres em {processing_time:.2f}s")
        else:
            print(f"❌ Falha no processamento: {result.get('error')}")
        
        return result

# Teste do serviço simplificado
async def test_simple_ocr():
    """Testa OCR simplificado"""
    
    service = SimpleOCRService()
    
    # Criar PDF de teste simples
    print("🧪 Testando Simple OCR Service...")
    
    # Criar imagem de teste
    img = Image.new('RGB', (800, 600), color='white')
    draw = ImageDraw.Draw(img)
    
    # Texto de contrato
    contract_text = """
    CONTRATO DE LOCAÇÃO RESIDENCIAL
    
    LOCADOR: Maria Silva, CPF 111.222.333-44
    LOCATÁRIO: João Santos, CPF 555.666.777-88
    
    IMÓVEL: Apartamento na Rua das Flores, 123
    VALOR: R$ 2.500,00 mensais
    PRAZO: 24 meses
    """
    
    # Desenhar texto
    try:
        font = ImageFont.load_default()
        y_offset = 50
        for line in contract_text.strip().split('\n'):
            draw.text((50, y_offset), line.strip(), fill='black', font=font)
            y_offset += 25
    except Exception as e:
        print(f"⚠️ Erro criando imagem de teste: {e}")
    
    # Converter para bytes
    img_buffer = io.BytesIO()
    img.save(img_buffer, format='PNG')
    img_bytes = img_buffer.getvalue()
    
    # Testar OCR
    try:
        result = await service.process_contract_document(img_bytes, "contrato_teste.png")
        
        print(f"\n📊 RESULTADO DO TESTE:")
        print(f"✅ Sucesso: {result['success']}")
        print(f"📄 Tipo: {result.get('file_type', 'N/A')}")
        print(f"⏱️ Tempo: {result.get('processing_time_seconds', 0):.2f}s")
        print(f"📝 Caracteres: {result.get('total_chars', 0)}")
        print(f"🔤 Tokens estimados: {result.get('estimated_tokens', 0)}")
        print(f"✅ Adequado para análise: {result.get('suitable_for_analysis', False)}")
        print(f"🛠️ Modo OCR: {result.get('ocr_mode', 'N/A')}")
        
        if result['success'] and result['text']:
            print(f"\n📋 TEXTO EXTRAÍDO (primeiros 300 chars):")
            text_preview = result['text'][:300] + "..." if len(result['text']) > 300 else result['text']
            print(text_preview)
        
        return result
        
    except Exception as e:
        print(f"❌ Erro no teste: {e}")
        return None

if __name__ == "__main__":
    asyncio.run(test_simple_ocr())