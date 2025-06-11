# Bulk Invoice Generator

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

A powerful Python script for generating randomized invoices in PDF, HTML, and CSV formats with realistic UK business data.

## Features

- 🚀 Generate multiple invoices with single command
- 📄 Output formats: PDF (default), HTML, and CSV summary
- 🇬🇧 UK-specific business data (companies, banks, VAT numbers)
- 🛒 Retail store receipts with supermarket items
- ⛽ Fuel transaction records
- 📱 Social media advertising line items
- ✍️ Automatic signature generation
- 📅 Date range customization (Sep-Nov 2023 by default)

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/bulk-invoice-generator.git
   cd bulk-invoice-generator
2. Install dependencies:
    ```
    pip install -r requirements.txt
3. Install wkhtmltopdf:
    ```
    Download from wkhtmltopdf.org
Or use package manager:
### Ubuntu/Debian
```
sudo apt-get install wkhtmltopdf
```
### MacOS (with Homebrew)
```
brew install --cask wkhtmltopdf
```

Usage
Basic Command
```bash
python Bulk_Invoice_Generator.py [COUNT] [OPTIONS]
```
### Options
	
| Option  | Description |
|---------|-------------|
|COUNT	| Number of invoices to generate (default: 5)|
|-t TEMPLATE, --template | TEMPLATE	Custom HTML template file (default: base_template.html)|
|--html	| Generate HTML output in addition to PDF|
|--csv	| Generate CSV summary in addition to PDF|
|--nopdf	| Skip PDF generation (only generate HTML/CSV if specified)|
|--wkhtmltopdf | PATH	Custom path to wkhtmltopdf executable|

### Examples
1. Generate 10 PDF invoices:
```
python Bulk_Invoice_Generator.py 10
```
2. Generate 5 invoices with HTML output:
```
python Bulk_Invoice_Generator.py 5 --html
```
3. Generate CSV summary only (no PDFs):

```
python Bulk_Invoice_Generator.py 20 --csv --nopdf
```
4. Use custom template and wkhtmltopdf path:

```
python Bulk_Invoice_Generator.py 3 -t my_template.html --wkhtmltopdf "C:\MyPath\wkhtmltopdf.exe"
```
## File Structure
```
├── Bulk_Invoice_Generator.py   # Main script
├── README.md                   # This documentation
├── requirements.txt            # Python dependencies
├── base_template.html          # Default invoice template
├── invoices/                   # Generated invoices (PDF/HTML)
├── signatures/                 # Generated signature images
├── assets/                     # Background patterns
│   ├── bg.png                  
│   └── backgrounds/            # Invoice backgrounds
└── fonts/                      # Fonts used (e.g., for signatures)
```

### Customization
Template Variables
All available template variables are automatically detected from the generate_invoice_data() function. Key variables include:
```
{{ company_name }}          {{ invoice_number }}
{{ company_address }}       {{ invoice_date }}
{{ client_name }}           {{ due_date }}
{{ items }}                 {{ subtotal }}
{{ vat }}                   {{ total }}
{{ bank_details }}          {{ signature }}
```

### Adding Custom Items
Edit these lists in the script:

* `PREDEFINED_ITEMS` - Main service items

* `SUPERMARKET_ITEMS` - Retail store items

* `UK_RETAIL_DATA` - Store names and taglines

* `SOCIAL_MEDIA_COMPANIES` - Ad platforms

Configuration
Environment Variables
Set default paths without modifying code:
```
# Windows
set WKHTMLTOPDF_PATH="C:\path\to\wkhtmltopdf.exe"

# Linux/Mac
export WKHTMLTOPDF_PATH="/usr/local/bin/wkhtmltopdf"
```
### Automatic Path Detection
The script checks these locations automatically:

* ### Windows:
  * C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe
  * %LOCALAPPDATA%\Programs\wkhtmltopdf\bin\wkhtmltopdf.exe

* ### Linux/Mac:
  * /usr/local/bin/wkhtmltopdf
  * /usr/bin/wkhtmltopdf

### Requirements
* Python 3.8+
* Packages (see requirements.txt):
  * `faker`
  * `pdfkit`
  * `jinja2`
  * `pillow`
  * `inflect`
  
## License
MIT License - See LICENSE file for details.