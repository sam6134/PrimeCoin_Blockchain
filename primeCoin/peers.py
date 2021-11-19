import asyncio

import structlog

from primeCoin.messages import (
    create_peers_message,
    create_block_message,
    create_transaction_message,
    create_ping_message,
)
from primeCoin.transactions import validate_transaction

logger = structlog.getLogger(__name__)


class P2PError(Exception):
    pass


class P2PProtocol:
    def __init__(self, server):
        self.server = server
        self.blockchain = server.blockchain
        self.connection_pool = server.connection_pool

    @staticmethod
    async def send_message(writer, message):
        writer.write(message.encode() + b"\n")

    async def handle_message(self, message, writer):
        message_handlers = {
            "block": self.handle_block,
            "ping": self.handle_ping,
            "peers": self.handle_peers,
            "transaction": self.handle_transaction,
        }
        print(message["name"])
        handler = message_handlers.get(message["name"], None)
        
        if not handler:
            raise P2PError("Missing handler for message")

        await handler(message, writer)

    async def handle_ping(self, message, writer):
        """
        Executed when we receive a `ping` message
        """
        logger.info("Recieved ping")

        block_height = message["payload"]["block_height"]

        # If they're a miner
        writer.is_miner = message["payload"]["is_miner"]

        # Send our 20 most "alive" peers
        peers = self.connection_pool.get_alive_peers(20)
        peerAddresses = [x[1].address for x in peers]
        peers_message = create_peers_message(
            self.server.external_ip, self.server.external_port, peerAddresses
        )
        await self.send_message(writer, peers_message)

        # Send them blocks if they have less than us
        if block_height < self.blockchain.last_block["height"]:
            # Send them the whole block chain
            await self.send_message(
                    writer,
                    create_block_message(
                        self.server.external_ip, self.server.external_port, self.blockchain.chain
                    ),
                )

    async def handle_transaction(self, message, writer):
        """
        Executed when we receive a transaction that was broadcast by a peer
        """
        logger.info("Received transaction")

        # Validate the transaction
        tx = message["payload"]

        if validate_transaction(tx) is True:
            # Add the tx to our pool, and propagate it to our peers
            if tx not in self.blockchain.pending_transactions:
                self.blockchain.pending_transactions.append(tx)

                for peer in self.connection_pool.get_alive_peers(20):
                    await self.send_message(
                        peer,
                        create_transaction_message(
                            self.server.external_ip, self.server.external_port, tx
                        ),
                    )
        else:
            logger.warning("Received invalid transaction")

    async def handle_block(self, message, writer):
        """
        Executed when we receive a block that was broadcast by a peer
        """

        newchain = message["payload"]

        # Give the block to the blockain to append if valid
        if(len(newchain) > len(self.blockchain.chain)):
            logger.info("Received new blockChain of greater length")
            self.blockchain.chain = newchain
            logger.info(f"New chain has height: {len(self.blockchain.chain)}")

        

    async def handle_peers(self, message, writer):
        """
        Executed when we receive a block that was broadcast by a peer
        """
        logger.info("Received new peers")

        peers = message["payload"]

        # Craft a ping message for us to send to each peer
        ping_message = create_ping_message(
            self.server.external_ip,
            self.server.external_port,
            len(self.blockchain.chain),
            len(self.connection_pool.get_alive_peers(20)),
            False,
        )

        for peer in peers:
            # if the peer is not ourselves and not in pool add it to the pool
            peerAddress = peer["ip"]+":"+str(peer["port"])
            selfAddress = self.server.external_ip+":"+str(self.server.external_port)

            if(peerAddress != selfAddress and peerAddress not in self.connection_pool.connection_pool):

                _, peerWriter = await asyncio.open_connection(peer["ip"], peer["port"])
                peerWriter.address = {"ip":peer["ip"], "port":peer["port"]}
                self.connection_pool.add_peer(peerWriter)

                # Send the peer a PING message
                await self.send_message(peerWriter, ping_message)
