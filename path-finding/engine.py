import pygame
'''
Class that handles drawing all the walls, circles, and goal
Pass Frame() the list of circles and walls
'''
class Render_Engine:
    def __init__(self, screen, goal_pos, screen_size):
        self.x_size, self.y_size = screen_size
        self.screen = screen
        self.circle_colour = (66, 134, 244) #Light blue
        self.circle_size = 5
        self.black = (0,0,0)
        self.goal_colour = (196, 54, 39) #Red
        self.goal_pos = goal_pos
    def frame(self, circles, walls=[]):
        self.screen.fill((255,255,255))
        self.draw_walls(walls)
        self.draw_circles(circles)
        self.draw_goal()
        pygame.display.update()
    def draw_goal(self):
        pygame.draw.circle(self.screen, self.goal_colour, self.goal_pos, self.circle_size, 0)
    def draw_walls(self, walls):
        for wall in walls:
            pygame.draw.rect(self.screen, self.black, wall, 0)
    def draw_circles(self, circles):
        if len(circles) < 1: return 0
        for i in range(1, len(circles)):
            pygame.draw.circle(self.screen, self.circle_colour, circles[i], self.circle_size, 0)
        pygame.draw.circle(self.screen, (21, 175, 72), circles[0], self.circle_size, 0)#Draw the first one as a different colour since it was the best one from last gen
