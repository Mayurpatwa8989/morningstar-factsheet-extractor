import os
from datetime import datetime

# Configuration Settings
CONFIG = {
    'PDF_INPUT_DIR': 'sample_input',
    'EXCEL_OUTPUT_DIR': 'output',
    'TIMESTAMP_FORMAT': '%Y%m%d_%H%M%S',
    'REGULAR_SCHEME_VARIANTS': ['Regular Growth', 'Regular Plan'],
    'EXCLUDE_VARIANTS': ['IDCW', 'Bonus', 'Direct', 'Dividend'],
    'EXTRACTION_TIMEOUT': 30,
}

# Create directories if they don't exist
os.makedirs(CONFIG['PDF_INPUT_DIR'], exist_ok=True)
os.makedirs(CONFIG['EXCEL_OUTPUT_DIR'], exist_ok=True)
