import time
import json
import logging
import requests
import random
from typing import List, Dict, Optional
from bs4 import BeautifulSoup
from config import Config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class IndeedScraper:
    def __init__(self):
        self.config = Config()
        self.jobs = []
        
        # Setup session with proper headers
        self.session = requests.Session()
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        ]
        
        self._setup_session()
        
    def _setup_session(self):
        """Setup session with proper headers"""
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
    
    def search_jobs(self, keyword: str) -> List[Dict]:
        """Search for jobs on Indeed"""
        jobs = []
        
        try:
            # Indeed search URL
            search_url = "https://in.indeed.com/jobs"
            
            # Build parameters
            params = {
                'q': keyword,
                'l': self.config.LOCATION,
                'fromage': '7',  # Last 7 days
                'sort': 'date',  # Sort by date
                'start': '0'     # Start from first page
            }
            
            # Add delay
            time.sleep(random.uniform(2, 4))
            
            # Make request
            response = self.session.get(search_url, params=params, timeout=30)
            
            if response.status_code == 200:
                jobs = self._parse_jobs_from_html(response.text, keyword)
                logger.info(f"Found {len(jobs)} jobs for keyword '{keyword}'")
            else:
                logger.warning(f"Indeed returned status code: {response.status_code}")
                
        except Exception as e:
            logger.error(f"Error searching Indeed for keyword '{keyword}': {str(e)}")
            
        return jobs
    
    def _parse_jobs_from_html(self, html_content: str, keyword: str) -> List[Dict]:
        """Parse jobs from Indeed HTML content"""
        jobs = []
        
        try:
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Indeed job selectors
            job_elements = soup.find_all('div', {'data-jk': True})
            
            if not job_elements:
                # Try alternative selectors
                job_elements = soup.find_all('div', class_=lambda x: x and 'job' in x.lower() and 'result' in x.lower())
            
            logger.info(f"Found {len(job_elements)} job elements on Indeed")
            
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
            logger.error(f"Error parsing Indeed HTML: {str(e)}")
        
        return jobs
    
    def _extract_job_data_from_element(self, job_element) -> Optional[Dict]:
        """Extract job data from Indeed job element"""
        try:
            # Extract job ID
            job_id = job_element.get('data-jk', '')
            
            # Extract title
            title_element = job_element.find('h2', class_='jobTitle')
            if not title_element:
                title_element = job_element.find('a', {'data-jk': True})
            
            title = title_element.get_text(strip=True) if title_element else ""
            
            # Extract company
            company_element = job_element.find('span', class_='companyName')
            if not company_element:
                company_element = job_element.find('div', class_='company')
            
            company = company_element.get_text(strip=True) if company_element else ""
            
            # Extract location
            location_element = job_element.find('div', class_='companyLocation')
            if not location_element:
                location_element = job_element.find('div', class_='location')
            
            location = location_element.get_text(strip=True) if location_element else self.config.LOCATION
            
            # Extract salary if available
            salary = ""
            salary_element = job_element.find('div', class_='salary-snippet')
            if salary_element:
                salary = salary_element.get_text(strip=True)
            
            # Extract job URL
            url = ""
            link_element = job_element.find('a', href=True)
            if link_element:
                url = link_element['href']
                if url and not url.startswith('http'):
                    url = f"https://in.indeed.com{url}"
            
            # Extract posted date
            posted_date = ""
            date_element = job_element.find('span', class_='date')
            if date_element:
                posted_date = date_element.get_text(strip=True)
            
            # Extract job description snippet
            description = ""
            desc_element = job_element.find('div', class_='job-snippet')
            if desc_element:
                description = desc_element.get_text(strip=True)
            
            # Only return if we have essential data
            if title and company:
                return {
                    'title': title,
                    'company': company,
                    'location': location,
                    'salary': salary,
                    'url': url,
                    'posted_date': posted_date,
                    'description': description,
                    'source': 'Indeed',
                    'experience_level': self.config.EXPERIENCE_LEVEL,
                    'job_id': job_id
                }
            
        except Exception as e:
            logger.warning(f"Failed to extract job data: {str(e)}")
        
        return None
    
    def search_all_keywords(self) -> List[Dict]:
        """Search for jobs using all configured keywords"""
        all_jobs = []
        
        logger.info("Starting Indeed job search...")
        
        for i, keyword in enumerate(self.config.JOB_KEYWORDS):
            logger.info(f"Searching Indeed for jobs with keyword: {keyword} ({i+1}/{len(self.config.JOB_KEYWORDS)})")
            
            jobs = self.search_jobs(keyword)
            all_jobs.extend(jobs)
            
            # Add delay between searches
            if i < len(self.config.JOB_KEYWORDS) - 1:
                delay = random.uniform(5, 10)
                logger.info(f"Waiting {delay:.1f} seconds before next search...")
                time.sleep(delay)
        
        # Remove duplicates
        unique_jobs = self._remove_duplicates(all_jobs)
        logger.info(f"Found {len(unique_jobs)} unique jobs from Indeed")
        
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

# Test function
def test_indeed_scraper():
    """Test the Indeed scraper"""
    scraper = IndeedScraper()
    
    try:
        # Test with a single keyword
        test_keyword = "software engineer"
        logger.info(f"Testing Indeed with keyword: {test_keyword}")
        
        jobs = scraper.search_jobs(test_keyword)
        
        if jobs:
            print(f"✅ Successfully found {len(jobs)} jobs on Indeed:")
            for job in jobs[:3]:  # Show first 3
                print(f"  - {job['title']} at {job['company']}")
                print(f"    Location: {job['location']}")
                print(f"    URL: {job['url']}")
                print()
        else:
            print("❌ No jobs found on Indeed")
        
    except Exception as e:
        logger.error(f"Indeed test failed: {str(e)}")

if __name__ == "__main__":
    test_indeed_scraper()
