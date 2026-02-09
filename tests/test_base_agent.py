"""Tests for base agent."""
import pytest
from pydantic import BaseModel

from backend.agents.base_agent import BaseAgent, AgentError


class TestRequest(BaseModel):
    """Test request model."""
    message: str


class TestResponse(BaseModel):
    """Test response model."""
    response: str


@pytest.mark.asyncio
async def test_base_agent_initialization():
    """Test base agent initialization."""
    agent = BaseAgent(
        agent_type="test",
        system_prompt="You are a test agent.",
        request_type=TestRequest,
        response_type=TestResponse
    )
    
    assert agent.agent_type == "test"
    assert not agent._initialized
    
    agent.initialize()
    assert agent._initialized


@pytest.mark.asyncio
async def test_base_agent_status():
    """Test agent status."""
    agent = BaseAgent(
        agent_type="test",
        system_prompt="You are a test agent.",
        request_type=TestRequest,
        response_type=TestResponse
    )
    
    status = agent.get_status()
    assert status["agent_type"] == "test"
    assert status["initialized"] == False
