from extractor.pdf_downloader import PDFDownloader
from extractor.pdf_parser import PDFParser
from extractor.data_processor import DataProcessor
from config import CONFIG

def main():
    print("🚀 Morningstar Factsheet Extractor Started\n")
    
    downloader = PDFDownloader(CONFIG['PDF_INPUT_DIR'])
    parser = PDFParser()
    processor = DataProcessor(CONFIG['EXCEL_OUTPUT_DIR'])
    
    # Option 1: Download from URLs
    urls = [
        # Add your Morningstar URLs here
        # Example: "https://www.morningstar.in/mutualfunds/f000010uho/..."
    ]
    
    for url in urls:
        pdf_path = downloader.download_from_url(url)
        if pdf_path:
            data = parser.extract_from_pdf(pdf_path)
            processor.add_data(data)
    
    # Option 2: Process local PDFs
    print("\n📂 Processing local PDFs from sample_input/ folder...\n")
    local_pdfs = downloader.get_local_pdfs()
    
    if not local_pdfs:
        print("⚠️ No PDFs found in sample_input/ folder")
        print("📝 Please add your Morningstar factsheet PDF to the sample_input/ folder")
    
    for pdf_path in local_pdfs:
        data = parser.extract_from_pdf(pdf_path)
        processor.add_data(data)
    
    # Export to Excel
    print("\n")
    output_file = processor.export_to_excel()
    
    if output_file:
        print(f"\n✅ SUCCESS! File saved at: {output_file}")
    else:
        print("\n❌ No data to export")

if __name__ == "__main__":
    main()
