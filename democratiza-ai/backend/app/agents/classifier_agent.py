from typing import Any, Dict

class ClassifierAgent:
    def __init__(self):
        self.contract_types = {
            "rental": self.is_rental_contract,
            "telecom": self.is_telecom_contract,
            "financial": self.is_financial_contract,
        }

    def classify(self, contract_text: str) -> str:
        for contract_type, check_function in self.contract_types.items():
            if check_function(contract_text):
                return contract_type
        return "unknown"

    def is_rental_contract(self, contract_text: str) -> bool:
        # Logic to identify rental contracts
        return "locação" in contract_text.lower()

    def is_telecom_contract(self, contract_text: str) -> bool:
        # Logic to identify telecommunications contracts
        return "telecomunicações" in contract_text.lower()

    def is_financial_contract(self, contract_text: str) -> bool:
        # Logic to identify financial contracts
        return "financeiro" in contract_text.lower() or "banco" in contract_text.lower()