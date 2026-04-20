import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
from datetime import datetime
import os

class DataProcessor:
    def __init__(self, output_dir='output'):
        self.output_dir = output_dir
        self.all_data = []
        os.makedirs(output_dir, exist_ok=True)
    
    def add_data(self, data):
        """Add extracted data"""
        if self._validate_data(data):
            self.all_data.append(data)
            print(f"✅ Valid scheme added: {data['Scheme Name']}")
        else:
            print(f"⚠️ Invalid scheme skipped: Missing ISIN or Name mismatch")
    
    def _validate_data(self, data):
        """Validate Scheme Name and ISIN Code"""
        if not data.get('Scheme Name') or data['Scheme Name'] == "N/A":
            return False
        if not data.get('ISIN Code') or data['ISIN Code'] == "N/A":
            return False
        return True
    
    def export_to_excel(self):
        """Export all data to Excel"""
        if not self.all_data:
            print("⚠️ No valid data to export")
            return None
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_file = os.path.join(self.output_dir, f'factsheet_data_{timestamp}.xlsx')
        
        # Create DataFrame
        df = pd.DataFrame(self.all_data)
        
        # Write to Excel with formatting
        with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='Factsheet Data', index=False)
            
            # Format Excel
            worksheet = writer.sheets['Factsheet Data']
            header_fill = PatternFill(start_color="4472C4", end_color="4472C4", fill_type="solid")
            header_font = Font(bold=True, color="FFFFFF")
            
            for cell in worksheet[1]:
                cell.fill = header_fill
                cell.font = header_font
                cell.alignment = Alignment(horizontal='center', vertical='center')
            
            # Auto-adjust column widths
            for column in worksheet.columns:
                max_length = 0
                column_letter = column[0].column_letter
                for cell in column:
                    try:
                        if len(str(cell.value)) > max_length:
                            max_length = len(str(cell.value))
                    except:
                        pass
                adjusted_width = (max_length + 2)
                worksheet.column_dimensions[column_letter].width = adjusted_width
        
        print(f"📊 Excel file created: {output_file}")
        return output_file
