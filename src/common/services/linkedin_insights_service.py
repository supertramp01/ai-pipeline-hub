import json
import re
from typing import Dict, List, Optional, Tuple
from src.common.utils.csv_manager import CSVManager
from src.common.utils.file_manager import FileManager
from src.common.utils.logger import setup_logger
from src.common.prompts.linkedin_insights import get_insights_system_prompt, get_insights_user_prompt
from src.common.configs.settings import get_settings
import openai

logger = setup_logger(__name__)

class LinkedInInsightsService:
    """Service for generating insights from LinkedIn profile data."""
    
    def __init__(self):
        self.csv_manager = CSVManager()
        self.file_manager = FileManager()
        self.settings = get_settings()
        
        # Initialize OpenAI client
        if self.settings.openai_api_key:
            openai.api_key = self.settings.openai_api_key
        else:
            logger.warning("OpenAI API key not found. LLM insights generation will not work.")
    
    def generate_insights(self, user_id: int, custom_prompt: Optional[str] = None) -> Tuple[bool, Dict]:
        """
        Generate comprehensive insights from LinkedIn profile data.
        
        Args:
            user_id: The user ID to generate insights for
            custom_prompt: Optional custom prompt for specific analysis focus
            
        Returns:
            Tuple of (success: bool, insights_data: Dict)
        """
        try:
            logger.info(f"Starting LinkedIn insights generation for user: {user_id}")
            
            # Get profile data
            profile_data = self._get_profile_data(user_id)
            if not profile_data:
                return False, {"error": "Profile data not found"}
            
            # Generate insights using LLM
            insights = self._generate_llm_insights(profile_data, custom_prompt)
            if not insights:
                return False, {"error": "Failed to generate insights"}
            
            # Save insights
            success = self.file_manager.save_linkedin_insights(user_id, insights)
            if not success:
                return False, {"error": "Failed to save insights"}
            
            logger.info(f"Successfully generated insights for user {user_id}")
            return True, insights
            
        except Exception as e:
            logger.error(f"Error generating LinkedIn insights: {str(e)}")
            return False, {"error": str(e)}
    
    def get_insights(self, user_id: int, auto_generate: bool = True) -> Optional[Dict]:
        """
        Get stored insights for a user.
        
        Args:
            user_id: The user ID to retrieve insights for
            auto_generate: If True, automatically generate insights if they don't exist
            
        Returns:
            Insights data or None if not found and auto_generate is False
        """
        try:
            # Try to get existing insights
            insights = self.file_manager.get_linkedin_insights(user_id)
            
            if insights is not None:
                logger.info(f"Retrieved existing insights for user {user_id}")
                return insights
            
            # If insights don't exist and auto_generate is enabled
            if auto_generate:
                logger.info(f"No insights found for user {user_id}, auto-generating...")
                success, generated_insights = self.generate_insights(user_id)
                
                if success:
                    logger.info(f"Successfully auto-generated insights for user {user_id}")
                    return generated_insights
                else:
                    logger.error(f"Failed to auto-generate insights for user {user_id}")
                    return None
            else:
                logger.info(f"No insights found for user {user_id} and auto_generate is disabled")
                return None
                
        except Exception as e:
            logger.error(f"Error retrieving insights for user {user_id}: {str(e)}")
            return None
    
    def _get_profile_data(self, user_id: int) -> Optional[str]:
        """Get LinkedIn profile data in markdown format for analysis."""
        try:
            # Get the markdown profile data
            profile_content = self.file_manager.get_linkedin_profile(user_id)
            if not profile_content:
                logger.error(f"Profile markdown not found for user {user_id}")
                return None
            
            return profile_content
        except Exception as e:
            logger.error(f"Error loading profile data for user {user_id}: {str(e)}")
            return None
    
    def _generate_llm_insights(self, profile_data: str, custom_prompt: Optional[str] = None) -> Optional[Dict]:
        """Generate insights using OpenAI GPT-4."""
        try:
            if not self.settings.openai_api_key:
                logger.error("OpenAI API key not configured. Cannot generate insights.")
                return None
            
            # Prepare the profile data for analysis
            analysis_data = self._prepare_analysis_data(profile_data)
            
            # Get prompts
            system_prompt = get_insights_system_prompt()
            user_prompt = get_insights_user_prompt(analysis_data, custom_prompt)
            
            # Call OpenAI API
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.3,
                max_tokens=2000
            )
            
            content = response.choices[0].message.content
            
            # Try to parse as JSON first
            try:
                insights = json.loads(content)
                return insights
            except json.JSONDecodeError:
                # If JSON parsing fails, create a structured response
                logger.warning("LLM response was not valid JSON, creating structured response")
                return self._create_structured_insights(content, analysis_data)
                
        except Exception as e:
            logger.error(f"Error generating LLM insights: {str(e)}")
            return None
    
    def _prepare_analysis_data(self, profile_data: str) -> Dict:
        """Prepare profile data for analysis by extracting key information from markdown."""
        analysis_data = {
            "basic_info": {},
            "experience": [],
            "education": [],
            "skills": [],
            "posts": [],
            "projects": [],
            "certifications": [],
            "volunteer": [],
            "publications": [],
            "recommendations": [],
            "interests": []
        }
        
        # First, extract basic info from formatted sections
        lines = profile_data.split('\n')
        current_section = None
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Detect sections
            if line.startswith('## Basic Information'):
                current_section = 'basic_info'
                continue
            elif line.startswith('## Experience'):
                current_section = 'experience'
                continue
            elif line.startswith('## Education'):
                current_section = 'education'
                continue
            elif line.startswith('## Skills'):
                current_section = 'skills'
                continue
            elif line.startswith('## Updates:'):
                current_section = 'posts'
                continue
            elif line.startswith('## Projects'):
                current_section = 'projects'
                continue
            elif line.startswith('## Certifications'):
                current_section = 'certifications'
                continue
            elif line.startswith('## Volunteer Experience'):
                current_section = 'volunteer'
                continue
            elif line.startswith('## Publications'):
                current_section = 'publications'
                continue
            elif line.startswith('##'):
                current_section = None
                continue
            
            # Process content based on current section
            if current_section == 'basic_info':
                if line.startswith('**Name:**'):
                    analysis_data['basic_info']['name'] = line.replace('**Name:**', '').strip()
                elif line.startswith('**Headline:**'):
                    analysis_data['basic_info']['headline'] = line.replace('**Headline:**', '').strip()
                elif line.startswith('**Company:**'):
                    analysis_data['basic_info']['company'] = line.replace('**Company:**', '').strip()
                elif line.startswith('**Location:**'):
                    analysis_data['basic_info']['location'] = line.replace('**Location:**', '').strip()
                elif line.startswith('**Industry:**'):
                    analysis_data['basic_info']['industry'] = line.replace('**Industry:**', '').strip()
                elif line.startswith('**About:**'):
                    analysis_data['basic_info']['about'] = line.replace('**About:**', '').strip()
        
        # Now extract detailed information from JSON data
        try:
            # Find all JSON blocks in the markdown
            json_blocks = []
            start_pos = 0
            while True:
                json_start = profile_data.find('```json', start_pos)
                if json_start == -1:
                    break
                
                json_end = profile_data.find('```', json_start + 7)
                if json_end == -1:
                    break
                
                json_content = profile_data[json_start + 7:json_end].strip()
                try:
                    json_data = json.loads(json_content)
                    json_blocks.append(json_data)
                except json.JSONDecodeError:
                    logger.warning(f"Failed to parse JSON block at position {json_start}")
                
                start_pos = json_end + 3
            
            # Find the main profile data (the largest JSON object)
            main_json_data = None
            for json_data in json_blocks:
                if isinstance(json_data, dict) and len(json_data) > 20:  # Main profile data is the largest
                    main_json_data = json_data
                    break
            
            if not main_json_data:
                logger.warning("Could not find main profile JSON data")
                return analysis_data
            
            logger.info(f"Successfully parsed main JSON data with keys: {list(main_json_data.keys())}")
            
            # Extract experience from JSON
            if main_json_data.get('experiences') and isinstance(main_json_data['experiences'], list):
                logger.info(f"Found {len(main_json_data['experiences'])} experiences")
                for exp in main_json_data['experiences']:
                    if isinstance(exp, dict):
                        experience = {
                            "title": exp.get('title', ''),
                            "company": exp.get('subtitle', '').split(' · ')[0] if exp.get('subtitle') else '',
                            "location": exp.get('metadata', ''),
                            "duration": exp.get('caption', ''),
                            "description": ""
                        }
                        
                        # Extract description from subComponents
                        if exp.get('subComponents') and isinstance(exp['subComponents'], list):
                            for sub in exp['subComponents']:
                                if isinstance(sub, dict) and sub.get('description'):
                                    if isinstance(sub['description'], list):
                                        for desc in sub['description']:
                                            if isinstance(desc, dict) and desc.get('text'):
                                                experience["description"] += desc['text'] + " "
                        
                        analysis_data['experience'].append(experience)
            
            # Extract education from JSON
            if main_json_data.get('educations') and isinstance(main_json_data['educations'], list):
                logger.info(f"Found {len(main_json_data['educations'])} education entries")
                for edu in main_json_data['educations']:
                    if isinstance(edu, dict):
                        education = {
                            "school": edu.get('title', ''),
                            "degree": edu.get('subtitle', ''),
                            "field": "",
                            "duration": edu.get('caption', ''),
                            "grade": ""
                        }
                        analysis_data['education'].append(education)
            
            # Extract skills from JSON
            if main_json_data.get('skills') and isinstance(main_json_data['skills'], list):
                logger.info(f"Found {len(main_json_data['skills'])} skills")
                for skill in main_json_data['skills']:
                    if isinstance(skill, dict) and skill.get('title'):
                        skill_name = skill.get('title', '')
                        if skill_name and skill_name != 'N/A':
                            analysis_data['skills'].append(skill_name)
            
            # Extract projects from JSON
            if main_json_data.get('projects') and isinstance(main_json_data['projects'], list):
                logger.info(f"Found {len(main_json_data['projects'])} projects")
                for project in main_json_data['projects']:
                    if isinstance(project, dict):
                        project_data = {
                            "title": project.get('title', ''),
                            "description": "",
                            "url": ""
                        }
                        
                        # Extract description from subComponents
                        if project.get('subComponents') and isinstance(project['subComponents'], list):
                            for sub in project['subComponents']:
                                if isinstance(sub, dict) and sub.get('description'):
                                    if isinstance(sub['description'], list):
                                        for desc in sub['description']:
                                            if isinstance(desc, dict) and desc.get('text'):
                                                project_data["description"] += desc['text'] + " "
                        
                        analysis_data['projects'].append(project_data)
            
            # Extract publications from JSON
            if main_json_data.get('publications') and isinstance(main_json_data['publications'], list):
                logger.info(f"Found {len(main_json_data['publications'])} publications")
                for pub in main_json_data['publications']:
                    if isinstance(pub, dict):
                        pub_data = {
                            "title": pub.get('title', ''),
                            "publisher": pub.get('subtitle', ''),
                            "date": ""
                        }
                        analysis_data['publications'].append(pub_data)
            
            # Extract volunteer experience from JSON
            if main_json_data.get('volunteerAndAwards') and isinstance(main_json_data['volunteerAndAwards'], list):
                logger.info(f"Found {len(main_json_data['volunteerAndAwards'])} volunteer experiences")
                for vol in main_json_data['volunteerAndAwards']:
                    if isinstance(vol, dict):
                        vol_data = {
                            "title": vol.get('title', ''),
                            "organization": vol.get('subtitle', ''),
                            "description": ""
                        }
                        analysis_data['volunteer'].append(vol_data)
            
            # Extract posts from JSON
            if main_json_data.get('updates') and isinstance(main_json_data['updates'], list):
                logger.info(f"Found {len(main_json_data['updates'])} posts")
                for post in main_json_data['updates'][:5]:  # Last 5 posts
                    if isinstance(post, dict):
                        post_data = {
                            "text": post.get('postText', ''),
                            "likes": post.get('numLikes', 0),
                            "comments": post.get('numComments', 0),
                            "date": post.get('date', '')
                        }
                        analysis_data['posts'].append(post_data)
            
            # Extract certifications from JSON
            if main_json_data.get('licenseAndCertificates') and isinstance(main_json_data['licenseAndCertificates'], list):
                logger.info(f"Found {len(main_json_data['licenseAndCertificates'])} certifications")
                for cert in main_json_data['licenseAndCertificates']:
                    if isinstance(cert, dict):
                        cert_data = {
                            "name": cert.get('name', ''),
                            "organization": cert.get('issuingOrganization', ''),
                            "issue_date": cert.get('issueDate', '')
                        }
                        analysis_data['certifications'].append(cert_data)
            
            # Extract recommendations from JSON
            if main_json_data.get('recommendations') and isinstance(main_json_data['recommendations'], list):
                logger.info(f"Found {len(main_json_data['recommendations'])} recommendation sections")
                for rec_section in main_json_data['recommendations']:
                    if isinstance(rec_section, dict) and rec_section.get('section_components'):
                        for rec in rec_section['section_components']:
                            if isinstance(rec, dict):
                                rec_data = {
                                    "from": rec.get('titleV2', ''),
                                    "role": rec.get('subtitle', ''),
                                    "text": ""
                                }
                                
                                # Extract recommendation text
                                if rec.get('subComponents') and isinstance(rec['subComponents'], list):
                                    for sub in rec['subComponents']:
                                        if isinstance(sub, dict) and sub.get('fixedListComponent'):
                                            for comp in sub['fixedListComponent']:
                                                if isinstance(comp, dict) and comp.get('text'):
                                                    rec_data["text"] += comp['text'] + " "
                                
                                analysis_data['recommendations'].append(rec_data)
            
            # Extract interests from JSON
            if main_json_data.get('interests') and isinstance(main_json_data['interests'], list):
                logger.info(f"Found {len(main_json_data['interests'])} interest sections")
                for interest_section in main_json_data['interests']:
                    if isinstance(interest_section, dict) and interest_section.get('section_components'):
                        for interest in interest_section['section_components']:
                            if isinstance(interest, dict):
                                interest_data = {
                                    "name": interest.get('titleV2', ''),
                                    "type": interest_section.get('section_name', ''),
                                    "description": interest.get('subtitle', '')
                                }
                                analysis_data['interests'].append(interest_data)
        
        except Exception as e:
            logger.warning(f"Error parsing JSON data: {e}")
            # Continue with basic info only
        
        logger.info(f"Final analysis data summary: {len(analysis_data['experience'])} experiences, {len(analysis_data['education'])} education, {len(analysis_data['skills'])} skills, {len(analysis_data['recommendations'])} recommendations")
        return analysis_data
    
    def _create_structured_insights(self, content: str, analysis_data: Dict) -> Dict:
        """Create structured insights from LLM text response."""
        insights = {
            "international_experience": {
                "countries": [],
                "summary": "International experience analysis not available"
            },
            "industry_sectors": {
                "sectors": [],
                "summary": "Industry sector analysis not available"
            },
            "education_analysis": {
                "degrees": [],
                "summary": "Education analysis not available"
            },
            "value_proposition": {
                "key_areas": [],
                "summary": "Value proposition analysis not available"
            },
            "professional_reputation": {
                "strengths": [],
                "summary": "Professional reputation analysis not available"
            },
            "current_interests": {
                "focus_areas": [],
                "summary": "Current interests analysis not available"
            },
            "talking_points": {
                "points": [],
                "summary": "Talking points not available"
            },
            "raw_llm_response": content
        }
        
        # Try to extract some basic insights from the content
        lines = content.split('\n')
        current_section = None
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Try to identify sections
            if 'international' in line.lower() or 'countries' in line.lower():
                current_section = 'international_experience'
            elif 'industry' in line.lower() or 'sector' in line.lower():
                current_section = 'industry_sectors'
            elif 'education' in line.lower() or 'degree' in line.lower():
                current_section = 'education_analysis'
            elif 'value' in line.lower() or 'expertise' in line.lower():
                current_section = 'value_proposition'
            elif 'reputation' in line.lower() or 'recommendation' in line.lower():
                current_section = 'professional_reputation'
            elif 'interest' in line.lower() or 'focus' in line.lower():
                current_section = 'current_interests'
            elif 'talking' in line.lower() or 'conversation' in line.lower():
                current_section = 'talking_points'
            
            # Add content to appropriate section
            if current_section and line and not line.startswith('#'):
                if current_section in insights:
                    if 'summary' in insights[current_section]:
                        insights[current_section]['summary'] = line
                    elif 'points' in insights[current_section]:
                        insights[current_section]['points'].append(line)
                    elif 'focus_areas' in insights[current_section]:
                        insights[current_section]['focus_areas'].append(line)
                    elif 'strengths' in insights[current_section]:
                        insights[current_section]['strengths'].append(line)
                    elif 'sectors' in insights[current_section]:
                        insights[current_section]['sectors'].append(line)
                    elif 'countries' in insights[current_section]:
                        insights[current_section]['countries'].append(line)
                    elif 'degrees' in insights[current_section]:
                        insights[current_section]['degrees'].append(line)
                    elif 'key_areas' in insights[current_section]:
                        insights[current_section]['key_areas'].append(line)
        
        return insights
    
    def get_all_insights(self) -> List[Dict]:
        """Get insights for all users who have them."""
        try:
            users = self.csv_manager.get_all_users()
            all_insights = []
            
            for user in users:
                user_id = int(user['user_id'])
                insights = self.get_insights(user_id)
                if insights:
                    insights['user_id'] = user_id
                    insights['name'] = user['name']
                    insights['company'] = user['company']
                    all_insights.append(insights)
            
            return all_insights
            
        except Exception as e:
            logger.error(f"Error getting all insights: {str(e)}")
            return [] 