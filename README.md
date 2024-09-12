# Cased Branch Deploy Action

This GitHub Action requests a branch deploy from [Cased](https://cased.com).

## Inputs

- `cased_token`: **Required** The token used for authentication with the Cased API.
- `branch_name`: The name of the branch to deploy. Defaults to 'main'.
- `target`: The target environment for the deployment. Defaults to 'prod'.
- `trigger`: The trigger for the deployment. Defaults to 'pr_merge'.

The action will automatically send the pull request number if available.

## Environment Variables

No additional environment variables are required. All necessary information is passed through inputs.

## Example Usage

```yaml
name: Notify Cased on Deploy
on:
  pull_request:
    types: [closed]

jobs:
  notify-cased:
    if: github.event.pull_request.merged == true
    runs-on: ubuntu-latest
    steps:
      - name: Send notification to Cased
        uses: cased/cased-branch-deploy-action@v1
        with:
          branch_name: ${{ github.event.pull_request.base.ref }}
          target: 'feat/我的新分支'
          cased_token: ${{ secrets.CASED_TOKEN }}
