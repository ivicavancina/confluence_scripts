"""
This script retrieves information about managed accounts in Confluence Cloud.
It counts the number of active users, the number of Confluence users per domain,
and the number of users active in the last month, last 2 months, and last 3 months.
It then saves this information to a JSON file named 'confluence_managed_accounts.json'.
"""

import json
import requests
from datetime import datetime, timedelta
from collections import defaultdict

# Replace these variables with your Confluence Cloud credentials and base URL
confluence_base_url = 'https://euema.atlassian.net'
username = 'ivica.vancina@valiantys.com'
api_token = 'ATCTT3xFfGN0G0ryKFlMoncbllwNH4LJ1k3c7O7HyaEZSZNVVXy25gnYLVqQ76zgS9VRGdYieNaD5ndnLSUkXXJQ5SJnyLINbIMNoiIsp5WrQzz1sEPnX2VBxvIXzlqLz6GplXVdxaq0QiSaxjtMf8CWU3b9sb5n5rNpNEFyx4J0G20JBmBpqrA=5C712000'

# Function to get managed accounts
def get_managed_accounts():
    url = f'https://api.atlassian.com/admin/v1/orgs/96k7d9d5-7d30-126a-7718-2bb4404j2a84/users'
    headers = {
        'Authorization': f'Bearer {api_token}',
        'Accept': 'application/json'
    }
    managed_accounts = []
    try:
        while url:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            data = response.json()
            managed_accounts.extend(data.get('data', []))
            url = data.get('links', {}).get('next', None)
        return managed_accounts
    except Exception as e:
        print(f"Error retrieving managed accounts: {e}")
        return []

# Function to filter active users and count them by domain
def filter_active_users(accounts):
    active_users = defaultdict(list)
    confluence_domain_counts = defaultdict(int)

    for account in accounts:
        if account['account_status'] == 'active':
            if 'product_access' in account:
                for access in account['product_access']:
                    if access.get('name') == 'Confluence':
                        domain = account['email'].split('@')[-1]
                        confluence_domain_counts[domain] += 1
                        break

    return confluence_domain_counts

# Function to get domain counts for a specific time period
def get_domain_counts(accounts, time_period):
    domain_counts = defaultdict(int)
    user_list = []

    for account in accounts:
        if account.get('last_active') and datetime.strptime(account['last_active'].split('T')[0], '%Y-%m-%d') >= time_period:
            domain = account['email'].split('@')[-1]
            domain_counts[domain] += 1
            user_list.append({'name': account.get('name'), 'email': account['email']})

    return domain_counts, user_list

def main():
    try:
        managed_accounts = get_managed_accounts()
        active_accounts = [account for account in managed_accounts if account['account_status'] == 'active']
        confluence_domain_counts = filter_active_users(managed_accounts)

        # Count the number of active users
        num_active_users = len(active_accounts)

        # Count the number of Confluence users for each domain
        confluence_users_count = sum(confluence_domain_counts.values())

        # Time periods
        three_months_ago = datetime.now() - timedelta(days=90)
        two_months_ago = datetime.now() - timedelta(days=60)
        one_month_ago = datetime.now() - timedelta(days=30)

        # Get domain counts and user lists for the specified time periods
        active_in_last_3_months, users_in_last_3_months = get_domain_counts(active_accounts, three_months_ago)
        active_in_last_2_months, users_in_last_2_months = get_domain_counts(active_accounts, two_months_ago)
        active_in_last_month, users_in_last_month = get_domain_counts(active_accounts, one_month_ago)

        # Save results to JSON file
        with open("File Examples/confluence_managed_accounts.json", "w") as json_file:
            json.dump({
                "active_users": num_active_users,
                "confluence_users_count": confluence_users_count,
                "active_in_last_3_months": len(users_in_last_3_months),
                "active_in_last_2_months": len(users_in_last_2_months),
                "active_in_last_month": len(users_in_last_month),
                "confluence_domain_counts": confluence_domain_counts,
                "active_in_last_3_months_domain_counts": active_in_last_3_months,
                "active_in_last_2_months_domain_counts": active_in_last_2_months,
                "active_in_last_month_domain_counts": active_in_last_month,
                "users_in_last_3_months": users_in_last_3_months,
                "users_in_last_2_months": users_in_last_2_months,
                "users_in_last_month": users_in_last_month,
                "accounts": active_accounts
            }, json_file, indent=4)

        print("Managed accounts data saved to 'confluence_managed_accounts.json'")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
