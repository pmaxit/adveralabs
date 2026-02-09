"""Multi-armed bandit optimization strategies for budget allocation."""
from typing import List, Dict, Optional
from enum import Enum
import math
import random
import numpy as np
from pydantic import BaseModel, Field

from backend.agents.ad_optimization_agent import ArmState


class OptimizationStrategy(str, Enum):
    """Optimization strategy types."""
    EPSILON_GREEDY = "epsilon_greedy"
    UCB = "ucb"  # Upper Confidence Bound
    THOMPSON_SAMPLING = "thompson_sampling"
    ADAPTIVE = "adaptive"


class ArmPerformance(BaseModel):
    """Performance metrics for an arm."""
    arm_id: str
    platform: str
    mean_reward: float = Field(default=0.0, description="Mean reward (ROAS, profit, etc.)")
    variance: float = Field(default=0.0, description="Reward variance")
    pulls: int = Field(default=0, description="Number of times arm was selected")
    confidence_interval: float = Field(default=0.0, description="Confidence interval width")
    
    @property
    def standard_error(self) -> float:
        """Calculate standard error."""
        if self.pulls == 0:
            return float('inf')
        return math.sqrt(self.variance / self.pulls) if self.variance > 0 else 0.0


class OptimizationStrategyService:
    """Service for multi-armed bandit optimization strategies."""
    
    def __init__(self):
        """Initialize strategy service."""
        self.arm_performance: Dict[str, ArmPerformance] = {}
    
    def update_arm_performance(
        self,
        arm: ArmState,
        optimization_goal: str = "roas"
    ) -> ArmPerformance:
        """Update performance metrics for an arm."""
        # Calculate reward based on optimization goal
        if optimization_goal == "roas":
            reward = arm.roas
        elif optimization_goal == "profit":
            reward = arm.profit_roas
        elif optimization_goal == "ltv":
            reward = arm.ltv_roas
        elif optimization_goal == "cpa":
            reward = 1.0 / arm.cpa if arm.cpa > 0 and arm.cpa != float('inf') else 0.0
        else:
            reward = arm.roas
        
        # Get or create performance record
        if arm.id not in self.arm_performance:
            self.arm_performance[arm.id] = ArmPerformance(
                arm_id=arm.id,
                platform=arm.platform,
                mean_reward=reward,
                variance=0.0,
                pulls=1
            )
            return self.arm_performance[arm.id]
        
        # Update using exponential moving average
        perf = self.arm_performance[arm.id]
        alpha = 0.1  # Learning rate
        old_mean = perf.mean_reward
        new_mean = old_mean + alpha * (reward - old_mean)
        
        # Update variance (simplified)
        if perf.pulls > 1:
            variance_update = (reward - old_mean) * (reward - new_mean)
            perf.variance = (perf.variance * (perf.pulls - 1) + variance_update) / perf.pulls
        
        perf.mean_reward = new_mean
        perf.pulls += 1
        
        # Calculate confidence interval (95% confidence)
        if perf.pulls > 1:
            z_score = 1.96  # 95% confidence
            perf.confidence_interval = z_score * perf.standard_error
        
        return perf
    
    def epsilon_greedy(
        self,
        arms: List[ArmState],
        total_budget: float,
        epsilon: float = 0.1,
        optimization_goal: str = "roas"
    ) -> Dict[str, float]:
        """Epsilon-greedy strategy: explore with probability epsilon, exploit otherwise."""
        if not arms:
            return {}
        
        # Update performance for all arms
        performances = {}
        for arm in arms:
            perf = self.update_arm_performance(arm, optimization_goal)
            performances[arm.id] = perf
        
        # Decide: explore or exploit
        if random.random() < epsilon:
            # Explore: random selection
            selected_arm = random.choice(arms)
            budget_per_arm = total_budget / len(arms)
            return {selected_arm.id: budget_per_arm}
        else:
            # Exploit: select best performing arm
            best_arm_id = max(performances.items(), key=lambda x: x[1].mean_reward)[0]
            return {best_arm_id: total_budget}
    
    def ucb(
        self,
        arms: List[ArmState],
        total_budget: float,
        optimization_goal: str = "roas",
        confidence_level: float = 2.0
    ) -> Dict[str, float]:
        """Upper Confidence Bound (UCB) strategy.
        
        Balances exploration and exploitation by selecting arms with highest
        upper confidence bound: mean_reward + confidence_level * sqrt(ln(total_pulls) / arm_pulls)
        """
        if not arms:
            return {}
        
        # Update performance for all arms
        performances = {}
        total_pulls = sum(arm.conversions for arm in arms) or 1
        
        for arm in arms:
            perf = self.update_arm_performance(arm, optimization_goal)
            performances[arm.id] = perf
        
        # Calculate UCB scores
        ucb_scores = {}
        for arm_id, perf in performances.items():
            if perf.pulls == 0:
                # High score for unexplored arms
                ucb_scores[arm_id] = float('inf')
            else:
                # UCB formula: mean + confidence * sqrt(ln(total_pulls) / pulls)
                exploration_bonus = confidence_level * math.sqrt(
                    math.log(total_pulls) / perf.pulls
                )
                ucb_scores[arm_id] = perf.mean_reward + exploration_bonus
        
        # Allocate budget proportionally to UCB scores
        total_score = sum(ucb_scores.values())
        if total_score == 0:
            # Equal allocation if no scores
            budget_per_arm = total_budget / len(arms)
            return {arm.id: budget_per_arm for arm in arms}
        
        allocations = {}
        for arm in arms:
            share = ucb_scores[arm.id] / total_score
            allocations[arm.id] = total_budget * share
        
        return allocations
    
    def thompson_sampling(
        self,
        arms: List[ArmState],
        total_budget: float,
        optimization_goal: str = "roas"
    ) -> Dict[str, float]:
        """Thompson Sampling strategy using Bayesian approach.
        
        Models each arm's reward as a Beta distribution and samples from it
        to balance exploration and exploitation.
        """
        if not arms:
            return {}
        
        # Update performance for all arms
        performances = {}
        for arm in arms:
            perf = self.update_arm_performance(arm, optimization_goal)
            performances[arm.id] = perf
        
        # Sample from Beta distribution for each arm
        # Beta(alpha, beta) where alpha = successes, beta = failures
        samples = {}
        for arm_id, perf in performances.items():
            if perf.pulls == 0:
                # Uniform prior for unexplored arms
                samples[arm_id] = random.random()
            else:
                # Estimate success rate from mean reward
                # Normalize reward to [0, 1] range (assuming max reward of 10)
                normalized_reward = min(perf.mean_reward / 10.0, 1.0)
                successes = int(normalized_reward * perf.pulls)
                failures = perf.pulls - successes
                
                # Sample from Beta distribution
                alpha = successes + 1  # Add 1 for prior
                beta = failures + 1
                samples[arm_id] = np.random.beta(alpha, beta)
        
        # Allocate budget proportionally to samples
        total_sample = sum(samples.values())
        if total_sample == 0:
            budget_per_arm = total_budget / len(arms)
            return {arm.id: budget_per_arm for arm in arms}
        
        allocations = {}
        for arm in arms:
            share = samples[arm.id] / total_sample
            allocations[arm.id] = total_budget * share
        
        return allocations
    
    def adaptive_strategy(
        self,
        arms: List[ArmState],
        total_budget: float,
        optimization_goal: str = "roas"
    ) -> Dict[str, float]:
        """Adaptive strategy that switches between methods based on data volume.
        
        - Low data: Use epsilon-greedy with high epsilon
        - Medium data: Use UCB
        - High data: Use Thompson Sampling
        """
        # Calculate total data volume
        total_conversions = sum(arm.conversions for arm in arms)
        avg_conversions = total_conversions / len(arms) if arms else 0
        
        if avg_conversions < 10:
            # Low data: use epsilon-greedy with high exploration
            return self.epsilon_greedy(arms, total_budget, epsilon=0.3, optimization_goal=optimization_goal)
        elif avg_conversions < 50:
            # Medium data: use UCB
            return self.ucb(arms, total_budget, optimization_goal=optimization_goal)
        else:
            # High data: use Thompson Sampling
            return self.thompson_sampling(arms, total_budget, optimization_goal=optimization_goal)
    
    def allocate_with_strategy(
        self,
        arms: List[ArmState],
        total_budget: float,
        strategy: OptimizationStrategy,
        optimization_goal: str = "roas",
        **kwargs
    ) -> Dict[str, float]:
        """Allocate budget using specified strategy."""
        if strategy == OptimizationStrategy.EPSILON_GREEDY:
            epsilon = kwargs.get("epsilon", 0.1)
            return self.epsilon_greedy(arms, total_budget, epsilon, optimization_goal)
        elif strategy == OptimizationStrategy.UCB:
            confidence = kwargs.get("confidence_level", 2.0)
            return self.ucb(arms, total_budget, optimization_goal, confidence)
        elif strategy == OptimizationStrategy.THOMPSON_SAMPLING:
            return self.thompson_sampling(arms, total_budget, optimization_goal)
        elif strategy == OptimizationStrategy.ADAPTIVE:
            return self.adaptive_strategy(arms, total_budget, optimization_goal)
        else:
            # Default to UCB
            return self.ucb(arms, total_budget, optimization_goal)
    
    def get_arm_performance(self, arm_id: str) -> Optional[ArmPerformance]:
        """Get performance metrics for an arm."""
        return self.arm_performance.get(arm_id)
    
    def reset_performance(self):
        """Reset all performance metrics."""
        self.arm_performance.clear()

