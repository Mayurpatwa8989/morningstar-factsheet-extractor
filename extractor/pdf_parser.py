import pdfplumber
import re

class PDFParser:
    def __init__(self):
        self.extracted_data = {}
    
    def extract_from_pdf(self, pdf_path):
        """Extract data from Morningstar factsheet PDF"""
        try:
            print(f"📄 Parsing: {pdf_path}")
            with pdfplumber.open(pdf_path) as pdf:
                text = ""
                for page in pdf.pages:
                    text += page.extract_text() or ""
            
            return self.parse_text(text)
        except Exception as e:
            print(f"❌ Parse error: {str(e)}")
            return {}
    
    def parse_text(self, text):
        """Extract specific fields from text"""
        data = {}
        
        # Extract Scheme Name
        scheme_match = re.search(r'([A-Za-z0-9\s\-&]+(?:Fund|Plan|Scheme).*?)(?:\n|ISIN)', text)
        data['Scheme Name'] = scheme_match.group(1).strip() if scheme_match else "N/A"
        
        # Extract ISIN Code
        isin_match = re.search(r'ISIN[:\s]*([A-Z]{2}[A-Z0-9]{9}[0-9])', text)
        data['ISIN Code'] = isin_match.group(1) if isin_match else "N/A"
        
        # Extract Morningstar Rating
        rating_match = re.search(r'Morningstar Rating[:\s]*(\★+|[0-9]+\s*(?:star)?)', text)
        data['Morningstar Rating'] = rating_match.group(1) if rating_match else "N/A"
        
        # Extract Inception Date
        inception_match = re.search(r'Inception[:\s]*(\d{1,2}[/-](?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[/-]\d{4})', text, re.IGNORECASE)
        data['Inception Date'] = inception_match.group(1) if inception_match else "N/A"
        
        # Extract Fund Company
        company_match = re.search(r'(?:Fund House|Company)[:\s]*([A-Za-z\s&]+?)(?:\n|Website)', text, re.IGNORECASE)
        data['Fund Company'] = company_match.group(1).strip() if company_match else "N/A"
        
        # Extract Manager Name
        manager_match = re.search(r'(?:Fund Manager|Manager)[:\s]*([A-Za-z\s]+?)(?:\n|,)', text, re.IGNORECASE)
        data['Manager Name'] = manager_match.group(1).strip() if manager_match else "N/A"
        
        # Extract Website
        website_match = re.search(r'(?:Website|www)[:\s]*(https?://[^\s]+|www\.[^\s]+)', text)
        data['Website'] = website_match.group(1) if website_match else "N/A"
        
        # Extract Exit Load
        exitload_match = re.search(r'Exit Load[:\s]*([^\n]+)', text)
        data['Exit Load'] = exitload_match.group(1).strip() if exitload_match else "N/A"
        
        return data
