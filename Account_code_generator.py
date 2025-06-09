import os
import re
import csv
from collections import defaultdict

def clean_filename(filename):
    # Remove extension
    filename = re.sub(r'\.pdf$', '', filename, flags=re.IGNORECASE)
    # Replace symbols with space
    filename = re.sub(r'[-_\.]+', ' ', filename)
    # Collapse multiple spaces and strip
    return filename.strip()

def generate_unique_ids(cleaned_names):
    counter = defaultdict(int)
    ids = []

    for name in cleaned_names:
        prefix = name[:3].upper()
        counter[prefix] += 1
        ids.append(f"{prefix}{counter[prefix]:03d}")
    
    return ids

def process_files(directory, output_csv):
    filenames = [f for f in os.listdir(directory) if f.lower().endswith('.pdf')]
    cleaned_names = [clean_filename(f) for f in filenames]
    ids = generate_unique_ids(cleaned_names)

    with open(output_csv, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Modified Name", "ID"])
        for name, id_ in zip(cleaned_names, ids):
            writer.writerow([name, id_])

# 🔧 Set your folder path and output CSV name
directory_path = r'E:\PROJECT\UPWORK\40540837\5\invoices\Sales'
output_csv_file = os.path.join(directory_path, 'output.csv')

process_files(directory_path, output_csv_file)
