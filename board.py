import pygame
import constants
from node import Node


class Grid:

    WIDTH = 1000
    HEIGHT = 1000
    ROWS = 40
    COLUMNS = 40

    def __init__(self):
        self.cell_width = self.WIDTH // self.COLUMNS
        self.cell_height = self.HEIGHT // self.ROWS
        self.grid = [[Node(i, j, self.cell_width, self.cell_height) for j in range(self.COLUMNS)] for i in
                     range(self.ROWS)]

    def draw(self, win):
        # Draw Nodes
        for row in self.grid:
            for node in row:
                node.draw(win)

        # Draw Grid Lines
        for i in range(self.ROWS):
            pygame.draw.line(win, constants.BLUE, (0, i * self.cell_height), (self.WIDTH, i * self.cell_height))
            for j in range(self.COLUMNS):
                pygame.draw.line(win, constants.BLUE, (j * self.cell_width, 0), (j * self.cell_width, self.HEIGHT))

        # Draw Sidebar
        self.draw_sidebar(win)

        pygame.display.update()


    def draw_sidebar(self, win):
        pygame.draw.rect(win, constants.WHITE, (self.WIDTH, 0, 400, self.HEIGHT))
        pygame.draw.line(win, constants.BLACK, (self.WIDTH, 0), (self.WIDTH, self.HEIGHT), 3)
        path_img = pygame.image.load('images\path.png')
        win.blit(path_img, (self.WIDTH - 250 + path_img.get_width(), 30))

        title_font = pygame.font.SysFont("comicsans", 32, True)
        title = title_font.render("A* Search Algorithm uses", 1, constants.GREEN)
        win.blit(title, (self.WIDTH + 200 - title.get_width() // 2, 320))
        title = title_font.render("heuristics to guarantee", 1, constants.GREEN)
        win.blit(title, (self.WIDTH + 200 - title.get_width() // 2, 360))
        title = title_font.render("the shortest path", 1, constants.GREEN)
        win.blit(title, (self.WIDTH + 200 - title.get_width() // 2, 400))
        sub_font = pygame.font.SysFont("comicsans", 28, True)
        sub = sub_font.render("Instructions:", 1, constants.BLACK)
        win.blit(sub, (self.WIDTH + 200 - sub.get_width() // 2, 500))
        sub_font = pygame.font.SysFont("comicsans", 24, False)
        sub = sub_font.render("1. Right click to pick a starting node", 1, constants.BLACK)
        win.blit(sub, (self.WIDTH + 200 - sub.get_width() // 2, 540))
        sub = sub_font.render("2. Right click to pick an end node", 1, constants.BLACK)
        win.blit(sub, (self.WIDTH + 200 - sub.get_width() // 2, 580))
        sub = sub_font.render("3. Right click to draw barriers", 1, constants.BLACK)
        win.blit(sub, (self.WIDTH + 200 - sub.get_width() // 2, 620))
        sub = sub_font.render("4. Press 'Space' and watch the magic happen!", 1, constants.BLACK)
        win.blit(sub, (self.WIDTH + 200 - sub.get_width() // 2, 660))
        sub = sub_font.render("Left click to erase a node", 1, constants.BLACK)
        win.blit(sub, (self.WIDTH + 200 - sub.get_width() // 2, 800))
        sub = sub_font.render("Press 'r' to reset", 1, constants.BLACK)
        win.blit(sub, (self.WIDTH + 200 - sub.get_width() // 2, 850))


    def get_clicked_position(self, pos):
        column = pos[0] // self.cell_width
        row = pos[1] // self.cell_height
        if row in range(self.ROWS) and column in range(self.COLUMNS):
            return self.grid[row][column]