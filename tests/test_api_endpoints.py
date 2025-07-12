#!/usr/bin/env python3
"""
Test script for API endpoints.
This script tests the REST API endpoints using simple Python requests.
"""

import requests
import json
import time

# API base URL
BASE_URL = "http://localhost:8000"

def test_health_check():
    """Test the health check endpoint."""
    print("Testing health check endpoint...")
    
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        print("✓ Health check passed\n")
        return True
    except Exception as e:
        print(f"✗ Health check failed: {e}\n")
        return False

def test_root_endpoint():
    """Test the root endpoint."""
    print("Testing root endpoint...")
    
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        print("✓ Root endpoint passed\n")
        return True
    except Exception as e:
        print(f"✗ Root endpoint failed: {e}\n")
        return False

def test_scrape_linkedin_profile(linkedin_url):
    """Test the LinkedIn profile scraping endpoint."""
    print(f"Testing LinkedIn profile scraping for: {linkedin_url}")
    
    try:
        payload = {"linkedin_url": linkedin_url}
        response = requests.post(f"{BASE_URL}/api/v1/linkedin/scrape", json=payload)
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"Response: {json.dumps(result, indent=2)}")
            print("✓ LinkedIn profile scraping passed\n")
            return result.get("user_id")
        else:
            print(f"Response: {response.text}")
            print("✗ LinkedIn profile scraping failed\n")
            return None
            
    except Exception as e:
        print(f"✗ LinkedIn profile scraping failed: {e}\n")
        return None

def test_get_linkedin_profile(user_id):
    """Test the get LinkedIn profile endpoint."""
    print(f"Testing get LinkedIn profile for user ID: {user_id}")
    
    try:
        response = requests.get(f"{BASE_URL}/api/v1/linkedin/profile/{user_id}")
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"User ID: {result.get('user_id')}")
            print(f"Format: {result.get('format')}")
            print(f"Profile content length: {len(result.get('profile_content', ''))} characters")
            print("✓ Get LinkedIn profile passed\n")
            return True
        else:
            print(f"Response: {response.text}")
            print("✗ Get LinkedIn profile failed\n")
            return False
            
    except Exception as e:
        print(f"✗ Get LinkedIn profile failed: {e}\n")
        return False

def test_get_linkedin_profile_summary(user_id):
    """Test the get LinkedIn profile summary endpoint."""
    print(f"Testing get LinkedIn profile summary for user ID: {user_id}")
    
    try:
        response = requests.get(f"{BASE_URL}/api/v1/linkedin/profile/{user_id}/summary")
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"Profile Summary:")
            print(f"  Name: {result.get('basic_info', {}).get('name', 'N/A')}")
            print(f"  Company: {result.get('basic_info', {}).get('company', 'N/A')}")
            print(f"  Experience Count: {result.get('experience_count', 0)}")
            print(f"  Education Count: {result.get('education_count', 0)}")
            print(f"  Skills Count: {result.get('skills_count', 0)}")
            print(f"  Certifications Count: {result.get('certifications_count', 0)}")
            print(f"  Languages Count: {result.get('languages_count', 0)}")
            print("✓ Get LinkedIn profile summary passed\n")
            return True
        else:
            print(f"Response: {response.text}")
            print("✗ Get LinkedIn profile summary failed\n")
            return False
            
    except Exception as e:
        print(f"✗ Get LinkedIn profile summary failed: {e}\n")
        return False

def test_list_users():
    """Test the list users endpoint."""
    print("Testing list users endpoint...")
    
    try:
        response = requests.get(f"{BASE_URL}/api/v1/linkedin/users")
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            users = response.json()
            print(f"Number of users: {len(users)}")
            for user in users:
                print(f"  - User ID: {user.get('user_id')}, Name: {user.get('name')}, Company: {user.get('company')}")
            print("✓ List users passed\n")
            return True
        else:
            print(f"Response: {response.text}")
            print("✗ List users failed\n")
            return False
            
    except Exception as e:
        print(f"✗ List users failed: {e}\n")
        return False

def main():
    """Main test function."""
    print("=" * 60)
    print("API ENDPOINT TESTS")
    print("=" * 60)
    
    # Test basic endpoints
    test_health_check()
    test_root_endpoint()
    
    # Test LinkedIn profile scraping
    # Note: Replace with a real LinkedIn URL for testing
    linkedin_url = "https://www.linkedin.com/in/satyanadella/"
    user_id = test_scrape_linkedin_profile(linkedin_url)
    
    if user_id:
        # Test getting the profile
        test_get_linkedin_profile(user_id)
        
        # Test getting the profile summary
        test_get_linkedin_profile_summary(user_id)
    
    # Test listing all users
    test_list_users()
    
    print("=" * 60)
    print("TEST COMPLETED")
    print("=" * 60)

if __name__ == "__main__":
    main() 