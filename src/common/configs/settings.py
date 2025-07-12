import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Settings:
    # Apify settings
    apify_actor_id = os.getenv("APIFY_ACTOR_ID")
    apify_api_token = os.getenv("APIFY_API_TOKEN")
    
    # Tavily settings
    tavily_api_key = os.getenv("TAVILY_API_KEY")
    
    # OpenAI settings
    openai_api_key = os.getenv("OPENAI_API_KEY")
    
    # Data storage settings
    data_dir = "data"
    linkedin_profiles_dir = os.path.join(data_dir, "lin_profiles")
    company_data_dir = os.path.join(data_dir, "company_info")
    user_profiles_csv = os.path.join(data_dir, "user_profiles.csv")
    company_csv_file = os.path.join(data_dir, "company_profiles.csv")
    
    # API settings
    api_host = "0.0.0.0"
    api_port = 8000
    api_title = "AI Pipeline Hub - Meeting Preparation API"
    api_version = "1.0.0"
    
    # Logging settings
    log_level = "INFO"
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

def get_settings() -> Settings:
    """Get settings instance."""
    return Settings()

# Backward compatibility
settings = Settings() 