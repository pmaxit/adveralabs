"""LLM service for Pydantic AI integration."""
from typing import Optional, Dict, Any
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.models.anthropic import AnthropicModel

from backend.config.settings import settings


class LLMService:
    """Service for managing LLM connections and configurations."""
    
    def __init__(self):
        """Initialize LLM service."""
        self._model = None
        self._token_usage_cache: Dict[str, int] = {}
    
    def get_model(self):
        """Get configured LLM model."""
        if self._model is None:
            if settings.llm_provider == "openai":
                if not settings.openai_api_key:
                    raise ValueError("OPENAI_API_KEY not configured")
                self._model = OpenAIModel(
                    'gpt-4-turbo-preview',
                    api_key=settings.openai_api_key
                )
            elif settings.llm_provider == "anthropic":
                if not settings.anthropic_api_key:
                    raise ValueError("ANTHROPIC_API_KEY not configured")
                self._model = AnthropicModel(
                    'claude-3-opus-20240229',
                    api_key=settings.anthropic_api_key
                )
            else:
                raise ValueError(f"Unsupported LLM provider: {settings.llm_provider}")
        return self._model
    
    def create_agent(
        self,
        system_prompt: str,
        result_type: type,
        model: Optional[Any] = None
    ) -> Agent:
        """Create a Pydantic AI agent."""
        if model is None:
            model = self.get_model()
        
        return Agent(
            model=model,
            system_prompt=system_prompt,
            result_type=result_type
        )
    
    def track_token_usage(self, agent_type: str, tokens: int):
        """Track token usage for an agent."""
        if agent_type not in self._token_usage_cache:
            self._token_usage_cache[agent_type] = 0
        self._token_usage_cache[agent_type] += tokens
    
    def get_token_usage(self, agent_type: Optional[str] = None) -> Dict[str, int]:
        """Get token usage statistics."""
        if agent_type:
            return {agent_type: self._token_usage_cache.get(agent_type, 0)}
        return self._token_usage_cache.copy()


# Global LLM service instance
llm_service = LLMService()
