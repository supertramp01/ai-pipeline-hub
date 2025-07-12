import json
import os
from typing import Dict, Any, Optional
import logging
from datetime import datetime
import openai
from ..utils.company_file_manager import CompanyFileManager
from ..utils.company_csv_manager import CompanyCSVManager
from ..configs.settings import get_settings
from ..prompts.company_summary import (
    get_company_summary_system_prompt,
    get_company_summary_user_prompt
)

logger = logging.getLogger(__name__)

class CompanySummaryService:
    """Service for generating company summaries using LLM."""
    
    def __init__(self):
        self.file_manager = CompanyFileManager()
        self.csv_manager = CompanyCSVManager()
        self.settings = get_settings()
        
        # Initialize OpenAI client
        if self.settings.openai_api_key:
            openai.api_key = self.settings.openai_api_key
        else:
            logger.warning("OpenAI API key not found. LLM summarization will not work.")
    
    def generate_summary(self, company_id: Optional[str] = None, company_website: Optional[str] = None, user_prompt: Optional[str] = None) -> Dict[str, Any]:
        """
        Generate a company summary using LLM based on research data and optional user prompt.
        
        Args:
            company_id: Company identifier (optional if company_website provided)
            company_website: Company website URL (optional if company_id provided)
            user_prompt: Optional user prompt to guide summarization
            
        Returns:
            Dictionary with summary results and metadata
        """
        try:
            # Determine company_id if not provided
            if not company_id and company_website:
                company_id = self._find_company_id_by_website(company_website)
                if not company_id:
                    return {
                        'status': 'error',
                        'message': f'Company not found for website: {company_website}'
                    }
            
            if not company_id:
                return {
                    'status': 'error',
                    'message': 'Either company_id or company_website must be provided'
                }
            
            # Get company research data from raw files
            research_data = self._load_raw_research_data(company_id)
            if not research_data:
                return {
                    'status': 'error',
                    'message': f'Research data not found for company: {company_id}'
                }
            
            # Generate summary using LLM
            summary_data = self._generate_llm_summary(research_data, user_prompt)
            
            # Save summary
            if self._save_summary(company_id, summary_data):
                logger.info(f"Successfully generated and saved LLM summary for company: {company_id}")
                
                return {
                    'company_id': company_id,
                    'status': 'success',
                    'message': 'LLM summary generated successfully',
                    'summary': summary_data
                }
            else:
                return {
                    'status': 'error',
                    'message': 'Failed to save summary'
                }
                
        except Exception as e:
            logger.error(f"Error generating company summary: {e}")
            return {
                'status': 'error',
                'message': f'Summary generation failed: {str(e)}'
            }
    
    def get_summary(self, company_id: Optional[str] = None, company_website: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """
        Get existing company summary.
        
        Args:
            company_id: Company identifier (optional if company_website provided)
            company_website: Company website URL (optional if company_id provided)
            
        Returns:
            Summary data or None if not found
        """
        try:
            # Determine company_id if not provided
            if not company_id and company_website:
                company_id = self._find_company_id_by_website(company_website)
                if not company_id:
                    return None
            
            if not company_id:
                return None
            
            # Get summary data
            summary_data = self._load_summary(company_id)
            return summary_data
            
        except Exception as e:
            logger.error(f"Error getting company summary: {e}")
            return None
    
    def _find_company_id_by_website(self, website_url: str) -> Optional[str]:
        """Find company ID by website URL."""
        try:
            companies = self.csv_manager.get_all_companies()
            for company in companies:
                if company['company_website'] == website_url:
                    return company['company_id']
            return None
        except Exception as e:
            logger.error(f"Error finding company by website: {e}")
            return None
    
    def _load_raw_research_data(self, company_id: str) -> Optional[Dict[str, Any]]:
        """
        Load raw research data from the data directory.
        
        Args:
            company_id: Company identifier
            
        Returns:
            Raw research data or None if not found
        """
        try:
            company_dir = os.path.join(self.file_manager.base_dir, company_id)
            json_file = os.path.join(company_dir, "research_data.json")
            
            if not os.path.exists(json_file):
                logger.warning(f"Raw research data not found: {json_file}")
                return None
            
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            logger.info(f"Loaded raw research data for company: {company_id}")
            return data
            
        except Exception as e:
            logger.error(f"Error loading raw research data for {company_id}: {e}")
            return None
    
    def _generate_llm_summary(self, research_data: Dict[str, Any], user_prompt: Optional[str] = None) -> Dict[str, Any]:
        """
        Generate summary using LLM from raw research data.
        
        Args:
            research_data: Raw research data from Tavily
            user_prompt: Optional user prompt to guide summarization
            
        Returns:
            LLM-generated summary data
        """
        try:
            if not self.settings.openai_api_key:
                raise Exception("OpenAI API key not configured")
            
            # Get prompts from prompts directory
            system_prompt = get_company_summary_system_prompt()
            user_prompt_text = get_company_summary_user_prompt(research_data, user_prompt)
            
            logger.info(f"Generating LLM summary with prompt length: {len(user_prompt_text)}")
            
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
                        "content": user_prompt_text
                    }
                ],
                max_tokens=2000,
                temperature=0.3
            )
            
            # Extract the generated summary
            llm_summary = response.choices[0].message.content.strip()
            
            # Parse the LLM response into structured format
            summary_data = self._parse_llm_response(llm_summary, research_data, user_prompt)
            
            return summary_data
            
        except Exception as e:
            logger.error(f"Error generating LLM summary: {e}")
            # Fallback to basic summary if LLM fails
            return self._create_fallback_summary(research_data, user_prompt)
    
    def _parse_llm_response(self, llm_response: str, research_data: Dict[str, Any], user_prompt: Optional[str] = None) -> Dict[str, Any]:
        """
        Parse the LLM response into structured format.
        
        Args:
            llm_response: Raw LLM response
            research_data: Original research data
            user_prompt: Original user prompt
            
        Returns:
            Structured summary data
        """
        try:
            # Try to extract JSON from the response
            import re
            json_match = re.search(r'\{.*\}', llm_response, re.DOTALL)
            
            if json_match:
                json_str = json_match.group(0)
                parsed_data = json.loads(json_str)
                
                # Add metadata
                parsed_data['generated_at'] = datetime.now().isoformat()
                parsed_data['user_prompt'] = user_prompt
                parsed_data['llm_model'] = 'gpt-4'
                parsed_data['raw_llm_response'] = llm_response
                
                return parsed_data
            else:
                # If JSON parsing fails, create structured format from text
                return self._create_structured_from_text(llm_response, research_data, user_prompt)
                
        except Exception as e:
            logger.error(f"Error parsing LLM response: {e}")
            return self._create_structured_from_text(llm_response, research_data, user_prompt)
    
    def _create_structured_from_text(self, llm_response: str, research_data: Dict[str, Any], user_prompt: Optional[str] = None) -> Dict[str, Any]:
        """
        Create structured summary from LLM text response when JSON parsing fails.
        
        Args:
            llm_response: Raw LLM response
            research_data: Original research data
            user_prompt: Original user prompt
            
        Returns:
            Structured summary data
        """
        return {
            'generated_at': datetime.now().isoformat(),
            'user_prompt': user_prompt,
            'llm_model': 'gpt-4',
            'raw_llm_response': llm_response,
            'company_overview': llm_response[:1000],  # First 1000 chars as overview
            'key_statistics': [],
            'recent_news': [],
            'key_facts': [],
            'business_model': '',
            'products_services': [],
            'market_position': '',
            'financial_highlights': [],
            'leadership': '',
            'competitors': [],
            'opportunities': [],
            'risks': [],
            'insights': llm_response
        }
    
    def _create_fallback_summary(self, research_data: Dict[str, Any], user_prompt: Optional[str] = None) -> Dict[str, Any]:
        """
        Create a basic fallback summary when LLM fails.
        
        Args:
            research_data: Raw research data
            user_prompt: Original user prompt
            
        Returns:
            Basic summary data
        """
        return {
            'generated_at': datetime.now().isoformat(),
            'user_prompt': user_prompt,
            'llm_model': 'fallback',
            'company_overview': research_data.get('answer', 'No overview available'),
            'key_statistics': [],
            'recent_news': [],
            'key_facts': [],
            'business_model': '',
            'products_services': [],
            'market_position': '',
            'financial_highlights': [],
            'leadership': '',
            'competitors': [],
            'opportunities': [],
            'risks': [],
            'insights': 'LLM summarization failed. Using basic fallback summary.',
            'error': 'LLM generation failed'
        }
    
    def _save_summary(self, company_id: str, summary_data: Dict[str, Any]) -> bool:
        """
        Save summary data to JSON and markdown files.
        
        Args:
            company_id: Company identifier
            summary_data: Summary data to save
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Get company directory
            company_dir = os.path.join(self.file_manager.base_dir, company_id)
            os.makedirs(company_dir, exist_ok=True)
            
            # Save as JSON
            json_file = os.path.join(company_dir, "summary.json")
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(summary_data, f, indent=2, ensure_ascii=False)
            
            # Save as markdown
            markdown_file = os.path.join(company_dir, "summary.md")
            markdown_content = self._convert_summary_to_markdown(summary_data)
            with open(markdown_file, 'w', encoding='utf-8') as f:
                f.write(markdown_content)
            
            return True
            
        except Exception as e:
            logger.error(f"Error saving summary for {company_id}: {e}")
            return False
    
    def _load_summary(self, company_id: str) -> Optional[Dict[str, Any]]:
        """
        Load summary data from JSON file.
        
        Args:
            company_id: Company identifier
            
        Returns:
            Summary data or None if not found
        """
        try:
            company_dir = os.path.join(self.file_manager.base_dir, company_id)
            json_file = os.path.join(company_dir, "summary.json")
            
            if not os.path.exists(json_file):
                return None
            
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            return data
            
        except Exception as e:
            logger.error(f"Error loading summary for {company_id}: {e}")
            return None
    
    def _convert_summary_to_markdown(self, summary_data: Dict[str, Any]) -> str:
        """
        Convert summary data to markdown format.
        
        Args:
            summary_data: Summary data dictionary
            
        Returns:
            Formatted markdown string
        """
        markdown_lines = []
        
        # Header
        markdown_lines.append("# Company Summary Report (LLM Generated)")
        markdown_lines.append("")
        
        # Metadata
        if summary_data.get('generated_at'):
            markdown_lines.append(f"**Generated:** {summary_data['generated_at']}")
            markdown_lines.append("")
        
        if summary_data.get('llm_model'):
            markdown_lines.append(f"**LLM Model:** {summary_data['llm_model']}")
            markdown_lines.append("")
        
        if summary_data.get('user_prompt'):
            markdown_lines.append(f"**User Prompt:** {summary_data['user_prompt']}")
            markdown_lines.append("")
        
        # Company Overview
        if summary_data.get('company_overview'):
            markdown_lines.append("## Company Overview")
            markdown_lines.append("")
            markdown_lines.append(summary_data['company_overview'])
            markdown_lines.append("")
        
        # Key Statistics
        if summary_data.get('key_statistics'):
            markdown_lines.append("## Key Statistics")
            markdown_lines.append("")
            for stat in summary_data['key_statistics']:
                markdown_lines.append(f"- {stat}")
            markdown_lines.append("")
        
        # Recent News
        if summary_data.get('recent_news'):
            markdown_lines.append("## Recent News")
            markdown_lines.append("")
            for news in summary_data['recent_news']:
                if isinstance(news, dict):
                    title = news.get('title', 'No title')
                    summary = news.get('summary', 'No summary')
                    url = news.get('url', 'No URL')
                    markdown_lines.append(f"### {title}")
                    markdown_lines.append("")
                    markdown_lines.append(f"**Source:** {url}")
                    markdown_lines.append("")
                    markdown_lines.append(summary)
                    markdown_lines.append("")
                else:
                    markdown_lines.append(f"- {news}")
            markdown_lines.append("")
        
        # Key Facts
        if summary_data.get('key_facts'):
            markdown_lines.append("## Key Facts")
            markdown_lines.append("")
            for fact in summary_data['key_facts']:
                markdown_lines.append(f"- {fact}")
            markdown_lines.append("")
        
        # Business Model
        if summary_data.get('business_model'):
            markdown_lines.append("## Business Model")
            markdown_lines.append("")
            markdown_lines.append(summary_data['business_model'])
            markdown_lines.append("")
        
        # Products & Services
        if summary_data.get('products_services'):
            markdown_lines.append("## Products & Services")
            markdown_lines.append("")
            for product in summary_data['products_services']:
                markdown_lines.append(f"- {product}")
            markdown_lines.append("")
        
        # Market Position
        if summary_data.get('market_position'):
            markdown_lines.append("## Market Position")
            markdown_lines.append("")
            markdown_lines.append(summary_data['market_position'])
            markdown_lines.append("")
        
        # Financial Highlights
        if summary_data.get('financial_highlights'):
            markdown_lines.append("## Financial Highlights")
            markdown_lines.append("")
            for highlight in summary_data['financial_highlights']:
                markdown_lines.append(f"- {highlight}")
            markdown_lines.append("")
        
        # Leadership
        if summary_data.get('leadership'):
            markdown_lines.append("## Leadership")
            markdown_lines.append("")
            markdown_lines.append(summary_data['leadership'])
            markdown_lines.append("")
        
        # Competitors
        if summary_data.get('competitors'):
            markdown_lines.append("## Competitors")
            markdown_lines.append("")
            for competitor in summary_data['competitors']:
                markdown_lines.append(f"- {competitor}")
            markdown_lines.append("")
        
        # Opportunities
        if summary_data.get('opportunities'):
            markdown_lines.append("## Opportunities")
            markdown_lines.append("")
            for opportunity in summary_data['opportunities']:
                markdown_lines.append(f"- {opportunity}")
            markdown_lines.append("")
        
        # Risks
        if summary_data.get('risks'):
            markdown_lines.append("## Risks")
            markdown_lines.append("")
            for risk in summary_data['risks']:
                markdown_lines.append(f"- {risk}")
            markdown_lines.append("")
        
        # Insights
        if summary_data.get('insights'):
            markdown_lines.append("## Additional Insights")
            markdown_lines.append("")
            markdown_lines.append(summary_data['insights'])
            markdown_lines.append("")
        
        # Error info if present
        if summary_data.get('error'):
            markdown_lines.append("## Error Information")
            markdown_lines.append("")
            markdown_lines.append(f"**Error:** {summary_data['error']}")
            markdown_lines.append("")
        
        return "\n".join(markdown_lines) 