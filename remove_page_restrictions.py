"""
This script is designed to interact with Confluence Cloud's REST API to remove all page restrictions within a specific space.
The EMA team can use this script to clean up restrictions in a phased approach.

The script performs the following tasks:
1. Retrieves all pages within the specified Confluence space.
2. Iterates through each page and removes any restrictions.

To use this script:
1. Replace the placeholder values for `confluence_base_url`, `username`, `api_token`, and `space_key` with your Confluence Cloud instance details and the target space key.
2. Ensure you have the `requests` library installed (`pip install requests`).
3. Run the script.

Dependencies:
- requests: To handle HTTP requests.

Functions:
- get_all_pages_in_space(space_key): Retrieves all pages in the specified Confluence space.
- remove_restrictions(page_id): Removes all restrictions from the specified page.

The script uses basic authentication with the Confluence Cloud API.

Usage:
1. Update the script with your Confluence instance details.
2. Execute the script to remove all restrictions from pages in the specified space.
"""

import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv
import os

# Load the .env file
load_dotenv()

confluence_base_url = os.getenv('CONFLUENCE_BASE_URL')
username = os.getenv('USERNAME')
api_token = os.getenv('USER_API_TOKEN')
space_key = 'SPACE_KEY'

# Function to get all pages in the space
def get_all_pages_in_space(space_key):
    url = f"{confluence_base_url}/rest/api/content"
    params = {
        'spaceKey': space_key,
        'type': 'page',
        'limit': 200
    }
    response = requests.get(url, params=params, auth=HTTPBasicAuth(username, api_token))
    response.raise_for_status()
    return response.json()['results']

# Function to remove restrictions from a page
def remove_restrictions(page_id):
    url = f"{confluence_base_url}/rest/api/content/{page_id}/restriction/"
    response = requests.delete(url, auth=HTTPBasicAuth(username, api_token))
    response.raise_for_status()
    print(f"Removed restrictions for page ID: {page_id}")

def main():
    try:
        pages = get_all_pages_in_space(space_key)
        for page in pages:
            remove_restrictions(page['id'])
        print("All page restrictions removed successfully.")
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
