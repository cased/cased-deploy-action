# Cased Deploy Action

This GitHub Action sends a notification to Cased about a deployment.

## Inputs

- `organization_id`: **Required** The Cased organization ID.
- `external_url`: The external URL of the deployment.
- `version`: The version of the deployment.
- `name`: The name of the deployment.
- `branch`: The branch of a deployment. Defaults to `GITHUB_REF_NAME` (the branch the triggered the workflow run).

The action will automatically send the commit SHA of the last commit, as well as the repository name.

## Environment Variables

- `CASED_TOKEN`: **Required** The token used for authentication with the Cased web service.

## Example Usage

```yaml
name: Notify Deployment

on:
  push:
    branches:
      - main

jobs:
  notify:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v2
      
      - name: Notify deployment
        uses: cased/cased-deploy-action@v1
        env:
          CASED_TOKEN: ${{ secrets.CASED_TOKEN }}
        with:
          organization_id: ${{ secrets.ORGANIZATION_ID }}
          external_url: 'https://github.com/your-org/your-repo'
          version: ${{ github.sha }}
          name: 'Example Deployment'
