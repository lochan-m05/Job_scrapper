import time
import json
import logging
import requests
import random
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

class GlassdoorScraperFixed:
    def __init__(self):
        self.config = Config()
        self.driver = None
        self.jobs = []
        
        # Enhanced session with better headers and rotation
        self.session = requests.Session()
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15'
        ]
        
        self._setup_session()
        
    def _setup_session(self):
        """Setup session with anti-detection measures"""
        # Rotate user agent
        user_agent = random.choice(self.user_agents)
        
        self.session.headers.update({
            'User-Agent': user_agent,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Cache-Control': 'max-age=0'
        })
        
        # Add cookies to appear more like a real browser
        self.session.cookies.update({
            'gdId': str(random.randint(100000000, 999999999)),
            'gdToken': ''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=32))
        })
    
    def setup_driver(self):
        """Setup Chrome driver with enhanced anti-detection"""
        chrome_options = Options()
        
        # Basic options
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        # Enhanced anti-detection
        chrome_options.add_argument("--disable-web-security")
        chrome_options.add_argument("--allow-running-insecure-content")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-plugins")
        chrome_options.add_argument("--disable-images")
        chrome_options.add_argument("--disable-javascript")
        
        # Random user agent
        user_agent = random.choice(self.user_agents)
        chrome_options.add_argument(f"--user-agent={user_agent}")
        
        # Window size
        chrome_options.add_argument("--window-size=1920,1080")
        
        # Uncomment for headless mode
        # chrome_options.add_argument("--headless")
        
        try:
            self.driver = webdriver.Chrome(
                service=webdriver.chrome.service.Service(ChromeDriverManager().install()),
                options=chrome_options
            )
            
            # Execute script to hide webdriver
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            self.driver.execute_script("Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3, 4, 5]})")
            self.driver.execute_script("Object.defineProperty(navigator, 'languages', {get: () => ['en-US', 'en']})")
            
            return True
        except Exception as e:
            logger.error(f"Failed to setup Chrome driver: {str(e)}")
            return False
    
    def search_jobs_with_delays(self, keyword: str) -> List[Dict]:
        """Search for jobs with proper delays and error handling"""
        jobs = []
        
        try:
            # Use a more realistic search approach
            search_url = f"https://www.glassdoor.com/Job/jobs.htm"
            
            # Build parameters more carefully
            params = {
                'sc.keyword': keyword,
                'locT': 'C',
                'locId': '1157405',  # Bangalore
                'jobType': '',
                'fromAge': '7',  # Last 7 days instead of 1
                'minSalary': '0',
                'includeNoSalaryJobs': 'true',
                'radius': '100',
                'cityId': '-1',
                'suggestCount': '0',
                'suggestChosen': 'false',
                'clickSource': 'searchBtn'
            }
            
            # Add random delay
            time.sleep(random.uniform(2, 5))
            
            # Make request with retry logic
            max_retries = 3
            for attempt in range(max_retries):
                try:
                    # Rotate user agent for each attempt
                    self.session.headers['User-Agent'] = random.choice(self.user_agents)
                    
                    response = self.session.get(search_url, params=params, timeout=30)
                    
                    if response.status_code == 200:
                        jobs = self._parse_jobs_from_html(response.text, keyword)
                        break
                    elif response.status_code == 403:
                        logger.warning(f"403 Forbidden on attempt {attempt + 1}. Waiting...")
                        time.sleep(random.uniform(10, 20))  # Wait longer for 403
                        continue
                    else:
                        logger.warning(f"Unexpected status code: {response.status_code}")
                        time.sleep(random.uniform(5, 10))
                        continue
                        
                except requests.exceptions.RequestException as e:
                    logger.warning(f"Request failed on attempt {attempt + 1}: {str(e)}")
                    time.sleep(random.uniform(5, 15))
                    continue
            
            if not jobs:
                logger.warning(f"No jobs found for keyword '{keyword}' after {max_retries} attempts")
                
        except Exception as e:
            logger.error(f"Error searching jobs for keyword '{keyword}': {str(e)}")
            
        return jobs
    
    def _parse_jobs_from_html(self, html_content: str, keyword: str) -> List[Dict]:
        """Parse jobs from HTML content"""
        jobs = []
        
        try:
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Look for job listings - Glassdoor uses different selectors
            job_selectors = [
                '[data-test="jobListing"]',
                '.jobContainer',
                '.jobSearchResult',
                '.jobListing'
            ]
            
            job_elements = []
            for selector in job_selectors:
                elements = soup.select(selector)
                if elements:
                    job_elements = elements
                    logger.info(f"Found {len(elements)} jobs using selector: {selector}")
                    break
            
            if not job_elements:
                # Try alternative parsing
                job_elements = soup.find_all('div', class_=lambda x: x and 'job' in x.lower())
                logger.info(f"Found {len(job_elements)} jobs using alternative parsing")
            
            for job_element in job_elements:
                try:
                    job_data = self._extract_job_data_from_element(job_element)
                    if job_data:
                        job_data['search_keyword'] = keyword
                        jobs.append(job_data)
                except Exception as e:
                    logger.warning(f"Failed to extract job data: {str(e)}")
                    continue
                    
        except Exception as e:
            logger.error(f"Error parsing HTML content: {str(e)}")
        
        return jobs
    
    def _extract_job_data_from_element(self, job_element) -> Optional[Dict]:
        """Extract job data from a job element"""
        try:
            # Try multiple selectors for each field
            title_selectors = [
                '[data-test="job-title"]',
                '.jobTitle',
                '.job-title',
                'a[data-test="job-link"]',
                'h3',
                'h2'
            ]
            
            company_selectors = [
                '[data-test="employer-name"]',
                '.employerName',
                '.company-name',
                '.employer'
            ]
            
            location_selectors = [
                '[data-test="job-location"]',
                '.jobLocation',
                '.location'
            ]
            
            # Extract title
            title = self._extract_text_by_selectors(job_element, title_selectors)
            
            # Extract company
            company = self._extract_text_by_selectors(job_element, company_selectors)
            
            # Extract location
            location = self._extract_text_by_selectors(job_element, location_selectors)
            
            # Extract URL
            url = ""
            link_element = job_element.find('a', href=True)
            if link_element:
                url = link_element['href']
                if url and not url.startswith('http'):
                    url = f"https://www.glassdoor.com{url}"
            
            # Extract salary if available
            salary = ""
            salary_element = job_element.find(text=lambda text: text and ('lpa' in text.lower() or 'lakh' in text.lower() or 'rs' in text.lower()))
            if salary_element:
                salary = str(salary_element).strip()
            
            # Only return if we have essential data
            if title and company:
                return {
                    'title': title.strip(),
                    'company': company.strip(),
                    'location': location.strip() if location else 'Bangalore',
                    'salary': salary,
                    'url': url,
                    'posted_date': '',
                    'source': 'Glassdoor',
                    'experience_level': self.config.EXPERIENCE_LEVEL
                }
            
        except Exception as e:
            logger.warning(f"Failed to extract job data: {str(e)}")
        
        return None
    
    def _extract_text_by_selectors(self, element, selectors: List[str]) -> str:
        """Extract text using multiple selectors"""
        for selector in selectors:
            try:
                found_element = element.select_one(selector)
                if found_element:
                    return found_element.get_text(strip=True)
            except:
                continue
        return ""
    
    def search_all_keywords(self) -> List[Dict]:
        """Search for jobs using all configured keywords with proper delays"""
        all_jobs = []
        
        logger.info("Starting Glassdoor search with anti-detection measures...")
        
        for i, keyword in enumerate(self.config.JOB_KEYWORDS):
            logger.info(f"Searching Glassdoor for jobs with keyword: {keyword} ({i+1}/{len(self.config.JOB_KEYWORDS)})")
            
            jobs = self.search_jobs_with_delays(keyword)
            all_jobs.extend(jobs)
            
            # Add delay between searches to avoid rate limiting
            if i < len(self.config.JOB_KEYWORDS) - 1:
                delay = random.uniform(10, 20)  # 10-20 seconds between searches
                logger.info(f"Waiting {delay:.1f} seconds before next search...")
                time.sleep(delay)
        
        # Remove duplicates
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

# Test function
def test_glassdoor_scraper():
    """Test the improved Glassdoor scraper"""
    scraper = GlassdoorScraperFixed()
    
    try:
        # Test with a single keyword first
        test_keyword = "software engineer"
        logger.info(f"Testing with keyword: {test_keyword}")
        
        jobs = scraper.search_jobs_with_delays(test_keyword)
        
        if jobs:
            print(f"✅ Successfully found {len(jobs)} jobs:")
            for job in jobs[:3]:  # Show first 3
                print(f"  - {job['title']} at {job['company']}")
        else:
            print("❌ No jobs found. This might be due to:")
            print("  - Anti-bot protection")
            print("  - Rate limiting")
            print("  - Network issues")
            print("  - Changes in Glassdoor's structure")
        
    except Exception as e:
        logger.error(f"Test failed: {str(e)}")
    finally:
        scraper.close()

if __name__ == "__main__":
    test_glassdoor_scraper()
