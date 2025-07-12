import csv
import os
from datetime import datetime
from typing import Dict, Optional, List
from ..configs.settings import get_settings
from .logger import setup_logger

logger = setup_logger(__name__)

class CSVManager:
    def __init__(self):
        settings = get_settings()
        self.csv_file = settings.user_profiles_csv
        self._ensure_csv_exists()
    
    def _ensure_csv_exists(self):
        """Ensure the CSV file exists with proper headers."""
        if not os.path.exists(self.csv_file):
            os.makedirs(os.path.dirname(self.csv_file), exist_ok=True)
            with open(self.csv_file, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(['user_id', 'name', 'company', 'linkedin_url', 'created_date', 'last_updated'])
            logger.info(f"Created new CSV file: {self.csv_file}")
    
    def get_next_user_id(self) -> int:
        """Get the next available user ID."""
        if not os.path.exists(self.csv_file):
            return 1
        
        with open(self.csv_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            user_ids = [int(row['user_id']) for row in reader if row['user_id'].isdigit()]
            return max(user_ids) + 1 if user_ids else 1
    
    def find_user_by_linkedin_url(self, linkedin_url: str) -> Optional[Dict]:
        """Find user by LinkedIn URL."""
        if not os.path.exists(self.csv_file):
            return None
        
        with open(self.csv_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['linkedin_url'] == linkedin_url:
                    return row
        return None
    
    def add_user(self, name: str, company: str, linkedin_url: str) -> int:
        """Add a new user to the CSV file."""
        user_id = self.get_next_user_id()
        current_time = datetime.now().isoformat()
        
        with open(self.csv_file, 'a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([user_id, name, company, linkedin_url, current_time, current_time])
        
        logger.info(f"Added new user: {name} (ID: {user_id})")
        return user_id
    
    def update_user(self, user_id: int, name: str, company: str, linkedin_url: str):
        """Update an existing user in the CSV file."""
        rows = []
        updated = False
        
        with open(self.csv_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if int(row['user_id']) == user_id:
                    row['name'] = name
                    row['company'] = company
                    row['linkedin_url'] = linkedin_url
                    row['last_updated'] = datetime.now().isoformat()
                    updated = True
                rows.append(row)
        
        if updated:
            with open(self.csv_file, 'w', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=['user_id', 'name', 'company', 'linkedin_url', 'created_date', 'last_updated'])
                writer.writeheader()
                writer.writerows(rows)
            logger.info(f"Updated user: {name} (ID: {user_id})")
        else:
            logger.warning(f"User with ID {user_id} not found for update")
    
    def get_all_users(self) -> List[Dict]:
        """Get all users from the CSV file."""
        if not os.path.exists(self.csv_file):
            return []
        
        with open(self.csv_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            return list(reader) 