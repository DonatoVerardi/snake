import pygame
import os
import sys
import time
import random
pygame.font.init()


# Game parameters
NB_BLOCK_X, NB_BLOCK_Y = 20, 20
BLOCK_SIZE = 20
FPS = 4
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
SILVER = (192, 192, 192)
GRID_COLOR = (62, 62, 62)
GAME_OVER_FONT = pygame.font.SysFont("comicsans", 80)
GAME_OVER_FONT.bold = True
GAME_OVER_FONT_SPACE = pygame.font.SysFont("comicsans", 20)

class Food:

    def __init__(self):
        self.x = 0
        self.y = 0
        self.food_surface = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
        self.food_surface.fill(RED)

    def draw_food(self, screen):
        food_rect = (self.food_surface).get_rect(
            topleft=(self.x * BLOCK_SIZE, self.y * BLOCK_SIZE))
        screen.blit(self.food_surface, food_rect)

    def generate_food(self, grid, snake):
        food_grid = []
        for i in grid.grid_tuples:
            if i not in snake.body:
                food_grid.append(i)

        position = random.choice(food_grid)
        self.x = position[0]
        self.y = position[1]


class Grid:
    def __init__(self):
        grid_rect = []
        grid_tuples = []
        for x in range(NB_BLOCK_X):
            for y in range(NB_BLOCK_Y):
                grid_rect.append(pygame.Rect(x * BLOCK_SIZE, y *
                                             BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
                grid_tuples.append((x, y))
        self.grid_rect = grid_rect
        self.grid_tuples = grid_tuples

    def draw_grid(self, screen):
        for square in self.grid_rect:
            pygame.draw.rect(screen, GRID_COLOR, square, 1)


class Snake:

    def __init__(self, x, y):
        self.head = (x, y)
        self.body = [(x, y), (x - 1, y)]
        self.snake_surface = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
        self.snake_surface.fill(WHITE)
        self.grow = False

 # left: l, right: r, up: u, down: d
    def move(self, direction):

        x, y = direction

        self.head = (self.head[0] + x, self.head[1] + y)
        self.body.insert(0, self.head)
        if self.grow:
            self.grow = False
        else:
            self.body.pop()

    def draw_snake(self, screen):
        for tail in self.body:
            x = tail[0]
            y = tail[1]
            # pygame.draw.rect(screen, RED,  pygame.Rect(tail[0] * BLOCK_SIZE, tail[1] * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1)
            snake_rect = (self.snake_surface).get_rect(
                topleft=(x * BLOCK_SIZE, y * BLOCK_SIZE))
            screen.blit(self.snake_surface, snake_rect)

    def eat_food(self, food):
        if (food.x, food.y) == self.head:
            self.grow = True


def draw_window(screen, grid, snake, food, game_over):

    screen.fill((0, 0, 0))
    # draw_grid(screen)
    grid.draw_grid(screen)
    food.draw_food(screen)
    snake.draw_snake(screen)

    if game_over:
        game_over_text = GAME_OVER_FONT.render("GAME OVER", 1, WHITE)
        space_text = GAME_OVER_FONT_SPACE.render(
            "Press the space bar to start again", 1, WHITE)

        screen.blit(game_over_text, ((NB_BLOCK_X * BLOCK_SIZE / 2) -
                                     (game_over_text.get_width() / 2), (NB_BLOCK_Y * BLOCK_SIZE / 2) - (game_over_text.get_height() / 2)))

        screen.blit(space_text, ((NB_BLOCK_X * BLOCK_SIZE / 2) -
                                 (space_text.get_width() / 2), (NB_BLOCK_Y * BLOCK_SIZE) - 20))

    pygame.display.update()


def main():

    # Game variables
    run = True
    game_over = False
    next_move = (0, 1)

    # init game
    screen = pygame.display.set_mode(
        (NB_BLOCK_X * BLOCK_SIZE, NB_BLOCK_Y * BLOCK_SIZE))
    pygame.display.set_caption("Snake")
    clock = pygame.time.Clock()

    # create grid
    grid = Grid()

    # Create snake
    snake = Snake(random.randint(3, NB_BLOCK_X - 3),
                  random.randint(3, int(NB_BLOCK_Y / 3)))

    # Create Food
    food = Food()
    food.generate_food(grid, snake)

    while run:
        clock.tick(FPS)

        last_move = next_move
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and last_move != (1, 0):
                    next_move = (-1, 0)
                if event.key == pygame.K_RIGHT and last_move != (-1, 0):
                    next_move = (1, 0)
                if event.key == pygame.K_UP and last_move != (0, 1):
                    next_move = (0, -1)
                if event.key == pygame.K_DOWN and last_move != (0, -1):
                    next_move = (0, 1)
                if event.key == pygame.K_SPACE and game_over:
                    game_over = False
                    snake = Snake(random.randint(3, NB_BLOCK_X - 3),
                                  random.randint(3, int(NB_BLOCK_Y / 3)))
                    next_move = (0, 1)
                    last_move = (0, 1)
                    food.generate_food(grid, snake)

        last_move = next_move
        if not game_over:
            snake.move(next_move)
            snake.eat_food(food)
            if snake.grow:
                food.generate_food(grid, snake)

        # GAME OVER
        # outside borders
        if snake.head[0] < 0 or snake.head[0] >= NB_BLOCK_X or snake.head[1] < 0 or snake.head[1] >= NB_BLOCK_Y:
            game_over = True
        # eat itself
        if snake.head in snake.body[1:]:
            game_over = True

        draw_window(screen, grid, snake, food, game_over)


main()
