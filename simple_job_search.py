#!/usr/bin/env python3
"""
Simplified Job Search Agent - Focus on Apollo.io enrichment with manual job input
"""

import logging
import json
from datetime import datetime
from typing import List, Dict
from apollo_enricher import ApolloEnricher
from data_processor import JobDataProcessor
from report_generator import ReportGenerator
from config import Config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SimpleJobSearchAgent:
    def __init__(self):
        self.config = Config()
        self.apollo_enricher = ApolloEnricher()
        self.data_processor = JobDataProcessor()
        self.report_generator = ReportGenerator()
        
    def add_manual_jobs(self) -> List[Dict]:
        """Add some sample jobs for testing - you can replace this with real job data"""
        sample_jobs = [
            {
                'title': 'Software Engineer - Fresher',
                'company': 'Infosys',
                'location': 'Bangalore',
                'source': 'Manual',
                'posted_date': '2024-01-15',
                'description': 'Entry level software engineer position for freshers with 0-1 years experience. Looking for candidates with strong programming fundamentals.',
                'url': 'https://example.com/job1'
            },
            {
                'title': 'Junior Developer',
                'company': 'TCS',
                'location': 'Bangalore',
                'source': 'Manual',
                'posted_date': '2024-01-14',
                'description': 'Junior developer role for fresh graduates. Training will be provided. Knowledge of Java/Python preferred.',
                'url': 'https://example.com/job2'
            },
            {
                'title': 'Trainee Software Engineer',
                'company': 'Wipro',
                'location': 'Bangalore',
                'source': 'Manual',
                'posted_date': '2024-01-13',
                'description': 'Trainee position for software engineering. Perfect for freshers looking to start their career in IT.',
                'url': 'https://example.com/job3'
            },
            {
                'title': 'Entry Level Python Developer',
                'company': 'Accenture',
                'location': 'Bangalore',
                'source': 'Manual',
                'posted_date': '2024-01-12',
                'description': 'Entry level Python developer position. No prior experience required. Training provided.',
                'url': 'https://example.com/job4'
            },
            {
                'title': 'Fresher Software Developer',
                'company': 'Cognizant',
                'location': 'Bangalore',
                'source': 'Manual',
                'posted_date': '2024-01-11',
                'description': 'Software developer position for freshers. Strong problem-solving skills required.',
                'url': 'https://example.com/job5'
            }
        ]
        
        logger.info(f"Added {len(sample_jobs)} sample jobs for testing")
        return sample_jobs
    
    def run_job_search(self) -> str:
        """Run the simplified job search process"""
        logger.info("Starting simplified job search process...")
        start_time = datetime.now()
        
        try:
            # Step 1: Get sample jobs (replace with real scraping when ready)
            logger.info("Step 1: Getting sample jobs...")
            jobs = self.add_manual_jobs()
            logger.info(f"Found {len(jobs)} jobs")
            
            # Step 2: Process and filter jobs
            logger.info("Step 2: Processing and filtering jobs...")
            processed_jobs = self.data_processor.process_jobs(jobs)
            logger.info(f"Jobs after processing: {len(processed_jobs)}")
            
            # Step 3: Enrich jobs with HR contacts
            logger.info("Step 3: Enriching jobs with HR contacts...")
            enriched_jobs = self.apollo_enricher.enrich_jobs_batch(processed_jobs)
            
            # Step 4: Get contacts summary
            contacts_summary = self.apollo_enricher.get_company_contacts_summary(enriched_jobs)
            
            # Step 5: Generate comprehensive report
            logger.info("Step 4: Generating comprehensive report...")
            report_path = self.report_generator.generate_comprehensive_report(
                enriched_jobs, contacts_summary
            )
            
            # Step 6: Log summary
            end_time = datetime.now()
            duration = end_time - start_time
            
            logger.info("=" * 50)
            logger.info("JOB SEARCH COMPLETED SUCCESSFULLY")
            logger.info("=" * 50)
            logger.info(f"Total jobs found: {len(jobs)}")
            logger.info(f"Jobs after filtering: {len(processed_jobs)}")
            logger.info(f"Jobs with HR contacts: {contacts_summary.get('jobs_with_contacts', 0)}")
            logger.info(f"Total HR contacts: {contacts_summary.get('total_contacts', 0)}")
            logger.info(f"Unique companies: {len(contacts_summary.get('companies_with_contacts', []))}")
            logger.info(f"Report generated: {report_path}")
            logger.info(f"Total execution time: {duration}")
            logger.info("=" * 50)
            
            return report_path
            
        except Exception as e:
            logger.error(f"Error during job search: {str(e)}")
            raise
    
    def add_custom_jobs(self, jobs: List[Dict]) -> str:
        """Add custom jobs and enrich them with HR contacts"""
        logger.info(f"Processing {len(jobs)} custom jobs...")
        
        try:
            # Process and filter jobs
            processed_jobs = self.data_processor.process_jobs(jobs)
            
            # Enrich with HR contacts
            enriched_jobs = self.apollo_enricher.enrich_jobs_batch(processed_jobs)
            
            # Get contacts summary
            contacts_summary = self.apollo_enricher.get_company_contacts_summary(enriched_jobs)
            
            # Generate report
            report_path = self.report_generator.generate_comprehensive_report(
                enriched_jobs, contacts_summary
            )
            
            logger.info(f"Custom job processing completed. Report: {report_path}")
            return report_path
            
        except Exception as e:
            logger.error(f"Error processing custom jobs: {str(e)}")
            raise

def main():
    """Main function"""
    agent = SimpleJobSearchAgent()
    
    print("Simple Job Search Agent")
    print("=" * 30)
    print("1. Run with sample jobs")
    print("2. Add custom jobs")
    print("3. Test Apollo.io connection only")
    
    choice = input("\nEnter your choice (1-3): ").strip()
    
    if choice == "1":
        report_path = agent.run_job_search()
        print(f"\n✅ Job search completed! Report saved to: {report_path}")
        
    elif choice == "2":
        print("\nEnter job details (press Enter on empty line to finish):")
        jobs = []
        
        while True:
            print(f"\nJob {len(jobs) + 1}:")
            title = input("Job Title: ").strip()
            if not title:
                break
                
            company = input("Company: ").strip()
            location = input("Location: ").strip() or "Bangalore"
            description = input("Description: ").strip()
            url = input("Job URL (optional): ").strip()
            
            job = {
                'title': title,
                'company': company,
                'location': location,
                'source': 'Manual',
                'posted_date': datetime.now().strftime('%Y-%m-%d'),
                'description': description,
                'url': url
            }
            jobs.append(job)
        
        if jobs:
            report_path = agent.add_custom_jobs(jobs)
            print(f"\n✅ Custom jobs processed! Report saved to: {report_path}")
        else:
            print("No jobs entered.")
            
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
    
    else:
        print("Invalid choice.")

if __name__ == "__main__":
    main()
