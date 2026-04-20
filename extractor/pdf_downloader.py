import requests
import os
from pathlib import Path

class PDFDownloader:
    def __init__(self, output_dir='sample_input'):
        self.output_dir = output_dir
        Path(output_dir).mkdir(exist_ok=True)
    
    def download_from_url(self, url):
        """Download PDF from Morningstar URL"""
        try:
            print(f"📥 Downloading PDF from: {url}")
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            
            filename = f"factsheet_{len(os.listdir(self.output_dir))}.pdf"
            filepath = os.path.join(self.output_dir, filename)
            
            with open(filepath, 'wb') as f:
                f.write(response.content)
            
            print(f"✅ PDF downloaded: {filepath}")
            return filepath
        except Exception as e:
            print(f"❌ Download failed: {str(e)}")
            return None
    
    def get_local_pdfs(self):
        """Get all local PDF files"""
        pdfs = []
        if os.path.exists(self.output_dir):
            pdfs = [os.path.join(self.output_dir, f) 
                   for f in os.listdir(self.output_dir) 
                   if f.endswith('.pdf')]
        return pdfs
