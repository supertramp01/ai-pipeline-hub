from typing import Dict, Optional, Tuple
from src.common.utils.apify_client import ApifyClient
from src.common.utils.csv_manager import CSVManager
from src.common.utils.file_manager import FileManager
from src.common.utils.logger import setup_logger

logger = setup_logger(__name__)

class LinkedInService:
    def __init__(self):
        self.apify_client = ApifyClient()
        self.csv_manager = CSVManager()
        self.file_manager = FileManager()
    
    def scrape_and_store_profile(self, linkedin_url: str, return_full_object: bool = True) -> Tuple[bool, Dict]:
        """
        Scrape LinkedIn profile and store the data.
        
        Args:
            linkedin_url: The LinkedIn profile URL to scrape
            return_full_object: Whether to return the entire profile object (default: True)
            
        Returns:
            Tuple of (success: bool, response_data: Dict)
        """
        try:
            logger.info(f"Starting LinkedIn profile scraping pipeline for: {linkedin_url}")
            
            # Check if profile already exists
            existing_user = self.csv_manager.find_user_by_linkedin_url(linkedin_url)
            
            # Scrape the profile
            profile_data = self.apify_client.scrape_linkedin_profile(linkedin_url)
            if not profile_data:
                return False, {"error": "Failed to scrape LinkedIn profile"}
            
            # Extract comprehensive information
            name = self._extract_name(profile_data)
            company = self._extract_company(profile_data)
            
            if existing_user:
                # Update existing user
                user_id = int(existing_user['user_id'])
                self.csv_manager.update_user(user_id, name, company, linkedin_url)
                logger.info(f"Updated existing user profile for: {name}")
            else:
                # Add new user
                user_id = self.csv_manager.add_user(name, company, linkedin_url)
                logger.info(f"Added new user profile for: {name}")
            
            # Save profile data
            success = self.file_manager.save_linkedin_profile(user_id, profile_data)
            if not success:
                return False, {"error": "Failed to save profile data"}
            
            # Create response data
            response_data = {
                "user_id": user_id,
                "name": name,
                "company": company,
                "linkedin_url": linkedin_url,
                "status": "updated" if existing_user else "created",
                "profile_summary": self._create_profile_summary(profile_data)
            }
            
            # Add full profile object if requested
            if return_full_object:
                response_data["full_profile"] = profile_data
                logger.info(f"Including full profile object in response for user {user_id}")
            
            logger.info(f"Successfully completed LinkedIn profile pipeline for user {user_id}")
            return True, response_data
            
        except Exception as e:
            logger.error(f"Error in LinkedIn profile pipeline: {str(e)}")
            return False, {"error": str(e)}
    
    def _extract_name(self, profile_data: Dict) -> str:
        """Extract the person's name from profile data."""
        # Try different possible name fields (Apify LinkedIn actor format)
        name_fields = ['fullName', 'name', 'firstName', 'lastName']
        
        for field in name_fields:
            if profile_data.get(field):
                return profile_data[field]
        
        # If no direct name field, try to construct from first and last name
        first_name = profile_data.get('firstName', '')
        last_name = profile_data.get('lastName', '')
        if first_name or last_name:
            return f"{first_name} {last_name}".strip()
        
        return "Unknown"
    
    def _extract_company(self, profile_data: Dict) -> str:
        """Extract the current company from profile data."""
        # Try different possible company fields (Apify LinkedIn actor format)
        company_fields = ['companyName', 'company', 'current_company', 'employer', 'organization']
        
        for field in company_fields:
            if profile_data.get(field):
                return profile_data[field]
        
        # Try to extract from experience if available
        if profile_data.get('experiences'):
            for exp in profile_data['experiences']:
                if exp.get('companyName') or exp.get('company'):
                    return exp.get('companyName') or exp.get('company')
        
        # Try to extract from headline
        headline = profile_data.get('headline', '')
        if headline and ' at ' in headline:
            company_part = headline.split(' at ')[-1]
            if company_part and company_part != headline:
                return company_part
        
        return "Unknown"
    
    def _create_profile_summary(self, profile_data: Dict) -> Dict:
        """Create a summary of the profile data for quick reference."""
        summary = {
            "basic_info": {},
            "experience_count": 0,
            "education_count": 0,
            "skills_count": 0,
            "certifications_count": 0,
            "languages_count": 0
        }
        
        # Basic information
        summary["basic_info"]["name"] = self._extract_name(profile_data)
        summary["basic_info"]["headline"] = profile_data.get('headline', 'N/A')
        summary["basic_info"]["company"] = self._extract_company(profile_data)
        summary["basic_info"]["location"] = profile_data.get('addressWithCountry', 'N/A')
        summary["basic_info"]["industry"] = profile_data.get('companyIndustry', 'N/A')
        
        # Counts
        if profile_data.get('experiences'):
            summary["experience_count"] = len(profile_data['experiences'])
        
        if profile_data.get('educations'):
            summary["education_count"] = len(profile_data['educations'])
        
        if profile_data.get('skills'):
            summary["skills_count"] = len(profile_data['skills'])
        
        if profile_data.get('licenseAndCertificates'):
            summary["certifications_count"] = len(profile_data['licenseAndCertificates'])
        
        if profile_data.get('languages'):
            summary["languages_count"] = len(profile_data['languages'])
        
        return summary
    
    def get_profile(self, user_id: int) -> Optional[str]:
        """
        Get LinkedIn profile data for a user.
        
        Args:
            user_id: The user ID to retrieve profile for
            
        Returns:
            Markdown content or None if not found
        """
        return self.file_manager.get_linkedin_profile(user_id)
    
    def get_all_users(self) -> list:
        """
        Get all users from the CSV file.
        
        Returns:
            List of user dictionaries
        """
        return self.csv_manager.get_all_users()
    
    def get_profile_summary(self, user_id: int) -> Optional[Dict]:
        """
        Get a summary of the LinkedIn profile data for a user.
        
        Args:
            user_id: The user ID to retrieve profile summary for
            
        Returns:
            Profile summary dictionary or None if not found
        """
        try:
            # Get the raw JSON data
            json_path = f"{self.file_manager.base_dir}/{user_id}/profile.json"
            import json
            import os
            
            if not os.path.exists(json_path):
                return None
            
            with open(json_path, 'r', encoding='utf-8') as file:
                profile_data = json.load(file)
            
            return self._create_profile_summary(profile_data)
            
        except Exception as e:
            logger.error(f"Error getting profile summary for user {user_id}: {str(e)}")
            return None 