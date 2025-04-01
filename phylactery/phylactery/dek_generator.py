"""
Module for generating and regenerating Data Encryption Keys using KEKGenerator
"""

from .kek_generator import KEKGenerator
import secrets

class DEKGenerator:
    def __init__(self):
        self._kek_generator = KEKGenerator()
        self._initialized = False
        self._dek = None

    def create_new_dek(self, quorum: int, total_shards: int) -> bool:
        """
        Create a new DEK by generating a new KEK
        
        Args:
            quorum: Number of shards required to reconstruct the KEK
            total_shards: Total number of shards to generate
            
        Returns:
            bool: True if successful, False otherwise
        """
        if self._kek_generator.create_new_kek(quorum, total_shards):
            # Generate a random 32-byte (256-bit) DEK
            self._dek = secrets.token_bytes(32)
            self._initialized = True
            return True
        return False

    def regenerate_dek(self, shards: list[str]) -> bool:
        """
        Regenerate a DEK from provided KEK shards
        
        Args:
            shards: List of shard strings to use for KEK reconstruction
            
        Returns:
            bool: True if successful, False otherwise
        """
        if self._kek_generator.regenerate_kek(shards):
            # Generate a new random DEK
            self._dek = secrets.token_bytes(32)
            self._initialized = True
            return True
        return False

    @property
    def initialized(self) -> bool:
        """Whether the DEK is currently initialized"""
        return self._initialized

    @property
    def dek(self) -> bytes:
        """Get the current DEK"""
        if not self._initialized or not self._dek:
            raise RuntimeError("DEK not initialized")
        return self._dek

    @property
    def shards(self) -> list[str]:
        """Get the current KEK shards"""
        if not self._initialized:
            raise RuntimeError("DEK not initialized")
        return self._kek_generator.shards 