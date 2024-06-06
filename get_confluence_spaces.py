"""
This script retrieves all spaces from a Confluence Cloud instance and exports the data to a JSON file.
It uses the Confluence Cloud REST API to gather data about spaces, including their names, IDs, keys, and types.
The script handles pagination to ensure all spaces are retrieved.

Permissions required:
Permission to access the Confluence site ('Can use' global permission).
Only spaces that the user has permission to view will be returned.

To use this script:
1. Ensure you have the `requests` and `python-dotenv` libraries installed (`pip install requests python-dotenv`).
2. Create a `.env` file with your Confluence instance details.
3. Run the script.

Functions:
- get_all_spaces(): Retrieves all spaces in the Confluence instance, handling pagination.

Usage:
1. Update the script with your Confluence instance details.
2. Execute the script to retrieve and export space data to a JSON file.
"""

import requests
from requests.auth import HTTPBasicAuth
import json
from dotenv import load_dotenv
import os

# Load the .env file
load_dotenv()

# Replace the following variables with your Confluence instance details
confluence_base_url = os.getenv('CONFLUENCE_BASE_URL')
username = os.getenv('USERNAME')
api_token = os.getenv('USER_API_TOKEN')

print(api_token)

# Function to get all spaces with pagination
def get_all_spaces():
    url = f'{confluence_base_url}/rest/api/space'
    params = {'limit': 50} # Limit the number of spaces per page
    spaces = []
    while url:
        response = requests.get(url, params=params, auth=HTTPBasicAuth(username, api_token))
        response.raise_for_status()
        data = response.json()
        spaces.extend(data['results'])
        url = data['_links'].get('next')
    return spaces

def main():
    result = []

    spaces = get_all_spaces()
    for space in spaces:
        space_data = {
            "space_name": space['name'],
            "space_id": space['id'],
            "space_key": space['key'],
            "space_type": space['type']
        }

        result.append(space_data)

    output_data = {
        "total_spaces": len(result),
        "spaces": result
    }

    with open("File Examples/confluence_spaces.json", "w") as json_file:
        json.dump(output_data, json_file, indent=4)

if __name__ == "__main__":
    main()
