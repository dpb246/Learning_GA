import population
import individual
from math import sqrt
class physics:
    def __init__(self, goal, engine):
        self.goal = goal
        self.engine = engine
        pass
    def clamp(self, minval, value, maxval):
        return sorted((value, minval, maxval))[1]
    def check(self, individuals, walls=[]):
        radius = self.engine.circle_size
        for person in individuals:
            if person.active(): continue
            #check walls
            x_p, y_p = person.get_pos()
            for wall in walls: #x, y, x_size, y_size
                x_w, y_w, x_size, y_size = wall
                distanceX = x_p - self.clamp(x_p, x_w, x_w+x_size)
                distanceY = y_p - self.clamp(y_p, y_w, y_w+y_size)
                if (distanceX * distanceX) + (distanceY * distanceY) < (radius * radius):
                    person.kill()
            #check edges
            if x_p-radius < 0 or x_p+radius > self.engine.x_size or y_p-radius < 0 or y_p+radius > self.engine.y_size:
                person.kill()
            #Check goal
            if (self.goal[0] - x_p)**2 + (self.goal[1] - y_p)**2 <= (radius*2)**2:
                person.win_game()
