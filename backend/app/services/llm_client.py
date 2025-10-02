"""
Democratiza AI - Cliente Unificado de LLMs
Implementa interfaces para todos os provedores de LLM
"""

import asyncio
import aiohttp
import json
from typing import Dict, Any, Optional, List, AsyncGenerator
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
import os
from datetime import datetime

from .llm_router import LLMProvider, LLMConfig

@dataclass
class LLMResponse:
    """Resposta padronizada de qualquer LLM"""
    content: str
    model: str
    provider: LLMProvider
    tokens_used: Dict[str, int]  # input, output, total
    cost_usd: float
    response_time_ms: int
    metadata: Dict[str, Any]

@dataclass
class LLMRequest:
    """Requisição padronizada para qualquer LLM"""
    messages: List[Dict[str, str]]  # [{"role": "user", "content": "..."}]
    system_prompt: Optional[str] = None
    max_tokens: int = 4000
    temperature: float = 0.7
    stream: bool = False
    contract_context: Optional[Dict[str, Any]] = None

class BaseLLMClient(ABC):
    """Classe base para clientes LLM"""
    
    def __init__(self, config: LLMConfig, api_key: str):
        self.config = config
        self.api_key = api_key
        self.usage_stats = {
            'total_requests': 0,
            'total_tokens': 0,
            'total_cost': 0.0,
            'average_response_time': 0.0
        }
    
    @abstractmethod
    async def generate_response(self, request: LLMRequest) -> LLMResponse:
        """Gera resposta do LLM"""
        pass
    
    @abstractmethod
    async def stream_response(self, request: LLMRequest) -> AsyncGenerator[str, None]:
        """Gera resposta em streaming"""
        pass
    
    def _calculate_cost(self, input_tokens: int, output_tokens: int) -> float:
        """Calcula custo baseado nos tokens utilizados"""
        total_tokens = input_tokens + output_tokens
        return (total_tokens / 1000) * self.config.cost_per_1k_tokens
    
    def _update_stats(self, tokens_used: int, cost: float, response_time: int):
        """Atualiza estatísticas de uso"""
        self.usage_stats['total_requests'] += 1
        self.usage_stats['total_tokens'] += tokens_used
        self.usage_stats['total_cost'] += cost
        
        # Média ponderada do tempo de resposta
        current_avg = self.usage_stats['average_response_time']
        total_requests = self.usage_stats['total_requests']
        self.usage_stats['average_response_time'] = (
            (current_avg * (total_requests - 1) + response_time) / total_requests
        )

class GroqLlamaClient(BaseLLMClient):
    """Cliente para Groq Llama (modelo econômico)"""
    
    def __init__(self, config: LLMConfig, api_key: str):
        super().__init__(config, api_key)
        self.base_url = "https://api.groq.com/openai/v1"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
    
    async def generate_response(self, request: LLMRequest) -> LLMResponse:
        """Gera resposta usando Groq Llama"""
        start_time = datetime.now()
        
        # Preparar mensagens
        messages = []
        if request.system_prompt:
            messages.append({"role": "system", "content": request.system_prompt})
        messages.extend(request.messages)
        
        payload = {
            "model": self.config.model_name,
            "messages": messages,
            "max_tokens": request.max_tokens,
            "temperature": request.temperature,
            "stream": False
        }
        
        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(
                    f"{self.base_url}/chat/completions",
                    headers=self.headers,
                    json=payload,
                    timeout=aiohttp.ClientTimeout(total=60)
                ) as response:
                    
                    if response.status != 200:
                        error_text = await response.text()
                        raise Exception(f"Groq API Error {response.status}: {error_text}")
                    
                    result = await response.json()
                    
                    response_time = int((datetime.now() - start_time).total_seconds() * 1000)
                    
                    # Extrair dados da resposta
                    content = result['choices'][0]['message']['content']
                    usage = result.get('usage', {})
                    
                    input_tokens = usage.get('prompt_tokens', 0)
                    output_tokens = usage.get('completion_tokens', 0)
                    total_tokens = usage.get('total_tokens', input_tokens + output_tokens)
                    
                    cost = self._calculate_cost(input_tokens, output_tokens)
                    
                    # Atualizar estatísticas
                    self._update_stats(total_tokens, cost, response_time)
                    
                    return LLMResponse(
                        content=content,
                        model=self.config.model_name,
                        provider=LLMProvider.GROQ_LLAMA,
                        tokens_used={
                            'input': input_tokens,
                            'output': output_tokens,
                            'total': total_tokens
                        },
                        cost_usd=cost,
                        response_time_ms=response_time,
                        metadata={
                            'finish_reason': result['choices'][0].get('finish_reason'),
                            'usage': usage
                        }
                    )
            
            except Exception as e:
                raise Exception(f"Erro ao comunicar com Groq: {str(e)}")
    
    async def stream_response(self, request: LLMRequest) -> AsyncGenerator[str, None]:
        """Streaming não implementado para Groq nesta versão"""
        response = await self.generate_response(request)
        yield response.content

class AnthropicClient(BaseLLMClient):
    """Cliente para modelos Anthropic Claude"""
    
    def __init__(self, config: LLMConfig, api_key: str):
        super().__init__(config, api_key)
        self.base_url = "https://api.anthropic.com/v1"
        self.headers = {
            "x-api-key": api_key,
            "Content-Type": "application/json",
            "anthropic-version": "2023-06-01"
        }
    
    async def generate_response(self, request: LLMRequest) -> LLMResponse:
        """Gera resposta usando Anthropic Claude"""
        start_time = datetime.now()
        
        # Preparar mensagens para formato Anthropic
        messages = []
        system_prompt = request.system_prompt or ""
        
        for msg in request.messages:
            messages.append({
                "role": msg["role"],
                "content": msg["content"]
            })
        
        payload = {
            "model": self.config.model_name,
            "max_tokens": request.max_tokens,
            "temperature": request.temperature,
            "messages": messages
        }
        
        if system_prompt:
            payload["system"] = system_prompt
        
        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(
                    f"{self.base_url}/messages",
                    headers=self.headers,
                    json=payload,
                    timeout=aiohttp.ClientTimeout(total=120)
                ) as response:
                    
                    if response.status != 200:
                        error_text = await response.text()
                        raise Exception(f"Anthropic API Error {response.status}: {error_text}")
                    
                    result = await response.json()
                    
                    response_time = int((datetime.now() - start_time).total_seconds() * 1000)
                    
                    # Extrair dados da resposta
                    content = result['content'][0]['text']
                    usage = result.get('usage', {})
                    
                    input_tokens = usage.get('input_tokens', 0)
                    output_tokens = usage.get('output_tokens', 0)
                    total_tokens = input_tokens + output_tokens
                    
                    cost = self._calculate_cost(input_tokens, output_tokens)
                    
                    # Atualizar estatísticas
                    self._update_stats(total_tokens, cost, response_time)
                    
                    return LLMResponse(
                        content=content,
                        model=self.config.model_name,
                        provider=self.config.provider,
                        tokens_used={
                            'input': input_tokens,
                            'output': output_tokens,
                            'total': total_tokens
                        },
                        cost_usd=cost,
                        response_time_ms=response_time,
                        metadata={
                            'stop_reason': result.get('stop_reason'),
                            'stop_sequence': result.get('stop_sequence'),
                            'usage': usage
                        }
                    )
            
            except Exception as e:
                raise Exception(f"Erro ao comunicar com Anthropic: {str(e)}")
    
    async def stream_response(self, request: LLMRequest) -> AsyncGenerator[str, None]:
        """Streaming para Anthropic (implementação futura)"""
        response = await self.generate_response(request)
        yield response.content

class GoogleGeminiClient(BaseLLMClient):
    """Cliente para Google Gemini (modelos econômicos)"""
    
    def __init__(self, config: LLMConfig, api_key: str):
        super().__init__(config, api_key)
        self.base_url = "https://generativelanguage.googleapis.com/v1beta"
        self.headers = {
            "Content-Type": "application/json"
        }
    
    async def generate_response(self, request: LLMRequest) -> LLMResponse:
        """Gera resposta usando Google Gemini"""
        start_time = datetime.now()
        
        # Preparar conteúdo para formato Gemini
        contents = []
        
        # System prompt como primeiro conteúdo
        if request.system_prompt:
            contents.append({
                "parts": [{"text": f"Instructions: {request.system_prompt}"}]
            })
        
        # Adicionar mensagens do usuário
        for msg in request.messages:
            role = "user" if msg["role"] == "user" else "model"
            contents.append({
                "role": role,
                "parts": [{"text": msg["content"]}]
            })
        
        # Configurações de geração
        generation_config = {
            "temperature": request.temperature,
            "maxOutputTokens": request.max_tokens,
            "topP": 0.95,
            "topK": 40
        }
        
        payload = {
            "contents": contents,
            "generationConfig": generation_config
        }
        
        # URL com API key
        url = f"{self.base_url}/models/{self.config.model_name}:generateContent?key={self.api_key}"
        
        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(
                    url,
                    headers=self.headers,
                    json=payload,
                    timeout=aiohttp.ClientTimeout(total=60)
                ) as response:
                    
                    if response.status != 200:
                        error_text = await response.text()
                        raise Exception(f"Gemini API Error {response.status}: {error_text}")
                    
                    result = await response.json()
                    
                    response_time = int((datetime.now() - start_time).total_seconds() * 1000)
                    
                    # Extrair conteúdo da resposta
                    if 'candidates' not in result or not result['candidates']:
                        raise Exception("Resposta vazia do Gemini")
                    
                    content = result['candidates'][0]['content']['parts'][0]['text']
                    
                    # Estimar tokens (Gemini não retorna usage detalhado na API gratuita)
                    input_tokens = sum(len(msg["content"]) for msg in request.messages) // 4
                    if request.system_prompt:
                        input_tokens += len(request.system_prompt) // 4
                    
                    output_tokens = len(content) // 4
                    total_tokens = input_tokens + output_tokens
                    
                    cost = self._calculate_cost(input_tokens, output_tokens)
                    
                    # Atualizar estatísticas
                    self._update_stats(total_tokens, cost, response_time)
                    
                    return LLMResponse(
                        content=content,
                        model=self.config.model_name,
                        provider=self.config.provider,
                        tokens_used={
                            'input': input_tokens,
                            'output': output_tokens,
                            'total': total_tokens
                        },
                        cost_usd=cost,
                        response_time_ms=response_time,
                        metadata={
                            'finish_reason': result['candidates'][0].get('finishReason', 'STOP'),
                            'safety_ratings': result['candidates'][0].get('safetyRatings', [])
                        }
                    )
            
            except Exception as e:
                raise Exception(f"Erro ao comunicar com Gemini: {str(e)}")
    
    async def stream_response(self, request: LLMRequest) -> AsyncGenerator[str, None]:
        """Streaming para Gemini (implementação futura)"""
        response = await self.generate_response(request)
        yield response.content

class LLMClientFactory:
    """Factory para criar clientes LLM apropriados"""
    
    @staticmethod
    def create_client(config: LLMConfig, api_keys: Dict[str, str]) -> BaseLLMClient:
        """Cria cliente apropriado baseado no provedor"""
        
        if config.provider == LLMProvider.GROQ_LLAMA:
            api_key = api_keys.get('GROQ_API_KEY')
            if not api_key:
                raise ValueError("GROQ_API_KEY não encontrada")
            return GroqLlamaClient(config, api_key)
        
        elif config.provider in [LLMProvider.GEMINI_FLASH, LLMProvider.GEMINI_PRO]:
            api_key = api_keys.get('GOOGLE_API_KEY')
            if not api_key:
                raise ValueError("GOOGLE_API_KEY não encontrada")
            return GoogleGeminiClient(config, api_key)
        
        elif config.provider in [
            LLMProvider.ANTHROPIC_HAIKU,
            LLMProvider.ANTHROPIC_SONNET,
            LLMProvider.ANTHROPIC_OPUS
        ]:
            api_key = api_keys.get('ANTHROPIC_API_KEY')
            if not api_key:
                raise ValueError("ANTHROPIC_API_KEY não encontrada")
            return AnthropicClient(config, api_key)
        
        else:
            raise ValueError(f"Provedor não suportado: {config.provider}")

class UnifiedLLMService:
    """Serviço unificado que gerencia todos os clientes LLM"""
    
    def __init__(self):
        self.clients: Dict[LLMProvider, BaseLLMClient] = {}
        self.api_keys = self._load_api_keys()
        self._initialize_clients()
    
    def _load_api_keys(self) -> Dict[str, str]:
        """Carrega chaves de API das variáveis de ambiente"""
        return {
            'ANTHROPIC_API_KEY': os.getenv('ANTHROPIC_API_KEY', ''),
            'GROQ_API_KEY': os.getenv('GROQ_API_KEY', ''),
            'GOOGLE_API_KEY': os.getenv('GOOGLE_API_KEY', '')
        }
    
    def _initialize_clients(self):
        """Inicializa clientes disponíveis baseado nas chaves de API"""
        from .llm_router import LLMRouter
        
        router = LLMRouter()
        
        for provider, config in router.llm_configs.items():
            try:
                client = LLMClientFactory.create_client(config, self.api_keys)
                self.clients[provider] = client
                print(f"✅ Cliente {provider.value} inicializado")
            except ValueError as e:
                print(f"⚠️ Cliente {provider.value} não disponível: {e}")
    
    async def generate_response(
        self, 
        provider: LLMProvider, 
        request: LLMRequest
    ) -> LLMResponse:
        """Gera resposta usando o provedor especificado"""
        
        if provider not in self.clients:
            raise ValueError(f"Cliente {provider.value} não disponível")
        
        client = self.clients[provider]
        return await client.generate_response(request)
    
    async def stream_response(
        self, 
        provider: LLMProvider, 
        request: LLMRequest
    ) -> AsyncGenerator[str, None]:
        """Gera resposta em streaming usando o provedor especificado"""
        
        if provider not in self.clients:
            raise ValueError(f"Cliente {provider.value} não disponível")
        
        client = self.clients[provider]
        async for chunk in client.stream_response(request):
            yield chunk
    
    def get_available_providers(self) -> List[LLMProvider]:
        """Retorna provedores disponíveis"""
        return list(self.clients.keys())
    
    def get_client_stats(self, provider: LLMProvider) -> Dict[str, Any]:
        """Retorna estatísticas de um cliente específico"""
        if provider not in self.clients:
            return {}
        
        return self.clients[provider].usage_stats
    
    def get_all_stats(self) -> Dict[str, Any]:
        """Retorna estatísticas de todos os clientes"""
        stats = {}
        for provider, client in self.clients.items():
            stats[provider.value] = client.usage_stats
        
        return stats

# Instância global do serviço
llm_service = UnifiedLLMService()