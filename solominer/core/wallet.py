"""
Bitcoin Wallet Generator Module
Generates and validates BTC wallets for solo mining
"""

import hashlib
import secrets
import binascii
from typing import Tuple, Optional
from dataclasses import dataclass


@dataclass
class WalletInfo:
    """Container for wallet information"""
    address: str
    private_key: str
    public_key: str
    mnemonic: str
    confirmed: bool = False


class WalletGenerator:
    """
    Bitcoin Wallet Generator
    Creates secure BTC wallets with mnemonic seed phrases
    """

    # BIP39 Word List (simplified - first 256 words for demo)
    WORDLIST = [
        "abandon", "ability", "able", "about", "above", "absent", "absorb", "abstract",
        "absurd", "abuse", "access", "accident", "account", "accuse", "achieve", "acid",
        "acoustic", "acquire", "across", "act", "action", "actor", "actress", "actual",
        "adapt", "add", "addict", "address", "adjust", "admit", "adult", "advance",
        "advice", "aerobic", "affair", "afford", "afraid", "again", "age", "agent",
        "agree", "ahead", "aim", "air", "airport", "aisle", "alarm", "album",
        "alcohol", "alert", "alien", "all", "alley", "allow", "almost", "alone",
        "alpha", "already", "also", "alter", "always", "amateur", "amazing", "among",
        "amount", "amused", "analyst", "anchor", "ancient", "anger", "angle", "angry",
        "animal", "ankle", "announce", "annual", "another", "answer", "antenna", "antique",
        "anxiety", "any", "apart", "apology", "appear", "apple", "approve", "april",
        "arch", "arctic", "area", "arena", "argue", "arm", "armed", "armor",
        "army", "around", "arrange", "arrest", "arrive", "arrow", "art", "artefact",
        "artist", "artwork", "ask", "aspect", "assault", "asset", "assist", "assume",
        "asthma", "athlete", "atom", "attack", "attend", "attitude", "attract", "auction",
        "audit", "august", "aunt", "author", "auto", "autumn", "average", "avocado",
        "avoid", "awake", "aware", "away", "awesome", "awful", "awkward", "axis",
        "baby", "bachelor", "bacon", "badge", "bag", "balance", "balcony", "ball",
        "bamboo", "banana", "banner", "bar", "barely", "bargain", "barrel", "base",
        "basic", "basket", "battle", "beach", "bean", "beauty", "because", "become",
        "beef", "before", "begin", "behave", "behind", "believe", "below", "belt",
        "bench", "benefit", "best", "betray", "better", "between", "beyond", "bicycle",
        "bid", "bike", "bind", "biology", "bird", "birth", "bitter", "black",
        "blade", "blame", "blanket", "blast", "bleak", "bless", "blind", "blood",
        "blossom", "blouse", "blue", "blur", "blush", "board", "boat", "body",
        "boil", "bomb", "bone", "bonus", "book", "boost", "border", "boring",
        "borrow", "boss", "bottom", "bounce", "box", "boy", "bracket", "brain",
        "brand", "brass", "brave", "bread", "breeze", "brick", "bridge", "brief",
        "bright", "bring", "brisk", "broccoli", "broken", "bronze", "broom", "brother",
        "brown", "brush", "bubble", "buddy", "budget", "buffalo", "build", "bulb",
        "bulk", "bullet", "bundle", "bunker", "burden", "burger", "burst", "bus",
        "business", "busy", "butter", "buyer", "buzz", "cabbage", "cabin", "cable",
    ]

    # Base58 alphabet for Bitcoin addresses
    BASE58_ALPHABET = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'

    def __init__(self):
        self.current_wallet: Optional[WalletInfo] = None

    def generate_entropy(self, bits: int = 128) -> bytes:
        """Generate cryptographically secure random entropy"""
        return secrets.token_bytes(bits // 8)

    def entropy_to_mnemonic(self, entropy: bytes) -> str:
        """Convert entropy to mnemonic phrase (BIP39 simplified)"""
        # Convert entropy to binary string
        h = hashlib.sha256(entropy).digest()
        b = bin(int.from_bytes(entropy + h[:1], 'big'))[2:].zfill(len(entropy) * 8 + 8)

        # Split into 11-bit chunks and map to words
        words = []
        for i in range(0, len(b) - 8, 11):
            idx = int(b[i:i+11], 2) % len(self.WORDLIST)
            words.append(self.WORDLIST[idx])

        return ' '.join(words[:12])  # Return 12-word mnemonic

    def mnemonic_to_seed(self, mnemonic: str, passphrase: str = "") -> bytes:
        """Convert mnemonic to seed using PBKDF2"""
        import hmac

        mnemonic_bytes = mnemonic.encode('utf-8')
        salt = ("mnemonic" + passphrase).encode('utf-8')

        # PBKDF2-HMAC-SHA512
        seed = hashlib.pbkdf2_hmac('sha512', mnemonic_bytes, salt, 2048, 64)
        return seed

    def generate_keypair(self, seed: bytes) -> Tuple[str, str]:
        """Generate private and public key pair from seed"""
        # Use first 32 bytes of seed as private key
        private_key = hashlib.sha256(seed[:32]).digest()

        # Generate public key (simplified - in production use ECDSA secp256k1)
        public_key = hashlib.sha256(private_key).digest() + hashlib.sha256(
            hashlib.sha256(private_key).digest()
        ).digest()[:1]

        return (
            binascii.hexlify(private_key).decode('ascii'),
            binascii.hexlify(public_key).decode('ascii')
        )

    def public_key_to_address(self, public_key_hex: str) -> str:
        """Convert public key to Bitcoin address"""
        public_key_bytes = binascii.unhexlify(public_key_hex)

        # SHA256 then RIPEMD160
        sha256_hash = hashlib.sha256(public_key_bytes).digest()
        ripemd160 = hashlib.new('ripemd160', sha256_hash).digest()

        # Add version byte (0x00 for mainnet)
        versioned = b'\x00' + ripemd160

        # Double SHA256 for checksum
        checksum = hashlib.sha256(hashlib.sha256(versioned).digest()).digest()[:4]

        # Encode in Base58
        address_bytes = versioned + checksum
        return self._base58_encode(address_bytes)

    def _base58_encode(self, data: bytes) -> str:
        """Encode bytes to Base58"""
        num = int.from_bytes(data, 'big')
        result = ''

        while num > 0:
            num, remainder = divmod(num, 58)
            result = self.BASE58_ALPHABET[remainder] + result

        # Handle leading zeros
        for byte in data:
            if byte == 0:
                result = '1' + result
            else:
                break

        return result

    def generate_wallet(self) -> WalletInfo:
        """Generate a complete new wallet"""
        # Generate entropy and mnemonic
        entropy = self.generate_entropy()
        mnemonic = self.entropy_to_mnemonic(entropy)

        # Generate seed from mnemonic
        seed = self.mnemonic_to_seed(mnemonic)

        # Generate key pair
        private_key, public_key = self.generate_keypair(seed)

        # Generate address
        address = self.public_key_to_address(public_key)

        self.current_wallet = WalletInfo(
            address=address,
            private_key=private_key,
            public_key=public_key,
            mnemonic=mnemonic,
            confirmed=False
        )

        return self.current_wallet

    def confirm_wallet(self) -> bool:
        """Confirm the current wallet for use"""
        if self.current_wallet:
            self.current_wallet.confirmed = True
            return True
        return False

    def validate_address(self, address: str) -> bool:
        """Validate a Bitcoin address format"""
        if not address:
            return False

        # Check length
        if len(address) < 26 or len(address) > 35:
            return False

        # Check starts with valid prefix
        if not (address.startswith('1') or address.startswith('3') or
                address.startswith('bc1')):
            return False

        # Check valid Base58 characters (for legacy addresses)
        if not address.startswith('bc1'):
            for char in address:
                if char not in self.BASE58_ALPHABET:
                    return False

        return True

    def get_wallet_info_display(self) -> dict:
        """Get wallet info formatted for display"""
        if not self.current_wallet:
            return {}

        return {
            "Address": self.current_wallet.address,
            "Public Key": f"{self.current_wallet.public_key[:16]}...{self.current_wallet.public_key[-16:]}",
            "Mnemonic": self.current_wallet.mnemonic,
            "Status": "Confirmed" if self.current_wallet.confirmed else "Pending Confirmation"
        }
