import random

import cv2
import numpy as np


class PixelType:
    EMPTY = np.array([0, 0, 0], dtype=np.uint8)
    SAND = np.array([1, 255, 255], dtype=np.uint8)
    WATER = np.array([255, 1, 1], dtype=np.uint8)


class Grid:
    def __init__(self, size: int):
        self.size = size
        self.grid = np.zeros((size, size, 3), dtype=np.uint8)
        self.occupied = set()

    def render(self):
        cv2.imshow("Sandbox", self.grid.transpose(1, 0, 2)[::-1, :, :])
        cv2.waitKey(1)

    def click(self, x: int, y: int, pixel_type: np.ndarray, size: int):
        min_x = max(0, x - size)
        max_x = min(self.size - 1, x + size)
        min_y = max(0, y - size)
        max_y = min(self.size - 1, y + size)

        for x in range(min_x, max_x):
            for y in range(min_y, max_y):
                if (x, y) not in self.occupied:
                    self.grid[x, y] = pixel_type
                    self.occupied.add((x, y))

    def step(self):
        for x, y in self.occupied:
            fall_coords = self.try_fall(x, y)
            if fall_coords:
                self.move(x, y, fall_coords[0], fall_coords[1])

            elif self.is_type(x, y, PixelType.SAND):
                slide_coords = self.try_slide(x, y, down=True)
                if slide_coords:
                    self.move(x, y, slide_coords[0], slide_coords[1])

            elif self.is_type(x, y, PixelType.WATER):
                slide_coords = self.try_slide(x, y, down=True)
                if not slide_coords:
                    slide_coords = self.try_slide(x, y, down=False)
                if slide_coords:
                    self.move(x, y, slide_coords[0], slide_coords[1])

    def try_fall(self, x: int, y: int):
        if y >= 0:
            if (x, y - 1) not in self.occupied:
                return (x, y - 1)
        return False

    def try_slide(self, x: int, y: int, down: bool = False):
        if down:
            if y < 1:
                return False
            new_y = y - 1
        else:
            new_y = y

        right = (x + 1, new_y)
        left = (x - 1, new_y)

        left_empty = x > 0 and left not in self.occupied
        right_empty = x < self.size - 1 and right not in self.occupied
        if left_empty and right_empty:
            if random.random() < 0.5:
                return left
            else:
                return right
        elif left_empty:
            return left
        elif right_empty:
            return right

    def move(self, x: int, y: int, new_x: int, new_y: int):
        self.occupied.remove((x, y))
        self.occupied.add((new_x, new_y))
        self.grid[new_x, new_y] = self.grid[x, y]
        self.grid[x, y] = PixelType.EMPTY

    def is_type(self, x: int, y: int, pixel_type: np.ndarray):
        return (self.grid[x, y] == pixel_type).all()


if __name__ == "__main__":
    grid = Grid(1000)
    grid.click(2, 2, PixelType.SAND, 4)
    grid.click(500, 500, PixelType.WATER, 300)
    grid.click(800, 800, PixelType.SAND, 30)
    grid.click(300, 300, PixelType.SAND, 30)

    import time

    while True:
        t0 = time.time()
        grid.step()
        t1 = time.time()
        grid.render()
        t2 = time.time()
        print(t1 - t0, t2 - t1)
