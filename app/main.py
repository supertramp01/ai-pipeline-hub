import sys
import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, HttpUrl
from typing import Optional, List, Dict, Any
import uvicorn

# Ensure src is in sys.path for local runs
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.common.configs.settings import get_settings
from src.common.services.linkedin_service import LinkedInService
from src.common.services.company_service import CompanyService
from src.common.services.company_summary_service import CompanySummaryService
from src.common.services.meeting_service import MeetingService
from src.common.services.linkedin_insights_service import LinkedInInsightsService
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
company_summary_service = CompanySummaryService()
meeting_service = MeetingService()
linkedin_insights_service = LinkedInInsightsService()

# Pydantic models
class LinkedInProfileRequest(BaseModel):
    linkedin_url: HttpUrl
    return_full_object: Optional[bool] = True

class CompanyResearchRequest(BaseModel):
    website_url: HttpUrl
    company_name: Optional[str] = None

class CompanySummaryRequest(BaseModel):
    company_id: Optional[str] = None
    company_website: Optional[str] = None
    user_prompt: Optional[str] = None

class ParticipantRequest(BaseModel):
    name: str
    company: str
    user_id: Optional[int] = None
    company_id: Optional[str] = None
    linkedin_url: Optional[str] = None
    background: Optional[str] = None
    meeting_objective: str
    looking_for: Optional[str] = None
    what_they_offer: Optional[str] = None

class MeetingRequest(BaseModel):
    meeting_title: str
    meeting_date: str
    participants: List[ParticipantRequest]

class MeetingResponse(BaseModel):
    meeting_id: str
    status: str
    message: str
    participant_count: int
    meeting_data: Dict[str, Any]

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
    full_profile: Optional[Dict[str, Any]] = None

class CompanyResearchResponse(BaseModel):
    company_id: str
    company_name: str
    company_website: str
    status: str  # 'created' or 'updated'
    message: str

class CompanySummaryResponse(BaseModel):
    company_id: str
    status: str
    message: str
    summary: Dict[str, Any]

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

class MeetingProfile(BaseModel):
    meeting_id: str
    meeting_title: str
    meeting_date: str
    participant_count: int
    created_date: str
    last_updated: str

class LinkedInInsightsRequest(BaseModel):
    user_id: int
    custom_prompt: Optional[str] = None

class LinkedInInsightsResponse(BaseModel):
    user_id: int
    status: str
    message: str
    insights: Dict[str, Any]

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
            "linkedin_insights": {
                "generate_insights": "POST /api/v1/linkedin/insights/generate",
                "get_insights": "GET /api/v1/linkedin/insights/{user_id}?auto_generate=true",
                "get_insights_markdown": "GET /api/v1/linkedin/insights/{user_id}/markdown?auto_generate=true",
                "list_all_insights": "GET /api/v1/linkedin/insights/list"
            },
            "company": {
                "research_company": "POST /api/v1/company/research",
                "get_company": "GET /api/v1/company/{company_id}",
                "get_company_json": "GET /api/v1/company/{company_id}/json",
                "get_company_markdown": "GET /api/v1/company/{company_id}/markdown",
                "list_companies": "GET /api/v1/company/list"
            },
            "company_summary": {
                "generate_summary": "POST /api/v1/company/summary/generate",
                "get_summary": "GET /api/v1/company/summary/{company_id}",
                "get_summary_by_website": "GET /api/v1/company/summary/website/{website_url}"
            },
            "meeting": {
                "create_meeting": "POST /api/v1/meeting/create",
                "get_meeting": "GET /api/v1/meeting/{meeting_id}",
                "get_meeting_metadata": "GET /api/v1/meeting/{meeting_id}/metadata",
                "list_meetings": "GET /api/v1/meeting/list"
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
    6. Optionally returns the full profile object
    """
    try:
        logger.info(f"Received LinkedIn profile scrape request for: {request.linkedin_url}")
        
        success, response_data = linkedin_service.scrape_and_store_profile(
            str(request.linkedin_url), 
            return_full_object=request.return_full_object
        )
        
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

# Company Summary Endpoints
@app.post("/api/v1/company/summary/generate", response_model=CompanySummaryResponse)
async def generate_company_summary(request: CompanySummaryRequest):
    """
    Generate a summary for a company based on its research data.
    
    This endpoint:
    1. Takes a company ID or website URL and optional user prompt
    2. Uses the company summary service to generate the summary
    3. Stores the summary in JSON and markdown formats
    4. Returns the generated summary and metadata
    """
    try:
        logger.info(f"Received company summary generation request for: {request.company_id or request.company_website}")
        
        result = company_summary_service.generate_summary(
            company_id=request.company_id,
            company_website=request.company_website,
            user_prompt=request.user_prompt
        )
        
        if result['status'] == 'error':
            raise HTTPException(status_code=500, detail=result['message'])
        
        return CompanySummaryResponse(**result)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in company summary generation endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/api/v1/company/summary/{company_id}")
async def get_company_summary(company_id: str):
    """
    Get a previously generated summary for a specific company.
    
    Returns the summary data.
    """
    try:
        logger.info(f"Received company summary retrieval request for: {company_id}")
        
        summary_data = company_summary_service.get_summary(company_id=company_id)
        
        if summary_data is None:
            raise HTTPException(status_code=404, detail="Company summary not found")
        
        return {
            "company_id": company_id,
            "summary": summary_data
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in get company summary endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/api/v1/company/summary/website/{website_url}")
async def get_company_summary_by_website(website_url: str):
    """
    Get a previously generated summary for a company based on its website URL.
    
    Returns the summary data.
    """
    try:
        logger.info(f"Received company summary retrieval by website request for: {website_url}")
        
        summary_data = company_summary_service.get_summary(company_website=website_url)
        
        if summary_data is None:
            raise HTTPException(status_code=404, detail="Company summary not found")
        
        return {
            "website_url": website_url,
            "summary": summary_data
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in get company summary by website endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

# Meeting Endpoints
@app.post("/api/v1/meeting/create", response_model=MeetingResponse)
async def create_meeting(request: MeetingRequest):
    """
    Create a new meeting.
    
    This endpoint:
    1. Takes a meeting title, date, and list of participants
    2. Stores the meeting data in JSON and markdown formats
    3. Returns the meeting ID and metadata
    """
    try:
        logger.info(f"Received meeting creation request for: {request.meeting_title}")
        
        # Convert Pydantic models to dictionaries
        participants = [participant.dict() for participant in request.participants]
        
        result = meeting_service.create_meeting(request.meeting_title, request.meeting_date, participants)
        
        if result['status'] == 'error':
            raise HTTPException(status_code=500, detail=result['message'])
        
        return MeetingResponse(**result)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in meeting creation endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/api/v1/meeting/{meeting_id}")
async def get_meeting(meeting_id: str):
    """
    Get a specific meeting by its ID.
    
    Returns the meeting data including metadata and participants.
    """
    try:
        logger.info(f"Received meeting retrieval request for: {meeting_id}")
        
        meeting_data = meeting_service.get_meeting(meeting_id)
        
        if meeting_data is None:
            raise HTTPException(status_code=404, detail="Meeting not found")
        
        return meeting_data
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in get meeting endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/api/v1/meeting/{meeting_id}/metadata", response_model=MeetingProfile)
async def get_meeting_metadata(meeting_id: str):
    """
    Get meeting metadata by its ID.
    
    Returns the meeting metadata without participant details.
    """
    try:
        logger.info(f"Received meeting metadata request for: {meeting_id}")
        
        meeting_data = meeting_service.get_meeting(meeting_id)
        
        if meeting_data is None:
            raise HTTPException(status_code=404, detail="Meeting not found")
        
        # Extract only the metadata fields for MeetingProfile
        metadata = {
            'meeting_id': meeting_data['meeting_id'],
            'meeting_title': meeting_data['meeting_title'],
            'meeting_date': meeting_data['meeting_date'],
            'participant_count': meeting_data['participant_count'],
            'created_date': meeting_data['created_date'],
            'last_updated': meeting_data['last_updated']
        }
        
        return MeetingProfile(**metadata)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in get meeting metadata endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/api/v1/meeting/list", response_model=List[MeetingProfile])
async def list_meetings():
    """
    Get all meetings from the CSV file.
    
    Returns a list of all stored meeting profiles.
    """
    try:
        logger.info("Received meeting list request")
        
        meetings = meeting_service.get_all_meetings()
        
        return [MeetingProfile(**meeting) for meeting in meetings]
        
    except Exception as e:
        logger.error(f"Unexpected error in list meetings endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

# LinkedIn Insights Endpoints
@app.post("/api/v1/linkedin/insights/generate", response_model=LinkedInInsightsResponse)
async def generate_linkedin_insights(request: LinkedInInsightsRequest):
    """
    Generate comprehensive insights from LinkedIn profile data.
    
    This endpoint:
    1. Takes a user_id as input
    2. Analyzes the stored LinkedIn profile data
    3. Uses AI to generate insights about international experience, industry sectors, education, value proposition, interests from posts, and talking points
    4. Stores the insights in JSON and markdown formats
    5. Returns the generated insights
    """
    try:
        logger.info(f"Received LinkedIn insights generation request for user: {request.user_id}")
        
        success, response_data = linkedin_insights_service.generate_insights(
            request.user_id, 
            request.custom_prompt
        )
        
        if not success:
            raise HTTPException(status_code=500, detail=response_data.get("error", "Unknown error"))
        
        return LinkedInInsightsResponse(
            user_id=request.user_id,
            status="success",
            message="Insights generated successfully",
            insights=response_data
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in generate insights endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/api/v1/linkedin/insights/{user_id}")
async def get_linkedin_insights(user_id: int, auto_generate: bool = True):
    """
    Get LinkedIn insights for a specific user.
    
    Args:
        user_id: The user ID to retrieve insights for
        auto_generate: If True (default), automatically generate insights if they don't exist
    
    Returns the insights data in JSON format.
    """
    try:
        logger.info(f"Received insights retrieval request for user: {user_id} (auto_generate: {auto_generate})")
        
        insights = linkedin_insights_service.get_insights(user_id, auto_generate=auto_generate)
        
        if insights is None:
            if auto_generate:
                raise HTTPException(status_code=500, detail="Failed to generate insights")
            else:
                raise HTTPException(status_code=404, detail="Insights not found")
        
        return {
            "user_id": user_id,
            "insights": insights,
            "format": "json",
            "auto_generated": auto_generate
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in get insights endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/api/v1/linkedin/insights/{user_id}/markdown")
async def get_linkedin_insights_markdown(user_id: int, auto_generate: bool = True):
    """
    Get LinkedIn insights for a specific user in markdown format.
    
    Args:
        user_id: The user ID to retrieve insights for
        auto_generate: If True (default), automatically generate insights if they don't exist
    
    Returns the insights data in markdown format.
    """
    try:
        logger.info(f"Received insights markdown retrieval request for user: {user_id} (auto_generate: {auto_generate})")
        
        # First try to get insights (with auto-generation if enabled)
        insights = linkedin_insights_service.get_insights(user_id, auto_generate=auto_generate)
        
        if insights is None:
            if auto_generate:
                raise HTTPException(status_code=500, detail="Failed to generate insights")
            else:
                raise HTTPException(status_code=404, detail="Insights not found")
        
        # Now get the markdown content
        insights_content = linkedin_insights_service.file_manager.get_linkedin_insights_markdown(user_id)
        
        if insights_content is None:
            raise HTTPException(status_code=404, detail="Insights markdown not found")
        
        return {
            "user_id": user_id,
            "insights_content": insights_content,
            "format": "markdown",
            "auto_generated": auto_generate
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in get insights markdown endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/api/v1/linkedin/insights/list")
async def list_all_linkedin_insights():
    """
    Get insights for all users who have them.
    
    Returns a list of all stored insights with user information.
    """
    try:
        logger.info("Received insights list request")
        
        all_insights = linkedin_insights_service.get_all_insights()
        
        return {
            "total_insights": len(all_insights),
            "insights": all_insights
        }
        
    except Exception as e:
        logger.error(f"Unexpected error in list insights endpoint: {str(e)}")
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