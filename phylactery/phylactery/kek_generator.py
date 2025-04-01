"""
Module for generating and regenerating Key Encryption Keys using Shamir's Secret Sharing
"""

from shamir_mnemonic import ShamirMnemonic
import secrets

class KEKGenerator:
    def __init__(self):
        self._shamir = ShamirMnemonic()
        self._initialized = False
        self._shards = None
        self._kek = None

    def create_new_kek(self, quorum: int, total_shards: int) -> bool:
        """
        Create a new KEK with randomly generated shards
        
        Args:
            quorum: Number of shards required to reconstruct the KEK
            total_shards: Total number of shards to generate
            
        Returns:
            bool: True if successful, False otherwise
        """
        if quorum > total_shards:
            raise ValueError("Quorum cannot be greater than total shards")
        
        # Generate a random 32-byte (256-bit) KEK
        self._kek = secrets.token_bytes(32)
        
        # Generate shards using Shamir's Secret Sharing
        self._shards = self._shamir.split_secret(
            self._kek,
            quorum,
            total_shards
        )
        
        self._initialized = True
        return True

    def regenerate_kek(self, shards: list[str]) -> bool:
        """
        Regenerate a KEK from provided shards
        
        Args:
            shards: List of shard strings to use for reconstruction
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            self._kek = self._shamir.combine_shares(shards)
            self._initialized = True
            return True
        except Exception:
            self._initialized = False
            return False

    @property
    def initialized(self) -> bool:
        """Whether the KEK is currently initialized"""
        return self._initialized

    @property
    def shards(self) -> list[str]:
        """Get the current shards"""
        if not self._initialized or not self._shards:
            raise RuntimeError("KEK not initialized")
        return self._shards

    @property
    def kek(self) -> bytes:
        """Get the current KEK"""
        if not self._initialized or not self._kek:
            raise RuntimeError("KEK not initialized")
        return self._kek 