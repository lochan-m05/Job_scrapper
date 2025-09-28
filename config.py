import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Job Search Filters
    LOCATION = "Bangalore"
    EXPERIENCE_LEVEL = "fresher"  # fresher, entry-level, 0-1 years
    JOB_TYPE = "full-time"  # full-time, part-time, contract, internship
    
    # LinkedIn Configuration
    LINKEDIN_EMAIL = os.getenv("LINKEDIN_EMAIL")
    LINKEDIN_PASSWORD = os.getenv("LINKEDIN_PASSWORD")
    
    # Apollo.io Configuration
    APOLLO_API_KEY = os.getenv("APOLLO_API_KEY")
    
    # Search Keywords
    JOB_KEYWORDS = [
        "software engineer",
        "developer",
        "programmer",
        "web developer",
        "python developer",
        "java developer",
        "frontend developer",
        "backend developer",
        "full stack developer",
        "data analyst",
        "business analyst",
        "quality assurance",
        "qa engineer",
        "test engineer"
    ]
    
    # Industries to focus on
    INDUSTRIES = [
        "Technology",
        "Software Development",
        "IT Services",
        "Fintech",
        "E-commerce",
        "Healthcare Technology"
    ]
    
    # Schedule Configuration
    SEARCH_FREQUENCY = "daily"  # daily, weekly
    SEARCH_TIME = "09:00"  # Time to run the search
    
    # Output Configuration
    OUTPUT_DIR = "job_reports"
    MAX_JOBS_PER_SEARCH = 50
    
    # Apollo.io Search Configuration
    APOLLO_SEARCH_LIMIT = 10  # Max contacts per company
    APOLLO_CONTACT_ROLES = [
        "HR Manager",
        "Talent Acquisition",
        "Recruiter",
        "HR Business Partner",
        "People Operations"
    ]
