import csv
import os
from typing import List, Dict, Any, Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class MeetingCSVManager:
    """Manages CSV file for storing meeting information."""
    
    def __init__(self, csv_file: str = "data/meetings.csv"):
        self.csv_file = csv_file
        self._ensure_csv_exists()
    
    def _ensure_csv_exists(self):
        """Ensure the CSV file exists with proper headers."""
        if not os.path.exists(self.csv_file):
            os.makedirs(os.path.dirname(self.csv_file), exist_ok=True)
            
            with open(self.csv_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow([
                    'meeting_id',
                    'meeting_title',
                    'meeting_date',
                    'participant_count',
                    'created_date',
                    'last_updated'
                ])
            logger.info(f"Created new meetings CSV file: {self.csv_file}")
    
    def create_meeting(self, meeting_id: str, meeting_title: str, meeting_date: str, participant_count: int) -> bool:
        """Create a new meeting entry."""
        try:
            with open(self.csv_file, 'a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow([
                    meeting_id,
                    meeting_title,
                    meeting_date,
                    participant_count,
                    datetime.now().isoformat(),
                    datetime.now().isoformat()
                ])
            logger.info(f"Created meeting entry: {meeting_id}")
            return True
        except Exception as e:
            logger.error(f"Error creating meeting entry: {e}")
            return False
    
    def get_meeting(self, meeting_id: str) -> Optional[Dict[str, Any]]:
        """Get meeting information by ID."""
        try:
            with open(self.csv_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row['meeting_id'] == meeting_id:
                        return row
            return None
        except Exception as e:
            logger.error(f"Error getting meeting: {e}")
            return None
    
    def get_all_meetings(self) -> List[Dict[str, Any]]:
        """Get all meetings."""
        try:
            meetings = []
            with open(self.csv_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    meetings.append(row)
            return meetings
        except Exception as e:
            logger.error(f"Error getting all meetings: {e}")
            return []
    
    def update_meeting(self, meeting_id: str, **kwargs) -> bool:
        """Update meeting information."""
        try:
            meetings = []
            updated = False
            
            with open(self.csv_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row['meeting_id'] == meeting_id:
                        row.update(kwargs)
                        row['last_updated'] = datetime.now().isoformat()
                        updated = True
                    meetings.append(row)
            
            if updated:
                with open(self.csv_file, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.DictWriter(f, fieldnames=meetings[0].keys())
                    writer.writeheader()
                    writer.writerows(meetings)
                logger.info(f"Updated meeting: {meeting_id}")
                return True
            
            return False
        except Exception as e:
            logger.error(f"Error updating meeting: {e}")
            return False 