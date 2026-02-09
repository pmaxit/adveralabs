"""ROI Audit Agent for detecting tracking issues and misconfigurations."""
from typing import List, Optional, Dict, Any, Literal
from pydantic import BaseModel, Field
from datetime import datetime, timedelta
import logging

from backend.agents.base_agent import BaseAgent
from backend.agents.ad_optimization_agent import ArmState

logger = logging.getLogger(__name__)


class TrackingIssue(BaseModel):
    """Detected tracking issue."""
    issue_type: str = Field(..., description="Type of issue")
    severity: Literal["critical", "high", "medium", "low"] = Field(..., description="Issue severity")
    description: str = Field(..., description="Issue description")
    affected_arms: List[str] = Field(default_factory=list, description="Affected arm IDs")
    recommendation: str = Field(..., description="Recommended fix")
    estimated_impact: Optional[str] = Field(default=None, description="Estimated performance impact")


class ConfigurationIssue(BaseModel):
    """Detected configuration issue."""
    issue_type: str = Field(..., description="Type of configuration issue")
    severity: Literal["critical", "high", "medium", "low"] = Field(..., description="Issue severity")
    description: str = Field(..., description="Issue description")
    platform: Optional[str] = Field(default=None, description="Affected platform")
    recommendation: str = Field(..., description="Recommended fix")
    estimated_impact: Optional[str] = Field(default=None, description="Estimated performance impact")


class ROIAuditRequest(BaseModel):
    """Request model for ROI audit."""
    arms: List[ArmState] = Field(..., description="Arm states to audit")
    account_id: str = Field(..., description="Account ID")
    time_window: str = Field(default="last_7d", description="Time window for audit")
    optimization_goal: Literal["roas", "profit", "ltv", "cpa"] = Field(
        default="roas",
        description="Current optimization goal"
    )
    platform_configs: Optional[Dict[str, Dict[str, Any]]] = Field(
        default=None,
        description="Platform-specific configurations"
    )


class ROIAuditResponse(BaseModel):
    """Response model for ROI audit."""
    tracking_issues: List[TrackingIssue] = Field(
        default_factory=list,
        description="Detected tracking issues"
    )
    configuration_issues: List[ConfigurationIssue] = Field(
        default_factory=list,
        description="Detected configuration issues"
    )
    overall_health_score: float = Field(
        ...,
        ge=0,
        le=100,
        description="Overall health score (0-100)"
    )
    critical_issues_count: int = Field(default=0, description="Number of critical issues")
    recommendations: List[str] = Field(
        default_factory=list,
        description="Priority recommendations"
    )
    estimated_roi_impact: Optional[str] = Field(
        default=None,
        description="Estimated ROI impact of fixing issues"
    )


class ROIAuditAgent:
    """Agent for auditing ROI and detecting tracking/configuration issues."""
    
    def __init__(self):
        """Initialize ROI audit agent."""
        self.agent = BaseAgent(
            agent_type="roi_audit",
            system_prompt="""You are an ROI audit agent. Your task is to identify issues that prevent 
            ad platforms from optimizing effectively.

            Common issues to detect:

            1. Tracking Issues:
               - Missing conversion tracking (zero conversions with spend)
               - Broken pixels (no events firing)
               - Server-side tracking issues
               - Attribution inconsistencies (last-click vs data-driven)
               - Missing user identifiers (email, phone) for enhanced conversions
               - Duplicate event tracking
            
            2. Configuration Issues:
               - Misconfigured conversion events (wrong primary event, missing values)
               - Low conversion volume (insufficient data for Smart Bidding)
               - Wrong optimization goal (optimizing for clicks instead of conversions)
               - Budget constraints too tight (can't scale winners)
               - Campaign structure issues (too many small campaigns)
               - Platform-specific misconfigurations:
                 * Facebook: Missing Conversions API setup
                 * Google: Missing Enhanced Conversions, wrong conversion actions
            
            3. Data Quality Issues:
               - Inconsistent revenue values (zeros, outliers)
               - Missing LTV data when optimizing for LTV
               - Missing profit margins when optimizing for profit
               - Low-quality conversion events (test events, bot traffic)
            
            4. Performance Issues:
               - Arms with negative ROAS running for extended periods
               - Arms with very low conversion volume (< 10 conversions)
               - Arms with high spend but no conversions
               - Arms with declining performance trends

            For each issue, provide:
            - Type and severity (critical, high, medium, low)
            - Clear description
            - Affected arms/platforms
            - Specific recommendation to fix
            - Estimated impact on ROI/performance

            Calculate an overall health score (0-100) based on:
            - Number and severity of issues
            - Data quality
            - Configuration correctness
            - Performance metrics

            Provide priority recommendations ordered by impact.""",
            request_type=ROIAuditRequest,
            response_type=ROIAuditResponse
        )
    
    async def audit(
        self,
        request: ROIAuditRequest
    ) -> ROIAuditResponse:
        """Perform ROI audit using intelligent agent."""
        try:
            self.agent.initialize()
            response = await self.agent.execute(request)
            logger.info(f"ROI audit completed for account {request.account_id}")
            return response
        except Exception as e:
            logger.warning(f"Agent audit failed, falling back to rule-based: {e}")
            return await self._audit_fallback(request)
    
    async def _audit_fallback(
        self,
        request: ROIAuditRequest
    ) -> ROIAuditResponse:
        """Fallback rule-based ROI audit."""
        tracking_issues = []
        config_issues = []
        
        # Check for tracking issues
        for arm in request.arms:
            # Missing conversions with spend
            if arm.spend > 0 and arm.conversions == 0:
                tracking_issues.append(
                    TrackingIssue(
                        issue_type="missing_conversions",
                        severity="critical",
                        description=f"Arm {arm.id} has ${arm.spend:.2f} spend but zero conversions",
                        affected_arms=[arm.id],
                        recommendation="Check conversion tracking setup, verify pixels are firing",
                        estimated_impact="High - Smart Bidding cannot optimize without conversion data"
                    )
                )
            
            # Low conversion volume
            if arm.conversions > 0 and arm.conversions < 10 and arm.spend > 100:
                tracking_issues.append(
                    TrackingIssue(
                        issue_type="low_conversion_volume",
                        severity="high",
                        description=f"Arm {arm.id} has only {arm.conversions} conversions with ${arm.spend:.2f} spend",
                        affected_arms=[arm.id],
                        recommendation="Increase conversion volume or extend time window for data collection",
                        estimated_impact="Medium - Smart Bidding needs more data for reliable optimization"
                    )
                )
            
            # Negative ROAS
            if arm.roas < 0.5 and arm.spend > 500:
                config_issues.append(
                    ConfigurationIssue(
                        issue_type="negative_roas",
                        severity="high",
                        description=f"Arm {arm.id} has ROAS of {arm.roas:.2f} (spending ${arm.spend:.2f})",
                        platform=arm.platform,
                        recommendation="Review campaign targeting, creatives, or consider pausing",
                        estimated_impact="High - Wasting ad spend"
                    )
                )
            
            # Missing LTV when optimizing for LTV
            if request.optimization_goal == "ltv" and arm.ltv is None:
                config_issues.append(
                    ConfigurationIssue(
                        issue_type="missing_ltv_data",
                        severity="medium",
                        description=f"Arm {arm.id} missing LTV data but optimizing for LTV",
                        platform=arm.platform,
                        recommendation="Set up LTV tracking or switch optimization goal to ROAS",
                        estimated_impact="Medium - Cannot optimize for LTV without LTV data"
                    )
                )
            
            # Missing profit margin when optimizing for profit
            if request.optimization_goal == "profit" and arm.profit_margin is None:
                config_issues.append(
                    ConfigurationIssue(
                        issue_type="missing_profit_margin",
                        severity="medium",
                        description=f"Arm {arm.id} missing profit margin but optimizing for profit",
                        platform=arm.platform,
                        recommendation="Add profit margin data or switch optimization goal to ROAS",
                        estimated_impact="Medium - Cannot optimize for profit without margin data"
                    )
                )
            
            # Out of stock inventory
            if arm.inventory_status == "out_of_stock" and arm.spend > 0:
                config_issues.append(
                    ConfigurationIssue(
                        issue_type="out_of_stock_campaign",
                        severity="high",
                        description=f"Arm {arm.id} is out of stock but still spending",
                        platform=arm.platform,
                        recommendation="Pause campaign or update inventory status",
                        estimated_impact="High - Wasting spend on unavailable products"
                    )
                )
        
        # Check platform-specific configurations
        if request.platform_configs:
            # Facebook-specific checks
            fb_config = request.platform_configs.get("facebook", {})
            if not fb_config.get("conversions_api_enabled", False):
                config_issues.append(
                    ConfigurationIssue(
                        issue_type="missing_capi",
                        severity="high",
                        description="Facebook Conversions API (CAPI) not enabled",
                        platform="facebook",
                        recommendation="Set up Conversions API for better tracking and optimization",
                        estimated_impact="High - Better conversion tracking improves Smart Bidding"
                    )
                )
            
            # Google-specific checks
            google_config = request.platform_configs.get("google", {})
            if not google_config.get("enhanced_conversions_enabled", False):
                config_issues.append(
                    ConfigurationIssue(
                        issue_type="missing_enhanced_conversions",
                        severity="high",
                        description="Google Enhanced Conversions not enabled",
                        platform="google",
                        recommendation="Enable Enhanced Conversions for better conversion matching",
                        estimated_impact="High - Better conversion matching improves Smart Bidding"
                    )
                )
        
        # Calculate health score
        critical_count = len([i for i in tracking_issues + config_issues if i.severity == "critical"])
        high_count = len([i for i in tracking_issues + config_issues if i.severity == "high"])
        medium_count = len([i for i in tracking_issues + config_issues if i.severity == "medium"])
        
        # Health score: 100 - (critical * 20 + high * 10 + medium * 5)
        health_score = max(0, 100 - (critical_count * 20 + high_count * 10 + medium_count * 5))
        
        # Generate recommendations
        recommendations = []
        if critical_count > 0:
            recommendations.append(f"Fix {critical_count} critical issue(s) immediately")
        if high_count > 0:
            recommendations.append(f"Address {high_count} high-priority issue(s)")
        if not request.platform_configs or not request.platform_configs.get("facebook", {}).get("conversions_api_enabled"):
            recommendations.append("Set up Facebook Conversions API for better tracking")
        if not request.platform_configs or not request.platform_configs.get("google", {}).get("enhanced_conversions_enabled"):
            recommendations.append("Enable Google Enhanced Conversions")
        
        return ROIAuditResponse(
            tracking_issues=tracking_issues,
            configuration_issues=config_issues,
            overall_health_score=health_score,
            critical_issues_count=critical_count,
            recommendations=recommendations,
            estimated_roi_impact=f"Fixing issues could improve ROI by 10-30%"
        )

