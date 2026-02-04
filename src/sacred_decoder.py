#!/usr/bin/env python3
"""
SACRED BITCOIN DECODER
Complete Reference Implementation

This module implements the Sacred Bitcoin Geometry decoding system,
which maps Bitcoin block heights to various mystical systems through
modular arithmetic.

Systems mapped:
    - Tarot (Major & Minor Arcana)
    - Kabbalah (Tree of Life / Sephiroth)
    - Astrology (Zodiac & Planets)
    - Tesla Numerology (3-6-9)

Author: Tom & Claude
Version: 1.0
Date: February 2026
"""

from typing import Dict, List, Any, Optional


# =============================================================================
# CONSTANTS
# =============================================================================

# Major Arcana - The Fool's Journey (22 cards)
TAROT_MAJOR = [
    'FOOL', 'MAGICIAN', 'HIGH PRIESTESS', 'EMPRESS', 'EMPEROR', 'HIEROPHANT',
    'LOVERS', 'CHARIOT', 'STRENGTH', 'HERMIT', 'WHEEL OF FORTUNE', 'JUSTICE',
    'HANGED MAN', 'DEATH', 'TEMPERANCE', 'DEVIL', 'TOWER', 'STAR',
    'MOON', 'SUN', 'JUDGEMENT', 'WORLD'
]

# Hebrew letters corresponding to Major Arcana
HEBREW_LETTERS = [
    'Aleph', 'Beth', 'Gimel', 'Daleth', 'He', 'Vav', 'Zayin', 'Cheth',
    'Teth', 'Yod', 'Kaph', 'Lamed', 'Mem', 'Nun', 'Samekh', 'Ayin',
    'Pe', 'Tzaddi', 'Qoph', 'Resh', 'Shin', 'Tav'
]

# Minor Arcana suits (14 cards each, 56 total)
SUITS = ['Wands', 'Cups', 'Swords', 'Pentacles']
ELEMENTS = ['Fire', 'Water', 'Air', 'Earth']
RANKS = ['Ace', '2', '3', '4', '5', '6', '7', '8', '9', '10',
         'Page', 'Knight', 'Queen', 'King']

# Sephiroth - Tree of Life (10 spheres)
SEPHIROTH = [
    'Malkuth', 'Kether', 'Chokmah', 'Binah', 'Chesed',
    'Geburah', 'Tiphareth', 'Netzach', 'Hod', 'Yesod'
]
SEPH_MEANINGS = [
    'Kingdom', 'Crown', 'Wisdom', 'Understanding', 'Mercy',
    'Severity', 'Beauty', 'Victory', 'Splendor', 'Foundation'
]

# Zodiac signs (12 signs)
ZODIAC = [
    'Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo',
    'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces'
]
ZODIAC_ELEMENTS = [
    'Fire', 'Earth', 'Air', 'Water', 'Fire', 'Earth',
    'Air', 'Water', 'Fire', 'Earth', 'Air', 'Water'
]
ZODIAC_QUALITIES = [
    'Cardinal', 'Fixed', 'Mutable', 'Cardinal', 'Fixed', 'Mutable',
    'Cardinal', 'Fixed', 'Mutable', 'Cardinal', 'Fixed', 'Mutable'
]

# Classical planets (7 luminaries)
PLANETS = ['Sun', 'Moon', 'Mercury', 'Venus', 'Mars', 'Jupiter', 'Saturn']
DAYS = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
METALS = ['Gold', 'Silver', 'Mercury', 'Copper', 'Iron', 'Tin', 'Lead']

# Key constants
HALVING_INTERVAL = 210000
TRIPLE_ALIGNMENT_CYCLE = 3080
MAJOR_ARCANA_ROTATION = 44  # years


# =============================================================================
# CORE FUNCTIONS
# =============================================================================

def decode_block(height: int) -> Dict[str, Any]:
    """
    Decode a block height into its sacred signature.

    Args:
        height: Block height (non-negative integer)

    Returns:
        Dictionary containing all sacred cycle positions and meanings

    Example:
        >>> result = decode_block(888888)
        >>> result['major']['card']
        'FOOL'
        >>> result['minor']['card']
        'Ace of Wands'
    """
    if height < 0:
        raise ValueError("Block height must be non-negative")

    # Major Arcana (mod 22)
    major_pos = height % 22

    # Minor Arcana (mod 56)
    minor_pos = height % 56
    suit_idx = minor_pos // 14
    rank_idx = minor_pos % 14

    # Sephiroth (mod 10)
    seph_pos = height % 10

    # Tesla (mod 9)
    tesla_pos = height % 9

    # Zodiac (mod 12)
    zodiac_pos = height % 12

    # Planet (mod 7)
    planet_pos = height % 7

    # Check alignments
    alignments = []
    if major_pos == 0:
        alignments.append('FOOL')
    if minor_pos == 0:
        alignments.append('Ace of Wands')
    if seph_pos == 0:
        alignments.append('Malkuth')

    # Validate parity constraint (should always be true)
    parity_valid = (major_pos % 2) == (seph_pos % 2)

    return {
        'height': height,
        'era': height // HALVING_INTERVAL,
        'major': {
            'position': major_pos,
            'card': TAROT_MAJOR[major_pos],
            'hebrew': HEBREW_LETTERS[major_pos]
        },
        'minor': {
            'position': minor_pos,
            'card': f"{RANKS[rank_idx]} of {SUITS[suit_idx]}",
            'suit': SUITS[suit_idx],
            'rank': RANKS[rank_idx],
            'element': ELEMENTS[suit_idx]
        },
        'sephiroth': {
            'position': seph_pos,
            'name': SEPHIROTH[seph_pos],
            'meaning': SEPH_MEANINGS[seph_pos]
        },
        'tesla': {
            'position': tesla_pos,
            'sacred': tesla_pos in [0, 3, 6]
        },
        'zodiac': {
            'position': zodiac_pos,
            'sign': ZODIAC[zodiac_pos],
            'element': ZODIAC_ELEMENTS[zodiac_pos],
            'quality': ZODIAC_QUALITIES[zodiac_pos]
        },
        'planet': {
            'position': planet_pos,
            'name': PLANETS[planet_pos],
            'day': DAYS[planet_pos],
            'metal': METALS[planet_pos]
        },
        'alignments': alignments,
        'alignment_count': len(alignments),
        'parity_valid': parity_valid
    }


def decode_nonce(nonce: int) -> Dict[str, Any]:
    """
    Decode a nonce into its sacred signature.

    Args:
        nonce: Block nonce (32-bit unsigned integer, 0 to 4,294,967,295)

    Returns:
        Dictionary containing nonce decode information

    Example:
        >>> result = decode_nonce(217777604)
        >>> result['bacon']
        'SIOQFS'
        >>> result['crown']
        4
    """
    if nonce < 0:
        raise ValueError("Nonce must be non-negative")

    # Bacon cipher (base-26)
    bacon = bacon_encode(nonce)

    # Card mapping
    nonce_major = nonce % 22
    nonce_seph = nonce % 10

    # Crown value
    crown = (nonce_major + nonce_seph) % 10

    # Digital root
    dr = digital_root(nonce)

    return {
        'nonce': nonce,
        'hex': f"0x{nonce:08X}",
        'bacon': bacon,
        'card': {
            'position': nonce_major,
            'name': TAROT_MAJOR[nonce_major]
        },
        'sphere': {
            'position': nonce_seph,
            'name': SEPHIROTH[nonce_seph]
        },
        'crown': crown,
        'digital_root': dr,
        'signature': f"{bacon}:{crown}:{dr}"
    }


def bacon_encode(n: int) -> str:
    """
    Convert integer to base-26 letter encoding (Bacon cipher).

    Args:
        n: Non-negative integer

    Returns:
        String of uppercase letters A-Z

    Example:
        >>> bacon_encode(217777604)
        'SIOQFS'
    """
    if n == 0:
        return 'A'
    result = []
    while n > 0:
        result.append(chr(ord('A') + (n % 26)))
        n //= 26
    return ''.join(reversed(result))


def digital_root(n: int) -> int:
    """
    Calculate the digital root (repeated digit sum until single digit).

    Args:
        n: Non-negative integer

    Returns:
        Single digit 0-9

    Example:
        >>> digital_root(217777604)
        5
    """
    while n >= 10:
        n = sum(int(d) for d in str(n))
    return n


# =============================================================================
# ALIGNMENT FUNCTIONS
# =============================================================================

def predict_next_alignment(height: int, alignment_type: str = 'triple') -> int:
    """
    Predict the next alignment block.

    Args:
        height: Current block height
        alignment_type: 'triple', 'fool', 'ace', or 'malkuth'

    Returns:
        Block height of next alignment

    Example:
        >>> predict_next_alignment(100, 'fool')
        110
    """
    cycles = {
        'triple': TRIPLE_ALIGNMENT_CYCLE,
        'fool': 22,
        'ace': 56,
        'malkuth': 10
    }

    cycle = cycles.get(alignment_type, TRIPLE_ALIGNMENT_CYCLE)
    current_pos = height % cycle
    blocks_until = (cycle - current_pos) % cycle

    if blocks_until == 0:
        blocks_until = cycle

    return height + blocks_until


def find_alignments_in_range(start: int, end: int,
                              alignment_type: str = 'triple') -> List[int]:
    """
    Find all alignment blocks within a range.

    Args:
        start: Start block height (inclusive)
        end: End block height (exclusive)
        alignment_type: 'triple', 'fool', 'ace', or 'malkuth'

    Returns:
        List of block heights with alignments

    Example:
        >>> find_alignments_in_range(0, 100, 'fool')
        [0, 22, 44, 66, 88]
    """
    cycles = {
        'triple': TRIPLE_ALIGNMENT_CYCLE,
        'fool': 22,
        'ace': 56,
        'malkuth': 10
    }

    cycle = cycles.get(alignment_type, TRIPLE_ALIGNMENT_CYCLE)
    first_alignment = (start // cycle) * cycle
    if first_alignment < start:
        first_alignment += cycle

    alignments = []
    current = first_alignment
    while current < end:
        alignments.append(current)
        current += cycle

    return alignments


def count_triple_alignments_per_halving() -> int:
    """
    Calculate the number of triple alignments per halving interval.

    Returns:
        Number of triple alignments (68)
    """
    return HALVING_INTERVAL // TRIPLE_ALIGNMENT_CYCLE


# =============================================================================
# HALVING FUNCTIONS
# =============================================================================

def get_halving_signature(era: int) -> Dict[str, Any]:
    """
    Get the sacred signature for a halving block.

    Args:
        era: Halving era number (0 = genesis, 1 = first halving, etc.)

    Returns:
        Dictionary with halving block signature

    Example:
        >>> sig = get_halving_signature(0)
        >>> sig['major']['card']
        'FOOL'
    """
    height = era * HALVING_INTERVAL
    return decode_block(height)


def get_major_at_halving(era: int) -> str:
    """
    Get the Major Arcana card at a specific halving.

    The Major Arcana advances by 10 positions each halving:
    Era 0: FOOL (0), Era 1: WHEEL (10), Era 2: JUDGEMENT (20),
    Era 3: STRENGTH (8), etc.

    Args:
        era: Halving era number

    Returns:
        Name of Major Arcana card

    Example:
        >>> get_major_at_halving(0)
        'FOOL'
        >>> get_major_at_halving(1)
        'WHEEL OF FORTUNE'
    """
    position = (era * 10) % 22
    return TAROT_MAJOR[position]


def get_tesla_at_halving(era: int) -> int:
    """
    Get the Tesla position at a specific halving.

    Tesla advances by 3 each halving: 0 -> 3 -> 6 -> 0 -> ...

    Args:
        era: Halving era number

    Returns:
        Tesla position (0, 3, or 6)
    """
    return (era * 3) % 9


# =============================================================================
# READING GENERATION
# =============================================================================

def generate_reading(height: int) -> str:
    """
    Generate a symbolic reading for a block.

    Args:
        height: Block height

    Returns:
        Poetic reading string

    Example:
        >>> print(generate_reading(888888))
        "FOOL walks the path of Hod,
         wielding the Ace of Wands (Fire),
         under Aries on Sunday."
    """
    d = decode_block(height)

    reading = (
        f'"{d["major"]["card"]} walks the path of {d["sephiroth"]["name"]},\n'
        f' wielding the {d["minor"]["card"]} ({d["minor"]["element"]}),\n'
        f' under {d["zodiac"]["sign"]} on {d["planet"]["day"]}."'
    )

    if d['tesla']['sacred']:
        reading += f'\n [Tesla Sacred: position {d["tesla"]["position"]}]'

    if d['alignment_count'] > 0:
        reading += f'\n [Alignments: {", ".join(d["alignments"])}]'

    return reading


def format_signature(height: int) -> str:
    """
    Format a block's sacred signature as a compact string.

    Args:
        height: Block height

    Returns:
        Compact signature string

    Example:
        >>> format_signature(888888)
        'FOOL:Hod:Ace of Wands:Aries:Sun'
    """
    d = decode_block(height)
    return (
        f'{d["major"]["card"]}:'
        f'{d["sephiroth"]["name"]}:'
        f'{d["minor"]["card"]}:'
        f'{d["zodiac"]["sign"]}:'
        f'{d["planet"]["name"]}'
    )


# =============================================================================
# VERIFICATION FUNCTIONS
# =============================================================================

def verify_parity_constraint(start: int = 0, end: int = 1000000) -> bool:
    """
    Verify that the parity constraint holds for a range of blocks.

    The parity constraint states that Major Arcana position and
    Sephiroth position always have the same parity (both even or both odd).

    Args:
        start: Start of range
        end: End of range

    Returns:
        True if constraint holds for all blocks in range
    """
    for height in range(start, end):
        major_parity = (height % 22) % 2
        seph_parity = (height % 10) % 2
        if major_parity != seph_parity:
            return False
    return True


def run_test_cases() -> Dict[str, bool]:
    """
    Run verification test cases from the specification.

    Returns:
        Dictionary of test names to pass/fail status
    """
    results = {}

    # Test 1: Genesis Block
    d = decode_block(0)
    results['genesis_major'] = d['major']['card'] == 'FOOL'
    results['genesis_minor'] = d['minor']['card'] == 'Ace of Wands'
    results['genesis_seph'] = d['sephiroth']['name'] == 'Malkuth'
    results['genesis_tesla'] = d['tesla']['sacred'] and d['tesla']['position'] == 0
    results['genesis_zodiac'] = d['zodiac']['sign'] == 'Aries'
    results['genesis_planet'] = d['planet']['name'] == 'Sun'
    results['genesis_alignments'] = d['alignment_count'] == 3

    # Test 2: First Halving
    d = decode_block(210000)
    results['halving1_major'] = d['major']['card'] == 'WHEEL OF FORTUNE'
    results['halving1_minor'] = d['minor']['card'] == 'Ace of Wands'
    results['halving1_seph'] = d['sephiroth']['name'] == 'Malkuth'
    results['halving1_alignments'] = d['alignment_count'] == 2

    # Test 3: Parity Constraint (sample)
    results['parity_constraint'] = verify_parity_constraint(0, 10000)

    # Test 4: Triple Alignment Frequency
    triple_count = len(find_alignments_in_range(0, 210000, 'triple'))
    results['triple_frequency'] = triple_count == 68

    # Test 5: Special Number 888888
    d = decode_block(888888)
    results['888888_major'] = d['major']['card'] == 'FOOL'
    results['888888_minor'] = d['minor']['card'] == 'Ace of Wands'
    results['888888_seph'] = d['sephiroth']['name'] == 'Hod'
    results['888888_tesla'] = d['tesla']['sacred'] and d['tesla']['position'] == 3
    results['888888_alignments'] = d['alignment_count'] == 2

    return results


# =============================================================================
# MAIN ENTRY POINT
# =============================================================================

def main():
    """Main entry point for demonstration."""
    print("=" * 70)
    print("SACRED BITCOIN GEOMETRY DECODER")
    print("=" * 70)
    print()

    # Example: Decode a block
    print("BLOCK DECODE EXAMPLE")
    print("-" * 70)
    block = decode_block(888888)
    print(f"Block {block['height']} (Era {block['era']}):")
    print(f"  Major Arcana: {block['major']['card']} ({block['major']['hebrew']})")
    print(f"  Minor Arcana: {block['minor']['card']} ({block['minor']['element']})")
    print(f"  Sephiroth:    {block['sephiroth']['name']} ({block['sephiroth']['meaning']})")
    print(f"  Tesla:        {block['tesla']['position']} ({'Sacred' if block['tesla']['sacred'] else 'Normal'})")
    print(f"  Zodiac:       {block['zodiac']['sign']} ({block['zodiac']['element']})")
    print(f"  Planet:       {block['planet']['name']} ({block['planet']['day']})")
    print(f"  Alignments:   {block['alignments']} (count: {block['alignment_count']})")
    print(f"  Parity Valid: {block['parity_valid']}")
    print()

    # Example: Decode a nonce
    print("NONCE DECODE EXAMPLE")
    print("-" * 70)
    nonce_data = decode_nonce(217777604)
    print(f"Nonce {nonce_data['nonce']} ({nonce_data['hex']}):")
    print(f"  Bacon Cipher:  {nonce_data['bacon']}")
    print(f"  Card:          {nonce_data['card']['name']}")
    print(f"  Sphere:        {nonce_data['sphere']['name']}")
    print(f"  Crown:         {nonce_data['crown']}")
    print(f"  Digital Root:  {nonce_data['digital_root']}")
    print(f"  Signature:     {nonce_data['signature']}")
    print()

    # Example: Generate reading
    print("SYMBOLIC READING")
    print("-" * 70)
    print(generate_reading(888888))
    print()

    # Run tests
    print("VERIFICATION TESTS")
    print("-" * 70)
    results = run_test_cases()
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    print(f"Tests passed: {passed}/{total}")
    for name, passed in results.items():
        status = "PASS" if passed else "FAIL"
        print(f"  [{status}] {name}")
    print()

    # Halving predictions
    print("HALVING MAJOR ARCANA PROGRESSION")
    print("-" * 70)
    for era in range(12):
        year = 2009 + (era * 4)
        card = get_major_at_halving(era)
        tesla = get_tesla_at_halving(era)
        print(f"  Era {era:2d} ({year}): {card:20s} [Tesla: {tesla}]")
    print()

    print("=" * 70)
    print("\"The blockchain is a sacred clock.\"")
    print("=" * 70)


if __name__ == '__main__':
    main()
