from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, HttpUrl
from typing import Optional, List, Dict
import uvicorn

from src.common.configs.settings import settings
from src.common.services.linkedin_service import LinkedInService
from src.common.utils.logger import setup_logger

# Set up logging
logger = setup_logger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title=settings.API_TITLE,
    version=settings.API_VERSION,
    description="API for meeting preparation with LinkedIn profile scraping"
)

# Initialize services
linkedin_service = LinkedInService()

# Pydantic models
class LinkedInProfileRequest(BaseModel):
    linkedin_url: HttpUrl

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

class ErrorResponse(BaseModel):
    error: str

class UserProfile(BaseModel):
    user_id: str
    name: str
    company: str
    linkedin_url: str
    created_date: str
    last_updated: str

@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "AI Pipeline Hub - Meeting Preparation API",
        "version": settings.API_VERSION,
        "endpoints": {
            "scrape_profile": "POST /api/v1/linkedin/scrape",
            "get_profile": "GET /api/v1/linkedin/profile/{user_id}",
            "get_profile_summary": "GET /api/v1/linkedin/profile/{user_id}/summary",
            "list_users": "GET /api/v1/linkedin/users"
        }
    }

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

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "ai-pipeline-hub"}

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=True
    ) 