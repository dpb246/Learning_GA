import sys,math

import pygame
from pygame.locals import *
from pygame.color import *

import pymunk
from pymunk.vec2d import Vec2d
import pymunk.pygame_util


width, height = 690,400
fps = 60
dt = 1./fps

def main():
    ### PyGame init
    pygame.init()
    screen = pygame.display.set_mode((width,height))

    clock = pygame.time.Clock()
    running = True
    font = pygame.font.SysFont("Arial", 16)

    ### Physics stuff
    space = pymunk.Space()
    space.gravity = 0,-1000
    draw_options = pymunk.pygame_util.DrawOptions(screen)

    static = [pymunk.Segment(space.static_body, (10, 50), (300, 50), 3)
                , pymunk.Segment(space.static_body, (300, 50), (325, 50), 3)
                , pymunk.Segment(space.static_body, (325, 50), (350, 50), 3)
                , pymunk.Segment(space.static_body, (350, 50), (375, 50), 3)
                , pymunk.Segment(space.static_body, (375, 50), (680, 50), 3)
                , pymunk.Segment(space.static_body, (680, 50), (680, 370), 3)
                , pymunk.Segment(space.static_body, (680, 370), (10, 370), 3)
                , pymunk.Segment(space.static_body, (10, 370), (10, 50), 3)
                ]
    # static platforms
    platforms = [pymunk.Segment(space.static_body, (170, 50), (270, 150), 3)
                #, pymunk.Segment(space.static_body, (270, 100), (300, 100), 5)
                , pymunk.Segment(space.static_body, (400, 150), (450, 150), 3)
                , pymunk.Segment(space.static_body, (400, 200), (450, 200), 3)
                , pymunk.Segment(space.static_body, (220, 200), (300, 200), 3)
                , pymunk.Segment(space.static_body, (50, 250), (200, 250), 3)
                , pymunk.Segment(space.static_body, (10, 370), (50, 250), 3)
                ]

    for s in static + platforms:
        s.friction = 1.
        s.group = 1
    space.add(static, platforms)












if __name__ == '__main__':
    sys.exit(main())
