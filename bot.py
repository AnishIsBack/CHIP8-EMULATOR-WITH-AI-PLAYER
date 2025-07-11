import random

class TetrisBot:
    def __init__(self, chip8):
        self.chip8 = chip8
        self.frame_counter = 0
        self.last_key = None

    def choose_move(self, display):
        # Placeholder: every 10 frames, randomly pick one key
        self.frame_counter += 1
        if self.frame_counter % 10 == 0:
            self.last_key = random.choice([0x4, 0x5, 0x6, 0x8])  # Q W E S

        keys = [0] * 16
        if self.last_key is not None:
            keys[self.last_key] = 1
        return keys
