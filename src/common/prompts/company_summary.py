def get_company_summary_system_prompt() -> str:
    """
    Get the system prompt for company summary generation.
    
    Returns:
        System prompt string for the LLM
    """
    return """You are an expert business analyst who creates comprehensive company summaries. 
Provide detailed, accurate, and well-structured summaries based on the research data provided.

Your role is to:
1. Analyze company research data from multiple sources
2. Extract key insights, statistics, and facts
3. Identify business models, products, and market position
4. Highlight recent news and developments
5. Assess competitive landscape and opportunities
6. Provide actionable insights for business decision-making

Always maintain objectivity and base your analysis on the provided research data."""

def get_company_summary_user_prompt(research_data: dict, user_prompt: str = None) -> str:
    """
    Create the user prompt for company summary generation.
    
    Args:
        research_data: Raw research data from Tavily
        user_prompt: Optional user prompt to guide summarization
        
    Returns:
        Formatted user prompt string
    """
    prompt_parts = []
    
    # Base instruction
    prompt_parts.append("Please analyze the following company research data and create a comprehensive summary.")
    
    # Add user prompt if provided
    if user_prompt:
        prompt_parts.append(f"Focus on: {user_prompt}")
    
    # Structure instruction
    prompt_parts.append("""
Please structure your response in the following JSON format:
{
    "company_overview": "A comprehensive overview of the company",
    "key_statistics": ["stat1", "stat2", "stat3"],
    "recent_news": [
        {
            "title": "News title",
            "summary": "Brief summary",
            "url": "Source URL"
        }
    ],
    "key_facts": ["fact1", "fact2", "fact3"],
    "business_model": "Description of business model",
    "products_services": ["product1", "product2"],
    "market_position": "Market position and competitive landscape",
    "financial_highlights": ["highlight1", "highlight2"],
    "leadership": "Key leadership information",
    "competitors": ["competitor1", "competitor2"],
    "opportunities": ["opportunity1", "opportunity2"],
    "risks": ["risk1", "risk2"],
    "insights": "Additional insights and analysis"
}
""")
    
    # Add research data
    prompt_parts.append("Research Data:")
    
    # Add answer if available
    if research_data.get('answer'):
        prompt_parts.append(f"Company Overview: {research_data['answer']}")
    
    # Add results
    if research_data.get('results'):
        prompt_parts.append("Research Results:")
        for i, result in enumerate(research_data['results'][:10], 1):  # Limit to first 10 results
            title = result.get('title', 'No title')
            content = result.get('content', 'No content')[:500]  # Limit content length
            url = result.get('url', 'No URL')
            prompt_parts.append(f"{i}. Title: {title}")
            prompt_parts.append(f"   Content: {content}")
            prompt_parts.append(f"   URL: {url}")
            prompt_parts.append("")
    
    # Add raw content if available
    if research_data.get('raw_content'):
        prompt_parts.append("Raw Content:")
        for i, content in enumerate(research_data['raw_content'][:5], 1):  # Limit to first 5
            title = content.get('title', 'No title')
            content_text = content.get('content', 'No content')[:300]  # Limit content length
            prompt_parts.append(f"{i}. {title}: {content_text}")
            prompt_parts.append("")
    
    return "\n".join(prompt_parts)

def get_financial_focus_prompt() -> str:
    """
    Get additional prompt for financial focus.
    
    Returns:
        Financial focus prompt string
    """
    return """When focusing on financial aspects, pay special attention to:
- Revenue figures and growth rates
- Profit margins and profitability metrics
- Market capitalization and valuation
- Financial performance trends
- Investment and funding information
- Quarterly earnings and financial reports
- Cost structure and efficiency metrics"""

def get_technology_focus_prompt() -> str:
    """
    Get additional prompt for technology focus.
    
    Returns:
        Technology focus prompt string
    """
    return """When focusing on technology aspects, pay special attention to:
- Technology stack and platforms
- AI/ML capabilities and innovations
- Product development and R&D
- Technical partnerships and integrations
- Patent portfolio and intellectual property
- Technology trends and adoption
- Engineering team and technical expertise"""

def get_market_focus_prompt() -> str:
    """
    Get additional prompt for market focus.
    
    Returns:
        Market focus prompt string
    """
    return """When focusing on market aspects, pay special attention to:
- Market size and growth potential
- Competitive landscape and positioning
- Market share and industry ranking
- Customer segments and target markets
- Geographic presence and expansion
- Industry trends and market dynamics
- Regulatory environment and compliance"""

def get_recent_developments_prompt() -> str:
    """
    Get additional prompt for recent developments focus.
    
    Returns:
        Recent developments focus prompt string
    """
    return """When focusing on recent developments, pay special attention to:
- Latest announcements and press releases
- Recent product launches and updates
- Acquisitions, mergers, and partnerships
- Leadership changes and organizational updates
- Strategic initiatives and new directions
- Recent financial results and performance
- Industry recognition and awards""" 