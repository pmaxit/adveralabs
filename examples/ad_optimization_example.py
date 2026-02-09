"""Example usage of the Ad Optimization Agent."""
import asyncio
from datetime import datetime
from backend.agents.ad_optimization_agent import (
    AdOptimizationAgent,
    BudgetAllocationRequest,
    ArmState
)
from backend.agents.signal_generation_agent import (
    SignalGenerationAgent,
    SignalGenerationRequest,
    BusinessEvent,
    LTVData
)
from backend.agents.roi_audit_agent import (
    ROIAuditAgent,
    ROIAuditRequest
)
from backend.services.optimization_strategies import (
    OptimizationStrategyService,
    OptimizationStrategy
)


async def example_budget_allocation():
    """Example: Allocate budget across campaigns using intelligent agent."""
    print("=" * 60)
    print("Example: Budget Allocation with Pydantic AI Agent")
    print("=" * 60)
    
    agent = AdOptimizationAgent()
    
    # Create sample arm states representing campaigns/adsets
    arms = [
        ArmState(
            platform="facebook",
            id="adset_summer_sale",
            campaign_id="campaign_123",
            campaign_name="Summer Sale Campaign",
            spend=1500.0,
            revenue=4500.0,
            conversions=75,
            clicks=750,
            impressions=15000,
            ltv=180.0,
            profit_margin=0.35,
            inventory_status="in_stock",
            audience_quality_score=0.85,
            days_active=30,
            current_daily_budget=1500.0
        ),
        ArmState(
            platform="facebook",
            id="adset_new_collection",
            campaign_id="campaign_123",
            campaign_name="New Collection Campaign",
            spend=800.0,
            revenue=2000.0,
            conversions=25,
            clicks=400,
            impressions=8000,
            ltv=150.0,
            profit_margin=0.30,
            inventory_status="in_stock",
            audience_quality_score=0.70,
            days_active=7,  # New campaign
            current_daily_budget=800.0
        ),
        ArmState(
            platform="google",
            id="campaign_product_search",
            campaign_id="campaign_456",
            campaign_name="Product Search Campaign",
            spend=1200.0,
            revenue=3600.0,
            conversions=60,
            clicks=600,
            impressions=12000,
            ltv=200.0,
            profit_margin=0.40,
            inventory_status="in_stock",
            audience_quality_score=0.90,
            days_active=45,
            current_daily_budget=1200.0
        ),
        ArmState(
            platform="google",
            id="campaign_brand_awareness",
            campaign_id="campaign_789",
            campaign_name="Brand Awareness Campaign",
            spend=500.0,
            revenue=800.0,
            conversions=5,  # Low conversions - needs exploration
            clicks=300,
            impressions=5000,
            ltv=None,  # Unknown LTV
            profit_margin=0.25,
            inventory_status="in_stock",
            audience_quality_score=0.60,
            days_active=10,
            current_daily_budget=500.0
        )
    ]
    
    # Create allocation request
    request = BudgetAllocationRequest(
        arms=arms,
        total_budget=4000.0,  # $4k/day total budget
        optimization_goal="profit",  # Optimize for profit
        min_conversions=10,
        max_change_ratio=0.3  # Max 30% change per update
    )
    
    print(f"\nTotal Budget: ${request.total_budget:,.2f}")
    print(f"Optimization Goal: {request.optimization_goal}")
    print(f"Number of Arms: {len(request.arms)}")
    print("\nCurrent Performance:")
    for arm in arms:
        print(f"  {arm.campaign_name} ({arm.platform}): "
              f"ROAS={arm.roas:.2f}, Profit ROAS={arm.profit_roas:.2f}, "
              f"Spend=${arm.spend:,.2f}")
    
    # Allocate budget using intelligent agent
    print("\n" + "-" * 60)
    print("Running intelligent budget allocation...")
    print("-" * 60)
    
    try:
        response = await agent.allocate_budget(request)
        
        print(f"\n✅ Allocation Complete!")
        print(f"Total Allocated: ${response.total_allocated:,.2f}")
        print(f"\nBudget Allocations:")
        
        for allocation in response.allocations:
            print(f"\n  {allocation.arm_id} ({allocation.platform}):")
            print(f"    Current: ${allocation.current_budget:,.2f}")
            print(f"    New:     ${allocation.new_budget:,.2f}")
            print(f"    Change:  {allocation.change_percentage:+.1f}%")
            print(f"    Score:   {allocation.score:.3f}")
            print(f"    Reason:  {allocation.reason}")
        
        print(f"\nExpected Improvement:")
        for key, value in response.expected_improvement.items():
            print(f"  {key}: {value}")
        
        print(f"\nRecommendations:")
        for rec in response.recommendations:
            print(f"  • {rec}")
            
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("This might be due to missing OpenAI API key or network issues.")


async def example_signal_generation():
    """Example: Generate high-quality conversion signals from business events."""
    print("\n" + "=" * 60)
    print("Example: Signal Generation with Pydantic AI Agent")
    print("=" * 60)
    
    agent = SignalGenerationAgent()
    
    # Create sample business events
    events = [
        BusinessEvent(
            event_type="purchase",
            event_id="purchase_001",
            user_id="user_123",
            timestamp=datetime.now(),
            revenue=149.99,
            currency="USD",
            product_id="product_premium",
            metadata={
                "email": "customer@example.com",
                "phone": "+1234567890",
                "product_id": "product_premium",
                "category": "electronics"
            }
        ),
        BusinessEvent(
            event_type="purchase",
            event_id="purchase_002",
            user_id="user_456",
            timestamp=datetime.now(),
            revenue=49.99,
            currency="USD",
            product_id="product_basic",
            metadata={
                "email": "customer2@example.com",
                "product_id": "product_basic",
                "category": "accessories"
            }
        ),
        BusinessEvent(
            event_type="lead",
            event_id="lead_001",
            user_id="user_789",
            timestamp=datetime.now(),
            revenue=None,
            currency="USD",
            metadata={
                "email": "lead@example.com",
                "phone": "+0987654321",
                "qualified": True,
                "source": "website_form"
            }
        )
    ]
    
    # LTV data for users
    ltv_data = [
        LTVData(
            user_id="user_123",
            predicted_ltv=350.0,
            confidence_score=0.90
        ),
        LTVData(
            user_id="user_456",
            predicted_ltv=120.0,
            confidence_score=0.75
        )
    ]
    
    # Profit margins by product
    profit_margins = {
        "product_premium": 0.40,
        "product_basic": 0.25
    }
    
    # Qualification rules
    qualification_rules = {
        "min_score": 70,
        "required_fields": ["email", "phone"]
    }
    
    # Create signal generation request
    request = SignalGenerationRequest(
        events=events,
        platform="both",  # Generate for both Facebook and Google
        vertical="ecommerce",
        ltv_data=ltv_data,
        profit_margins=profit_margins,
        qualification_rules=qualification_rules
    )
    
    print(f"\nBusiness Events: {len(request.events)}")
    print(f"Platform: {request.platform}")
    print(f"Vertical: {request.vertical}")
    
    # Generate signals using intelligent agent
    print("\n" + "-" * 60)
    print("Generating platform-optimized signals...")
    print("-" * 60)
    
    try:
        response = await agent.generate_signals(request)
        
        print(f"\n✅ Signal Generation Complete!")
        print(f"Total Signals Generated: {len(response.signals)}")
        print(f"Total Conversion Value: ${response.total_value:,.2f}")
        print(f"Signals by Platform: {response.signals_by_platform}")
        
        print(f"\nGenerated Signals:")
        for signal in response.signals:
            print(f"\n  {signal.event_id} ({signal.platform}):")
            print(f"    Event: {signal.event_name}")
            print(f"    Classification: {signal.classification}")
            print(f"    Value: ${signal.value:,.2f} {signal.currency}")
            print(f"    Reasoning: {signal.reasoning}")
        
        if response.issues_detected:
            print(f"\n⚠️  Issues Detected:")
            for issue in response.issues_detected:
                print(f"  • {issue}")
        
        if response.recommendations:
            print(f"\n💡 Recommendations:")
            for rec in response.recommendations:
                print(f"  • {rec}")
                
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("This might be due to missing OpenAI API key or network issues.")


async def example_bandit_strategies():
    """Example: Using different bandit strategies for optimization."""
    print("\n" + "=" * 60)
    print("Example: Multi-Armed Bandit Strategies")
    print("=" * 60)
    
    strategy_service = OptimizationStrategyService()
    
    # Create sample arms
    arms = [
        ArmState(
            platform="facebook",
            id="adset_1",
            campaign_name="Campaign A",
            spend=1000.0,
            revenue=3000.0,
            conversions=50,
            clicks=500,
            impressions=10000,
            current_daily_budget=1000.0
        ),
        ArmState(
            platform="google",
            id="campaign_2",
            campaign_name="Campaign B",
            spend=800.0,
            revenue=2000.0,
            conversions=30,
            clicks=400,
            impressions=8000,
            current_daily_budget=800.0
        )
    ]
    
    strategies = [
        ("UCB", OptimizationStrategy.UCB),
        ("Thompson Sampling", OptimizationStrategy.THOMPSON_SAMPLING),
        ("Epsilon-Greedy", OptimizationStrategy.EPSILON_GREEDY),
        ("Adaptive", OptimizationStrategy.ADAPTIVE)
    ]
    
    print(f"\nTesting different strategies with ${2000.0:,.2f} total budget:")
    print(f"Number of arms: {len(arms)}")
    
    for strategy_name, strategy in strategies:
        print(f"\n{strategy_name}:")
        allocations = strategy_service.allocate_with_strategy(
            arms,
            total_budget=2000.0,
            strategy=strategy,
            optimization_goal="roas"
        )
        
        for arm_id, budget in allocations.items():
            arm = next(a for a in arms if a.id == arm_id)
            print(f"  {arm.campaign_name}: ${budget:,.2f} ({budget/2000.0*100:.1f}%)")


async def example_roi_audit():
    """Example: ROI audit to detect issues."""
    print("\n" + "=" * 60)
    print("Example: ROI Audit")
    print("=" * 60)
    
    agent = ROIAuditAgent()
    
    # Create arms with various issues
    arms = [
        ArmState(
            platform="facebook",
            id="adset_good",
            campaign_name="Good Campaign",
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
            platform="facebook",
            id="adset_no_conversions",
            campaign_name="No Conversions Campaign",
            spend=500.0,
            revenue=0.0,
            conversions=0,  # Issue: spending but no conversions
            clicks=200,
            impressions=5000,
            current_daily_budget=500.0
        ),
        ArmState(
            platform="google",
            id="campaign_low_volume",
            campaign_name="Low Volume Campaign",
            spend=300.0,
            revenue=600.0,
            conversions=3,  # Issue: low conversion volume
            clicks=150,
            impressions=3000,
            current_daily_budget=300.0
        ),
        ArmState(
            platform="google",
            id="campaign_missing_ltv",
            campaign_name="Missing LTV Campaign",
            spend=800.0,
            revenue=2400.0,
            conversions=40,
            clicks=400,
            impressions=8000,
            ltv=None,  # Issue: missing LTV when optimizing for LTV
            profit_margin=0.25,
            current_daily_budget=800.0
        )
    ]
    
    request = ROIAuditRequest(
        arms=arms,
        account_id="account_123",
        time_window="last_7d",
        optimization_goal="ltv",
        platform_configs={
            "facebook": {
                "conversions_api_enabled": False  # Issue: CAPI not enabled
            },
            "google": {
                "enhanced_conversions_enabled": False  # Issue: Enhanced Conversions not enabled
            }
        }
    )
    
    print(f"\nAuditing {len(request.arms)} arms...")
    print(f"Optimization Goal: {request.optimization_goal}")
    
    try:
        response = await agent.audit(request)
        
        print(f"\n✅ Audit Complete!")
        print(f"Overall Health Score: {response.overall_health_score}/100")
        print(f"Critical Issues: {response.critical_issues_count}")
        
        if response.tracking_issues:
            print(f"\n📊 Tracking Issues ({len(response.tracking_issues)}):")
            for issue in response.tracking_issues:
                print(f"\n  [{issue.severity.upper()}] {issue.issue_type}")
                print(f"    Description: {issue.description}")
                print(f"    Recommendation: {issue.recommendation}")
                if issue.estimated_impact:
                    print(f"    Impact: {issue.estimated_impact}")
        
        if response.configuration_issues:
            print(f"\n⚙️  Configuration Issues ({len(response.configuration_issues)}):")
            for issue in response.configuration_issues:
                print(f"\n  [{issue.severity.upper()}] {issue.issue_type}")
                print(f"    Description: {issue.description}")
                print(f"    Recommendation: {issue.recommendation}")
                if issue.estimated_impact:
                    print(f"    Impact: {issue.estimated_impact}")
        
        if response.recommendations:
            print(f"\n💡 Priority Recommendations:")
            for rec in response.recommendations:
                print(f"  • {rec}")
        
        if response.estimated_roi_impact:
            print(f"\n📈 {response.estimated_roi_impact}")
            
    except Exception as e:
        print(f"\n❌ Error: {e}")


async def main():
    """Run all examples."""
    print("\n" + "=" * 60)
    print("Ad Optimization Agent Examples")
    print("=" * 60)
    
    # Example 1: Budget Allocation
    await example_budget_allocation()
    
    # Example 2: Signal Generation
    await example_signal_generation()
    
    # Example 3: Bandit Strategies
    await example_bandit_strategies()
    
    # Example 4: ROI Audit
    await example_roi_audit()
    
    print("\n" + "=" * 60)
    print("Examples Complete!")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())

