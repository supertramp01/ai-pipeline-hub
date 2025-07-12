import os
import requests
import logging
from typing import Dict, Any, Optional
from ..configs.settings import get_settings

logger = logging.getLogger(__name__)

class TavilyClient:
    """Client for interacting with Tavily API for company research."""
    
    def __init__(self):
        self.settings = get_settings()
        self.api_key = self.settings.tavily_api_key
        self.base_url = "https://api.tavily.com"
        
        if not self.api_key:
            raise ValueError("TavILY_API_KEY not found in environment variables")
    
    def research_company(self, company_name: Optional[str], website_url: str) -> Dict[str, Any]:
        """
        Research a company using Tavily API.
        
        Args:
            company_name: Optional company name
            website_url: Company website URL
            
        Returns:
            Dictionary containing research results
        """
        try:
            # Construct the search query
            if company_name:
                query = f"Research company: {company_name} - Website: {website_url}"
            else:
                query = f"Research company at website: {website_url}"
            
            payload = {
                "api_key": self.api_key,
                "query": query,
                "search_depth": "advanced",
                "include_answer": True,
                "include_raw_content": True,
                "include_images": False,
                "max_results": 20
            }
            
            logger.info(f"Researching company: {query}")
            
            response = requests.post(
                f"{self.base_url}/search",
                json=payload,
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                logger.info(f"Successfully researched company: {website_url}")
                return result
            else:
                logger.error(f"Tavily API error: {response.status_code} - {response.text}")
                raise Exception(f"Tavily API error: {response.status_code}")
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Request error during company research: {e}")
            raise
        except Exception as e:
            logger.error(f"Error researching company: {e}")
            raise 