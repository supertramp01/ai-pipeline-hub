import sys
import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, HttpUrl
from typing import Optional, List, Dict
import uvicorn

# Ensure src is in sys.path for local runs
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.common.configs.settings import get_settings
from src.common.services.linkedin_service import LinkedInService
from src.common.services.company_service import CompanyService
from src.common.utils.logger import setup_logger

# Set up logging
logger = setup_logger(__name__)

# Initialize FastAPI app
settings = get_settings()
app = FastAPI(
    title=settings.api_title,
    version=settings.api_version,
    description="API for meeting preparation with LinkedIn profile scraping and company research"
)

# Initialize services
linkedin_service = LinkedInService()
company_service = CompanyService()

# Pydantic models
class LinkedInProfileRequest(BaseModel):
    linkedin_url: HttpUrl

class CompanyResearchRequest(BaseModel):
    website_url: HttpUrl
    company_name: Optional[str] = None

class BasicInfo(BaseModel):
    name: str
    headline: str
    company: str
    location: str
    industry: str

class ProfileSummary(BaseModel):
    basic_info: BasicInfo
    experience_count: int
    education_count: int
    skills_count: int
    certifications_count: int
    languages_count: int

class LinkedInProfileResponse(BaseModel):
    user_id: int
    name: str
    company: str
    linkedin_url: str
    status: str
    profile_summary: ProfileSummary

class CompanyResearchResponse(BaseModel):
    company_id: str
    company_name: str
    company_website: str
    status: str  # 'created' or 'updated'
    message: str

class ErrorResponse(BaseModel):
    error: str

class UserProfile(BaseModel):
    user_id: str
    name: str
    company: str
    linkedin_url: str
    created_date: str
    last_updated: str

class CompanyProfile(BaseModel):
    company_id: str
    company_website: str
    create_date: str
    last_updated: str

@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "AI Pipeline Hub - Meeting Preparation API",
        "version": settings.api_version,
        "endpoints": {
            "linkedin": {
                "scrape_profile": "POST /api/v1/linkedin/scrape",
                "get_profile": "GET /api/v1/linkedin/profile/{user_id}",
                "get_profile_summary": "GET /api/v1/linkedin/profile/{user_id}/summary",
                "list_users": "GET /api/v1/linkedin/users"
            },
            "company": {
                "research_company": "POST /api/v1/company/research",
                "get_company": "GET /api/v1/company/{company_id}",
                "get_company_json": "GET /api/v1/company/{company_id}/json",
                "get_company_markdown": "GET /api/v1/company/{company_id}/markdown",
                "list_companies": "GET /api/v1/company/list"
            }
        }
    }

# LinkedIn Profile Endpoints
@app.post("/api/v1/linkedin/scrape", response_model=LinkedInProfileResponse)
async def scrape_linkedin_profile(request: LinkedInProfileRequest):
    """
    Scrape LinkedIn profile and store the data.
    
    This endpoint:
    1. Takes a LinkedIn URL as input
    2. Uses Apify to scrape the profile
    3. Stores the data in markdown format
    4. Updates or creates user entry in CSV
    5. Returns comprehensive profile information
    """
    try:
        logger.info(f"Received LinkedIn profile scrape request for: {request.linkedin_url}")
        
        success, response_data = linkedin_service.scrape_and_store_profile(str(request.linkedin_url))
        
        if not success:
            raise HTTPException(status_code=500, detail=response_data.get("error", "Unknown error"))
        
        return LinkedInProfileResponse(**response_data)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in scrape endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/api/v1/linkedin/profile/{user_id}")
async def get_linkedin_profile(user_id: int):
    """
    Get LinkedIn profile data for a specific user.
    
    Returns the profile data in markdown format.
    """
    try:
        logger.info(f"Received profile retrieval request for user: {user_id}")
        
        profile_content = linkedin_service.get_profile(user_id)
        
        if profile_content is None:
            raise HTTPException(status_code=404, detail="Profile not found")
        
        return {
            "user_id": user_id,
            "profile_content": profile_content,
            "format": "markdown"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in get profile endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/api/v1/linkedin/profile/{user_id}/summary", response_model=ProfileSummary)
async def get_linkedin_profile_summary(user_id: int):
    """
    Get a summary of LinkedIn profile data for a specific user.
    
    Returns a structured summary of the profile including counts and basic information.
    """
    try:
        logger.info(f"Received profile summary request for user: {user_id}")
        
        profile_summary = linkedin_service.get_profile_summary(user_id)
        
        if profile_summary is None:
            raise HTTPException(status_code=404, detail="Profile not found")
        
        return ProfileSummary(**profile_summary)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in get profile summary endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/api/v1/linkedin/users", response_model=List[UserProfile])
async def list_users():
    """
    Get all users from the CSV file.
    
    Returns a list of all stored user profiles.
    """
    try:
        logger.info("Received request to list all users")
        
        users = linkedin_service.get_all_users()
        
        return [UserProfile(**user) for user in users]
        
    except Exception as e:
        logger.error(f"Unexpected error in list users endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

# Company Research Endpoints
@app.post("/api/v1/company/research", response_model=CompanyResearchResponse)
async def research_company(request: CompanyResearchRequest):
    """
    Research a company website and store the data.
    
    This endpoint:
    1. Takes a company website URL and optional company name
    2. Uses Tavily API to research the company
    3. Stores the data in JSON and markdown formats
    4. Updates or creates company entry in CSV
    5. Returns research results and metadata
    """
    try:
        logger.info(f"Received company research request for: {request.website_url}")
        
        result = company_service.research_company(request.company_name, str(request.website_url))
        
        if result['status'] == 'error':
            raise HTTPException(status_code=500, detail=result['message'])
        
        return CompanyResearchResponse(**result)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in company research endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/api/v1/company/{company_id}")
async def get_company_info(company_id: str):
    """
    Get company research data for a specific company.
    
    Returns the company data including CSV metadata and research data.
    """
    try:
        logger.info(f"Received company retrieval request for: {company_id}")
        
        company_data = company_service.get_company_data(company_id)
        
        if company_data is None:
            raise HTTPException(status_code=404, detail="Company not found")
        
        return company_data
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in get company endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/api/v1/company/{company_id}/json")
async def get_company_json(company_id: str):
    """
    Get company research data as JSON for a specific company.
    
    Returns the raw research data in JSON format.
    """
    try:
        logger.info(f"Received company JSON request for: {company_id}")
        
        company_data = company_service.get_company_data(company_id)
        
        if company_data is None:
            raise HTTPException(status_code=404, detail="Company not found")
        
        return {
            "company_id": company_id,
            "research_data": company_data.get('research_data', {})
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in get company JSON endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/api/v1/company/{company_id}/markdown")
async def get_company_markdown(company_id: str):
    """
    Get company research data as markdown for a specific company.
    
    Returns the research data in markdown format.
    """
    try:
        logger.info(f"Received company markdown request for: {company_id}")
        
        markdown_content = company_service.get_company_markdown(company_id)
        
        if markdown_content is None:
            raise HTTPException(status_code=404, detail="Company not found")
        
        return {
            "company_id": company_id,
            "content": markdown_content,
            "format": "markdown"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in get company markdown endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/api/v1/company/list", response_model=List[CompanyProfile])
async def list_companies():
    """
    Get all companies from the CSV file.
    
    Returns a list of all stored company profiles.
    """
    try:
        logger.info("Received company list request")
        
        companies = company_service.get_all_companies()
        
        return [CompanyProfile(**company) for company in companies]
        
    except Exception as e:
        logger.error(f"Unexpected error in list companies endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "ai-pipeline-hub"}

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=True
    ) 