"""Excel file handler module for Financial Report Generator"""

import os
import pandas as pd
from datetime import datetime
from openpyxl.styles import Alignment, Font

class ExcelHandler:
    """Handles Excel file creation and formatting"""
    
    @staticmethod
    def create_excel_file(data):
        """Create Excel file from the data"""
        if not data:
            print("No data to export")
            return None
            
        try:
            df = pd.DataFrame(data)
            today = datetime.now().strftime("%Y-%m-%d")
            filename = f"Rapport_Marche_{today}.xlsx"
            
            # Get user's Downloads folder
            downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")
            filepath = os.path.join(downloads_path, filename)
            
            # Create Excel with formatting
            with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
                df.to_excel(writer, sheet_name='Rapport Quotidien', index=False)
                
                # Get the workbook and worksheet for formatting
                worksheet = writer.sheets['Rapport Quotidien']
                
                # Apply formatting
                ExcelHandler._format_worksheet(worksheet, len(data))
            
            print(f"✅ Excel file created successfully: {filepath}")
            print(f"📊 Report contains {len(data)} currency pairs")
            return filepath
            
        except Exception as e:
            print(f"❌ Error creating Excel file: {e}")
            return None
    
    @staticmethod
    def _format_worksheet(worksheet, data_rows):
        """Apply formatting to the worksheet"""
        # Adjust column widths
        column_widths = {
            'A': 15,  # Paire
            'B': 15,  # Biais_Quotidien
            'C': 50,  # Resume_Executif
            'D': 80   # Explication_Approfondie
        }
        
        for col, width in column_widths.items():
            worksheet.column_dimensions[col].width = width
        
        # Format headers
        header_font = Font(bold=True)
        for cell in worksheet[1]:
            cell.font = header_font
            cell.alignment = Alignment(horizontal='center', vertical='center')
        
        # Format data rows
        for row in worksheet.iter_rows(min_row=2):
            for cell in row:
                cell.alignment = Alignment(wrap_text=True, vertical='top')
        
        # Set row heights for better visibility
        for row in range(2, data_rows + 2):
            worksheet.row_dimensions[row].height = 60