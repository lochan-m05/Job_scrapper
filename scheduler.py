import schedule
import time
import logging
from job_search_agent import JobSearchAgent

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def run_job_search():
    """Function to run job search"""
    agent = JobSearchAgent()
    try:
        report_path = agent.run_job_search()
        logger.info(f"Job search completed successfully. Report: {report_path}")
    except Exception as e:
        logger.error(f"Job search failed: {str(e)}")

def main():
    """Main scheduler function"""
    from config import Config
    config = Config()
    
    logger.info("Starting Job Search Scheduler...")
    
    # Schedule based on configuration
    if config.SEARCH_FREQUENCY.lower() == "daily":
        schedule.every().day.at(config.SEARCH_TIME).do(run_job_search)
        logger.info(f"Scheduled daily job search at {config.SEARCH_TIME}")
    elif config.SEARCH_FREQUENCY.lower() == "weekly":
        schedule.every().monday.at(config.SEARCH_TIME).do(run_job_search)
        logger.info(f"Scheduled weekly job search on Mondays at {config.SEARCH_TIME}")
    else:
        logger.error(f"Unknown search frequency: {config.SEARCH_FREQUENCY}")
        return
    
    # Run initial search
    logger.info("Running initial job search...")
    run_job_search()
    
    # Keep scheduler running
    logger.info("Scheduler is running. Press Ctrl+C to stop.")
    try:
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute
    except KeyboardInterrupt:
        logger.info("Scheduler stopped by user")

if __name__ == "__main__":
    main()
