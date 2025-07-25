# AI Pipeline Hub - Meeting Preparation API

A REST API application for meeting preparation that scrapes LinkedIn profiles using Apify, researches company websites using Tavily API, generates intelligent company summaries, and orchestrates meetings with AI-powered talking points.

## Features

- **LinkedIn Profile Scraping**: Uses Apify to scrape LinkedIn profiles with comprehensive data extraction
- **Company Research**: Uses Tavily API to research company websites and extract comprehensive information
- **Company Summaries**: Generates intelligent summaries with optional user prompts and bullet points
- **Meeting Orchestration**: Creates meetings with AI-generated talking points based on participant objectives and offerings
- **Data Storage**: Stores profile, company research, summary, and meeting data in markdown format with JSON backup
- **User Management**: Tracks users in CSV format with auto-incrementing IDs
- **Company Management**: Tracks companies in CSV format with UUID-based IDs
- **Meeting Management**: Tracks meetings in CSV format with UUID-based IDs
- **REST API**: FastAPI-based endpoints for scraping profiles, researching companies, generating summaries, and creating meetings
- **Profile Summaries**: Structured summaries with counts and basic information
- **Comprehensive Field Extraction**: Extracts all possible LinkedIn profile fields
- **Advanced Company Research**: Comprehensive company analysis with multiple data sources
- **Intelligent Summarization**: AI-powered summaries with user prompt customization
- **AI-Powered Meeting Preparation**: Generates personalized talking points for each participant
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
│       │   ├── meeting_csv_manager.py # Meeting CSV data management
│       │   ├── file_manager.py # LinkedIn file storage management
│       │   ├── company_file_manager.py # Company file storage management
│       │   ├── meeting_file_manager.py # Meeting file storage management
│       │   └── logger.py       # Logging utilities
│       ├── services/
│       │   ├── __init__.py
│       │   ├── linkedin_service.py # LinkedIn service orchestration
│       │   ├── company_service.py # Company service orchestration
│       │   ├── company_summary_service.py # Company summary service
│       │   └── meeting_service.py # Meeting service orchestration
│       └── prompts/
│           ├── __init__.py
│           ├── company_summary.py # Company summary prompts
│           └── meeting_preparation.py # Meeting preparation prompts
├── data/
│   ├── lin_profiles/           # LinkedIn profile data storage
│   ├── company_info/           # Company research and summary data storage
│   └── meetings/               # Meeting data storage
├── examples/
│   └── meeting_example.py      # Meeting preparation example
├── tests/
│   ├── test_api_endpoints.py   # API endpoint tests
│   ├── test_functions_directly.py # Direct function tests
│   ├── test_comprehensive_data.py # Comprehensive data test
│   ├── test_company_research.py # Company research tests
│   ├── test_company_summary.py # Company summary tests
│   └── test_meeting_service.py # Meeting service tests
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
- **POST** `/api/v1/company/research`
- **Body**: `{"website_url": "https://company.com", "company_name": "Company Name"}` (company_name is optional)
- Researches a company website and stores comprehensive data
- Returns company information, status, and research metadata

### 8. Get Company Data
- **GET** `/api/v1/company/{company_id}`
- Retrieves stored company research data including CSV metadata and research data

### 9. Get Company JSON
- **GET** `/api/v1/company/{company_id}/json`
- Returns the raw company research data in JSON format

### 10. Get Company Markdown
- **GET** `/api/v1/company/{company_id}/markdown`
- Returns the company research data in formatted markdown

### 11. List All Companies
- **GET** `/api/v1/company/list`
- Returns a list of all stored company profiles

### Company Summary Endpoints

### 12. Generate Company Summary
- **POST** `/api/v1/company/summary/generate`
- **Body**: `{"company_id": "uuid", "company_website": "https://company.com", "user_prompt": "Focus on financial performance"}` (company_id or company_website required, user_prompt optional)
- Generates an intelligent summary based on company research data and optional user prompt
- Stores summary in JSON and markdown formats
- Returns summary data and metadata

### 13. Get Company Summary
- **GET** `/api/v1/company/summary/{company_id}`
- Retrieves previously generated company summary by company ID

### 14. Get Company Summary by Website
- **GET** `/api/v1/company/summary/website/{website_url}`
- Retrieves previously generated company summary by website URL

### Meeting Preparation Endpoints

### 15. Create Meeting
- **POST** `/api/v1/meeting/create`
- **Body**: 
```json
{
  "meeting_title": "AI Partnership Meeting",
  "meeting_date": "2024-02-15",
  "participants": [
    {
      "name": "John Doe",
      "company": "Tech Corp",
      "user_id": 1,
      "company_id": "tech-corp-123",
      "linkedin_url": "https://linkedin.com/in/johndoe",
      "background": "Software engineer with 10 years experience",
      "what_they_offer": "AI/ML expertise, technical consulting, development resources",
      "meeting_objective": "Find potential partners for AI project",
      "looking_for": "Companies working on AI/ML solutions, funding opportunities"
    }
  ]
}
```
- Creates a new meeting with AI-generated talking points for each participant
- Enriches participant data with LinkedIn and company information using user_id and company_id
- Generates personalized talking points based on mutual objectives and offerings
- Stores meeting data in JSON and markdown formats
- Returns meeting ID, status, and participant count

**Participant Fields:**
- `name` (required): Participant's name
- `company` (required): Company name
- `user_id` (optional): LinkedIn user ID for data enrichment
- `company_id` (optional): Company ID for data enrichment
- `linkedin_url` (optional): LinkedIn URL (used if user_id not provided)
- `background` (optional): Professional background
- `what_they_offer` (optional): Skills, resources, and expertise they can offer
- `meeting_objective` (required): What they want to achieve in the meeting
- `looking_for` (optional): What they need from other participants

### 16. Get Meeting
- **GET** `/api/v1/meeting/{meeting_id}`
- Retrieves meeting information including participant data and talking points
- Returns comprehensive meeting data with CSV metadata

### 17. List All Meetings
- **GET** `/api/v1/meeting/list`
- Returns a list of all stored meetings with metadata

## Comprehensive LinkedIn Data Extraction

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

## Company Research Features

The company research pipeline provides comprehensive analysis including:

### Research Data
- **Answer**: AI-generated summary of the company
- **Results**: Multiple search results with titles, URLs, and content
- **Raw Content**: Detailed content from various sources
- **Metadata**: Research timestamp and company information

### Company Information Extraction
- **Company Name**: Automatically extracted from research data or website URL
- **Website Analysis**: Comprehensive analysis of company website content
- **Industry Information**: Business sector and market positioning
- **Company Overview**: Products, services, and business model
- **Recent News**: Latest developments and announcements
- **Competitive Analysis**: Market position and competitors

## Company Summary Features

The company summary pipeline generates intelligent summaries with:

### Summary Components
- **Company Overview**: AI-generated company description
- **Key Statistics**: Extracted financial and business metrics
- **Recent News**: Latest company announcements and developments
- **Key Facts**: Important company information and milestones
- **Business Model**: Company's revenue and operational model
- **Products & Services**: Company offerings and solutions
- **Market Position**: Competitive landscape and industry standing
- **Financial Highlights**: Revenue, growth, and financial metrics
- **Leadership**: Executive team and management information
- **Competitors**: Main competitors and market rivals
- **Opportunities**: Growth opportunities and market potential
- **Risks**: Business risks and challenges

### User Prompt Customization
- **Financial Focus**: Prioritizes financial performance and metrics
- **Technology Focus**: Emphasizes technology innovations and products
- **Market Focus**: Highlights competitive position and market analysis
- **Recent Developments**: Focuses on latest news and announcements
- **Custom Prompts**: User-defined focus areas and queries

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

### Research a Company

```bash
curl -X POST "http://localhost:8000/api/v1/company/research" \
     -H "Content-Type: application/json" \
     -d '{"website_url": "https://www.microsoft.com", "company_name": "Microsoft"}'
```

### Get Company Data

```bash
curl "http://localhost:8000/api/v1/company/{company_id}"
```

### Get Company JSON

```bash
curl "http://localhost:8000/api/v1/company/{company_id}/json"
```

### Get Company Markdown

```bash
curl "http://localhost:8000/api/v1/company/{company_id}/markdown"
```

### List All Companies

```bash
curl "http://localhost:8000/api/v1/company/list"
```

### Generate Company Summary

```bash
curl -X POST "http://localhost:8000/api/v1/company/summary/generate" \
     -H "Content-Type: application/json" \
     -d '{"company_website": "https://www.apple.com", "user_prompt": "Focus on financial performance and recent innovations"}'
```

### Get Company Summary

```bash
curl "http://localhost:8000/api/v1/company/summary/{company_id}"
```

### Get Company Summary by Website

```bash
curl "http://localhost:8000/api/v1/company/summary/website/https%3A//www.apple.com"
```

### Create a Meeting

```bash
curl -X POST "http://localhost:8000/api/v1/meeting/create" \
     -H "Content-Type: application/json" \
     -d '{
       "meeting_title": "AI Partnership Meeting",
       "meeting_date": "2024-02-15",
       "participants": [
         {
           "name": "Sarah Johnson",
           "company": "TechStart AI",
           "user_id": 1,
           "company_id": "techstart-ai-789",
           "linkedin_url": "https://linkedin.com/in/sarahjohnson",
           "background": "AI researcher with 8 years experience",
           "what_they_offer": "AI/ML expertise, research capabilities, technical consulting",
           "meeting_objective": "Find partners for AI healthcare solutions",
           "looking_for": "Healthcare domain expertise, clinical data access, funding"
         },
         {
           "name": "Dr. Michael Chen",
           "company": "HealthTech Solutions",
           "user_id": 2,
           "company_id": "healthtech-solutions-456",
           "background": "Medical doctor turned healthcare technology entrepreneur",
           "what_they_offer": "Healthcare domain expertise, clinical validation, regulatory knowledge",
           "meeting_objective": "Identify AI solutions to improve patient outcomes",
           "looking_for": "AI/ML technical expertise, data science capabilities"
         }
       ]
     }'
```

### Get Meeting Details

```bash
curl "http://localhost:8000/api/v1/meeting/{meeting_id}"
```

### List All Meetings

```bash
curl "http://localhost:8000/api/v1/meeting/list"
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

### Test Company Research

```bash
python tests/test_company_research.py
```

### Test Company Summary

```bash
python tests/test_company_summary.py
```

## Data Storage

### LinkedIn CSV File (`data/user_profiles.csv`)
Stores user information with the following columns:
- `user_id`: Auto-incrementing integer ID
- `name`: User's name
- `company`: User's company
- `linkedin_url`: LinkedIn profile URL
- `created_date`: When the entry was created
- `last_updated`: When the entry was last updated

### LinkedIn Profile Data (`data/lin_profiles/{user_id}/`)
Each user gets a directory containing:
- `profile.md`: Profile data in comprehensive markdown format
- `profile.json`: Raw profile data in JSON format

### Company CSV File (`data/company_profiles.csv`)
Stores company information with the following columns:
- `company_id`: UUID-based company identifier
- `company_website`: Company website URL
- `create_date`: When the entry was created
- `last_updated`: When the entry was last updated

### Company Research Data (`data/company_info/{company_id}/`)
Each company gets a directory containing:
- `research_data.md`: Company research data in markdown format
- `research_data.json`: Raw research data in JSON format
- `summary.md`: Generated company summary in markdown format
- `summary.json`: Generated company summary in JSON format

### Meeting CSV File (`data/meetings/`)
Stores meeting information with the following columns:
- `meeting_id`: UUID-based meeting identifier
- `meeting_title`: Meeting title
- `meeting_date`: Meeting date
- `created_date`: When the entry was created
- `last_updated`: When the entry was last updated

### Meeting Data (`data/meetings/{meeting_id}/`)
Each meeting gets a directory containing:
- `participants.md`: Participant data in markdown format
- `participants.json`: Raw participant data in JSON format
- `talking_points.md`: AI-generated talking points in markdown format
- `talking_points.json`: Raw talking points in JSON format

## Pipeline Flow

### LinkedIn Profile Pipeline
1. **Input**: LinkedIn URL via POST request
2. **Scraping**: Apify actor scrapes the LinkedIn profile
3. **Data Processing**: Extracts comprehensive information from all available fields
4. **Storage**: 
   - Updates/creates entry in CSV file
   - Saves profile data in markdown and JSON formats
5. **Response**: Returns user information, status, and profile summary

### Company Research Pipeline
1. **Input**: Company website URL and optional company name via POST request
2. **Research**: Tavily API researches the company website and related information
3. **Data Processing**: Extracts company name and organizes research data
4. **Storage**: 
   - Creates entry in company CSV file with UUID
   - Saves research data in markdown and JSON formats
5. **Response**: Returns company information, status, and research metadata

### Company Summary Pipeline
1. **Input**: Company ID or website URL and optional user prompt via POST request
2. **Data Retrieval**: Loads existing company research data
3. **Summary Generation**: Analyzes research data and extracts key information
4. **User Prompt Processing**: Applies user prompt to focus summary on specific aspects
5. **Storage**: 
   - Saves summary data in markdown and JSON formats
   - Stores in company-specific directory
6. **Response**: Returns summary data and metadata

### Meeting Preparation Pipeline
1. **Input**: Meeting title, date, and participant information via POST request
2. **Participant Processing**: 
   - Enriches participant data with LinkedIn profile information using user_id (preferred) or linkedin_url
   - Incorporates company research data using company_id (preferred) or company name
   - Combines user-provided and LinkedIn background information
3. **Talking Points Generation**: 
   - Analyzes each participant's objectives, offerings, and needs
   - Generates personalized talking points for each participant
   - Uses AI to identify mutual value and collaboration opportunities
4. **Data Storage**: 
   - Creates entry in meeting CSV file with UUID
   - Saves comprehensive meeting data in JSON and markdown formats
5. **Response**: Returns meeting ID, status, and participant count

## Error Handling

- Comprehensive error handling throughout the application
- Detailed logging for debugging
- Graceful handling of API failures
- Input validation using Pydantic models
- Fallback mechanisms for missing data fields
- Company name extraction from multiple sources
- User prompt validation and processing

## Future Enhancements

- S3 integration for cloud storage
- Additional data sources beyond LinkedIn and company websites
- Meeting preparation insights generation
- User authentication and authorization
- Rate limiting and API quotas
- Data analytics and reporting
- Export functionality (PDF, Word, etc.)
- Integration with CRM systems
- Automated meeting agenda generation
- Competitor analysis features
- Advanced AI summarization with multiple models
- Real-time news integration
- Financial data API integration
- Custom summary templates
- Batch processing capabilities

## Contributing

1. Follow the existing code structure
2. Add appropriate logging
3. Include tests for new functionality
4. Update documentation as needed

## License

This project is for internal use and meeting preparation purposes.
