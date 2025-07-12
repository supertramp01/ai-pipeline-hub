#!/usr/bin/env python3
"""
Test script for company summary functionality.
Tests both API endpoints and direct function calls.
"""

import requests
import json
import sys
import os
from datetime import datetime

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.common.services.company_summary_service import CompanySummaryService
from src.common.services.company_service import CompanyService

# API base URL
API_BASE_URL = "http://localhost:8000"

def test_company_summary_service():
    """Test company summary service directly."""
    print("\n=== Testing Company Summary Service ===")
    
    try:
        summary_service = CompanySummaryService()
        company_service = CompanyService()
        
        # First, ensure we have a company to work with
        website_url = "https://www.google.com"
        company_name = "Google"
        
        print(f"Ensuring company exists: {company_name}")
        research_result = company_service.research_company(company_name, website_url)
        
        if research_result['status'] not in ['success', 'created', 'updated']:
            print(f"❌ Company research failed: {research_result['message']}")
            return False
        
        company_id = research_result['company_id']
        print(f"✅ Company ready: {company_id}")
        
        # Test summary generation without user prompt
        print(f"Testing summary generation without user prompt")
        result = summary_service.generate_summary(company_id=company_id)
        
        if result['status'] == 'success':
            print(f"✅ Summary generation successful")
            print(f"   Company ID: {result['company_id']}")
            print(f"   Statistics count: {len(result['summary'].get('key_statistics', []))}")
            print(f"   Recent news count: {len(result['summary'].get('recent_news', []))}")
            print(f"   Facts count: {len(result['summary'].get('facts', []))}")
        else:
            print(f"❌ Summary generation failed: {result['message']}")
            return False
        
        # Test summary generation with user prompt
        user_prompt = "Focus on financial performance and recent developments"
        print(f"Testing summary generation with user prompt: '{user_prompt}'")
        result_with_prompt = summary_service.generate_summary(
            company_id=company_id, 
            user_prompt=user_prompt
        )
        
        if result_with_prompt['status'] == 'success':
            print(f"✅ Summary generation with prompt successful")
            print(f"   User prompt: {result_with_prompt['summary'].get('user_prompt')}")
        else:
            print(f"❌ Summary generation with prompt failed: {result_with_prompt['message']}")
            return False
        
        # Test summary retrieval
        print(f"Testing summary retrieval")
        retrieved_summary = summary_service.get_summary(company_id=company_id)
        
        if retrieved_summary:
            print(f"✅ Summary retrieval successful")
            print(f"   Generated at: {retrieved_summary.get('generated_at')}")
        else:
            print(f"❌ Summary retrieval failed")
            return False
        
        # Test summary retrieval by website
        print(f"Testing summary retrieval by website")
        retrieved_by_website = summary_service.get_summary(company_website=website_url)
        
        if retrieved_by_website:
            print(f"✅ Summary retrieval by website successful")
        else:
            print(f"❌ Summary retrieval by website failed")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Company summary service test failed: {e}")
        return False

def test_api_endpoints():
    """Test company summary API endpoints."""
    print("\n=== Testing API Endpoints ===")
    
    try:
        # Test summary generation endpoint
        summary_request = {
            "company_website": "https://www.microsoft.com",
            "user_prompt": "Focus on technology innovations and market position"
        }
        
        print(f"Testing summary generation API for: {summary_request['company_website']}")
        response = requests.post(f"{API_BASE_URL}/api/v1/company/summary/generate", json=summary_request)
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Summary generation API successful")
            print(f"   Company ID: {result['company_id']}")
            print(f"   Status: {result['status']}")
            
            company_id = result['company_id']
            
            # Test getting summary by company ID
            print(f"Testing get summary by company ID API")
            response = requests.get(f"{API_BASE_URL}/api/v1/company/summary/{company_id}")
            
            if response.status_code == 200:
                summary_data = response.json()
                print(f"✅ Get summary by company ID API successful")
                print(f"   Summary keys: {list(summary_data['summary'].keys())}")
            else:
                print(f"❌ Get summary by company ID API failed: {response.status_code}")
            
            # Test getting summary by website
            print(f"Testing get summary by website API")
            website_url = summary_request['company_website']
            response = requests.get(f"{API_BASE_URL}/api/v1/company/summary/website/{website_url}")
            
            if response.status_code == 200:
                summary_data = response.json()
                print(f"✅ Get summary by website API successful")
                print(f"   Website: {summary_data['website_url']}")
            else:
                print(f"❌ Get summary by website API failed: {response.status_code}")
            
            return True
        else:
            print(f"❌ Summary generation API failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print(f"❌ API connection failed. Make sure the server is running on {API_BASE_URL}")
        return False
    except Exception as e:
        print(f"❌ API test failed: {e}")
        return False

def test_summary_content():
    """Test the quality and structure of generated summaries."""
    print("\n=== Testing Summary Content Quality ===")
    
    try:
        summary_service = CompanySummaryService()
        company_service = CompanyService()
        
        # Test with a well-known company
        website_url = "https://www.apple.com"
        company_name = "Apple"
        
        print(f"Testing summary content for: {company_name}")
        
        # Ensure company exists
        research_result = company_service.research_company(company_name, website_url)
        if research_result['status'] not in ['success', 'created', 'updated']:
            print(f"❌ Company research failed: {research_result['message']}")
            return False
        
        company_id = research_result['company_id']
        
        # Generate summary
        result = summary_service.generate_summary(company_id=company_id)
        
        if result['status'] != 'success':
            print(f"❌ Summary generation failed: {result['message']}")
            return False
        
        summary = result['summary']
        
        # Check summary structure
        required_fields = [
            'generated_at', 'company_overview', 'key_statistics', 
            'recent_news', 'facts', 'products_services'
        ]
        
        missing_fields = []
        for field in required_fields:
            if not summary.get(field):
                missing_fields.append(field)
        
        if missing_fields:
            print(f"❌ Missing required fields: {missing_fields}")
            return False
        
        print(f"✅ Summary structure validation passed")
        
        # Check content quality
        if len(summary['company_overview']) > 50:
            print(f"✅ Company overview has substantial content")
        else:
            print(f"⚠️  Company overview seems short")
        
        if len(summary['key_statistics']) > 0:
            print(f"✅ Found {len(summary['key_statistics'])} key statistics")
        else:
            print(f"⚠️  No key statistics found")
        
        if len(summary['recent_news']) > 0:
            print(f"✅ Found {len(summary['recent_news'])} recent news items")
        else:
            print(f"⚠️  No recent news found")
        
        if len(summary['facts']) > 0:
            print(f"✅ Found {len(summary['facts'])} key facts")
        else:
            print(f"⚠️  No key facts found")
        
        return True
        
    except Exception as e:
        print(f"❌ Summary content test failed: {e}")
        return False

def main():
    """Run all tests."""
    print("🚀 Starting Company Summary Tests")
    print("=" * 50)
    
    # Test individual components
    tests = [
        ("Company Summary Service", test_company_summary_service),
        ("Summary Content Quality", test_summary_content),
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