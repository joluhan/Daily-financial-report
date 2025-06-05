"""Main application module for Financial Report Generator"""

from datetime import datetime
from config import Config
from api_client import OpenAIClient
from excel_handler import ExcelHandler

class FinancialReportGenerator:
    """Main financial report generator application"""
    
    def __init__(self):
        self.config = Config()
        self.client = None
        self.excel_handler = ExcelHandler()
        
        if self.config.is_valid:
            self.client = OpenAIClient(self.config.openai_api_key)
    
    def generate_report_data(self):
        """Generate financial report data using OpenAI API"""
        if not self.client:
            print("❌ OpenAI client not initialized")
            return None
        
        print("📡 Calling OpenAI API...")
        
        # Try enhanced search first, then fallback to standard
        data = self.client.generate_report_with_search()
        if not data:
            print("⚠️  Enhanced API failed, trying standard Chat API...")
            data = self.client.generate_report_standard()
        
        return data
    
    def run(self):
        """Main execution function"""
        print("🚀 Starting financial report generation...")
        print(f"📅 Date: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
        
        if not self.config.is_valid:
            print("❌ Cannot proceed without valid configuration")
            return
        
        # Generate report data
        data = self.generate_report_data()
        if not data:
            print("❌ Failed to generate report data")
            return
        
        print("✅ Report data generated successfully")
        
        # Create Excel file
        filename = self.excel_handler.create_excel_file(data)
        if filename:
            print(f"🎉 Process completed! File saved as: {filename}")
        else:
            print("❌ Failed to create Excel file")

if __name__ == "__main__":
    generator = FinancialReportGenerator()
    generator.run()