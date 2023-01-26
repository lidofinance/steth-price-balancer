from prometheus_client import Counter, Gauge, Histogram

from variables import PROMETHEUS_PREFIX

BUILD_INFO = Gauge(
    "build_info",
    "Build info",
    ["name"],
    namespace=PROMETHEUS_PREFIX,
)

ACCOUNT_BALANCE = Gauge(
    "account_balance",
    "Account balance",
    ["address"],
    namespace=PROMETHEUS_PREFIX,
)

EXCEPTIONS_COUNT = Counter(
    "exceptions_count",
    "Exceptions count",
    ["module"],
    namespace=PROMETHEUS_PREFIX,
)

RPC_REQUESTS = Counter(
    "eth_rpc_requests",
    "Total count of requests to ETH1 RPC",
    ["method", "code", "domain"],
    namespace=PROMETHEUS_PREFIX,
)

RPC_REQUESTS_DURATION = Histogram(
    "eth_rpc_requests_duration",
    "Duration of requests to ETH1 RPC",
    namespace=PROMETHEUS_PREFIX,
)

TX_SEND = Counter(
    "tx_send",
    "Sent tx count.",
    namespace=PROMETHEUS_PREFIX,
)

TX_FAILURE = Counter(
    "tx_failure",
    "Tx failures.",
    namespace=PROMETHEUS_PREFIX,
)
