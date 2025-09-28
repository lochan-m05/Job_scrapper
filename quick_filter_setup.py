#!/usr/bin/env python3
"""
Quick Filter Setup for Common Job Search Scenarios
"""

def setup_software_engineer_filters():
    """Setup filters for software engineering roles"""
    return {
        "LOCATION": "Bangalore",
        "EXPERIENCE_LEVEL": "fresher",
        "JOB_TYPE": "full-time",
        "JOB_KEYWORDS": [
            "software engineer",
            "software developer",
            "programmer",
            "python developer",
            "java developer",
            "full stack developer",
            "backend developer",
            "frontend developer",
            "mobile developer",
            "web developer"
        ],
        "INDUSTRIES": [
            "Technology",
            "Software Development",
            "IT Services",
            "Fintech",
            "E-commerce"
        ]
    }

def setup_data_analyst_filters():
    """Setup filters for data analyst roles"""
    return {
        "LOCATION": "Bangalore",
        "EXPERIENCE_LEVEL": "fresher",
        "JOB_TYPE": "full-time",
        "JOB_KEYWORDS": [
            "data analyst",
            "business analyst",
            "data scientist",
            "data engineer",
            "business intelligence",
            "analytics engineer",
            "machine learning engineer",
            "data architect"
        ],
        "INDUSTRIES": [
            "Technology",
            "Fintech",
            "E-commerce",
            "Healthcare Technology",
            "Consulting"
        ]
    }

def setup_qa_testing_filters():
    """Setup filters for QA and testing roles"""
    return {
        "LOCATION": "Bangalore",
        "EXPERIENCE_LEVEL": "fresher",
        "JOB_TYPE": "full-time",
        "JOB_KEYWORDS": [
            "quality assurance",
            "qa engineer",
            "test engineer",
            "automation engineer",
            "software tester",
            "quality analyst",
            "performance tester",
            "manual tester"
        ],
        "INDUSTRIES": [
            "Technology",
            "Software Development",
            "IT Services",
            "Fintech"
        ]
    }

def setup_devops_filters():
    """Setup filters for DevOps roles"""
    return {
        "LOCATION": "Bangalore",
        "EXPERIENCE_LEVEL": "entry-level",
        "JOB_TYPE": "full-time",
        "JOB_KEYWORDS": [
            "devops engineer",
            "cloud engineer",
            "site reliability engineer",
            "aws engineer",
            "azure engineer",
            "kubernetes engineer",
            "infrastructure engineer",
            "platform engineer"
        ],
        "INDUSTRIES": [
            "Technology",
            "Cloud Services",
            "IT Services",
            "Fintech"
        ]
    }

def setup_product_management_filters():
    """Setup filters for product management roles"""
    return {
        "LOCATION": "Bangalore",
        "EXPERIENCE_LEVEL": "entry-level",
        "JOB_TYPE": "full-time",
        "JOB_KEYWORDS": [
            "product manager",
            "project manager",
            "scrum master",
            "business analyst",
            "product owner",
            "program manager",
            "technical product manager",
            "associate product manager"
        ],
        "INDUSTRIES": [
            "Technology",
            "E-commerce",
            "Fintech",
            "Healthcare Technology"
        ]
    }

def setup_multiple_locations():
    """Setup filters for multiple locations"""
    return {
        "LOCATIONS": ["Bangalore", "Mumbai", "Delhi", "Hyderabad", "Pune"],
        "EXPERIENCE_LEVEL": "fresher",
        "JOB_TYPE": "full-time",
        "JOB_KEYWORDS": [
            "software engineer",
            "developer",
            "programmer",
            "data analyst",
            "business analyst"
        ]
    }

def setup_remote_work_filters():
    """Setup filters for remote work opportunities"""
    return {
        "LOCATION": "Remote",
        "EXPERIENCE_LEVEL": "fresher",
        "JOB_TYPE": "full-time",
        "REMOTE_WORK": True,
        "JOB_KEYWORDS": [
            "software engineer",
            "developer",
            "data analyst",
            "business analyst",
            "remote developer",
            "work from home"
        ]
    }

def setup_startup_filters():
    """Setup filters for startup companies"""
    return {
        "LOCATION": "Bangalore",
        "EXPERIENCE_LEVEL": "fresher",
        "JOB_TYPE": "full-time",
        "COMPANY_SIZE": "1-100",
        "COMPANY_TYPE": "Startup",
        "JOB_KEYWORDS": [
            "software engineer",
            "full stack developer",
            "startup engineer",
            "early stage engineer"
        ]
    }

def setup_mnc_filters():
    """Setup filters for MNC companies"""
    return {
        "LOCATION": "Bangalore",
        "EXPERIENCE_LEVEL": "fresher",
        "JOB_TYPE": "full-time",
        "COMPANY_SIZE": "1000+",
        "COMPANY_TYPE": "MNC",
        "JOB_KEYWORDS": [
            "software engineer",
            "developer",
            "programmer",
            "associate engineer",
            "graduate engineer"
        ],
        "INDUSTRIES": [
            "Technology",
            "IT Services",
            "Consulting",
            "Fintech"
        ]
    }

def get_filter_presets():
    """Get all available filter presets"""
    return {
        "1": ("Software Engineer", setup_software_engineer_filters),
        "2": ("Data Analyst", setup_data_analyst_filters),
        "3": ("QA & Testing", setup_qa_testing_filters),
        "4": ("DevOps & Cloud", setup_devops_filters),
        "5": ("Product Management", setup_product_management_filters),
        "6": ("Multiple Locations", setup_multiple_locations),
        "7": ("Remote Work", setup_remote_work_filters),
        "8": ("Startup Companies", setup_startup_filters),
        "9": ("MNC Companies", setup_mnc_filters)
    }

def main():
    """Main function to run quick filter setup"""
    print("Quick Filter Setup for Job Search")
    print("=" * 40)
    
    presets = get_filter_presets()
    
    print("\nAvailable filter presets:")
    for key, (name, _) in presets.items():
        print(f"{key}. {name}")
    
    choice = input("\nSelect a preset (1-9): ").strip()
    
    if choice in presets:
        name, setup_func = presets[choice]
        filters = setup_func()
        
        print(f"\n✅ {name} filters configured:")
        print("-" * 30)
        for key, value in filters.items():
            if isinstance(value, list):
                print(f"{key}: {', '.join(value[:3])}{'...' if len(value) > 3 else ''}")
            else:
                print(f"{key}: {value}")
        
        # Save to file
        import json
        with open(f"filters_{name.lower().replace(' ', '_')}.json", "w") as f:
            json.dump(filters, f, indent=2)
        
        print(f"\n💾 Filters saved to: filters_{name.lower().replace(' ', '_')}.json")
        print("\nTo use these filters:")
        print("1. Copy the values to your config.py file")
        print("2. Or use the configure_filters.py tool to apply them")
        
    else:
        print("Invalid choice.")

if __name__ == "__main__":
    main()
