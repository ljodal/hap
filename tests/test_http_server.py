import asyncio

import pytest

from hap.http.server import serve

pytestmark = pytest.mark.asyncio


@pytest.mark.skip("Slow test due to timeout")
async def test_timeout(unused_tcp_port: int) -> None:
    print("Starting server")
    async with serve(port=unused_tcp_port) as server:
        print("Connecting to server")
        reader, writer = await asyncio.open_connection("127.0.0.1", unused_tcp_port)
        print("Connected, stopping server")

        # Close the server
        server.close()
        await server.wait_closed()
        print("Server closed, writing request")

        # Should still respond to requests on an already opened connection
        writer.write(b"GET / HTTP/1.1\nHost: example.com\r\n\r\n")
        await writer.drain()

        print("Wrote request, reading response")

        response = await reader.read()
        print("Read response", response)
        assert response

    print("Done")
