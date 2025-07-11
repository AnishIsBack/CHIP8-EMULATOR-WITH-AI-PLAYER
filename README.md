# Chip-8 Tetris Emulator with AI Bot

This project is a Chip-8 emulator written in Python using Pygame. It runs classic Chip-8 games like TETRIS and includes a simple AI bot that plays the game automatically by simulating keypresses.

The emulator is lightweight, accurate enough to support a variety of ROMs, and serves as a foundation for experimenting with game automation and heuristics-based bots.

---

## Features

- Chip-8 emulator implemented from scratch in Python
- Supports most standard opcodes
- Loads and runs `TETRIS.ch8` ROM
- AI bot simulates player inputs
- Uses Pygame for rendering and keyboard mapping

---

## Controls (if playing manually)

| Key | Action  |
|-----|---------|
| Q   | Left    |
| E   | Right   |
| W   | Rotate  |
| S   | Drop    |

> The AI bot takes over gameplay by default.

---

## Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/chip8-tetris-ai.git
cd chip8-tetris-ai
```

### 2. Install Requirements
```bash
pip install pygame
```

### 3. Add ROM
Place your TETRIS.ch8 file in the root directory.

### 4. Run the Emulator
```bash
python emulator.py
```

---

## File Structure

```
chip8-tetris-ai/
├── bot.py             # AI bot logic
├── emulator.py        # Emulator core with integrated bot control
├── TETRIS.ch8         # ROM file (not included)
└── README.md
```

---

## To-Do / Roadmap

- [ ] Add heuristic-based scoring system for bot decisions
- [ ] Support multiple ROMs and bot switching
- [ ] Add human/bot toggle during runtime
- [ ] Improve opcode coverage and testing

---

## Author
Created by **Anish Bommena**

This project is a fun intersection of low-level emulation and basic game AI. Contributions, forks, and ideas are welcome!
