"""
Module for AES-256-GCM encryption and decryption of bytestreams
"""

from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import os
import base64

class BytestreamCrypto:
    def __init__(self):
        self._dek = None
        self._aesgcm = None

    def generate_dek(self) -> bytes:
        """Generate a random Data Encryption Key (DEK)"""
        self._dek = os.urandom(32)  # 256 bits
        self._aesgcm = AESGCM(self._dek)
        return self._dek

    def set_dek(self, dek: bytes) -> None:
        """Set an existing Data Encryption Key (DEK)"""
        if len(dek) != 32:
            raise ValueError("DEK must be 32 bytes (256 bits)")
        self._dek = dek
        self._aesgcm = AESGCM(self._dek)

    def encrypt(self, data: bytes) -> tuple[bytes, bytes]:
        """
        Encrypt data using AES-256-GCM
        
        Returns:
            tuple: (nonce, ciphertext)
        """
        if not self._aesgcm:
            raise RuntimeError("DEK not set. Call generate_dek() or set_dek() first.")
        
        nonce = os.urandom(12)  # 96 bits for GCM
        ciphertext = self._aesgcm.encrypt(nonce, data, None)
        return nonce, ciphertext

    def decrypt(self, nonce: bytes, ciphertext: bytes) -> bytes:
        """
        Decrypt data using AES-256-GCM
        
        Args:
            nonce: The nonce used during encryption
            ciphertext: The encrypted data
            
        Returns:
            bytes: The decrypted data
        """
        if not self._aesgcm:
            raise RuntimeError("DEK not set. Call set_dek() first.")
        
        return self._aesgcm.decrypt(nonce, ciphertext, None)

    def get_dek(self) -> bytes:
        """Get the current DEK"""
        if not self._dek:
            raise RuntimeError("DEK not set")
        return self._dek 