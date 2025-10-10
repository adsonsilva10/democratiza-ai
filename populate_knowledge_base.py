"""
Script simplificado para popular a base de conhecimento
Usa dados sintéticos essenciais para começar
"""
import asyncio
import os
import sys
from datetime import datetime
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent / "backend"))
sys.path.insert(0, str(Path(__file__).parent))

from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# Carregar .env
load_dotenv()

# Dados essenciais da legislação brasileira
ESSENTIAL_KNOWLEDGE = [
    # CDC - Código de Defesa do Consumidor
    {
        "source": "Lei 8.078/1990 (CDC)",
        "category": "consumer_protection",
        "article": "Art. 6º, III",
        "content": "São direitos básicos do consumidor: III - a informação adequada e clara sobre os diferentes produtos e serviços, com especificação correta de quantidade, características, composição, qualidade, tributos incidentes e preço, bem como sobre os riscos que apresentem."
    },
    {
        "source": "Lei 8.078/1990 (CDC)",
        "category": "consumer_protection",
        "article": "Art. 39, V",
        "content": "É vedado ao fornecedor de produtos ou serviços: V - exigir do consumidor vantagem manifestamente excessiva."
    },
    {
        "source": "Lei 8.078/1990 (CDC)",
        "category": "consumer_protection",
        "article": "Art. 51, IV",
        "content": "São nulas de pleno direito, entre outras, as cláusulas contratuais relativas ao fornecimento de produtos e serviços que: IV - estabeleçam obrigações consideradas iníquas, abusivas, que coloquem o consumidor em desvantagem exagerada, ou sejam incompatíveis com a boa-fé ou a equidade."
    },
    
    # Lei do Inquilinato
    {
        "source": "Lei 8.245/1991 (Lei do Inquilinato)",
        "category": "rental_law",
        "article": "Art. 22",
        "content": "O locador é obrigado a: I - entregar ao locatário o imóvel alugado em estado de servir ao uso a que se destina; II - garantir, durante o tempo da locação, o uso pacífico do imóvel locado."
    },
    {
        "source": "Lei 8.245/1991 (Lei do Inquilinato)",
        "category": "rental_law",
        "article": "Art. 23",
        "content": "O locatário é obrigado a: I - pagar pontualmente o aluguel e os encargos da locação, legal ou contratualmente exigíveis, no prazo estipulado ou, em sua falta, até o sexto dia útil do mês vincendo."
    },
    
    # Código Civil - Contratos
    {
        "source": "Lei 10.406/2002 (Código Civil)",
        "category": "civil_contracts",
        "article": "Art. 421",
        "content": "A liberdade contratual será exercida nos limites da função social do contrato."
    },
    {
        "source": "Lei 10.406/2002 (Código Civil)",
        "category": "civil_contracts",
        "article": "Art. 422",
        "content": "Os contratantes são obrigados a guardar, assim na conclusão do contrato, como em sua execução, os princípios de probidade e boa-fé."
    },
    {
        "source": "Lei 10.406/2002 (Código Civil)",
        "category": "civil_contracts",
        "article": "Art. 423",
        "content": "Quando houver no contrato de adesão cláusulas ambíguas ou contraditórias, dever-se-á adotar a interpretação mais favorável ao aderente."
    },
    
    # Marco Civil da Internet
    {
        "source": "Lei 12.965/2014 (Marco Civil da Internet)",
        "category": "telecommunications",
        "article": "Art. 7º, VIII",
        "content": "O acesso à internet é essencial ao exercício da cidadania, e ao usuário são asseguradas as seguintes garantias: VIII - informações claras e completas sobre coleta, uso, armazenamento, tratamento e proteção de seus dados pessoais, que somente poderão ser utilizados para finalidades que justifiquem sua coleta e não sejam vedadas pela legislação."
    },
    
    # LGPD
    {
        "source": "Lei 13.709/2018 (LGPD)",
        "category": "data_protection",
        "article": "Art. 6º, I",
        "content": "As atividades de tratamento de dados pessoais deverão observar a boa-fé e os seguintes princípios: I - finalidade: realização do tratamento para propósitos legítimos, específicos, explícitos e informados ao titular."
    },
    
    # Direito Previdenciário - Lei de Benefícios da Previdência Social
    {
        "source": "Lei 8.213/1991 (Plano de Benefícios da Previdência Social)",
        "category": "retirement_pension",
        "article": "Art. 18, I",
        "content": "O Regime Geral de Previdência Social compreende as seguintes prestações, devidas inclusive em razão de eventos decorrentes de acidente do trabalho, expressas em benefícios e serviços: I - quanto ao segurado: a) aposentadoria por invalidez; b) aposentadoria por idade; c) aposentadoria por tempo de contribuição; d) aposentadoria especial; e) auxílio-doença; f) salário-família; g) salário-maternidade; h) auxílio-acidente."
    },
    {
        "source": "Lei 8.213/1991 (Plano de Benefícios da Previdência Social)",
        "category": "retirement_pension",
        "article": "Art. 48",
        "content": "A aposentadoria por idade será devida ao segurado que, cumprida a carência exigida, completar 65 (sessenta e cinco) anos de idade, se homem, e 62 (sessenta e dois) anos, se mulher. § 1º Os limites fixados no caput são reduzidos para sessenta e cinquenta e cinco anos no caso de trabalhadores rurais."
    },
    {
        "source": "Lei 8.213/1991 (Plano de Benefícios da Previdência Social)",
        "category": "retirement_pension",
        "article": "Art. 74",
        "content": "A pensão por morte será devida ao conjunto dos dependentes do segurado que falecer, aposentado ou não, a contar da data: I - do óbito, quando requerida até 90 (noventa) dias depois deste; II - do requerimento, quando requerida após o prazo previsto no inciso anterior."
    },
    {
        "source": "Lei 8.213/1991 (Plano de Benefícios da Previdência Social)",
        "category": "retirement_pension",
        "article": "Art. 77",
        "content": "A pensão por morte concedida a dependente inválido ou com deficiência terá duração indeterminada. A pensão por morte havida por outros dependentes terá os seguintes prazos de duração: I - 4 (quatro) meses se o óbito ocorrer sem que o segurado tenha vertido 18 (dezoito) contribuições mensais; II - duração variável conforme idade do beneficiário."
    },
    {
        "source": "Emenda Constitucional 103/2019 (Reforma da Previdência)",
        "category": "retirement_pension",
        "article": "Art. 201, §7º, I",
        "content": "É assegurada aposentadoria no regime geral de previdência social, nos termos da lei, obedecidas as seguintes condições: I - 65 (sessenta e cinco) anos de idade, se homem, e 62 (sessenta e dois) anos de idade, se mulher, observado tempo mínimo de contribuição."
    },
    {
        "source": "Lei 8.213/1991 (Plano de Benefícios da Previdência Social)",
        "category": "retirement_pension",
        "article": "Art. 57",
        "content": "A aposentadoria especial será devida, uma vez cumprida a carência exigida, ao segurado empregado, trabalhador avulso e contribuinte individual, este somente quando cooperado filiado a cooperativa de trabalho ou de produção, que tenha trabalhado sujeito a condições especiais que prejudiquem a saúde ou a integridade física, durante 15 (quinze), 20 (vinte) ou 25 (vinte e cinco) anos."
    },
    {
        "source": "Lei 8.213/1991 (Plano de Benefícios da Previdência Social)",
        "category": "retirement_pension",
        "article": "Art. 29, §5º",
        "content": "Não será computado como tempo de contribuição, para efeito de concessão do benefício de que trata esta subseção, o período em que o segurado contribuinte individual ou facultativo tiver contribuído na forma do § 2º do art. 21 da Lei nº 8.212, de 24 de julho de 1991, salvo se tiver complementado as contribuições na forma do § 3º do mesmo artigo."
    }
]

def populate_knowledge_base():
    """Popula a base de conhecimento com dados essenciais"""
    
    print("\n" + "="*60)
    print("📚 POPULAÇÃO DA BASE DE CONHECIMENTO JURÍDICO")
    print("="*60)
    
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        print("❌ DATABASE_URL não configurado!")
        return False
    
    try:
        engine = create_engine(database_url)
        Session = sessionmaker(bind=engine)
        session = Session()
        
        print(f"\n📊 Inserindo {len(ESSENTIAL_KNOWLEDGE)} documentos essenciais...")
        print(f"   📚 Categorias: consumer_protection, rental_law, civil_contracts,")
        print(f"                  telecommunications, data_protection, retirement_pension")
        
        inserted = 0
        for doc in ESSENTIAL_KNOWLEDGE:
            try:
                import json
                
                # Criar metadata com source, category e article
                metadata = {
                    "source": doc["source"],
                    "category": doc["category"],
                    "article": doc["article"]
                }
                
                # Inserir documento (schema correto: content + metadata)
                result = session.execute(text("""
                    INSERT INTO knowledge_base 
                    (content, metadata, created_at)
                    VALUES 
                    (:content, :metadata, :created_at)
                    RETURNING id
                """), {
                    "content": doc["content"],
                    "metadata": json.dumps(metadata),
                    "created_at": datetime.now()
                })
                
                doc_id = result.scalar()
                print(f"   ✅ {doc_id} - {doc['source']} - {doc['article']}")
                inserted += 1
                
            except Exception as e:
                print(f"   ❌ Erro ao inserir {doc['article']}: {e}")
        
        session.commit()
        session.close()
        
        print(f"\n✅ {inserted}/{len(ESSENTIAL_KNOWLEDGE)} documentos inseridos com sucesso!")
        
        # Verificar total
        with engine.connect() as conn:
            result = conn.execute(text("SELECT COUNT(*) FROM knowledge_base"))
            total = result.scalar()
            print(f"📊 Total na base: {total} documentos")
        
        print("\n⚠️  NOTA: Embeddings serão gerados ao testar o RAG Service")
        print("   Execute: python test_openai_embeddings.py")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Erro ao popular base: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    print("\n" + "🚀"*30)
    print("DEMOCRATIZA AI - BOOTSTRAP DA BASE JURÍDICA")
    print("🚀"*30)
    
    success = populate_knowledge_base()
    
    print("\n" + "="*60)
    if success:
        print("✅ POPULAÇÃO CONCLUÍDA!")
        print("\n📋 Próximos passos:")
        print("  1. python check_knowledge_base.py  # Verificar")
        print("  2. cd backend")
        print("  3. python test_openai_embeddings.py  # Gerar embeddings")
    else:
        print("❌ FALHA NA POPULAÇÃO")
    print("="*60)
    print()
