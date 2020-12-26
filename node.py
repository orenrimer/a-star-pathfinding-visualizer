import constants
import pygame



class Node:

    START_NODE_IMG = pygame.image.load("images/location_PNG.png")
    END_NODE_IMG = pygame.image.load("images/target_PNG.png")

    def __init__(self, row, column, width, height):
        self.row = row
        self.column = column
        self.width = width
        self.height = height
        self.x = column * width
        self.y = row * height
        self.h_score = float("inf")
        self.g_score = float("inf")
        self.f_score = float("inf")
        self.color = constants.WHITE
        self.neighbors = []
        self.is_start = False
        self.is_end = False
        self.is_barrier = False

    def get_position(self):
        return self.row, self.column

    def draw(self, win):
        if self.is_start:
            self.make_start(win)
        elif self.is_end:
            self.make_end(win)
        else:
            pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))

    def make_start(self, win):
        self.END_NODE_IMG = pygame.transform.scale(self.END_NODE_IMG, (self.width, self.height))
        win.blit(self.END_NODE_IMG, (self.x, self.y))

    def make_end(self, win):
        self.START_NODE_IMG = pygame.transform.scale(self.START_NODE_IMG, (self.width, self.height))
        win.blit(self.START_NODE_IMG, (self.x, self.y))

    def make_open(self):
        self.color = constants.TURQUOISE

    def make_closed(self):
        self.color = constants.GREEN

    def make_barrier(self):
        self.is_barrier = True
        self.color = constants.BLACK

    def make_path(self):
        self.color = constants.YELLOW

    def reset(self):
        if self.is_start:
            self.START_NODE_IMG.fill((0, 0, 0, 0))
            self.is_start = False
        elif self.is_end:
            self.is_end = False
            self.END_NODE_IMG.fill((0, 0, 0, 0))
        self.color = constants.WHITE

    def __lt__(self, value):
        return self.g_score < value.g_score

    def update_neighbors(self, grid, rows, columns):
        if self.row < rows - 1 and not grid[self.row + 1][self.column].is_barrier:
            self.neighbors.append(grid[self.row + 1][self.column])

        if self.row > 0 and not grid[self.row - 1][self.column].is_barrier:
            self.neighbors.append(grid[self.row - 1][self.column])

        if self.column < columns - 1 and not grid[self.row][self.column + 1].is_barrier:
            self.neighbors.append(grid[self.row][self.column + 1])

        if self.column > 0 and not grid[self.row][self.column - 1].is_barrier:
            self.neighbors.append(grid[self.row][self.column - 1])