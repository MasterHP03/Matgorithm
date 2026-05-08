import collections
import random as r
import os
import time

W = int(input("Enter the width (Ex. 20): "))
H = int(input("Enter the height (Ex. 20): "))

# live_cells = {(x, y) for x in range(W) for y in range(H) if r.randint(0, 1) == 1}
# live_cells = {(1, 0), (2, 1), (0, 2), (1, 2), (2, 2)} # glider! 🚀

# 🔫 Gosper Glider Gun
live_cells = {
    (1, 5), (1, 6), (2, 5), (2, 6),
    (11, 5), (11, 6), (11, 7), (12, 4), (12, 8), (13, 3), (13, 9), (14, 3), (14, 9), (15, 6), (16, 4), (16, 8), (17, 5), (17, 6), (17, 7), (18, 6),
    (21, 3), (21, 4), (21, 5), (22, 3), (22, 4), (22, 5), (23, 2), (23, 6), (25, 1), (25, 2), (25, 6), (25, 7),
    (35, 3), (35, 4), (36, 3), (36, 4)
}

while True:
    os.system('cls' if os.name == 'nt' else 'clear')

    print('\n'.join(''.join('🟩 ' if (x, y) in live_cells else '⬛ '
                            for x in range(W)) for y in range(H)))

    neighbors = [(x+dx, y+dy) for (x, y) in live_cells
                 for dx in (-1, 0, 1) for dy in (-1, 0, 1)
                 if 0 <= x+dx < W and 0 <= y+dy < H and (dx or dy)]

    """
    neighbors = [((x+dx) % W, (y+dy) % H) for (x, y) in live_cells
                 for dx in (-1, 0, 1) for dy in (-1, 0, 1)
                 if dx or dy]
    """

    next_cells = {p for p, count in collections.Counter(neighbors).items()
                  if count == 3 or (count == 2 and p in live_cells)}

    live_cells = next_cells

    time.sleep(0.03)
