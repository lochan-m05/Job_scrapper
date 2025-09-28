#!/usr/bin/env python3
"""
Interactive Filter Configuration Tool
"""

import json
from datetime import datetime
from config import Config

class FilterConfigurator:
    def __init__(self):
        self.config = Config()
        
    def show_current_filters(self):
        """Display current filter configuration"""
        print("=" * 50)
        print("CURRENT FILTER CONFIGURATION")
        print("=" * 50)
        print(f"Location: {self.config.LOCATION}")
        print(f"Experience Level: {self.config.EXPERIENCE_LEVEL}")
        print(f"Job Type: {self.config.JOB_TYPE}")
        print(f"Search Frequency: {self.config.SEARCH_FREQUENCY}")
        print(f"Search Time: {self.config.SEARCH_TIME}")
        print(f"Max Jobs per Search: {self.config.MAX_JOBS_PER_SEARCH}")
        print(f"\nJob Keywords ({len(self.config.JOB_KEYWORDS)}):")
        for i, keyword in enumerate(self.config.JOB_KEYWORDS, 1):
            print(f"  {i}. {keyword}")
        print(f"\nIndustries ({len(self.config.INDUSTRIES)}):")
        for i, industry in enumerate(self.config.INDUSTRIES, 1):
            print(f"  {i}. {industry}")
        print(f"\nHR Contact Roles ({len(self.config.APOLLO_CONTACT_ROLES)}):")
        for i, role in enumerate(self.config.APOLLO_CONTACT_ROLES, 1):
            print(f"  {i}. {role}")
    
    def configure_basic_filters(self):
        """Configure basic search filters"""
        print("\n" + "=" * 30)
        print("BASIC FILTER CONFIGURATION")
        print("=" * 30)
        
        # Location
        print(f"\nCurrent Location: {self.config.LOCATION}")
        new_location = input("Enter new location (or press Enter to keep current): ").strip()
        if new_location:
            self.config.LOCATION = new_location
        
        # Experience Level
        print(f"\nCurrent Experience Level: {self.config.EXPERIENCE_LEVEL}")
        print("Options: fresher, entry-level, 0-1 years, 1-2 years")
        new_exp = input("Enter new experience level (or press Enter to keep current): ").strip()
        if new_exp:
            self.config.EXPERIENCE_LEVEL = new_exp
        
        # Job Type
        print(f"\nCurrent Job Type: {self.config.JOB_TYPE}")
        print("Options: full-time, part-time, contract, internship")
        new_type = input("Enter new job type (or press Enter to keep current): ").strip()
        if new_type:
            self.config.JOB_TYPE = new_type
    
    def configure_keywords(self):
        """Configure job search keywords"""
        print("\n" + "=" * 30)
        print("JOB KEYWORDS CONFIGURATION")
        print("=" * 30)
        
        print("\nCurrent keywords:")
        for i, keyword in enumerate(self.config.JOB_KEYWORDS, 1):
            print(f"  {i}. {keyword}")
        
        print("\nOptions:")
        print("1. Add new keywords")
        print("2. Remove keywords")
        print("3. Replace all keywords")
        print("4. Use predefined keyword sets")
        
        choice = input("\nEnter your choice (1-4): ").strip()
        
        if choice == "1":
            self._add_keywords()
        elif choice == "2":
            self._remove_keywords()
        elif choice == "3":
            self._replace_keywords()
        elif choice == "4":
            self._use_predefined_keywords()
    
    def _add_keywords(self):
        """Add new keywords"""
        print("\nEnter new keywords (one per line, empty line to finish):")
        new_keywords = []
        while True:
            keyword = input("Keyword: ").strip()
            if not keyword:
                break
            new_keywords.append(keyword)
        
        self.config.JOB_KEYWORDS.extend(new_keywords)
        print(f"Added {len(new_keywords)} new keywords")
    
    def _remove_keywords(self):
        """Remove keywords"""
        print("\nEnter keyword numbers to remove (comma-separated):")
        for i, keyword in enumerate(self.config.JOB_KEYWORDS, 1):
            print(f"  {i}. {keyword}")
        
        try:
            indices = input("Enter numbers: ").strip()
            if indices:
                indices = [int(x.strip()) - 1 for x in indices.split(',')]
                # Remove in reverse order to maintain indices
                for i in sorted(indices, reverse=True):
                    if 0 <= i < len(self.config.JOB_KEYWORDS):
                        removed = self.config.JOB_KEYWORDS.pop(i)
                        print(f"Removed: {removed}")
        except ValueError:
            print("Invalid input")
    
    def _replace_keywords(self):
        """Replace all keywords"""
        print("\nEnter new keywords (one per line, empty line to finish):")
        new_keywords = []
        while True:
            keyword = input("Keyword: ").strip()
            if not keyword:
                break
            new_keywords.append(keyword)
        
        self.config.JOB_KEYWORDS = new_keywords
        print(f"Replaced with {len(new_keywords)} keywords")
    
    def _use_predefined_keywords(self):
        """Use predefined keyword sets"""
        predefined_sets = {
            "1": {
                "name": "Software Engineering",
                "keywords": [
                    "software engineer", "software developer", "programmer",
                    "python developer", "java developer", "full stack developer",
                    "backend developer", "frontend developer", "mobile developer"
                ]
            },
            "2": {
                "name": "Data & Analytics",
                "keywords": [
                    "data analyst", "business analyst", "data scientist",
                    "data engineer", "business intelligence", "analytics engineer",
                    "machine learning engineer", "data architect"
                ]
            },
            "3": {
                "name": "QA & Testing",
                "keywords": [
                    "quality assurance", "qa engineer", "test engineer",
                    "automation engineer", "software tester", "quality analyst",
                    "performance tester", "manual tester"
                ]
            },
            "4": {
                "name": "DevOps & Cloud",
                "keywords": [
                    "devops engineer", "cloud engineer", "site reliability engineer",
                    "aws engineer", "azure engineer", "kubernetes engineer",
                    "infrastructure engineer", "platform engineer"
                ]
            },
            "5": {
                "name": "Product & Management",
                "keywords": [
                    "product manager", "project manager", "scrum master",
                    "business analyst", "product owner", "program manager",
                    "technical product manager", "associate product manager"
                ]
            }
        }
        
        print("\nPredefined keyword sets:")
        for key, value in predefined_sets.items():
            print(f"{key}. {value['name']}")
        
        choice = input("\nSelect a set (1-5): ").strip()
        if choice in predefined_sets:
            self.config.JOB_KEYWORDS = predefined_sets[choice]["keywords"]
            print(f"Applied {predefined_sets[choice]['name']} keywords")
    
    def configure_schedule(self):
        """Configure search schedule"""
        print("\n" + "=" * 30)
        print("SCHEDULE CONFIGURATION")
        print("=" * 30)
        
        print(f"\nCurrent Frequency: {self.config.SEARCH_FREQUENCY}")
        print("Options: daily, weekly")
        new_freq = input("Enter new frequency (or press Enter to keep current): ").strip()
        if new_freq in ["daily", "weekly"]:
            self.config.SEARCH_FREQUENCY = new_freq
        
        print(f"\nCurrent Search Time: {self.config.SEARCH_TIME}")
        new_time = input("Enter new time (HH:MM format, or press Enter to keep current): ").strip()
        if new_time:
            self.config.SEARCH_TIME = new_time
    
    def configure_apollo_settings(self):
        """Configure Apollo.io settings"""
        print("\n" + "=" * 30)
        print("APOLLO.IO CONFIGURATION")
        print("=" * 30)
        
        print(f"\nCurrent Search Limit: {self.config.APOLLO_SEARCH_LIMIT}")
        new_limit = input("Enter new search limit (or press Enter to keep current): ").strip()
        if new_limit.isdigit():
            self.config.APOLLO_SEARCH_LIMIT = int(new_limit)
        
        print("\nCurrent HR Contact Roles:")
        for i, role in enumerate(self.config.APOLLO_CONTACT_ROLES, 1):
            print(f"  {i}. {role}")
        
        print("\nOptions:")
        print("1. Add new roles")
        print("2. Remove roles")
        print("3. Replace all roles")
        
        choice = input("\nEnter your choice (1-3): ").strip()
        
        if choice == "1":
            self._add_contact_roles()
        elif choice == "2":
            self._remove_contact_roles()
        elif choice == "3":
            self._replace_contact_roles()
    
    def _add_contact_roles(self):
        """Add new contact roles"""
        print("\nEnter new HR contact roles (one per line, empty line to finish):")
        new_roles = []
        while True:
            role = input("Role: ").strip()
            if not role:
                break
            new_roles.append(role)
        
        self.config.APOLLO_CONTACT_ROLES.extend(new_roles)
        print(f"Added {len(new_roles)} new roles")
    
    def _remove_contact_roles(self):
        """Remove contact roles"""
        print("\nEnter role numbers to remove (comma-separated):")
        for i, role in enumerate(self.config.APOLLO_CONTACT_ROLES, 1):
            print(f"  {i}. {role}")
        
        try:
            indices = input("Enter numbers: ").strip()
            if indices:
                indices = [int(x.strip()) - 1 for x in indices.split(',')]
                for i in sorted(indices, reverse=True):
                    if 0 <= i < len(self.config.APOLLO_CONTACT_ROLES):
                        removed = self.config.APOLLO_CONTACT_ROLES.pop(i)
                        print(f"Removed: {removed}")
        except ValueError:
            print("Invalid input")
    
    def _replace_contact_roles(self):
        """Replace all contact roles"""
        print("\nEnter new HR contact roles (one per line, empty line to finish):")
        new_roles = []
        while True:
            role = input("Role: ").strip()
            if not role:
                break
            new_roles.append(role)
        
        self.config.APOLLO_CONTACT_ROLES = new_roles
        print(f"Replaced with {len(new_roles)} roles")
    
    def save_configuration(self):
        """Save configuration to file"""
        config_data = {
            "LOCATION": self.config.LOCATION,
            "EXPERIENCE_LEVEL": self.config.EXPERIENCE_LEVEL,
            "JOB_TYPE": self.config.JOB_TYPE,
            "SEARCH_FREQUENCY": self.config.SEARCH_FREQUENCY,
            "SEARCH_TIME": self.config.SEARCH_TIME,
            "MAX_JOBS_PER_SEARCH": self.config.MAX_JOBS_PER_SEARCH,
            "JOB_KEYWORDS": self.config.JOB_KEYWORDS,
            "INDUSTRIES": self.config.INDUSTRIES,
            "APOLLO_SEARCH_LIMIT": self.config.APOLLO_SEARCH_LIMIT,
            "APOLLO_CONTACT_ROLES": self.config.APOLLO_CONTACT_ROLES,
            "last_updated": datetime.now().isoformat()
        }
        
        with open("custom_config.json", "w") as f:
            json.dump(config_data, f, indent=2)
        
        print(f"\n✅ Configuration saved to custom_config.json")
        print("To use this configuration, update your config.py file with these values.")
    
    def run_interactive_config(self):
        """Run interactive configuration"""
        print("Job Search Filter Configuration Tool")
        print("=" * 40)
        
        while True:
            print("\n" + "=" * 30)
            print("CONFIGURATION MENU")
            print("=" * 30)
            print("1. Show current filters")
            print("2. Configure basic filters")
            print("3. Configure job keywords")
            print("4. Configure schedule")
            print("5. Configure Apollo.io settings")
            print("6. Save configuration")
            print("7. Exit")
            
            choice = input("\nEnter your choice (1-7): ").strip()
            
            if choice == "1":
                self.show_current_filters()
            elif choice == "2":
                self.configure_basic_filters()
            elif choice == "3":
                self.configure_keywords()
            elif choice == "4":
                self.configure_schedule()
            elif choice == "5":
                self.configure_apollo_settings()
            elif choice == "6":
                self.save_configuration()
            elif choice == "7":
                print("Exiting configuration tool...")
                break
            else:
                print("Invalid choice. Please try again.")

def main():
    """Main function"""
    configurator = FilterConfigurator()
    configurator.run_interactive_config()

if __name__ == "__main__":
    main()
