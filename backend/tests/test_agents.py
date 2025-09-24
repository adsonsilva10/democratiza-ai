import pytest
from unittest.mock import AsyncMock, MagicMock
from app.agents.base_agent import BaseContractAgent, ContractAnalysis
from app.agents.classifier_agent import ClassifierAgent
from app.agents.rental_agent import RentalAgent
from app.agents.telecom_agent import TelecomAgent
from app.agents.financial_agent import FinancialAgent

class TestBaseContractAgent:
    """Test base contract agent functionality."""
    
    def test_contract_analysis_model(self):
        """Test ContractAnalysis model validation."""
        analysis = ContractAnalysis(
            contract_type="locacao",
            risk_level="medium",
            summary="Test summary",
            key_findings=["Finding 1", "Finding 2"],
            risk_factors=[
                {
                    "type": "test_risk",
                    "severity": "high",
                    "description": "Test risk description"
                }
            ],
            recommendations=["Recommendation 1"],
            clauses_analysis=[
                {
                    "clause_type": "pagamento",
                    "content": "Test clause",
                    "risk_level": "low"
                }
            ],
            confidence_score=0.85
        )
        
        assert analysis.contract_type == "locacao"
        assert analysis.risk_level == "medium"
        assert len(analysis.key_findings) == 2
        assert analysis.confidence_score == 0.85

@pytest.mark.agents
class TestClassifierAgent:
    """Test contract classification agent."""
    
    @pytest.fixture
    def classifier_agent(self, mock_claude_client, mock_rag_service):
        """Create classifier agent instance."""
        return ClassifierAgent(mock_claude_client, mock_rag_service)
    
    @pytest.mark.asyncio
    async def test_classify_rental_contract(self, classifier_agent, sample_contract_text):
        """Test classification of rental contract."""
        result = await classifier_agent.classify_contract(sample_contract_text)
        
        assert "contract_type" in result
        assert "confidence" in result
        assert result["contract_type"] in ["locacao", "telecom", "financeiro"]
        assert 0.0 <= result["confidence"] <= 1.0
    
    @pytest.mark.asyncio
    async def test_classify_telecom_contract(self, classifier_agent):
        """Test classification of telecom contract."""
        telecom_text = """
        CONTRATO DE PRESTAÇÃO DE SERVIÇOS DE TELECOMUNICAÇÕES
        
        CONTRATANTE: João Silva
        CONTRATADA: TelecomCorp Ltda
        
        CLÁUSULA 1ª - DO OBJETO
        Prestação de serviços de internet banda larga
        
        CLÁUSULA 2ª - DA VELOCIDADE
        Velocidade contratada: 100 Mbps
        
        CLÁUSULA 3ª - DA FIDELIDADE
        Prazo de fidelidade de 12 meses
        """
        
        result = await classifier_agent.classify_contract(telecom_text)
        
        # Should classify as telecom with reasonable confidence
        assert result["contract_type"] == "telecom"
        assert result["confidence"] > 0.7

    @pytest.mark.asyncio
    async def test_classify_financial_contract(self, classifier_agent):
        """Test classification of financial contract."""
        financial_text = """
        CONTRATO DE EMPRÉSTIMO PESSOAL
        
        CREDOR: Banco XYZ S.A.
        DEVEDOR: Maria Santos
        
        CLÁUSULA 1ª - DO EMPRÉSTIMO
        Valor emprestado: R$ 10.000,00
        
        CLÁUSULA 2ª - DOS JUROS
        Taxa de juros: 2,5% ao mês
        
        CLÁUSULA 3ª - DO PAGAMENTO
        Pagamento em 24 parcelas mensais
        """
        
        result = await classifier_agent.classify_contract(financial_text)
        
        assert result["contract_type"] == "financeiro"
        assert result["confidence"] > 0.7

@pytest.mark.agents
class TestRentalAgent:
    """Test rental contract agent."""
    
    @pytest.fixture
    def rental_agent(self, mock_claude_client, mock_rag_service):
        """Create rental agent instance."""
        return RentalAgent(mock_claude_client, mock_rag_service)
    
    @pytest.mark.asyncio
    async def test_analyze_rental_contract(self, rental_agent, sample_contract_text):
        """Test rental contract analysis."""
        result = await rental_agent.analyze_contract(sample_contract_text)
        
        assert isinstance(result, ContractAnalysis)
        assert result.contract_type == "locacao"
        assert result.risk_level in ["baixo", "medio", "alto"]
        assert len(result.summary) > 0
        assert len(result.key_findings) > 0
        assert len(result.recommendations) > 0
    
    @pytest.mark.asyncio
    async def test_detect_abusive_clauses(self, rental_agent):
        """Test detection of abusive clauses in rental contracts."""
        abusive_contract = """
        CONTRATO DE LOCAÇÃO
        
        CLÁUSULA 1ª - DO FORO
        Fica eleito o foro da Comarca de Recife, PE, mesmo que o locatário resida em São Paulo.
        
        CLÁUSULA 2ª - DA MULTA
        Em caso de atraso, multa de 20% sobre o valor do aluguel.
        
        CLÁUSULA 3ª - DA RENOVAÇÃO
        Este contrato será renovado automaticamente por prazo indeterminado.
        """
        
        result = await rental_agent.analyze_contract(abusive_contract)
        
        # Should detect high risk due to abusive clauses
        assert result.risk_level == "alto"
        assert len(result.risk_factors) > 0
        
        # Check if specific risks are detected
        risk_types = [rf.get("type", "") for rf in result.risk_factors]
        assert any("foro" in rt for rt in risk_types)
        assert any("multa" in rt for rt in risk_types)

@pytest.mark.agents  
class TestTelecomAgent:
    """Test telecom contract agent."""
    
    @pytest.fixture
    def telecom_agent(self, mock_claude_client, mock_rag_service):
        """Create telecom agent instance."""
        return TelecomAgent(mock_claude_client, mock_rag_service)
    
    @pytest.mark.asyncio
    async def test_analyze_telecom_contract(self, telecom_agent):
        """Test telecom contract analysis."""
        telecom_text = """
        CONTRATO DE INTERNET BANDA LARGA
        
        Velocidade: 100 Mbps
        Valor: R$ 89,90/mês
        Fidelidade: 12 meses
        Multa por cancelamento: R$ 200,00
        """
        
        result = await telecom_agent.analyze_contract(telecom_text)
        
        assert isinstance(result, ContractAnalysis)
        assert result.contract_type == "telecom"
        assert len(result.key_findings) > 0
        assert any("velocidade" in finding.lower() or "mbps" in finding.lower() 
                  for finding in result.key_findings)

@pytest.mark.agents
class TestFinancialAgent:
    """Test financial contract agent."""
    
    @pytest.fixture  
    def financial_agent(self, mock_claude_client, mock_rag_service):
        """Create financial agent instance."""
        return FinancialAgent(mock_claude_client, mock_rag_service)
    
    @pytest.mark.asyncio
    async def test_analyze_financial_contract(self, financial_agent):
        """Test financial contract analysis."""
        financial_text = """
        CONTRATO DE EMPRÉSTIMO
        
        Valor: R$ 50.000,00
        Taxa: 3,5% ao mês
        Prazo: 36 meses
        CET: 65,8% ao ano
        """
        
        result = await financial_agent.analyze_contract(financial_text)
        
        assert isinstance(result, ContractAnalysis)
        assert result.contract_type == "financeiro"
        
        # Should detect high risk due to high interest rate
        assert result.risk_level in ["medio", "alto"]
        assert any("taxa" in finding.lower() or "juros" in finding.lower()
                  for finding in result.key_findings)

@pytest.mark.integration
class TestAgentIntegration:
    """Test agent integration scenarios."""
    
    @pytest.mark.asyncio
    async def test_agent_with_rag_context(self, mock_claude_client, mock_rag_service):
        """Test agent using RAG context."""
        agent = RentalAgent(mock_claude_client, mock_rag_service)
        
        # Mock RAG service to return relevant context
        mock_rag_service.get_relevant_context = AsyncMock(
            return_value="Jurisprudência: Cláusulas de foro são consideradas abusivas quando..."
        )
        
        contract_text = "Contrato com cláusula de foro em cidade distante..."
        result = await agent.analyze_contract(contract_text)
        
        # Verify RAG service was called
        mock_rag_service.get_relevant_context.assert_called_once()
        assert isinstance(result, ContractAnalysis)
    
    @pytest.mark.asyncio
    async def test_error_handling(self, mock_rag_service):
        """Test agent error handling."""
        # Create agent with broken Claude client
        broken_client = MagicMock()
        broken_client.messages_create = AsyncMock(side_effect=Exception("API Error"))
        
        agent = RentalAgent(broken_client, mock_rag_service)
        
        # Should handle errors gracefully
        with pytest.raises(Exception):
            await agent.analyze_contract("test contract")

@pytest.mark.slow
class TestAgentPerformance:
    """Test agent performance characteristics."""
    
    @pytest.mark.asyncio
    async def test_analysis_speed(self, mock_claude_client, mock_rag_service):
        """Test that analysis completes within reasonable time."""
        import time
        
        agent = RentalAgent(mock_claude_client, mock_rag_service)
        
        start_time = time.time()
        result = await agent.analyze_contract("Small test contract")
        end_time = time.time()
        
        # Should complete within 5 seconds (generous for mock)
        assert (end_time - start_time) < 5.0
        assert isinstance(result, ContractAnalysis)
    
    @pytest.mark.asyncio
    async def test_concurrent_analysis(self, mock_claude_client, mock_rag_service):
        """Test concurrent contract analysis."""
        import asyncio
        
        agent = RentalAgent(mock_claude_client, mock_rag_service)
        
        # Analyze multiple contracts concurrently
        tasks = [
            agent.analyze_contract(f"Contract {i}")
            for i in range(5)
        ]
        
        results = await asyncio.gather(*tasks)
        
        assert len(results) == 5
        assert all(isinstance(r, ContractAnalysis) for r in results)