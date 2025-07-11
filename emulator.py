import pygame
import sys
import random
from bot import TetrisBot

SCREEN_WIDTH, SCREEN_HEIGHT = 64, 32
SCALE = 10
FPS = 60

KEYMAP = {
    pygame.K_x: 0x0, pygame.K_1: 0x1, pygame.K_2: 0x2, pygame.K_3: 0x3,
    pygame.K_q: 0x4, pygame.K_w: 0x5, pygame.K_e: 0x6, pygame.K_a: 0x7,
    pygame.K_s: 0x8, pygame.K_d: 0x9, pygame.K_z: 0xA, pygame.K_c: 0xB,
    pygame.K_4: 0xC, pygame.K_r: 0xD, pygame.K_f: 0xE, pygame.K_v: 0xF,
}

def update_keys(chip8):
    keys = [0] * 16
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    pressed = pygame.key.get_pressed()
    for key, val in KEYMAP.items():
        if pressed[key]:
            keys[val] = 1
    chip8.set_keys(keys)

class Chip8:
    def __init__(self):
        self.memory = [0] * 4096
        self.V = [0] * 16
        self.I = 0
        self.pc = 0x200
        self.stack = []
        self.display = [[0] * SCREEN_WIDTH for _ in range(SCREEN_HEIGHT)]
        self.keys = [0] * 16
        self.delay_timer = 0
        self.sound_timer = 0

    def load_rom(self, path):
        with open(path, 'rb') as f:
            rom = f.read()
            for i in range(len(rom)):
                self.memory[0x200 + i] = rom[i]

    def emulate_cycle(self):
        opcode = (self.memory[self.pc] << 8) | self.memory[self.pc + 1]
        self.pc += 2
        self.decode_execute(opcode)

        if self.delay_timer > 0:
            self.delay_timer -= 1
        if self.sound_timer > 0:
            self.sound_timer -= 1

    def decode_execute(self, opcode):
        x = (opcode & 0x0F00) >> 8
        y = (opcode & 0x00F0) >> 4
        n = opcode & 0x000F
        nn = opcode & 0x00FF
        nnn = opcode & 0x0FFF

        if opcode == 0x00E0:
            self.display = [[0] * SCREEN_WIDTH for _ in range(SCREEN_HEIGHT)]
        elif opcode == 0x00EE:
            self.pc = self.stack.pop()
        elif opcode & 0xF000 == 0x1000:
            self.pc = nnn
        elif opcode & 0xF000 == 0x2000:
            self.stack.append(self.pc)
            self.pc = nnn
        elif opcode & 0xF000 == 0x3000:
            if self.V[x] == nn:
                self.pc += 2
        elif opcode & 0xF000 == 0x4000:
            if self.V[x] != nn:
                self.pc += 2
        elif opcode & 0xF00F == 0x5000:
            if self.V[x] == self.V[y]:
                self.pc += 2
        elif opcode & 0xF000 == 0x6000:
            self.V[x] = nn
        elif opcode & 0xF000 == 0x7000:
            self.V[x] = (self.V[x] + nn) & 0xFF
        elif opcode & 0xF00F == 0x8000:
            self.V[x] = self.V[y]
        elif opcode & 0xF00F == 0x8001:
            self.V[x] |= self.V[y]
        elif opcode & 0xF00F == 0x8002:
            self.V[x] &= self.V[y]
        elif opcode & 0xF00F == 0x8003:
            self.V[x] ^= self.V[y]
        elif opcode & 0xF00F == 0x8004:
            result = self.V[x] + self.V[y]
            self.V[0xF] = 1 if result > 0xFF else 0
            self.V[x] = result & 0xFF
        elif opcode & 0xF00F == 0x8005:
            self.V[0xF] = 1 if self.V[x] > self.V[y] else 0
            self.V[x] = (self.V[x] - self.V[y]) & 0xFF
        elif opcode & 0xF00F == 0x8006:
            self.V[0xF] = self.V[x] & 1
            self.V[x] >>= 1
        elif opcode & 0xF00F == 0x8007:
            self.V[0xF] = 1 if self.V[y] > self.V[x] else 0
            self.V[x] = (self.V[y] - self.V[x]) & 0xFF
        elif opcode & 0xF00F == 0x800E:
            self.V[0xF] = (self.V[x] & 0x80) >> 7
            self.V[x] = (self.V[x] << 1) & 0xFF
        elif opcode & 0xF00F == 0x9000:
            if self.V[x] != self.V[y]:
                self.pc += 2
        elif opcode & 0xF000 == 0xA000:
            self.I = nnn
        elif opcode & 0xF000 == 0xC000:
            self.V[x] = random.randint(0, 255) & nn
        elif opcode & 0xF000 == 0xD000:
            self.V[0xF] = 0
            for row in range(n):
                sprite = self.memory[self.I + row]
                for col in range(8):
                    if sprite & (0x80 >> col):
                        px = (self.V[x] + col) % SCREEN_WIDTH
                        py = (self.V[y] + row) % SCREEN_HEIGHT
                        if self.display[py][px]:
                            self.V[0xF] = 1
                        self.display[py][px] ^= 1
        elif opcode & 0xF0FF == 0xE09E:
            if self.keys[self.V[x]]:
                self.pc += 2
        elif opcode & 0xF0FF == 0xE0A1:
            if not self.keys[self.V[x]]:
                self.pc += 2
        elif opcode & 0xF0FF == 0xF007:
            self.V[x] = self.delay_timer
        elif opcode & 0xF0FF == 0xF015:
            self.delay_timer = self.V[x]
        elif opcode & 0xF0FF == 0xF018:
            self.sound_timer = self.V[x]
        elif opcode & 0xF0FF == 0xF01E:
            self.I = (self.I + self.V[x]) & 0xFFF
        elif opcode & 0xF0FF == 0xF029:
            self.I = self.V[x] * 5
        elif opcode & 0xF0FF == 0xF033:
            self.memory[self.I] = self.V[x] // 100
            self.memory[self.I + 1] = (self.V[x] // 10) % 10
            self.memory[self.I + 2] = self.V[x] % 10
        elif opcode & 0xF0FF == 0xF055:
            for i in range(x + 1):
                self.memory[self.I + i] = self.V[i]
        elif opcode & 0xF0FF == 0xF065:
            for i in range(x + 1):
                self.V[i] = self.memory[self.I + i]
        else:
            print(f"Unknown opcode: {hex(opcode)}")

    def get_display(self):
        return self.display

    def set_keys(self, keys):
        self.keys = keys

def draw(screen, display):
    screen.fill((0, 0, 0))
    for y in range(SCREEN_HEIGHT):
        for x in range(SCREEN_WIDTH):
            if display[y][x]:
                pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(x*SCALE, y*SCALE, SCALE, SCALE))
    pygame.display.flip()

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH * SCALE, SCREEN_HEIGHT * SCALE))
    pygame.display.set_caption("Chip-8 Tetris Emulator with Bot")
    clock = pygame.time.Clock()

    chip8 = Chip8()
    chip8.load_rom("TETRIS.ch8")
    bot = TetrisBot(chip8)

    while True:
        keys = bot.choose_move(chip8.get_display())
        chip8.set_keys(keys)
        chip8.emulate_cycle()
        draw(screen, chip8.get_display())
        clock.tick(FPS)

if __name__ == "__main__":
    main()
