import logging
import time
from functools import lru_cache

from timeout_decorator import TimeoutError, timeout
from web3 import Web3
from web3.exceptions import BlockNotFound

from steth_price_balancer import constants, variables
from steth_price_balancer.blockchain.contracts import contracts
from steth_price_balancer.blockchain.tx_execution import (
    check_transaction,
    sign_and_send_transaction,
)
from steth_price_balancer.services.build_proof import encode_proof_data

# from web3_multi_provider import NoActiveProviderError


logger = logging.getLogger(__name__)


class StethPriceBalancer:
    def __init__(self, web3: Web3):
        logger.info({"msg": "Initialize Oracle STETH Price Balancer Module."})

        self._w3 = web3

    def run_as_daemon(self):
        while True:
            self._cycle_handler()

    @timeout(variables.MAX_CYCLE_LIFETIME_IN_SECONDS)
    def _cycle_handler(self):
        try:
            self.run_cycle()
        except BlockNotFound as error:
            logger.warning({"msg": "Fetch block exception.", "error": str(error)})
            time.sleep(constants.DEFAULT_SLEEP)
        except TimeoutError as exception:
            # Bot is stuck. Drop bot and restart using Docker service
            logger.error(
                {"msg": "Price balancer do not respond.", "error": str(exception)}
            )
            raise TimeoutError("Price balancer stuck.") from exception
        # except NoActiveProviderError as exception:
        #     logger.error({'msg': 'No active node available.', 'error': str(exception)})
        #     raise NoActiveProviderError from exception
        except ConnectionError as error:
            logger.error({"msg": error.args, "error": str(error)})
            raise ConnectionError from error
        except ValueError as error:
            logger.error({"msg": error.args, "error": str(error)})
            time.sleep(constants.DEFAULT_SLEEP)
        except Exception as error:
            logger.warning({"msg": "Unexpected exception.", "error": str(error)})
            time.sleep(constants.DEFAULT_SLEEP)
        else:
            time.sleep(constants.DEFAULT_SLEEP)

    @lru_cache(maxsize=1)
    def _get_proof_params(self, block_identifier):
        return contracts.stable_swap_state_oracle.functions.getProofParams().call(
            block_identifier=block_identifier
        )

    def run_cycle(self):
        block_number = (
            self._w3.eth.get_block("latest").number
            - variables.STETH_PRICE_ORACLE_BLOCK_NUMBER_SHIFT
        )
        logger.info(
            {
                "msg": f"Start balancer cycle for block {block_number}.",
                "value": block_number,
            }
        )

        oracle_price = contracts.stable_swap_state_oracle.functions.stethPrice().call(
            block_identifier=block_number
        )
        logger.info({"msg": "Fetch steth price in oracle.", "value": oracle_price})

        pool_price = contracts.pool.functions.get_dy(1, 0, 10**18).call(
            block_identifier=block_number
        )
        logger.info({"msg": "Fetch steth price in pool.", "value": pool_price})

        percentage_diff = 100 * abs(1 - oracle_price / pool_price)
        logger.info(
            {"msg": "Calculate different percentage.", "value": percentage_diff}
        )

        proof_params = self._get_proof_params(block_number)
        logger.info({"msg": "Fetch proof params.", "value": proof_params})

        # proof_params[-1] contains priceUpdateThreshold value in basis points: 10000 BP equal to 100%, 100 BP to 1%.
        price_update_threshold = proof_params[-1] / 100
        is_state_actual = percentage_diff < price_update_threshold

        if is_state_actual:
            logging.info(
                f"StETH Price Oracle state valid (prices difference < {price_update_threshold:.2f}%). No update required."
            )
            self.submit_new_state(block_number)
        else:
            logging.info(
                f"StETH Price Oracle state outdated (prices difference >= {price_update_threshold:.2f}%). Submitting new one..."
            )
            self.submit_new_state(block_number)

    def submit_new_state(self, block_number: int):
        logger.info({"msg": f"Submit new state for block: {block_number}"})

        proof_params = self._get_proof_params(block_number)
        logger.info({"msg": "Get proof params.", "value": proof_params})

        header_blob, proofs_blob = encode_proof_data(
            self._w3.provider, block_number, proof_params
        )

        logger.info(
            {
                "msg": "Calculating proofs.",
                "value": {"header_blob": header_blob, "proofs_blob": proofs_blob},
            }
        )

        tx = contracts.stable_swap_state_oracle.functions.submitState(
            header_blob, proofs_blob
        )

        if check_transaction(tx, variables.ACCOUNT.address):
            sign_and_send_transaction(self._w3, tx, variables.ACCOUNT)
        sign_and_send_transaction(self._w3, tx, variables.ACCOUNT)
