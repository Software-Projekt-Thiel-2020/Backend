import hashlib
import time
from typing import List

import base58
import ecdsa
import jwt
import requests


def my_assert(statement: bool):
    if not statement:
        raise AssertionError


class BlockstackAuth:
    NAME_LOOKUP_URL = "https://core.blockstack.org/v1/names/"

    @staticmethod
    def _do_signatures_match_public_keys(decoded):
        primary_key = decoded["public_keys"][0]
        my_assert(len(decoded["public_keys"]) == 1)
        ecdsa.VerifyingKey.from_string(bytes.fromhex(primary_key), curve=ecdsa.SECP256k1)

    @staticmethod
    def _get_did_type(did: str):
        did_parts: List[str] = did.split(":")

        my_assert(len(did_parts) == 3)
        my_assert(did_parts[0].lower() == "did")

        return did_parts[1]

    @classmethod
    def _get_address_from_did(cls, decentralized_id):
        did_type = cls._get_did_type(decentralized_id)

        my_assert(did_type == 'btc-addr')
        return decentralized_id.split(":")[2]

    @staticmethod
    def _hash_sha256sync(data):
        tmp = hashlib.sha256()
        tmp.update(data)
        return tmp.digest()

    @staticmethod
    def _hash_ripemd160(data):
        tmp = hashlib.new('ripemd160')
        tmp.update(data)
        return tmp.digest()

    @staticmethod
    def _to_base58_check(data):
        data = (bytes("\x00", encoding="ascii") + data)  # append 0 byte for version
        return base58.b58encode_check(data)

    @classmethod
    def _public_key_to_address(cls, primary_key):
        pk_hash160 = cls._hash_ripemd160(cls._hash_sha256sync(primary_key))
        return cls._to_base58_check(pk_hash160)

    @classmethod
    def _do_public_keys_match_issuer(cls, decoded):
        address_from_issuer = cls._get_address_from_did(decoded["iss"])

        my_assert(len(decoded["public_keys"]) == 1)
        primary_key = decoded["public_keys"][0]
        address_from_public_keys = cls._public_key_to_address(bytes.fromhex(primary_key)).decode("ascii")

        my_assert(address_from_issuer == address_from_public_keys)

    @classmethod
    def _do_public_keys_match_username(cls, decoded, name_lookup_url):
        headers = {
            'referrer': 'no-referrer',
            'referrerPolicy': 'no-referrer',
        }

        my_assert(decoded["username"] is not None)  # we specifically need the name in our app
        my_assert(name_lookup_url is not None)
        my_assert(isinstance(name_lookup_url, str))

        username = decoded["username"]
        url = name_lookup_url + username

        response = requests.get(url, headers=headers)
        my_assert(response.status_code == 200)
        response_json = response.json()

        my_assert("address" in response_json)

        name_owning_address = response_json["address"]
        address_from_issuer = cls._get_address_from_did(decoded["iss"])

        my_assert(name_owning_address == address_from_issuer)
        return True

    @classmethod
    def verify_auth_response(cls, token, name_lookup_url=None):
        """
        Verifies a Blockstack JWT (including public key matching for issuer and username against blockstack-core-api).

        :param token:
        :param name_lookup_url:
        :return:
        """
        if name_lookup_url is None:
            name_lookup_url = cls.NAME_LOOKUP_URL

        decoded = jwt.decode(token, verify=False)
        try:
            my_assert(int(time.time()) < decoded["exp"])  # isExpirationDateValid
            my_assert(int(time.time()) > decoded["iat"])  # isIssuanceDateValid
            cls._do_signatures_match_public_keys(decoded)
            cls._do_public_keys_match_issuer(decoded)
            cls._do_public_keys_match_username(decoded, name_lookup_url)
            return True
        except AssertionError:
            return False

    @classmethod
    def get_username_from_token(cls, token):
        decoded = jwt.decode(token, verify=False)
        return decoded["username"]

    @classmethod
    def short_jwt(cls, token):
        decoded = jwt.decode(token, verify=False)
        decoded.pop("private_key", None)
        decoded.pop("associationToken", None)
        decoded.pop("profile", None)
        return jwt.encode(decoded, key="").decode('utf-8')
