"""OpenAI API client module for Financial Report Generator"""

import json
import re
from openai import OpenAI
from prompts import PromptManager

class OpenAIClient:
    """Handles OpenAI API interactions"""
    
    def __init__(self, api_key):
        self.client = OpenAI(api_key=api_key)
        self.prompt_manager = PromptManager()
    
    def generate_report_standard(self):
        """Generate report using standard Chat Completions API"""
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": self.prompt_manager.get_system_message()},
                    {"role": "user", "content": self.prompt_manager.get_base_prompt()}
                ],
                temperature=0.7
            )
            
            content = response.choices[0].message.content.strip()
            return self._parse_response(content)
            
        except Exception as e:
            print(f"Error with Chat Completions API: {e}")
            return None
    
    def generate_report_with_search(self):
        """Generate report with enhanced search instructions"""
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": self.prompt_manager.get_enhanced_system_message()},
                    {"role": "user", "content": self.prompt_manager.get_search_enhanced_prompt()}
                ],
                temperature=0.7
            )
            
            content = response.choices[0].message.content.strip()
            return self._parse_response(content)
            
        except Exception as e:
            print(f"Error with enhanced API: {e}")
            return None
    
    def _parse_response(self, content):
        """Parse the API response to extract JSON data"""
        try:
            # Remove markdown code blocks if present
            content = re.sub(r'```json\s*', '', content)
            content = re.sub(r'```\s*$', '', content)
            
            # Extract JSON from response (in case there's extra text)
            json_match = re.search(r'\{.*\}', content, re.DOTALL)
            if json_match:
                content = json_match.group()
            
            data = json.loads(content)
            return data.get('data', [])
            
        except Exception as e:
            print(f"Error parsing response: {e}")
            print(f"Raw content: {content}")
            return None