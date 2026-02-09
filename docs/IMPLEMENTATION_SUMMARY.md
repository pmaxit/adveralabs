# Ad Optimization Agent Implementation Summary

## Overview

This document summarizes the implementation of the intelligent ad optimization agent using Pydantic AI, based on the startup plan in `startup-plan.md`.

## What Was Implemented

### 1. Enhanced Data Models ✅

**File**: `backend/agents/ad_optimization_agent.py`

#### ArmState Model Enhancements
- Added `ltv` (Lifetime Value) field for LTV-based optimization
- Added `profit_margin` field for profit-based optimization
- Added `inventory_status` for e-commerce campaigns (in_stock, low_stock, out_of_stock)
- Added `audience_quality_score` for audience quality assessment
- Added `days_active` for campaign maturity tracking
- Added `current_daily_budget` for budget change calculations

#### New Properties
- `profit`: Calculates profit (revenue * margin - spend)
- `profit_roas`: Profit-based ROAS calculation
- `ltv_roas`: LTV-based ROAS calculation
- `has_sufficient_data`: Checks if arm has enough data for reliable optimization

### 2. Intelligent Budget Allocation Agent ✅

**File**: `backend/agents/ad_optimization_agent.py`

#### Features
- **Pydantic AI Integration**: Uses intelligent agent with detailed system prompt
- **Multi-Objective Optimization**: Supports ROAS, profit, LTV, and CPA goals
- **Exploration vs Exploitation**: Balances trying new opportunities with scaling winners
- **Statistical Confidence**: Gives exploration bonus to low-data arms
- **Business-Level Optimization**: Considers profit margins and LTV, not just platform metrics
- **Constraint Handling**: Respects max_change_ratio and other constraints
- **Fallback Logic**: Rule-based allocation if agent fails

#### System Prompt Highlights
- Detailed instructions on exploration/exploitation balance
- Guidance on statistical confidence and data volume
- Business-level optimization principles
- Constraint handling (max change ratio, inventory status)
- Clear reasoning requirements

### 3. Multi-Armed Bandit Strategies ✅

**File**: `backend/services/optimization_strategies.py` (NEW)

#### Purpose
Provides multiple optimization strategies for budget allocation, allowing choice between intelligent AI agent and proven bandit algorithms.

#### Strategies Implemented
1. **Epsilon-Greedy**: Simple exploration/exploitation balance
2. **Upper Confidence Bound (UCB)**: Balances mean performance with uncertainty
3. **Thompson Sampling**: Bayesian approach using probability distributions
4. **Adaptive**: Switches strategies based on data volume

#### Features
- Performance tracking per arm (mean reward, variance, pulls)
- Confidence intervals
- Automatic strategy selection based on data volume
- Integration with AdOptimizationAgent

### 4. ROI Audit Agent ✅

**File**: `backend/agents/roi_audit_agent.py` (NEW)

#### Purpose
Detects tracking issues, configuration problems, and data quality issues that prevent effective ad optimization.

#### Detected Issues
- Missing conversions with spend
- Low conversion volume
- Missing LTV/profit margin data
- Platform-specific misconfigurations (CAPI, Enhanced Conversions)
- Negative ROAS campaigns
- Out of stock campaigns still spending

#### Features
- Overall health score (0-100)
- Issue severity classification
- Specific recommendations for each issue
- Estimated ROI impact

### 5. Signal Generation Agent ✅

**File**: `backend/agents/signal_generation_agent.py` (NEW)

#### Purpose
Converts raw business events into high-quality conversion signals for ad platforms (Meta CAPI, Google Enhanced Conversions).

#### Features
- **Event Classification**: Classifies events as high_value_purchase, qualified_lead, etc.
- **Value Calculation**: Calculates appropriate conversion values based on LTV, margins, business rules
- **Vertical-Specific Logic**: E-commerce, SaaS, lead-gen best practices
- **Issue Detection**: Flags tracking issues, misconfigurations, missing data
- **Platform Mapping**: Maps events to Meta CAPI and Google Enhanced Conversions formats

#### Models
- `BusinessEvent`: Raw business event from internal systems
- `LTVData`: Lifetime Value data for users/cohorts
- `SignalGenerationRequest`: Request with events, platform, vertical, LTV data
- `PlatformSignal`: Platform-optimized conversion signal
- `SignalGenerationResponse`: Response with signals, issues, recommendations

### 7. Cross-Channel Optimization Agent ✅

**File**: `backend/agents/ad_optimization_agent.py`

#### Features
- Intelligent cross-platform budget allocation
- Marginal return analysis
- Platform-specific recommendations
- Unified business objectives

## Architecture

### Agent Flow

```
Platform APIs (Facebook/Google)
    ↓
Integration Services (fetch_arm_states)
    ↓
ArmState (normalized data model)
    ↓
AdOptimizationAgent.allocate_budget()
    ↓
Pydantic AI Agent (intelligent reasoning)
    ↓
BudgetAllocationResponse
    ↓
Platform APIs (apply budget changes)
```

### Signal Generation Flow

```
Business Events (purchase, signup, etc.)
    ↓
SignalGenerationAgent.generate_signals()
    ↓
Pydantic AI Agent (classification & value calculation)
    ↓
PlatformSignal (Meta CAPI / Google Enhanced Conversions)
    ↓
Platform APIs (send conversion events)
```

## Usage Examples

### Budget Allocation

```python
from backend.agents.ad_optimization_agent import (
    AdOptimizationAgent,
    BudgetAllocationRequest,
    ArmState
)

agent = AdOptimizationAgent()

# Create arm states
arms = [
    ArmState(
        platform="facebook",
        id="adset_123",
        campaign_name="Summer Sale",
        spend=1000.0,
        revenue=3000.0,
        conversions=50,
        clicks=500,
        impressions=10000,
        ltv=150.0,
        profit_margin=0.3,
        current_daily_budget=1000.0
    ),
    ArmState(
        platform="google",
        id="campaign_456",
        campaign_name="Product Search",
        spend=800.0,
        revenue=2400.0,
        conversions=40,
        clicks=400,
        impressions=8000,
        ltv=120.0,
        profit_margin=0.25,
        current_daily_budget=800.0
    )
]

# Allocate budget
request = BudgetAllocationRequest(
    arms=arms,
    total_budget=2000.0,  # $2k/day total
    optimization_goal="profit",  # Optimize for profit
    min_conversions=10,
    max_change_ratio=0.3
)

response = await agent.allocate_budget(request)

# Response contains:
# - allocations: List of BudgetAllocation with new budgets
# - expected_improvement: Expected performance improvement
# - recommendations: Optimization recommendations
```

### Signal Generation

```python
from backend.agents.signal_generation_agent import (
    SignalGenerationAgent,
    SignalGenerationRequest,
    BusinessEvent,
    LTVData
)
from datetime import datetime

agent = SignalGenerationAgent()

# Create business events
events = [
    BusinessEvent(
        event_type="purchase",
        event_id="purchase_001",
        user_id="user_123",
        timestamp=datetime.now(),
        revenue=99.99,
        currency="USD",
        product_id="product_abc",
        metadata={"email": "user@example.com", "product_id": "product_abc"}
    )
]

# LTV data
ltv_data = [
    LTVData(
        user_id="user_123",
        predicted_ltv=250.0,
        confidence_score=0.85
    )
]

# Generate signals
request = SignalGenerationRequest(
    events=events,
    platform="both",  # Generate for both Facebook and Google
    vertical="ecommerce",
    ltv_data=ltv_data,
    profit_margins={"product_abc": 0.3}
)

response = await agent.generate_signals(request)

# Response contains:
# - signals: List of PlatformSignal ready to send to platforms
# - issues_detected: Any tracking/configuration issues
# - recommendations: Improvement recommendations
```

## Key Design Decisions

### 1. Agent-First Approach
- Each major capability is an intelligent agent powered by Pydantic AI
- Agents provide reasoning and context-aware decisions
- Fallback to rule-based logic if agent fails

### 2. Enhanced Data Models
- ArmState includes business-level metrics (LTV, profit margins)
- Supports multiple optimization goals (ROAS, profit, LTV, CPA)
- Includes inventory and audience quality data

### 3. Intelligent Signal Generation
- Transforms raw events into platform-optimized signals
- Considers LTV, margins, qualification rules
- Detects issues and provides recommendations

### 4. Graceful Degradation
- Agents have fallback rule-based logic
- Error handling and logging throughout
- Continues to function even if AI agent fails

## Next Steps

### High Priority
1. ✅ Enhanced ArmState model - DONE
2. ✅ Pydantic AI Budget Allocation Agent - DONE
3. ✅ Signal Generation Agent - DONE
4. ✅ Multi-armed bandit strategies - DONE
5. ✅ ROI audit agent - DONE
6. 🔄 Cross-channel optimization enhancements

### Medium Priority
7. Automation rules engine
8. Experimentation framework

### Lower Priority
9. LTV modeling service
10. Advanced RL-based policies

## Testing

To test the agents:

```python
# Test budget allocation
python -m pytest tests/test_ad_optimization_agent.py

# Test signal generation
python -m pytest tests/test_signal_generation_agent.py
```

## Configuration

Ensure environment variables are set:
- `OPENAI_API_KEY`: For Pydantic AI agent
- `LLM_PROVIDER`: "openai" (default) or "anthropic"
- `FACEBOOK_ADS_API_KEY`: For Facebook API integration
- `GOOGLE_ADS_API_KEY`: For Google Ads API integration

## Notes

- The agents use Pydantic AI for intelligent reasoning
- Fallback logic ensures reliability even if AI fails
- All agents provide detailed reasoning for decisions
- Models are extensible for future enhancements

