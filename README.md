# GTABackFeed

**Audio Suppressor** – Python tool to remove background noise from audio files (perfect for GTA voice chat, podcasts, calls, etc.)

## Features
- Spectral noise reduction using `noisereduce`
- CLI + **beautiful GUI** (CustomTkinter)
- Supports WAV, MP3, etc.
- Real-time ready for future expansion

## Quick Start

1. Clone the repo
   ```bash
   git clone https://github.com/gifftripp/GTABackFeed.git
   cd GTABackFeed
   ```

2. Create & activate virtual environment
   ```bash
   python3 -m venv venv
   source venv/bin/activate   # Mac/Linux
   # Windows: venv\Scripts\activate
   ```

3. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```

## Run the GUI (recommended)
```bash
python gui.py
```

## Run the CLI (alternative)
```bash
python main.py -i your_noisy_file.wav -o clean_output.wav
```

## Project Structure
- `gui.py` – Modern GUI interface
- `main.py` – CLI tool
- `src/suppressor.py` – Core audio processing logic
- `requirements.txt` – All libraries

Built for easy expansion (real-time mic, GTA-specific filters, etc.)

Made with ❤️ by Giff Tripp
