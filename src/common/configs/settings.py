import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Settings:
    # Apify settings
    APIFY_ACTOR_ID = os.getenv("APIFY_ACTOR_ID")
    APIFY_API_TOKEN = os.getenv("APIFY_API_TOKEN")
    
    # Data storage settings
    DATA_DIR = "data"
    LINKEDIN_PROFILES_DIR = os.path.join(DATA_DIR, "lin_profiles")
    USER_PROFILES_CSV = os.path.join(DATA_DIR, "user_profiles.csv")
    
    # API settings
    API_HOST = "0.0.0.0"
    API_PORT = 8000
    API_TITLE = "AI Pipeline Hub - Meeting Preparation API"
    API_VERSION = "1.0.0"
    
    # Logging settings
    LOG_LEVEL = "INFO"
    LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

settings = Settings() 