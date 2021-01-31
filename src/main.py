import pygame
import colors
from board import Grid
from queue import PriorityQueue


pygame.font.init()
WIN = pygame.display.set_mode((Grid.WIDTH + 400, Grid.WIDTH))
pygame.display.set_caption("A* Path Finding Algorithm")
WIN.fill(colors.WHITE)


def algorithm(draw, start, end):
    order = 0
    open_set = PriorityQueue()
    open_set.put((0, order, start))
    previous_nodes = {}
    start.g_score = 0
    open_set_hash = {start}

    while not open_set.empty():
        current_node = open_set.get()[2]
        open_set_hash.remove(current_node)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    continue

        for neighbor in current_node.neighbors:
            temp_g_score = current_node.g_score + 1
            if current_node.__lt__(neighbor):
                previous_nodes[neighbor] = current_node
                neighbor.g_score = temp_g_score
                neighbor.h_score = heuristic(neighbor.get_position(), end.get_position())
                neighbor.f_score = neighbor.g_score + neighbor.h_score
                if neighbor not in open_set_hash:
                    order += 1
                    open_set.put((neighbor.f_score, order, neighbor))
                    open_set_hash.add(neighbor)
                    if neighbor != end:
                        neighbor.make_open()

        if current_node != start:
            current_node.make_closed()

        if current_node == end:
            while current_node in previous_nodes:
                current_node = previous_nodes[current_node]
                if current_node != start:
                    current_node.make_path()
                draw()
            return True
        draw()
    return False


def heuristic(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    return abs(x1 - x2) + abs(y1 - y2)


def main(win):
    grid = Grid()
    start = None
    end = None
    run = True
    while run:
        grid.redraw(win)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                node = grid.get_clicked_position(pos)
                if not start and node != end:
                    start = node
                    start.is_start = True
                elif not end and node != start and node:
                    end = node
                    end.is_end = True
                elif node != end and node != start and node:
                    node.make_barrier()

            if pygame.mouse.get_pressed()[2]:
                pos = pygame.mouse.get_pos()
                node = grid.get_clicked_position(pos)
                if node:
                    node.reset()
                    if node == start:
                        start = None
                    elif node == end:
                        end = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    for row in grid.grid:
                        for node in row:
                            node.update_neighbors(grid.grid, grid.ROWS, grid.ROWS)
                    algorithm((lambda: grid.redraw(win)), start, end)

                if event.key == pygame.K_r:
                    start = None
                    end = None
                    grid = Grid()
    pygame.quit()


if __name__ == '__main__':
    main(WIN)
