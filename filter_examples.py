#!/usr/bin/env python3
"""
Examples of how to customize search filters
"""

# Example 1: Basic Location and Experience Filters
BASIC_FILTERS = {
    "LOCATION": "Mumbai",  # Change to your preferred city
    "EXPERIENCE_LEVEL": "entry-level",  # fresher, entry-level, 0-1 years
    "JOB_TYPE": "full-time"  # full-time, part-time, contract, internship
}

# Example 2: Custom Job Keywords for Different Roles
SOFTWARE_ENGINEER_KEYWORDS = [
    "software engineer",
    "software developer", 
    "programmer",
    "python developer",
    "java developer",
    "full stack developer",
    "backend developer",
    "frontend developer"
]

DATA_ANALYST_KEYWORDS = [
    "data analyst",
    "business analyst",
    "data scientist",
    "data engineer",
    "business intelligence",
    "analytics engineer"
]

QA_TESTING_KEYWORDS = [
    "quality assurance",
    "qa engineer",
    "test engineer",
    "automation engineer",
    "software tester",
    "quality analyst"
]

# Example 3: Industry-Specific Filters
TECH_INDUSTRIES = [
    "Technology",
    "Software Development", 
    "IT Services",
    "Fintech",
    "E-commerce"
]

HEALTHCARE_INDUSTRIES = [
    "Healthcare Technology",
    "Medical Devices",
    "Pharmaceuticals",
    "Health IT"
]

# Example 4: Location-Specific Filters
BANGALORE_FILTERS = {
    "LOCATION": "Bangalore",
    "EXPERIENCE_LEVEL": "fresher",
    "JOB_KEYWORDS": [
        "software engineer",
        "developer",
        "python developer",
        "java developer"
    ]
}

MUMBAI_FILTERS = {
    "LOCATION": "Mumbai", 
    "EXPERIENCE_LEVEL": "entry-level",
    "JOB_KEYWORDS": [
        "business analyst",
        "data analyst",
        "financial analyst",
        "consultant"
    ]
}

# Example 5: Company Size Filters (for Apollo.io)
STARTUP_FILTERS = {
    "COMPANY_SIZE": "1-50",  # Small companies
    "FUNDING_STAGE": ["Series A", "Series B", "Seed"]
}

ENTERPRISE_FILTERS = {
    "COMPANY_SIZE": "1000+",  # Large companies
    "INDUSTRY": ["Technology", "IT Services"]
}

# Example 6: Advanced Search Criteria
ADVANCED_FILTERS = {
    "LOCATION": "Bangalore",
    "EXPERIENCE_LEVEL": "fresher",
    "JOB_TYPE": "full-time",
    "SALARY_RANGE": "3-8 LPA",  # Lakhs per annum
    "REMOTE_WORK": True,
    "COMPANY_TYPES": ["Product", "Startup", "MNC"],
    "SKILLS_REQUIRED": ["Python", "Java", "SQL", "React"],
    "EDUCATION": "B.Tech/B.E"
}
