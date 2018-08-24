import queue
import threading
class food:
    def __init__(self, x_size, y_size, goal):
        self.y_size = int((y_size+5)/5)
        self.x_size = int((x_size+5)/5)
        self.map = [[0 for i in range(self.x_size)] for j in range(self.y_size)]
        self.goal = goal

    def calc(self, row):
        for x in range(self.x_size):
            distance = (x-self.goal[0])**2 + (row-self.goal[1])**2
            self.map[row][x] += 1000 * 2**(-distance**0.2) #scale with time
    def worker(self):
        while True:
            row = self.q.get()
            if row is None:
                break
            self.calc(row)
            self.q.task_done()
    def upfood(self):
        self.q = queue.Queue()
        threads = []
        num_worker_threads = 2
        for i in range(num_worker_threads):
            t = threading.Thread(target=self.worker)
            t.start()
            threads.append(t)
        for row in range(self.y_size):
            self.q.put(row)
        # block until all tasks are done
        self.q.join()
        # stop workers
        for i in range(num_worker_threads):
            self.q.put(None)
        for t in threads:
            t.join()
    def get_food(self, pos):
        temp = self.map[int(pos[1]/5)][int(pos[0]/5)]/2
        self.map[int(pos[1]/5)][int(pos[0]/5)] /= 2
        return temp
