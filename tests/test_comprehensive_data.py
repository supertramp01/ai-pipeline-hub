#!/usr/bin/env python3
"""
Test script with comprehensive LinkedIn profile data.
This script demonstrates all possible fields that could be extracted from the Apify LinkedIn actor.
"""

import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from common.services.linkedin_service import LinkedInService
from common.utils.file_manager import FileManager

def test_comprehensive_linkedin_data():
    """Test with comprehensive LinkedIn profile data."""
    print("Testing Comprehensive LinkedIn Data Processing...")
    
    # Comprehensive LinkedIn profile data that could be returned by Apify actor
    comprehensive_profile_data = {
        # Basic Information
        "name": "John Smith",
        "first_name": "John",
        "last_name": "Smith",
        "headline": "Senior Software Engineer at TechCorp",
        "company": "TechCorp",
        "current_company": "TechCorp",
        "location": "San Francisco, CA",
        "industry": "Technology",
        "summary": "Experienced software engineer with 8+ years in web development.",
        
        # Contact Information
        "email": "john.smith@techcorp.com",
        "phone": "+1-555-123-4567",
        "website": "https://johnsmith.dev",
        "twitter": "@johnsmith",
        
        # About Section
        "about": "I'm a passionate software engineer with expertise in Python, JavaScript, and cloud technologies. I love building scalable applications and mentoring junior developers.",
        
        # Experience
        "experience": [
            {
                "title": "Senior Software Engineer",
                "company": "TechCorp",
                "duration": "2020-Present",
                "location": "San Francisco, CA",
                "description": "Leading development of microservices architecture. Mentoring junior developers and implementing best practices.",
                "start_date": "2020-01",
                "end_date": None
            },
            {
                "title": "Software Engineer",
                "company": "StartupXYZ",
                "duration": "2018-2020",
                "location": "San Francisco, CA",
                "description": "Developed full-stack web applications using React and Node.js.",
                "start_date": "2018-03",
                "end_date": "2020-01"
            },
            {
                "title": "Junior Developer",
                "company": "BigTech Inc",
                "duration": "2016-2018",
                "location": "Seattle, WA",
                "description": "Worked on internal tools and automation scripts.",
                "start_date": "2016-06",
                "end_date": "2018-03"
            }
        ],
        
        # Education
        "education": [
            {
                "school": "Stanford University",
                "degree": "Master of Science",
                "field": "Computer Science",
                "duration": "2014-2016",
                "start_date": "2014-09",
                "end_date": "2016-06",
                "grade": "3.9/4.0"
            },
            {
                "school": "University of California, Berkeley",
                "degree": "Bachelor of Science",
                "field": "Computer Science",
                "duration": "2010-2014",
                "start_date": "2010-09",
                "end_date": "2014-06",
                "grade": "3.8/4.0"
            }
        ],
        
        # Skills
        "skills": [
            {
                "name": "Python",
                "endorsements": "45"
            },
            {
                "name": "JavaScript",
                "endorsements": "38"
            },
            {
                "name": "React",
                "endorsements": "32"
            },
            {
                "name": "Node.js",
                "endorsements": "28"
            },
            {
                "name": "AWS",
                "endorsements": "25"
            },
            {
                "name": "Docker",
                "endorsements": "22"
            },
            {
                "name": "Kubernetes",
                "endorsements": "18"
            },
            {
                "name": "MongoDB",
                "endorsements": "15"
            }
        ],
        
        # Certifications
        "certifications": [
            {
                "name": "AWS Certified Solutions Architect",
                "issuing_organization": "Amazon Web Services",
                "issue_date": "2021-03",
                "expiration_date": "2024-03",
                "credential_id": "AWS-123456"
            },
            {
                "name": "Google Cloud Professional Developer",
                "issuing_organization": "Google",
                "issue_date": "2020-08",
                "expiration_date": "2023-08",
                "credential_id": "GCP-789012"
            }
        ],
        
        # Languages
        "languages": [
            {
                "name": "English",
                "proficiency": "Native"
            },
            {
                "name": "Spanish",
                "proficiency": "Professional"
            },
            {
                "name": "French",
                "proficiency": "Conversational"
            }
        ],
        
        # Volunteer Experience
        "volunteer_experience": [
            {
                "title": "Mentor",
                "organization": "Code.org",
                "duration": "2019-Present",
                "description": "Teaching programming to high school students."
            },
            {
                "title": "Board Member",
                "organization": "Local Tech Community",
                "duration": "2020-Present",
                "description": "Organizing tech meetups and workshops."
            }
        ],
        
        # Publications
        "publications": [
            {
                "title": "Microservices Best Practices",
                "publisher": "TechCorp Blog",
                "date": "2022-01",
                "description": "A comprehensive guide to building scalable microservices."
            },
            {
                "title": "React Performance Optimization",
                "publisher": "Medium",
                "date": "2021-06",
                "description": "Techniques for optimizing React application performance."
            }
        ],
        
        # Patents
        "patents": [
            {
                "title": "System for Automated Code Review",
                "patent_office": "USPTO",
                "issue_date": "2021-12",
                "patent_number": "US12345678"
            }
        ],
        
        # Courses
        "courses": [
            "Advanced Algorithms and Data Structures",
            "Machine Learning Fundamentals",
            "Distributed Systems",
            "Software Architecture Patterns"
        ],
        
        # Projects
        "projects": [
            {
                "title": "Open Source Library",
                "description": "A popular Python library for data processing with 1000+ stars on GitHub.",
                "url": "https://github.com/johnsmith/awesome-lib"
            },
            {
                "title": "Personal Blog",
                "description": "Technical blog covering software engineering topics.",
                "url": "https://johnsmith.dev/blog"
            }
        ],
        
        # Honors & Awards
        "honors_awards": [
            {
                "title": "Employee of the Year",
                "issuer": "TechCorp",
                "date": "2022-12",
                "description": "Recognized for outstanding contributions to the engineering team."
            },
            {
                "title": "Best Paper Award",
                "issuer": "IEEE Conference",
                "date": "2021-10",
                "description": "Awarded for research on distributed systems."
            }
        ],
        
        # Organizations
        "organizations": [
            {
                "name": "ACM",
                "role": "Member",
                "duration": "2014-Present"
            },
            {
                "name": "IEEE",
                "role": "Senior Member",
                "duration": "2018-Present"
            }
        ],
        
        # Test Scores
        "test_scores": [
            {
                "name": "GRE",
                "score": "330/340",
                "date": "2014"
            },
            {
                "name": "TOEFL",
                "score": "115/120",
                "date": "2014"
            }
        ],
        
        # Causes
        "causes": [
            "Education",
            "Technology",
            "Environmental Protection",
            "Social Justice"
        ],
        
        # Additional fields that might be present
        "profile_url": "https://linkedin.com/in/johnsmith",
        "profile_picture": "https://media.licdn.com/dms/image/...",
        "connection_count": "500+",
        "follower_count": "1200",
        "recommendations_count": 15,
        "endorsements_count": 200,
        "public_profile": True,
        "premium_member": False,
        "last_updated": "2023-12-01T10:30:00Z"
    }
    
    try:
        # Test the file manager with comprehensive data
        file_manager = FileManager()
        test_user_id = 9999
        
        # Save the comprehensive profile
        success = file_manager.save_linkedin_profile(test_user_id, comprehensive_profile_data)
        if success:
            print(f"✓ Saved comprehensive profile for user {test_user_id}")
        
        # Retrieve and display the markdown content
        profile_content = file_manager.get_linkedin_profile(test_user_id)
        if profile_content:
            print(f"✓ Retrieved comprehensive profile for user {test_user_id}")
            print(f"  Content length: {len(profile_content)} characters")
            
            # Show a preview of the content
            lines = profile_content.split('\n')
            print("\nProfile Preview (first 20 lines):")
            for i, line in enumerate(lines[:20]):
                print(f"  {i+1:2d}: {line}")
            if len(lines) > 20:
                print(f"  ... and {len(lines) - 20} more lines")
        
        # Test the LinkedIn service with comprehensive data
        linkedin_service = LinkedInService()
        
        # Test name extraction
        extracted_name = linkedin_service._extract_name(comprehensive_profile_data)
        print(f"\n✓ Extracted name: {extracted_name}")
        
        # Test company extraction
        extracted_company = linkedin_service._extract_company(comprehensive_profile_data)
        print(f"✓ Extracted company: {extracted_company}")
        
        # Test profile summary creation
        profile_summary = linkedin_service._create_profile_summary(comprehensive_profile_data)
        print(f"\n✓ Profile Summary:")
        print(f"  Basic Info: {profile_summary['basic_info']}")
        print(f"  Experience Count: {profile_summary['experience_count']}")
        print(f"  Education Count: {profile_summary['education_count']}")
        print(f"  Skills Count: {profile_summary['skills_count']}")
        print(f"  Certifications Count: {profile_summary['certifications_count']}")
        print(f"  Languages Count: {profile_summary['languages_count']}")
        
        print("\n✓ Comprehensive LinkedIn data processing test passed")
        return True
        
    except Exception as e:
        print(f"✗ Comprehensive LinkedIn data processing test failed: {e}")
        return False

def main():
    """Main test function."""
    print("=" * 60)
    print("COMPREHENSIVE LINKEDIN DATA TEST")
    print("=" * 60)
    
    test_comprehensive_linkedin_data()
    
    print("=" * 60)
    print("COMPREHENSIVE DATA TEST COMPLETED")
    print("=" * 60)

if __name__ == "__main__":
    main() 