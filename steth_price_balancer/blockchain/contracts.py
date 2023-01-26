import json

from web3 import Web3

from steth_price_balancer import variables


class Contracts:
    pool = None
    stable_swap_state_oracle = None

    @staticmethod
    def _load_abi(abi_path, abi_name):
        f = open(f"{abi_path}{abi_name}.json")
        return json.load(f)

    def initialize(self, w3: Web3, abi_path="./abi/"):
        self.pool = w3.eth.contract(
            address=variables.STETH_CURVE_POOL_CONTRACT,
            abi=self._load_abi(abi_path, "steth_curve_pool"),
        )

        self.stable_swap_state_oracle = w3.eth.contract(
            address=variables.STETH_PRICE_ORACLE_CONTRACT,
            abi=self._load_abi(abi_path, "steth_price_oracle"),
        )


contracts = Contracts()
