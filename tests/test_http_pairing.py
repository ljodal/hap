from hap import tlv
from hap.crypto import chacha20poly1305, ed22519, hkdf, srp
from hap.http.api.pairing import SETUP_CODE

from .fixtures import Client


def test_pairing_setup(client: Client) -> None:
    """
    Test the full pairing setup, from unpaired to successfully paired.
    """

    #
    # Initial request to the accessory
    #

    response = client.post("/pair-setup", tlv=(tlv.State(1), tlv.Method(1)))
    assert response.status == 200

    tlv_data = response.tlv()
    match tlv_data:
        case tlv.State(2), tlv.PublicKey(public_key), tlv.Salt(salt):
            pass
        case _:
            raise AssertionError(f"Unexpected TLV data: {tlv_data}")

    #
    # Second request, send our public key and proof that we know the setup code
    #

    srp_session = srp.Client("Pair-Setup", SETUP_CODE, salt, public_key)

    response = client.post(
        "/pair-setup",
        tlv=(
            tlv.State(3),
            tlv.PublicKey(srp_session.public_key),
            tlv.Proof(srp_session.get_proof()),
        ),
    )
    assert response.status == 200

    tlv_data = response.tlv()
    match tlv_data:
        case tlv.State(4), tlv.Proof(proof):
            pass
        case _:
            raise AssertionError(f"Unexpected TLV data: {tlv_data}")

    assert srp_session.verify_servers_proof(proof)

    #
    # Third and final request to the accessory
    #

    ios_device_pairing_id = "foo"
    ios_device_ltsk = ed22519.generate_private_key()
    ios_device_ltpk = ed22519.get_public_key(ios_device_ltsk)
    ios_device_x = hkdf(
        srp_session.get_session_key(),
        b"Pair-Setup-Controller-Sign-Salt",
        b"Pair-Setup-Controller-Sign-Info",
    )
    ios_device_info = ios_device_x + ios_device_pairing_id.encode() + ios_device_ltpk

    ios_device_signature = ios_device_ltsk.sign(ios_device_info)

    sub_tlv = tlv.encode(
        tlv.Identifier(ios_device_pairing_id),
        tlv.PublicKey(ios_device_ltpk),
        tlv.Signature(ios_device_signature),
    )

    session_key = hkdf(
        srp_session.get_shared_secret(),
        b"Pair-Setup-Encrypt-Salt",
        b"Pair-Setup-Encrypt-Info",
    )

    encrypted_data = chacha20poly1305.encrypt(
        session_key, b"PS-Msg05\x00\x00\x00\x00", sub_tlv
    )

    response = client.post(
        "/pair-setup", tlv=(tlv.State(5), tlv.EncryptedData(encrypted_data))
    )
    assert response.status == 200

    tlv_data = response.tlv()
    match tlv_data:
        case tlv.State(6), tlv.EncryptedData(encrypted_data):
            pass
        case _:
            raise AssertionError(f"Unexpected TLV data: {tlv_data}")

    assert False
