#!/usr/bin/env python
"""
An attempt at some basic tests of the required functionality
"""
import pygame
from pygame.locals import (QUIT, KEYDOWN, K_ESCAPE)
import random
from Box2D import * # The main library
# Box2D.b2 maps Box2D.b2Vec2 to vec2 (and so on)
from Box2D.b2 import (world, polygonShape, circleShape, edgeShape, staticBody, dynamicBody)

# --- constants ---
# Box2D deals with meters, but we want to display pixels,
# so define a conversion factor:
PPM = 20.0  # pixels per meter
TARGET_FPS = 60
TIME_STEP = 1.0 / TARGET_FPS
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
XOFFSET = 0
YOFFSET = SCREEN_HEIGHT

# --- pygame setup ---
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Simple car demo')
clock = pygame.time.Clock()

# --- pybox2d world setup ---
# Create the world
world = world(gravity=(0, -10), doSleep=True)

# The ground -- create some terrain
ground = world.CreateStaticBody(
    shapes=b2EdgeShape(vertices=[(-20, 0), (40, 0)])
)

x, y1, dx = 40, 0, 4
vertices = [0.25, 1, 4, 0, 0, -1, -2, -2, -1.25, 0]
def add_ground():
    global x, y1, dx
    print("Adding")
    for y2 in vertices*2:  # iterate through vertices multiple times
        ground.CreateEdgeFixture(
            vertices=[(x, y1), (x + dx, y2)],
            density=0,
            friction=0.1,
        )
        y1 = y2
        x += dx
add_ground()
# Create a car with 2 wheels
box = world.CreateDynamicBody(
    position=(25, 4),
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
        friction=1,
        density=1
    )
)
wheel2 = world.CreateDynamicBody(
    position=(23.75, 3),
    fixtures=b2FixtureDef(
        shape=b2CircleShape(radius=1),
        friction=1,
        density=1
    )
)
spring = world.CreateWheelJoint(
            bodyA=box,
            bodyB=wheel,
            anchor=wheel.position,
            axis=(0.0, 1.0),
            motorSpeed=-40.0,
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
            motorSpeed=-10.0,
            maxMotorTorque=50,
            enableMotor=True,
            frequencyHz=10,
            dampingRatio=0.7
        )

#DRAWING
colors = {
    dynamicBody: (255, 255, 255, 255),
    staticBody: (0, 127, 127, 255),
}
def my_draw_polygon(polygon, body, fixture):
    vertices = [(body.transform * v) * PPM for v in polygon.vertices]
    vertices = [(v[0]+XOFFSET, YOFFSET - v[1]) for v in vertices]
    pygame.draw.polygon(screen, colors[body.type], vertices)
polygonShape.draw = my_draw_polygon

def my_draw_circle(circle, body, fixture):
    position = body.transform * circle.pos * PPM
    position = (position[0]+XOFFSET, YOFFSET - position[1])
    pygame.draw.circle(screen, colors[body.type], [int(
        x) for x in position], int(circle.radius * PPM))
circleShape.draw = my_draw_circle

def fix_vertices(vertices):
        return [(int(XOFFSET + v[0]), int(YOFFSET-v[1]))
                for v in vertices]
def _draw_edge(edge, body, fixture):
        vertices = fix_vertices([body.transform * edge.vertex1 * PPM,
                                 body.transform * edge.vertex2 * PPM])
        pygame.draw.line(screen, colors[body.type], vertices[0], vertices[1], 5)
edgeShape.draw = _draw_edge

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
            #continue
            fixture.shape.draw(body, fixture)

    # Make Box2D simulate the physics of our world for one step.
    world.Step(TIME_STEP, 10, 10)
    if x < box.position[0]+30:
        add_ground()
    #Have screen follow the car
    XOFFSET = (-box.position[0]) * PPM + SCREEN_WIDTH // 2
    YOFFSET = (box.position[1]) * PPM + SCREEN_HEIGHT // 2

    # Flip the screen and try to keep at the target FPS
    pygame.display.flip()
    clock.tick(TARGET_FPS)

pygame.quit()
print('Done!')
