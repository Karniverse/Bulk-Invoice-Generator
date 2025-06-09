import random
import sys
import os
from faker import Faker
from jinja2 import Template
import pdfkit
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
import argparse

# === Argument Parser ===
parser = argparse.ArgumentParser(description="Generate random invoices using a given HTML template.")
parser.add_argument("count", type=int, help="Number of invoices to generate")
parser.add_argument("-t", "--template", type=str, required=True, help="Path to the HTML template file")

args = parser.parse_args()
invoice_count = args.count

# === SETTINGS ===
SIGNATURE_FONT_PATH = "fonts/PrimeraSignature.ttf"
pattern_location = "assets/bg.png"
background_location="assets/backgrounds"
SIGNATURE_DIR = "signatures"
OUTPUT_DIR = "invoices"
os.makedirs(SIGNATURE_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

uk_time = datetime.now(ZoneInfo("Europe/London"))
formatted_time = uk_time.strftime("%H:%M:%S")

fake = Faker("en_GB")
fake_ir = Faker("en_IE")
UK_BANKS = [
    "HSBC",
    "Barclays",
    "Lloyds Bank",
    "NatWest",
    "Royal Bank of Scotland",
    "Santander UK",
    "TSB Bank",
    "Metro Bank",
    "Virgin Money",
    "Nationwide Building Society"
]

PREDEFINED_ITEMS = [
    "Website Design",
    "SEO Optimization",
    "Cloud Hosting",
    "Software Development",
    "Consulting Services",
    "Technical Support",
    "Marketing Campaign",
    "Data Analysis",
    "Graphic Design",
    "Content Creation"
]

SOCIAL_MEDIA_COMPANIES = [
    "Meta",
    "Google",
    "Twitter",
    "TikTok",
    "Quora",
    "LinkedIn",
    "Pinterest",
    "Instagram",
    "YouTube",
    "Tumblr",
    "Twitch",
    "Threads"
]

SUPERMARKET_ITEMS = [
    # "Toilet Paper",
    # "Laundry Detergent",
    # "Shampoo",
    # "Toothpaste",
    # "Dish Soap",
    # "Aluminum Foil",
    # "Trash Bags",
    # "Paper Towels",
    # "Batteries",
    # "Light Bulbs",
    # "Shaving Razor",
    # "Hand Sanitizer",
    # "Notebook",
    # "Energy Drink",
    # "Ballpoint Pens",
    # "Sticky Notes",
    # "Plastic Wrap",
    # "Shower Gel",
    # "Lip Balm",
    # "Cleaning Spray",
    # "Nail Clipper"
    "Ballpoint Pens",
    "Sticky Notes",
    "Stapler",
    "Paper Clips",
    "Highlighters",
    "Notepad",
    "Scissors",
    "Printer Paper",
    "Pencil Sharpener",
    "Erasers",
    "Desk Organizer",
    "Correction Tape",
    "Glue Stick",
    "Permanent Marker",
    "File Folders",
    "Ruler",
    "Envelopes"
]

UK_RETAIL_DATA = [
    {"name": "Tesco", "tagline": "Every little helps"},
    {"name": "Sainsbury's", "tagline": "Live well for less"},
    {"name": "Asda", "tagline": "Save money. Live better"},
    {"name": "Morrisons", "tagline": "More of what matters"},
    {"name": "Aldi", "tagline": "Shop differently"},
    {"name": "Lidl", "tagline": "Big on quality, Lidl on price"},
    {"name": "Waitrose", "tagline": "Quality food, honestly priced"},
    {"name": "Iceland", "tagline": "That's why mums go to Iceland"},
    {"name": "Co-op", "tagline": "It's what we do"},
    {"name": "Marks & Spencer", "tagline": "Only the best for less"},
    {"name": "B&M", "tagline": "Big brands, big savings"},
    {"name": "Home Bargains", "tagline": "Top brands at bottom prices"},
    {"name": "Wilko", "tagline": "Where there's a Wilko, there's a way"},
    {"name": "Argos", "tagline": "Find it. Get it. Argos it."},
    {"name": "Boots", "tagline": "Let’s feel good"},
    {"name": "Superdrug", "tagline": "The beauty of everyday"},
    {"name": "Poundland", "tagline": "Amazing value every day"},
    {"name": "Costco", "tagline": "Warehouse savings, every time"},
    {"name": "Screwfix", "tagline": "Serious tools, seriously low prices"},
    {"name": "Currys", "tagline": "We help keep your tech in check"}
]


# === Load HTML template ===
try:
    with open(args.template, "r", encoding="utf-8") as f:
        invoice_template = f.read()
except FileNotFoundError:
    print(f"Error: Template file '{args.template}' not found.")
    sys.exit(1)


def clean_name(name):
    return ''.join(c for c in name if c.isalnum() or c == ' ')

def social_adverts_items():
    social_media_company = random.choice(SOCIAL_MEDIA_COMPANIES)
    qty = random.randint(1, 10)
    rate = random.choice(range(300, 10000, 500))
    total = qty * rate
    return social_media_company, social_media_company + " Ad", qty, rate, total



def generate_signature(name, filepath):
    image = Image.new('RGBA', (350, 100), (255, 255, 255, 0))
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(SIGNATURE_FONT_PATH, 40)
    bbox = draw.textbbox((0, 0), name, font=font)
    position = ((300 - (bbox[2] - bbox[0])) / 2, (100 - (bbox[3] - bbox[1])) / 2)
    draw.text(position, name, font=font, fill=(0, 0, 0))
    image.save(filepath)

def amount_to_words(amount):
    import inflect
    p = inflect.engine()
    words = p.number_to_words(int(amount)).capitalize()
    return f"{words} Pound GBP"

def generate_invoice_data():
    company_name = fake.company()
    company_name_clean = clean_name(company_name)
    address = fake.street_address()
    postal = fake.postcode()
    city = fake.city()
    email = f"sales@{company_name_clean.replace(' ', '').lower()}.com"
    phone = fake.phone_number()
    invoice_number = random.randint(1000, 99999)
    account_name = company_name_clean.replace(' ', '').lower()
    account_number = fake.bban()
    background_filename = f"{random.choice(range(1, 8))}.png"
    store_data = random.choice(UK_RETAIL_DATA)
    social_media_company, social_adverts_description, social_adverts_qty, social_adverts_rate, social_adverts_total = social_adverts_items()

    # Date range between Sep 1 - Nov 30, 2023
    start_date = datetime(2023, 9, 1)
    end_date = datetime(2023, 11, 30)
    invoice_date = fake.date_between(start_date=start_date, end_date=end_date)
    due_date = invoice_date + timedelta(days=7)

    client_name = fake.company()
    client_address = f"{fake.street_address()}, {fake.postcode()}<br>{fake.city()}, United Kingdom"

    items = []
    subtotal = 0
    for _ in range(random.randint(1, 4)):
        qty = random.randint(1, 10)
        rate = random.choice(range(30, 100, 50))
        total = qty * rate
        items.append({
            "description": random.choice(PREDEFINED_ITEMS),
            "qty": qty,
            "rate": rate,
            "total": total
        })
        subtotal += total

    vat = round(subtotal * 0.2, 2)
    total_amount = round(subtotal + vat, 2)    
    total_words = amount_to_words(total_amount)
    subtotal_words = amount_to_words(subtotal)
    
    
    uk_store_items=[]
    Store_subtotal=0
    for _ in range(random.randint(1, 1)):
        qty = random.randint(1, 3)
        rate = random.choice(range(1, 5, 1))
        total = qty * rate
        uk_store_items.append({
            "description": random.choice(SUPERMARKET_ITEMS),
            "qty": qty,
            "rate": rate,
            "total": total
        })
        Store_subtotal += total
    fuel_qty=random.choice(range(5, 9, 1))
    fuel_rate=random.choice(range(4, 7, 2))
    fuel_total=fuel_qty*fuel_rate
    fuel_total= fuel_total + 0.2 * fuel_total    





    # Signature
    signature_file = os.path.join(SIGNATURE_DIR, f"{company_name_clean.replace(' ', '_')}.png")
    generate_signature(company_name_clean, signature_file)
    signature_path = os.path.abspath(signature_file).replace('\\', '/')

    return {
        "uk_time_now":formatted_time,
        "company_name": company_name,
        "company_address": address,
        "postal_code": postal,
        "city": city,
        "email": email,
        "phone": phone,
        "ir_company_address": fake_ir.street_address(),
        "ir_postal_code": fake_ir.postcode(),
        "ir_city": fake_ir.city(),
        "invoice_number": invoice_number,
        "invoice_date": invoice_date.strftime('%B %d, %Y'),
        "alt_invoice_date": invoice_date.strftime('%d/%m/%Y'),
        "due_date": due_date.strftime('%B %d, %Y'),
        "alt_due_date": due_date.strftime('%d/%m/%Y'),
        "client_name": client_name,
        "client_address": client_address,
        "bank" : random.choice(UK_BANKS),
        "account_name" : account_name,
        "account_number":account_number,
        "items": items,
        "subtotal": f"{subtotal:,.2f}",
        "vat": f"{vat:,.2f}",
        "vat_no": random.choice(range(100000, 800000, 16)),
        "total": f"{total_amount:,.2f}",
        "total_words": total_words,
        "subtotal_words": subtotal_words,
        "signature_path": signature_path,
        "pattern_path": os.path.abspath(pattern_location).replace('\\', '/'),
        "social_media_company" : social_media_company,
        "social_adverts_description": social_adverts_description,
        "social_adverts_qty" : social_adverts_qty,
        "social_adverts_rate":social_adverts_rate,
        "social_adverts_total":social_adverts_total,
        "social_adverts_total_words": amount_to_words(social_adverts_total),
        "random_background": os.path.abspath(os.path.join(background_location, background_filename)).replace('\\', '/'),
        "uk_store_data": store_data,
        "uk_store_items": uk_store_items,
        "uk_store_site": "www."+store_data["name"].replace("'", "").replace(" ", "").replace("&", "")+".com",
        "Store_subtotal" : Store_subtotal,
        "Store_total":Store_subtotal+ fuel_total,
        "fuel_type":random.choice(["Petrol", "Diesel"]),
        "fuel_qty":fuel_qty,
        "fuel_rate":fuel_rate,
        "fuel_total":fuel_total
        
    }


# === PDFKit Config ===
config = pdfkit.configuration(wkhtmltopdf=r"E:\PROJECT\PYTHON\Invoice Generator\wkhtmltox\bin\wkhtmltopdf.exe")
options = {
    'enable-local-file-access': '',
    'page-size': 'A4',
    'orientation': 'Portrait',
    'margin-top': '0mm',
    'margin-right': '0mm',
    'margin-bottom': '0mm',
    'margin-left': '0mm',
    'background': '',  # Critical for backgrounds
    'no-outline': None,
    'disable-smart-shrinking': '',
    'dpi': 300,
    'quiet': '',  # Suppress warnings
}

# === Generate Invoices ===
for i in range(invoice_count):
    data = generate_invoice_data()
    html = Template(invoice_template).render(**data)
    filename = f"{OUTPUT_DIR}/{data['company_name'].replace(' ', '_')}.pdf"
    pdfkit.from_string(html, filename, configuration=config, options=options)
    print(f"[✓] Generated {filename}")

print(f"\nAll {invoice_count} invoices saved to '{OUTPUT_DIR}/'")
