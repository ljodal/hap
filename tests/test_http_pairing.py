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

    match tlv.decode(response.body):
        case tlv.State(2), tlv.PublicKey(accessory_public_key), tlv.Salt(salt):
            pass
        case tlv_data:
            raise AssertionError(f"Unexpected TLV data: {tlv_data}")

    #
    # Second request, send our public key and proof that we know the setup code
    #

    srp_session = srp.Client("Pair-Setup", SETUP_CODE, salt, accessory_public_key)
    shared_secret = srp_session.get_shared_secret()
    session_key = hkdf(
        shared_secret, b"Pair-Setup-Encrypt-Salt", b"Pair-Setup-Encrypt-Info"
    )

    response = client.post(
        "/pair-setup",
        tlv=(
            tlv.State(3),
            tlv.PublicKey(srp_session.public_key),
            tlv.Proof(srp_session.get_proof()),
        ),
    )
    assert response.status == 200

    match tlv.decode(response.body):
        case tlv.State(4), tlv.Proof(proof):
            pass
        case tlv_data:
            raise AssertionError(f"Unexpected TLV data: {tlv_data}")

    assert srp_session.verify_servers_proof(proof)

    #
    # Third and final request to the accessory
    #

    ios_device_pairing_id = "foo"
    ios_device_private_key = ed22519.generate_private_key()
    ios_device_public_key = ed22519.get_public_key(ios_device_private_key)
    ios_device_x = hkdf(
        shared_secret,
        b"Pair-Setup-Controller-Sign-Salt",
        b"Pair-Setup-Controller-Sign-Info",
    )
    ios_device_info = (
        ios_device_x + ios_device_pairing_id.encode() + ios_device_public_key
    )

    ios_device_signature = ios_device_private_key.sign(ios_device_info)

    sub_tlv = tlv.encode(
        tlv.Identifier(ios_device_pairing_id),
        tlv.PublicKey(ios_device_public_key),
        tlv.Signature(ios_device_signature),
    )

    nonce = b"PS-Msg05\x00\x00\x00\x00"
    encrypted_data = chacha20poly1305.encrypt(session_key, nonce, sub_tlv)

    response = client.post(
        "/pair-setup", tlv=(tlv.State(5), tlv.EncryptedData(encrypted_data))
    )
    assert response.status == 200

    match tlv.decode(response.body):
        case tlv.State(6), tlv.EncryptedData(encrypted_data):
            pass
        case tlv_data:
            raise AssertionError(f"Unexpected TLV data: {tlv_data}")

    nonce = b"PS-Msg06\x00\x00\x00\x00"
    decrypted_data = chacha20poly1305.decrypt(session_key, nonce, encrypted_data)
    match tlv.decode(decrypted_data):
        case [
            tlv.Identifier(accessory_pairing_id),
            tlv.PublicKey(accessory_public_key),
            tlv.Signature(accessory_signature),
        ]:
            pass
        case tlv_data:
            raise AssertionError(f"Unexpected TLV data: {tlv_data}")

    accessory_x = hkdf(
        shared_secret,
        b"Pair-Setup-Accessory-Sign-Salt",
        b"Pair-Setup-Accessory-Sign-Info",
    )
    accessory_info = accessory_x + accessory_pairing_id.encode() + accessory_public_key

    ed22519.verify(accessory_public_key, accessory_signature, accessory_info)
