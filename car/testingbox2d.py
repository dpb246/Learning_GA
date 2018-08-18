#!/usr/bin/env python
"""
An attempt at some basic tests of the required functionality
"""
import pygame
from pygame.locals import (QUIT, KEYDOWN, K_ESCAPE)

from Box2D import * # The main library
# Box2D.b2 maps Box2D.b2Vec2 to vec2 (and so on)
from Box2D.b2 import (world, polygonShape, circleShape, staticBody, dynamicBody)

# --- constants ---
# Box2D deals with meters, but we want to display pixels,
# so define a conversion factor:
PPM = 20.0  # pixels per meter
TARGET_FPS = 60
TIME_STEP = 1.0 / TARGET_FPS
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
SIDE_SCROLL = 0

# --- pygame setup ---
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Simple pygame example')
clock = pygame.time.Clock()

# --- pybox2d world setup ---
# Create the world
world = world(gravity=(0, -10), doSleep=True)

# And a static body to hold the ground shape
ground_body = world.CreateStaticBody(position=(0, 0), shapes=polygonShape(box=(50, 1)))

# Create a couple dynamic bodies
box = world.CreateDynamicBody(
    position=(25, 4),
    fixtures=b2FixtureDef(
        shape=b2PolygonShape(box=(2.5, 1)),
        friction=0.2,
        density=1
    )
)
box2 = world.CreateDynamicBody(
    position=(30, 4),
    fixtures=b2FixtureDef(
        shape=b2PolygonShape(box=(2.5, 1)),
        friction=0.2,
        density=1
    )
)
wheel = world.CreateDynamicBody(
    position=(26.25, 3),
    fixtures=b2FixtureDef(
        shape=b2CircleShape(radius=1),
        friction=0.3,
        density=1
    )
)
wheel2 = world.CreateDynamicBody(
    position=(23.75, 3),
    fixtures=b2FixtureDef(
        shape=b2CircleShape(radius=1),
        friction=0.3,
        density=1
    )
)
spring = world.CreateWheelJoint(
            bodyA=box,
            bodyB=wheel,
            anchor=wheel.position,
            axis=(0.0, 1.0),
            motorSpeed=10.0,
            maxMotorTorque=50,
            enableMotor=True,
            frequencyHz=10,
            dampingRatio=0.7
        )
spring2 = world.CreateWheelJoint(
            bodyA=box,
            bodyB=wheel2,
            anchor=wheel2.position,
            axis=(0.0, 1.0),
            motorSpeed=10.0,
            maxMotorTorque=50,
            enableMotor=True,
            frequencyHz=10,
            dampingRatio=0.7
        )
colors = {
    staticBody: (255, 255, 255, 255),
    dynamicBody: (127, 127, 127, 255),
}

# Let's play with extending the shape classes to draw for us.

def my_draw_polygon(polygon, body, fixture):
    vertices = [(body.transform * v) * PPM for v in polygon.vertices]
    vertices = [(v[0]-SIDE_SCROLL, SCREEN_HEIGHT - v[1]) for v in vertices]
    pygame.draw.polygon(screen, colors[body.type], vertices)
polygonShape.draw = my_draw_polygon

def my_draw_circle(circle, body, fixture):
    position = body.transform * circle.pos * PPM
    position = (position[0]-SIDE_SCROLL, SCREEN_HEIGHT - position[1])
    pygame.draw.circle(screen, colors[body.type], [int(
        x) for x in position], int(circle.radius * PPM))
    # Note: Python 3.x will enforce that pygame get the integers it requests,
    #       and it will not convert from float.
circleShape.draw = my_draw_circle

# --- main game loop ---

running = True
while running:
    # Check the event queue
    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            # The user closed the window or pressed escape
            running = False

    screen.fill((0, 0, 0, 0))
    # Draw the world
    for body in world.bodies:
        for fixture in body.fixtures:
            fixture.shape.draw(body, fixture)

    # Make Box2D simulate the physics of our world for one step.
    world.Step(TIME_STEP, 10, 10)

    #Have screen follow the car
    SIDE_SCROLL = (box.position[0]) * PPM - SCREEN_WIDTH // 2
    print(SIDE_SCROLL)
    # Flip the screen and try to keep at the target FPS
    pygame.display.flip()
    clock.tick(TARGET_FPS)

pygame.quit()
print('Done!')
