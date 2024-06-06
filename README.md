# Confluence Scripts

This repository contains scripts to retrieve various types of information from Confluence Cloud. The scripts included are:

1. `confluence_managed_accounts.py`: Counts the number of active users, the number of Confluence users per domain, and the number of users active in the last month, last 2 months, and last 3 months. It also identifies inactive users and top active users. Uses the [Orgs API](https://developer.atlassian.com/cloud/admin/organization/rest/api-group-users/#api-v1-orgs-orgid-users-get).
2. `confluence_permissions_and_restrictions.py`: Retrieves permissions and restrictions for spaces and pages. Uses the [Content Restrictions API](https://developer.atlassian.com/cloud/confluence/rest/v1/api-group-content-restrictions/#api-wiki-rest-api-content-id-restriction-get) and the [Space Permissions API](https://developer.atlassian.com/cloud/confluence/rest/v2/api-group-space-permissions/#api-spaces-id-permissions-get).
3. `confluence_space_and_page_watchers.py`: Retrieves watchers for spaces and pages. This script uses Chrome tools/Inspect/Network to get the URL and GraphQL query to get results.
4. `remove_page_restrictions.py`: Removes all page restrictions within a specific space. Uses the [Content Restrictions API](https://developer.atlassian.com/cloud/confluence/rest/v1/api-group-content-restrictions/#api-wiki-rest-api-content-id-restriction-delete).
5. `get_confluence_spaces.py`: Retrieves all spaces from Confluence. Uses the [Spaces API](https://developer.atlassian.com/cloud/confluence/rest/v2/api-group-space/#api-spaces-get).

The results from these scripts are saved to JSON files.

## Prerequisites

Before running the scripts, ensure you have the following installed:

- Python 3.x
- `requests` library
- `python-dotenv` library

### Installing Python

- **Windows**: Download and install Python from [python.org](https://www.python.org/downloads/windows/). Make sure to check the box that says "Add Python to PATH" during installation.
- **macOS**: Python 3 comes pre-installed on macOS. You can verify it by running `python3 --version` in Terminal.
- **Linux**: Python 3 is usually pre-installed on most distributions. You can verify it by running `python3 --version` in Terminal.

### Installing Required Libraries

You can install the required libraries using pip. Open your command line interface (Command Prompt on Windows, Terminal on macOS and Linux) and run:

```sh
pip install requests python-dotenv
```
The `json` library is included with Python, so no additional installation is required.

## Setup

Clone the repository or download the scripts to your local machine.

Create a .env file in the same directory as your scripts. In this file, store your Confluence Cloud credentials
```python
API_TOKEN="your-org-api-token"
CONFLUENCE_BASE_URL="https://your-confluence-instance.atlassian.net"
USERNAME="your-email@example.com"
USER_API_TOKEN="your-api-token"
```
## Running the Scripts

### On Windows

1. Open Command Prompt.
2. Navigate to the directory containing the script:

    ```sh
    cd path\to\your\script
    ```

3. Run the script:

    ```sh
    python script_name.py
    ```

You can also install the required libraries using the provided setup scripts.

#### On Windows

Open Command Prompt and navigate to the directory containing the `setup.bat` file:

```sh
cd path\to\your\script
```
Then run the setup.bat file:
```sh
setup.bat
```

### On macOS and Linux

1. Open Terminal.
2. Navigate to the directory containing the script:

    ```sh
    cd path/to/your/script
    ```

3. Run the script:

    ```sh
    python3 script_name.py
    ```

You can also install the required libraries using the provided setup scripts.

#### On macOS and Linux
Open Terminal and navigate to the directory containing the setup.sh file:

```sh
cd path/to/your/script
```
Then run the setup.sh file:

```sh
./setup.sh
```
Replace `script_name.py` with the name of the script you want to run.

## Script Descriptions

### `confluence_managed_accounts.py`

This script retrieves managed accounts and provides the following information:

- Number of active users.
- Number of Confluence users per domain.
- Number of users active in the last month, last 2 months, and last 3 months.
- Domain counts for users active in the last month, last 2 months, and last 3 months.
- Lists of user objects with username and email for active users in the last month, last 2 months, and last 3 months.
- Inactive users (inactive for more than 6 months).
- Top active users in the last 3 months.

### `confluence_permissions_and_restrictions.py`

This script retrieves permissions and restrictions for spaces and pages. It provides the following information:

- Permissions for each space.
- Restrictions for each page within the spaces.

### `confluence_space_and_page_watchers.py`

This script retrieves watchers for spaces and pages. It provides the following information:

- Watchers for each space.
- Watchers for each page within the spaces.

### `remove_page_restrictions.py`

This script removes all page restrictions within a specific space. It provides the following functionality:

- Retrieves all pages within the specified space.
- Iterates through each page and removes any restrictions.

### `get_confluence_spaces.py`

- This script retrieves all spaces from Confluence. It provides the following information:
- List of all spaces.

### Additional Resources
- Confluence REST API Documentation: [Using the REST API](https://developer.atlassian.com/cloud/confluence/rest/v2/intro/#about)
- Creating API Tokens: [Atlassian API Tokens](https://id.atlassian.com/manage-profile/security/api-tokens)