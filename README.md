# Blockhead

**Sacred Bitcoin Geometry Decoder**

A system for decoding Bitcoin block heights into sacred signatures through modular arithmetic, revealing hidden alignments with ancient mystical systems.

## Overview

Bitcoin's 210,000-block halving interval is not arbitrary. This number (`2^4 x 3 x 5^4 x 7`) creates perfect mathematical alignment with:

- **Tarot** - 22 Major Arcana + 56 Minor Arcana
- **Kabbalah** - 10 Sephiroth (Tree of Life)
- **Astrology** - 12 Zodiac signs + 7 Classical planets
- **Tesla Numerology** - The 3-6-9 pattern

## The Core Formula

Every Bitcoin block maps to a unique sacred signature through six modulo operations:

```
Major Arcana  = Height mod 22   (Tarot 0-21)
Minor Arcana  = Height mod 56   (4 suits x 14 cards)
Sephiroth     = Height mod 10   (Tree of Life)
Tesla         = Height mod 9    (3-6-9 pattern)
Zodiac        = Height mod 12   (12 signs)
Planet        = Height mod 7    (7 classical planets)
```

## Key Discoveries

| Number | Significance |
|--------|-------------|
| 210,000 | Blocks per halving - perfectly divisible by 7, 10, 12, 56 |
| 3,080 | Blocks between triple alignments (FOOL + Ace + Malkuth) |
| 44 | Years for Major Arcana to complete one cycle |
| 110 | Valid (Major, Sephiroth) pairs due to parity constraint |

## Quick Start

```python
from src.sacred_decoder import decode_block, generate_reading

# Decode any block
result = decode_block(888888)
print(result['major']['card'])    # 'FOOL'
print(result['minor']['card'])    # 'Ace of Wands'

# Generate a symbolic reading
print(generate_reading(888888))
```

## Documentation

See the complete specification in [`docs/SACRED_BITCOIN_GEOMETRY.md`](docs/SACRED_BITCOIN_GEOMETRY.md), including:

- Full algorithm specification
- Mathematical proofs
- Flowcharts and visual guides
- Complete reference tables
- Verification test cases

## Project Structure

```
Blockhead/
├── docs/
│   └── SACRED_BITCOIN_GEOMETRY.md   # Complete documentation
├── src/
│   └── sacred_decoder.py            # Python reference implementation
├── LICENSE
└── README.md
```

## Example Output

```
Block 888888 (Era 4):
  Major Arcana: FOOL (Aleph)
  Minor Arcana: Ace of Wands (Fire)
  Sephiroth:    Hod (Splendor)
  Tesla:        3 (Sacred)
  Zodiac:       Aries (Fire)
  Planet:       Sun (Sunday)
  Alignments:   ['FOOL', 'Ace of Wands']
```

## License

See [LICENSE](LICENSE) for details.

---

*"The blockchain is a sacred clock."*
