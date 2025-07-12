# AI Pipeline Hub - Meeting Preparation API

A REST API application for meeting preparation that scrapes LinkedIn profiles using Apify and researches company websites using Tavily API.

## Features

- **LinkedIn Profile Scraping**: Uses Apify to scrape LinkedIn profiles with comprehensive data extraction
- **Company Research**: Uses Tavily API to research company websites and extract comprehensive information
- **Data Storage**: Stores profile and company data in markdown format with JSON backup
- **User Management**: Tracks users in CSV format with auto-incrementing IDs
- **Company Management**: Tracks companies in CSV format with UUID-based IDs
- **REST API**: FastAPI-based endpoints for scraping profiles and researching companies
- **Profile Summaries**: Structured summaries with counts and basic information
- **Comprehensive Field Extraction**: Extracts all possible LinkedIn profile fields
- **Advanced Company Research**: Comprehensive company analysis with multiple data sources
- **Logging**: Comprehensive logging throughout the application

## Project Structure

```
ai-pipeline-hub/
├── app/
│   ├── __init__.py
│   └── main.py                 # FastAPI application
├── src/
│   └── common/
│       ├── configs/
│       │   ├── __init__.py
│       │   └── settings.py     # Application settings
│       ├── utils/
│       │   ├── __init__.py
│       │   ├── apify_client.py # Apify API client
│       │   ├── tavily_client.py # Tavily API client
│       │   ├── csv_manager.py  # LinkedIn CSV data management
│       │   ├── company_csv_manager.py # Company CSV data management
│       │   ├── file_manager.py # LinkedIn file storage management
│       │   ├── company_file_manager.py # Company file storage management
│       │   └── logger.py       # Logging utilities
│       ├── services/
│       │   ├── __init__.py
│       │   ├── linkedin_service.py # LinkedIn service orchestration
│       │   └── company_service.py # Company service orchestration
│       └── __init__.py
├── data/
│   ├── lin_profiles/           # LinkedIn profile data storage
│   └── company_info/           # Company research data storage
├── tests/
│   ├── test_api_endpoints.py   # API endpoint tests
│   ├── test_functions_directly.py # Direct function tests
│   ├── test_comprehensive_data.py # Comprehensive data test
│   └── test_company_research.py # Company research tests
├── .env                        # Environment variables
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Environment Variables

Create a `.env` file in the root directory with the following variables:

```env
APIFY_ACTOR_ID=your_apify_actor_id
APIFY_API_TOKEN=your_apify_api_token
TAVILY_API_KEY=your_tavily_api_key
```

### 3. Run the Application

```bash
# Start the FastAPI server
python app/main.py
```

The API will be available at `http://localhost:8000`

## API Endpoints

### 1. Health Check
- **GET** `/health`
- Returns the health status of the service

### 2. Root Information
- **GET** `/`
- Returns API information and available endpoints

### LinkedIn Profile Endpoints

### 3. Scrape LinkedIn Profile
- **POST** `/api/v1/linkedin/scrape`
- **Body**: `{"linkedin_url": "https://linkedin.com/in/username"}`
- Scrapes a LinkedIn profile and stores the data
- Returns user information, status, and profile summary

### 4. Get LinkedIn Profile
- **GET** `/api/v1/linkedin/profile/{user_id}`
- Retrieves stored LinkedIn profile data in markdown format

### 5. Get LinkedIn Profile Summary
- **GET** `/api/v1/linkedin/profile/{user_id}/summary`
- Returns a structured summary of the profile with counts and basic information

### 6. List All Users
- **GET** `/api/v1/linkedin/users`
- Returns a list of all stored user profiles

### Company Research Endpoints

### 7. Research Company
The application extracts all possible fields from LinkedIn profiles, including:

### Basic Information
- Name (first_name, last_name, full_name)
- Headline
- Company/Current Company
- Location
- Industry
- Summary

### Contact Information
- Email
- Phone
- Website
- Twitter

### About Section
- About text

### Experience
- Job title
- Company
- Duration
- Location
- Description
- Start date
- End date

### Education
- School
- Degree
- Field of study
- Duration
- Start date
- End date
- Grade

### Skills
- Skill name
- Endorsement count

### Certifications
- Certification name
- Issuing organization
- Issue date
- Expiration date
- Credential ID

### Languages
- Language name
- Proficiency level

### Volunteer Experience
- Title
- Organization
- Duration
- Description

### Publications
- Title
- Publisher
- Date
- Description

### Patents
- Title
- Patent office
- Issue date
- Patent number

### Courses
- Course names

### Projects
- Title
- Description
- URL

### Honors & Awards
- Title
- Issuer
- Date
- Description

### Organizations
- Name
- Role
- Duration

### Test Scores
- Test name
- Score
- Date

### Causes
- Cause names

### Additional Fields
- Profile URL
- Profile picture
- Connection count
- Follower count
- Recommendations count
- Endorsements count
- Public profile status
- Premium member status
- Last updated timestamp

## Usage Examples

### Scrape a LinkedIn Profile

```bash
curl -X POST "http://localhost:8000/api/v1/linkedin/scrape" \
     -H "Content-Type: application/json" \
     -d '{"linkedin_url": "https://linkedin.com/in/satyanadella/"}'
```

### Get Profile Data

```bash
curl "http://localhost:8000/api/v1/linkedin/profile/1"
```

### Get Profile Summary

```bash
curl "http://localhost:8000/api/v1/linkedin/profile/1/summary"
```

### List All Users

```bash
curl "http://localhost:8000/api/v1/linkedin/users"
```

## Testing

### Test API Endpoints

```bash
python tests/test_api_endpoints.py
```

### Test Functions Directly

```bash
python tests/test_functions_directly.py
```

### Test Comprehensive Data Processing

```bash
python tests/test_comprehensive_data.py
```

## Data Storage

### CSV File (`data/user_profiles.csv`)
Stores user information with the following columns:
- `user_id`: Auto-incrementing integer ID
- `name`: User's name
- `company`: User's company
- `linkedin_url`: LinkedIn profile URL
- `created_date`: When the entry was created
- `last_updated`: When the entry was last updated

### Profile Data (`data/lin_profiles/{user_id}/`)
Each user gets a directory containing:
- `profile.md`: Profile data in comprehensive markdown format
- `profile.json`: Raw profile data in JSON format

## Pipeline Flow

1. **Input**: LinkedIn URL via POST request
2. **Scraping**: Apify actor scrapes the LinkedIn profile
3. **Data Processing**: Extracts comprehensive information from all available fields
4. **Storage**: 
   - Updates/creates entry in CSV file
   - Saves profile data in markdown and JSON formats
5. **Response**: Returns user information, status, and profile summary

## Error Handling

- Comprehensive error handling throughout the application
- Detailed logging for debugging
- Graceful handling of API failures
- Input validation using Pydantic models
- Fallback mechanisms for missing data fields

## Future Enhancements

- S3 integration for cloud storage
- Additional data sources beyond LinkedIn
- Meeting preparation insights generation
- User authentication and authorization
- Rate limiting and API quotas
- Data analytics and reporting
- Export functionality (PDF, Word, etc.)

## Contributing

1. Follow the existing code structure
2. Add appropriate logging
3. Include tests for new functionality
4. Update documentation as needed

## License

This project is for internal use and meeting preparation purposes.
