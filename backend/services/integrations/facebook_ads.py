"""Facebook Ads API integration."""
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import httpx
import logging

from backend.config.settings import settings

logger = logging.getLogger(__name__)


class FacebookAdsIntegration:
    """Facebook Marketing API integration service."""
    
    def __init__(self):
        """Initialize Facebook Ads integration."""
        self.access_token = settings.facebook_ads_api_key
        self.api_version = "v19.0"
        self.base_url = f"https://graph.facebook.com/{self.api_version}"
    
    async def get_insights(
        self,
        account_id: str,
        date_preset: str = "yesterday",
        level: str = "campaign",
        time_increment: int = 1,
        fields: Optional[List[str]] = None
    ) -> List[Dict[str, Any]]:
        """Get insights from Facebook Ads API.
        
        Example usage based on PDF:
        - Fetch campaign/adset performance data
        - Supports date_preset: 'yesterday', 'last_7d', 'last_30d', or custom time_range
        - Level: 'campaign', 'adset', 'ad', 'account'
        """
        if fields is None:
            fields = [
                "campaign_id",
                "campaign_name",
                "impressions",
                "clicks",
                "spend",
                "actions",
                "action_values"
            ]
        
        url = f"{self.base_url}/{account_id}/insights"
        params = {
            "access_token": self.access_token,
            "date_preset": date_preset,
            "level": level,
            "time_increment": time_increment,
            "fields": ",".join(fields)
        }
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url, params=params)
                response.raise_for_status()
                data = response.json()
                return data.get("data", [])
        except Exception as e:
            logger.error(f"Error fetching Facebook insights: {e}")
            return []
    
    async def update_adset_budget(
        self,
        adset_id: str,
        daily_budget: float
    ) -> Dict[str, Any]:
        """Update adset daily budget.
        
        Based on PDF example: Update budget for an adset via API.
        """
        url = f"{self.base_url}/{adset_id}"
        params = {
            "access_token": self.access_token,
            "daily_budget": int(daily_budget * 100)  # Convert to cents
        }
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(url, params=params)
                response.raise_for_status()
                return response.json()
        except Exception as e:
            logger.error(f"Error updating adset budget: {e}")
            raise
    
    async def send_conversion_event(
        self,
        pixel_id: str,
        event_name: str,
        event_id: str,
        value: float,
        currency: str = "USD",
        user_data: Optional[Dict[str, str]] = None,
        custom_data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Send conversion event via Conversions API (CAPI).
        
        Based on PDF example: Send high-quality conversion signals back to Meta.
        """
        url = f"{self.base_url}/{pixel_id}/events"
        params = {"access_token": self.access_token}
        
        event_data = {
            "data": [{
                "event_name": event_name,
                "event_id": event_id,
                "event_time": int(datetime.now().timestamp()),
                "user_data": user_data or {},
                "custom_data": {
                    **(custom_data or {}),
                    "value": value,
                    "currency": currency.upper()
                }
            }]
        }
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(url, params=params, json=event_data)
                response.raise_for_status()
                return response.json()
        except Exception as e:
            logger.error(f"Error sending conversion event: {e}")
            raise
    
    async def get_ad_accounts(self) -> List[Dict[str, Any]]:
        """Get ad accounts."""
        url = f"{self.base_url}/me/adaccounts"
        params = {
            "access_token": self.access_token,
            "fields": "id,name,account_id,currency"
        }
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url, params=params)
                response.raise_for_status()
                data = response.json()
                return data.get("data", [])
        except Exception as e:
            logger.error(f"Error fetching ad accounts: {e}")
            return []
    
    async def create_ad_campaign(
        self,
        account_id: str,
        campaign_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Create a new ad campaign."""
        url = f"{self.base_url}/act_{account_id}/campaigns"
        params = {
            "access_token": self.access_token,
            **campaign_data
        }
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(url, params=params)
                response.raise_for_status()
                return response.json()
        except Exception as e:
            logger.error(f"Error creating campaign: {e}")
            raise
    
    async def get_audiences(
        self,
        account_id: str
    ) -> List[Dict[str, Any]]:
        """Get custom audiences."""
        url = f"{self.base_url}/act_{account_id}/customaudiences"
        params = {
            "access_token": self.access_token,
            "fields": "id,name,subtype,approximate_count"
        }
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url, params=params)
                response.raise_for_status()
                data = response.json()
                return data.get("data", [])
        except Exception as e:
            logger.error(f"Error fetching audiences: {e}")
            return []
    
    async def get_ad_performance(
        self,
        account_id: str,
        campaign_id: Optional[str] = None,
        date_range: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """Get ad performance metrics."""
        if date_range:
            time_range = {
                "since": date_range.get("start_date"),
                "until": date_range.get("end_date")
            }
        else:
            time_range = {"date_preset": "yesterday"}
        
        insights = await self.get_insights(
            account_id=f"act_{account_id}",
            level="campaign" if campaign_id else "account",
            **time_range
        )
        
        if not insights:
            return {
                "impressions": 0,
                "clicks": 0,
                "spend": 0.0,
                "conversions": 0
            }
        
        # Aggregate metrics
        total_impressions = sum(int(i.get("impressions", 0)) for i in insights)
        total_clicks = sum(int(i.get("clicks", 0)) for i in insights)
        total_spend = sum(float(i.get("spend", 0)) for i in insights)
        
        # Extract conversions from actions
        total_conversions = 0
        for insight in insights:
            actions = insight.get("actions", [])
            for action in actions:
                if action.get("action_type") in ["purchase", "lead", "complete_registration"]:
                    total_conversions += int(action.get("value", 0))
        
        return {
            "impressions": total_impressions,
            "clicks": total_clicks,
            "spend": total_spend,
            "conversions": total_conversions
        }
