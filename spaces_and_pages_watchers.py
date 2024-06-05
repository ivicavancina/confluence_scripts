"""
 This script retrieves and exports Confluence Cloud space watchers and page watchers to a JSON file.
 It uses the Confluence Cloud REST API and GraphQL API to gather data about spaces, their watchers, and page watchers.
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

# Function to get space watchers
def get_space_watchers(space_key):
    url = f'https://euema.atlassian.net/cgraphql?q=SpaceWatchersQuery'
    payload = {
        "operationName": "SpaceWatchersQuery",
        "variables": {
            "first": 20,
            "spaceKey": space_key
        },
        "query": """query SpaceWatchersQuery($spaceKey: String, $spaceId: ID, $offset: Int, $after: String, $first: Int = 20) {
            spaceWatchers(
                spaceKey: $spaceKey
                spaceId: $spaceId
                offset: $offset
                after: $after
                first: $first
            ) {
                count
                nodes {
                    ...userNodeFragment
                    __typename
                }
                pageInfo {
                    hasNextPage
                    endCursor
                    __typename
                }
                __typename
            }
        }
        fragment userNodeFragment on Person {
            ... on KnownUser {
                accountId
                __typename
            }
            ... on UnknownUser {
                accountId
                __typename
            }
            ... on User {
                accountId
                __typename
            }
            displayName
            permissionType
            profilePicture {
                path
                __typename
            }
            __typename
        }"""
    }

    headers = {
        "Content-Type": "application/json"
    }

    response = requests.post(url, auth=HTTPBasicAuth(username, api_token), headers=headers, data=json.dumps(payload))

    if response.status_code == 404:
        print(f"Error: Space watchers for space '{space_key}' not found (404)")
        return {}
    response.raise_for_status()
    return response.json()

# Function to get page watchers
def get_page_watchers(page_id):
    url = f'https://euema.atlassian.net/cgraphql?q=ContentWatchersQuery'
    payload = {
        "operationName": "ContentWatchersQuery",
        "variables": {
            "first": 20,
            "contentId": page_id
        },
        "query": """query ContentWatchersQuery($contentId: ID!, $offset: Int, $after: String, $first: Int = 20) {
            contentWatchers(
                contentId: $contentId
                offset: $offset
                after: $after
                first: $first
            ) {
                count
                nodes {
                    ...userNodeFragment
                    __typename
                }
                pageInfo {
                    hasNextPage
                    endCursor
                    __typename
                }
                __typename
            }
        }
        fragment userNodeFragment on Person {
            ... on KnownUser {
                accountId
                __typename
            }
            ... on UnknownUser {
                accountId
                __typename
            }
            ... on User {
                accountId
                __typename
            }
            displayName
            permissionType
            profilePicture {
                path
                __typename
            }
            __typename
        }"""
    }

    headers = {
        "Content-Type": "application/json"
    }

    response = requests.post(url, auth=HTTPBasicAuth(username, api_token), headers=headers, data=json.dumps(payload))

    if response.status_code == 404:
        print(f"Error: Watchers for page '{page_id}' not found (404)")
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

        space_watchers = get_space_watchers(space['key'])
        space_data["space_watchers"] = space_watchers

        space_pages = []
        pages_response = requests.get(f"{confluence_base_url}/rest/api/space/{space['key']}/content/page", auth=HTTPBasicAuth(username, api_token))
        pages_response.raise_for_status()
        pages = pages_response.json()['results']

        for page in pages:
            page_data = {
                "page_name": page['title'],
                "page_id": page['id']
            }

            page_watchers = get_page_watchers(page['id'])
            page_data["page_watchers"] = page_watchers
            space_pages.append(page_data)

        space_data["space_pages"] = space_pages
        result.append(space_data)

    with open("File Examples/confluence_space_and_page_watchers_data.json", "w") as json_file:
        json.dump(result, json_file, indent=4)

if __name__ == "__main__":
    main()