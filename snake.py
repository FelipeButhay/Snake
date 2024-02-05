import pygame
import random
import snake_bot as bot
import tkinter as tk

resolution_screen = tk.Tk()
screen_x = resolution_screen.winfo_screenwidth()
screen_y = resolution_screen.winfo_screenheight()

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((screen_x, screen_y))

grid = 30, 18
sq = (screen_x*.8 + .99)//grid[0]
x_gap = (screen_x-sq*grid[0])*0.5
y_gap = (screen_y-sq*grid[1])*0.5

class snakec:
    def __init__(self, body, face):
        self.facing = face
        self.facing_save = face
        self.body = body
        self.head = body[-1]
        self.apple = False
        
    def move(self):
        self.body.append((self.body[-1][0] + self.facing[0], self.body[-1][1] + self.facing[1]))
        if not self.apple:
            self.body.pop(0)
        else:
            self.apple = False
        self.head = self.body[-1]
        
    def illegal(self):
        if len(self.body) > len(set(self.body)):
            return True

        for x in self.body:
            if x[0] >= grid[0] or x[0] < 0 or x[1] >= grid[1] or x[1] < 0:
                return True
        
        return False
    
    def draw(self):
        for x in self.body:
            pygame.draw.rect(screen, "green", (x_gap + sq*x[0], y_gap + sq*x[1], sq, sq))
        
class applec:
    def __init__(self):
        self.exist = False
        self.pos = None
        
    def spawn(self, body):
        self.exist = True
        while True:
            self.pos = random.randint(0, grid[0]-1), random.randint(0, grid[1]-1)
            if not self.pos in body:
                break
        
    def draw(self):
        pygame.draw.circle(screen, "red", (x_gap + sq*self.pos[0] + sq/2, y_gap + sq*self.pos[1] + sq/2), sq*.4)

snake = snakec([(3,3), (4,3), (5,3)], (1, 0))
apple = applec()
n = 0
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
            
    n += 1
    if n%20 == 0:
        snake.move()
        snake.facing_save = snake.facing
        if apple.pos in snake.body:
            snake.apple = True
            apple.exist = False
            apple.pos = None
        if snake.illegal():
            break
        
    if not apple.exist:
        apple.spawn(snake.body)
        
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]      and snake.facing_save != ( 0,  1):
        snake.facing = ( 0, -1)
    elif keys[pygame.K_DOWN]  and snake.facing_save != ( 0, -1):
        snake.facing = ( 0,  1)
    elif keys[pygame.K_LEFT]  and snake.facing_save != ( 1,  0):
        snake.facing = (-1,  0)
    elif keys[pygame.K_RIGHT] and snake.facing_save != (-1,  0):
        snake.facing = ( 1,  0)
            
    screen.fill(tuple(20 for x in range(0,3)))
    pygame.draw.rect(screen, tuple(50 for x in range(0,3)), (x_gap, y_gap, grid[0]*sq, grid[1]*sq))
    snake.draw()
    apple.draw()
            
    pygame.display.update()
    clock.tick(60)