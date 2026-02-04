"""
BTC Block data structure representing a Bitcoin block.
"""

import hashlib
import time
import struct
from typing import Optional, List
from dataclasses import dataclass, field


@dataclass
class BTCBlock:
    """
    Represents a Bitcoin block with all its components.

    The block structure follows the Bitcoin protocol specification:
    - Version: Block version number
    - Previous Block Hash: 256-bit hash of the previous block header
    - Merkle Root: 256-bit hash derived from all transactions in the block
    - Timestamp: Current block timestamp as seconds since 1970-01-01T00:00 UTC
    - Bits: Current target in compact format
    - Nonce: 32-bit number that miners vary to find valid hash
    """

    version: int = 1
    prev_block_hash: str = "0" * 64
    merkle_root: str = "0" * 64
    timestamp: int = field(default_factory=lambda: int(time.time()))
    bits: int = 0x1d00ffff  # Difficulty target
    nonce: int = 0

    # Block data
    transactions: List[str] = field(default_factory=list)
    block_hash: Optional[str] = None

    def __post_init__(self):
        """Calculate block hash after initialization."""
        if self.block_hash is None:
            self.block_hash = self.calculate_hash()

    def get_header_bytes(self) -> bytes:
        """
        Get the 80-byte block header.

        The header consists of:
        - 4 bytes: version
        - 32 bytes: previous block hash
        - 32 bytes: merkle root
        - 4 bytes: timestamp
        - 4 bytes: bits (difficulty)
        - 4 bytes: nonce
        """
        header = struct.pack('<I', self.version)
        header += bytes.fromhex(self.prev_block_hash)[::-1]  # Little-endian
        header += bytes.fromhex(self.merkle_root)[::-1]  # Little-endian
        header += struct.pack('<I', self.timestamp)
        header += struct.pack('<I', self.bits)
        header += struct.pack('<I', self.nonce)
        return header

    def calculate_hash(self) -> str:
        """
        Calculate the block hash using double SHA-256.

        Bitcoin uses SHA256(SHA256(header)) for block hashing.
        """
        header = self.get_header_bytes()
        first_hash = hashlib.sha256(header).digest()
        second_hash = hashlib.sha256(first_hash).digest()
        return second_hash[::-1].hex()  # Reverse for display

    def mine(self, target_zeros: int = 4, max_nonce: int = 2**32) -> bool:
        """
        Simple mining simulation - find a nonce that produces a hash
        starting with the specified number of zeros.

        Args:
            target_zeros: Number of leading zeros required
            max_nonce: Maximum nonce value to try

        Returns:
            True if valid nonce found, False otherwise
        """
        target = "0" * target_zeros

        for nonce in range(max_nonce):
            self.nonce = nonce
            self.block_hash = self.calculate_hash()

            if self.block_hash.startswith(target):
                return True

            if nonce % 100000 == 0:
                yield nonce, self.block_hash

        return False

    def get_rotation_data(self) -> List[int]:
        """
        Get block data as rotation values for visualization.

        Converts the block hash into rotation angles for the GUI.
        """
        if not self.block_hash:
            return [0] * 32

        # Convert hash to bytes and then to rotation values
        hash_bytes = bytes.fromhex(self.block_hash)
        rotations = [(b / 255.0) * 360 for b in hash_bytes]
        return rotations

    def get_wheel_speeds(self) -> List[float]:
        """
        Get wheel speeds derived from block components.

        Each component of the block influences different wheel speeds.
        """
        speeds = []

        # Version influences base speed
        speeds.append((self.version % 10) * 0.5 + 0.5)

        # Nonce influences inner wheels
        nonce_bytes = struct.pack('<I', self.nonce)
        for b in nonce_bytes:
            speeds.append((b / 255.0) * 2 + 0.5)

        # Timestamp influences outer wheels
        ts_bytes = struct.pack('<I', self.timestamp)
        for b in ts_bytes:
            speeds.append((b / 255.0) * 1.5 + 0.3)

        # Difficulty influences middle wheels
        speeds.append((self.bits % 256) / 255.0 * 2 + 0.5)

        return speeds[:10]  # Return 10 wheel speeds

    def to_dict(self) -> dict:
        """Convert block to dictionary representation."""
        return {
            'version': self.version,
            'prev_block_hash': self.prev_block_hash,
            'merkle_root': self.merkle_root,
            'timestamp': self.timestamp,
            'bits': hex(self.bits),
            'nonce': self.nonce,
            'block_hash': self.block_hash,
            'transactions': len(self.transactions)
        }

    def __str__(self) -> str:
        return f"BTCBlock(hash={self.block_hash[:16]}..., nonce={self.nonce})"

    @classmethod
    def create_genesis(cls) -> 'BTCBlock':
        """Create a genesis block (first block in chain)."""
        return cls(
            version=1,
            prev_block_hash="0" * 64,
            merkle_root="4a5e1e4baab89f3a32518a88c31bc87f618f76673e2cc77ab2127b7afdeda33b",
            timestamp=1231006505,  # Bitcoin genesis timestamp
            bits=0x1d00ffff,
            nonce=2083236893
        )
