import os
import sys
import requests

def main():
    cased_token = os.getenv('INPUT_CASED_TOKEN')
    if not cased_token:
        print('CASED_TOKEN input is not set.')
        sys.exit(1)

    branch_name = os.getenv('INPUT_BRANCH_NAME', 'main')
    target = os.getenv('INPUT_TARGET', 'prod')
    pr_number = os.getenv('GITHUB_EVENT_PULL_REQUEST_NUMBER')
    trigger = os.getenv('INPUT_TRIGGER', 'pr_merge')

    project_name = os.getenv('GITHUB_REPOSITORY')
    if not project_name:
        print('Unable to determine project name from GITHUB_REPOSITORY.')
        sys.exit(1)

    data = {
        'branch_name': branch_name,
        'target_name': target,
        'trigger': trigger,
        'project_name': project_name
    }

    if pr_number:
        data['pr_number'] = pr_number

    headers = {
        'Authorization': f'Bearer {cased_token}',
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    response = requests.post('https://app.cased.com/api/v1/branch-deploys', json=data, headers=headers)

    if response.status_code == 201:
        print('Branch deploy notification sent successfully.')
    else:
        print(f'Failed to send branch deploy notification: {response.status_code} {response.text}')
        sys.exit(1)

if __name__ == '__main__':
    main()
