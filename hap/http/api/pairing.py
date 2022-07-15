import enum
import logging
from typing import Any

from ... import tlv
from ...crypto import chacha20poly1305, ed22519, hkdf, srp
from ..request import Request
from ..response import BadRequest, Response, TLVResponse, UnprocessableEntity

logger = logging.getLogger(__name__)


class Method(enum.IntEnum):
    PAIR_SETUP = 0
    PAIR_SETUP_WITH_AUTH = 1
    PAIR_VERIFY = 2
    ADD_PAIRING = 3
    REMOVE_PAIRING = 4
    LIST_PAIRINGS = 5


UNKNOWN = 1
AUTHENTICATION = 2
BACKOFF = 3
MAX_PEERS = 4
MAX_TRIES = 5
UNAVAILABLE = 6
BUSY = 7


# Pairing

SETUP_CODE = "843-15-743"


def _paring_setup_m1(request: Request, *values: tlv.TLV[Any]) -> TLVResponse:
    """
    First pairing stage.
    """

    # TODO: Get this from somewhere
    # if is_paired:
    #     return TLVResponse(tlv.STATE(State.M2), tlv.ERROR(Error.UNAVAILABLE))
    # if is_paring:
    #     return TLVResponse(tlv.STATE(State.M2), tlv.ERROR(Error.BUSY))

    match values:
        case [tlv.Method(Method.PAIR_SETUP_WITH_AUTH)]:
            pass
        case [tlv.Method(Method.PAIR_SETUP), tlv.Flags(_)]:
            logger.error("Tried to pare without auth, not supported")
            # TODO: Might have to support this
            return TLVResponse(tlv.State(2), tlv.Error(AUTHENTICATION))
        case tlv_data:
            logger.error("Unexpected M1 data received: %s", tlv_data)
            return TLVResponse(tlv.State(2), tlv.Error(UNKNOWN))

    session = request.session
    session.srp = srp.Server(username="Pair-Setup", password=SETUP_CODE)

    return TLVResponse(
        tlv.State(2),
        tlv.PublicKey(session.srp.public_key),
        tlv.Salt(session.srp.salt),
    )


def _paring_setup_m3(request: Request, *values: tlv.TLV[Any]) -> TLVResponse:
    """
    Second pairing stage.
    """

    if (srp_session := request.session.srp) is None:
        logger.error("SRP session is missing")
        return TLVResponse(tlv.State(4), tlv.Error(UNKNOWN))

    match values:
        case [tlv.PublicKey(public_key), tlv.Proof(client_proof)]:
            pass
        case tlv_data:
            logger.error("Unexpected M3 data received: %s", tlv_data)
            return TLVResponse(tlv.State(4), tlv.Error(UNKNOWN))

    srp_session.set_client_public_key(public_key)

    if not srp_session.verify_clients_proof(client_proof):
        logger.error("Client proof did not match")
        return TLVResponse(tlv.State(4), tlv.Error(AUTHENTICATION))

    our_proof = srp_session.get_proof(client_proof)
    return TLVResponse(tlv.State(4), tlv.Proof(our_proof))


def _paring_setup_m5(request: Request, *values: tlv.TLV[Any]) -> TLVResponse:
    """
    Third pairing stage.
    """

    if (srp_session := request.session.srp) is None:
        logger.error("SRP session is missing")
        return TLVResponse(tlv.State(6), tlv.Error(UNKNOWN))

    shared_secret = srp_session.get_shared_secret()
    session_key = hkdf(
        shared_secret, b"Pair-Setup-Encrypt-Salt", b"Pair-Setup-Encrypt-Info"
    )

    match values:
        case [tlv.EncryptedData(encrypted_data)]:
            pass
        case tlv_data:
            logger.error("Unexpected M5 data received: %s", tlv_data)
            return TLVResponse(tlv.State(6), tlv.Error(UNKNOWN))

    try:
        # Decrypt the received data
        nonce = b"PS-Msg05\x00\x00\x00\x00"
        decrypted_data = chacha20poly1305.decrypt(session_key, nonce, encrypted_data)
        # Decode the decrypted data
        decoded_values = tlv.decode(decrypted_data)
        # Verify the client's signature
        _verify_client_signature(shared_secret, *decoded_values)
    except ValueError:
        logger.exception("Unable to verify client's signature")
        return TLVResponse(tlv.State(6), tlv.Error(AUTHENTICATION))

    # The client has been verified, so we need to store the pairing id and
    # public key of the client

    our_signature = _generate_our_signature(shared_secret, session_key)
    return TLVResponse(tlv.State(6), tlv.EncryptedData(our_signature))


def _verify_client_signature(shared_secret: bytes, *values: tlv.TLV[Any]) -> None:

    match values:
        case [
            tlv.Identifier(ios_device_pairing_id),
            tlv.PublicKey(ios_device_public_key),
            tlv.Signature(ios_device_signature),
        ]:
            pass
        case _:
            raise ValueError("Invalid encrypted data")

    ios_device_x = hkdf(
        shared_secret,
        salt=b"Pair-Setup-Controller-Sign-Salt",
        info=b"Pair-Setup-Controller-Sign-Info",
    )

    ios_device_info = (
        ios_device_x + ios_device_pairing_id.encode() + ios_device_public_key
    )

    ed22519.verify(ios_device_public_key, ios_device_signature, ios_device_info)


def _generate_our_signature(shared_secret: bytes, session_key: bytes) -> bytes:

    # TODO: Store private keys
    accessory_pairing_id = "bar"
    accessory_private_key = ed22519.generate_private_key()
    accessory_public_key = ed22519.get_public_key(accessory_private_key)
    accessory_x = hkdf(
        shared_secret,
        b"Pair-Setup-Accessory-Sign-Salt",
        b"Pair-Setup-Accessory-Sign-Info",
    )
    accessory_info = accessory_x + accessory_pairing_id.encode() + accessory_public_key
    accessory_signature = accessory_private_key.sign(accessory_info)

    sub_tlv = tlv.encode(
        tlv.Identifier(accessory_pairing_id),
        tlv.PublicKey(accessory_public_key),
        tlv.Signature(accessory_signature),
    )
    return chacha20poly1305.encrypt(session_key, b"PS-Msg06\x00\x00\x00\x00", sub_tlv)


async def pairing_setup(request: Request) -> Response:
    try:
        values = request.tlv()
    except ValueError:
        return BadRequest(b"Expected a TLV encoded request")

    match values:
        case [tlv.State(1), *rest]:
            return _paring_setup_m1(request, *rest)
        case [tlv.State(3), *rest]:
            return _paring_setup_m3(request, *rest)
        case [tlv.State(5), *rest]:
            return _paring_setup_m5(request, *rest)
        case _:
            return UnprocessableEntity(b"")
