import os
import pandas as pd
from datetime import datetime
from openai import OpenAI
import json
import re

class FinancialReportGenerator:
    def __init__(self):
        # Configuration - Load API key from file
        self.openai_api_key = self.load_api_key()
        
        # Initialize OpenAI client
        if self.openai_api_key:
            self.client = OpenAI(api_key=self.openai_api_key)
        
        # Your prompt
        self.prompt = """Génère un tableau structuré au format exportable (Excel) contenant le rapport financier quotidien pour les paires suivantes :  
BCOUSD, NATGASUSD, EURUSD, GBPJPY, XAUUSD, XAUEUR, NAS100USD, SPX500USD.
Le tableau doit contenir les colonnes suivantes :  
- **Paire**  
- **Biais Quotidien** (Haussier, Baissier ou Neutre)  
- **Résumé Exécutif** (très concis en une ligne)  
- **Explication Approfondie du Biais** (explication détaillée en plusieurs phrases)
Pour chaque paire :
1. Analyse les **facteurs fondamentaux** :  
   - Données macroéconomiques récentes (inflation, PIB, emploi, etc.)  
   - Politiques monétaires des banques centrales (Fed, BCE, BoJ, etc.)  
   - Tensions géopolitiques, conflits ou décisions politiques majeures  
   - Impact de la force ou faiblesse du Dollar Américain  
   - Tout autre élément influent (stocks, saisonnalité, demande énergétique, etc.)
2. Utilise un **langage clair et professionnel**, facile à comprendre pour un trader qui suit les marchés au quotidien. Toujours faire des recherches sur les actualités du jours pour former le biais.
3. Fournis le tableau au format exportable (fichier Excel), avec une ligne par paire et des explications précises adaptées au trading sur le timeframe H1 entre 8h et 15h heure de Paris.

Retourne UNIQUEMENT un JSON valide avec cette structure exacte :
{
  "data": [
    {
      "Paire": "BCOUSD",
      "Biais_Quotidien": "Haussier/Baissier/Neutre",
      "Resume_Executif": "résumé en une ligne",
      "Explication_Approfondie": "explication détaillée"
    }
  ]
}"""

    def load_api_key(self):
        """Load API key from api_key.txt file"""
        try:
            with open('api_key.txt', 'r', encoding='utf-8') as file:
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

    def generate_report_standard_api(self):
        """Generate report using standard Chat Completions API"""
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",  # Using gpt-4o which is more current
                messages=[
                    {"role": "system", "content": "Tu es un analyste financier expert. Réponds UNIQUEMENT avec du JSON valide."},
                    {"role": "user", "content": self.prompt}
                ],
                temperature=0.7
            )
            
            content = response.choices[0].message.content.strip()
            return self.parse_response(content)
            
        except Exception as e:
            print(f"Error with Chat Completions API: {e}")
            return None

    def generate_report_with_search(self):
        """Generate report with web search - simplified approach"""
        try:
            # Add web search instruction to the prompt
            search_prompt = self.prompt + "\n\nIMPORTANT: Recherche les actualités financières et économiques les plus récentes pour chaque paire avant de formuler ton analyse."
            
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "Tu es un analyste financier expert avec accès aux données de marché actuelles. Utilise tes connaissances les plus récentes pour analyser les marchés. Réponds UNIQUEMENT avec du JSON valide."},
                    {"role": "user", "content": search_prompt}
                ],
                temperature=0.7
            )
            
            content = response.choices[0].message.content.strip()
            return self.parse_response(content)
            
        except Exception as e:
            print(f"Error with enhanced API: {e}")
            return None

    def parse_response(self, content):
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

    def create_excel_file(self, data):
        """Create Excel file from the data"""
        if not data:
            print("No data to export")
            return None
            
        try:
            df = pd.DataFrame(data)
            today = datetime.now().strftime("%Y-%m-%d")
            filename = f"Rapport_Marche_{today}.xlsx"
            
            # Get user's Downloads folder (works on any Windows computer)
            downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")
            filepath = os.path.join(downloads_path, filename)
            
            # Create Excel with formatting
            with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
                df.to_excel(writer, sheet_name='Rapport Quotidien', index=False)
                
                # Get the workbook and worksheet for formatting
                workbook = writer.book
                worksheet = writer.sheets['Rapport Quotidien']
                
                # Adjust column widths
                worksheet.column_dimensions['A'].width = 15  # Paire
                worksheet.column_dimensions['B'].width = 15  # Biais_Quotidien
                worksheet.column_dimensions['C'].width = 50  # Resume_Executif
                worksheet.column_dimensions['D'].width = 80  # Explication_Approfondie
                
                # Wrap text and align for better readability
                from openpyxl.styles import Alignment, Font
                header_font = Font(bold=True)
                
                # Format headers
                for cell in worksheet[1]:
                    cell.font = header_font
                    cell.alignment = Alignment(horizontal='center', vertical='center')
                
                # Format data rows
                for row in worksheet.iter_rows(min_row=2):
                    for cell in row:
                        cell.alignment = Alignment(wrap_text=True, vertical='top')
                
                # Set row heights for better visibility
                for row in range(2, len(data) + 2):
                    worksheet.row_dimensions[row].height = 60
            
            print(f"✅ Excel file created successfully: {filepath}")
            print(f"📊 Report contains {len(data)} currency pairs")
            return filepath
            
        except Exception as e:
            print(f"❌ Error creating Excel file: {e}")
            return None

    def run(self):
        """Main execution function"""
        print("🚀 Starting financial report generation...")
        print(f"📅 Date: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
        
        # Check if API key is loaded
        if not self.openai_api_key:
            print("❌ Cannot proceed without API key")
            return
        
        # Try different API approaches
        print("📡 Calling OpenAI API...")
        
        # First try with enhanced search instructions
        data = self.generate_report_with_search()
        if not data:
            print("⚠️  Enhanced API failed, trying standard Chat API...")
            data = self.generate_report_standard_api()
        
        if not data:
            print("❌ Failed to generate report with both API methods")
            return
        
        print(f"✅ Report data generated successfully")
        
        # Create Excel file
        filename = self.create_excel_file(data)
        if filename:
            print(f"🎉 Process completed! File saved as: {filename}")
        else:
            print("❌ Failed to create Excel file")

if __name__ == "__main__":
    # The script will automatically load the API key from api_key.txt
    # Make sure to create this file with your OpenAI API key
    
    generator = FinancialReportGenerator()
    generator.run()