"""
Quick Test - Teste rápido do Legal Data Collector
"""
import asyncio
import sys
import os

# Add backend to path  
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.legal_data_collector import LegalDataCollector

async def quick_test():
    """Teste rápido das funcionalidades principais"""
    
    print("🧪 TESTE RÁPIDO DO LEGAL DATA COLLECTOR")
    print("="*50)
    
    try:
        async with LegalDataCollector() as collector:
            
            # Teste 1: Verificar se consegue criar uma instância
            print("✅ 1. Instância do collector criada")
            
            # Teste 2: Testar parsing de texto jurídico
            sample_html = """
            <div align="justify">
                <h2>LEI Nº 8.078, DE 11 DE SETEMBRO DE 1990</h2>
                <p>Art. 1º O presente código estabelece normas de proteção e defesa do consumidor.</p>
                <p>Art. 51. São nulas de pleno direito, entre outras, as cláusulas contratuais relativas ao fornecimento de produtos e serviços que:</p>
                <p>I - impossibilitem, exonerem ou atenuem a responsabilidade do fornecedor;</p>
            </div>
            """
            
            parsed_content = collector._parse_planalto_law(sample_html, "Código de Defesa do Consumidor")
            if "Art. 1º" in parsed_content and "Art. 51" in parsed_content:
                print("✅ 2. Parser de leis funcionando")
            else:
                print("❌ 2. Parser de leis com problema")
            
            # Teste 3: Testar limpeza de texto
            dirty_text = "    Presidência da República    Casa Civil    Art. 1º Teste    Voltar ao topo    "
            clean_text = collector._clean_legal_text(dirty_text)
            if "Art. 1º Teste" in clean_text and "Presidência" not in clean_text:
                print("✅ 3. Limpeza de texto funcionando")
            else:
                print("❌ 3. Limpeza de texto com problema")
            
            # Teste 4: Testar extração de palavras-chave
            keywords = collector._extract_keywords("Lei do Consumidor", "contrato fornecedor consumidor direito")
            if len(keywords) > 0 and "consumidor" in keywords:
                print("✅ 4. Extração de keywords funcionando")
            else:
                print("❌ 4. Extração de keywords com problema")
            
            print("\\n🎉 Teste rápido concluído!")
            print("💡 Para teste completo, execute: python legal_bootstrap.py")
            
    except Exception as e:
        print(f"❌ Erro no teste: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(quick_test())