#DRAWING
import pygame

class draw:
    def __init__(self, screen=None):
        self.screen = screen
        self.XOFFSET = 0
        self.YOFFSET = 0
        self.PPM = 20.0  # pixels per meter
s = draw()
def _draw_polygon(polygon, body, fixture):
    vertices = [(body.transform * v) * s.PPM for v in polygon.vertices]
    vertices = [(v[0]+s.XOFFSET, s.YOFFSET - v[1]) for v in vertices]
    pygame.draw.polygon(s.screen, (49, 109, 206, 255), vertices)

def _draw_circle(circle, body, fixture):
    position = body.transform * circle.pos * s.PPM
    position = (position[0]+s.XOFFSET, s.YOFFSET - position[1])
    pygame.draw.circle(s.screen, (112, 10, 10, 255), [int(x) for x in position], int(circle.radius * s.PPM))

def fix_vertices(vertices):
        return [(int(s.XOFFSET + v[0]), int(s.YOFFSET-v[1])) for v in vertices]
def _draw_edge(edge, body, fixture):
        vertices = fix_vertices([body.transform * edge.vertex1 * s.PPM,
                                 body.transform * edge.vertex2 * s.PPM])
        pygame.draw.line(s.screen, (0, 127, 127, 255), vertices[0], vertices[1], 5)
