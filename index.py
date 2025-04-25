import os
import sys
import requests
import json

def get_pr_number():
    # First try direct PR number env var
    pr_number = os.getenv('GITHUB_EVENT_PULL_REQUEST_NUMBER')
    if pr_number:
        return pr_number
        
    # If not found, try to extract from the event payload
    event_path = os.getenv('GITHUB_EVENT_PATH')
    if event_path and os.path.exists(event_path):
        try:
            with open(event_path, 'r') as f:
                event_data = json.load(f)
                # For merge events, PR number is in pull_request.number
                if 'pull_request' in event_data:
                    return str(event_data['pull_request']['number'])
                # For merged PR events, it might be in merge_group.head_ref
                elif 'merge_group' in event_data:
                    head_ref = event_data['merge_group']['head_ref']
                    if head_ref and head_ref.startswith('pull/'):
                        return head_ref.split('/')[1]
        except Exception as e:
            print(f"Error reading event file: {e}")
    
    return None

def main():
    cased_token = os.getenv('INPUT_CASED_TOKEN')
    if not cased_token:
        print('CASED_TOKEN input is not set.')
        sys.exit(1)

    branch_name = os.getenv('INPUT_BRANCH_NAME', 'main')
    target = os.getenv('INPUT_TARGET', 'prod')
    trigger = os.getenv('INPUT_TRIGGER', 'pr_merge')
    pr_number = get_pr_number()

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
    else:
        print('Warning: Could not determine PR number')

    workflow_inputs = os.getenv('INPUT_WORKFLOW_INPUTS')
    if workflow_inputs:
        try:
            workflow_inputs_dict = json.loads(workflow_inputs)
            data['workflow_inputs'] = workflow_inputs_dict
        except Exception as e:
            print(f'Invalid JSON for workflow_inputs: {e}')
            sys.exit(1)

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

