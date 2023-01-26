import logging

from prometheus_client import start_http_server
from web3 import HTTPProvider, Web3

from steth_price_balancer import variables
from steth_price_balancer.blockchain.contracts import contracts
from steth_price_balancer.blockchain.middlewares import add_requests_metric_middleware
from steth_price_balancer.metrics.healthcheck import start_pulse_server
from steth_price_balancer.services.steth_price_balancer import StethPriceBalancer

# from web3_multi_provider import MultiProvider


logger = logging.getLogger(__name__)


if __name__ == "__main__":
    logger.info(
        {
            "msg": "Start up steth price balancer.",
            "variables": {
                "STETH_PRICE_ORACLE_BLOCK_NUMBER_SHIFT": variables.STETH_PRICE_ORACLE_BLOCK_NUMBER_SHIFT,
                "STETH_CURVE_POOL_CONTRACT": variables.STETH_CURVE_POOL_CONTRACT,
                "STETH_PRICE_ORACLE_CONTRACT": variables.STETH_PRICE_ORACLE_CONTRACT,
                "PROMETHEUS_PORT": variables.PROMETHEUS_PORT,
                "HEALTHCHECK_SERVER_PORT": variables.HEALTHCHECK_SERVER_PORT,
                "MAX_CYCLE_LIFETIME_IN_SECONDS": variables.MAX_CYCLE_LIFETIME_IN_SECONDS,
                "GAS_LIMIT": variables.GAS_LIMIT,
            },
        }
    )

    logger.info(
        {
            "msg": f"Start healthcheck server for Docker container on port {variables.HEALTHCHECK_SERVER_PORT}"
        }
    )
    start_pulse_server()

    logger.info(
        {
            "msg": f"Start http server with prometheus metrics on port {variables.PROMETHEUS_PORT}"
        }
    )
    start_http_server(variables.PROMETHEUS_PORT)

    logger.info({"msg": "Initialize multi web3 provider."})
    w3 = Web3(HTTPProvider(variables.WEB3_RPC_ENDPOINTS[0]))
    # w3 = Web3(MultiProvider(variables.WEB3_RPC_ENDPOINTS))

    logger.info({"msg": "Add metrics middleware for ETH1 requests."})
    add_requests_metric_middleware(w3)

    logger.info({"msg": "Initialize contracts."})
    contracts.initialize(w3)

    logger.info({"msg": "Initialize Oracle."})
    service = StethPriceBalancer(w3)

    service.run_as_daemon()
