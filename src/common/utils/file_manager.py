import os
import json
from typing import Optional, Dict, List, Any
from ..configs.settings import get_settings
from .logger import setup_logger

logger = setup_logger(__name__)

class FileManager:
    def __init__(self):
        settings = get_settings()
        self.base_dir = settings.linkedin_profiles_dir
        self._ensure_base_dir()
    
    def _ensure_base_dir(self):
        """Ensure the base directory exists."""
        os.makedirs(self.base_dir, exist_ok=True)
    
    def save_linkedin_profile(self, user_id: int, profile_data: Dict) -> bool:
        """
        Save LinkedIn profile data as markdown file.
        
        Args:
            user_id: The user ID to create directory for
            profile_data: The scraped LinkedIn profile data
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Create user directory
            user_dir = os.path.join(self.base_dir, str(user_id))
            os.makedirs(user_dir, exist_ok=True)
            
            # Convert profile data to markdown
            markdown_content = self._convert_to_markdown(profile_data)
            
            # Save to file
            file_path = os.path.join(user_dir, "profile.md")
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(markdown_content)
            
            # Also save raw JSON for backup
            json_path = os.path.join(user_dir, "profile.json")
            with open(json_path, 'w', encoding='utf-8') as file:
                json.dump(profile_data, file, indent=2, ensure_ascii=False)
            
            logger.info(f"Saved LinkedIn profile for user {user_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error saving LinkedIn profile for user {user_id}: {str(e)}")
            return False
    
    def get_linkedin_profile(self, user_id: int) -> Optional[str]:
        """
        Get LinkedIn profile data as markdown.
        
        Args:
            user_id: The user ID to retrieve profile for
            
        Returns:
            Markdown content or None if not found
        """
        try:
            file_path = os.path.join(self.base_dir, str(user_id), "profile.md")
            
            if not os.path.exists(file_path):
                logger.warning(f"Profile not found for user {user_id}")
                return None
            
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            
            logger.info(f"Retrieved LinkedIn profile for user {user_id}")
            return content
            
        except Exception as e:
            logger.error(f"Error retrieving LinkedIn profile for user {user_id}: {str(e)}")
            return None
    
    def _convert_to_markdown(self, profile_data: Dict) -> str:
        """
        Convert LinkedIn profile data to markdown format.
        Extracts all possible fields from the Apify LinkedIn actor.
        
        Args:
            profile_data: The scraped LinkedIn profile data
            
        Returns:
            Formatted markdown string
        """
        markdown_lines = []
        
        # Basic profile information
        markdown_lines.append("# LinkedIn Profile")
        markdown_lines.append("")
        
        # Basic Information Section
        markdown_lines.append("## Basic Information")
        markdown_lines.append("")
        
        # Name and headline
        if profile_data.get('fullName'):
            markdown_lines.append(f"**Name:** {profile_data['fullName']}")
            markdown_lines.append("")
        
        if profile_data.get('headline'):
            markdown_lines.append(f"**Headline:** {profile_data['headline']}")
            markdown_lines.append("")
        
        if profile_data.get('companyName'):
            markdown_lines.append(f"**Company:** {profile_data['companyName']}")
            markdown_lines.append("")
        
        if profile_data.get('addressWithCountry'):
            markdown_lines.append(f"**Location:** {profile_data['addressWithCountry']}")
            markdown_lines.append("")
        
        if profile_data.get('companyIndustry'):
            markdown_lines.append(f"**Industry:** {profile_data['companyIndustry']}")
            markdown_lines.append("")
        
        if profile_data.get('about'):
            markdown_lines.append(f"**About:** {profile_data['about']}")
            markdown_lines.append("")
        
        # Contact Information
        contact_info = []
        if profile_data.get('email'):
            contact_info.append(f"**Email:** {profile_data['email']}")
        if profile_data.get('mobileNumber'):
            contact_info.append(f"**Phone:** {profile_data['mobileNumber']}")
        if profile_data.get('companyWebsite'):
            contact_info.append(f"**Website:** {profile_data['companyWebsite']}")
        
        if contact_info:
            markdown_lines.append("## Contact Information")
            markdown_lines.append("")
            markdown_lines.extend(contact_info)
            markdown_lines.append("")
        
        # About Section
        if profile_data.get('about'):
            markdown_lines.append("## About")
            markdown_lines.append("")
            markdown_lines.append(profile_data['about'])
            markdown_lines.append("")
        
        # Experience Section
        if profile_data.get('experiences'):
            markdown_lines.append("## Experience")
            markdown_lines.append("")
            for exp in profile_data['experiences']:
                markdown_lines.append(f"### {exp.get('title', 'N/A')}")
                markdown_lines.append(f"**Company:** {exp.get('companyName', 'N/A')}")
                if exp.get('duration'):
                    markdown_lines.append(f"**Duration:** {exp['duration']}")
                if exp.get('location'):
                    markdown_lines.append(f"**Location:** {exp['location']}")
                if exp.get('description'):
                    markdown_lines.append(f"**Description:** {exp['description']}")
                if exp.get('startDate'):
                    markdown_lines.append(f"**Start Date:** {exp['startDate']}")
                if exp.get('endDate'):
                    markdown_lines.append(f"**End Date:** {exp['endDate']}")
                markdown_lines.append("")
        
        # Education Section
        if profile_data.get('educations'):
            markdown_lines.append("## Education")
            markdown_lines.append("")
            for edu in profile_data['educations']:
                markdown_lines.append(f"### {edu.get('schoolName', 'N/A')}")
                markdown_lines.append(f"**Degree:** {edu.get('degreeName', 'N/A')}")
                if edu.get('fieldOfStudy'):
                    markdown_lines.append(f"**Field:** {edu['fieldOfStudy']}")
                if edu.get('duration'):
                    markdown_lines.append(f"**Duration:** {edu['duration']}")
                if edu.get('startDate'):
                    markdown_lines.append(f"**Start Date:** {edu['startDate']}")
                if edu.get('endDate'):
                    markdown_lines.append(f"**End Date:** {edu['endDate']}")
                if edu.get('grade'):
                    markdown_lines.append(f"**Grade:** {edu['grade']}")
                markdown_lines.append("")
        
        # Skills Section
        if profile_data.get('skills'):
            markdown_lines.append("## Skills")
            markdown_lines.append("")
            for skill in profile_data['skills']:
                if isinstance(skill, dict):
                    skill_name = skill.get('name', 'N/A')
                    skill_endorsements = skill.get('endorsements', '')
                    if skill_endorsements:
                        markdown_lines.append(f"- {skill_name} ({skill_endorsements} endorsements)")
                    else:
                        markdown_lines.append(f"- {skill_name}")
                else:
                    markdown_lines.append(f"- {skill}")
            markdown_lines.append("")
        
        # Top Skills by Endorsements
        if profile_data.get('topSkillsByEndorsements'):
            markdown_lines.append("## Top Skills by Endorsements")
            markdown_lines.append("")
            for skill in profile_data['topSkillsByEndorsements']:
                if isinstance(skill, dict):
                    skill_name = skill.get('name', 'N/A')
                    skill_endorsements = skill.get('endorsements', '')
                    if skill_endorsements:
                        markdown_lines.append(f"- {skill_name} ({skill_endorsements} endorsements)")
                    else:
                        markdown_lines.append(f"- {skill_name}")
                else:
                    markdown_lines.append(f"- {skill}")
            markdown_lines.append("")
        
        # Certifications
        if profile_data.get('licenseAndCertificates'):
            markdown_lines.append("## Certifications")
            markdown_lines.append("")
            for cert in profile_data['licenseAndCertificates']:
                markdown_lines.append(f"### {cert.get('name', 'N/A')}")
                markdown_lines.append(f"**Issuing Organization:** {cert.get('issuingOrganization', 'N/A')}")
                if cert.get('issueDate'):
                    markdown_lines.append(f"**Issue Date:** {cert['issueDate']}")
                if cert.get('expirationDate'):
                    markdown_lines.append(f"**Expiration Date:** {cert['expirationDate']}")
                if cert.get('credentialId'):
                    markdown_lines.append(f"**Credential ID:** {cert['credentialId']}")
                markdown_lines.append("")
        
        # Languages
        if profile_data.get('languages'):
            markdown_lines.append("## Languages")
            markdown_lines.append("")
            for lang in profile_data['languages']:
                if isinstance(lang, dict):
                    lang_name = lang.get('name', 'N/A')
                    lang_proficiency = lang.get('proficiency', '')
                    if lang_proficiency:
                        markdown_lines.append(f"- {lang_name} ({lang_proficiency})")
                    else:
                        markdown_lines.append(f"- {lang_name}")
                else:
                    markdown_lines.append(f"- {lang}")
            markdown_lines.append("")
        
        # Additional sections with correct field names
        sections = [
            ('volunteerAndAwards', 'Volunteer Experience'),
            ('publications', 'Publications'),
            ('patents', 'Patents'),
            ('courses', 'Courses'),
            ('projects', 'Projects'),
            ('honorsAndAwards', 'Honors & Awards'),
            ('organizations', 'Organizations'),
            ('testScores', 'Test Scores'),
            ('volunteerCauses', 'Causes')
        ]
        
        for field_name, section_title in sections:
            if profile_data.get(field_name):
                markdown_lines.append(f"## {section_title}")
                markdown_lines.append("")
                for item in profile_data[field_name]:
                    if isinstance(item, dict):
                        # Handle structured items
                        for key, value in item.items():
                            if value:
                                markdown_lines.append(f"**{key.replace('_', ' ').title()}:** {value}")
                        markdown_lines.append("")
                    else:
                        # Handle simple items
                        markdown_lines.append(f"- {item}")
                markdown_lines.append("")
        
        # Additional Information
        additional_fields = []
        for key, value in profile_data.items():
            if key not in [
                'fullName', 'firstName', 'lastName', 'headline', 'companyName', 'addressWithCountry', 
                'companyIndustry', 'about', 'email', 'mobileNumber', 'companyWebsite', 'experiences',
                'educations', 'skills', 'topSkillsByEndorsements', 'licenseAndCertificates', 'languages',
                'volunteerAndAwards', 'publications', 'patents', 'courses', 'projects', 'honorsAndAwards',
                'organizations', 'testScores', 'volunteerCauses'
            ] and value:
                additional_fields.append((key, value))
        
        if additional_fields:
            markdown_lines.append("## Additional Information")
            markdown_lines.append("")
            for key, value in additional_fields:
                if isinstance(value, (list, dict)):
                    markdown_lines.append(f"**{key.replace('_', ' ').title()}:**")
                    markdown_lines.append(f"```json")
                    markdown_lines.append(json.dumps(value, indent=2, ensure_ascii=False))
                    markdown_lines.append(f"```")
                    markdown_lines.append("")
                else:
                    markdown_lines.append(f"**{key.replace('_', ' ').title()}:** {value}")
                    markdown_lines.append("")
        
        # Raw data section
        markdown_lines.append("## Raw Data")
        markdown_lines.append("")
        markdown_lines.append("```json")
        markdown_lines.append(json.dumps(profile_data, indent=2, ensure_ascii=False))
        markdown_lines.append("```")
        
        return "\n".join(markdown_lines) 
    
    def save_linkedin_insights(self, user_id: int, insights_data: Dict) -> bool:
        """
        Save LinkedIn insights data as JSON and markdown files.
        
        Args:
            user_id: The user ID to create directory for
            insights_data: The generated insights data
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Create user directory if it doesn't exist
            user_dir = os.path.join(self.base_dir, str(user_id))
            os.makedirs(user_dir, exist_ok=True)
            
            # Save JSON insights
            json_path = os.path.join(user_dir, "insights.json")
            with open(json_path, 'w', encoding='utf-8') as file:
                json.dump(insights_data, file, indent=2, ensure_ascii=False)
            
            # Convert to markdown and save
            markdown_content = self._convert_insights_to_markdown(insights_data)
            markdown_path = os.path.join(user_dir, "insights.md")
            with open(markdown_path, 'w', encoding='utf-8') as file:
                file.write(markdown_content)
            
            logger.info(f"Saved LinkedIn insights for user {user_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error saving LinkedIn insights for user {user_id}: {str(e)}")
            return False
    
    def get_linkedin_insights(self, user_id: int) -> Optional[Dict]:
        """
        Get LinkedIn insights data as JSON.
        
        Args:
            user_id: The user ID to retrieve insights for
            
        Returns:
            Insights data or None if not found
        """
        try:
            json_path = os.path.join(self.base_dir, str(user_id), "insights.json")
            
            if not os.path.exists(json_path):
                logger.warning(f"Insights not found for user {user_id}")
                return None
            
            with open(json_path, 'r', encoding='utf-8') as file:
                insights_data = json.load(file)
            
            logger.info(f"Retrieved LinkedIn insights for user {user_id}")
            return insights_data
            
        except Exception as e:
            logger.error(f"Error retrieving LinkedIn insights for user {user_id}: {str(e)}")
            return None
    
    def get_linkedin_insights_markdown(self, user_id: int) -> Optional[str]:
        """
        Get LinkedIn insights data as markdown.
        
        Args:
            user_id: The user ID to retrieve insights for
            
        Returns:
            Markdown content or None if not found
        """
        try:
            markdown_path = os.path.join(self.base_dir, str(user_id), "insights.md")
            
            if not os.path.exists(markdown_path):
                logger.warning(f"Insights markdown not found for user {user_id}")
                return None
            
            with open(markdown_path, 'r', encoding='utf-8') as file:
                content = file.read()
            
            logger.info(f"Retrieved LinkedIn insights markdown for user {user_id}")
            return content
            
        except Exception as e:
            logger.error(f"Error retrieving LinkedIn insights markdown for user {user_id}: {str(e)}")
            return None
    
    def _convert_insights_to_markdown(self, insights_data: Dict) -> str:
        """
        Convert LinkedIn insights data to markdown format.
        
        Args:
            insights_data: The insights data to convert
            
        Returns:
            Formatted markdown string
        """
        markdown_lines = []
        
        markdown_lines.append("# LinkedIn Profile Insights")
        markdown_lines.append("")
        
        # International Experience
        if insights_data.get('international_experience'):
            exp = insights_data['international_experience']
            markdown_lines.append("## 🌍 International Experience")
            markdown_lines.append("")
            if exp.get('countries'):
                markdown_lines.append("**Countries/Regions:**")
                for country in exp['countries']:
                    markdown_lines.append(f"- {country}")
                markdown_lines.append("")
            if exp.get('summary'):
                markdown_lines.append(f"**Summary:** {exp['summary']}")
                markdown_lines.append("")
        
        # Industry Sectors
        if insights_data.get('industry_sectors'):
            sectors = insights_data['industry_sectors']
            markdown_lines.append("## 🏢 Industry Sectors")
            markdown_lines.append("")
            if sectors.get('sectors'):
                markdown_lines.append("**Sectors:**")
                for sector in sectors['sectors']:
                    markdown_lines.append(f"- {sector}")
                markdown_lines.append("")
            if sectors.get('summary'):
                markdown_lines.append(f"**Summary:** {sectors['summary']}")
                markdown_lines.append("")
        
        # Education Analysis
        if insights_data.get('education_analysis'):
            edu = insights_data['education_analysis']
            markdown_lines.append("## 🎓 Education Analysis")
            markdown_lines.append("")
            if edu.get('degrees'):
                markdown_lines.append("**Degrees & Qualifications:**")
                for degree in edu['degrees']:
                    markdown_lines.append(f"- {degree}")
                markdown_lines.append("")
            if edu.get('summary'):
                markdown_lines.append(f"**Summary:** {edu['summary']}")
                markdown_lines.append("")
        
        # Value Proposition
        if insights_data.get('value_proposition'):
            value = insights_data['value_proposition']
            markdown_lines.append("## 💼 Value Proposition")
            markdown_lines.append("")
            if value.get('key_areas'):
                markdown_lines.append("**Key Areas of Value:**")
                for area in value['key_areas']:
                    markdown_lines.append(f"- {area}")
                markdown_lines.append("")
            if value.get('summary'):
                markdown_lines.append(f"**Summary:** {value['summary']}")
                markdown_lines.append("")
        
        # Interests from Posts
        if insights_data.get('interests_from_posts'):
            interests = insights_data['interests_from_posts']
            markdown_lines.append("## 📱 Current Interests (from Posts)")
            markdown_lines.append("")
            if interests.get('topics'):
                markdown_lines.append("**Topics of Interest:**")
                for topic in interests['topics']:
                    markdown_lines.append(f"- {topic}")
                markdown_lines.append("")
            if interests.get('summary'):
                markdown_lines.append(f"**Summary:** {interests['summary']}")
                markdown_lines.append("")
        
        # Talking Points
        if insights_data.get('talking_points'):
            talking = insights_data['talking_points']
            markdown_lines.append("## 💬 Talking Points")
            markdown_lines.append("")
            if talking.get('points'):
                markdown_lines.append("**Conversation Starters:**")
                for i, point in enumerate(talking['points'], 1):
                    markdown_lines.append(f"{i}. {point}")
                markdown_lines.append("")
            if talking.get('summary'):
                markdown_lines.append(f"**Summary:** {talking['summary']}")
                markdown_lines.append("")
        
        # Raw LLM Response (if available)
        if insights_data.get('raw_llm_response'):
            markdown_lines.append("## 🤖 Raw AI Analysis")
            markdown_lines.append("")
            markdown_lines.append("```")
            markdown_lines.append(insights_data['raw_llm_response'])
            markdown_lines.append("```")
            markdown_lines.append("")
        
        return "\n".join(markdown_lines) 