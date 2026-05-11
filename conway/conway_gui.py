import warnings

warnings.filterwarnings('ignore', category=UserWarning)
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

import pygame
import collections

pygame.init()

W, H = 800, 600
CELL_SIZE = 10
COLS, ROWS = W // CELL_SIZE, H // CELL_SIZE

screen = pygame.display.set_mode((W, H))
pygame.display.set_caption('GUI')
clock = pygame.time.Clock()

# 🔫 Gosper Glider Gun
live_set = {
    (1, 5), (1, 6), (2, 5), (2, 6),
    (11, 5), (11, 6), (11, 7), (12, 4), (12, 8), (13, 3), (13, 9), (14, 3), (14, 9), (15, 6), (16, 4), (16, 8), (17, 5), (17, 6), (17, 7), (18, 6),
    (21, 3), (21, 4), (21, 5), (22, 3), (22, 4), (22, 5), (23, 2), (23, 6), (25, 1), (25, 2), (25, 6), (25, 7),
    (35, 3), (35, 4), (36, 3), (36, 4)
}

live_cells = {cell: 0 for cell in live_set}

is_dragging = False
start_live = True

frozen = False

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                frozen = not frozen
        if frozen:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    x, y = event.pos
                    start_cell = (x // CELL_SIZE, y // CELL_SIZE)
                    start_live = start_cell in live_cells
                    is_dragging = True
                    if 0 <= start_cell[0] < COLS and 0 <= start_cell[1] < ROWS:
                        if not start_live:
                            live_cells[start_cell] = 0
                        else:
                            live_cells.pop(start_cell, None)
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    is_dragging = False
                    x, y = event.pos
                    end_cell = (x // CELL_SIZE, y // CELL_SIZE)
            elif event.type == pygame.MOUSEMOTION:
                if is_dragging:
                    x, y = event.pos
                    current_cell = (x // CELL_SIZE, y // CELL_SIZE)
                    if 0 <= current_cell[0] < COLS and 0 <= current_cell[1] < ROWS:
                        if (current_cell in live_cells) is start_live:
                            if not start_live:
                                live_cells[current_cell] = 0
                            else:
                                live_cells.pop(current_cell, None)

    screen.fill((0, 0, 0))

    for (x, y), age in live_cells.items():
        if 0 <= x < COLS and 0 <= y < ROWS:
            opq = max(100, min(255, 255 - age * 10))
            pygame.draw.rect(screen, (opq, 0, opq),
                             (x * CELL_SIZE + 1, y * CELL_SIZE + 1, CELL_SIZE - 1, CELL_SIZE - 1))

    if not frozen:
        neighbors = [(x+dx, y+dy) for (x, y) in live_cells
                     for dx in (-1, 0, 1) for dy in (-1, 0, 1)
                     if dx or dy]

        next_cells = {}
        for p, count in collections.Counter(neighbors).items():
            if count == 3 or (count == 2 and p in live_cells):
                if p in live_cells:
                    next_cells[p] = live_cells[p] + 1
                else:
                    next_cells[p] = 0

        live_cells = next_cells

    pygame.display.flip()

    clock.tick(15)

pygame.quit()
