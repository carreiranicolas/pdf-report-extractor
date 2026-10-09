import os
from pathlib import Path
from PyPDF2 import PdfReader

BASE_DIR = Path(__file__).parent
INPUT_DIR = BASE_DIR / 'input'
OUTPUT_DIR = BASE_DIR / 'output'

os.makedirs(INPUT_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

PDF_FILE = next(INPUT_DIR.glob(pattern="*.pdf"))

reader = PdfReader(PDF_FILE)

