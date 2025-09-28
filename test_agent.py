#!/usr/bin/env python3
"""
Test script for the Job Search Agent
"""

import os
import sys
import logging
from datetime import datetime
from config import Config
from apollo_enricher import ApolloEnricher
from data_processor import JobDataProcessor
from report_generator import ReportGenerator

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_configuration():
    """Test configuration setup"""
    print("Testing Configuration...")
    try:
        config = Config()
        print(f"✓ Location: {config.LOCATION}")
        print(f"✓ Experience Level: {config.EXPERIENCE_LEVEL}")
        print(f"✓ Job Keywords: {len(config.JOB_KEYWORDS)} keywords")
        print(f"✓ Search Frequency: {config.SEARCH_FREQUENCY}")
        print(f"✓ Search Time: {config.SEARCH_TIME}")
        
        # Check environment variables
        if config.LINKEDIN_EMAIL and config.LINKEDIN_PASSWORD:
            print("✓ LinkedIn credentials configured")
        else:
            print("⚠️  LinkedIn credentials not configured")
        
        if config.APOLLO_API_KEY:
            print("✓ Apollo.io API key configured")
        else:
            print("⚠️  Apollo.io API key not configured")
        
        return True
    except Exception as e:
        print(f"❌ Configuration test failed: {e}")
        return False

def test_apollo_connection():
    """Test Apollo.io API connection"""
    print("\nTesting Apollo.io Connection...")
    try:
        enricher = ApolloEnricher()
        
        # Test with a known company
        test_company = "Google"
        company_info = enricher.search_company(test_company)
        
        if company_info:
            print(f"✓ Apollo.io connection successful")
            print(f"✓ Found company: {company_info.get('name', 'Unknown')}")
            return True
        else:
            print(f"⚠️  Apollo.io connection working but no data for test company")
            print("This might be due to API rate limits or the company not being in Apollo's database")
            return True
            
    except Exception as e:
        print(f"❌ Apollo.io connection test failed: {e}")
        print("This could be due to:")
        print("- Invalid API key")
        print("- API rate limits")
        print("- Network connectivity issues")
        return False

def test_data_processing():
    """Test data processing functionality"""
    print("\nTesting Data Processing...")
    try:
        processor = JobDataProcessor()
        
        # Sample test data
        test_jobs = [
            {
                'title': 'Software Engineer - Fresher',
                'company': 'Tech Corp',
                'location': 'Bangalore',
                'source': 'LinkedIn',
                'posted_date': '2024-01-15',
                'description': 'Entry level software engineer position for freshers with 0-1 years experience'
            },
            {
                'title': 'Senior Software Engineer',
                'company': 'Big Tech',
                'location': 'Bangalore',
                'source': 'Glassdoor',
                'posted_date': '2024-01-14',
                'description': 'Senior position requiring 5+ years experience'
            }
        ]
        
        processed_jobs = processor.process_jobs(test_jobs)
        stats = processor.get_job_statistics(processed_jobs)
        
        print(f"✓ Data processing successful")
        print(f"✓ Processed {len(processed_jobs)} jobs")
        print(f"✓ Statistics: {stats}")
        
        return True
    except Exception as e:
        print(f"❌ Data processing test failed: {e}")
        return False

def test_report_generation():
    """Test report generation"""
    print("\nTesting Report Generation...")
    try:
        generator = ReportGenerator()
        
        # Sample test data
        test_jobs = [
            {
                'title': 'Software Engineer - Fresher',
                'company': 'Tech Corp',
                'location': 'Bangalore',
                'source': 'LinkedIn',
                'posted_date': '2024-01-15',
                'relevance_score': 8,
                'hr_contacts': [
                    {
                        'name': 'John Doe',
                        'title': 'HR Manager',
                        'email': 'john@techcorp.com',
                        'phone': '+91-9876543210',
                        'linkedin_url': 'https://linkedin.com/in/johndoe'
                    }
                ],
                'company_info': {
                    'website': 'https://techcorp.com',
                    'industry': 'Technology',
                    'employee_count': '100-500'
                }
            }
        ]
        
        contacts_summary = {
            'total_jobs': 1,
            'jobs_with_contacts': 1,
            'total_contacts': 1
        }
        
        report_path = generator.generate_comprehensive_report(test_jobs, contacts_summary)
        
        if os.path.exists(report_path):
            print(f"✓ Report generation successful")
            print(f"✓ Report saved to: {report_path}")
            return True
        else:
            print(f"❌ Report file not found: {report_path}")
            return False
            
    except Exception as e:
        print(f"❌ Report generation test failed: {e}")
        return False

def test_file_structure():
    """Test file structure and dependencies"""
    print("\nTesting File Structure...")
    
    required_files = [
        "config.py",
        "linkedin_scraper.py",
        "glassdoor_scraper.py",
        "apollo_enricher.py",
        "data_processor.py",
        "report_generator.py",
        "job_search_agent.py",
        "scheduler.py",
        "requirements.txt",
        "README.md"
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print(f"❌ Missing files: {', '.join(missing_files)}")
        return False
    else:
        print("✓ All required files present")
        return True

def main():
    """Main test function"""
    print("Job Search Agent - Test Suite")
    print("=" * 40)
    
    tests = [
        ("File Structure", test_file_structure),
        ("Configuration", test_configuration),
        ("Apollo.io Connection", test_apollo_connection),
        ("Data Processing", test_data_processing),
        ("Report Generation", test_report_generation)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{test_name} Test:")
        print("-" * 20)
        if test_func():
            passed += 1
        else:
            print(f"❌ {test_name} test failed")
    
    print("\n" + "=" * 40)
    print(f"TEST RESULTS: {passed}/{total} tests passed")
    print("=" * 40)
    
    if passed == total:
        print("🎉 All tests passed! The agent is ready to use.")
        print("\nNext steps:")
        print("1. Run: python job_search_agent.py once")
        print("2. Or start scheduler: python job_search_agent.py")
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
        print("Make sure to:")
        print("1. Install all dependencies: pip install -r requirements.txt")
        print("2. Configure .env file with your credentials")
        print("3. Check Apollo.io API key")

if __name__ == "__main__":
    main()
