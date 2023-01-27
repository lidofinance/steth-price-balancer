# <img src="https://docs.lido.fi/img/logo.svg" alt="Lido" width="46"/> STETH Price Balancer

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

This bot check the stEth price in Oracle and in pool and checks difference if it is higher than threshold submit new price to contract.

## Startup

```bash
git clone https://github.com/lidofinance/steth-price-balancer
cd steth-price-balancer
poetry install
```

Startup

```bash
cd steth_price_balancer
export WALLET_PRIVATE_KEY={pk}
export WEB3_PROVIDER_URI=https://mainnet.infura.io/v3/{infura_key}
python main.py
```

## Variables

| Env variables                         | Default - Raw                                | Description                                                                                                                                     |
|---------------------------------------|:---------------------------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------|
| WEB3_RPC_ENDPOINTS (required)         | `None`                                       | List of rpc endpoints that will be used to send requests separated by comma (`,`). If not provided will be used infura (WEB3_INFURA_PROJECT_ID) |
| WALLET_PRIVATE_KEY                    | `None`                                       | Private key to ETH wallet                                                                                                                       |
| GAS_LIMIT                             | `300000`                                     | Gas limit for transaction                                                                                                                       |
| STETH_PRICE_ORACLE_BLOCK_NUMBER_SHIFT | `15`                                         | The price will be checked for this number of blocks in the past                                                                                 |
| STETH_CURVE_POOL_CONTRACT             | `0xDC24316b9AE028F1497c275EB9192a3Ea0f67022` | Address to pool contract (default for mainnet)                                                                                                  |
| STETH_PRICE_ORACLE_CONTRACT           | `0x3A6Bd15abf19581e411621D669B6a2bbe741ffD6` | Address to oracle state contract (default for mainnet)                                                                                          |
| PROMETHEUS_PORT                       | `9000`                                       | Port for prometheus server                                                                                                                      |
| PROMETHEUS_PREFIX                     | `steth_price_balancer`                       | Prefix for                                                                                                                                      |
| HEALTHCHECK_SERVER_PORT               | `9010`                                       | Port for heath-check server used by docker                                                                                                      |
| MAX_CYCLE_LIFETIME_IN_SECONDS         | `60`                                         | Timeout for main cycle                                                                                                                          |
