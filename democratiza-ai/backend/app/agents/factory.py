from typing import Type

from app.agents.rental_agent import RentalAgent
from app.agents.telecom_agent import TelecomAgent
from app.agents.financial_agent import FinancialAgent
from app.agents.classifier_agent import ClassifierAgent

class AgentFactory:
    @staticmethod
    def create_agent(contract_type: str) -> Type:
        if contract_type == "rental":
            return RentalAgent()
        elif contract_type == "telecom":
            return TelecomAgent()
        elif contract_type == "financial":
            return FinancialAgent()
        else:
            raise ValueError(f"Unknown contract type: {contract_type}")

def get_classifier_agent() -> ClassifierAgent:
    return ClassifierAgent()