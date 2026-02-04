# Blockhead - SoloMiner

A beautiful Bitcoin Solo Mining GUI application with wallet generation and real-time mining visualization.

## Features

- **Secure Wallet Generation**: Generate BTC wallets with 12-word mnemonic seed phrases
- **Mining Difficulty Levels 0-12**: Choose from Demo mode to Maximum difficulty
- **Real-time Dashboard**: Live hash visualization, statistics, and progress tracking
- **Beautiful Dark Theme**: Modern UI with Bitcoin orange accents
- **Cross-platform**: Works on Windows, macOS, and Linux

## Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Quick Install

```bash
# Clone the repository
git clone https://github.com/Zero2oneZ/Blockhead.git
cd Blockhead

# Run the installer
python install.py
```

### Manual Install

```bash
pip install -r requirements.txt
```

## Usage

### Launch the Application

```bash
# Option 1: Using the run script
python run.py

# Option 2: As a Python module
python -m solominer

# Option 3: Using launcher scripts (after install)
./launch_solominer.sh    # Unix/Mac
launch_solominer.bat     # Windows
```

### Getting Started

1. **Launch** the application
2. **Generate** a new wallet or import an existing one
3. **Select** your mining difficulty (0-12)
4. **Start** mining and watch the real-time visualization

## Mining Difficulty Levels

Probability of N leading zeros: `(1/16)^N`

| Level | Name | Target Zeros | Probability | Avg Hashes Needed |
|-------|------|--------------|-------------|-------------------|
| 0 | Demo Mode | 1 | 1 in 16 | 16 |
| 1-2 | Beginner/Easy | 2 | 1 in 256 | 256 |
| 3-4 | Light/Standard | 3 | 1 in 4,096 | 4,096 |
| 5-6 | Moderate/Intermediate | 4 | 1 in 65,536 | 65,536 |
| 7-8 | Advanced/Expert | 5 | 1 in 1,048,576 | ~1M |
| 9-10 | Professional/Extreme | 6 | 1 in 16,777,216 | ~17M |
| 11 | Ultra | 7 | 1 in 268,435,456 | ~268M |
| 12 | Maximum | 8 | 1 in 4,294,967,296 | ~4.3B |

**Note**: 7 zeros achieved = 1 in 268 million probability!

## Project Structure

```
Blockhead/
├── solominer/
│   ├── core/
│   │   ├── wallet.py      # BTC wallet generation
│   │   └── miner.py       # Mining algorithm engine
│   ├── gui/
│   │   ├── main_window.py     # Main application
│   │   ├── wallet_screen.py   # Wallet generation UI
│   │   ├── mining_dashboard.py # Mining dashboard
│   │   └── theme.py           # UI theme configuration
│   └── utils/
│       └── helpers.py     # Utility functions
├── install.py             # Installation script
├── run.py                 # Quick launcher
└── requirements.txt       # Dependencies
```

## Dependencies

- customtkinter - Modern GUI framework
- Pillow - Image processing
- requests - HTTP client
- rich - Terminal formatting

## Security Notice

- Private keys and seed phrases are generated locally
- Keys never leave your device
- Always securely backup your recovery seed phrase

## License

MIT License - See [LICENSE](LICENSE) for details.

## Contributing

Contributions welcome! Please feel free to submit pull requests.

---

Made with ⚡ by Blockhead
