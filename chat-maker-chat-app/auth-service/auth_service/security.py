from dataclasses import dataclass

from Crypto.Cipher import AES


@dataclass
class CipherObject:
    ciphertext: bytes
    tag: bytes
    nonce: bytes

    def to_string(self) -> str:
        return f"{self.tag.hex()}.{self.ciphertext.hex()}.{self.nonce.hex()}"

    @classmethod
    def from_string(cls, string: str) -> "CipherObject":
        items = string.split(".")
        assert len(items) == 3, "Invalid string to decrypt!"
        tag, ciphertext, nonce = items
        return CipherObject(
            ciphertext=bytes.fromhex(ciphertext),
            tag=bytes.fromhex(tag),
            nonce=bytes.fromhex(nonce),
        )


class DecryptionError(Exception):
    pass


def _encrypt(secret_key: bytes, plaintext: str) -> str:
    cipher = AES.new(secret_key, AES.MODE_EAX)
    nonce = cipher.nonce
    ciphertext, tag = cipher.encrypt_and_digest(plaintext.encode())
    return CipherObject(ciphertext, tag, nonce).to_string()


def _decrypt(secret_key: bytes, encrypted_str: str) -> str:
    cipher_obj = CipherObject.from_string(encrypted_str)
    cipher = AES.new(secret_key, AES.MODE_EAX, nonce=cipher_obj.nonce)
    plaintext = cipher.decrypt(cipher_obj.ciphertext)
    try:
        cipher.verify(cipher_obj.tag)
    except ValueError:
        raise DecryptionError("Key incorrect or message corrupted")
    return plaintext.decode()


class Cipher:
    def __init__(self, secret_key: str):
        self._secret_key: bytes = secret_key.encode()

    def encrypt(self, plaintext: str) -> str:
        return _encrypt(self._secret_key, plaintext)

    def decrypt(self, encrypted_str: str) -> str:
        return _decrypt(self._secret_key, encrypted_str)
