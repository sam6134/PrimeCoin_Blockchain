import asyncio

from primeCoin.blockchain import Blockchain
from primeCoin.connections import ConnectionPool
from primeCoin.peers import P2PProtocol
from primeCoin.server import Server


blockchain = Blockchain()  # <1>
connection_pool = ConnectionPool()  # <2>


server = Server(blockchain, connection_pool)
server.p2p_protocol = P2PProtocol(server)

nodePort = int(input("Enter port: "))
async def main():
    # Start the server
    await server.listen(port=nodePort)

asyncio.run(main())
