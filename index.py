import os
import sys
import requests

def main():
    organization_id = os.getenv('INPUT_ORGANIZATION_ID')
    external_url = os.getenv('INPUT_EXTERNAL_URL', None)  # Optional
    version = os.getenv('INPUT_VERSION', None)  # Optional
    name = os.getenv('INPUT_NAME', None)  # Optional
    cased_token = os.getenv('CASED_TOKEN')

    if not cased_token:
        print('CASED_TOKEN environment variable is not set.')
        sys.exit(1)

    data = {
        'organization_id': organization_id,
        'external_url': external_url,
        'version': version,
        'name': name,
        "repository_name": os.getenv('GITHUB_REPOSITORY'),
    }

    headers = {
        'Authorization': f'Bearer {cased_token}',
        'Content-Type': 'application/json'
    }

    response = requests.post(f'https://preview.cased.com/api/v1/organizations/{organization_id}/deployments/', json=data, headers=headers)

    if response.status_code == 201:
        print('Deployment notification sent successfully.')
    else:
        print(f'Failed to send deployment notification: {response.status_code} {response.text}')
        sys.exit(1)

if __name__ == '__main__':
    main()
