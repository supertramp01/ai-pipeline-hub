#!/usr/bin/env python3
"""
Test script for company research functionality.
Tests both API endpoints and direct function calls.
"""

import requests
import json
import sys
import os
from datetime import datetime

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.common.services.company_service import CompanyService
from src.common.utils.tavily_client import TavilyClient
from src.common.utils.company_csv_manager import CompanyCSVManager
from src.common.utils.company_file_manager import CompanyFileManager

# API base URL
API_BASE_URL = "http://localhost:8000"

def test_tavily_client():
    """Test Tavily client directly."""
    print("\n=== Testing Tavily Client ===")
    
    try:
        client = TavilyClient()
        
        # Test with a sample company
        website_url = "https://www.openai.com"
        company_name = "OpenAI"
        
        print(f"Researching company: {company_name} at {website_url}")
        result = client.research_company(company_name, website_url)
        
        print(f"✅ Tavily research successful")
        print(f"   Answer length: {len(result.get('answer', ''))}")
        print(f"   Results count: {len(result.get('results', []))}")
        print(f"   Raw content count: {len(result.get('raw_content', []))}")
        
        return True
        
    except Exception as e:
        print(f"❌ Tavily client test failed: {e}")
        return False

def test_company_service():
    """Test company service directly."""
    print("\n=== Testing Company Service ===")
    
    try:
        service = CompanyService()
        
        # Test company research
        website_url = "https://www.microsoft.com"
        company_name = "Microsoft"
        
        print(f"Researching company: {company_name} at {website_url}")
        result = service.research_company(company_name, website_url)
        
        if result['status'] in ['success', 'created', 'updated']:
            print(f"✅ Company research successful")
            print(f"   Company ID: {result['company_id']}")
            print(f"   Company Name: {result['company_name']}")
            print(f"   Status: {result['status']}")
            
            # Test retrieving the data
            company_id = result['company_id']
            company_data = service.get_company_data(company_id)
            
            if company_data:
                print(f"✅ Company data retrieval successful")
                print(f"   Create date: {company_data['create_date']}")
                print(f"   Last updated: {company_data['last_updated']}")
            else:
                print(f"❌ Company data retrieval failed")
            
            # Test markdown retrieval
            markdown_content = service.get_company_markdown(company_id)
            if markdown_content:
                print(f"✅ Markdown retrieval successful")
                print(f"   Content length: {len(markdown_content)}")
            else:
                print(f"❌ Markdown retrieval failed")
            
            return True
        else:
            print(f"❌ Company research failed: {result['message']}")
            return False
            
    except Exception as e:
        print(f"❌ Company service test failed: {e}")
        return False

def test_company_csv_manager():
    """Test company CSV manager directly."""
    print("\n=== Testing Company CSV Manager ===")
    
    try:
        csv_manager = CompanyCSVManager()
        
        # Test adding a company
        company_id = "test-company-123"
        website_url = "https://www.testcompany.com"
        
        print(f"Adding test company: {company_id}")
        success = csv_manager.add_company(company_id, website_url)
        
        if success:
            print(f"✅ Company added successfully")
            
            # Test retrieving the company
            company_data = csv_manager.get_company(company_id)
            if company_data:
                print(f"✅ Company retrieval successful")
                print(f"   Website: {company_data['company_website']}")
                print(f"   Create date: {company_data['create_date']}")
            
            # Test updating the company
            update_success = csv_manager.update_company(company_id)
            if update_success:
                print(f"✅ Company update successful")
            
            # Test getting all companies
            all_companies = csv_manager.get_all_companies()
            print(f"✅ Retrieved {len(all_companies)} companies")
            
            return True
        else:
            print(f"❌ Company addition failed")
            return False
            
    except Exception as e:
        print(f"❌ CSV manager test failed: {e}")
        return False

def test_company_file_manager():
    """Test company file manager directly."""
    print("\n=== Testing Company File Manager ===")
    
    try:
        file_manager = CompanyFileManager()
        
        # Test data
        company_id = "test-file-company-456"
        test_data = {
            "answer": "This is a test company research answer.",
            "results": [
                {
                    "title": "Test Result 1",
                    "url": "https://example.com/1",
                    "content": "This is test content for result 1."
                },
                {
                    "title": "Test Result 2", 
                    "url": "https://example.com/2",
                    "content": "This is test content for result 2."
                }
            ],
            "raw_content": [
                {
                    "title": "Raw Content 1",
                    "url": "https://example.com/raw1",
                    "content": "Raw content for testing."
                }
            ],
            "search_timestamp": datetime.now().isoformat()
        }
        
        print(f"Saving test data for company: {company_id}")
        success = file_manager.save_company_data(company_id, test_data)
        
        if success:
            print(f"✅ Data saved successfully")
            
            # Test retrieving JSON data
            retrieved_data = file_manager.get_company_data(company_id)
            if retrieved_data:
                print(f"✅ JSON data retrieval successful")
                print(f"   Answer: {retrieved_data['answer']}")
                print(f"   Results count: {len(retrieved_data['results'])}")
            
            # Test retrieving markdown
            markdown_content = file_manager.get_company_markdown(company_id)
            if markdown_content:
                print(f"✅ Markdown retrieval successful")
                print(f"   Content length: {len(markdown_content)}")
            
            # Test checking if data exists
            exists = file_manager.company_data_exists(company_id)
            print(f"✅ Data exists check: {exists}")
            
            return True
        else:
            print(f"❌ Data save failed")
            return False
            
    except Exception as e:
        print(f"❌ File manager test failed: {e}")
        return False

def test_api_endpoints():
    """Test company research API endpoints."""
    print("\n=== Testing API Endpoints ===")
    
    try:
        # Test company research endpoint
        research_data = {
            "website_url": "https://www.apple.com",
            "company_name": "Apple Inc."
        }
        
        print(f"Testing company research API for: {research_data['company_name']}")
        response = requests.post(f"{API_BASE_URL}/api/v1/company/research", json=research_data)
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Company research API successful")
            print(f"   Company ID: {result['company_id']}")
            print(f"   Status: {result['status']}")
            
            company_id = result['company_id']
            
            # Test getting company data
            print(f"Testing get company data API")
            response = requests.get(f"{API_BASE_URL}/api/v1/company/{company_id}")
            
            if response.status_code == 200:
                company_data = response.json()
                print(f"✅ Get company data API successful")
                print(f"   Website: {company_data['company_website']}")
                print(f"   Create date: {company_data['create_date']}")
            else:
                print(f"❌ Get company data API failed: {response.status_code}")
            
            # Test getting company JSON
            print(f"Testing get company JSON API")
            response = requests.get(f"{API_BASE_URL}/api/v1/company/{company_id}/json")
            
            if response.status_code == 200:
                json_data = response.json()
                print(f"✅ Get company JSON API successful")
                print(f"   Research data keys: {list(json_data['research_data'].keys())}")
            else:
                print(f"❌ Get company JSON API failed: {response.status_code}")
            
            # Test getting company markdown
            print(f"Testing get company markdown API")
            response = requests.get(f"{API_BASE_URL}/api/v1/company/{company_id}/markdown")
            
            if response.status_code == 200:
                markdown_data = response.json()
                print(f"✅ Get company markdown API successful")
                print(f"   Content length: {len(markdown_data['content'])}")
            else:
                print(f"❌ Get company markdown API failed: {response.status_code}")
            
            # Test listing companies
            print(f"Testing list companies API")
            response = requests.get(f"{API_BASE_URL}/api/v1/company/list")
            
            if response.status_code == 200:
                companies = response.json()
                print(f"✅ List companies API successful")
                print(f"   Companies count: {len(companies)}")
            else:
                print(f"❌ List companies API failed: {response.status_code}")
            
            return True
        else:
            print(f"❌ Company research API failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print(f"❌ API connection failed. Make sure the server is running on {API_BASE_URL}")
        return False
    except Exception as e:
        print(f"❌ API test failed: {e}")
        return False

def main():
    """Run all tests."""
    print("🚀 Starting Company Research Tests")
    print("=" * 50)
    
    # Test individual components
    tests = [
        ("Tavily Client", test_tavily_client),
        ("Company CSV Manager", test_company_csv_manager),
        ("Company File Manager", test_company_file_manager),
        ("Company Service", test_company_service),
        ("API Endpoints", test_api_endpoints)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} test crashed: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Results Summary")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed!")
        return 0
    else:
        print("⚠️  Some tests failed. Check the output above for details.")
        return 1

if __name__ == "__main__":
    exit(main()) 