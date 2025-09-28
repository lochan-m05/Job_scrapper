#!/usr/bin/env python3
"""
Comprehensive Job Search Solution - Focus on Working Components
"""

import logging
from datetime import datetime
from typing import List, Dict
from apollo_enricher import ApolloEnricher
from data_processor import JobDataProcessor
from report_generator import ReportGenerator
from config import Config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class JobSearchSolution:
    def __init__(self):
        self.config = Config()
        self.apollo_enricher = ApolloEnricher()
        self.data_processor = JobDataProcessor()
        self.report_generator = ReportGenerator()
        
    def get_sample_jobs(self) -> List[Dict]:
        """Get comprehensive sample jobs for different roles"""
        sample_jobs = [
            # Software Engineering Roles
            {
                'title': 'Software Engineer - Fresher',
                'company': 'Infosys',
                'location': 'Bangalore',
                'source': 'Sample',
                'posted_date': '2024-01-15',
                'description': 'Entry level software engineer position for freshers with 0-1 years experience. Strong programming fundamentals required.',
                'url': 'https://example.com/infosys-se',
                'salary': '3-5 LPA'
            },
            {
                'title': 'Junior Software Developer',
                'company': 'TCS',
                'location': 'Bangalore',
                'source': 'Sample',
                'posted_date': '2024-01-14',
                'description': 'Junior developer role for fresh graduates. Training will be provided. Knowledge of Java/Python preferred.',
                'url': 'https://example.com/tcs-junior',
                'salary': '3.5-5.5 LPA'
            },
            {
                'title': 'Python Developer - Entry Level',
                'company': 'Wipro',
                'location': 'Bangalore',
                'source': 'Sample',
                'posted_date': '2024-01-13',
                'description': 'Entry level Python developer position. No prior experience required. Training provided.',
                'url': 'https://example.com/wipro-python',
                'salary': '4-6 LPA'
            },
            {
                'title': 'Full Stack Developer - Fresher',
                'company': 'Accenture',
                'location': 'Bangalore',
                'source': 'Sample',
                'posted_date': '2024-01-12',
                'description': 'Full stack developer position for freshers. Knowledge of React, Node.js preferred.',
                'url': 'https://example.com/accenture-fullstack',
                'salary': '4-7 LPA'
            },
            {
                'title': 'Software Engineer Trainee',
                'company': 'Cognizant',
                'location': 'Bangalore',
                'source': 'Sample',
                'posted_date': '2024-01-11',
                'description': 'Software engineer trainee position. Strong problem-solving skills required.',
                'url': 'https://example.com/cognizant-trainee',
                'salary': '3.5-5 LPA'
            },
            
            # Data Analytics Roles
            {
                'title': 'Data Analyst - Fresher',
                'company': 'Deloitte',
                'location': 'Bangalore',
                'source': 'Sample',
                'posted_date': '2024-01-10',
                'description': 'Entry level data analyst position. SQL and Excel skills required.',
                'url': 'https://example.com/deloitte-data',
                'salary': '4-6 LPA'
            },
            {
                'title': 'Business Analyst - Entry Level',
                'company': 'Capgemini',
                'location': 'Bangalore',
                'source': 'Sample',
                'posted_date': '2024-01-09',
                'description': 'Business analyst role for freshers. Strong analytical skills required.',
                'url': 'https://example.com/capgemini-ba',
                'salary': '3.5-5.5 LPA'
            },
            
            # QA Testing Roles
            {
                'title': 'QA Engineer - Fresher',
                'company': 'HCL',
                'location': 'Bangalore',
                'source': 'Sample',
                'posted_date': '2024-01-08',
                'description': 'Quality assurance engineer position for freshers. Manual testing knowledge preferred.',
                'url': 'https://example.com/hcl-qa',
                'salary': '3-5 LPA'
            },
            {
                'title': 'Test Engineer - Entry Level',
                'company': 'Tech Mahindra',
                'location': 'Bangalore',
                'source': 'Sample',
                'posted_date': '2024-01-07',
                'description': 'Test engineer position for fresh graduates. Automation testing training provided.',
                'url': 'https://example.com/techm-test',
                'salary': '3.5-5 LPA'
            },
            
            # Startup Companies
            {
                'title': 'Software Developer - Startup',
                'company': 'Razorpay',
                'location': 'Bangalore',
                'source': 'Sample',
                'posted_date': '2024-01-06',
                'description': 'Software developer role at fintech startup. Fast-paced environment.',
                'url': 'https://example.com/razorpay-dev',
                'salary': '5-8 LPA'
            },
            {
                'title': 'Full Stack Developer - Early Stage',
                'company': 'Zomato',
                'location': 'Bangalore',
                'source': 'Sample',
                'posted_date': '2024-01-05',
                'description': 'Full stack developer at food tech company. React and Node.js required.',
                'url': 'https://example.com/zomato-fullstack',
                'salary': '4-7 LPA'
            },
            
            # MNC Companies
            {
                'title': 'Associate Software Engineer',
                'company': 'Microsoft',
                'location': 'Bangalore',
                'source': 'Sample',
                'posted_date': '2024-01-04',
                'description': 'Associate software engineer at Microsoft. Strong coding skills required.',
                'url': 'https://example.com/microsoft-ase',
                'salary': '8-12 LPA'
            },
            {
                'title': 'Software Engineer - Graduate',
                'company': 'Amazon',
                'location': 'Bangalore',
                'source': 'Sample',
                'posted_date': '2024-01-03',
                'description': 'Graduate software engineer position at Amazon. Problem-solving skills essential.',
                'url': 'https://example.com/amazon-graduate',
                'salary': '10-15 LPA'
            },
            {
                'title': 'Junior Developer',
                'company': 'Google',
                'location': 'Bangalore',
                'source': 'Sample',
                'posted_date': '2024-01-02',
                'description': 'Junior developer role at Google. Strong algorithms knowledge required.',
                'url': 'https://example.com/google-junior',
                'salary': '12-18 LPA'
            }
        ]
        
        logger.info(f"Generated {len(sample_jobs)} sample jobs covering various roles and companies")
        return sample_jobs
    
    def add_manual_jobs(self) -> List[Dict]:
        """Interactive function to add manual jobs"""
        print("\n" + "=" * 50)
        print("MANUAL JOB INPUT")
        print("=" * 50)
        print("Enter job details (press Enter on empty line to finish):")
        
        jobs = []
        while True:
            print(f"\nJob {len(jobs) + 1}:")
            title = input("Job Title: ").strip()
            if not title:
                break
                
            company = input("Company: ").strip()
            location = input("Location (default: Bangalore): ").strip() or "Bangalore"
            description = input("Description: ").strip()
            salary = input("Salary (optional): ").strip()
            url = input("Job URL (optional): ").strip()
            
            job = {
                'title': title,
                'company': company,
                'location': location,
                'source': 'Manual',
                'posted_date': datetime.now().strftime('%Y-%m-%d'),
                'description': description,
                'salary': salary,
                'url': url
            }
            jobs.append(job)
        
        return jobs
    
    def run_comprehensive_search(self) -> str:
        """Run comprehensive job search with sample data"""
        logger.info("Starting comprehensive job search...")
        start_time = datetime.now()
        
        try:
            # Get sample jobs
            jobs = self.get_sample_jobs()
            logger.info(f"Using {len(jobs)} sample jobs")
            
            # Process and filter jobs
            logger.info("Processing and filtering jobs...")
            processed_jobs = self.data_processor.process_jobs(jobs)
            logger.info(f"Jobs after processing: {len(processed_jobs)}")
            
            # Enrich jobs with HR contacts
            logger.info("Enriching jobs with HR contacts...")
            enriched_jobs = self.apollo_enricher.enrich_jobs_batch(processed_jobs)
            
            # Get contacts summary
            contacts_summary = self.apollo_enricher.get_company_contacts_summary(enriched_jobs)
            
            # Generate comprehensive report
            logger.info("Generating comprehensive report...")
            report_path = self.report_generator.generate_comprehensive_report(
                enriched_jobs, contacts_summary
            )
            
            # Log summary
            end_time = datetime.now()
            duration = end_time - start_time
            
            logger.info("=" * 60)
            logger.info("COMPREHENSIVE JOB SEARCH COMPLETED")
            logger.info("=" * 60)
            logger.info(f"Total jobs processed: {len(jobs)}")
            logger.info(f"Jobs after filtering: {len(processed_jobs)}")
            logger.info(f"Jobs with HR contacts: {contacts_summary.get('jobs_with_contacts', 0)}")
            logger.info(f"Total HR contacts: {contacts_summary.get('total_contacts', 0)}")
            logger.info(f"Unique companies: {len(contacts_summary.get('companies_with_contacts', []))}")
            logger.info(f"Report generated: {report_path}")
            logger.info(f"Total execution time: {duration}")
            logger.info("=" * 60)
            
            return report_path
            
        except Exception as e:
            logger.error(f"Error during comprehensive search: {str(e)}")
            raise
    
    def run_with_manual_input(self) -> str:
        """Run job search with manual job input"""
        logger.info("Starting job search with manual input...")
        
        try:
            # Get manual jobs
            jobs = self.add_manual_jobs()
            
            if not jobs:
                logger.info("No jobs entered. Exiting.")
                return None
            
            # Process jobs
            processed_jobs = self.data_processor.process_jobs(jobs)
            
            # Enrich with HR contacts
            enriched_jobs = self.apollo_enricher.enrich_jobs_batch(processed_jobs)
            
            # Get contacts summary
            contacts_summary = self.apollo_enricher.get_company_contacts_summary(enriched_jobs)
            
            # Generate report
            report_path = self.report_generator.generate_comprehensive_report(
                enriched_jobs, contacts_summary
            )
            
            logger.info(f"Manual job search completed. Report: {report_path}")
            return report_path
            
        except Exception as e:
            logger.error(f"Error during manual job search: {str(e)}")
            raise

def main():
    """Main function"""
    solution = JobSearchSolution()
    
    print("Comprehensive Job Search Solution")
    print("=" * 40)
    print("1. Run with sample jobs (comprehensive demo)")
    print("2. Add manual jobs")
    print("3. Test Apollo.io connection")
    print("4. Show current configuration")
    
    choice = input("\nEnter your choice (1-4): ").strip()
    
    if choice == "1":
        report_path = solution.run_comprehensive_search()
        print(f"\n✅ Comprehensive search completed! Report: {report_path}")
        
    elif choice == "2":
        report_path = solution.run_with_manual_input()
        if report_path:
            print(f"\n✅ Manual job search completed! Report: {report_path}")
        
    elif choice == "3":
        print("\nTesting Apollo.io connection...")
        enricher = ApolloEnricher()
        test_company = input("Enter company name to test (or press Enter for 'Google'): ").strip() or "Google"
        
        company_info = enricher.search_company(test_company)
        if company_info:
            print(f"✅ Found company: {company_info.get('name', 'Unknown')}")
            print(f"Website: {company_info.get('website_url', 'N/A')}")
            print(f"Industry: {company_info.get('industry', 'N/A')}")
        else:
            print(f"❌ Company '{test_company}' not found")
    
    elif choice == "4":
        config = Config()
        print(f"\nCurrent Configuration:")
        print(f"Location: {config.LOCATION}")
        print(f"Experience Level: {config.EXPERIENCE_LEVEL}")
        print(f"Job Type: {config.JOB_TYPE}")
        print(f"Keywords: {len(config.JOB_KEYWORDS)} keywords")
        print(f"Search Frequency: {config.SEARCH_FREQUENCY}")
        print(f"Search Time: {config.SEARCH_TIME}")
    
    else:
        print("Invalid choice.")

if __name__ == "__main__":
    main()
