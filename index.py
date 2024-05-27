import os
import sys
import requests

def main():
    organization_id = os.getenv('INPUT_ORGANIZATION_ID')
    deployed_at = os.getenv('INPUT_DEPLOYED_AT')
    external_url = os.getenv('INPUT_EXTERNAL_URL', '')  # Optional
    status = os.getenv('INPUT_STATUS', 'pending')  # Default to 'pending'
    version = os.getenv('INPUT_VERSION', '')  # Optional
    name = os.getenv('INPUT_NAME', '')  # Optional
    cased_token = os.getenv('CASED_TOKEN')

    if not cased_token:
        print('CASED_TOKEN environment variable is not set.')
        sys.exit(1)

    data = {
        'organization_id': organization_id,
        'deployed_at': deployed_at,
        'external_url': external_url,
        'status': status,
        'version': version,
        'name': name
    }

    headers = {
        'Authorization': f'Bearer {cased_token}',
        'Content-Type': 'application/json'
    }

    response = requests.post(f'https://preview.cased.com/api/v1/organizations/{organization_id}/deployments/', json=data, headers=headers)

    if response.status_code == 200:
        print('Deployment notification sent successfully.')
    else:
        print(f'Failed to send deployment notification: {response.status_code} {response.text}')
        sys.exit(1)

if __name__ == '__main__':
    main()
