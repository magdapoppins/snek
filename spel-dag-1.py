import pygame
import random
import sys

# Skärmens storlek (du kan ändra dessa själv i efterhand)
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
MIDDLE_COORDINATES = ((SCREEN_WIDTH/2), (SCREEN_HEIGHT/2))

# Spel "pixlarna" på skärmen kallas grid
GRID_PIXEL_SIZE = 30
GRID_WIDTH = SCREEN_WIDTH//GRID_PIXEL_SIZE
GRID_HEIGHT = SCREEN_HEIGHT//GRID_PIXEL_SIZE

# Koordinaterna åt olika håll 
UP = (0,-1)
DOWN = (0,1)
LEFT = (-1,0) 
RIGHT = (1,0)

# Färger vi kommer använda
LIGHT_PINK = '#ffc8dd'
DARK_PINK = '#ffafcc'
GREEN = '#caffbf'
ORANGE = '#ffd6a5'
BLACK = '#495057'

def get_random_direction():
    return random.choice([UP, DOWN, LEFT, RIGHT])

def are_opposite_directions(direction_a, direction_b):
    # Du kan testa: upp (0, 1) blir ner (0, -1) då man multiplicerar bägge koordinaterna med -1!
    x, y = direction_a
    return (x*-1, y*-1) == direction_b

def get_random_position():
    return random.randint(0, GRID_WIDTH-1)*GRID_PIXEL_SIZE, random.randint(0, GRID_HEIGHT-1)*GRID_PIXEL_SIZE


class Snake():
    def __init__(self):
        self.positions = [MIDDLE_COORDINATES]
        self.direction = get_random_direction()
        self.score = 0
        self.is_alive = True

    def turn(self, direction):
        # Vi vill svänga upp (0, 1)
        if len(self.positions) > 1 and are_opposite_directions(direction, self.direction):
            # Du kan inte göra en u-sväng om ormen är längre en ett!
            return
        else:
            self.direction = direction

    def move(self):
        current_x, current_y = self.positions[0]
        x, y = self.direction
        new = (((current_x+(x*GRID_PIXEL_SIZE))%SCREEN_WIDTH), (current_y+(y*GRID_PIXEL_SIZE))%SCREEN_HEIGHT)
        if len(self.positions) > 2 and new in self.positions[2:]:
            # Ormen kör över sig själv!
            self.is_alive = False
        else:
            # Lägg en ny första ruta
            self.positions.insert(0, new)
            # Om vi har inte har fått mer poäng, fäll bort den sista rutan
            if len(self.positions) > (self.score + 1):
                self.positions.pop()

    def reset(self):
        self.length = 1
        self.positions = [MIDDLE_COORDINATES]
        self.direction = get_random_direction()
        self.score = 0

    def draw(self,surface):
        for x, y in self.positions:
            r = pygame.Rect((x, y), (GRID_PIXEL_SIZE,GRID_PIXEL_SIZE))
            pygame.draw.rect(surface, GREEN, r)
            pygame.draw.rect(surface, BLACK, r, 2)

    def handle_keys(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.turn(UP)
                elif event.key == pygame.K_DOWN:
                    self.turn(DOWN)
                elif event.key == pygame.K_LEFT:
                    self.turn(LEFT)
                elif event.key == pygame.K_RIGHT:
                    self.turn(RIGHT)
                elif event.key == pygame.K_RETURN:
                    if not self.is_alive:
                        self.reset()
                        self.is_alive = True


class Food(object):
    def __init__(self):
        self.position = get_random_position()

    def draw(self, surface):
        r = pygame.Rect((self.position[0], self.position[1]), (GRID_PIXEL_SIZE, GRID_PIXEL_SIZE))
        pygame.draw.rect(surface, ORANGE, r)
        pygame.draw.rect(surface, BLACK, r, 2)
