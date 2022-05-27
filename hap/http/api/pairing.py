import enum
from typing import Any

from ... import tlv
from ...crypto import srp
from ..request import Request
from ..response import BadRequest, PairingResponse, Response, UnprocessableEntity


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


def _paring_setup_m1(request: Request, *values: tlv.TLV[Any]) -> PairingResponse:
    """
    First pairing stage.
    """

    # TODO: Get this from somewhere
    # if is_paired:
    #     return PairingResponse(tlv.STATE(State.M2), tlv.ERROR(Error.UNAVAILABLE))
    # if is_paring:
    #     return PairingResponse(tlv.STATE(State.M2), tlv.ERROR(Error.BUSY))

    match values:
        case [tlv.Method(Method.PAIR_SETUP_WITH_AUTH)]:
            pass
        case [tlv.Method(Method.PAIR_SETUP), tlv.Flags(_)]:
            # TODO: Might have to support this
            return PairingResponse(tlv.State(2), tlv.Error(AUTHENTICATION))
        case _:
            return PairingResponse(tlv.State(2), tlv.Error(UNKNOWN))

    srp_session = srp.Server(username="Pair-Setup", password=SETUP_CODE)

    return PairingResponse(
        tlv.State(2),
        tlv.PublicKey(srp_session.public_key),
        tlv.Salt(srp_session.salt),
        # TODO: Flags
    )


def _paring_setup_m3(request: Request, *values: tlv.TLV[Any]) -> PairingResponse:
    """
    Second pairing stage.
    """

    if (srp_session := request.srp_session) is None:
        return PairingResponse(tlv.State(4), tlv.Error(UNKNOWN))

    match values:
        case [tlv.PublicKey(public_key), tlv.Proof(client_proof)]:
            srp_session.set_client_public_key(public_key)

            if not srp_session.verify_clients_proof(client_proof):
                return PairingResponse(tlv.State(4), tlv.Error(AUTHENTICATION))

            our_proof = srp_session.get_proof(client_proof)
            return PairingResponse(tlv.State(4), tlv.Proof(our_proof))
        case _:
            return PairingResponse(tlv.State(4), tlv.Error(UNKNOWN))


def _paring_setup_m5(request: Request, *values: tlv.TLV[Any]) -> PairingResponse:
    """
    Third pairing stage.
    """

    # if (srp_session := request.srp_session) is None:
    #     return PairingResponse((tlv.STATE, State.M4), (tlv.ERROR, Error.UNKNOWN))

    match values:
        case [tlv.EncryptedData(_)]:
            raise NotImplementedError
        case _:
            return PairingResponse(tlv.State(6), tlv.Error(UNKNOWN))


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
