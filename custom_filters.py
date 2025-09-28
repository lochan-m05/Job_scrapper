#!/usr/bin/env python3
"""
Custom Filter Examples for Advanced Job Search
"""

def filter_by_salary_range(jobs, min_salary=300000, max_salary=800000):
    """Filter jobs by salary range (in INR per annum)"""
    filtered_jobs = []
    for job in jobs:
        # Extract salary from description or salary field
        salary_text = (job.get('salary', '') + ' ' + job.get('description', '')).lower()
        
        # Look for salary indicators
        if any(indicator in salary_text for indicator in ['lpa', 'lakh', 'lac', 'rs', 'inr']):
            # Simple salary extraction (you can make this more sophisticated)
            if '3-5' in salary_text or '3 to 5' in salary_text:
                filtered_jobs.append(job)
            elif '4-6' in salary_text or '4 to 6' in salary_text:
                filtered_jobs.append(job)
            elif '5-8' in salary_text or '5 to 8' in salary_text:
                filtered_jobs.append(job)
        else:
            # If no salary mentioned, include the job
            filtered_jobs.append(job)
    
    return filtered_jobs

def filter_by_company_size(jobs, company_sizes=['100-500', '500-1000', '1000+']):
    """Filter jobs by company size"""
    filtered_jobs = []
    for job in jobs:
        company_info = job.get('company_info', {})
        employee_count = company_info.get('employee_count', '')
        
        if any(size in employee_count for size in company_sizes):
            filtered_jobs.append(job)
        elif not employee_count:  # Include if no size info
            filtered_jobs.append(job)
    
    return filtered_jobs

def filter_by_skills_required(jobs, required_skills=['Python', 'Java', 'SQL']):
    """Filter jobs by required skills"""
    filtered_jobs = []
    for job in jobs:
        description = job.get('description', '').lower()
        title = job.get('title', '').lower()
        text = f"{title} {description}"
        
        # Check if any required skills are mentioned
        if any(skill.lower() in text for skill in required_skills):
            filtered_jobs.append(job)
    
    return filtered_jobs

def filter_by_education(jobs, education_levels=['B.Tech', 'B.E', 'B.Sc', 'MCA']):
    """Filter jobs by education requirements"""
    filtered_jobs = []
    for job in jobs:
        description = job.get('description', '').lower()
        
        # Check if education requirements are mentioned
        if any(edu.lower() in description for edu in education_levels):
            filtered_jobs.append(job)
        elif 'graduate' in description or 'degree' in description:
            filtered_jobs.append(job)
        else:
            # Include if no specific education mentioned
            filtered_jobs.append(job)
    
    return filtered_jobs

def filter_by_work_mode(jobs, work_modes=['hybrid', 'remote', 'work from home']):
    """Filter jobs by work mode"""
    filtered_jobs = []
    for job in jobs:
        description = job.get('description', '').lower()
        location = job.get('location', '').lower()
        
        # Check if work mode is mentioned
        if any(mode in description or mode in location for mode in work_modes):
            filtered_jobs.append(job)
        elif 'remote' in location.lower():
            filtered_jobs.append(job)
        else:
            # Include office-based jobs too
            filtered_jobs.append(job)
    
    return filtered_jobs

def filter_by_company_type(jobs, company_types=['Product', 'Startup', 'MNC']):
    """Filter jobs by company type"""
    filtered_jobs = []
    for job in jobs:
        company_info = job.get('company_info', {})
        industry = company_info.get('industry', '')
        company_name = job.get('company', '').lower()
        
        # Simple company type detection
        if any(type_name.lower() in company_name for type_name in company_types):
            filtered_jobs.append(job)
        elif 'startup' in industry.lower() or 'product' in industry.lower():
            filtered_jobs.append(job)
        else:
            # Include all if no specific type detected
            filtered_jobs.append(job)
    
    return filtered_jobs

def apply_custom_filters(jobs, filter_config):
    """Apply multiple custom filters"""
    filtered_jobs = jobs.copy()
    
    # Apply salary filter
    if filter_config.get('salary_range'):
        min_sal, max_sal = filter_config['salary_range']
        filtered_jobs = filter_by_salary_range(filtered_jobs, min_sal, max_sal)
    
    # Apply company size filter
    if filter_config.get('company_sizes'):
        filtered_jobs = filter_by_company_size(filtered_jobs, filter_config['company_sizes'])
    
    # Apply skills filter
    if filter_config.get('required_skills'):
        filtered_jobs = filter_by_skills_required(filtered_jobs, filter_config['required_skills'])
    
    # Apply education filter
    if filter_config.get('education_levels'):
        filtered_jobs = filter_by_education(filtered_jobs, filter_config['education_levels'])
    
    # Apply work mode filter
    if filter_config.get('work_modes'):
        filtered_jobs = filter_by_work_mode(filtered_jobs, filter_config['work_modes'])
    
    # Apply company type filter
    if filter_config.get('company_types'):
        filtered_jobs = filter_by_company_type(filtered_jobs, filter_config['company_types'])
    
    return filtered_jobs

# Example usage
if __name__ == "__main__":
    # Example filter configuration
    custom_filter_config = {
        'salary_range': (300000, 800000),  # 3-8 LPA
        'company_sizes': ['100-500', '500-1000', '1000+'],
        'required_skills': ['Python', 'Java', 'SQL'],
        'education_levels': ['B.Tech', 'B.E', 'MCA'],
        'work_modes': ['hybrid', 'remote'],
        'company_types': ['Product', 'Startup']
    }
    
    print("Custom filter configuration:")
    for key, value in custom_filter_config.items():
        print(f"  {key}: {value}")
