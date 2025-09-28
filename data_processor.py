import pandas as pd
import logging
from typing import List, Dict, Optional
from datetime import datetime, timedelta
import re
from config import Config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class JobDataProcessor:
    def __init__(self):
        self.config = Config()
        
    def process_jobs(self, jobs: List[Dict]) -> List[Dict]:
        """Process and filter job data"""
        if not jobs:
            return []
        
        logger.info(f"Processing {len(jobs)} jobs")
        
        # Convert to DataFrame for easier processing
        df = pd.DataFrame(jobs)
        
        # Apply filters
        df = self._apply_filters(df)
        
        # Clean and standardize data
        df = self._clean_data(df)
        
        # Score jobs based on relevance
        df = self._score_jobs(df)
        
        # Sort by score and other criteria
        df = self._sort_jobs(df)
        
        # Convert back to list of dictionaries
        processed_jobs = df.to_dict('records')
        
        logger.info(f"Processed {len(processed_jobs)} jobs after filtering")
        return processed_jobs
    
    def _apply_filters(self, df: pd.DataFrame) -> pd.DataFrame:
        """Apply various filters to job data"""
        original_count = len(df)
        
        # Filter by location (case-insensitive)
        if 'location' in df.columns:
            df = df[df['location'].str.contains('bangalore|bengaluru', case=False, na=False)]
        
        # Filter by experience level keywords
        if 'title' in df.columns and 'description' in df.columns:
            # Look for fresher/entry-level keywords in title or description
            fresher_keywords = [
                'fresher', 'entry level', 'entry-level', 'junior', 'trainee', 
                'graduate', '0-1 years', '0-2 years', '1-2 years', 'intern'
            ]
            
            def has_fresher_keywords(row):
                title = str(row.get('title', '')).lower()
                description = str(row.get('description', '')).lower()
                text = f"{title} {description}"
                return any(keyword in text for keyword in fresher_keywords)
            
            df = df[df.apply(has_fresher_keywords, axis=1)]
        
        # Filter out senior positions
        if 'title' in df.columns:
            senior_keywords = [
                'senior', 'lead', 'principal', 'architect', 'manager', 
                'director', 'vp', 'vice president', 'head of', '5+ years',
                '10+ years', '8+ years'
            ]
            
            def is_not_senior(row):
                title = str(row.get('title', '')).lower()
                return not any(keyword in title for keyword in senior_keywords)
            
            df = df[df.apply(is_not_senior, axis=1)]
        
        # Filter by job type if specified
        if self.config.JOB_TYPE and 'description' in df.columns:
            job_type = self.config.JOB_TYPE.lower()
            if job_type == 'full-time':
                df = df[~df['description'].str.contains('part.time|contract|freelance', case=False, na=False)]
        
        filtered_count = len(df)
        logger.info(f"Filtered from {original_count} to {filtered_count} jobs")
        
        return df
    
    def _clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean and standardize job data"""
        # Clean company names
        if 'company' in df.columns:
            df['company'] = df['company'].str.strip()
            df['company'] = df['company'].str.replace(r'\s+', ' ', regex=True)
        
        # Clean job titles
        if 'title' in df.columns:
            df['title'] = df['title'].str.strip()
            df['title'] = df['title'].str.replace(r'\s+', ' ', regex=True)
        
        # Clean locations
        if 'location' in df.columns:
            df['location'] = df['location'].str.strip()
            df['location'] = df['location'].str.replace(r'\s+', ' ', regex=True)
        
        # Clean descriptions
        if 'description' in df.columns:
            df['description'] = df['description'].str.strip()
            df['description'] = df['description'].str.replace(r'\s+', ' ', regex=True)
        
        # Standardize posted dates
        if 'posted_date' in df.columns:
            df['posted_date'] = df['posted_date'].apply(self._standardize_date)
        
        return df
    
    def _standardize_date(self, date_str: str) -> str:
        """Standardize date format"""
        if not date_str or pd.isna(date_str):
            return ""
        
        date_str = str(date_str).lower()
        
        # Handle relative dates
        if 'hour' in date_str or 'minute' in date_str:
            return datetime.now().strftime('%Y-%m-%d')
        elif 'day' in date_str:
            days_ago = re.search(r'(\d+)', date_str)
            if days_ago:
                days = int(days_ago.group(1))
                return (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
        elif 'week' in date_str:
            weeks_ago = re.search(r'(\d+)', date_str)
            if weeks_ago:
                weeks = int(weeks_ago.group(1))
                return (datetime.now() - timedelta(weeks=weeks)).strftime('%Y-%m-%d')
        
        return date_str
    
    def _score_jobs(self, df: pd.DataFrame) -> pd.DataFrame:
        """Score jobs based on relevance and quality"""
        df['relevance_score'] = 0
        
        # Score based on title keywords
        if 'title' in df.columns:
            high_value_keywords = [
                'software engineer', 'developer', 'programmer', 'python', 'java',
                'full stack', 'frontend', 'backend', 'data analyst', 'qa engineer'
            ]
            
            for keyword in high_value_keywords:
                df.loc[df['title'].str.contains(keyword, case=False, na=False), 'relevance_score'] += 2
        
        # Score based on company size (if available)
        if 'company_info' in df.columns:
            def score_company_size(company_info):
                if not company_info or not isinstance(company_info, dict):
                    return 0
                
                employee_count = company_info.get('employee_count', '')
                if isinstance(employee_count, str):
                    if '1000+' in employee_count or '10000+' in employee_count:
                        return 3
                    elif '100+' in employee_count or '500+' in employee_count:
                        return 2
                    elif '10+' in employee_count or '50+' in employee_count:
                        return 1
                return 0
            
            df['company_score'] = df['company_info'].apply(score_company_size)
            df['relevance_score'] += df['company_score']
        
        # Score based on HR contacts availability
        if 'hr_contacts' in df.columns:
            def score_contacts(contacts):
                if not contacts:
                    return 0
                return min(len(contacts), 3)  # Max 3 points for contacts
            
            df['contact_score'] = df['hr_contacts'].apply(score_contacts)
            df['relevance_score'] += df['contact_score']
        
        # Score based on job source
        if 'source' in df.columns:
            df.loc[df['source'] == 'LinkedIn', 'relevance_score'] += 1
        
        # Score based on recency
        if 'posted_date' in df.columns:
            def score_recency(date_str):
                if not date_str:
                    return 0
                try:
                    if isinstance(date_str, str) and len(date_str) == 10:  # YYYY-MM-DD format
                        job_date = datetime.strptime(date_str, '%Y-%m-%d')
                        days_ago = (datetime.now() - job_date).days
                        if days_ago <= 1:
                            return 3
                        elif days_ago <= 3:
                            return 2
                        elif days_ago <= 7:
                            return 1
                except:
                    pass
                return 0
            
            df['recency_score'] = df['posted_date'].apply(score_recency)
            df['relevance_score'] += df['recency_score']
        
        return df
    
    def _sort_jobs(self, df: pd.DataFrame) -> pd.DataFrame:
        """Sort jobs by relevance and other criteria"""
        # Sort by relevance score (descending), then by posted date (descending)
        sort_columns = ['relevance_score']
        
        if 'posted_date' in df.columns:
            sort_columns.append('posted_date')
        
        df = df.sort_values(by=sort_columns, ascending=[False] + [False] * (len(sort_columns) - 1))
        
        return df
    
    def get_job_statistics(self, jobs: List[Dict]) -> Dict:
        """Get statistics about the processed jobs"""
        if not jobs:
            return {}
        
        df = pd.DataFrame(jobs)
        
        stats = {
            'total_jobs': len(jobs),
            'jobs_with_contacts': len([job for job in jobs if job.get('hr_contacts')]),
            'unique_companies': df['company'].nunique() if 'company' in df.columns else 0,
            'sources': df['source'].value_counts().to_dict() if 'source' in df.columns else {},
            'top_companies': df['company'].value_counts().head(10).to_dict() if 'company' in df.columns else {},
            'average_relevance_score': df['relevance_score'].mean() if 'relevance_score' in df.columns else 0,
            'jobs_by_date': df['posted_date'].value_counts().to_dict() if 'posted_date' in df.columns else {}
        }
        
        return stats
    
    def filter_by_criteria(self, jobs: List[Dict], criteria: Dict) -> List[Dict]:
        """Filter jobs by specific criteria"""
        filtered_jobs = jobs.copy()
        
        # Filter by minimum relevance score
        if 'min_relevance_score' in criteria:
            min_score = criteria['min_relevance_score']
            filtered_jobs = [job for job in filtered_jobs if job.get('relevance_score', 0) >= min_score]
        
        # Filter by companies with HR contacts
        if criteria.get('only_with_contacts', False):
            filtered_jobs = [job for job in filtered_jobs if job.get('hr_contacts')]
        
        # Filter by specific companies
        if 'companies' in criteria and criteria['companies']:
            company_list = [c.lower() for c in criteria['companies']]
            filtered_jobs = [job for job in filtered_jobs if job.get('company', '').lower() in company_list]
        
        # Filter by specific job titles
        if 'job_titles' in criteria and criteria['job_titles']:
            title_list = [t.lower() for t in criteria['job_titles']]
            filtered_jobs = [job for job in filtered_jobs if any(title in job.get('title', '').lower() for title in title_list)]
        
        # Filter by date range
        if 'date_from' in criteria or 'date_to' in criteria:
            date_from = criteria.get('date_from')
            date_to = criteria.get('date_to')
            
            def is_in_date_range(job):
                job_date = job.get('posted_date', '')
                if not job_date:
                    return True  # Include jobs without dates
                
                try:
                    if isinstance(job_date, str) and len(job_date) == 10:
                        job_dt = datetime.strptime(job_date, '%Y-%m-%d')
                        if date_from and job_dt < datetime.strptime(date_from, '%Y-%m-%d'):
                            return False
                        if date_to and job_dt > datetime.strptime(date_to, '%Y-%m-%d'):
                            return False
                except:
                    pass
                return True
            
            filtered_jobs = [job for job in filtered_jobs if is_in_date_range(job)]
        
        return filtered_jobs

if __name__ == "__main__":
    # Test the data processor
    processor = JobDataProcessor()
    
    # Sample test data
    test_jobs = [
        {
            'title': 'Software Engineer - Fresher',
            'company': 'Tech Corp',
            'location': 'Bangalore',
            'source': 'LinkedIn',
            'posted_date': '2024-01-15',
            'description': 'Entry level software engineer position for freshers'
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
    
    print(f"Processed {len(processed_jobs)} jobs")
    print(f"Statistics: {stats}")
