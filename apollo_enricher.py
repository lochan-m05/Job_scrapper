import requests
import logging
import time
from typing import List, Dict, Optional
from config import Config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ApolloEnricher:
    def __init__(self):
        self.config = Config()
        self.api_key = self.config.APOLLO_API_KEY
        self.base_url = "https://api.apollo.io/v1"
        self.session = requests.Session()
        self.session.headers.update({
            'Cache-Control': 'no-cache',
            'Content-Type': 'application/json',
            'X-Api-Key': self.api_key
        })
        
    def search_company(self, company_name: str) -> Optional[Dict]:
        """Search for company information in Apollo"""
        try:
            # Try organization search first (more reliable)
            url = f"{self.base_url}/organizations/search"
            params = {
                'q_organization_name': company_name,
                'page': 1,
                'per_page': 1
            }
            
            response = self.session.get(url, params=params)
            response.raise_for_status()
            
            data = response.json()
            companies = data.get('organizations', [])
            
            if companies:
                return companies[0]
            else:
                # Try alternative search with domains
                return self._search_company_alternative(company_name)
                
        except Exception as e:
            logger.error(f"Error searching company '{company_name}': {str(e)}")
            return None
    
    def _search_company_alternative(self, company_name: str) -> Optional[Dict]:
        """Alternative company search method"""
        try:
            # Try mixed companies search as alternative
            url = f"{self.base_url}/mixed_companies/search"
            params = {
                'q_organization_domains': company_name,
                'page': 1,
                'per_page': 1
            }
            
            response = self.session.get(url, params=params)
            response.raise_for_status()
            
            data = response.json()
            companies = data.get('organizations', [])
            
            return companies[0] if companies else None
            
        except Exception as e:
            logger.error(f"Error in alternative company search for '{company_name}': {str(e)}")
            return None
    
    def search_contacts(self, company_id: str, company_name: str) -> List[Dict]:
        """Search for HR contacts in a company"""
        contacts = []
        
        try:
            # Search for contacts with HR-related titles
            for role in self.config.APOLLO_CONTACT_ROLES:
                url = f"{self.base_url}/mixed_people/search"
                params = {
                    'q_organization_ids': company_id,
                    'person_titles': role,
                    'page': 1,
                    'per_page': self.config.APOLLO_SEARCH_LIMIT
                }
                
                response = self.session.get(url, params=params)
                response.raise_for_status()
                
                data = response.json()
                people = data.get('people', [])
                
                for person in people:
                    contact_info = self._extract_contact_info(person)
                    if contact_info:
                        contacts.append(contact_info)
                
                # Add delay to respect rate limits
                time.sleep(0.5)
                
        except Exception as e:
            logger.error(f"Error searching contacts for company '{company_name}': {str(e)}")
        
        return contacts
    
    def _extract_contact_info(self, person: Dict) -> Optional[Dict]:
        """Extract relevant contact information from person data"""
        try:
            # Get basic information
            first_name = person.get('first_name', '')
            last_name = person.get('last_name', '')
            title = person.get('title', '')
            
            # Get contact information
            email = person.get('email', '')
            phone = person.get('phone_numbers', [{}])[0].get('sanitized_number', '') if person.get('phone_numbers') else ''
            
            # Get LinkedIn profile
            linkedin_url = person.get('linkedin_url', '')
            
            # Get organization info
            organization = person.get('organization', {})
            company_name = organization.get('name', '') if organization else ''
            
            # Only return if we have at least email or phone
            if email or phone:
                return {
                    'name': f"{first_name} {last_name}".strip(),
                    'title': title,
                    'email': email,
                    'phone': phone,
                    'linkedin_url': linkedin_url,
                    'company': company_name,
                    'contact_type': 'HR Contact'
                }
            
        except Exception as e:
            logger.warning(f"Failed to extract contact info: {str(e)}")
        
        return None
    
    def enrich_job_with_contacts(self, job: Dict) -> Dict:
        """Enrich a job posting with HR contact information"""
        company_name = job.get('company', '')
        if not company_name:
            return job
        
        logger.info(f"Enriching job at {company_name} with HR contacts")
        
        # Search for company
        company_info = self.search_company(company_name)
        if not company_info:
            logger.warning(f"Company '{company_name}' not found in Apollo")
            return job
        
        company_id = company_info.get('id')
        if not company_id:
            logger.warning(f"No company ID found for '{company_name}'")
            return job
        
        # Search for HR contacts
        contacts = self.search_contacts(company_id, company_name)
        
        # Add enrichment data to job
        enriched_job = job.copy()
        enriched_job['company_info'] = {
            'apollo_id': company_id,
            'website': company_info.get('website_url', ''),
            'industry': company_info.get('industry', ''),
            'employee_count': company_info.get('estimated_num_employees', ''),
            'description': company_info.get('short_description', '')
        }
        enriched_job['hr_contacts'] = contacts
        
        logger.info(f"Found {len(contacts)} HR contacts for {company_name}")
        return enriched_job
    
    def enrich_jobs_batch(self, jobs: List[Dict]) -> List[Dict]:
        """Enrich multiple jobs with HR contact information"""
        enriched_jobs = []
        
        for i, job in enumerate(jobs):
            try:
                enriched_job = self.enrich_job_with_contacts(job)
                enriched_jobs.append(enriched_job)
                
                # Add delay between requests to respect rate limits
                if i < len(jobs) - 1:
                    time.sleep(1)
                    
            except Exception as e:
                logger.error(f"Failed to enrich job {i+1}: {str(e)}")
                enriched_jobs.append(job)  # Add original job if enrichment fails
        
        return enriched_jobs
    
    def get_company_contacts_summary(self, enriched_jobs: List[Dict]) -> Dict:
        """Get a summary of all HR contacts found"""
        summary = {
            'total_jobs': len(enriched_jobs),
            'jobs_with_contacts': 0,
            'total_contacts': 0,
            'companies_with_contacts': set(),
            'contact_details': []
        }
        
        for job in enriched_jobs:
            contacts = job.get('hr_contacts', [])
            if contacts:
                summary['jobs_with_contacts'] += 1
                summary['total_contacts'] += len(contacts)
                summary['companies_with_contacts'].add(job.get('company', ''))
                
                for contact in contacts:
                    summary['contact_details'].append({
                        'company': job.get('company', ''),
                        'job_title': job.get('title', ''),
                        'contact_name': contact.get('name', ''),
                        'contact_title': contact.get('title', ''),
                        'email': contact.get('email', ''),
                        'phone': contact.get('phone', ''),
                        'linkedin': contact.get('linkedin_url', '')
                    })
        
        summary['companies_with_contacts'] = list(summary['companies_with_contacts'])
        return summary

if __name__ == "__main__":
    # Test the Apollo enricher
    enricher = ApolloEnricher()
    
    # Test with a sample job
    test_job = {
        'title': 'Software Engineer',
        'company': 'Google',
        'location': 'Bangalore',
        'source': 'LinkedIn'
    }
    
    enriched_job = enricher.enrich_job_with_contacts(test_job)
    print(f"Enriched job: {enriched_job}")
