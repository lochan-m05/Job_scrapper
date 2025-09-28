import time
import json
import logging
import requests
from typing import List, Dict, Optional
from bs4 import BeautifulSoup
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

class GlassdoorJobScraper:
    def __init__(self):
        self.config = Config()
        self.driver = None
        self.jobs = []
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
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
    
    def search_jobs_selenium(self, keyword: str) -> List[Dict]:
        """Search for jobs using Selenium (for dynamic content)"""
        jobs = []
        try:
            # Construct Glassdoor search URL
            search_url = f"https://www.glassdoor.com/Job/jobs.htm?sc.keyword={keyword}&locT=C&locId=1157405&jobType=&fromAge=1&minSalary=0&includeNoSalaryJobs=true&radius=100&cityId=-1"
            
            self.driver.get(search_url)
            time.sleep(3)
            
            # Wait for jobs to load
            try:
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "[data-test='jobListing']"))
                )
            except TimeoutException:
                logger.warning(f"No jobs found for keyword: {keyword}")
                return jobs
            
            # Scroll to load more jobs
            self._scroll_and_load_jobs()
            
            # Extract job information
            job_elements = self.driver.find_elements(By.CSS_SELECTOR, "[data-test='jobListing']")
            
            for job_element in job_elements:
                try:
                    job_data = self._extract_job_data_selenium(job_element)
                    if job_data:
                        jobs.append(job_data)
                except Exception as e:
                    logger.warning(f"Failed to extract job data: {str(e)}")
                    continue
                    
        except Exception as e:
            logger.error(f"Error searching jobs for keyword '{keyword}': {str(e)}")
            
        return jobs
    
    def search_jobs_requests(self, keyword: str) -> List[Dict]:
        """Search for jobs using requests (for static content)"""
        jobs = []
        try:
            # Glassdoor search URL
            search_url = f"https://www.glassdoor.com/Job/jobs.htm"
            params = {
                'sc.keyword': keyword,
                'locT': 'C',
                'locId': '1157405',  # Bangalore location ID
                'jobType': '',
                'fromAge': '1',  # Last 24 hours
                'minSalary': '0',
                'includeNoSalaryJobs': 'true',
                'radius': '100',
                'cityId': '-1'
            }
            
            response = self.session.get(search_url, params=params)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find job listings
            job_elements = soup.find_all('div', {'data-test': 'jobListing'})
            
            for job_element in job_elements:
                try:
                    job_data = self._extract_job_data_requests(job_element)
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
        max_scrolls = 3
        
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
    
    def _extract_job_data_selenium(self, job_element) -> Optional[Dict]:
        """Extract job data from a job element using Selenium"""
        try:
            # Extract job title
            title_element = job_element.find_element(By.CSS_SELECTOR, "[data-test='job-title']")
            title = title_element.text.strip()
            
            # Extract company name
            company_element = job_element.find_element(By.CSS_SELECTOR, "[data-test='employer-name']")
            company = company_element.text.strip()
            
            # Extract location
            location_element = job_element.find_element(By.CSS_SELECTOR, "[data-test='job-location']")
            location = location_element.text.strip()
            
            # Extract salary if available
            salary = ""
            try:
                salary_element = job_element.find_element(By.CSS_SELECTOR, "[data-test='detailSalary']")
                salary = salary_element.text.strip()
            except NoSuchElementException:
                pass
            
            # Extract job URL
            job_url = ""
            try:
                link_element = job_element.find_element(By.CSS_SELECTOR, "a[data-test='job-link']")
                job_url = link_element.get_attribute("href")
            except NoSuchElementException:
                pass
            
            # Extract posted date
            posted_date = ""
            try:
                date_element = job_element.find_element(By.CSS_SELECTOR, "[data-test='job-age']")
                posted_date = date_element.text.strip()
            except NoSuchElementException:
                pass
            
            return {
                "title": title,
                "company": company,
                "location": location,
                "salary": salary,
                "url": job_url,
                "posted_date": posted_date,
                "source": "Glassdoor",
                "experience_level": self.config.EXPERIENCE_LEVEL
            }
            
        except Exception as e:
            logger.warning(f"Failed to extract job data: {str(e)}")
            return None
    
    def _extract_job_data_requests(self, job_element) -> Optional[Dict]:
        """Extract job data from a job element using BeautifulSoup"""
        try:
            # Extract job title
            title_element = job_element.find('a', {'data-test': 'job-title'})
            title = title_element.text.strip() if title_element else ""
            
            # Extract company name
            company_element = job_element.find('div', {'data-test': 'employer-name'})
            company = company_element.text.strip() if company_element else ""
            
            # Extract location
            location_element = job_element.find('div', {'data-test': 'job-location'})
            location = location_element.text.strip() if location_element else ""
            
            # Extract salary if available
            salary_element = job_element.find('div', {'data-test': 'detailSalary'})
            salary = salary_element.text.strip() if salary_element else ""
            
            # Extract job URL
            job_url = ""
            if title_element:
                job_url = title_element.get('href', '')
                if job_url and not job_url.startswith('http'):
                    job_url = f"https://www.glassdoor.com{job_url}"
            
            # Extract posted date
            date_element = job_element.find('div', {'data-test': 'job-age'})
            posted_date = date_element.text.strip() if date_element else ""
            
            return {
                "title": title,
                "company": company,
                "location": location,
                "salary": salary,
                "url": job_url,
                "posted_date": posted_date,
                "source": "Glassdoor",
                "experience_level": self.config.EXPERIENCE_LEVEL
            }
            
        except Exception as e:
            logger.warning(f"Failed to extract job data: {str(e)}")
            return None
    
    def search_all_keywords(self) -> List[Dict]:
        """Search for jobs using all configured keywords"""
        all_jobs = []
        
        # Try Selenium first, fallback to requests
        try:
            self.setup_driver()
            use_selenium = True
        except Exception as e:
            logger.warning(f"Failed to setup Selenium driver: {str(e)}. Using requests method.")
            use_selenium = False
        
        for keyword in self.config.JOB_KEYWORDS:
            logger.info(f"Searching Glassdoor for jobs with keyword: {keyword}")
            
            if use_selenium:
                jobs = self.search_jobs_selenium(keyword)
            else:
                jobs = self.search_jobs_requests(keyword)
                
            all_jobs.extend(jobs)
            
            # Add delay between searches
            time.sleep(2)
        
        # Remove duplicates based on title and company
        unique_jobs = self._remove_duplicates(all_jobs)
        logger.info(f"Found {len(unique_jobs)} unique jobs from Glassdoor")
        
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
    scraper = GlassdoorJobScraper()
    try:
        jobs = scraper.search_all_keywords()
        print(f"Found {len(jobs)} jobs")
        for job in jobs[:5]:  # Print first 5 jobs
            print(f"- {job['title']} at {job['company']}")
    finally:
        scraper.close()
