import requests
import json
import time
from typing import Dict, Optional
from ..configs.settings import get_settings
from .logger import setup_logger
from apify_client import ApifyClient as OfficialApifyClient

logger = setup_logger(__name__)

class ApifyClient:
    def __init__(self):
        settings = get_settings()
        self.api_token = settings.apify_api_token
        self.actor_id = settings.apify_actor_id
        
        if not self.actor_id or not self.api_token:
            raise ValueError("APIFY_ACTOR_ID and APIFY_API_TOKEN must be set in environment variables")
        
        # Initialize the official Apify client
        self.client = OfficialApifyClient(self.api_token)
    
    def scrape_linkedin_profile(self, linkedin_url: str) -> Optional[Dict]:
        """
        Scrape LinkedIn profile using Apify actor.
        
        Args:
            linkedin_url: The LinkedIn profile URL to scrape
            
        Returns:
            Dictionary containing the scraped profile data or None if failed
        """
        try:
            logger.info(f"Starting LinkedIn profile scrape for: {linkedin_url}")
            
            # Prepare the Actor input
            run_input = {
                "profileUrls": [linkedin_url]
            }
            
            # Run the Actor and wait for it to finish
            run = self.client.actor(self.actor_id).call(run_input=run_input)
            
            logger.info(f"Apify run completed with ID: {run.get('id')}")
            
            # Check if we have any results
            if not self.client.dataset(run["defaultDatasetId"]).list_items().items:
                logger.warning("No results found in the dataset")
                return None
            
            # Get the first profile data (since we're only requesting one URL)
            profile_data = next(self.client.dataset(run["defaultDatasetId"]).iterate_items())
            
            logger.info(f"Successfully scraped LinkedIn profile for: {linkedin_url}")
            return profile_data
            
        except Exception as e:
            logger.error(f"Error scraping LinkedIn profile: {str(e)}")
            return None 