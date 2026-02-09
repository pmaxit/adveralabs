"""Base agent implementation using Pydantic AI."""
from typing import TypeVar, Generic, Dict, Any, Optional
from datetime import datetime
from pydantic import BaseModel
from pydantic_ai import Agent
import logging

from backend.services.llm_service import llm_service

logger = logging.getLogger(__name__)

TRequest = TypeVar('TRequest', bound=BaseModel)
TResponse = TypeVar('TResponse', bound=BaseModel)


class AgentError(BaseException):
    """Base exception for agent errors."""
    pass


class BaseAgent(Generic[TRequest, TResponse]):
    """Base agent class for all marketing agents."""
    
    def __init__(
        self,
        agent_type: str,
        system_prompt: str,
        request_type: type[TRequest],
        response_type: type[TResponse]
    ):
        """Initialize base agent."""
        self.agent_type = agent_type
        self.system_prompt = system_prompt
        self.request_type = request_type
        self.response_type = response_type
        self._agent: Optional[Agent] = None
        self._initialized = False
    
    def initialize(self):
        """Initialize the agent."""
        if not self._initialized:
            self._agent = llm_service.create_agent(
                system_prompt=self.system_prompt,
                result_type=self.response_type
            )
            self._initialized = True
            logger.info(f"Initialized {self.agent_type} agent")
    
    async def execute(
        self,
        request: TRequest,
        **kwargs
    ) -> TResponse:
        """Execute the agent with a request."""
        if not self._initialized:
            self.initialize()
        
        try:
            start_time = datetime.now()
            logger.info(f"Executing {self.agent_type} agent with request: {request}")
            
            # Validate request
            if not isinstance(request, self.request_type):
                request = self.request_type(**request) if isinstance(request, dict) else request
            
            # Run agent
            result = await self._agent.run(request, **kwargs)
            
            # Calculate execution time
            execution_time = (datetime.now() - start_time).total_seconds() * 1000
            
            logger.info(
                f"{self.agent_type} agent completed in {execution_time:.2f}ms"
            )
            
            return result.data
            
        except Exception as e:
            logger.error(f"Error executing {self.agent_type} agent: {str(e)}")
            raise AgentError(f"{self.agent_type} agent failed: {str(e)}") from e
    
    async def cleanup(self):
        """Cleanup agent resources."""
        self._agent = None
        self._initialized = False
        logger.info(f"Cleaned up {self.agent_type} agent")
    
    def get_status(self) -> Dict[str, Any]:
        """Get agent status."""
        return {
            "agent_type": self.agent_type,
            "initialized": self._initialized,
            "request_type": self.request_type.__name__,
            "response_type": self.response_type.__name__
        }


class AgentResponse(BaseModel):
    """Base response model for agents."""
    success: bool = True
    message: Optional[str] = None
    data: Optional[Dict[str, Any]] = None
    execution_time_ms: Optional[float] = None


class AgentRequest(BaseModel):
    """Base request model for agents."""
    pass
