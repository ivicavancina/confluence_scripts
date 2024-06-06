"""
This script retrieves and exports Confluence Cloud space permissions and page restrictions to a JSON file.
It uses the Confluence Cloud REST API to gather data about spaces, their permissions, and page restrictions.

The script performs the following tasks:
1. Retrieves all spaces within the Confluence instance.
2. For each space, if it's not a personal space and not named "Cloud Acceleration Service", it fetches space permissions.
3. Retrieves all pages within the space and their respective page restrictions.
4. Exports the gathered data to a JSON file.

To use this script:
1. Ensure you have the `requests` library installed (`pip install requests`).
2. Run the script.

Dependencies:
- requests: To handle HTTP requests.
- json: To handle JSON data.

Functions:
- get_all_spaces(): Retrieves all spaces in the Confluence instance.
- get_space_permissions(space_id): Retrieves permissions for a specific space.
- get_page_restrictions(page_id): Retrieves page restrictions for a specific page.

Usage:
1. Update the script with your Confluence instance details.
2. Execute the script to retrieve and export space permissions and page restrictions to a JSON file.
"""

import requests
from requests.auth import HTTPBasicAuth
import json
from dotenv import load_dotenv
import os

# Load the .env file
load_dotenv()

confluence_base_url = os.getenv('CONFLUENCE_BASE_URL')
username = os.getenv('USERNAME')
api_token = os.getenv('USER_API_TOKEN')

# Function to get all spaces
def get_all_spaces():
    url = f'{confluence_base_url}/rest/api/space'
    response = requests.get(url, auth=HTTPBasicAuth(username, api_token))
    response.raise_for_status()
    return response.json()['results']

# Function to get space permissions
def get_space_permissions(space_id):
    url = f'{confluence_base_url}/api/v2/spaces/{space_id}/permission'
    response = requests.get(url, auth=HTTPBasicAuth(username, api_token))
    if response.status_code == 404:
        print(f"Error: Permissions endpoint for space '{space_id}' not found (404)")
        return {}
    response.raise_for_status()
    return response.json()

# Function to get page restrictions
def get_page_restrictions(page_id):
    url = f'{confluence_base_url}/rest/api/content/{page_id}/restriction/'
    response = requests.get(url, auth=HTTPBasicAuth(username, api_token))
    if response.status_code == 404:
        print(f"Error: Restrictions endpoint for page '{page_id}' not found (404)")
        return {}
    response.raise_for_status()
    return response.json()

def main():
    result = []

    spaces = get_all_spaces()
    for space in spaces:
        space_data = {
            "space_name": space['name'],
            "space_id": space['id'],
            "space_type": space['type']
        }

        if space['type'] != 'personal' and space['name'] != "Cloud Acceleration Service":
            permissions = get_space_permissions(space['key'])
            space_data["space_permissions"] = permissions

            url = f"{confluence_base_url}/rest/api/space/{space['key']}/content/page"
            pages_response = requests.get(url, auth=HTTPBasicAuth(username, api_token))
            if pages_response.status_code == 404:
                print(f"Error: Pages endpoint for space '{space['key']}' not found (404)")
                continue
            pages_response.raise_for_status()
            pages = pages_response.json()['results']

            space_pages = []
            for page in pages:
                page_data = {
                    "page_name": page['title'],
                    "page_id": page['id']
                }

                restrictions = get_page_restrictions(page['id'])
                page_data["page_restrictions"] = restrictions
                space_pages.append(page_data)

            space_data["space_pages"] = space_pages
        result.append(space_data)

    with open("File Examples/confluence_permissions_and_restrictions_data.json", "w") as json_file:
        json.dump(result, json_file, indent=4)

if __name__ == "__main__":
    main()
