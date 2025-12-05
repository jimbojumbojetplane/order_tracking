"""
Script to parse Canadian handsets CSV and convert to our Phone model format
"""
import csv
import re
import json
import os

# Default colors by brand (can be customized)
BRAND_COLORS = {
    'Apple': ['Space Black', 'White', 'Natural Titanium', 'Blue Titanium', 'Desert Titanium', 'Titanium Gray'],
    'Samsung': ['Phantom Black', 'Marble Gray', 'Cobalt Violet', 'Amber Yellow', 'Onyx Black'],
    'Google': ['Obsidian', 'Porcelain', 'Hazel', 'Rose Quartz'],
    'OnePlus': ['Silky Black', 'Emerald Flow', 'Nebula Noir', 'Black Eclipse'],
    'Motorola': ['Deep Forest', 'Midnight Blue', 'Beach Sand', 'Forest Grey', 'Peach Fuzz'],
    'Sony': ['Black', 'White', 'Platinum Silver'],
    'Nothing': ['White', 'Black'],
}

# Base pricing multipliers by storage (approximate)
STORAGE_PRICING = {
    '128GB': 1.0,
    '256GB': 1.2,
    '512GB': 1.5,
    '1TB': 2.0,
}

# Base prices by brand/model tier (estimated Canadian prices in CAD)
BASE_PRICES = {
    'Apple': {
        'iPhone 16 Pro Max': 1599,
        'iPhone 16 Pro': 1399,
        'iPhone 16 Plus': 1199,
        'iPhone 16': 1049,
        'iPhone 15 Pro Max': 1499,
        'iPhone 15 Pro': 1299,
        'iPhone 15 Plus': 1099,
        'iPhone 15': 949,
        'iPhone 14': 849,
    },
    'Samsung': {
        'Galaxy S24 Ultra': 1599,
        'Galaxy S24+': 1299,
        'Galaxy S24': 1099,
        'Galaxy Z Fold6': 2249,
        'Galaxy Z Flip6': 1249,
        'Galaxy Z Fold5': 2199,
        'Galaxy Z Flip5': 1149,
        'Galaxy A54 5G': 549,
    },
    'Google': {
        'Pixel 9 Pro XL': 1299,
        'Pixel 9 Pro': 1099,
        'Pixel 9': 899,
        'Pixel 9 Pro Fold': 2199,
        'Pixel 8 Pro': 999,
        'Pixel 8': 799,
    },
    'OnePlus': {
        'OnePlus 13': 1149,
        'OnePlus 13R': 799,
        'OnePlus 12': 1049,
        'OnePlus Open': 2199,
    },
    'Motorola': {
        'Edge 2025': 899,
        'Edge 2024': 799,
        'Razr+ 2024': 1199,
        'Edge 50 Ultra': 999,
        'Razr 50 Ultra': 1099,
    },
}

def extract_storage_options(storage_str):
    """Extract storage options from string like '256GB,512GB,1TB'"""
    if not storage_str:
        return ['128 GB']  # Default
    
    # Remove quotes and split by comma
    storage_str = storage_str.strip().strip('"')
    options = [s.strip() for s in storage_str.split(',')]
    
    # Normalize format
    normalized = []
    for opt in options:
        # Ensure space before GB/TB
        opt = re.sub(r'(\d+)(GB|TB)', r'\1 \2', opt)
        normalized.append(opt)
    
    return normalized if normalized else ['128 GB']

def calculate_price(brand, model, storage):
    """Calculate price based on brand, model, and storage"""
    # Try to find exact match
    if brand in BASE_PRICES and model in BASE_PRICES[brand]:
        base_price = BASE_PRICES[brand][model]
    else:
        # Estimate based on brand
        if brand == 'Apple':
            base_price = 1299  # Default premium
        elif brand == 'Samsung':
            base_price = 1099  # Default premium
        elif brand == 'Google':
            base_price = 899   # Default mid-high
        elif brand == 'OnePlus':
            base_price = 799   # Default mid-range
        elif brand == 'Motorola':
            base_price = 699   # Default mid-range
        else:
            base_price = 599   # Default budget
    
    # Apply storage multiplier
    storage_key = storage.replace(' ', '')
    multiplier = STORAGE_PRICING.get(storage_key, 1.0)
    
    return round(base_price * multiplier, 2)

def generate_sku(brand, model, storage):
    """Generate Bell SKU from brand, model, and storage"""
    # Shorten brand names
    brand_abbrev = {
        'Apple': 'IPH',
        'Samsung': 'SGS',
        'Google': 'PIX',
        'OnePlus': 'OP',
        'Motorola': 'MT',
        'Sony': 'SON',
        'Nothing': 'NOT',
    }.get(brand, brand[:3].upper())
    
    # Get model number/year
    model_num = re.search(r'(\d+)', model)
    model_code = model_num.group(1) if model_num else model[:3].upper()
    
    # Get storage code
    storage_code = storage.replace(' ', '').replace('GB', '').replace('TB', 'T')
    
    # Get model variant
    variant = ''
    if 'Pro Max' in model or 'Ultra' in model or 'XL' in model:
        variant = 'PM'
    elif 'Pro' in model or 'Plus' in model:
        variant = 'P'
    elif 'Fold' in model:
        variant = 'F'
    elif 'Flip' in model or 'Razr' in model:
        variant = 'R'
    
    return f"{brand_abbrev}{model_code}{variant}{storage_code}".upper()

def get_default_color(brand):
    """Get default color for brand"""
    colors = BRAND_COLORS.get(brand, ['Black'])
    return colors[0]

def is_featured(brand, model):
    """Determine if phone should be featured"""
    featured_keywords = ['Pro Max', 'Ultra', 'Pro XL', 'Fold', '16 Pro', 'S24 Ultra']
    return any(keyword in model for keyword in featured_keywords)

def parse_handsets_csv(csv_path):
    """Parse handsets CSV and return list of Phone dicts"""
    phones = []
    
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        
        for row in reader:
            brand = row.get('Brand', '').strip()
            model = row.get('Model', '').strip()
            
            if not brand or not model:
                continue
            
            # Get storage options
            storage_options = extract_storage_options(row.get('Storage_Options', ''))
            
            # Create one entry per storage option
            for storage in storage_options:
                # Generate price
                price = calculate_price(brand, model, storage)
                
                # Generate SKU
                sku = generate_sku(brand, model, storage)
                
                # Get color (default for now, could be enhanced)
                color = get_default_color(brand)
                
                # Determine if featured
                featured = is_featured(brand, model)
                
                phone_dict = {
                    'brand': brand,
                    'model': model,
                    'storage': storage,
                    'colour': color,
                    'bell_sku': sku,
                    'full_price': price,
                    'is_featured': featured
                }
                
                phones.append(phone_dict)
    
    return phones

def main():
    """Main function to convert CSV to our format"""
    csv_path = '/Users/jgf/Downloads/canadian_handsets_database.csv'
    
    if not os.path.exists(csv_path):
        print(f"Error: File not found: {csv_path}")
        return
    
    print(f"Parsing handsets from: {csv_path}")
    phones = parse_handsets_csv(csv_path)
    
    # Sort by brand, then featured, then model
    phones.sort(key=lambda x: (x['brand'], not x['is_featured'], x['model']))
    
    # Output to JSON file for seed script
    output_path = os.path.join(os.path.dirname(__file__), 'handsets.json')
    with open(output_path, 'w') as f:
        json.dump(phones, f, indent=2)
    
    print(f"\n✓ Successfully parsed {len(phones)} handset configurations")
    print(f"✓ Output written to: {output_path}")
    
    # Count by brand
    brand_counts = {}
    for phone in phones:
        brand = phone['brand']
        brand_counts[brand] = brand_counts.get(brand, 0) + 1
    
    print("\nHandsets by brand:")
    for brand, count in sorted(brand_counts.items()):
        print(f"  - {brand}: {count} configurations")

if __name__ == '__main__':
    main()

