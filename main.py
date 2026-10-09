import os
import pandas as pd
from pathlib import Path
import pdfplumber




BASE_DIR = Path(__file__).parent
INPUT_DIR = BASE_DIR / 'input'
OUTPUT_DIR = BASE_DIR / 'output'

os.makedirs(INPUT_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

PDF_FILE = next(INPUT_DIR.glob(pattern="*.pdf"))

with pdfplumber.open(PDF_FILE) as pdf:

    ...
        

