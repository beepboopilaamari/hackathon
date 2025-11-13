"""
Test script for INSEE Sirene API
This script tests fetching company data using SIREN and SIRET numbers
"""

import requests
import json
from datetime import datetime

# API Configuration
BASE_URL = "https://api.insee.fr/api-sirene/3.11"  # Updated endpoint

# You need to get these credentials from https://portail-api.insee.fr/
# After creating an account and subscribing to the Sirene API
# The API uses a custom header X-INSEE-Api-Key-Integration
API_KEY = "f339d307-3eac-42e5-b9d3-073eac62e5fb"  # This is your subscription key from the portal

# Test data
TEST_SIREN = "497784454"
TEST_SIRET = "49778445400041"


def fetch_siren_data(siren, api_key):
    """
    Fetch company data by SIREN number (9 digits)
    """
    url = f"{BASE_URL}/siren/{siren}"
    headers = {
        "X-INSEE-Api-Key-Integration": api_key,
        "Accept": "application/json"
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"   Error fetching SIREN data: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"   Status Code: {e.response.status_code}")
            print(f"   Response: {e.response.text}")
        return None


def fetch_siret_data(siret, api_key):
    """
    Fetch establishment data by SIRET number (14 digits)
    """
    url = f"{BASE_URL}/siret/{siret}"
    headers = {
        "X-INSEE-Api-Key-Integration": api_key,
        "Accept": "application/json"
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"   Error fetching SIRET data: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"   Status Code: {e.response.status_code}")
            print(f"   Response: {e.response.text}")
        return None


def save_results_to_file(results, filename="insee_api_results.txt"):
    """
    Save API results to a text file for analysis
    """
    with open(filename, 'w', encoding='utf-8') as f:
        f.write("=" * 80 + "\n")
        f.write("INSEE SIRENE API TEST RESULTS\n")
        f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("=" * 80 + "\n\n")
        
        for result in results:
            f.write(f"\n{'=' * 80}\n")
            f.write(f"Query Type: {result['type']}\n")
            f.write(f"Query Value: {result['value']}\n")
            f.write(f"{'=' * 80}\n\n")
            
            if result['data']:
                f.write(json.dumps(result['data'], indent=2, ensure_ascii=False))
            else:
                f.write("ERROR: No data returned\n")
            
            f.write("\n\n")
    
    print(f"\nResults saved to: {filename}")


def main():
    """
    Main function to test the INSEE API
    """
    print("=" * 80)
    print("Testing INSEE Sirene API")
    print("=" * 80)
    
    # Check if API key is set
    if API_KEY == "YOUR_API_KEY_HERE":
        print("\n⚠️  WARNING: API key not configured!")
        print("\nTo use this script, you need to:")
        print("1. Go to https://portail-api.insee.fr/")
        print("2. Create an account and log in")
        print("3. Create an application")
        print("4. Subscribe to the 'Sirene' API")
        print("5. Copy your API subscription key")
        print("6. Update the API_KEY in this script")
        print("\nThe API endpoints this script will use:")
        print(f"  - SIREN endpoint: {BASE_URL}/siren/{TEST_SIREN}")
        print(f"  - SIRET endpoint: {BASE_URL}/siret/{TEST_SIRET}")
        print("\nWhat this API returns:")
        print("  - Company legal information (name, legal form, address)")
        print("  - Establishment details")
        print("  - Activity codes (NAF/APE)")
        print("  - Registration status and dates")
        print("  - And more company registry data")
        return
    
    print(f"\n1. Using API key: {API_KEY[:8]}...")
    
    results = []
    
    # Test SIREN query
    print(f"\n2. Fetching data for SIREN: {TEST_SIREN}")
    siren_data = fetch_siren_data(TEST_SIREN, API_KEY)
    if siren_data:
        print("✓ SIREN data retrieved")
        results.append({
            'type': 'SIREN',
            'value': TEST_SIREN,
            'data': siren_data
        })
    
    # Test SIRET query
    print(f"\n3. Fetching data for SIRET: {TEST_SIRET}")
    siret_data = fetch_siret_data(TEST_SIRET, API_KEY)
    if siret_data:
        print("✓ SIRET data retrieved")
        results.append({
            'type': 'SIRET',
            'value': TEST_SIRET,
            'data': siret_data
        })
    
    # Save results
    if results:
        print("\n4. Saving results to file...")
        save_results_to_file(results)
        print("\n✓ Test complete!")
    else:
        print("\n✗ No data retrieved. Check your credentials and API subscription.")


if __name__ == "__main__":
    main()
