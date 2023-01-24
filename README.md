

# <img src="https://docs.lido.fi/img/logo.svg" alt="Lido" width="46"/> My Project

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Myproject is a base template for all python project with preinstalled packages that are common for Lido's codebase.

## How to install

1. `poetry install` - to install dep

## Usage

```py
from steth_price_balancer import BaseClass
from steth_price_balancer import base_function

BaseClass().base_method()
base_function()
```

```bash
$ python -m myproject

Hello world!
```

## Release flow

To create new release:

1. Merge all changes to the `main` branch
1. Navigate to Repo => Actions
1. Run action "Prepare release" action against `main` branch
1. When action execution is finished, navigate to Repo => Pull requests
1. Find pull request named "chore(release): X.X.X" review and merge it with "Rebase and merge" (or "Squash and merge")
1. After merge release action will be triggered automatically
1. Navigate to Repo => Actions and see last actions logs for further details 


### Secrets
List of secrets that you should add to secrets
* TARGET_REPO - Repository with our infra (lidofinance/infra-mainnet). This var need to run workflows from target repository.
* APP_ID and APP_PRIVATE_KEY - are ID and key to application that calls workflows in another application.