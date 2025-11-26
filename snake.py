import pygame
import random
import time
import heapq

#------Window config------
SCREEN_WIDTH = 720
SCREEN_HEIGHT = 720
TILE_SIZE = 20
GIRD_WIDTH = SCREEN_WIDTH//TILE_SIZE
GRID_HEIGHT = SCREEN_HEIGHT//TILE_SIZE
FPS = 25

#---------------COLORS---------------
BLACK = "black"
AZURE = "azure4"
PATH_COLOR = "chartreuse3"
RED = "red"
BLUE = "royalblue1"

#snake game code

class SnakeAI:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.current_path = []
        pygame.display.set_caption("Snake game")
        self.clock = pygame.time.Clock()
        self.reset()

    def reset(self):
        #Start in the middle for starting of the game
        self.snake = [(5, 5), (5, 4), (5, 3)]
        self.direction = (0,1) #Moving up initially
        self.food = self.spawn_food()
        self.score = 0
    
    def spawn_food(self):
        while True:
            x = random.randint(0, GIRD_WIDTH - 1)
            y = random.randint(0, GRID_HEIGHT - 1)
            if (x, y) not in self.snake:
                return (x, y)
            
    def get_neighbours(self, node):
        x, y = node
        dir = [
                (0,1),
                (1, 0),
                (-1, 0),
                (0,-1)
        ]
        valid_neighbours = []
        for (dx, dy) in dir:
            nx, ny = x+dx,y+dy
            if (0<=nx<GIRD_WIDTH and
                0<=ny<GRID_HEIGHT):
                valid_neighbours.append((nx, ny))
        
        return valid_neighbours
    
    def heuristic(self, a, b):
        """
        Docstring for heuristic
        
        :param self: self
        :param a: coords of snake's head
        :param b: coords of food

        gets the dist between the head and the food
        """
        return abs(a[0]-b[0])+abs(a[1]-b[1])
    
    def a_star(self, start, target):
        count = 0
        open_set = []
        heapq.heappush(open_set, (0, count, start))

        parent = {}

        g_score = {start:0} #cost from start to curr node

        f_score = {start:self.heuristic(start, target)}

        open_set_hash = {start}
        obstactles = set(self.snake[:-1])

        while open_set:
            current = heapq.heappop(open_set)[2]
            open_set_hash.remove(current)

            if current == target:
                return self.reconstruct_path(parent, current)
            
            for neighbour in self.get_neighbours(current):
                if neighbour in obstactles:
                    continue
            
                t_g_score = g_score[current]+1

                if t_g_score<g_score.get(neighbour, float('inf')):
                    parent[neighbour] = current
                    g_score[neighbour] = t_g_score
                    f_score[neighbour] = t_g_score+self.heuristic(neighbour, target)

                    if neighbour not in open_set_hash:
                        count += 1
                        heapq.heappush(open_set, (f_score[neighbour], count, neighbour))
                        open_set_hash.add(neighbour)
        return []
    
    def reconstruct_path(self, parent, current):
        path = []
        while current in parent:
            path.append(current)
            current = parent[current]
        
        path.append(current)
        path.reverse()
        return path

    def get_ai_move(self):
        if not self.snake:
            return self.direction
        head = self.snake[0]

        path = self.a_star(head, self.food)
        self.current_path = path

        if len(path)>1:
            next_step = path[1]
            return (next_step[0] - head[0], next_step[1] - head[1])
        
        #if a* fails
        neighbours = self.get_neighbours(head)

        neighbours.sort(key=lambda n:self.heuristic(n, self.food))

        for n in neighbours:
            if n not in self.snake[:-1]:
                return (n[0]-head[0], n[1]-head[1])
            
    def update(self):
        if not self.snake:
            return
        self.direction= self.get_ai_move()

        head_x, head_y = self.snake[0]
        dx, dy = self.direction
        new_head = (head_x+dx, head_y+dy)

        #Collsion detection
        if(new_head[0]<0 or new_head[0]>=GIRD_WIDTH or
            new_head[1]<0 or new_head[1]>=GRID_HEIGHT or
            new_head in self.snake):
            print(f"Game over! Score:{self.score}")
            self.reset()
            return
        self.snake.insert(0, new_head)
    
        #eat food
        if new_head == self.food:
            self.score += 1
            self.food = self.spawn_food()
        else:
            self.snake.pop()
    
    def draw(self):
        self.screen.fill(BLACK)

        #draw grid
        for x in range(0, SCREEN_WIDTH, TILE_SIZE):
            pygame.draw.line(self.screen, AZURE, (x, 0), (x, SCREEN_HEIGHT))
        for y in range(0, SCREEN_HEIGHT, TILE_SIZE):
            pygame.draw.line(self.screen, AZURE, (0, y), (SCREEN_WIDTH, y))
        
        #draw path
        if len(self.current_path)>1:
            for node in self.current_path:
                rect = pygame.Rect(
                    node[0]*TILE_SIZE+TILE_SIZE//2,
                    node[1]*TILE_SIZE+TILE_SIZE//2,
                    TILE_SIZE//3, TILE_SIZE//3
                )
                pygame.draw.rect(self.screen, PATH_COLOR, rect)

        #draw snake
        for i, segment in enumerate(self.snake):
            rect = pygame.Rect(
                segment[0]*TILE_SIZE, segment[1]*TILE_SIZE, TILE_SIZE-1, TILE_SIZE-1
            )
            color = BLUE if i == 0 else "royalblue3"
            pygame.draw.rect(self.screen, color, rect)
        
        #draw food
        food_rect = pygame.Rect(
            self.food[0]*TILE_SIZE, self.food[1]*TILE_SIZE, TILE_SIZE, TILE_SIZE
        )
        pygame.draw.rect(self.screen, RED, food_rect)

        pygame.display.flip()

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    self.reset()
                
            self.update()
            self.draw()
            self.clock.tick(FPS)

        pygame.quit()


if __name__ == "__main__":
    game = SnakeAI()
    game.run()            
