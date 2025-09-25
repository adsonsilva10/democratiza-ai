"""
Legal Data Collector - Sistema de coleta automatizada de dados jurídicos brasileiros
Coleta leis, jurisprudência e regulamentações de fontes oficiais
"""
import asyncio
import aiohttp
import aiofiles
import re
import json
from typing import Dict, List, Optional, Tuple
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from datetime import datetime
import hashlib
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LegalDataCollector:
    """Coletor automatizado e ético de dados jurídicos brasileiros"""
    
    def __init__(self):
        self.session = None
        self.rate_limit_delay = 3.0  # 3 segundos entre requests para ser respeitoso
        self.collected_data = []
        
        # Headers para parecer um navegador real e ser respeitoso
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'pt-BR,pt;q=0.8,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
    
    async def __aenter__(self):
        """Context manager para gerenciar sessão HTTP"""
        connector = aiohttp.TCPConnector(limit=1, limit_per_host=1)
        timeout = aiohttp.ClientTimeout(total=30, connect=10)
        self.session = aiohttp.ClientSession(
            connector=connector,
            timeout=timeout,
            headers=self.headers
        )
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Fechar sessão HTTP"""
        if self.session:
            await self.session.close()
    
    async def _fetch_with_rate_limit(self, url: str) -> Optional[str]:
        """Fetch URL com rate limiting e tratamento de erros"""
        
        try:
            logger.info(f"🌐 Coletando: {url}")
            
            # Rate limiting respeitoso
            await asyncio.sleep(self.rate_limit_delay)
            
            async with self.session.get(url) as response:
                if response.status == 200:
                    content = await response.text(encoding='utf-8')
                    logger.info(f"✅ Coletado com sucesso: {len(content)} caracteres")
                    return content
                else:
                    logger.warning(f"⚠️  Status {response.status} para {url}")
                    return None
                    
        except asyncio.TimeoutError:
            logger.error(f"⏰ Timeout para {url}")
            return None
        except Exception as e:
            logger.error(f"❌ Erro ao coletar {url}: {str(e)}")
            return None
    
    async def collect_planalto_laws(self) -> List[Dict]:
        """Coleta leis fundamentais do portal planalto.gov.br"""
        
        logger.info("📚 Iniciando coleta de leis do Planalto...")
        
        # Leis fundamentais para análise de contratos
        fundamental_laws = {
            "Código Civil - Contratos": {
                "url": "http://www.planalto.gov.br/ccivil_03/leis/2002/l10406.htm",
                "category": "geral",
                "priority_sections": ["TÍTULO V", "CAPÍTULO I", "Seção I"]  # Seções sobre contratos
            },
            "Código de Defesa do Consumidor": {
                "url": "http://www.planalto.gov.br/ccivil_03/leis/l8078.htm", 
                "category": "geral",
                "priority_sections": ["CAPÍTULO VI"]  # Práticas abusivas
            },
            "Lei do Inquilinato": {
                "url": "http://www.planalto.gov.br/ccivil_03/leis/l8245.htm",
                "category": "locacao",
                "priority_sections": ["CAPÍTULO I", "CAPÍTULO II"]
            },
            "Lei Geral de Telecomunicações": {
                "url": "http://www.planalto.gov.br/ccivil_03/leis/l9472.htm",
                "category": "telecom", 
                "priority_sections": ["TÍTULO V"]  # Direitos dos usuários
            },
            "Lei do Sistema Financeiro Nacional": {
                "url": "http://www.planalto.gov.br/ccivil_03/leis/l4595.htm",
                "category": "financeiro",
                "priority_sections": ["CAPÍTULO III"]
            }
        }
        
        laws_data = []
        
        for law_name, law_info in fundamental_laws.items():
            try:
                html_content = await self._fetch_with_rate_limit(law_info["url"])
                
                if html_content:
                    # Parse e limpeza do HTML
                    cleaned_content = self._parse_planalto_law(html_content, law_name)
                    
                    if cleaned_content:
                        # Criar hash único para detectar mudanças futuras
                        content_hash = hashlib.md5(cleaned_content.encode()).hexdigest()
                        
                        law_data = {
                            "title": law_name,
                            "content": cleaned_content,
                            "document_type": "lei",
                            "category": law_info["category"],
                            "source": "Planalto.gov.br",
                            "source_url": law_info["url"],
                            "reference_number": self._extract_law_number(law_name),
                            "authority_level": "high",
                            "legal_area": self._determine_legal_areas(law_name),
                            "keywords": self._extract_keywords(law_name, cleaned_content),
                            "collection_date": datetime.now().isoformat(),
                            "content_hash": content_hash
                        }
                        
                        laws_data.append(law_data)
                        logger.info(f"✅ Lei processada: {law_name}")
                    else:
                        logger.warning(f"⚠️  Conteúdo vazio para {law_name}")
                else:
                    logger.error(f"❌ Falha ao coletar {law_name}")
                    
            except Exception as e:
                logger.error(f"❌ Erro processando {law_name}: {str(e)}")
                continue
        
        logger.info(f"📋 Total de leis coletadas: {len(laws_data)}")
        return laws_data
    
    def _parse_planalto_law(self, html_content: str, law_name: str) -> str:
        """Parse específico para estrutura HTML do Planalto"""
        
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Remover elementos desnecessários
        for tag in soup(["script", "style", "nav", "header", "footer"]):
            tag.decompose()
        
        # Tentar diferentes seletores para o conteúdo principal
        content_selectors = [
            'div[align="justify"]',  # Estrutura comum do Planalto
            'div.texto-lei',
            '#content-core',
            'body > div:nth-child(3)',  # Estrutura específica observada
            'td[align="justify"]'  # Tabelas com texto da lei
        ]
        
        text_content = ""
        
        for selector in content_selectors:
            elements = soup.select(selector)
            if elements:
                for element in elements:
                    text = element.get_text(separator='\\n', strip=True)
                    if len(text) > 1000:  # Filtro por tamanho mínimo
                        text_content += text + "\\n\\n"
                break
        
        # Se não encontrou pelos seletores, pegar todo o body
        if not text_content:
            body = soup.find('body')
            if body:
                text_content = body.get_text(separator='\\n', strip=True)
        
        # Limpeza e normalização do texto
        cleaned_text = self._clean_legal_text(text_content)
        
        # Filtrar apenas o texto da lei (remover navegação, etc.)
        law_text = self._extract_law_content(cleaned_text, law_name)
        
        return law_text
    
    def _clean_legal_text(self, text: str) -> str:
        """Limpa e normaliza texto jurídico extraído"""
        
        # Remover elementos de navegação e layout
        navigation_patterns = [
            r"Presidência da República.*?Casa Civil",
            r"Subchefia para Assuntos Jurídicos",
            r"Imprimir.*?Voltar ao topo", 
            r"Este texto não substitui.*?publicado",
            r"Vide.*?Regulamento",
            r"\\(Vide.*?\\)",
            r"Menu.*?Buscar",
            r"Compartilhar.*?Imprimir"
        ]
        
        cleaned = text
        for pattern in navigation_patterns:
            cleaned = re.sub(pattern, "", cleaned, flags=re.IGNORECASE | re.DOTALL)
        
        # Normalizar espaços em branco
        cleaned = re.sub(r'\\s+', ' ', cleaned)
        cleaned = re.sub(r'\\n\\s*\\n', '\\n\\n', cleaned)  # Duplas quebras
        
        # Remover linhas muito curtas (provavelmente navegação)
        lines = cleaned.split('\\n')
        meaningful_lines = []
        
        for line in lines:
            line = line.strip()
            if len(line) > 10 and not self._is_navigation_line(line):
                meaningful_lines.append(line)
        
        return '\\n'.join(meaningful_lines)
    
    def _is_navigation_line(self, line: str) -> bool:
        """Identifica se uma linha é elemento de navegação"""
        
        navigation_keywords = [
            "menu", "buscar", "imprimir", "voltar", "topo",
            "compartilhar", "facebook", "twitter", "whatsapp",
            "presidência", "casa civil", "planalto"
        ]
        
        line_lower = line.lower()
        return any(keyword in line_lower for keyword in navigation_keywords)
    
    def _extract_law_content(self, text: str, law_name: str) -> str:
        """Extrai apenas o conteúdo da lei, removendo preâmbulos"""
        
        # Procurar pelo início típico de leis brasileiras
        law_start_patterns = [
            r"Art\\.?\\s*1[°º]",  # Artigo 1°
            r"Artigo\\s+1[°º]",
            r"CAPÍTULO\\s+I",
            r"TÍTULO\\s+I",
            law_name.split()[0] if law_name else ""
        ]
        
        for pattern in law_start_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                # Pegar do início da lei em diante
                law_content = text[match.start():]
                
                # Remover rodapé se houver
                footer_patterns = [
                    r"Brasília.*?\\d{4}",
                    r"Este texto.*?DOU",
                    r"Publicado.*?Seção"
                ]
                
                for footer_pattern in footer_patterns:
                    law_content = re.sub(footer_pattern, "", law_content, flags=re.IGNORECASE | re.DOTALL)
                
                return law_content.strip()
        
        # Se não achou padrão específico, retornar texto limpo
        return text
    
    def _extract_law_number(self, law_name: str) -> str:
        """Extrai número/referência da lei"""
        
        # Procurar padrões como "Lei 8.245/91", "Decreto 1.234/2020"
        patterns = [
            r"Lei\\s+(\\d+\\.?\\d*/\\d+)",
            r"Decreto\\s+(\\d+\\.?\\d*/\\d+)",
            r"Código\\s+(\\w+)"
        ]
        
        for pattern in patterns:
            match = re.search(pattern, law_name, re.IGNORECASE)
            if match:
                return match.group(1)
        
        return law_name
    
    def _determine_legal_areas(self, law_name: str) -> List[str]:
        """Determina áreas do direito aplicáveis"""
        
        area_mapping = {
            "civil": ["direito civil", "contratos"],
            "consumidor": ["direito do consumidor", "contratos"],
            "inquilinato": ["direito imobiliário", "locação"],
            "telecomunicações": ["direito das telecomunicações", "regulatório"],
            "financeiro": ["direito bancário", "financeiro"]
        }
        
        law_lower = law_name.lower()
        areas = []
        
        for key, values in area_mapping.items():
            if key in law_lower:
                areas.extend(values)
        
        return areas if areas else ["direito geral"]
    
    def _extract_keywords(self, law_name: str, content: str) -> List[str]:
        """Extrai palavras-chave relevantes"""
        
        # Keywords específicas por tipo de lei
        base_keywords = []
        
        if "civil" in law_name.lower():
            base_keywords = ["contrato", "obrigação", "direito", "cláusula"]
        elif "consumidor" in law_name.lower():
            base_keywords = ["consumidor", "fornecedor", "abusiva", "direito"]
        elif "inquilinato" in law_name.lower():
            base_keywords = ["locação", "aluguel", "locador", "locatário"]
        elif "telecomunicações" in law_name.lower():
            base_keywords = ["telecomunicações", "usuário", "serviço", "ANATEL"]
        
        # Extrair termos jurídicos do conteúdo
        legal_terms_pattern = r"\\b(artigo?|parágrafo|inciso|alínea|cláusula|contrato|direito|dever|obrigação)\\b"
        legal_terms = re.findall(legal_terms_pattern, content.lower())
        
        # Combinar e deduplicar
        all_keywords = base_keywords + list(set(legal_terms))
        
        return list(set(all_keywords))[:10]  # Limitar a 10 keywords
    
    async def collect_stj_jurisprudence(self, search_terms: List[str]) -> List[Dict]:
        """Coleta jurisprudência do STJ"""
        
        logger.info("⚖️ Iniciando coleta de jurisprudência STJ...")
        
        jurisprudence_data = []
        
        # URLs base do STJ
        stj_search_base = "https://scon.stj.jus.br/SCON/pesquisar.jsp"
        
        for term in search_terms:
            try:
                logger.info(f"🔍 Buscando jurisprudência para: {term}")
                
                # Construir URL de busca do STJ
                search_url = f"{stj_search_base}?pesq={term.replace(' ', '+')}&tipo_visualizacao=RESUMO"
                
                html_content = await self._fetch_with_rate_limit(search_url)
                
                if html_content:
                    precedents = self._parse_stj_results(html_content, term)
                    jurisprudence_data.extend(precedents)
                    
                    logger.info(f"✅ Encontrados {len(precedents)} precedentes para '{term}'")
                
            except Exception as e:
                logger.error(f"❌ Erro ao buscar jurisprudência para '{term}': {str(e)}")
                continue
        
        logger.info(f"📋 Total de jurisprudência coletada: {len(jurisprudence_data)}")
        return jurisprudence_data
    
    def _parse_stj_results(self, html_content: str, search_term: str) -> List[Dict]:
        """Parse dos resultados de busca do STJ"""
        
        soup = BeautifulSoup(html_content, 'html.parser')
        precedents = []
        
        # Procurar por elementos típicos de resultado do STJ
        result_selectors = [
            'div.acordao',
            'div.resultado',
            'tr.resultado',
            'div.jurisprudencia'
        ]
        
        results_found = False
        
        for selector in result_selectors:
            results = soup.select(selector)
            if results:
                results_found = True
                
                for result in results[:5]:  # Limitar a 5 resultados por termo
                    try:
                        # Extrair dados do precedente
                        precedent_data = self._extract_precedent_data(result, search_term)
                        if precedent_data:
                            precedents.append(precedent_data)
                    
                    except Exception as e:
                        logger.warning(f"⚠️  Erro ao processar resultado: {str(e)}")
                        continue
                
                break
        
        if not results_found:
            logger.warning(f"⚠️  Nenhum resultado estruturado encontrado para '{search_term}'")
            
            # Fallback: criar entrada baseada no termo de busca
            fallback_precedent = {
                "title": f"Precedente STJ sobre {search_term}",
                "content": f"Jurisprudência do Superior Tribunal de Justiça relacionada a {search_term}. Consultar diretamente no portal do STJ para casos específicos.",
                "document_type": "jurisprudencia",
                "category": self._categorize_search_term(search_term),
                "source": "STJ",
                "source_url": f"https://scon.stj.jus.br/SCON/",
                "reference_number": f"STJ-{search_term.replace(' ', '-')}",
                "authority_level": "high",
                "legal_area": ["jurisprudencia"],
                "keywords": search_term.split(),
                "search_term": search_term,
                "collection_date": datetime.now().isoformat()
            }
            precedents.append(fallback_precedent)
        
        return precedents
    
    def _extract_precedent_data(self, result_element, search_term: str) -> Optional[Dict]:
        """Extrai dados de um precedente específico"""
        
        try:
            # Procurar por título/ementa
            title_selectors = ['h3', 'h4', '.titulo', '.ementa', 'strong']
            title = "Precedente STJ"
            
            for selector in title_selectors:
                title_element = result_element.select_one(selector)
                if title_element:
                    title = title_element.get_text(strip=True)[:100]
                    break
            
            # Procurar por conteúdo/ementa
            content = result_element.get_text(strip=True)
            
            # Procurar por número do processo
            process_pattern = r"(\\d{7}-\\d{2}\\.\\d{4}\\.\\d\\.\\d{2}\\.\\d{4})"
            process_match = re.search(process_pattern, content)
            process_number = process_match.group(1) if process_match else None
            
            return {
                "title": title,
                "content": content[:2000],  # Limitar tamanho
                "document_type": "jurisprudencia",
                "category": self._categorize_search_term(search_term),
                "source": "STJ",
                "source_url": "https://scon.stj.jus.br/SCON/",
                "reference_number": process_number or f"STJ-{search_term.replace(' ', '-')}",
                "authority_level": "high",
                "legal_area": ["jurisprudencia"],
                "keywords": search_term.split() + ["STJ", "precedente"],
                "search_term": search_term,
                "collection_date": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.warning(f"⚠️  Erro ao extrair dados do precedente: {str(e)}")
            return None
    
    def _categorize_search_term(self, search_term: str) -> str:
        """Categoriza termo de busca"""
        
        categories_map = {
            "locação": ["locação", "aluguel", "inquilino", "locador"],
            "telecom": ["telecomunicações", "telefone", "internet", "ANATEL"],
            "financeiro": ["financiamento", "banco", "juros", "crédito"],
        }
        
        term_lower = search_term.lower()
        
        for category, keywords in categories_map.items():
            if any(keyword in term_lower for keyword in keywords):
                return category
        
        return "geral"
    
    async def save_collected_data(self, data: List[Dict], filename: str = None) -> str:
        """Salva dados coletados em arquivo JSON"""
        
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"legal_data_{timestamp}.json"
        
        filepath = f"collected_data/{filename}"
        
        # Criar diretório se não existir
        import os
        os.makedirs("collected_data", exist_ok=True)
        
        # Salvar dados
        async with aiofiles.open(filepath, 'w', encoding='utf-8') as f:
            await f.write(json.dumps(data, indent=2, ensure_ascii=False))
        
        logger.info(f"💾 Dados salvos em: {filepath}")
        logger.info(f"📊 Total de documentos: {len(data)}")
        
        return filepath

# Função principal para executar coleta
async def run_legal_data_collection():
    """Executa coleta completa de dados jurídicos"""
    
    logger.info("🚀 Iniciando coleta de dados jurídicos brasileiros...")
    
    async with LegalDataCollector() as collector:
        
        all_collected_data = []
        
        # 1. Coletar leis do Planalto
        logger.info("\\n" + "="*50)
        logger.info("📚 COLETANDO LEIS FEDERAIS")
        logger.info("="*50)
        
        laws_data = await collector.collect_planalto_laws()
        all_collected_data.extend(laws_data)
        
        # 2. Coletar jurisprudência STJ
        logger.info("\\n" + "="*50)
        logger.info("⚖️ COLETANDO JURISPRUDÊNCIA STJ")
        logger.info("="*50)
        
        search_terms = [
            "cláusula abusiva contrato",
            "locação inquilino multa",
            "telecomunicações cancelamento serviço",
            "financiamento taxa juros abusiva",
            "consumidor fornecedor direitos"
        ]
        
        jurisprudence_data = await collector.collect_stj_jurisprudence(search_terms)
        all_collected_data.extend(jurisprudence_data)
        
        # 3. Salvar dados coletados
        logger.info("\\n" + "="*50)
        logger.info("💾 SALVANDO DADOS COLETADOS")
        logger.info("="*50)
        
        saved_file = await collector.save_collected_data(all_collected_data)
        
        # 4. Estatísticas finais
        logger.info("\\n" + "="*50)
        logger.info("📊 ESTATÍSTICAS FINAIS")
        logger.info("="*50)
        
        stats = {
            "total_documentos": len(all_collected_data),
            "leis_coletadas": len([d for d in all_collected_data if d["document_type"] == "lei"]),
            "jurisprudencia_coletada": len([d for d in all_collected_data if d["document_type"] == "jurisprudencia"]),
            "categorias": {}
        }
        
        for doc in all_collected_data:
            category = doc.get("category", "geral")
            stats["categorias"][category] = stats["categorias"].get(category, 0) + 1
        
        logger.info(f"📋 Total de documentos coletados: {stats['total_documentos']}")
        logger.info(f"📜 Leis federais: {stats['leis_coletadas']}")
        logger.info(f"⚖️ Precedentes jurisprudenciais: {stats['jurisprudencia_coletada']}")
        logger.info(f"📁 Categorias: {stats['categorias']}")
        logger.info(f"💾 Arquivo salvo: {saved_file}")
        
        logger.info("\\n🎉 Coleta de dados jurídicos concluída com sucesso!")
        
        return all_collected_data, saved_file

if __name__ == "__main__":
    collected_data, file_path = asyncio.run(run_legal_data_collection())