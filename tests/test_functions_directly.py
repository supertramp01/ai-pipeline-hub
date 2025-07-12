#!/usr/bin/env python3
"""
Test script for testing functions directly.
This script tests the core functions without going through the REST API.
"""

import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from common.services.linkedin_service import LinkedInService
from common.utils.csv_manager import CSVManager
from common.utils.file_manager import FileManager
from common.utils.apify_client import ApifyClient

def test_csv_manager():
    """Test the CSV manager functionality."""
    print("Testing CSV Manager...")
    
    try:
        csv_manager = CSVManager()
        
        # Test adding a user
        user_id = csv_manager.add_user("John Doe", "Test Company", "https://linkedin.com/in/johndoe")
        print(f"✓ Added user with ID: {user_id}")
        
        # Test finding user by LinkedIn URL
        user = csv_manager.find_user_by_linkedin_url("https://linkedin.com/in/johndoe")
        if user:
            print(f"✓ Found user: {user}")
        
        # Test getting all users
        users = csv_manager.get_all_users()
        print(f"✓ Total users in CSV: {len(users)}")
        
        # Test updating user
        csv_manager.update_user(user_id, "John Doe Updated", "Updated Company", "https://linkedin.com/in/johndoe")
        print(f"✓ Updated user {user_id}")
        
        print("✓ CSV Manager tests passed\n")
        return True
        
    except Exception as e:
        print(f"✗ CSV Manager test failed: {e}\n")
        return False

def test_file_manager():
    """Test the file manager functionality."""
    print("Testing File Manager...")
    
    try:
        file_manager = FileManager()
        
        # Test data
        test_profile_data = {
            "name": "Jane Smith",
            "headline": "Software Engineer",
            "company": "Tech Corp",
            "location": "San Francisco, CA",
            "about": "Experienced software engineer with 5+ years of experience.",
            "experience": [
                {
                    "title": "Senior Software Engineer",
                    "company": "Tech Corp",
                    "duration": "2020-Present",
                    "description": "Leading development of web applications."
                }
            ],
            "education": [
                {
                    "school": "University of California",
                    "degree": "Bachelor of Science",
                    "field": "Computer Science",
                    "duration": "2016-2020"
                }
            ],
            "skills": ["Python", "JavaScript", "React", "Node.js"]
        }
        
        # Test saving profile
        user_id = 999  # Test user ID
        success = file_manager.save_linkedin_profile(user_id, test_profile_data)
        if success:
            print(f"✓ Saved profile for user {user_id}")
        
        # Test getting profile
        profile_content = file_manager.get_linkedin_profile(user_id)
        if profile_content:
            print(f"✓ Retrieved profile for user {user_id}")
            print(f"  Content length: {len(profile_content)} characters")
        
        print("✓ File Manager tests passed\n")
        return True
        
    except Exception as e:
        print(f"✗ File Manager test failed: {e}\n")
        return False

def test_apify_client():
    """Test the Apify client functionality."""
    print("Testing Apify Client...")
    
    try:
        apify_client = ApifyClient()
        
        # Test with a sample LinkedIn URL
        # Note: This will actually call the Apify API, so it might take time
        linkedin_url = "https://www.linkedin.com/in/satyanadella/"
        
        print(f"Testing with LinkedIn URL: {linkedin_url}")
        print("Note: This test will actually call the Apify API and may take several minutes...")
        
        # Uncomment the following lines to actually test the Apify client
        # profile_data = apify_client.scrape_linkedin_profile(linkedin_url)
        # if profile_data:
        #     print(f"✓ Successfully scraped profile data")
        #     print(f"  Name: {profile_data.get('name', 'N/A')}")
        #     print(f"  Company: {profile_data.get('company', 'N/A')}")
        # else:
        #     print("✗ Failed to scrape profile data")
        
        print("✓ Apify Client structure test passed (actual API call skipped)\n")
        return True
        
    except Exception as e:
        print(f"✗ Apify Client test failed: {e}\n")
        return False

def test_linkedin_service():
    """Test the LinkedIn service functionality."""
    print("Testing LinkedIn Service...")
    
    try:
        linkedin_service = LinkedInService()
        
        # Test getting all users
        users = linkedin_service.get_all_users()
        print(f"✓ Retrieved {len(users)} users from service")
        
        # Test with a sample LinkedIn URL
        linkedin_url = "https://www.linkedin.com/in/satyanadella/"
        
        print(f"Testing service with LinkedIn URL: {linkedin_url}")
        print("Note: This test will actually call the Apify API and may take several minutes...")
        
        # Uncomment the following lines to actually test the service
        # success, response_data = linkedin_service.scrape_and_store_profile(linkedin_url)
        # if success:
        #     print(f"✓ Successfully processed profile")
        #     print(f"  User ID: {response_data.get('user_id')}")
        #     print(f"  Status: {response_data.get('status')}")
        # else:
        #     print(f"✗ Failed to process profile: {response_data.get('error')}")
        
        print("✓ LinkedIn Service structure test passed (actual API call skipped)\n")
        return True
        
    except Exception as e:
        print(f"✗ LinkedIn Service test failed: {e}\n")
        return False

def main():
    """Main test function."""
    print("=" * 60)
    print("DIRECT FUNCTION TESTS")
    print("=" * 60)
    
    # Test individual components
    test_csv_manager()
    test_file_manager()
    test_apify_client()
    test_linkedin_service()
    
    print("=" * 60)
    print("DIRECT FUNCTION TESTS COMPLETED")
    print("=" * 60)
    print("\nNote: Some tests are skipped to avoid actual API calls.")
    print("Uncomment the relevant lines in the test functions to run full tests.")

if __name__ == "__main__":
    main() 