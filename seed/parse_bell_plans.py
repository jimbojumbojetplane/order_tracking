"""
Script to parse Bell rate plan JSON and convert to our RatePlan format
"""
import json
import re
import os

def extract_price(price_str):
    """Extract numeric price from string like '$70 per month' or '$70'"""
    if not price_str:
        return None
    # Remove currency symbols and text, extract number
    match = re.search(r'(\d+\.?\d*)', price_str.replace(',', ''))
    if match:
        return float(match.group(1))
    return None

def extract_data_gb(data_str, speed_features=None):
    """Extract GB amount from string like '60 GB' or '200 GB'
    Also checks speed_features for data amounts if data_str seems incorrect
    """
    # First try data_str
    if data_str:
        match = re.search(r'(\d+)', data_str.replace(',', ''))
        if match:
            gb_value = int(match.group(1))
            # If dataAmount seems low but speed_features mentions higher amounts, check speed_features
            if gb_value < 50 and speed_features:
                for feature in speed_features:
                    # Look for patterns like "200 GB" in speed features
                    feature_match = re.search(r'(\d+)\s*GB', feature, re.IGNORECASE)
                    if feature_match:
                        feature_gb = int(feature_match.group(1))
                        if feature_gb > gb_value:
                            return feature_gb
            return gb_value
    
    # If no data_str, try speed_features
    if speed_features:
        for feature in speed_features:
            match = re.search(r'(\d+)\s*GB', feature, re.IGNORECASE)
            if match:
                return int(match.group(1))
    
    return None

def check_unlimited_canada(calling_features, roaming_features):
    """Check if plan has unlimited Canada"""
    all_features = ' '.join(calling_features + roaming_features).lower()
    return 'canada' in all_features or 'unlimited' in all_features

def check_unlimited_us(calling_features, roaming_features, roaming_obj):
    """Check if plan has unlimited US roaming"""
    all_features = ' '.join(calling_features + roaming_features).lower()
    if 'united states' in all_features or 'u.s' in all_features or 'us' in all_features:
        return True
    if roaming_obj and isinstance(roaming_obj, dict):
        if roaming_obj.get('classification') and 'US' in roaming_obj.get('classification', ''):
            return True
    return False

def build_roaming_notes(plan):
    """Build roaming notes from plan features"""
    notes_parts = []
    
    # Add calling features
    if plan.get('callingFeatures'):
        notes_parts.extend(plan['callingFeatures'])
    
    # Add roaming features
    if plan.get('roamingFeatures'):
        notes_parts.extend(plan['roamingFeatures'])
    
    # Add roaming details if available
    if plan.get('roaming') and isinstance(plan['roaming'], dict):
        if plan['roaming'].get('details'):
            notes_parts.append(plan['roaming']['details'])
    
    # Add speed features
    if plan.get('speedFeatures'):
        speed_text = '; '.join(plan['speedFeatures'])
        if speed_text:
            notes_parts.append(f"Speed: {speed_text}")
    
    # Add other features
    if plan.get('otherFeatures'):
        other_text = '; '.join(plan['otherFeatures'])
        if other_text:
            notes_parts.append(f"Features: {other_text}")
    
    return ' | '.join(notes_parts) if notes_parts else None

def parse_bell_json(json_path):
    """Parse Bell JSON and return list of RatePlan dicts"""
    with open(json_path, 'r') as f:
        data = json.load(f)
    
    plans_list = []
    
    # Focus on 1_line_mobile_only scenario for individual mobile orders
    scenarios_to_use = ['1_line_mobile_only', '2_line_mobile_only']
    
    for scenario_name in scenarios_to_use:
        if scenario_name not in data.get('scenarios', {}):
            continue
        
        scenario = data['scenarios'][scenario_name]
        plans = scenario.get('plans', [])
        
        for plan in plans:
            plan_name = plan.get('planName', 'Unknown')
            
            # Use currentPrice, fallback to regularPrice
            price_str = plan.get('currentPrice') or plan.get('regularPrice')
            monthly_price = extract_price(price_str)
            
            if not monthly_price:
                print(f"Warning: Could not extract price for {plan_name}, skipping")
                continue
            
            # Extract data amount
            data_str = plan.get('dataAmount', '')
            speed_features = plan.get('speedFeatures', [])
            data_gb = extract_data_gb(data_str, speed_features)
            
            # Check for unlimited flags
            calling_features = plan.get('callingFeatures', [])
            roaming_features = plan.get('roamingFeatures', [])
            roaming_obj = plan.get('roaming')
            
            unlimited_canada = check_unlimited_canada(calling_features, roaming_features)
            unlimited_us = check_unlimited_us(calling_features, roaming_features, roaming_obj)
            
            # Build roaming notes
            roaming_notes = build_roaming_notes(plan)
            
            # Generate plan code (simplified)
            plan_code = plan_name.upper().replace(' ', '')[:10]
            
            # Determine segment (consumer by default)
            segment = 'consumer'
            if 'business' in plan_name.lower() or 'biz' in plan_name.lower():
                segment = 'business'
            
            # Add scenario suffix to plan name for clarity if needed
            display_name = plan_name
            if scenario_name == '2_line_mobile_only':
                display_name = f"{plan_name} (2-line)"
            
            plan_dict = {
                'name': display_name,
                'monthly_price': monthly_price,
                'data_gb': data_gb,
                'unlimited_canada': unlimited_canada,
                'unlimited_us': unlimited_us,
                'roaming_notes': roaming_notes[:500] if roaming_notes else None,  # Limit length
                'bell_plan_code': plan_code,
                'segment': segment
            }
            
            plans_list.append(plan_dict)
    
    return plans_list

def main():
    """Main function to convert Bell JSON to our format"""
    # Path to Bell JSON file
    bell_json_path = '/Users/jgf/coding/rate_plan_pricing_extractor_v2/data/bell/output/bell_llm_output_all_plans_20251123_172521.json'
    
    if not os.path.exists(bell_json_path):
        print(f"Error: File not found: {bell_json_path}")
        return
    
    print(f"Parsing Bell rate plans from: {bell_json_path}")
    plans = parse_bell_json(bell_json_path)
    
    # Output to JSON file for seed script
    output_path = os.path.join(os.path.dirname(__file__), 'rate_plans.json')
    with open(output_path, 'w') as f:
        json.dump(plans, f, indent=2)
    
    print(f"\n✓ Successfully parsed {len(plans)} rate plans")
    print(f"✓ Output written to: {output_path}")
    print("\nPlans extracted:")
    for plan in plans:
        print(f"  - {plan['name']}: ${plan['monthly_price']}/mo ({plan['data_gb']} GB)")

if __name__ == '__main__':
    main()

