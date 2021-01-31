import pygame
import colors

class Grid:

    WIDTH = 800
    ROWS = 40
    CELL_WIDTH = WIDTH//ROWS

    def __init__(self):

        self.grid = [[Node(i, j, self.CELL_WIDTH, self.CELL_WIDTH) for j in range(self.ROWS)] for i in
                     range(self.ROWS)]

    def draw_grid(self, win):
        x = 0
        y = 0
        for i in range(self.ROWS):
            x = x + self.CELL_WIDTH
            y = y + self.CELL_WIDTH

            pygame.draw.line(win, colors.BLUE, (x, 0), (x, self.WIDTH))
            pygame.draw.line(win, colors.BLUE, (0, y), (self.WIDTH, y))


    def redraw(self, win):
        for row in self.grid:
            for node in row:
                node.draw(win)
        self.draw_grid(win)
        self.draw_sidebar(win)
        pygame.display.update()

    def draw_sidebar(self, win):
        pygame.draw.rect(win, colors.WHITE, (self.WIDTH, 0, 400, self.WIDTH))
        pygame.draw.line(win, colors.BLACK, (self.WIDTH, 0), (self.WIDTH, self.WIDTH), 3)
        path_img = pygame.image.load('images\path.png')
        win.blit(path_img, (self.WIDTH - 250 + path_img.get_width(), 30))

        sub_font = pygame.font.SysFont("comicsans", 28, True)
        sub = sub_font.render("Instructions:", 1, colors.BLACK)
        win.blit(sub, (self.WIDTH + 200 - sub.get_width() // 2, 400))
        sub_font = pygame.font.SysFont("comicsans", 24, False)
        sub = sub_font.render("1. Right click to pick a starting node", 1, colors.BLACK)
        win.blit(sub, (self.WIDTH + 200 - sub.get_width() // 2, 440))
        sub = sub_font.render("2. Right click to pick an end node", 1, colors.BLACK)
        win.blit(sub, (self.WIDTH + 200 - sub.get_width() // 2, 480))
        sub = sub_font.render("3. Right click to draw barriers", 1, colors.BLACK)
        win.blit(sub, (self.WIDTH + 200 - sub.get_width() // 2, 520))
        sub = sub_font.render("4. Press 'Space' and watch the magic happen!", 1, colors.BLACK)
        win.blit(sub, (self.WIDTH + 200 - sub.get_width() // 2, 560))
        sub = sub_font.render("Left click to erase a node", 1, colors.BLACK)
        win.blit(sub, (self.WIDTH + 200 - sub.get_width() // 2, 800))
        sub = sub_font.render("Press 'r' to reset", 1, colors.BLACK)
        win.blit(sub, (self.WIDTH + 200 - sub.get_width() // 2, 850))

    def get_clicked_position(self, pos):
        column = pos[0] // self.CELL_WIDTH
        row = pos[1] // self.CELL_WIDTH
        if row in range(self.ROWS) and column in range(self.ROWS):
            return self.grid[row][column]


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
        self.color = colors.WHITE
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
        self.color = colors.TURQUOISE

    def make_closed(self):
        self.color = colors.GREEN

    def make_barrier(self):
        self.is_barrier = True
        self.color = colors.BLACK

    def make_path(self):
        self.color = colors.YELLOW

    def reset(self):
        if self.is_start:
            self.START_NODE_IMG.fill((0, 0, 0, 0))
            self.is_start = False
        elif self.is_end:
            self.is_end = False
            self.END_NODE_IMG.fill((0, 0, 0, 0))
        self.color = colors.WHITE

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
