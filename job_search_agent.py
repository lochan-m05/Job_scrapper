import logging
import time
from datetime import datetime
from typing import List, Dict
import schedule
import threading
from linkedin_scraper import LinkedInJobScraper
from glassdoor_scraper import GlassdoorJobScraper
from apollo_enricher import ApolloEnricher
from data_processor import JobDataProcessor
from report_generator import ReportGenerator
from config import Config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class JobSearchAgent:
    def __init__(self):
        self.config = Config()
        self.linkedin_scraper = LinkedInJobScraper()
        self.glassdoor_scraper = GlassdoorJobScraper()
        self.apollo_enricher = ApolloEnricher()
        self.data_processor = JobDataProcessor()
        self.report_generator = ReportGenerator()
        self.is_running = False
        
    def run_job_search(self) -> str:
        """Run the complete job search process"""
        logger.info("Starting job search process...")
        start_time = datetime.now()
        
        try:
            # Step 1: Search for jobs on LinkedIn
            logger.info("Step 1: Searching LinkedIn for jobs...")
            linkedin_jobs = self._search_linkedin_jobs()
            logger.info(f"Found {len(linkedin_jobs)} jobs from LinkedIn")
            
            # Step 2: Search for jobs on Glassdoor
            logger.info("Step 2: Searching Glassdoor for jobs...")
            glassdoor_jobs = self._search_glassdoor_jobs()
            logger.info(f"Found {len(glassdoor_jobs)} jobs from Glassdoor")
            
            # Step 3: Combine and deduplicate jobs
            logger.info("Step 3: Combining and deduplicating jobs...")
            all_jobs = self._combine_jobs(linkedin_jobs, glassdoor_jobs)
            logger.info(f"Total unique jobs found: {len(all_jobs)}")
            
            # Step 4: Process and filter jobs
            logger.info("Step 4: Processing and filtering jobs...")
            processed_jobs = self.data_processor.process_jobs(all_jobs)
            logger.info(f"Jobs after processing: {len(processed_jobs)}")
            
            # Step 5: Enrich jobs with HR contacts
            logger.info("Step 5: Enriching jobs with HR contacts...")
            enriched_jobs = self.apollo_enricher.enrich_jobs_batch(processed_jobs)
            
            # Step 6: Get contacts summary
            contacts_summary = self.apollo_enricher.get_company_contacts_summary(enriched_jobs)
            
            # Step 7: Generate comprehensive report
            logger.info("Step 7: Generating comprehensive report...")
            report_path = self.report_generator.generate_comprehensive_report(
                enriched_jobs, contacts_summary
            )
            
            # Step 8: Log summary
            end_time = datetime.now()
            duration = end_time - start_time
            
            logger.info("=" * 50)
            logger.info("JOB SEARCH COMPLETED SUCCESSFULLY")
            logger.info("=" * 50)
            logger.info(f"Total jobs found: {len(all_jobs)}")
            logger.info(f"Jobs after filtering: {len(processed_jobs)}")
            logger.info(f"Jobs with HR contacts: {contacts_summary.get('jobs_with_contacts', 0)}")
            logger.info(f"Total HR contacts: {contacts_summary.get('total_contacts', 0)}")
            logger.info(f"Unique companies: {contacts_summary.get('companies_with_contacts', 0)}")
            logger.info(f"Report generated: {report_path}")
            logger.info(f"Total execution time: {duration}")
            logger.info("=" * 50)
            
            return report_path
            
        except Exception as e:
            logger.error(f"Error during job search: {str(e)}")
            raise
    
    def _search_linkedin_jobs(self) -> List[Dict]:
        """Search for jobs on LinkedIn"""
        try:
            self.linkedin_scraper.setup_driver()
            jobs = self.linkedin_scraper.search_all_keywords()
            return jobs
        except Exception as e:
            logger.error(f"Error searching LinkedIn: {str(e)}")
            return []
        finally:
            self.linkedin_scraper.close()
    
    def _search_glassdoor_jobs(self) -> List[Dict]:
        """Search for jobs on Glassdoor"""
        try:
            jobs = self.glassdoor_scraper.search_all_keywords()
            return jobs
        except Exception as e:
            logger.error(f"Error searching Glassdoor: {str(e)}")
            return []
        finally:
            self.glassdoor_scraper.close()
    
    def _combine_jobs(self, linkedin_jobs: List[Dict], glassdoor_jobs: List[Dict]) -> List[Dict]:
        """Combine jobs from different sources and remove duplicates"""
        all_jobs = linkedin_jobs + glassdoor_jobs
        
        # Remove duplicates based on title and company
        seen = set()
        unique_jobs = []
        
        for job in all_jobs:
            key = (job.get("title", "").lower(), job.get("company", "").lower())
            if key not in seen:
                seen.add(key)
                unique_jobs.append(job)
        
        return unique_jobs
    
    def run_scheduled_search(self):
        """Run scheduled job search"""
        if self.is_running:
            logger.warning("Job search is already running, skipping this execution")
            return
        
        self.is_running = True
        try:
            logger.info("Starting scheduled job search...")
            report_path = self.run_job_search()
            logger.info(f"Scheduled job search completed. Report: {report_path}")
        except Exception as e:
            logger.error(f"Scheduled job search failed: {str(e)}")
        finally:
            self.is_running = False
    
    def start_scheduler(self):
        """Start the job scheduler"""
        logger.info("Starting job search scheduler...")
        
        # Schedule based on configuration
        if self.config.SEARCH_FREQUENCY.lower() == "daily":
            schedule.every().day.at(self.config.SEARCH_TIME).do(self.run_scheduled_search)
            logger.info(f"Scheduled daily job search at {self.config.SEARCH_TIME}")
        elif self.config.SEARCH_FREQUENCY.lower() == "weekly":
            schedule.every().monday.at(self.config.SEARCH_TIME).do(self.run_scheduled_search)
            logger.info(f"Scheduled weekly job search on Mondays at {self.config.SEARCH_TIME}")
        else:
            logger.warning(f"Unknown search frequency: {self.config.SEARCH_FREQUENCY}")
            return
        
        # Run initial search
        logger.info("Running initial job search...")
        self.run_scheduled_search()
        
        # Keep scheduler running
        logger.info("Scheduler started. Press Ctrl+C to stop.")
        try:
            while True:
                schedule.run_pending()
                time.sleep(60)  # Check every minute
        except KeyboardInterrupt:
            logger.info("Scheduler stopped by user")
    
    def run_once(self):
        """Run job search once (for manual execution)"""
        logger.info("Running job search once...")
        return self.run_job_search()
    
    def get_job_statistics(self, jobs: List[Dict]) -> Dict:
        """Get statistics about jobs"""
        return self.data_processor.get_job_statistics(jobs)
    
    def filter_jobs(self, jobs: List[Dict], criteria: Dict) -> List[Dict]:
        """Filter jobs by specific criteria"""
        return self.data_processor.filter_by_criteria(jobs, criteria)

def main():
    """Main function to run the job search agent"""
    agent = JobSearchAgent()
    
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "once":
        # Run once
        report_path = agent.run_once()
        print(f"Job search completed. Report saved to: {report_path}")
    else:
        # Run with scheduler
        agent.start_scheduler()

if __name__ == "__main__":
    main()
