import pdfplumber
import re
import os
import csv
from pathlib import Path
from datetime import datetime

def extract_invoice_data(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        text = ''
        for page in pdf.pages:
            text += (page.extract_text() or '') + '\n'

    # Extract sender from filename (assuming format "SenderName_...pdf")
    sender = Path(pdf_path).stem.split('_')[0].replace('and', '&').title()
    
    sendername = None
    vat_match = re.search(r'^(.*VAT\s*No.*)$', text, re.IGNORECASE | re.MULTILINE)
    
    if vat_match:
        vat_line = vat_match.group(1)
        lines = text.splitlines()
        for i, line in enumerate(lines):
            if vat_line.strip() in line.strip():
                if i > 0:
                    sendername = lines[i - 1].strip()
                    break
    
    # Extract invoice number
    invoice_no = re.search(r'Invoice\s*#:\s*(\d+)', text)
    
    # Extract invoice date (looking for date after "Device date")
    invoice_date = (
    re.search(r'Invoice\s*Date[:\s]*([\d]{2}/[\d]{2}/[\d]{4})', text, re.IGNORECASE) or
    re.search(r'\b(\d{2}/\d{2}/\d{4})\b', text)  # fallback: first DD/MM/YYYY found
    )

    
    # Extract receiver (Bill To section)
    receiver = re.search(r'Bill to:\s*\n(.+)', text, re.DOTALL)
    
    # Extract total amount
    total_amount = (
        re.search(r'(Total(?: Price)?[:\s]*£\s*([\d,]+\.\d{2}))', text, re.IGNORECASE) or
        re.search(r'Total\s*([\d,]+\.\d{2})\s*£', text, re.IGNORECASE)
        )
    if total_amount:
    # Use group 2 if available (for the first pattern), otherwise group 1 (for the second pattern)
        total = total_amount.group(2) if total_amount.lastindex == 2 else total_amount.group(1)
        total = total.strip()
    else:
        total = None

    
    # Format the date to 'DD Month YYYY'
    formatted_date = None
    if invoice_date:
        date_str = invoice_date.group(1).strip()
        try:
            if '/' in date_str:
                parsed = datetime.strptime(date_str, "%d/%m/%Y")
            elif '-' in date_str:
                parsed = datetime.strptime(date_str, "%d-%m-%Y")
            else:
                parsed = datetime.strptime(date_str, "%d %B %Y")
            formatted_date = parsed.strftime("%d %B %Y")
        except ValueError:
            formatted_date = date_str  # fallback: keep original if parsing fails
    
    

    return {
        'sender': sender,        
        'invoice_date': formatted_date,
        'invoice_number': invoice_no.group(1) if invoice_no else None,
        'receiver': receiver.group(1).strip() if receiver else None,
        'total_amount': total,
        'file_name': os.path.basename(pdf_path),
        'filename formatted': os.path.basename(pdf_path).replace("_", " ").replace("-"," ").replace(".pdf",""),
        'receipt name':sendername
    }

def process_pdf_folder(folder_path, output_csv):
    # Get all PDF files in folder
    pdf_files = [os.path.join(folder_path, f) 
                for f in os.listdir(folder_path) 
                if f.lower().endswith('.pdf')]
    
    # Extract data from all PDFs
    results = []
    for pdf_file in pdf_files:
        try:
            data = extract_invoice_data(pdf_file)
            results.append(data)
        except Exception as e:
            print(f"Error processing {pdf_file}: {str(e)}")
    
    # Write to CSV
    if results:
        keys = results[0].keys()
        with open(output_csv, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            writer.writerows(results)
        print(f"Successfully processed {len(results)} invoices to {output_csv}")
    else:
        print("No valid PDFs found or processed")

# Example usage
pdf_folder = r"E:\PROJECT\UPWORK\40540837\5\invoices\WIth Reverse charges Ireland"
output_file = "invoice_data.csv"
process_pdf_folder(pdf_folder, output_file)