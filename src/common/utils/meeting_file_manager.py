import json
import os
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

class MeetingFileManager:
    """Manages file storage for meeting data."""
    
    def __init__(self, base_dir: str = "data/meetings"):
        self.base_dir = base_dir
        os.makedirs(base_dir, exist_ok=True)
    
    def save_meeting_data(self, meeting_id: str, meeting_data: Dict[str, Any]) -> bool:
        """Save meeting data to JSON and markdown files."""
        try:
            meeting_dir = os.path.join(self.base_dir, meeting_id)
            os.makedirs(meeting_dir, exist_ok=True)
            
            # Save as JSON
            json_file = os.path.join(meeting_dir, "meeting_data.json")
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(meeting_data, f, indent=2, ensure_ascii=False)
            
            # Save as markdown
            markdown_file = os.path.join(meeting_dir, "meeting_data.md")
            markdown_content = self._convert_meeting_to_markdown(meeting_data)
            with open(markdown_file, 'w', encoding='utf-8') as f:
                f.write(markdown_content)
            
            logger.info(f"Saved meeting data for: {meeting_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error saving meeting data for {meeting_id}: {e}")
            return False
    
    def load_meeting_data(self, meeting_id: str) -> Optional[Dict[str, Any]]:
        """Load meeting data from JSON file."""
        try:
            meeting_dir = os.path.join(self.base_dir, meeting_id)
            json_file = os.path.join(meeting_dir, "meeting_data.json")
            
            if not os.path.exists(json_file):
                return None
            
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            return data
            
        except Exception as e:
            logger.error(f"Error loading meeting data for {meeting_id}: {e}")
            return None
    
    def _convert_meeting_to_markdown(self, meeting_data: Dict[str, Any]) -> str:
        """Convert meeting data to markdown format."""
        markdown_lines = []
        
        # Header
        markdown_lines.append(f"# Meeting: {meeting_data.get('meeting_title', 'Untitled')}")
        markdown_lines.append("")
        
        # Meeting Info
        markdown_lines.append("## Meeting Information")
        markdown_lines.append("")
        markdown_lines.append(f"**Meeting ID:** {meeting_data.get('meeting_id', 'N/A')}")
        markdown_lines.append(f"**Date:** {meeting_data.get('meeting_date', 'N/A')}")
        markdown_lines.append(f"**Created:** {meeting_data.get('created_date', 'N/A')}")
        markdown_lines.append("")
        
        # Participants
        participants = meeting_data.get('participants', [])
        if participants:
            markdown_lines.append("## Participants")
            markdown_lines.append("")
            
            for i, participant in enumerate(participants, 1):
                markdown_lines.append(f"### {i}. {participant.get('name', 'Unknown')}")
                markdown_lines.append("")
                
                # Basic Info
                if participant.get('company'):
                    markdown_lines.append(f"**Company:** {participant['company']}")
                if participant.get('linkedin_url'):
                    markdown_lines.append(f"**LinkedIn:** {participant['linkedin_url']}")
                if participant.get('background'):
                    markdown_lines.append(f"**Background:** {participant['background']}")
                if participant.get('what_they_offer'):
                    markdown_lines.append(f"**What They Have to Offer:** {participant['what_they_offer']}")
                markdown_lines.append("")
                
                # Meeting Objective
                if participant.get('meeting_objective'):
                    markdown_lines.append("**Meeting Objective:**")
                    markdown_lines.append(participant['meeting_objective'])
                    markdown_lines.append("")
                
                # What they're looking for
                if participant.get('looking_for'):
                    markdown_lines.append("**What They're Looking For:**")
                    markdown_lines.append(participant['looking_for'])
                    markdown_lines.append("")
                
                # Key Talking Points
                talking_points = participant.get('talking_points', {})
                if talking_points:
                    markdown_lines.append("**Key Talking Points:**")
                    markdown_lines.append("")
                    for target_user, points in talking_points.items():
                        markdown_lines.append(f"**To {target_user}:**")
                        if isinstance(points, list):
                            for point in points:
                                markdown_lines.append(f"- {point}")
                        else:
                            markdown_lines.append(f"- {points}")
                        markdown_lines.append("")
                
                markdown_lines.append("---")
                markdown_lines.append("")
        
        return "\n".join(markdown_lines) 