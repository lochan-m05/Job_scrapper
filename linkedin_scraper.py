import time
import json
import logging
from typing import List, Dict, Optional
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from config import Config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LinkedInJobScraper:
    def __init__(self):
        self.config = Config()
        self.driver = None
        self.jobs = []
        
    def setup_driver(self):
        """Setup Chrome driver with appropriate options"""
        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
        
        # Uncomment for headless mode
        # chrome_options.add_argument("--headless")
        
        self.driver = webdriver.Chrome(
            service=webdriver.chrome.service.Service(ChromeDriverManager().install()),
            options=chrome_options
        )
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
    def login_to_linkedin(self):
        """Login to LinkedIn"""
        try:
            self.driver.get("https://www.linkedin.com/login")
            
            # Wait for login form
            email_field = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "username"))
            )
            password_field = self.driver.find_element(By.ID, "password")
            
            # Enter credentials
            email_field.send_keys(self.config.LINKEDIN_EMAIL)
            password_field.send_keys(self.config.LINKEDIN_PASSWORD)
            
            # Click login button
            login_button = self.driver.find_element(By.XPATH, "//button[@type='submit']")
            login_button.click()
            
            # Wait for successful login
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "global-nav"))
            )
            
            logger.info("Successfully logged into LinkedIn")
            return True
            
        except Exception as e:
            logger.error(f"Failed to login to LinkedIn: {str(e)}")
            return False
    
    def search_jobs(self, keyword: str) -> List[Dict]:
        """Search for jobs with specific keyword"""
        jobs = []
        try:
            # Navigate to jobs page
            search_url = f"https://www.linkedin.com/jobs/search/?keywords={keyword}&location={self.config.LOCATION}&f_E=2&f_JT=F&f_TPR=r86400"
            self.driver.get(search_url)
            
            # Wait for jobs to load
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "jobs-search-results-list"))
            )
            
            # Scroll to load more jobs
            self._scroll_and_load_jobs()
            
            # Extract job information
            job_elements = self.driver.find_elements(By.CSS_SELECTOR, ".jobs-search-results__list-item")
            
            for job_element in job_elements:
                try:
                    job_data = self._extract_job_data(job_element)
                    if job_data:
                        jobs.append(job_data)
                except Exception as e:
                    logger.warning(f"Failed to extract job data: {str(e)}")
                    continue
                    
        except Exception as e:
            logger.error(f"Error searching jobs for keyword '{keyword}': {str(e)}")
            
        return jobs
    
    def _scroll_and_load_jobs(self):
        """Scroll down to load more jobs"""
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        scroll_attempts = 0
        max_scrolls = 5
        
        while scroll_attempts < max_scrolls:
            # Scroll down
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            
            # Check if new content loaded
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
                
            last_height = new_height
            scroll_attempts += 1
    
    def _extract_job_data(self, job_element) -> Optional[Dict]:
        """Extract job data from a job element"""
        try:
            # Click on job to get more details
            job_element.click()
            time.sleep(2)
            
            # Extract basic information
            title_element = job_element.find_element(By.CSS_SELECTOR, ".job-card-list__title")
            title = title_element.text.strip()
            
            company_element = job_element.find_element(By.CSS_SELECTOR, ".job-card-container__company-name")
            company = company_element.text.strip()
            
            location_element = job_element.find_element(By.CSS_SELECTOR, ".job-card-container__metadata-item")
            location = location_element.text.strip()
            
            # Try to get job description
            description = ""
            try:
                desc_element = self.driver.find_element(By.CSS_SELECTOR, ".jobs-description-content__text")
                description = desc_element.text.strip()
            except NoSuchElementException:
                pass
            
            # Try to get job URL
            job_url = ""
            try:
                link_element = job_element.find_element(By.CSS_SELECTOR, "a.job-card-list__title-link")
                job_url = link_element.get_attribute("href")
            except NoSuchElementException:
                pass
            
            # Try to get posted date
            posted_date = ""
            try:
                date_element = job_element.find_element(By.CSS_SELECTOR, "time")
                posted_date = date_element.get_attribute("datetime")
            except NoSuchElementException:
                pass
            
            return {
                "title": title,
                "company": company,
                "location": location,
                "description": description,
                "url": job_url,
                "posted_date": posted_date,
                "source": "LinkedIn",
                "experience_level": self.config.EXPERIENCE_LEVEL
            }
            
        except Exception as e:
            logger.warning(f"Failed to extract job data: {str(e)}")
            return None
    
    def search_all_keywords(self) -> List[Dict]:
        """Search for jobs using all configured keywords"""
        all_jobs = []
        
        if not self.login_to_linkedin():
            return all_jobs
        
        for keyword in self.config.JOB_KEYWORDS:
            logger.info(f"Searching for jobs with keyword: {keyword}")
            jobs = self.search_jobs(keyword)
            all_jobs.extend(jobs)
            
            # Add delay between searches
            time.sleep(3)
        
        # Remove duplicates based on title and company
        unique_jobs = self._remove_duplicates(all_jobs)
        logger.info(f"Found {len(unique_jobs)} unique jobs from LinkedIn")
        
        return unique_jobs
    
    def _remove_duplicates(self, jobs: List[Dict]) -> List[Dict]:
        """Remove duplicate jobs based on title and company"""
        seen = set()
        unique_jobs = []
        
        for job in jobs:
            key = (job.get("title", "").lower(), job.get("company", "").lower())
            if key not in seen:
                seen.add(key)
                unique_jobs.append(job)
                
        return unique_jobs
    
    def close(self):
        """Close the browser"""
        if self.driver:
            self.driver.quit()

if __name__ == "__main__":
    scraper = LinkedInJobScraper()
    try:
        scraper.setup_driver()
        jobs = scraper.search_all_keywords()
        print(f"Found {len(jobs)} jobs")
        for job in jobs[:5]:  # Print first 5 jobs
            print(f"- {job['title']} at {job['company']}")
    finally:
        scraper.close()
