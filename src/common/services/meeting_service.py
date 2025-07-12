import json
import uuid
from typing import Dict, Any, List, Optional
import logging
from datetime import datetime
import openai
from ..utils.meeting_csv_manager import MeetingCSVManager
from ..utils.meeting_file_manager import MeetingFileManager
from ..utils.csv_manager import CSVManager
from ..utils.company_csv_manager import CompanyCSVManager
from ..configs.settings import get_settings
from ..prompts.meeting_preparation import (
    get_meeting_talking_points_system_prompt,
    get_meeting_talking_points_user_prompt
)

logger = logging.getLogger(__name__)

class MeetingService:
    """Service for managing meeting preparation and participant analysis."""
    
    def __init__(self):
        self.csv_manager = MeetingCSVManager()
        self.file_manager = MeetingFileManager()
        self.user_csv_manager = CSVManager()
        self.company_csv_manager = CompanyCSVManager()
        self.settings = get_settings()
        
        # Initialize OpenAI client
        if self.settings.openai_api_key:
            openai.api_key = self.settings.openai_api_key
        else:
            logger.warning("OpenAI API key not found. LLM talking points generation will not work.")
    
    def create_meeting(self, meeting_title: str, meeting_date: str, participants: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Create a new meeting with participant analysis and talking points.
        
        Args:
            meeting_title: Title of the meeting
            meeting_date: Date of the meeting
            participants: List of participant data (can be Pydantic models or dictionaries)
            
        Returns:
            Dictionary with meeting creation results
        """
        try:
            # Generate unique meeting ID
            meeting_id = str(uuid.uuid4())
            
            # Convert participants to dictionaries if they are Pydantic models
            participant_dicts = []
            for participant in participants:
                if hasattr(participant, 'dict'):
                    participant_dicts.append(participant.dict())
                else:
                    participant_dicts.append(participant)
            
            # Process participants and generate talking points
            processed_participants = self._process_participants(participant_dicts)
            
            # Generate talking points for each participant
            for participant in processed_participants:
                talking_points = self._generate_talking_points(participant, processed_participants)
                participant['talking_points'] = talking_points
            
            # Create meeting data structure
            meeting_data = {
                'meeting_id': meeting_id,
                'meeting_title': meeting_title,
                'meeting_date': meeting_date,
                'created_date': datetime.now().isoformat(),
                'participants': processed_participants
            }
            
            # Save meeting data
            if self.file_manager.save_meeting_data(meeting_id, meeting_data):
                # Create CSV entry
                self.csv_manager.create_meeting(
                    meeting_id=meeting_id,
                    meeting_title=meeting_title,
                    meeting_date=meeting_date,
                    participant_count=len(processed_participants)
                )
                
                logger.info(f"Successfully created meeting: {meeting_id}")
                
                return {
                    'meeting_id': meeting_id,
                    'status': 'success',
                    'message': 'Meeting created successfully',
                    'participant_count': len(processed_participants),
                    'meeting_data': meeting_data
                }
            else:
                return {
                    'status': 'error',
                    'message': 'Failed to save meeting data'
                }
                
        except Exception as e:
            logger.error(f"Error creating meeting: {e}")
            return {
                'status': 'error',
                'message': f'Meeting creation failed: {str(e)}'
            }
    
    def get_meeting(self, meeting_id: str) -> Optional[Dict[str, Any]]:
        """
        Get meeting information and participant data.
        
        Args:
            meeting_id: Meeting identifier
            
        Returns:
            Meeting data or None if not found
        """
        try:
            # Get meeting data from file
            meeting_data = self.file_manager.load_meeting_data(meeting_id)
            
            if not meeting_data:
                return None
            
            # Get CSV metadata
            csv_data = self.csv_manager.get_meeting(meeting_id)
            if csv_data:
                meeting_data['csv_metadata'] = csv_data
            
            return meeting_data
            
        except Exception as e:
            logger.error(f"Error getting meeting: {e}")
            return None
    
    def get_all_meetings(self) -> List[Dict[str, Any]]:
        """
        Get all meetings from CSV.
        
        Returns:
            List of meeting data
        """
        try:
            return self.csv_manager.get_all_meetings()
        except Exception as e:
            logger.error(f"Error getting all meetings: {e}")
            return []
    
    def _process_participants(self, participants: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Process participants and enrich with LinkedIn and company data.
        
        Args:
            participants: Raw participant data (can be Pydantic models or dictionaries)
            
        Returns:
            Enriched participant data
        """
        processed_participants = []
        
        for participant in participants:
            # Convert Pydantic model to dictionary if needed
            if hasattr(participant, 'dict'):
                participant_dict = participant.dict()
            else:
                participant_dict = participant.copy()
            
            processed_participant = participant_dict.copy()
            
            # Ensure all required fields are present
            processed_participant.setdefault('name', 'Unknown')
            processed_participant.setdefault('company', 'Unknown')
            processed_participant.setdefault('meeting_objective', 'Not specified')
            processed_participant.setdefault('looking_for', 'Not specified')
            processed_participant.setdefault('background', 'Not provided')
            processed_participant.setdefault('what_they_offer', 'Not specified')
            processed_participant.setdefault('user_id', None)
            processed_participant.setdefault('company_id', None)
            
            # Enrich with LinkedIn data if available (prefer user_id over linkedin_url)
            if participant_dict.get('user_id'):
                linkedin_data = self._get_linkedin_data_by_user_id(participant_dict['user_id'])
                if linkedin_data:
                    processed_participant.update(linkedin_data)
                    # If no background provided, use LinkedIn background
                    if not participant_dict.get('background') or participant_dict.get('background') == 'Not provided':
                        processed_participant['background'] = linkedin_data.get('background', 'Not available')
            elif participant_dict.get('linkedin_url'):
                linkedin_data = self._get_linkedin_data_by_url(participant_dict['linkedin_url'])
                if linkedin_data:
                    processed_participant.update(linkedin_data)
                    # If no background provided, use LinkedIn background
                    if not participant_dict.get('background') or participant_dict.get('background') == 'Not provided':
                        processed_participant['background'] = linkedin_data.get('background', 'Not available')
            
            # Enrich with company data if available (prefer company_id over company name)
            if participant_dict.get('company_id'):
                company_data = self._get_company_data_by_id(participant_dict['company_id'])
                if company_data:
                    processed_participant['company_info'] = company_data
            elif participant_dict.get('company'):
                company_data = self._get_company_data_by_name(participant_dict['company'])
                if company_data:
                    processed_participant['company_info'] = company_data
            
            # Combine user-provided background with LinkedIn data
            if participant_dict.get('background') and participant_dict.get('background') != 'Not provided':
                linkedin_background = processed_participant.get('background', '')
                if linkedin_background and linkedin_background != 'Not available':
                    processed_participant['background'] = f"{participant_dict['background']}\n\nLinkedIn Background:\n{linkedin_background}"
                else:
                    processed_participant['background'] = participant_dict['background']
            
            processed_participants.append(processed_participant)
        
        return processed_participants
    
    def _get_linkedin_data_by_user_id(self, user_id: int) -> Optional[Dict[str, Any]]:
        """Get LinkedIn profile data for a participant by user ID."""
        try:
            # Load LinkedIn profile data directly by user ID
            from ..services.linkedin_service import LinkedInService
            linkedin_service = LinkedInService()
            profile_data = linkedin_service.get_profile(user_id)
            
            if profile_data:
                # Extract key information
                return {
                    'linkedin_profile': profile_data,
                    'background': self._extract_background_from_linkedin(profile_data)
                }
            return None
        except Exception as e:
            logger.error(f"Error getting LinkedIn data by user ID {user_id}: {e}")
            return None
    
    def _get_linkedin_data_by_url(self, linkedin_url: str) -> Optional[Dict[str, Any]]:
        """Get LinkedIn profile data for a participant by LinkedIn URL."""
        try:
            # Find user by LinkedIn URL
            users = self.user_csv_manager.get_all_users()
            for user in users:
                if user.get('linkedin_url') == linkedin_url:
                    user_id = user.get('user_id')
                    if user_id:
                        return self._get_linkedin_data_by_user_id(int(user_id))
            return None
        except Exception as e:
            logger.error(f"Error getting LinkedIn data by URL: {e}")
            return None
    
    def _get_company_data_by_id(self, company_id: str) -> Optional[Dict[str, Any]]:
        """Get company data for a participant by company ID."""
        try:
            # Load company research data directly by company ID
            from ..services.company_service import CompanyService
            company_service = CompanyService()
            company_data = company_service.get_company_json(company_id)
            
            if company_data:
                return company_data
            return None
        except Exception as e:
            logger.error(f"Error getting company data by ID {company_id}: {e}")
            return None
    
    def _get_company_data_by_name(self, company_name: str) -> Optional[Dict[str, Any]]:
        """Get company data for a participant by company name."""
        try:
            # Find company by name
            companies = self.company_csv_manager.get_all_companies()
            for company in companies:
                if company.get('company_name') == company_name:
                    company_id = company.get('company_id')
                    if company_id:
                        return self._get_company_data_by_id(company_id)
            return None
        except Exception as e:
            logger.error(f"Error getting company data by name: {e}")
            return None
    
    # Keep the old method names for backward compatibility
    def _get_linkedin_data(self, linkedin_url: str) -> Optional[Dict[str, Any]]:
        """Get LinkedIn profile data for a participant (deprecated, use _get_linkedin_data_by_url)."""
        return self._get_linkedin_data_by_url(linkedin_url)
    
    def _get_company_data(self, company_name: str) -> Optional[Dict[str, Any]]:
        """Get company data for a participant (deprecated, use _get_company_data_by_name)."""
        return self._get_company_data_by_name(company_name)
    
    def _extract_background_from_linkedin(self, profile_data: str) -> str:
        """Extract background information from LinkedIn profile data."""
        try:
            # Simple extraction - in a real implementation, you might want to parse the markdown
            # For now, return a summary of the profile
            lines = profile_data.split('\n')
            background_lines = []
            
            for line in lines:
                if any(keyword in line.lower() for keyword in ['experience', 'education', 'skills', 'certification']):
                    background_lines.append(line.strip())
            
            return '\n'.join(background_lines[:10])  # Limit to first 10 relevant lines
        except Exception as e:
            logger.error(f"Error extracting background: {e}")
            return "Background information not available"
    
    def _generate_talking_points(self, participant: Dict[str, Any], all_participants: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Generate talking points for a participant based on their objectives and other participants.
        
        Args:
            participant: Current participant data
            all_participants: All participants in the meeting
            
        Returns:
            Dictionary of talking points for each other participant
        """
        try:
            if not self.settings.openai_api_key:
                return self._create_fallback_talking_points(participant, all_participants)
            
            # Get prompts from prompts directory
            system_prompt = get_meeting_talking_points_system_prompt()
            user_prompt = get_meeting_talking_points_user_prompt(participant, all_participants)
            
            logger.info(f"Generating talking points for {participant.get('name', 'Unknown')}")
            
            # Call OpenAI API
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {
                        "role": "system",
                        "content": system_prompt
                    },
                    {
                        "role": "user",
                        "content": user_prompt
                    }
                ],
                max_tokens=1500,
                temperature=0.3
            )
            
            # Extract the generated talking points
            llm_response = response.choices[0].message.content.strip()
            
            # Parse the LLM response
            talking_points = self._parse_talking_points_response(llm_response, all_participants)
            
            return talking_points
            
        except Exception as e:
            logger.error(f"Error generating talking points: {e}")
            return self._create_fallback_talking_points(participant, all_participants)
    
    def _parse_talking_points_response(self, llm_response: str, all_participants: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Parse LLM response into structured talking points."""
        try:
            # Try to extract JSON from the response
            import re
            json_match = re.search(r'\{.*\}', llm_response, re.DOTALL)
            
            if json_match:
                json_str = json_match.group(0)
                parsed_data = json.loads(json_str)
                return parsed_data
            else:
                # If JSON parsing fails, create structured format from text
                return self._create_structured_talking_points_from_text(llm_response, all_participants)
                
        except Exception as e:
            logger.error(f"Error parsing talking points response: {e}")
            return self._create_structured_talking_points_from_text(llm_response, all_participants)
    
    def _create_structured_talking_points_from_text(self, llm_response: str, all_participants: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Create structured talking points from LLM text response."""
        talking_points = {}
        
        for participant in all_participants:
            participant_name = participant.get('name', 'Unknown')
            talking_points[participant_name] = [
                "Discuss mutual interests and potential collaboration opportunities",
                "Share relevant experience and expertise",
                "Explore how we can help each other achieve our objectives"
            ]
        
        return talking_points
    
    def _create_fallback_talking_points(self, participant: Dict[str, Any], all_participants: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Create basic fallback talking points when LLM fails."""
        talking_points = {}
        
        for other_participant in all_participants:
            if other_participant.get('name') != participant.get('name'):
                talking_points[other_participant.get('name', 'Unknown')] = [
                    "Introduce yourself and your background",
                    "Share your meeting objectives",
                    "Discuss potential areas of collaboration",
                    "Ask about their expertise and interests"
                ]
        
        return talking_points 