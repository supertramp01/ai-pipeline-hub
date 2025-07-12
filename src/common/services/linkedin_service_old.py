from apify_client import ApifyClient
from typing import Optional, Tuple, Dict, Any
from dotenv import load_dotenv
import os
load_dotenv()

# Initialize the ApifyClient with your API token
client = ApifyClient(os.getenv("APIFY_API_TOKEN"))
actor_id = os.getenv("APIFY_ACTOR_ID")

def fetch_linkedin_profile(linkedin_profile_url: str, db_service, company_id: Optional[int] = None, ) -> Tuple[bool, Optional[Dict[str, Any]]]:
    # Prepare the Actor input
    run_input = {
        "profileUrls": [linkedin_profile_url]
    }

    # Run the Actor and wait for it to finish
    run = client.actor(actor_id).call(run_input=run_input)

    # Fetch and store Actor results
    for item in client.dataset(run["defaultDatasetId"]).iterate_items():
        # Store each profile data in the database
        db_service.create_research_professional(
            source="linkedin",
            content=item,
            company_id=company_id
        )
    # Check if we have any results
    if not client.dataset(run["defaultDatasetId"]).list_items().items:
        return False, None
    
    # Get the first profile data (since we're only requesting one URL)
    profile_data = next(client.dataset(run["defaultDatasetId"]).iterate_items())
    
    # Return success status and the profile data
    return True, profile_data

def scrape_profile(linkedin_profile_url: str) -> Optional[Dict[str, Any]]:
    """
    Fetch LinkedIn profile data without storing it in the database.
    Returns the profile data if successful, None if failed.
    """
    try:
        # Prepare the Actor input
        run_input = {
            "profileUrls": [linkedin_profile_url]
        }

        # Run the Actor and wait for it to finish
        run = client.actor(actor_id).call(run_input=run_input)

        # Check if we have any results
        if not client.dataset(run["defaultDatasetId"]).list_items().items:
            return None
        
        # Get the first profile data (since we're only requesting one URL)
        profile_data = next(client.dataset(run["defaultDatasetId"]).iterate_items())
        
        return profile_data
        
    except Exception as e:
        print(f"Error scraping LinkedIn profile: {str(e)}")
        return None
    