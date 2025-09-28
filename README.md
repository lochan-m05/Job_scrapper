# Automated Job Search Agent

An intelligent job search agent that automatically searches for fresher-level job openings across LinkedIn, Glassdoor, and other job sites, then enriches each job posting with HR contact information using Apollo.io.

## Features

- **Multi-Platform Job Search**: Searches LinkedIn and Glassdoor for job openings
- **Smart Filtering**: Filters for fresher/entry-level positions in Bangalore
- **HR Contact Enrichment**: Uses Apollo.io to find HR contacts and phone numbers
- **Comprehensive Reporting**: Generates detailed reports in multiple formats (Excel, HTML, JSON)
- **Scheduled Execution**: Runs automatically on a daily or weekly schedule
- **Data Processing**: Intelligent filtering and scoring of job opportunities

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Copy the example environment file and fill in your credentials:

```bash
cp env_example.txt .env
```

Edit `.env` file with your credentials:

```
# LinkedIn Credentials
LINKEDIN_EMAIL=your_linkedin_email@example.com
LINKEDIN_PASSWORD=your_linkedin_password

# Apollo.io API Key
APOLLO_API_KEY=your_apollo_api_key_here
```

### 3. Get Apollo.io API Key

1. Sign up for Apollo.io account at https://apollo.io
2. Go to Settings > API Keys
3. Generate a new API key
4. Add the key to your `.env` file

### 4. Configure Search Parameters

Edit `config.py` to customize your search:

```python
# Job Search Filters
LOCATION = "Bangalore"
EXPERIENCE_LEVEL = "fresher"
JOB_TYPE = "full-time"

# Search Keywords
JOB_KEYWORDS = [
    "software engineer",
    "developer",
    "python developer",
    # Add more keywords as needed
]

# Schedule Configuration
SEARCH_FREQUENCY = "daily"  # daily or weekly
SEARCH_TIME = "09:00"  # Time to run the search
```

## Usage

### Run Once (Manual Execution)

```bash
python job_search_agent.py once
```

### Run with Scheduler

```bash
python job_search_agent.py
```

Or use the dedicated scheduler:

```bash
python scheduler.py
```

## Output

The agent generates comprehensive reports in the `job_reports/` directory:

### Excel Report (`job_report_YYYYMMDD_HHMMSS.xlsx`)
- **Summary Sheet**: Overview of search results and statistics
- **Job Details Sheet**: Complete job information with relevance scores
- **HR Contacts Sheet**: All HR contacts with contact details
- **Company Analysis Sheet**: Company-wise analysis and job counts

### HTML Report (`job_report_YYYYMMDD_HHMMSS.html`)
- Interactive web-based report
- Easy to view and share
- Includes all job details and HR contacts

### JSON Report (`job_report_YYYYMMDD_HHMMSS.json`)
- Machine-readable format
- Complete data for further processing
- Includes metadata and statistics

## Configuration Options

### Search Filters
- **Location**: Target city for job search
- **Experience Level**: Filter for fresher/entry-level positions
- **Job Type**: Full-time, part-time, contract, internship
- **Keywords**: Customizable job title keywords
- **Industries**: Focus on specific industries

### Apollo.io Settings
- **Contact Roles**: HR roles to search for
- **Search Limit**: Maximum contacts per company
- **Rate Limiting**: Respects API rate limits

### Schedule Settings
- **Frequency**: Daily or weekly execution
- **Time**: Specific time to run the search
- **Output Directory**: Where to save reports

## Job Scoring System

Jobs are scored based on:
- **Title Keywords**: Relevance to target roles
- **Company Size**: Larger companies get higher scores
- **HR Contacts**: Availability of contact information
- **Job Source**: LinkedIn jobs get slight preference
- **Recency**: Newer jobs get higher scores

## Troubleshooting

### Common Issues

1. **LinkedIn Login Issues**
   - Ensure credentials are correct
   - Check for 2FA requirements
   - Consider using app-specific passwords

2. **Apollo.io API Issues**
   - Verify API key is valid
   - Check API rate limits
   - Ensure sufficient API credits

3. **Chrome Driver Issues**
   - The system automatically downloads ChromeDriver
   - Ensure Chrome browser is installed
   - Check internet connection

### Logs

Check the console output for detailed logs. The system provides:
- Progress updates for each step
- Error messages with context
- Final statistics and summary

## Legal and Ethical Considerations

- **Respect Rate Limits**: The system includes delays to respect website rate limits
- **Terms of Service**: Ensure compliance with LinkedIn, Glassdoor, and Apollo.io ToS
- **Data Privacy**: Handle HR contact information responsibly
- **Professional Use**: Use for legitimate job search purposes only

## Customization

### Adding New Job Sites

1. Create a new scraper class following the pattern in `linkedin_scraper.py`
2. Add the scraper to `job_search_agent.py`
3. Update the `_search_jobs` method

### Custom Filters

1. Modify the `_apply_filters` method in `data_processor.py`
2. Add new filtering criteria
3. Update the scoring system if needed

### Report Formats

1. Extend `report_generator.py` with new format methods
2. Add new output options to the main agent
3. Customize report templates

## Support

For issues and questions:
1. Check the logs for error messages
2. Verify configuration settings
3. Ensure all dependencies are installed
4. Check API credentials and limits

## License

This project is for educational and personal use. Please respect the terms of service of all platforms used.
