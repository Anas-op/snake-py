import pygame
import sys
from pygame.math import Vector2
import random


class MAIN:
    def __init__(self):
        self.snake = SNAKE()
        self.fruit = FRUIT()

    def update(self):
        self.snake.move_snake()
        self.collision()

    def draw_elements(self):
        self.fruit.fruit_draw()
        self.snake.snake_draw()
        self.check_death()

    def loadImages(self):
        for filename in filenames:
            item = pygame.image.load(filename).convert_alpha()
            images.append(item)

    # check collision of snake and fruit
    def collision(self):
        if self.fruit.pos == self.snake.body[0]:
            # reposition the fruit and add block to snake
            self.fruit.randomizePosition()
            self.snake.increase_size()

    def check_death(self):
        # check if is outside of wall
        if not 0 <= self.snake.body[0].x < cell_number or not 0 <= self.snake.body[0].y < cell_number:
            self.game_over()
        # check if it hits itself
        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.game_over()

    def game_over(self):
        pygame.quit()
        sys.exit()


class SNAKE:
    def __init__(self):
        self.body = [Vector2(7, 10), Vector2(6, 10),
                     Vector2(5, 10)]  # blocks one near each other that will represent the snake
        self.direction = Vector2(1, 0)
        self.new_block = False

        # head positions
        self.head_up = pygame.image.load('Images/head_up.png').convert_alpha()
        self.head_down = pygame.image.load('Images/head_down.png').convert_alpha()
        self.head_right = pygame.image.load('Images/head_right.png').convert_alpha()
        self.head_left = pygame.image.load('Images/head_left.png').convert_alpha()

        # body tail positions
        self.tail_up = pygame.image.load('Images/tail_up.png').convert_alpha()
        self.tail_down = pygame.image.load('Images/tail_down.png').convert_alpha()
        self.tail_right = pygame.image.load('Images/tail_right.png').convert_alpha()
        self.tail_left = pygame.image.load('Images/tail_left.png').convert_alpha()

        # vertical and horizontal body
        self.body_vertical = pygame.image.load('Images/body_vertical.png').convert_alpha()
        self.body_horizontal = pygame.image.load('Images/body_horizontal.png').convert_alpha()

        # curve body parts
        self.body_tr = pygame.image.load('Images/body_tr.png').convert_alpha()
        self.body_tl = pygame.image.load('Images/body_tl.png').convert_alpha()
        self.body_br = pygame.image.load('Images/body_br.png').convert_alpha()
        self.body_bl = pygame.image.load('Images/body_bl.png').convert_alpha()

    def snake_draw(self):

        self.update_head()
        self.update_tail()

        for index, block in enumerate(self.body):  # enumerate gets index of the current block inside the loop
            # 1. we still need a rect for the positioning
            x_pos = (block.x * cell_size)
            y_pos = (block.y * cell_size)
            block_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)

            # 2. which part of body has the specific graphic using indexes
            if index == 0:  # head element
                screen.blit(self.head, block_rect)
            elif index == len(self.body) - 1:
                screen.blit(self.tail, block_rect)
            else:
                # get relation between previous and next block
                previous_block = self.body[index + 1] - block
                next_block = self.body[index - 1] - block
                if previous_block.x == next_block.x:  # check if previous and next block are in the same x or y if true puts the vertical body
                    screen.blit(self.body_vertical, block_rect)
                elif previous_block.y == next_block.y:
                    screen.blit(self.body_horizontal, block_rect)
                else:
                    if previous_block.x == -1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == -1:
                        screen.blit(self.body_tl, block_rect)
                    elif previous_block.x == -1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == -1:
                        screen.blit(self.body_bl, block_rect)
                    elif previous_block.x == 1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == 1:
                        screen.blit(self.body_tr, block_rect)
                    elif previous_block.x == 1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == 1:
                        screen.blit(self.body_br, block_rect)

    # checking by subtracting head with body and check relation between x y of head and x y of body to see in which direction they're moving
    def update_head(self):
        head_relation = self.body[1] - self.body[0]  # you find the block where is based on the head
        if head_relation == Vector2(1, 0):
            self.head = self.head_left  # body is in the right and head in the left
        elif head_relation == Vector2(-1, 0):
            self.head = self.head_right
        elif head_relation == Vector2(0, 1):
            self.head = self.head_up
        elif head_relation == Vector2(0, -1):
            self.head = self.head_down

    def update_tail(self):
        tail_relation = self.body[-2] - self.body[-1]  # find the block but subtracting last to penultimate
        if tail_relation == Vector2(1, 0):
            self.tail = self.tail_left  # body is in the right and head in the left
        elif tail_relation == Vector2(-1, 0):
            self.tail = self.tail_right
        elif tail_relation == Vector2(0, 1):
            self.tail = self.tail_up
        elif tail_relation == Vector2(0, -1):
            self.tail = self.tail_down

    # for block in self.body:
    #    block_rect = pygame.Rect(block.x * cell_size, block.y * cell_size, cell_size, cell_size)
    #   pygame.draw.rect(screen, (255, 120, 120), block_rect)
    #    # create rect from position
    #    # draw rectangle

    def move_snake(self):
        if self.new_block == True:
            # gets all body and append another block
            body2 = self.body[:]
            body2.insert(0, body2[0] + self.direction)
            self.body = body2[:]
            self.new_block = False
        else:
            body2 = self.body[:-1]
            body2.insert(0, body2[0] + self.direction)
            self.body = body2[:]

    def increase_size(self):
        # take entire body
        self.new_block = True


class FRUIT:



    def __init__(self):
        self.x = random.randint(0, cell_number - 1)
        self.y = random.randint(0, cell_number - 1)
        self.pos = Vector2(self.x, self.y)  # values x and y placed in vector
        self.index = 0
        # create x and y position
        # draw square which will be the fruit

    def fruit_draw(self):
        fruit_rect = pygame.Rect(self.pos.x * cell_size, self.pos.y * cell_size, cell_size, cell_size)
        screen.blit(images[self.index], fruit_rect)  # insert fruit image with blit function
        # pygame.draw.rect(screen, (126, 166, 114), fruit_rect)
        # create rectangle

    def randomizePosition(self):
        self.x = random.randint(0, cell_number - 1)
        self.y = random.randint(0, cell_number - 1)
        self.index = random.randint(0, len(images)-1)
        self.pos = Vector2(self.x, self.y)  # values x and y placed in vector


# display surface the canvas containing the game, is drawn 1
# surfaces we can have multiple surfaces

cell_size = 40
cell_number = 20
backgroundColor = (0, 255, 45)  # rgb color definition
pygame.init()
screen = pygame.display.set_mode((cell_number * cell_size, cell_number * cell_size))
clock = pygame.time.Clock()  # influence time in pygame to open and manage events
images = []
filenames = ['Images/Items/py.png', 'Images/Items/c.png', 'Images/Items/hashtag.png', 'Images/Items/html.png', 'Images/Items/brands.png', 'Images/Items/css.png', 'Images/Items/java.png', 'Images/Items/javascript.png', 'Images/Items/json.png', 'Images/Items/nodejs.png', 'Images/Items/py.png', 'Images/Items/react.png', 'Images/Items/sql.png', 'Images/Items/xml.png', 'Images/Items/zip-file.png']

fruit = FRUIT()
snake = SNAKE()
main_game = MAIN()

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 150)  # triggereato ogni 150 millisecondi
main_game.loadImages()
index = random.randint(0, len(images) - 1)

