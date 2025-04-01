"""
Module for file encryption and decryption using BytestreamCrypto
"""

from .bytestream_crypto import BytestreamCrypto
import os
import struct

class FileLocker:
    def __init__(self):
        self._crypto = BytestreamCrypto()

    def encrypt_file(self, input_path: str, output_path: str, dek: bytes) -> None:
        """
        Encrypt a file using the provided DEK
        
        Args:
            input_path: Path to the input file
            output_path: Path where the encrypted file will be saved
            dek: The Data Encryption Key to use
        """
        self._crypto.set_dek(dek)
        
        with open(input_path, 'rb') as f:
            data = f.read()
        
        nonce, ciphertext = self._crypto.encrypt(data)
        
        with open(output_path, 'wb') as f:
            # Write nonce (12 bytes) and ciphertext
            f.write(nonce)
            f.write(ciphertext)

    def decrypt_file(self, input_path: str, output_path: str, dek: bytes) -> None:
        """
        Decrypt a file using the provided DEK
        
        Args:
            input_path: Path to the encrypted file
            output_path: Path where the decrypted file will be saved
            dek: The Data Encryption Key to use
        """
        self._crypto.set_dek(dek)
        
        with open(input_path, 'rb') as f:
            # Read nonce (12 bytes) and ciphertext
            nonce = f.read(12)
            ciphertext = f.read()
        
        plaintext = self._crypto.decrypt(nonce, ciphertext)
        
        with open(output_path, 'wb') as f:
            f.write(plaintext) 