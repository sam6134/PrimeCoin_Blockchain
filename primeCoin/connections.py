import structlog
from more_itertools import take
from asyncio import StreamWriter
logger = structlog.getLogger(__name__)


class ConnectionPool:
    def __init__(self):
        self.connection_pool = dict()  # <1>

    @staticmethod
    def get_address_string(writer):
        ip = writer.address["ip"]
        port = writer.address["port"]
        return f"{ip}:{port}"  # <2>

    def add_peer(self, writer):
        address = self.get_address_string(writer)
        if(address not in self.connection_pool):
            self.connection_pool[address] = writer
            logger.info("Added new peer to pool", address=address)

    def remove_peer(self, writer):
        address = self.get_address_string(writer)
        self.connection_pool.pop(address)
        logger.info("Removed peer from pool", address=address)

    def get_alive_peers(self, count):
        # TODO: implement sort by most active time
        # get the first *count* of the peers
        return take(count, self.connection_pool.items())  # <3>
