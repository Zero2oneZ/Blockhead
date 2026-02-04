"""
Solo Mining Core Module
Implements Bitcoin mining algorithms with difficulty levels 0-12
"""

import hashlib
import time
import random
import threading
from typing import Optional, Callable, Dict, Any
from dataclasses import dataclass, field
from enum import Enum


class MiningState(Enum):
    """Mining operation states"""
    IDLE = "idle"
    INITIALIZING = "initializing"
    MINING = "mining"
    PAUSED = "paused"
    BLOCK_FOUND = "block_found"
    STOPPED = "stopped"


@dataclass
class MiningStats:
    """Statistics for mining operation"""
    hashrate: float = 0.0
    total_hashes: int = 0
    blocks_found: int = 0
    current_difficulty: int = 0
    start_time: float = 0.0
    elapsed_time: float = 0.0
    current_nonce: int = 0
    best_hash: str = ""
    best_hash_zeros: int = 0
    estimated_time_to_block: str = "Calculating..."


@dataclass
class MiningAlgorithm:
    """Mining algorithm configuration"""
    name: str
    description: str
    difficulty_level: int
    target_zeros: int
    hash_function: str = "sha256d"
    extra_params: Dict[str, Any] = field(default_factory=dict)


class SoloMiner:
    """
    Bitcoin Solo Miner
    Supports difficulty levels 0-12 with visual feedback
    """

    # Mining algorithm configurations for levels 0-12
    # Probability of N zeros: (1/16)^N
    # 4 zeros = 1 in 65,536 | 5 zeros = 1 in 1M | 6 zeros = 1 in 16M | 7 zeros = 1 in 268M
    ALGORITHMS = {
        0: MiningAlgorithm("Demo Mode", "Instant results for testing", 0, 1),          # 1 in 16
        1: MiningAlgorithm("Beginner", "Very easy - quick blocks", 1, 2),              # 1 in 256
        2: MiningAlgorithm("Easy", "Low difficulty", 2, 2),                             # 1 in 256
        3: MiningAlgorithm("Light", "Light load", 3, 3),                                # 1 in 4,096
        4: MiningAlgorithm("Standard", "Standard mining", 4, 3),                        # 1 in 4,096
        5: MiningAlgorithm("Moderate", "Moderate challenge", 5, 4),                     # 1 in 65,536
        6: MiningAlgorithm("Intermediate", "Intermediate", 6, 4),                       # 1 in 65,536
        7: MiningAlgorithm("Advanced", "Advanced - 5 zeros", 7, 5),                     # 1 in 1,048,576
        8: MiningAlgorithm("Expert", "Expert - 5 zeros", 8, 5),                         # 1 in 1,048,576
        9: MiningAlgorithm("Professional", "Pro - 6 zeros", 9, 6),                      # 1 in 16,777,216
        10: MiningAlgorithm("Extreme", "Extreme - 6 zeros", 10, 6),                     # 1 in 16,777,216
        11: MiningAlgorithm("Ultra", "Ultra - 7 zeros (your record!)", 11, 7),         # 1 in 268,435,456
        12: MiningAlgorithm("Maximum", "Maximum - 8 zeros", 12, 8),                     # 1 in 4,294,967,296
    }

    def __init__(self, wallet_address: str = ""):
        self.wallet_address = wallet_address
        self.state = MiningState.IDLE
        self.stats = MiningStats()
        self.current_algorithm: Optional[MiningAlgorithm] = None
        self._mining_thread: Optional[threading.Thread] = None
        self._stop_event = threading.Event()
        self._pause_event = threading.Event()
        self._callbacks: Dict[str, Callable] = {}

        # Block template (simulated)
        self.block_template = {
            "version": 0x20000000,
            "prev_block": "0" * 64,
            "merkle_root": "",
            "timestamp": 0,
            "bits": 0,
            "nonce": 0
        }

    def register_callback(self, event: str, callback: Callable):
        """Register callback for mining events"""
        self._callbacks[event] = callback

    def _emit(self, event: str, data: Any = None):
        """Emit event to registered callbacks"""
        if event in self._callbacks:
            try:
                self._callbacks[event](data)
            except Exception as e:
                print(f"Callback error: {e}")

    def set_difficulty(self, level: int) -> MiningAlgorithm:
        """Set mining difficulty level (0-12)"""
        if level < 0:
            level = 0
        elif level > 12:
            level = 12

        self.current_algorithm = self.ALGORITHMS[level]
        self.stats.current_difficulty = level
        self._emit("difficulty_changed", self.current_algorithm)
        return self.current_algorithm

    def get_algorithm_info(self, level: int) -> Dict[str, Any]:
        """Get information about a specific algorithm level"""
        algo = self.ALGORITHMS.get(level)
        if not algo:
            return {}

        return {
            "level": level,
            "name": algo.name,
            "description": algo.description,
            "target_zeros": algo.target_zeros,
            "estimated_hashes": 16 ** algo.target_zeros,
            "hash_function": algo.hash_function
        }

    def _double_sha256(self, data: bytes) -> bytes:
        """Perform double SHA256 hash (Bitcoin standard)"""
        return hashlib.sha256(hashlib.sha256(data).digest()).digest()

    def _create_block_header(self, nonce: int) -> bytes:
        """Create a block header for hashing"""
        # Simulated block header construction
        header = (
            self.block_template["version"].to_bytes(4, 'little') +
            bytes.fromhex(self.block_template["prev_block"])[::-1] +
            bytes.fromhex(self.block_template["merkle_root"])[::-1] +
            self.block_template["timestamp"].to_bytes(4, 'little') +
            self.block_template["bits"].to_bytes(4, 'little') +
            nonce.to_bytes(4, 'little')
        )
        return header

    def _check_hash_meets_target(self, hash_result: str, target_zeros: int) -> bool:
        """Check if hash meets the target difficulty"""
        return hash_result.startswith('0' * target_zeros)

    def _update_block_template(self):
        """Update block template with fresh data"""
        self.block_template["timestamp"] = int(time.time())
        self.block_template["merkle_root"] = hashlib.sha256(
            (self.wallet_address + str(time.time())).encode()
        ).hexdigest()
        self.block_template["prev_block"] = hashlib.sha256(
            str(random.random()).encode()
        ).hexdigest()
        self.block_template["bits"] = 0x1d00ffff  # Standard difficulty bits

    def _mining_loop(self):
        """Main mining loop executed in separate thread"""
        self.stats.start_time = time.time()
        self.stats.total_hashes = 0
        nonce = 0
        last_update_time = time.time()
        hashes_since_update = 0

        target_zeros = self.current_algorithm.target_zeros if self.current_algorithm else 4

        self._emit("mining_started", {"algorithm": self.current_algorithm})

        while not self._stop_event.is_set():
            # Check for pause
            if self._pause_event.is_set():
                self.state = MiningState.PAUSED
                self._emit("mining_paused", None)
                while self._pause_event.is_set() and not self._stop_event.is_set():
                    time.sleep(0.1)
                if not self._stop_event.is_set():
                    self.state = MiningState.MINING
                    self._emit("mining_resumed", None)
                continue

            # Create hash input
            data = f"{self.wallet_address}{nonce}{time.time_ns()}".encode()
            hash_result = self._double_sha256(data).hex()

            # Update statistics
            self.stats.total_hashes += 1
            self.stats.current_nonce = nonce
            hashes_since_update += 1

            # Count leading zeros
            zeros = len(hash_result) - len(hash_result.lstrip('0'))
            if zeros > self.stats.best_hash_zeros:
                self.stats.best_hash = hash_result
                self.stats.best_hash_zeros = zeros
                self._emit("new_best_hash", {
                    "hash": hash_result,
                    "zeros": zeros,
                    "nonce": nonce
                })

            # Check if we found a valid block
            if self._check_hash_meets_target(hash_result, target_zeros):
                self.stats.blocks_found += 1
                self.state = MiningState.BLOCK_FOUND
                self._emit("block_found", {
                    "hash": hash_result,
                    "nonce": nonce,
                    "difficulty": target_zeros,
                    "total_hashes": self.stats.total_hashes
                })

                # Continue mining after block found
                self._update_block_template()
                self.state = MiningState.MINING

            # Update hashrate every 0.5 seconds
            current_time = time.time()
            if current_time - last_update_time >= 0.5:
                elapsed = current_time - last_update_time
                self.stats.hashrate = hashes_since_update / elapsed
                self.stats.elapsed_time = current_time - self.stats.start_time

                # Estimate time to block
                if self.stats.hashrate > 0:
                    expected_hashes = 16 ** target_zeros
                    seconds_to_block = expected_hashes / self.stats.hashrate
                    if seconds_to_block < 60:
                        self.stats.estimated_time_to_block = f"{seconds_to_block:.0f}s"
                    elif seconds_to_block < 3600:
                        self.stats.estimated_time_to_block = f"{seconds_to_block/60:.1f}m"
                    elif seconds_to_block < 86400:
                        self.stats.estimated_time_to_block = f"{seconds_to_block/3600:.1f}h"
                    else:
                        self.stats.estimated_time_to_block = f"{seconds_to_block/86400:.1f}d"

                self._emit("stats_update", self.stats)

                hashes_since_update = 0
                last_update_time = current_time

            nonce += 1

            # Small delay to prevent CPU overload in demo
            if target_zeros <= 2:
                time.sleep(0.001)

        self.state = MiningState.STOPPED
        self._emit("mining_stopped", self.stats)

    def start_mining(self, difficulty_level: int = 4) -> bool:
        """Start mining operation"""
        if self.state == MiningState.MINING:
            return False

        if not self.wallet_address:
            self._emit("error", "No wallet address configured")
            return False

        self.set_difficulty(difficulty_level)
        self._update_block_template()

        self._stop_event.clear()
        self._pause_event.clear()
        self.state = MiningState.INITIALIZING

        self._emit("initializing", {
            "wallet": self.wallet_address,
            "difficulty": difficulty_level,
            "algorithm": self.current_algorithm.name if self.current_algorithm else "Unknown"
        })

        # Start mining thread
        self._mining_thread = threading.Thread(target=self._mining_loop, daemon=True)
        self._mining_thread.start()
        self.state = MiningState.MINING

        return True

    def stop_mining(self):
        """Stop mining operation"""
        self._stop_event.set()
        if self._mining_thread:
            self._mining_thread.join(timeout=2.0)
        self.state = MiningState.STOPPED

    def pause_mining(self):
        """Pause mining operation"""
        self._pause_event.set()

    def resume_mining(self):
        """Resume mining operation"""
        self._pause_event.clear()

    def get_stats(self) -> MiningStats:
        """Get current mining statistics"""
        return self.stats

    def get_state(self) -> MiningState:
        """Get current mining state"""
        return self.state

    @staticmethod
    def get_all_algorithms() -> Dict[int, Dict[str, Any]]:
        """Get information about all available algorithms"""
        return {
            level: {
                "name": algo.name,
                "description": algo.description,
                "target_zeros": algo.target_zeros
            }
            for level, algo in SoloMiner.ALGORITHMS.items()
        }
