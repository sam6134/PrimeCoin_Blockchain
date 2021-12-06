import asyncio
from asyncio import StreamReader, StreamWriter
import structlog
from marshmallow.exceptions import MarshmallowError
from primeCoin.peers import P2PProtocol
from primeCoin.messages import BaseSchema
from primeCoin.messages import create_ping_message

logger = structlog.getLogger()  # <7>


class Server:
    def __init__(self, blockchain, connection_pool):
        self.blockchain = blockchain  # <1>
        self.connection_pool = connection_pool
        self.p2p_protocol: P2PProtocol= None
        self.external_ip = None
        self.external_port = None
        self.isMining = False

        if not (blockchain and connection_pool):
            logger.error(
                "'blockchain' or 'connection_pool' is not instantiated"
            )
            raise Exception("Could not start")

    async def handle_connection(self, reader: StreamReader, writer: StreamWriter):
        while True:
            try:
                # Wait forever on new data to arrive
                logger.info("Waiting for new data")
                data = await reader.readuntil(b"\n")  # <3>

                decoded_data = data.decode("utf8").strip()  # <4>
                logger.info(f"Received data: {decoded_data}")
                
                try:
                    message = BaseSchema().loads(decoded_data)  # <5>
                except MarshmallowError as e:
                    logger.error(f"Error parsing message: {e}")
                    logger.info("Received unreadable message", peer=writer)
                    break
                
                await asyncio.sleep(7)
                _, sendWriter = await asyncio.open_connection(message["meta"]["address"]["ip"], int(message["meta"]["address"]["port"]))
                # Extract the address from the message, add it to the writer object
                sendWriter.address = message["meta"]["address"]

                # Let's add the peer to our connection pool
                self.connection_pool.add_peer(sendWriter)
                
                # ...and handle the message
                await self.p2p_protocol.handle_message(message["message"], sendWriter)

                await writer.drain()
                if writer.is_closing():
                    break

            except Exception as e:
                # An error happened, break out of the wait loop
                logger.error("break out of connection "+str(e))
                # break
                

        # The connection has closed. Let's clean up...
        writer.close()
        await writer.wait_closed()
        self.connection_pool.remove_peer(writer)  # <7>

    async def startMining(self):
        while True:
            if(self.isMining):
                await self.blockchain.mine_new_block()
            else:
                await asyncio.sleep(1)
            


    async def listen(self, hostname="0.0.0.0", port=8888):
        server = await asyncio.start_server(self.handle_connection, hostname, port)
        logger.info(f"Server listening on {hostname}:{port}")

        self.external_ip = hostname
        self.external_port = port
        addPeerOpt = input("Do you want to add a peer? (y/n)")

        if(addPeerOpt == "y"):
            peerHostname = input("Enter peer hostname: ")
            peerPort = int(input("Enter peer port: "))
            await self.addPeer(peerHostname, peerPort)
        else:
            logger.info("No peer added")
        
        isMiner = input("Do you want to mine? (y/n)")
        if(isMiner == "y"):
            self.isMining = True
        
        asyncio.create_task(self.startMining())
        asyncio.create_task(self.pingPeers())
        async with server:
            await server.serve_forever()
        
    async def pingPeers(self):
        """
            Send a ping message to each peer in the connection pool
        """  
        pingTimeout = 0
        while(True):
            pingTimeout += 1
            if(pingTimeout > 5):
                pingTimeout = 0
                for address, writer in self.connection_pool.get_alive_peers(20):
                    ping_message = create_ping_message(
                            self.external_ip,
                            self.external_port,
                            len(self.blockchain.chain),
                            len(self.connection_pool.get_alive_peers(20)),
                            False,
                        )
                    logger.info(f"Pinging to: {address}")
                    await self.p2p_protocol.send_message(writer, ping_message)
            else:
                await asyncio.sleep(1)
            

    async def addPeer(self, peerHostname, peerPort):
        """
            Adds new peer to the connection pool
            1. Send a ping message to peerHost
            2. If the peer responds,
            our listen logic adds the peer to the connection pool
        """
        logger.info(f"Pinging to {peerHostname}:{peerPort}")
        ping_message = create_ping_message(
            self.external_ip,
            self.external_port,
            len(self.blockchain.chain),
            len(self.connection_pool.get_alive_peers(20)),
            False,
        )
        _, writer = await asyncio.open_connection(peerHostname, peerPort)
        await self.p2p_protocol.send_message(writer, ping_message)
        