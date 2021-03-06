import binascii

import asynctest
from tests.decorators import with_client


class TestClient(asynctest.TestCase):
    @with_client
    async def test_connect(self, client, protocol):
        connect_return = binascii.unhexlify(
            "636f6d6f6b20312c36372d302c4e5834383237543034335f303131522c3133302c36313438382c453436383543423335423631333633362c3136373737323136"
        )

        protocol.read = asynctest.CoroutineMock(
            side_effect=[b"1a", connect_return, b"", b"\01", b""]
        )
        await client.connect()

    @with_client
    async def test_get_numeric(self, client, protocol):
        client._connection = protocol

        response_data = binascii.unhexlify("7101000000")

        protocol.read = asynctest.CoroutineMock(
            side_effect=[response_data, b"\01", b""]
        )

        result = await client.get("sleep")
        protocol.write.assert_called_once_with(b"get sleep")

        assert result == True

    @with_client
    async def test_get_string(self, client, protocol):
        client._connection = protocol

        response_data = binascii.unhexlify("703430")

        protocol.read = asynctest.CoroutineMock(
            side_effect=[response_data, b"\01", b""]
        )

        result = await client.get("t16.txt")
        protocol.write.assert_called_once_with(b"get t16.txt")

        assert result == "40"

    @with_client
    async def test_set(self, client, protocol):
        client._connection = protocol

        protocol.read = asynctest.CoroutineMock(side_effect=[b"\01", b""])

        result = await client.set("sleep", 1)
        protocol.write.assert_called_once_with(b"sleep=1")

        assert result == True
