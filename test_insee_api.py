"""
Test script for INSEE Sirene API
This script tests fetching company data using SIREN and SIRET numbers
"""

import requests
import json
from datetime import datetime

# API Configuration
BASE_URL = "https://api.insee.fr/entreprises/sirene/V3.11"

# You need to get these credentials from https://portail-api.insee.fr/
# After creating an account and subscribing to the Sirene API
CONSUMER_KEY = "84de7c45-f97e-48c1-bbb0-aa33eef4bdf8"
CONSUMER_SECRET = "0apA3hPs6QiE8MamjpcS0Hy5LT-S0EvE5"

# Test data
TEST_SIREN = "497784454"
TEST_SIRET = "49778445400041"


def get_access_token(consumer_key, consumer_secret):
    """
    Get OAuth access token from INSEE API
    """
    # Try the new authentication endpoint
    auth_url = "https://auth.insee.net/auth/realms/apim-gravitee/protocol/openid-connect/token"
    
    print(f"   Attempting authentication with consumer key: {consumer_key[:8]}...")
    
    try:
        response = requests.post(
            auth_url,
            data={
                "grant_type": "client_credentials",
                "client_id": consumer_key,
                "client_secret": consumer_secret
            },
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        response.raise_for_status()
        token_data = response.json()
        print(f"   Token obtained successfully")
        return token_data.get("access_token")
    except requests.exceptions.RequestException as e:
        print(f"   Error getting access token: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"   Status Code: {e.response.status_code}")
            print(f"   Response: {e.response.text}")
        return None


def fetch_siren_data(siren, access_token):
    """
    Fetch company data by SIREN number (9 digits)
    """
    url = f"{BASE_URL}/siren/{siren}"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/json"
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching SIREN data: {e}")
        if hasattr(e.response, 'text'):
            print(f"Response: {e.response.text}")
        return None


def fetch_siret_data(siret, access_token):
    """
    Fetch establishment data by SIRET number (14 digits)
    """
    url = f"{BASE_URL}/siret/{siret}"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/json"
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching SIRET data: {e}")
        if hasattr(e.response, 'text'):
            print(f"Response: {e.response.text}")
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
    
    # Check if credentials are set
    if CONSUMER_KEY == "YOUR_CONSUMER_KEY_HERE" or CONSUMER_SECRET == "YOUR_CONSUMER_SECRET_HERE":
        print("\n⚠️  WARNING: API credentials not configured!")
        print("\nTo use this script, you need to:")
        print("1. Go to https://portail-api.insee.fr/")
        print("2. Create an account and log in")
        print("3. Subscribe to the 'Sirene' API")
        print("4. Get your Consumer Key and Consumer Secret")
        print("5. Update the credentials in this script")
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
    
    # Get access token
    print("\n1. Getting access token...")
    access_token = get_access_token(CONSUMER_KEY, CONSUMER_SECRET)
    
    if not access_token:
        print("Failed to get access token. Please check your credentials.")
        return
    
    print("✓ Access token obtained")
    
    results = []
    
    # Test SIREN query
    print(f"\n2. Fetching data for SIREN: {TEST_SIREN}")
    siren_data = fetch_siren_data(TEST_SIREN, access_token)
    if siren_data:
        print("✓ SIREN data retrieved")
        results.append({
            'type': 'SIREN',
            'value': TEST_SIREN,
            'data': siren_data
        })
    
    # Test SIRET query
    print(f"\n3. Fetching data for SIRET: {TEST_SIRET}")
    siret_data = fetch_siret_data(TEST_SIRET, access_token)
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
