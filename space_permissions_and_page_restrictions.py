"""
 This script retrieves and exports Confluence Cloud space permissions and page restrictions to a JSON file.
 It uses the Confluence Cloud REST API to gather data about spaces, their permissions, and page restrictions.
"""

import requests
from requests.auth import HTTPBasicAuth
import json

# Replace these variables with your Confluence Cloud credentials and base URL
confluence_base_url = 'https://euema.atlassian.net/wiki'
username = 'your@email.com'
api_token = 'API-TOKEN'

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
    url = f'{confluence_base_url}/rest/api/content/{page_id}/restriction/byOperation'
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
