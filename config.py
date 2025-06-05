"""Configuration module for Financial Report Generator"""

import os

class Config:
    """Configuration handler for the application"""
    
    def __init__(self, api_key_file='api_key.txt'):
        self.api_key_file = api_key_file
        self.openai_api_key = self.load_api_key()
    
    def load_api_key(self):
        """Load API key from file"""
        try:
            with open(self.api_key_file, 'r', encoding='utf-8') as file:
                api_key = file.read().strip()
                if not api_key:
                    raise ValueError("API key file is empty")
                return api_key
        except FileNotFoundError:
            print("❌ Error: api_key.txt file not found")
            print("Please create an api_key.txt file with your OpenAI API key")
            return None
        except Exception as e:
            print(f"❌ Error reading API key: {e}")
            return None
    
    @property
    def is_valid(self):
        """Check if configuration is valid"""
        return self.openai_api_key is not None