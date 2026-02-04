"""
Bitcoin mining algorithm representation and visualization data.
"""

from typing import List, Tuple, Generator
from dataclasses import dataclass
import hashlib
import struct


@dataclass
class AlgorithmStep:
    """Represents a single step in the SHA-256 algorithm."""
    name: str
    description: str
    operation: str
    values: List[str]


class SHA256Algorithm:
    """
    SHA-256 Algorithm representation for visualization.

    This class breaks down the SHA-256 algorithm into visual components
    that can be displayed in the GUI, showing how Bitcoin mining works.
    """

    # SHA-256 Constants (first 32 bits of fractional parts of cube roots of first 64 primes)
    K = [
        0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5,
        0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
        0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3,
        0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
        0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc,
        0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
        0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7,
        0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
        0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13,
        0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
        0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3,
        0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
        0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5,
        0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
        0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208,
        0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2
    ]

    # Initial hash values (first 32 bits of fractional parts of square roots of first 8 primes)
    H = [
        0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a,
        0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19
    ]

    def __init__(self):
        self.steps: List[AlgorithmStep] = []
        self._build_steps()

    def _build_steps(self):
        """Build the algorithm steps for visualization."""
        self.steps = [
            AlgorithmStep(
                name="1. Message Padding",
                description="Pad message to 512-bit blocks",
                operation="M' = M || 1 || 0^k || len(M)",
                values=["Block header (80 bytes)", "Padding bits", "Length (64 bits)"]
            ),
            AlgorithmStep(
                name="2. Parse Message",
                description="Break into 512-bit chunks",
                operation="M' → M₁, M₂, ..., Mₙ",
                values=["512-bit block 1", "512-bit block 2"]
            ),
            AlgorithmStep(
                name="3. Initialize Hash",
                description="Set initial hash values H₀-H₇",
                operation="H = [H₀, H₁, H₂, H₃, H₄, H₅, H₆, H₇]",
                values=[hex(h) for h in self.H]
            ),
            AlgorithmStep(
                name="4. Message Schedule",
                description="Expand 16 words to 64 words",
                operation="Wₜ = σ₁(Wₜ₋₂) + Wₜ₋₇ + σ₀(Wₜ₋₁₅) + Wₜ₋₁₆",
                values=["W₀-W₁₅: Direct from block", "W₁₆-W₆₃: Computed"]
            ),
            AlgorithmStep(
                name="5. Compression",
                description="64 rounds of mixing",
                operation="a,b,c,d,e,f,g,h = Round(a,b,c,d,e,f,g,h,Kₜ,Wₜ)",
                values=["Ch(e,f,g)", "Maj(a,b,c)", "Σ₀(a)", "Σ₁(e)"]
            ),
            AlgorithmStep(
                name="6. Add to Hash",
                description="Add compressed chunk to hash",
                operation="Hᵢ = Hᵢ + working_vars",
                values=["H₀+=a", "H₁+=b", "...", "H₇+=h"]
            ),
            AlgorithmStep(
                name="7. Final Hash",
                description="Concatenate hash values",
                operation="Hash = H₀ || H₁ || H₂ || H₃ || H₄ || H₅ || H₆ || H₇",
                values=["256-bit final hash"]
            ),
            AlgorithmStep(
                name="8. Double SHA-256",
                description="Bitcoin uses SHA256(SHA256(header))",
                operation="BlockHash = SHA256(SHA256(header))",
                values=["First hash", "Second hash = Block Hash"]
            )
        ]

    def get_steps(self) -> List[AlgorithmStep]:
        """Get all algorithm steps."""
        return self.steps

    def get_constants_for_wheel(self, wheel_index: int) -> List[int]:
        """
        Get constants to display on a specific wheel.

        Args:
            wheel_index: Which wheel (0-7 for 8 wheels)

        Returns:
            List of constants for that wheel
        """
        # Distribute K constants across wheels
        per_wheel = len(self.K) // 8
        start = wheel_index * per_wheel
        end = start + per_wheel
        return self.K[start:end]

    def get_rotation_angles(self) -> List[float]:
        """
        Get rotation angles derived from algorithm constants.

        Used to drive the wheel animations.
        """
        angles = []
        for k in self.K[:16]:
            angle = (k % 360)
            angles.append(angle)
        return angles

    def get_tree_connections(self) -> List[Tuple[int, int]]:
        """
        Get connections for the Tree of Life based on algorithm flow.

        Returns pairs of node indices that should be connected.
        """
        # Tree of Life has 10 nodes (Sephirot)
        # Map algorithm steps to tree paths
        connections = [
            (0, 1),  # Kether to Chokmah
            (0, 2),  # Kether to Binah
            (1, 3),  # Chokmah to Chesed
            (2, 4),  # Binah to Geburah
            (1, 4),  # Chokmah to Geburah
            (2, 3),  # Binah to Chesed
            (3, 5),  # Chesed to Tiphareth
            (4, 5),  # Geburah to Tiphareth
            (3, 6),  # Chesed to Netzach
            (4, 7),  # Geburah to Hod
            (5, 6),  # Tiphareth to Netzach
            (5, 7),  # Tiphareth to Hod
            (5, 8),  # Tiphareth to Yesod
            (6, 8),  # Netzach to Yesod
            (7, 8),  # Hod to Yesod
            (8, 9),  # Yesod to Malkuth
        ]
        return connections


class MiningAlgorithm:
    """
    Bitcoin mining process representation.

    Demonstrates how miners search for valid nonces.
    """

    def __init__(self, difficulty: int = 4):
        self.difficulty = difficulty
        self.target = "0" * difficulty
        self.attempts = 0
        self.found = False

    def mine_step(self, header: bytes, nonce: int) -> Tuple[str, bool]:
        """
        Perform one mining step.

        Args:
            header: 76-byte header (without nonce)
            nonce: Current nonce to try

        Returns:
            Tuple of (hash, is_valid)
        """
        full_header = header + struct.pack('<I', nonce)
        first_hash = hashlib.sha256(full_header).digest()
        second_hash = hashlib.sha256(first_hash).digest()
        hash_hex = second_hash[::-1].hex()

        is_valid = hash_hex.startswith(self.target)
        self.attempts += 1

        if is_valid:
            self.found = True

        return hash_hex, is_valid

    def get_mining_visualization_data(self) -> dict:
        """Get data for mining visualization."""
        return {
            'difficulty': self.difficulty,
            'target': self.target,
            'attempts': self.attempts,
            'found': self.found,
            'target_display': f"Hash must start with {self.difficulty} zeros"
        }

    def simulate_mining(self, max_attempts: int = 1000) -> Generator[dict, None, None]:
        """
        Simulate mining process yielding visualization data.

        Yields progress updates for animation.
        """
        import random

        # Create a sample header
        header = bytes(76)  # Simplified header

        for nonce in range(max_attempts):
            hash_result, is_valid = self.mine_step(header, nonce)

            yield {
                'nonce': nonce,
                'hash': hash_result,
                'valid': is_valid,
                'leading_zeros': len(hash_result) - len(hash_result.lstrip('0')),
                'progress': nonce / max_attempts
            }

            if is_valid:
                break
