import logging
import os

from eth_account import Account

logger = logging.getLogger(__name__)


WEB3_RPC_ENDPOINTS = os.getenv("WEB3_PROVIDER_URI", "").split(",")

WALLET_PRIVATE_KEY = os.getenv("WALLET_PRIVATE_KEY", None)
if WALLET_PRIVATE_KEY:
    ACCOUNT = Account.from_key(WALLET_PRIVATE_KEY)
    logger.info({"msg": "Load account from private key.", "value": ACCOUNT.address})
else:
    ACCOUNT = None
    logger.warning({"msg": "Account not provided. Run in dry mode."})

GAS_LIMIT = int(os.getenv("GAS_LIMIT", 300_000))

# - App specific -
STETH_PRICE_ORACLE_BLOCK_NUMBER_SHIFT = int(
    os.getenv("STETH_PRICE_ORACLE_BLOCK_NUMBER_SHIFT", 15)
)
STETH_CURVE_POOL_CONTRACT = os.environ.get(
    "STETH_CURVE_POOL_CONTRACT", "0xDC24316b9AE028F1497c275EB9192a3Ea0f67022"
)
STETH_PRICE_ORACLE_CONTRACT = os.environ.get(
    "STETH_PRICE_ORACLE_CONTRACT", "0x3A6Bd15abf19581e411621D669B6a2bbe741ffD6"
)

# - Metrics -
PROMETHEUS_PORT = int(os.getenv("PROMETHEUS_PORT", "9000"))
PROMETHEUS_PREFIX = os.getenv("PROMETHEUS_PREFIX", "steth_price_balancer")

HEALTHCHECK_SERVER_PORT = int(os.getenv("HEALTHCHECK_SERVER_PORT", "9010"))

MAX_CYCLE_LIFETIME_IN_SECONDS = int(os.getenv("MAX_CYCLE_LIFETIME_IN_SECONDS", 60))
