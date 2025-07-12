"""
Company research prompts for Tavily API.
These prompts are designed to extract comprehensive company information from websites.
"""

def get_company_research_prompt(company_website: str, company_name: str = None) -> str:
    """
    Generate a comprehensive company research prompt for Tavily API.
    
    Args:
        company_website: The company website URL
        company_name: Optional company name for context
        
    Returns:
        Formatted prompt string for Tavily API
    """
    base_prompt = f"""
    Comprehensive market research for website: {company_website}
    
    Please provide detailed information about this company including:
    
    1. **Company Overview & Background**
       - Company history and founding story
       - Mission, vision, and values
       - Key milestones and achievements
       - Company size and employee count
       - Industry and sector classification
    
    2. **Leadership & Management**
       - Key executives and leadership team
       - Board of directors
       - Organizational structure
       - Leadership background and experience
    
    3. **Products & Services**
       - Core products and services offered
       - Product portfolio and features
       - Target market and customer segments
       - Pricing models and strategies
       - Technology stack and platforms
    
    4. **Business Model & Strategy**
       - Revenue streams and business model
       - Market positioning and competitive advantages
       - Growth strategy and expansion plans
       - Partnerships and collaborations
       - Geographic presence and markets served
    
    5. **Financial Information**
       - Funding history and investors
       - Revenue and financial performance
       - Valuation and market cap (if public)
       - Recent financial news and developments
    
    6. **Competitive Analysis**
       - Main competitors and market position
       - Competitive advantages and differentiators
       - Market share and industry standing
       - Competitive threats and challenges
    
    7. **Recent News & Developments**
       - Latest company news and announcements
       - Product launches and updates
       - Strategic initiatives and partnerships
       - Industry recognition and awards
    
    8. **Technology & Innovation**
       - Technology stack and platforms
       - Innovation initiatives and R&D
       - Patents and intellectual property
       - Digital transformation efforts
    
    9. **Corporate Social Responsibility**
       - ESG initiatives and sustainability
       - Community involvement and philanthropy
       - Diversity and inclusion programs
       - Environmental impact and policies
    
    10. **Contact & Location Information**
        - Headquarters and office locations
        - Contact information and social media
        - Customer support and sales channels
        - Global presence and international offices
    
    Please provide comprehensive, factual information based on publicly available sources.
    Focus on accuracy and include specific details, numbers, and recent developments.
    """
    
    if company_name:
        base_prompt = f"Company: {company_name}\n" + base_prompt
    
    return base_prompt.strip()

def get_company_quick_prompt(company_website: str, company_name: str = None) -> str:
    """
    Generate a quick company research prompt for faster results.
    
    Args:
        company_website: The company website URL
        company_name: Optional company name for context
        
    Returns:
        Simplified prompt string for Tavily API
    """
    quick_prompt = f"""
    Market research for website: {company_website}
    
    Include:
    - Company overview and milestones
    - Company leadership
    - Competitive analysis
    - Funding overview
    - Products and services
    - Recent news and developments
    - Contact information and locations
    """
    
    if company_name:
        quick_prompt = f"Company: {company_name}\n" + quick_prompt
    
    return quick_prompt.strip()

def get_company_financial_prompt(company_website: str, company_name: str = None) -> str:
    """
    Generate a financial-focused company research prompt.
    
    Args:
        company_website: The company website URL
        company_name: Optional company name for context
        
    Returns:
        Financial-focused prompt string for Tavily API
    """
    financial_prompt = f"""
    Financial analysis for website: {company_website}
    
    Focus on:
    - Revenue and financial performance
    - Funding history and investors
    - Valuation and market cap
    - Business model and revenue streams
    - Financial news and developments
    - Growth metrics and projections
    - Investment rounds and exits
    """
    
    if company_name:
        financial_prompt = f"Company: {company_name}\n" + financial_prompt
    
    return financial_prompt.strip() 