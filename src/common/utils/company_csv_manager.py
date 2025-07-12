import csv
import os
from datetime import datetime
from typing import Dict, List, Optional
import logging
from ..configs.settings import get_settings

logger = logging.getLogger(__name__)

class CompanyCSVManager:
    """Manages company data in CSV format."""
    
    def __init__(self):
        self.settings = get_settings()
        self.csv_file = self.settings.company_csv_file
        self._ensure_csv_exists()
    
    def _ensure_csv_exists(self):
        """Ensure the CSV file exists with proper headers."""
        if not os.path.exists(self.csv_file):
            os.makedirs(os.path.dirname(self.csv_file), exist_ok=True)
            
            with open(self.csv_file, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(['company_id', 'company_website', 'create_date', 'last_updated'])
            
            logger.info(f"Created new company CSV file: {self.csv_file}")
    
    def add_company(self, company_id: str, company_website: str) -> bool:
        """
        Add a new company to the CSV.
        
        Args:
            company_id: Unique identifier for the company
            company_website: Company website URL
            
        Returns:
            True if successful, False otherwise
        """
        try:
            current_time = datetime.now().isoformat()
            
            with open(self.csv_file, 'a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow([company_id, company_website, current_time, current_time])
            
            logger.info(f"Added company to CSV: {company_id} - {company_website}")
            return True
            
        except Exception as e:
            logger.error(f"Error adding company to CSV: {e}")
            return False
    
    def update_company(self, company_id: str) -> bool:
        """
        Update the last_updated timestamp for a company.
        
        Args:
            company_id: Company identifier
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Read all rows
            rows = []
            with open(self.csv_file, 'r', newline='', encoding='utf-8') as file:
                reader = csv.reader(file)
                header = next(reader)  # Skip header
                rows.append(header)
                
                for row in reader:
                    if row[0] == company_id:
                        # Update the last_updated field
                        row[3] = datetime.now().isoformat()
                    rows.append(row)
            
            # Write back all rows
            with open(self.csv_file, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerows(rows)
            
            logger.info(f"Updated company in CSV: {company_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error updating company in CSV: {e}")
            return False
    
    def get_company(self, company_id: str) -> Optional[Dict]:
        """
        Get company information from CSV.
        
        Args:
            company_id: Company identifier
            
        Returns:
            Dictionary with company data or None if not found
        """
        try:
            with open(self.csv_file, 'r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row['company_id'] == company_id:
                        return row
            
            return None
            
        except Exception as e:
            logger.error(f"Error getting company from CSV: {e}")
            return None
    
    def company_exists(self, company_id: str) -> bool:
        """
        Check if a company exists in the CSV.
        
        Args:
            company_id: Company identifier
            
        Returns:
            True if company exists, False otherwise
        """
        return self.get_company(company_id) is not None
    
    def get_all_companies(self) -> List[Dict]:
        """
        Get all companies from the CSV.
        
        Returns:
            List of dictionaries containing company data
        """
        try:
            companies = []
            with open(self.csv_file, 'r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    companies.append(row)
            
            return companies
            
        except Exception as e:
            logger.error(f"Error getting all companies from CSV: {e}")
            return [] 