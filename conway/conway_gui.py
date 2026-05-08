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
live_cells = {
    (1, 5), (1, 6), (2, 5), (2, 6),
    (11, 5), (11, 6), (11, 7), (12, 4), (12, 8), (13, 3), (13, 9), (14, 3), (14, 9), (15, 6), (16, 4), (16, 8), (17, 5), (17, 6), (17, 7), (18, 6),
    (21, 3), (21, 4), (21, 5), (22, 3), (22, 4), (22, 5), (23, 2), (23, 6), (25, 1), (25, 2), (25, 6), (25, 7),
    (35, 3), (35, 4), (36, 3), (36, 4)
}

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))

    for (x, y) in live_cells:
        if 0 <= x < COLS and 0 <= y < ROWS:
            pygame.draw.rect(screen, (0, 255, 100),
                             (x * CELL_SIZE + 1, y * CELL_SIZE + 1, CELL_SIZE - 1, CELL_SIZE - 1))

    neighbors = [(x+dx, y+dy) for (x, y) in live_cells
                 for dx in (-1, 0, 1) for dy in (-1, 0, 1)
                 if dx or dy]

    next_cells = {p for p, count in collections.Counter(neighbors).items()
                  if count == 3 or (count == 2 and p in live_cells)}

    live_cells = next_cells

    pygame.display.flip()

    clock.tick(15)

pygame.quit()
