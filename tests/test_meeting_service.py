import pytest
import json
import os
from unittest.mock import Mock, patch, MagicMock
from src.common.services.meeting_service import MeetingService
from src.common.utils.meeting_csv_manager import MeetingCSVManager
from src.common.utils.meeting_file_manager import MeetingFileManager

class TestMeetingService:
    """Test cases for MeetingService."""
    
    @pytest.fixture
    def meeting_service(self):
        """Create a MeetingService instance for testing."""
        return MeetingService()
    
    @pytest.fixture
    def sample_participants(self):
        """Sample participant data for testing."""
        return [
            {
                "name": "John Doe",
                "company": "Tech Corp",
                "user_id": 1,
                "company_id": "tech-corp-123",
                "linkedin_url": "https://linkedin.com/in/johndoe",
                "background": "Software engineer with 10 years experience",
                "what_they_offer": "AI/ML expertise, technical consulting, development resources",
                "meeting_objective": "Find potential partners for AI project",
                "looking_for": "Companies working on AI/ML solutions, funding opportunities"
            },
            {
                "name": "Jane Smith",
                "company": "Data Solutions Inc",
                "user_id": 2,
                "company_id": "data-solutions-456",
                "linkedin_url": "https://linkedin.com/in/janesmith",
                "background": "Data scientist and business analyst",
                "what_they_offer": "Data analytics services, market research, business intelligence",
                "meeting_objective": "Explore collaboration opportunities",
                "looking_for": "Technical expertise and market insights"
            }
        ]
    
    def test_create_meeting_success(self, meeting_service, sample_participants):
        """Test successful meeting creation."""
        with patch.object(meeting_service, '_process_participants') as mock_process, \
             patch.object(meeting_service, '_generate_talking_points') as mock_generate, \
             patch.object(meeting_service.file_manager, 'save_meeting_data') as mock_save, \
             patch.object(meeting_service.csv_manager, 'create_meeting') as mock_csv_create:
            
            # Mock return values
            mock_process.return_value = sample_participants
            mock_generate.return_value = {"John Doe": ["Point 1", "Point 2"]}
            mock_save.return_value = True
            mock_csv_create.return_value = True
            
            # Test meeting creation
            result = meeting_service.create_meeting(
                meeting_title="Test Meeting",
                meeting_date="2024-01-15",
                participants=sample_participants
            )
            
            # Assertions
            assert result['status'] == 'success'
            assert 'meeting_id' in result
            assert result['participant_count'] == 2
            assert result['message'] == 'Meeting created successfully'
            
            # Verify method calls
            mock_process.assert_called_once_with(sample_participants)
            assert mock_generate.call_count == 2  # Called for each participant
            mock_save.assert_called_once()
            mock_csv_create.assert_called_once()
    
    def test_create_meeting_with_pydantic_models(self, meeting_service, sample_participants):
        """Test meeting creation with Pydantic model participants."""
        # Create mock Pydantic models
        class MockParticipant:
            def __init__(self, data):
                self.data = data
            
            def dict(self):
                return self.data
        
        pydantic_participants = [MockParticipant(participant) for participant in sample_participants]
        
        with patch.object(meeting_service, '_process_participants') as mock_process, \
             patch.object(meeting_service, '_generate_talking_points') as mock_generate, \
             patch.object(meeting_service.file_manager, 'save_meeting_data') as mock_save, \
             patch.object(meeting_service.csv_manager, 'create_meeting') as mock_csv_create:
            
            # Mock return values
            mock_process.return_value = sample_participants
            mock_generate.return_value = {"John Doe": ["Point 1", "Point 2"]}
            mock_save.return_value = True
            mock_csv_create.return_value = True
            
            # Test meeting creation with Pydantic models
            result = meeting_service.create_meeting(
                meeting_title="Test Meeting",
                meeting_date="2024-01-15",
                participants=pydantic_participants
            )
            
            # Assertions
            assert result['status'] == 'success'
            assert 'meeting_id' in result
            assert result['participant_count'] == 2
            assert result['message'] == 'Meeting created successfully'
            
            # Verify method calls
            mock_process.assert_called_once_with(sample_participants)
            assert mock_generate.call_count == 2  # Called for each participant
            mock_save.assert_called_once()
            mock_csv_create.assert_called_once()
    
    def test_create_meeting_save_failure(self, meeting_service, sample_participants):
        """Test meeting creation when file save fails."""
        with patch.object(meeting_service, '_process_participants') as mock_process, \
             patch.object(meeting_service, '_generate_talking_points') as mock_generate, \
             patch.object(meeting_service.file_manager, 'save_meeting_data') as mock_save:
            
            # Mock return values
            mock_process.return_value = sample_participants
            mock_generate.return_value = {"John Doe": ["Point 1", "Point 2"]}
            mock_save.return_value = False  # Simulate save failure
            
            # Test meeting creation
            result = meeting_service.create_meeting(
                meeting_title="Test Meeting",
                meeting_date="2024-01-15",
                participants=sample_participants
            )
            
            # Assertions
            assert result['status'] == 'error'
            assert result['message'] == 'Failed to save meeting data'
    
    def test_get_meeting_success(self, meeting_service):
        """Test successful meeting retrieval."""
        expected_data = {
            'meeting_id': 'test-123',
            'meeting_title': 'Test Meeting',
            'participants': []
        }
        
        with patch.object(meeting_service.file_manager, 'load_meeting_data') as mock_load, \
             patch.object(meeting_service.csv_manager, 'get_meeting') as mock_csv_get:
            
            mock_load.return_value = expected_data
            mock_csv_get.return_value = {'created_date': '2024-01-01'}
            
            result = meeting_service.get_meeting('test-123')
            
            assert result == expected_data
            assert result['csv_metadata'] == {'created_date': '2024-01-01'}
    
    def test_get_meeting_not_found(self, meeting_service):
        """Test meeting retrieval when meeting doesn't exist."""
        with patch.object(meeting_service.file_manager, 'load_meeting_data') as mock_load:
            mock_load.return_value = None
            
            result = meeting_service.get_meeting('nonexistent-123')
            
            assert result is None
    
    def test_get_all_meetings(self, meeting_service):
        """Test retrieval of all meetings."""
        expected_meetings = [
            {'meeting_id': 'meeting-1', 'title': 'Meeting 1'},
            {'meeting_id': 'meeting-2', 'title': 'Meeting 2'}
        ]
        
        with patch.object(meeting_service.csv_manager, 'get_all_meetings') as mock_get_all:
            mock_get_all.return_value = expected_meetings
            
            result = meeting_service.get_all_meetings()
            
            assert result == expected_meetings
    
    def test_process_participants(self, meeting_service, sample_participants):
        """Test participant processing."""
        with patch.object(meeting_service, '_get_linkedin_data_by_user_id') as mock_linkedin, \
             patch.object(meeting_service, '_get_company_data_by_id') as mock_company:
            
            mock_linkedin.return_value = {'linkedin_profile': 'profile data'}
            mock_company.return_value = {'company_info': 'company data'}
            
            result = meeting_service._process_participants(sample_participants)
            
            assert len(result) == 2
            assert result[0]['linkedin_profile'] == 'profile data'
            assert result[0]['company_info'] == 'company data'
    
    def test_generate_talking_points_with_openai(self, meeting_service, sample_participants):
        """Test talking points generation with OpenAI."""
        with patch('openai.ChatCompletion.create') as mock_openai, \
             patch.object(meeting_service, 'settings') as mock_settings:
            
            mock_settings.openai_api_key = 'test-key'
            mock_openai.return_value.choices[0].message.content = '{"John Doe": ["Point 1", "Point 2"]}'
            
            result = meeting_service._generate_talking_points(sample_participants[0], sample_participants)
            
            assert result == {"John Doe": ["Point 1", "Point 2"]}
            mock_openai.assert_called_once()
    
    def test_generate_talking_points_fallback(self, meeting_service, sample_participants):
        """Test talking points generation fallback when OpenAI fails."""
        with patch.object(meeting_service, 'settings') as mock_settings:
            mock_settings.openai_api_key = None  # No API key
            
            result = meeting_service._generate_talking_points(sample_participants[0], sample_participants)
            
            # Should return fallback talking points
            assert isinstance(result, dict)
            assert len(result) > 0
    
    def test_parse_talking_points_response_json(self, meeting_service, sample_participants):
        """Test parsing JSON talking points response."""
        json_response = '{"John Doe": ["Point 1", "Point 2"], "Jane Smith": ["Point 3"]}'
        
        result = meeting_service._parse_talking_points_response(json_response, sample_participants)
        
        assert result == {"John Doe": ["Point 1", "Point 2"], "Jane Smith": ["Point 3"]}
    
    def test_parse_talking_points_response_text(self, meeting_service, sample_participants):
        """Test parsing text talking points response."""
        text_response = "Here are some talking points for the meeting..."
        
        result = meeting_service._parse_talking_points_response(text_response, sample_participants)
        
        assert isinstance(result, dict)
        assert len(result) > 0
    
    def test_extract_background_from_linkedin(self, meeting_service):
        """Test LinkedIn background extraction."""
        profile_data = """
        # John Doe
        ## Experience
        - Software Engineer at Tech Corp
        ## Education
        - BS Computer Science
        ## Skills
        - Python, JavaScript
        """
        
        result = meeting_service._extract_background_from_linkedin(profile_data)
        
        assert "Experience" in result
        assert "Education" in result
        assert "Skills" in result


class TestMeetingCSVManager:
    """Test cases for MeetingCSVManager."""
    
    @pytest.fixture
    def csv_manager(self, tmp_path):
        """Create a MeetingCSVManager instance for testing."""
        csv_file = tmp_path / "test_meetings.csv"
        return MeetingCSVManager(str(csv_file))
    
    def test_create_meeting(self, csv_manager):
        """Test meeting creation in CSV."""
        result = csv_manager.create_meeting(
            meeting_id="test-123",
            meeting_title="Test Meeting",
            meeting_date="2024-01-15",
            participant_count=3
        )
        
        assert result is True
        
        # Verify the meeting was created
        meeting = csv_manager.get_meeting("test-123")
        assert meeting is not None
        assert meeting['meeting_id'] == "test-123"
        assert meeting['meeting_title'] == "Test Meeting"
    
    def test_get_meeting_not_found(self, csv_manager):
        """Test getting non-existent meeting."""
        result = csv_manager.get_meeting("nonexistent-123")
        assert result is None
    
    def test_get_all_meetings(self, csv_manager):
        """Test getting all meetings."""
        # Create multiple meetings
        csv_manager.create_meeting("meeting-1", "Meeting 1", "2024-01-15", 2)
        csv_manager.create_meeting("meeting-2", "Meeting 2", "2024-01-16", 3)
        
        meetings = csv_manager.get_all_meetings()
        
        assert len(meetings) == 2
        assert meetings[0]['meeting_id'] == "meeting-1"
        assert meetings[1]['meeting_id'] == "meeting-2"
    
    def test_update_meeting(self, csv_manager):
        """Test meeting update."""
        # Create a meeting
        csv_manager.create_meeting("test-123", "Original Title", "2024-01-15", 2)
        
        # Update the meeting
        result = csv_manager.update_meeting("test-123", meeting_title="Updated Title")
        
        assert result is True
        
        # Verify the update
        meeting = csv_manager.get_meeting("test-123")
        assert meeting['meeting_title'] == "Updated Title"


class TestMeetingFileManager:
    """Test cases for MeetingFileManager."""
    
    @pytest.fixture
    def file_manager(self, tmp_path):
        """Create a MeetingFileManager instance for testing."""
        base_dir = tmp_path / "test_meetings"
        return MeetingFileManager(str(base_dir))
    
    def test_save_and_load_meeting_data(self, file_manager):
        """Test saving and loading meeting data."""
        meeting_data = {
            'meeting_id': 'test-123',
            'meeting_title': 'Test Meeting',
            'participants': [
                {'name': 'John Doe', 'company': 'Tech Corp'}
            ]
        }
        
        # Save meeting data
        result = file_manager.save_meeting_data('test-123', meeting_data)
        assert result is True
        
        # Load meeting data
        loaded_data = file_manager.load_meeting_data('test-123')
        assert loaded_data is not None
        assert loaded_data['meeting_id'] == 'test-123'
        assert loaded_data['meeting_title'] == 'Test Meeting'
        assert len(loaded_data['participants']) == 1
    
    def test_load_meeting_data_not_found(self, file_manager):
        """Test loading non-existent meeting data."""
        result = file_manager.load_meeting_data('nonexistent-123')
        assert result is None
    
    def test_convert_meeting_to_markdown(self, file_manager):
        """Test meeting data to markdown conversion."""
        meeting_data = {
            'meeting_id': 'test-123',
            'meeting_title': 'Test Meeting',
            'meeting_date': '2024-01-15',
            'created_date': '2024-01-01',
            'participants': [
                {
                    'name': 'John Doe',
                    'company': 'Tech Corp',
                    'linkedin_url': 'https://linkedin.com/in/johndoe',
                    'background': 'Software Engineer',
                    'what_they_offer': 'AI/ML expertise and technical consulting',
                    'meeting_objective': 'Find partners',
                    'looking_for': 'AI companies',
                    'talking_points': {
                        'Jane Smith': ['Point 1', 'Point 2']
                    }
                }
            ]
        }
        
        markdown = file_manager._convert_meeting_to_markdown(meeting_data)
        
        assert '# Test Meeting' in markdown
        assert 'John Doe' in markdown
        assert 'Tech Corp' in markdown
        assert 'Find partners' in markdown
        assert 'AI/ML expertise and technical consulting' in markdown 