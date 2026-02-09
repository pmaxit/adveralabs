# Ad Optimization Agent - Task Plan

## Overview

This document outlines the implementation plan for building a sophisticated ad optimization agent using Pydantic AI, based on the startup plan described in `startup-plan.md`. The agent will implement the 4-pillar system design for cross-channel ad optimization.

## Architecture Principles

1. **Agent-First Design**: Each major capability is an intelligent agent powered by Pydantic AI
2. **Data Normalization**: Unified data models across Facebook and Google platforms
3. **Incremental Improvement**: Start with rule-based, evolve to ML/RL-based optimization
4. **Business-Level Optimization**: Optimize for profit, LTV, margin - not just ROAS
5. **Cross-Channel Intelligence**: Unified decision-making across platforms

## Task Breakdown

### Phase 1: Core Data Models & Infrastructure ✅ (Partially Complete)

#### Task 1.1: Enhance ArmState Model
- [x] Basic ArmState with spend, revenue, conversions
- [ ] Add LTV (Lifetime Value) field
- [ ] Add profit margin field
- [ ] Add inventory/stock status (for e-commerce)
- [ ] Add audience quality scores
- [ ] Add historical performance trends
- [ ] Add confidence intervals for metrics

**File**: `backend/agents/ad_optimization_agent.py`

#### Task 1.2: Enhanced Request/Response Models
- [x] Basic BudgetAllocationRequest/Response
- [ ] Add OptimizationStrategy enum (bandit, greedy, thompson_sampling, ucb)
- [ ] Add ExperimentConfig for A/B testing
- [ ] Add ROI audit request/response models
- [ ] Add signal generation request/response models

**File**: `backend/agents/ad_optimization_agent.py`

### Phase 2: Intelligent Budget Allocation Agent

#### Task 2.1: Create Pydantic AI Budget Allocation Agent
**Goal**: Replace simple scoring with intelligent agent that reasons about budget allocation

**Implementation**:
- Create agent with system prompt focused on multi-armed bandit principles
- Agent should consider:
  - Exploration vs exploitation tradeoff
  - Statistical confidence in performance data
  - Business objectives (ROAS, profit, LTV)
  - Platform-specific constraints
  - Budget change limits (max_change_ratio)
- Agent should provide reasoning for each allocation decision

**System Prompt Template**:
```
You are an expert ad budget optimization agent. Your task is to allocate budgets across 
campaigns and ad sets (arms) to maximize business outcomes.

Key principles:
1. Balance exploration (trying new opportunities) with exploitation (scaling winners)
2. Consider statistical confidence - low conversion volume arms need exploration bonus
3. Optimize for business-level metrics (profit, LTV) not just platform metrics
4. Respect constraints: max budget change ratio, minimum spend thresholds
5. Provide clear reasoning for each allocation decision

Given arm performance data, allocate the total budget optimally.
```

**File**: `backend/agents/ad_optimization_agent.py`

#### Task 2.2: Multi-Armed Bandit Strategies
**Goal**: Implement different optimization strategies

**Strategies to implement**:
1. **Epsilon-Greedy**: Simple exploration/exploitation
2. **Upper Confidence Bound (UCB)**: Balances mean performance with uncertainty
3. **Thompson Sampling**: Bayesian approach using probability distributions
4. **Adaptive**: Switches strategies based on data volume

**File**: `backend/services/optimization_strategies.py` (new)

### Phase 3: Signal Generation Agent

#### Task 3.1: Create Signal Generation Agent
**Goal**: Intelligent conversion signal mapping

**Capabilities**:
- Map internal events to platform-optimized events
- Classify events as "high_value_purchase", "qualified_lead", etc.
- Calculate appropriate conversion values
- Handle LTV modeling and prediction
- Provide guardrails and best-practice mappings

**System Prompt**:
```
You are a conversion signal optimization agent. Your task is to transform raw business 
events into high-quality conversion signals for ad platforms.

Responsibilities:
1. Classify events by business value (high_value_purchase, qualified_lead, etc.)
2. Calculate appropriate conversion values based on LTV, margins, business rules
3. Apply vertical-specific best practices (e-commerce, SaaS, lead-gen)
4. Flag potential issues: misconfigured events, broken tracking, wrong primary events
5. Map events to platform-specific formats (Meta CAPI, Google Enhanced Conversions)

Your goal is to feed platforms better signals than they receive natively.
```

**File**: `backend/agents/signal_generation_agent.py` (new)

#### Task 3.2: LTV Modeling Integration
- Create LTV prediction service
- Integrate with signal generation agent
- Support both historical LTV and predicted LTV

**File**: `backend/services/ltv_service.py` (new)

### Phase 4: Cross-Channel Optimization Agent

#### Task 4.1: Create Cross-Channel Optimization Agent
**Goal**: Intelligent budget allocation across Facebook and Google

**Capabilities**:
- Compute marginal return curves
- Compare performance across platforms
- Make unified budget decisions
- Provide platform-specific recommendations
- Handle platform-specific constraints

**System Prompt**:
```
You are a cross-channel ad optimization expert. Your task is to optimize budgets across 
Facebook and Google Ads platforms to maximize overall business outcomes.

Key considerations:
1. Marginal returns: "If I add $x to Campaign A on Meta vs Campaign B on Google, 
   which yields more profit/ROAS?"
2. Platform-specific performance patterns
3. Unified business objectives (profit per day, not per-platform ROAS)
4. Cross-platform budget coordination
5. Platform-specific constraints and best practices

Provide actionable recommendations for budget shifts and bid adjustments.
```

**File**: `backend/agents/ad_optimization_agent.py` (enhance existing)

#### Task 4.2: Marginal Return Analysis
- Implement marginal return curve calculation
- Compare incremental returns across platforms
- Support different optimization goals (profit, ROAS, LTV)

**File**: `backend/services/marginal_returns.py` (new)

### Phase 5: Automation & Experimentation Engine

#### Task 5.1: Automation Rules Engine
**Goal**: Automate common optimization tasks

**Automation Types**:
1. **Budget Scaling**: "If ROAS > 3 for 5 days, increase budget by 25%"
2. **Creative Testing**: Rotate creatives, allocate to winners
3. **Audience Management**: Suppress converters, expand high-LTV lookalikes
4. **Campaign Pausing**: Pause negative ROI segments
5. **Bid Adjustment**: Adjust tCPA/ROAS targets within safe bounds

**File**: `backend/services/automation_engine.py` (new)

#### Task 5.2: Experimentation Framework
**Goal**: A/B testing and incrementality measurement

**Features**:
- Account-level / campaign-level splits
- Geo holdout experiments
- Statistical power calculation
- Incremental lift computation
- Built-in reporting

**File**: `backend/services/experimentation_service.py` (new)

### Phase 6: ROI Audit Agent

#### Task 6.1: Create ROI Audit Agent
**Goal**: Detect tracking issues and misconfigurations

**Checks**:
- Misconfigured conversions
- Broken tracking
- Wrong primary events
- Low conversion volume warnings
- Attribution inconsistencies
- Platform-specific configuration issues

**System Prompt**:
```
You are an ROI audit agent. Your task is to identify issues that prevent ad platforms 
from optimizing effectively.

Common issues to detect:
1. Misconfigured conversion events (wrong primary event, missing values)
2. Broken tracking (missing pixels, server-side issues)
3. Low conversion volume (insufficient data for Smart Bidding)
4. Attribution inconsistencies (last-click vs data-driven)
5. Platform-specific misconfigurations

Provide actionable recommendations to fix issues.
```

**File**: `backend/agents/roi_audit_agent.py` (new)

### Phase 7: Integration & API Enhancements

#### Task 7.1: Enhance Optimization Service
- Integrate all agents
- Add scheduling support
- Add error handling and retries
- Add performance monitoring

**File**: `backend/services/optimization_service.py`

#### Task 7.2: API Endpoints
- [x] Basic optimization endpoints
- [ ] Signal generation endpoint
- [ ] ROI audit endpoint
- [ ] Experimentation endpoints
- [ ] Automation rule management endpoints

**File**: `backend/api/routes/agents.py`

### Phase 8: Testing & Validation

#### Task 8.1: Unit Tests
- Test each agent independently
- Test optimization strategies
- Test data normalization

#### Task 8.2: Integration Tests
- Test full optimization cycle
- Test cross-channel optimization
- Test signal generation flow

#### Task 8.3: Validation Framework
- A/B test framework validation
- Incrementality measurement validation
- Statistical significance testing

## Implementation Priority

### High Priority (MVP)
1. ✅ Enhanced ArmState model
2. 🔄 Pydantic AI Budget Allocation Agent
3. 🔄 Cross-Channel Optimization Agent
4. 🔄 Signal Generation Agent

### Medium Priority
5. Multi-armed bandit strategies
6. Automation rules engine
7. ROI audit agent

### Lower Priority (Future)
8. Experimentation framework
9. LTV modeling service
10. Advanced RL-based policies

## Technical Decisions

### Pydantic AI Usage
- Use `Agent` class with structured output (Pydantic models)
- System prompts should be detailed and include examples
- Use `result_type` to ensure type safety
- Handle errors gracefully with fallback logic

### Data Flow
```
Platform APIs → Integration Services → ArmState (normalized) → 
Optimization Agents → Allocation Decisions → Platform APIs
```

### Agent Communication
- Agents can call other agents when needed
- Use shared data models (ArmState, etc.)
- Maintain agent state for context

### Error Handling
- Graceful degradation if agent fails
- Fallback to rule-based logic
- Log all agent decisions for audit

## Success Metrics

1. **Budget Allocation Quality**: Improved ROAS/profit vs baseline
2. **Agent Reasoning Quality**: Clear, actionable recommendations
3. **Cross-Channel Performance**: Better unified outcomes
4. **Signal Quality**: Higher conversion value signals to platforms
5. **Issue Detection**: Early detection of tracking/config issues

## Next Steps

1. Start with Task 2.1: Create Pydantic AI Budget Allocation Agent
2. Enhance ArmState model with additional fields
3. Test with sample data
4. Iterate based on results

