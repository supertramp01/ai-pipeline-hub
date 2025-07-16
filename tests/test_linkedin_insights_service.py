#!/usr/bin/env python3
"""
Test cases for LinkedIn Insights Service.
"""

import sys
import os
import json
from unittest.mock import patch, MagicMock

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from common.services.linkedin_insights_service import LinkedInInsightsService

class TestLinkedInInsightsService:
    """Test cases for LinkedInInsightsService."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.insights_service = LinkedInInsightsService()
        
        # Sample profile data for testing
        self.sample_profile_data = {
            "fullName": "John Doe",
            "headline": "Senior Software Engineer at TechCorp",
            "companyName": "TechCorp",
            "addressWithCountry": "San Francisco, CA, United States",
            "companyIndustry": "Technology",
            "about": "Experienced software engineer with expertise in Python and cloud technologies.",
            "experiences": [
                {
                    "title": "Senior Software Engineer",
                    "companyName": "TechCorp",
                    "location": "San Francisco, CA",
                    "duration": "2 years",
                    "description": "Led development of cloud-based applications"
                },
                {
                    "title": "Software Engineer",
                    "companyName": "StartupXYZ",
                    "location": "London, UK",
                    "duration": "3 years",
                    "description": "Developed web applications using Python"
                }
            ],
            "educations": [
                {
                    "schoolName": "Stanford University",
                    "degreeName": "Master of Science",
                    "fieldOfStudy": "Computer Science",
                    "duration": "2 years"
                }
            ],
            "skills": ["Python", "JavaScript", "AWS", "Docker"],
            "updates": [
                {
                    "postText": "Just published a new article about machine learning in production! #ML #AI",
                    "numLikes": 50,
                    "numComments": 10
                },
                {
                    "postText": "Excited to speak at the upcoming tech conference about cloud architecture",
                    "numLikes": 30,
                    "numComments": 5
                }
            ],
            "projects": [
                {
                    "title": "Cloud Migration Project",
                    "description": "Led migration of legacy systems to AWS",
                    "url": "https://github.com/johndoe/cloud-migration"
                }
            ]
        }
    
    def test_prepare_analysis_data(self):
        """Test preparation of profile data for analysis."""
        analysis_data = self.insights_service._prepare_analysis_data(self.sample_profile_data)
        
        # Check basic info
        assert analysis_data["basic_info"]["name"] == "John Doe"
        assert analysis_data["basic_info"]["headline"] == "Senior Software Engineer at TechCorp"
        assert analysis_data["basic_info"]["company"] == "TechCorp"
        
        # Check experience
        assert len(analysis_data["experience"]) == 2
        assert analysis_data["experience"][0]["title"] == "Senior Software Engineer"
        assert analysis_data["experience"][1]["location"] == "London, UK"
        
        # Check education
        assert len(analysis_data["education"]) == 1
        assert analysis_data["education"][0]["school"] == "Stanford University"
        
        # Check skills
        assert len(analysis_data["skills"]) == 4
        assert "Python" in analysis_data["skills"]
        
        # Check posts
        assert len(analysis_data["posts"]) == 2
        assert "machine learning" in analysis_data["posts"][0]["text"].lower()
        
        # Check projects
        assert len(analysis_data["projects"]) == 1
        assert analysis_data["projects"][0]["title"] == "Cloud Migration Project"
    
    @patch('openai.OpenAI')
    def test_generate_llm_insights_success(self, mock_openai):
        """Test successful LLM insights generation."""
        # Mock OpenAI response
        mock_response = MagicMock()
        mock_response.choices[0].message.content = json.dumps({
            "international_experience": {
                "countries": ["United States", "United Kingdom"],
                "summary": "Has worked in multiple countries"
            },
            "industry_sectors": {
                "sectors": ["Technology", "Software Development"],
                "summary": "Deep expertise in technology sector"
            },
            "education_analysis": {
                "degrees": ["Master of Science in Computer Science"],
                "summary": "Strong educational background"
            },
            "value_proposition": {
                "key_areas": ["Cloud Architecture", "Python Development"],
                "summary": "Expert in cloud and Python development"
            },
            "interests_from_posts": {
                "topics": ["Machine Learning", "Cloud Architecture"],
                "summary": "Interested in ML and cloud technologies"
            },
            "talking_points": {
                "points": ["Cloud migration experience", "ML in production"],
                "summary": "Great conversation starters about cloud and ML"
            }
        })
        
        mock_openai.return_value.chat.completions.create.return_value = mock_response
        
        # Test insights generation
        insights = self.insights_service._generate_llm_insights(self.sample_profile_data)
        
        assert insights is not None
        assert "international_experience" in insights
        assert "industry_sectors" in insights
        assert "education_analysis" in insights
        assert "value_proposition" in insights
        assert "interests_from_posts" in insights
        assert "talking_points" in insights
        
        # Check specific values
        assert "United States" in insights["international_experience"]["countries"]
        assert "Technology" in insights["industry_sectors"]["sectors"]
        assert "Machine Learning" in insights["interests_from_posts"]["topics"]
    
    @patch('openai.OpenAI')
    def test_generate_llm_insights_fallback(self, mock_openai):
        """Test LLM insights generation with fallback to structured response."""
        # Mock OpenAI response with invalid JSON
        mock_response = MagicMock()
        mock_response.choices[0].message.content = "This is not valid JSON"
        
        mock_openai.return_value.chat.completions.create.return_value = mock_response
        
        # Test insights generation
        insights = self.insights_service._generate_llm_insights(self.sample_profile_data)
        
        assert insights is not None
        assert "international_experience" in insights
        assert "industry_sectors" in insights
        assert "education_analysis" in insights
        assert "value_proposition" in insights
        assert "interests_from_posts" in insights
        assert "talking_points" in insights
        assert "raw_llm_response" in insights
    
    @patch('builtins.open', create=True)
    @patch('json.load')
    def test_get_profile_data_success(self, mock_json_load, mock_open):
        """Test successful profile data retrieval."""
        mock_json_load.return_value = self.sample_profile_data
        
        profile_data = self.insights_service._get_profile_data(1)
        
        assert profile_data == self.sample_profile_data
        mock_open.assert_called_once()
    
    @patch('builtins.open', side_effect=FileNotFoundError())
    def test_get_profile_data_not_found(self, mock_open):
        """Test profile data retrieval when file doesn't exist."""
        profile_data = self.insights_service._get_profile_data(999)
        
        assert profile_data is None
    
    def test_create_structured_insights(self):
        """Test creation of structured insights from text response."""
        content = """
        International Experience: Worked in US and UK
        Industry Sectors: Technology and software development
        Education: Master's degree in Computer Science
        Value Proposition: Expert in cloud and Python
        Interests from Posts: Machine learning and cloud architecture
        Talking Points: Cloud migration and ML in production
        """
        
        insights = self.insights_service._create_structured_insights(content, {})
        
        assert insights is not None
        assert "international_experience" in insights
        assert "industry_sectors" in insights
        assert "education_analysis" in insights
        assert "value_proposition" in insights
        assert "interests_from_posts" in insights
        assert "talking_points" in insights
        assert "raw_llm_response" in insights
    
    @patch.object(LinkedInInsightsService, '_get_profile_data')
    @patch.object(LinkedInInsightsService, '_generate_llm_insights')
    @patch.object(LinkedInInsightsService, 'file_manager')
    def test_generate_insights_success(self, mock_file_manager, mock_generate_llm, mock_get_profile):
        """Test successful insights generation."""
        # Mock dependencies
        mock_get_profile.return_value = self.sample_profile_data
        mock_generate_llm.return_value = {"test": "insights"}
        mock_file_manager.save_linkedin_insights.return_value = True
        
        # Test insights generation
        success, response_data = self.insights_service.generate_insights(1)
        
        assert success is True
        assert response_data == {"test": "insights"}
        mock_get_profile.assert_called_once_with(1)
        mock_generate_llm.assert_called_once_with(self.sample_profile_data, None)
        mock_file_manager.save_linkedin_insights.assert_called_once_with(1, {"test": "insights"})
    
    @patch.object(LinkedInInsightsService, '_get_profile_data')
    def test_generate_insights_profile_not_found(self, mock_get_profile):
        """Test insights generation when profile data is not found."""
        mock_get_profile.return_value = None
        
        success, response_data = self.insights_service.generate_insights(1)
        
        assert success is False
        assert "error" in response_data
        assert "Profile data not found" in response_data["error"]
    
    @patch.object(LinkedInInsightsService, '_get_profile_data')
    @patch.object(LinkedInInsightsService, '_generate_llm_insights')
    def test_generate_insights_llm_failure(self, mock_generate_llm, mock_get_profile):
        """Test insights generation when LLM fails."""
        mock_get_profile.return_value = self.sample_profile_data
        mock_generate_llm.return_value = None
        
        success, response_data = self.insights_service.generate_insights(1)
        
        assert success is False
        assert "error" in response_data
        assert "Failed to generate insights" in response_data["error"]
    
    @patch.object(LinkedInInsightsService, 'file_manager')
    def test_get_insights_success(self, mock_file_manager):
        """Test successful insights retrieval."""
        mock_insights = {"test": "insights"}
        mock_file_manager.get_linkedin_insights.return_value = mock_insights
        
        insights = self.insights_service.get_insights(1)
        
        assert insights == mock_insights
        mock_file_manager.get_linkedin_insights.assert_called_once_with(1)
    
    @patch.object(LinkedInInsightsService, 'file_manager')
    def test_get_insights_not_found(self, mock_file_manager):
        """Test insights retrieval when not found."""
        mock_file_manager.get_linkedin_insights.return_value = None
        
        insights = self.insights_service.get_insights(1)
        
        assert insights is None
    
    @patch.object(LinkedInInsightsService, 'csv_manager')
    @patch.object(LinkedInInsightsService, 'get_insights')
    def test_get_all_insights(self, mock_get_insights, mock_csv_manager):
        """Test retrieval of all insights."""
        # Mock CSV data
        mock_csv_manager.get_all_users.return_value = [
            {"user_id": "1", "name": "John Doe", "company": "TechCorp"},
            {"user_id": "2", "name": "Jane Smith", "company": "StartupXYZ"}
        ]
        
        # Mock insights for first user only
        mock_get_insights.side_effect = lambda user_id: {"insights": "data"} if user_id == 1 else None
        
        all_insights = self.insights_service.get_all_insights()
        
        assert len(all_insights) == 1
        assert all_insights[0]["user_id"] == 1
        assert all_insights[0]["name"] == "John Doe"
        assert all_insights[0]["company"] == "TechCorp"
        assert all_insights[0]["insights"] == {"insights": "data"}
    
    def test_custom_prompt_handling(self):
        """Test that custom prompts are properly handled."""
        custom_prompt = "Focus on technical skills and cloud experience"
        
        # This would be tested in the actual LLM call, but we can verify the prompt is passed through
        with patch.object(self.insights_service, '_get_profile_data') as mock_get_profile, \
             patch.object(self.insights_service, '_generate_llm_insights') as mock_generate_llm, \
             patch.object(self.insights_service, 'file_manager') as mock_file_manager:
            
            mock_get_profile.return_value = self.sample_profile_data
            mock_generate_llm.return_value = {"test": "insights"}
            mock_file_manager.save_linkedin_insights.return_value = True
            
            success, response_data = self.insights_service.generate_insights(1, custom_prompt)
            
            assert success is True
            mock_generate_llm.assert_called_once_with(self.sample_profile_data, custom_prompt)

if __name__ == "__main__":
    # Run tests
    import pytest
    pytest.main([__file__]) 