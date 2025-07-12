import os
import json
from typing import Dict, Any, Optional
import logging
from ..configs.settings import get_settings

logger = logging.getLogger(__name__)

class CompanyFileManager:
    """Manages file operations for company data."""
    
    def __init__(self):
        self.settings = get_settings()
        self.base_dir = self.settings.company_data_dir
    
    def _get_company_dir(self, company_id: str) -> str:
        """Get the directory path for a specific company."""
        return os.path.join(self.base_dir, company_id)
    
    def _ensure_company_dir(self, company_id: str) -> str:
        """Ensure the company directory exists."""
        company_dir = self._get_company_dir(company_id)
        os.makedirs(company_dir, exist_ok=True)
        return company_dir
    
    def save_company_data(self, company_id: str, data: Dict[str, Any]) -> bool:
        """
        Save company research data as JSON and markdown files.
        
        Args:
            company_id: Company identifier
            data: Research data to save
            
        Returns:
            True if successful, False otherwise
        """
        try:
            company_dir = self._ensure_company_dir(company_id)
            
            # Save as JSON
            json_file = os.path.join(company_dir, "research_data.json")
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            # Save as markdown
            markdown_file = os.path.join(company_dir, "research_data.md")
            markdown_content = self._convert_to_markdown(data)
            with open(markdown_file, 'w', encoding='utf-8') as f:
                f.write(markdown_content)
            
            logger.info(f"Saved company data for {company_id}: JSON and Markdown")
            return True
            
        except Exception as e:
            logger.error(f"Error saving company data for {company_id}: {e}")
            return False
    
    def get_company_data(self, company_id: str) -> Optional[Dict[str, Any]]:
        """
        Get company research data from JSON file.
        
        Args:
            company_id: Company identifier
            
        Returns:
            Dictionary with research data or None if not found
        """
        try:
            company_dir = self._get_company_dir(company_id)
            json_file = os.path.join(company_dir, "research_data.json")
            
            if not os.path.exists(json_file):
                return None
            
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            return data
            
        except Exception as e:
            logger.error(f"Error reading company data for {company_id}: {e}")
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
            company_dir = self._get_company_dir(company_id)
            markdown_file = os.path.join(company_dir, "research_data.md")
            
            if not os.path.exists(markdown_file):
                return None
            
            with open(markdown_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            return content
            
        except Exception as e:
            logger.error(f"Error reading company markdown for {company_id}: {e}")
            return None
    
    def company_data_exists(self, company_id: str) -> bool:
        """
        Check if company data exists.
        
        Args:
            company_id: Company identifier
            
        Returns:
            True if data exists, False otherwise
        """
        company_dir = self._get_company_dir(company_id)
        json_file = os.path.join(company_dir, "research_data.json")
        return os.path.exists(json_file)
    
    def _convert_to_markdown(self, data: Dict[str, Any]) -> str:
        """
        Convert company research data to markdown format.
        
        Args:
            data: Research data dictionary
            
        Returns:
            Formatted markdown string
        """
        markdown_lines = []
        
        # Header
        markdown_lines.append("# Company Research Report")
        markdown_lines.append("")
        
        # Metadata
        if 'search_timestamp' in data:
            markdown_lines.append(f"**Research Date:** {data['search_timestamp']}")
            markdown_lines.append("")
        
        # Answer section
        if 'answer' in data:
            markdown_lines.append("## Summary")
            markdown_lines.append("")
            markdown_lines.append(data['answer'])
            markdown_lines.append("")
        
        # Results section
        if 'results' in data and data['results']:
            markdown_lines.append("## Research Results")
            markdown_lines.append("")
            
            for i, result in enumerate(data['results'], 1):
                markdown_lines.append(f"### Result {i}")
                markdown_lines.append("")
                
                if 'title' in result:
                    markdown_lines.append(f"**Title:** {result['title']}")
                    markdown_lines.append("")
                
                if 'url' in result:
                    markdown_lines.append(f"**URL:** {result['url']}")
                    markdown_lines.append("")
                
                if 'content' in result:
                    markdown_lines.append("**Content:**")
                    markdown_lines.append("")
                    markdown_lines.append(result['content'])
                    markdown_lines.append("")
                
                markdown_lines.append("---")
                markdown_lines.append("")
        
        # Raw content section
        if 'raw_content' in data and data['raw_content']:
            markdown_lines.append("## Raw Content")
            markdown_lines.append("")
            
            for i, content in enumerate(data['raw_content'], 1):
                markdown_lines.append(f"### Raw Content {i}")
                markdown_lines.append("")
                
                if 'title' in content:
                    markdown_lines.append(f"**Title:** {content['title']}")
                    markdown_lines.append("")
                
                if 'url' in content:
                    markdown_lines.append(f"**URL:** {content['url']}")
                    markdown_lines.append("")
                
                if 'content' in content:
                    markdown_lines.append("**Content:**")
                    markdown_lines.append("")
                    markdown_lines.append(content['content'])
                    markdown_lines.append("")
                
                markdown_lines.append("---")
                markdown_lines.append("")
        
        # Additional info
        if 'additional_info' in data:
            markdown_lines.append("## Additional Information")
            markdown_lines.append("")
            markdown_lines.append(str(data['additional_info']))
            markdown_lines.append("")
        
        return "\n".join(markdown_lines) 