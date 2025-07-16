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
- **LinkedIn Profile Insights**: AI-powered analysis of LinkedIn profiles to extract international experience, industry sectors, education, value proposition, interests from posts, and talking points
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
│       │   ├── meeting_service.py # Meeting service orchestration
│       │   └── linkedin_insights_service.py # LinkedIn insights service
│       └── prompts/
│           ├── __init__.py
│           ├── company_summary.py # Company summary prompts
│           ├── meeting_preparation.py # Meeting preparation prompts
│           └── linkedin_insights.py # LinkedIn insights prompts
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
│   ├── test_meeting_service.py # Meeting service tests
│   └── test_linkedin_insights_service.py # LinkedIn insights tests
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
OPENAI_API_KEY=your_openai_api_key
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
- **Body**: `{"linkedin_url": "https://linkedin.com/in/username", "return_full_object": true}`
- Scrapes a LinkedIn profile and stores the data
- Returns user information, status, profile summary, and optionally the full profile object
- **Parameters**:
  - `linkedin_url` (required): LinkedIn profile URL to scrape
  - `return_full_object` (optional, default: true): Whether to include the full profile object in the response

### 4. Get LinkedIn Profile
- **GET** `/api/v1/linkedin/profile/{user_id}`
- Retrieves stored LinkedIn profile data in markdown format

### 5. Get LinkedIn Profile Summary
- **GET** `/api/v1/linkedin/profile/{user_id}/summary`
- Returns a structured summary of the profile with counts and basic information

### 6. List All Users
- **GET** `/api/v1/linkedin/users`
- Returns a list of all stored user profiles

### LinkedIn Insights Endpoints

### 7. Generate LinkedIn Insights
- **POST** `/api/v1/linkedin/insights/generate`
- **Body**: `{"user_id": 1, "custom_prompt": "Focus on technical skills and cloud experience"}` (custom_prompt is optional)
- Analyzes LinkedIn profile data using AI to generate comprehensive insights
- Extracts international experience, industry sectors, education, value proposition, interests from posts, and talking points
- Stores insights in JSON and markdown formats
- Returns generated insights with status and metadata
- **Parameters**:
  - `user_id` (required): LinkedIn user ID to analyze
  - `custom_prompt` (optional): Custom analysis focus or requirements

### 8. Get LinkedIn Insights
- **GET** `/api/v1/linkedin/insights/{user_id}`
- Retrieves stored LinkedIn insights data in JSON format
- Returns comprehensive analysis including international experience, industry sectors, education, value proposition, interests, and talking points

### 9. Get LinkedIn Insights Markdown
- **GET** `/api/v1/linkedin/insights/{user_id}/markdown`
- Retrieves stored LinkedIn insights data in formatted markdown
- Returns human-readable analysis with emojis and structured sections

### 10. List All LinkedIn Insights
- **GET** `/api/v1/linkedin/insights/list`
- Returns a list of all stored insights with user information
- Provides overview of all analyzed profiles and their insights

### Company Research Endpoints

### 11. Research Company
- **POST** `/api/v1/company/research`
- **Body**: `{"website_url": "https://company.com", "company_name": "Company Name"}` (company_name is optional)
- Researches a company website and stores comprehensive data
- Returns company information, status, and research metadata

### 12. Get Company Data
- **GET** `/api/v1/company/{company_id}`
- Retrieves stored company research data including CSV metadata and research data

### 13. Get Company JSON
- **GET** `/api/v1/company/{company_id}/json`
- Returns the raw company research data in JSON format

### 14. Get Company Markdown
- **GET** `/api/v1/company/{company_id}/markdown`
- Returns the company research data in formatted markdown

### 15. List All Companies
- **GET** `/api/v1/company/list`
- Returns a list of all stored company profiles

### Company Summary Endpoints

### 16. Generate Company Summary
- **POST** `/api/v1/company/summary/generate`
- **Body**: `{"company_id": "uuid", "company_website": "https://company.com", "user_prompt": "Focus on financial performance"}` (company_id or company_website required, user_prompt optional)
- Generates an intelligent summary based on company research data and optional user prompt
- Stores summary in JSON and markdown formats
- Returns summary data and metadata

### 17. Get Company Summary
- **GET** `/api/v1/company/summary/{company_id}`
- Retrieves previously generated company summary by company ID

### 18. Get Company Summary by Website
- **GET** `/api/v1/company/summary/website/{website_url}`
- Retrieves previously generated company summary by website URL

### Meeting Preparation Endpoints

### 19. Create Meeting
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

### 20. Get Meeting
- **GET** `/api/v1/meeting/{meeting_id}`
- Retrieves complete meeting information including participant data and talking points
- Returns comprehensive meeting data with all details

### 21. Get Meeting Metadata
- **GET** `/api/v1/meeting/{meeting_id}/metadata`
- Retrieves meeting metadata without participant details
- Returns structured meeting profile information

### 22. List All Meetings
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

## LinkedIn Insights Features

The LinkedIn insights pipeline provides AI-powered analysis of LinkedIn profiles to extract meaningful professional insights:

### Insight Categories
- **🌍 International Experience**: Countries and regions where the person has worked, studied, or lived
- **🏢 Industry Sectors**: Different industries and sectors they've worked in throughout their career
- **🎓 Education Analysis**: Educational background, degrees, and qualifications with relevance assessment
- **💼 Value Proposition**: How their skills, experience, and projects make them valuable to organizations
- **📱 Interests from Posts**: Current interests and focus areas based on recent LinkedIn posts
- **💬 Talking Points**: Conversation starters and networking topics based on their background

### Analysis Components
- **Profile Data Processing**: Extracts and structures LinkedIn profile information for analysis
- **AI-Powered Analysis**: Uses OpenAI GPT-4 to generate comprehensive insights
- **Custom Prompt Support**: Allows users to specify analysis focus areas
- **Structured Output**: Provides insights in both JSON and markdown formats
- **Fallback Handling**: Graceful handling of LLM failures with structured responses

### Insight Generation Process
1. **Data Extraction**: Loads stored LinkedIn profile data (JSON format)
2. **Data Preparation**: Structures profile data for AI analysis
3. **LLM Analysis**: Sends structured data to OpenAI GPT-4 with specialized prompts
4. **Response Processing**: Parses JSON response or creates structured fallback
5. **Storage**: Saves insights in both JSON and markdown formats
6. **Retrieval**: Provides endpoints to access insights in multiple formats

### Custom Analysis Focus
- **Technical Skills**: Focus on programming languages, technologies, and technical expertise
- **Leadership Experience**: Emphasize management and leadership roles
- **Industry Expertise**: Highlight specific industry knowledge and experience
- **Geographic Focus**: Analyze regional or international experience
- **Recent Activities**: Focus on current interests and recent professional activities
- **Networking Value**: Identify potential collaboration and partnership opportunities

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
# With full profile object (default)
curl -X POST "http://localhost:8000/api/v1/linkedin/scrape" \
     -H "Content-Type: application/json" \
     -d '{"linkedin_url": "https://linkedin.com/in/satyanadella/", "return_full_object": true}'

# Without full profile object (summary only)
curl -X POST "http://localhost:8000/api/v1/linkedin/scrape" \
     -H "Content-Type: application/json" \
     -d '{"linkedin_url": "https://linkedin.com/in/satyanadella/", "return_full_object": false}'
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

### Generate LinkedIn Insights

```bash
# Generate insights with default analysis
curl -X POST "http://localhost:8000/api/v1/linkedin/insights/generate" \
     -H "Content-Type: application/json" \
     -d '{"user_id": 1}'

# Generate insights with custom focus
curl -X POST "http://localhost:8000/api/v1/linkedin/insights/generate" \
     -H "Content-Type: application/json" \
     -d '{"user_id": 1, "custom_prompt": "Focus on technical skills and cloud architecture experience"}'
```

### Get LinkedIn Insights

```bash
# Get insights in JSON format
curl "http://localhost:8000/api/v1/linkedin/insights/1"

# Get insights in markdown format
curl "http://localhost:8000/api/v1/linkedin/insights/1/markdown"
```

### List All LinkedIn Insights

```bash
curl "http://localhost:8000/api/v1/linkedin/insights/list"
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
# Get complete meeting data with participants and talking points
curl "http://localhost:8000/api/v1/meeting/{meeting_id}"

# Get meeting metadata only (without participants)
curl "http://localhost:8000/api/v1/meeting/{meeting_id}/metadata"
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