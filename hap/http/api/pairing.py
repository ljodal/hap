import enum
from typing import cast

from ... import tlv
from ...crypto.srp import Server as SRPServer
from ..request import Request
from ..response import BadRequest, PairingResponse, Response, UnprocessableEntity


class Method(bytes, enum.Enum):
    PAIR_SETUP = b"\x00"
    PAIR_SETUP_WITH_AUTH = b"\x01"
    PAIR_VERIFY = b"\x02"
    ADD_PAIRING = b"\x03"
    REMOVE_PAIRING = b"\x04"
    LIST_PAIRINGS = b"\x05"


class State(bytes, enum.Enum):
    M1 = b"\x01"
    M2 = b"\x02"
    M3 = b"\x03"
    M4 = b"\x04"
    M5 = b"\x05"
    M6 = b"\x06"


class Error(bytes, enum.Enum):
    UNKNOWN = b"\x01"
    AUTHENTICATION = b"\x02"
    BACKOFF = b"\x03"
    MAX_PEERS = b"\x04"
    MAX_TRIES = b"\x05"
    UNAVAILABLE = b"\x06"
    BUSY = b"\x07"


# Pairing

SETUP_CODE = "843-15-743"


def _paring_setup_m1(
    request: Request, *values: tuple[tlv.TLVType, bytes]
) -> PairingResponse:
    """
    First pairing stage.
    """

    # TODO: Get this from somewhere
    # if is_paired:
    #     return PairingResponse(tlv.STATE(State.M2), tlv.ERROR(Error.UNAVAILABLE))
    # if is_paring:
    #     return PairingResponse(tlv.STATE(State.M2), tlv.ERROR(Error.BUSY))

    match values:
        case [
            (tlv.METHOD, Method.PAIR_SETUP_WITH_AUTH),
        ]:
            pass
        case [
            (tlv.METHOD, Method.PAIR_SETUP),
            (tlv.FLAGS, _),
        ]:
            # TODO: Might have to support this
            return PairingResponse(tlv.STATE(State.M2), tlv.ERROR(Error.AUTHENTICATION))
        case _:
            return PairingResponse(tlv.STATE(State.M2), tlv.ERROR(Error.UNKNOWN))

    srp = SRPServer(username="Pair-Setup", password=SETUP_CODE)

    return PairingResponse(
        tlv.STATE(State.M2),
        tlv.PUBLIC_KEY(srp.public_key),
        tlv.SALT(srp.salt),
        # TODO: Flags
    )


def _paring_setup_m3(
    request: Request, *values: tuple[tlv.TLVType, bytes]
) -> PairingResponse:
    """
    Second pairing stage.
    """

    # Extract the SRP session from the scope
    match request.scope["extensions"]:
        case {"hap": {"srp": srp}}:
            srp = cast(SRPServer, srp)
        case _:
            return PairingResponse((tlv.STATE, State.M4), (tlv.ERROR, Error.UNKNOWN))

    match values:
        case [
            (tlv.PUBLIC_KEY, public_key),
            (tlv.PROOF, client_proof),
        ]:
            srp.set_client_public_key(public_key)

            if not srp.verify_clients_proof(client_proof):
                return PairingResponse(
                    tlv.STATE(State.M4), tlv.ERROR(Error.AUTHENTICATION)
                )

            # TODO: Needs to set session_key on transport and upgrade to encrypted session
            our_proof = srp.get_proof(client_proof)
            return PairingResponse(tlv.STATE(State.M4), tlv.PROOF(our_proof))
        case _:
            return PairingResponse(
                (tlv.STATE, State.M4),
                (tlv.ERROR, Error.UNKNOWN),
            )


def _paring_setup_m5(
    request: Request, *values: tuple[tlv.TLVType, bytes]
) -> PairingResponse:
    """
    Third pairing stage.
    """

    # Extract the SRP session from the scope
    match request.scope["extensions"]:
        case {"hap": {"srp": srp}}:
            srp = cast(SRPServer, srp)
        case _:
            return PairingResponse((tlv.STATE, State.M4), (tlv.ERROR, Error.UNKNOWN))

    match values:
        case [(tlv.ENCRYPTED_DATA, _)]:
            raise NotImplementedError
        case _:
            return PairingResponse(
                (tlv.STATE, State.M6),
                (tlv.ERROR, Error.UNKNOWN),
            )


async def pairing_setup(request: Request) -> Response:
    try:
        values = request.tlv()
    except ValueError:
        return BadRequest(b"Expected a TLV encoded request")

    match values:
        case [(tlv.STATE, State.M1), *rest]:
            return _paring_setup_m1(request, *rest)
        case [(tlv.STATE, State.M3), *rest]:
            return _paring_setup_m3(request, *rest)
        case [(tlv.STATE, State.M5), *rest]:
            return _paring_setup_m5(request, *rest)
        case _:
            return UnprocessableEntity(b"")
