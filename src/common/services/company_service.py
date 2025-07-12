import uuid
import re
from typing import Dict, Any, Optional
import logging
from ..utils.tavily_client import TavilyClient
from ..utils.company_csv_manager import CompanyCSVManager
from ..utils.company_file_manager import CompanyFileManager

logger = logging.getLogger(__name__)

class CompanyService:
    """Service for company research and data management."""
    
    def __init__(self):
        self.tavily_client = TavilyClient()
        self.csv_manager = CompanyCSVManager()
        self.file_manager = CompanyFileManager()
    
    def research_company(self, company_name: Optional[str], website_url: str) -> Dict[str, Any]:
        """
        Research a company and store the results.
        
        Args:
            company_name: Optional company name
            website_url: Company website URL
            
        Returns:
            Dictionary with research results and metadata
        """
        try:
            # Check if company already exists by website URL
            existing_company = self._find_company_by_website(website_url)
            
            if existing_company:
                # Update existing company
                company_id = existing_company['company_id']
                logger.info(f"Updating existing company: {company_id} for website: {website_url}")
            else:
                # Create new company with UUID
                company_id = str(uuid.uuid4())
                logger.info(f"Creating new company: {company_id} for website: {website_url}")
            
            # Research company using Tavily
            logger.info(f"Starting company research for: {website_url}")
            research_data = self.tavily_client.research_company(company_name, website_url)
            
            # Extract company name from research if not provided
            if not company_name:
                company_name = self._extract_company_name(research_data, website_url)
            
            # Add metadata to research data
            research_data['metadata'] = {
                'company_id': company_id,
                'company_name': company_name,
                'company_website': website_url,
                'research_timestamp': research_data.get('search_timestamp', ''),
                'is_update': existing_company is not None
            }
            
            # Save data to files
            if self.file_manager.save_company_data(company_id, research_data):
                # Update CSV
                if existing_company:
                    self.csv_manager.update_company(company_id)
                else:
                    self.csv_manager.add_company(company_id, website_url)
                
                logger.info(f"Successfully researched and stored company: {company_id}")
                
                return {
                    'company_id': company_id,
                    'company_name': company_name,
                    'company_website': website_url,
                    'status': 'updated' if existing_company else 'created',
                    'message': f"Company research {'updated' if existing_company else 'completed'} successfully"
                }
            else:
                logger.error(f"Failed to save company data for: {company_id}")
                return {
                    'status': 'error',
                    'message': 'Failed to save company data'
                }
                
        except Exception as e:
            logger.error(f"Error researching company: {e}")
            return {
                'status': 'error',
                'message': f'Research failed: {str(e)}'
            }
    
    def _find_company_by_website(self, website_url: str) -> Optional[Dict]:
        """
        Find existing company by website URL.
        
        Args:
            website_url: Company website URL
            
        Returns:
            Company data if found, None otherwise
        """
        try:
            companies = self.csv_manager.get_all_companies()
            for company in companies:
                if company['company_website'] == website_url:
                    return company
            return None
        except Exception as e:
            logger.error(f"Error finding company by website: {e}")
            return None
    
    def get_company_data(self, company_id: str) -> Optional[Dict[str, Any]]:
        """
        Get company research data.
        
        Args:
            company_id: Company identifier
            
        Returns:
            Company data or None if not found
        """
        try:
            # Check if company exists in CSV
            csv_data = self.csv_manager.get_company(company_id)
            if not csv_data:
                logger.warning(f"Company not found in CSV: {company_id}")
                return None
            
            # Get research data
            research_data = self.file_manager.get_company_data(company_id)
            if not research_data:
                logger.warning(f"Company research data not found: {company_id}")
                return None
            
            # Combine CSV and research data
            result = {
                'company_id': company_id,
                'company_website': csv_data['company_website'],
                'create_date': csv_data['create_date'],
                'last_updated': csv_data['last_updated'],
                'research_data': research_data
            }
            
            return result
            
        except Exception as e:
            logger.error(f"Error getting company data for {company_id}: {e}")
            return None
    
    def get_company_markdown(self, company_id: str) -> Optional[str]:
        """
        Get company research data as markdown.
        
        Args:
            company_id: Company identifier
            
        Returns:
            Markdown content or None if not found
        """
        try:
            return self.file_manager.get_company_markdown(company_id)
        except Exception as e:
            logger.error(f"Error getting company markdown for {company_id}: {e}")
            return None
    
    def get_all_companies(self) -> list:
        """
        Get all companies from the CSV.
        
        Returns:
            List of company data dictionaries
        """
        try:
            return self.csv_manager.get_all_companies()
        except Exception as e:
            logger.error(f"Error getting all companies: {e}")
            return []
    
    def _extract_company_name(self, research_data: Dict[str, Any], website_url: str) -> str:
        """
        Extract company name from research data or website URL.
        
        Args:
            research_data: Research data from Tavily
            website_url: Company website URL
            
        Returns:
            Extracted company name
        """
        # Try to extract from answer first
        if 'answer' in research_data and research_data['answer']:
            # Look for company name patterns in the answer
            answer = research_data['answer']
            
            # Common patterns for company names
            patterns = [
                r'(\w+(?:\s+\w+){0,3})\s+(?:is|was|has been|remains)\s+(?:a|an)\s+(?:company|corporation|organization|business|firm)',
                r'(?:company|corporation|organization|business|firm)\s+(\w+(?:\s+\w+){0,3})',
                r'(\w+(?:\s+\w+){0,3})\s+(?:Inc\.|LLC|Ltd\.|Corp\.|Corporation|Company)',
            ]
            
            for pattern in patterns:
                match = re.search(pattern, answer, re.IGNORECASE)
                if match:
                    return match.group(1).strip()
        
        # Try to extract from results
        if 'results' in research_data and research_data['results']:
            for result in research_data['results']:
                if 'title' in result and result['title']:
                    title = result['title']
                    # Look for company name in title
                    patterns = [
                        r'(\w+(?:\s+\w+){0,3})\s+(?:Inc\.|LLC|Ltd\.|Corp\.|Corporation|Company)',
                        r'(\w+(?:\s+\w+){0,3})\s+-\s+',
                    ]
                    
                    for pattern in patterns:
                        match = re.search(pattern, title, re.IGNORECASE)
                        if match:
                            return match.group(1).strip()
        
        # Fallback: extract from domain
        try:
            domain = website_url.replace('https://', '').replace('http://', '').split('/')[0]
            # Remove www. prefix
            if domain.startswith('www.'):
                domain = domain[4:]
            
            # Convert domain to readable name
            name = domain.replace('.com', '').replace('.org', '').replace('.net', '')
            name = name.replace('-', ' ').replace('_', ' ')
            
            # Capitalize words
            name = ' '.join(word.capitalize() for word in name.split())
            
            return name
            
        except Exception:
            return "Unknown Company" 