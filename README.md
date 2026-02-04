# Blockhead

**BTC Block Rotation GUI** - A mystical visualization of Bitcoin's SHA-256 mining algorithm.

## Features

### 3D Rotating Block
- Real-time 3D cube visualization of Bitcoin blocks
- Colors derived from block hash
- Rotation speeds influenced by block data (nonce, timestamp)
- Hash segments displayed on cube faces

### Tree of Life
- Kabbalistic Tree of Life (10 Sephirot) visualization
- Algorithm flow mapped to sacred geometry paths
- Animated data flow between nodes
- Each node represents a step in the SHA-256 process:
  - **Kether (Crown)** - Block Header
  - **Chokmah/Binah** - Initial hash rounds
  - **Chesed/Geburah** - Message scheduling and compression
  - **Tiphareth** - Working variables
  - **Netzach/Hod** - Hash updates and nonce iteration
  - **Yesod** - Double hash
  - **Malkuth** - Final block hash

### Wheels Within Wheels
- Inspired by Ezekiel's vision
- 8 nested spinning wheels
- SHA-256 round constants (K values) displayed on wheel segments
- Speeds derived from block properties
- "Eyes" around the outer wheel watching the process
- Central hub displays current hash

### Algorithm Panel
- Step-by-step SHA-256 visualization
- Mining simulation with progress tracking
- Real-time hash and nonce display
- Adjustable difficulty settings
- Visual indication of current algorithm step

## Installation

### Requirements
- Python 3.8+
- tkinter (usually included with Python)

### Optional Dependencies
```bash
pip install pillow numpy
```

### Running the Application
```bash
python main.py
```

## Project Structure

```
Blockhead/
├── main.py              # Entry point
├── requirements.txt     # Dependencies
├── btc/                 # Bitcoin module
│   ├── __init__.py
│   ├── block.py         # BTCBlock data structure
│   └── algorithm.py     # SHA-256 algorithm representation
└── gui/                 # GUI components
    ├── __init__.py
    ├── main_window.py   # Main application window
    ├── btc_block_view.py    # 3D rotating block
    ├── tree_of_life.py      # Sacred geometry view
    ├── spinning_wheels.py   # Wheels within wheels
    └── algorithm_panel.py   # Algorithm display
```

## Usage

### Menu Options
- **File > New Block** - Generate a random block
- **File > Load Genesis** - Load Bitcoin's genesis block
- **View > Toggle Animations** - Start/stop all animations
- **View > Reset View** - Reset to default state
- **Mining > Start/Stop Mining** - Run mining simulation
- **Mining > Set Difficulty** - Adjust required leading zeros

### Controls
- **Speed Slider** - Adjust wheel rotation speed
- **Start Mining Button** - Begin mining simulation
- **Reset Button** - Reset mining state

## The Algorithm Visualization

The application visualizes Bitcoin's double SHA-256 mining process:

1. **Block Header Assembly** (80 bytes)
   - Version (4 bytes)
   - Previous block hash (32 bytes)
   - Merkle root (32 bytes)
   - Timestamp (4 bytes)
   - Difficulty bits (4 bytes)
   - Nonce (4 bytes)

2. **SHA-256 Process**
   - Message padding to 512-bit blocks
   - Initialize hash values (H0-H7)
   - Message schedule expansion (16 to 64 words)
   - 64 compression rounds with constants K0-K63
   - Add compressed values to hash
   - Apply SHA-256 again (double hash)

3. **Mining**
   - Compare hash to target difficulty
   - Increment nonce and repeat until valid

## License

MIT License - see [LICENSE](LICENSE) file.

## Author

Zero2oneZ - 2026
