"""
Script to parse Notion store database and create seed data
Note: This script uses the Notion API results that were already fetched
We'll save it to a JSON file for the seed script to use
"""
import json

# Store data extracted from Notion API
# This will be populated by running the Notion API query
stores_data = [
    # Data will be populated from Notion API results
]

def save_stores_to_json(notion_results):
    """Convert Notion API results to our store format and save to JSON"""
    stores = []
    
    for page in notion_results.get('results', []):
        props = page.get('properties', {})
        
        # Extract data from Notion properties
        name = ''
        if props.get('Name') and props['Name'].get('title'):
            name = props['Name']['title'][0].get('plain_text', '')
        
        street = ''
        if props.get('Street') and props['Street'].get('rich_text'):
            street = props['Street']['rich_text'][0].get('plain_text', '') if props['Street']['rich_text'] else ''
        
        city = ''
        if props.get('City') and props['City'].get('rich_text'):
            city = props['City']['rich_text'][0].get('plain_text', '') if props['City']['rich_text'] else ''
        
        province = ''
        if props.get('Province') and props['Province'].get('rich_text'):
            province = props['Province']['rich_text'][0].get('plain_text', '') if props['Province']['rich_text'] else ''
        
        postal_code = ''
        if props.get('Postal Code') and props['Postal Code'].get('rich_text'):
            postal_code = props['Postal Code']['rich_text'][0].get('plain_text', '') if props['Postal Code']['rich_text'] else ''
        
        latitude = None
        if props.get('Latitude') and props['Latitude'].get('number'):
            latitude = props['Latitude']['number']
        
        longitude = None
        if props.get('Longitude') and props['Longitude'].get('number'):
            longitude = props['Longitude']['number']
        
        if name:  # Only add if we have a name
            stores.append({
                'name': name,
                'street': street,
                'city': city,
                'province': province,
                'postal_code': postal_code,
                'latitude': latitude,
                'longitude': longitude,
                'is_active': True
            })
    
    return stores

# Example: This would be run after fetching from Notion API
# For now, I'll manually parse the data from the API response we got

if __name__ == '__main__':
    # This script would be called after fetching from Notion
    # For now, we'll create the JSON file directly with the parsed data
    pass

