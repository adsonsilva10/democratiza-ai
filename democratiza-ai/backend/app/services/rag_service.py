from typing import Any, Dict, List
from sqlalchemy.orm import Session
from app.models.database import Contract
from app.agents.classifier_agent import ClassifierAgent
from app.agents.factory import AgentFactory

class RAGService:
    def __init__(self, db: Session):
        self.db = db
        self.classifier_agent = ClassifierAgent()
        self.agent_factory = AgentFactory()

    def index_contract(self, contract_data: Dict[str, Any]) -> Contract:
        contract = Contract(**contract_data)
        self.db.add(contract)
        self.db.commit()
        self.db.refresh(contract)
        return contract

    def retrieve_contract(self, contract_id: int) -> Contract:
        return self.db.query(Contract).filter(Contract.id == contract_id).first()

    def analyze_contract(self, contract_text: str) -> Dict[str, Any]:
        contract_type = self.classifier_agent.classify(contract_text)
        agent = self.agent_factory.create_agent(contract_type)
        analysis_result = agent.analyze(contract_text)
        return analysis_result

    def get_all_contracts(self) -> List[Contract]:
        return self.db.query(Contract).all()