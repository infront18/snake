import pygame     
import time
from datetime import datetime
from datetime import timedelta
import random

RED = 255, 0, 0      
GREEN = 0, 255, 0  
BLUE = 0, 0, 255   
PURPLE = 127, 0, 127 
BLACK = 0, 0, 0     
GRAY = 127, 127, 127
WHITE = 255, 255, 255 

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 400
BLOCK_SIZE = 20

class Snake:
    color = GREEN  

    def __init__(self):
        self.positions = [(9, 6), (9, 7), (9, 8), (9, 9)]  
        self.direction = 'north'  

    def draw(self, screen):
        for position in self.positions:  
            #draw_block(screen, self.color, position)
            draw_image_block(screen, circleImg, position)  

    def crawl(self):
        head_position = self.positions[0]
        y, x = head_position
        if self.direction == 'north':
            self.positions = [(y - 1, x)] + self.positions[:-1]
        elif self.direction == 'south':
            self.positions = [(y + 1, x)] + self.positions[:-1]
        elif self.direction == 'west':
            self.positions = [(y, x - 1)] + self.positions[:-1]
        elif self.direction == 'east':
            self.positions = [(y, x + 1)] + self.positions[:-1]

    def turn(self, direction):
        if self.direction == 'north' and direction == 'south':
            print("north => south")
            return
        if self.direction == 'south' and direction == 'north':
            print("north => south")
            return
        if self.direction == 'west' and direction == 'east':
            print("west => east")
            return
        if self.direction == 'east' and direction == 'west':
            print("east => west")
            return

        self.direction = direction
        

    def grow(self):
        tail_position = self.positions[-1]
        y, x = tail_position
        if self.direction == 'north':
            self.positions.append((y - 1, x))
        elif self.direction == 'south':
            self.positions.append((y + 1, x))
        elif self.direction == 'west':
            self.positions.append((y, x - 1))
        elif self.direction == 'east':
            self.positions.append((y, x + 1))



class Apple:
    color = RED  

    def __init__(self, position=(5, 5)):
        self.position = position   

    def draw(self, screen):
        #draw_block(screen, self.color, self.position)
        draw_image_block(screen, appleImg, self.position)  

class GameBoard:
    width = 20   
    height = 20  

    def __init__(self):
        self.snake = Snake() 
        self.apple = Apple() 

    def draw(self, screen):
        self.apple.draw(screen) 
        self.snake.draw(screen)

    def process_turn(self):
        self.snake.crawl()  

        #뱀 머리와 몸통이 충돌되었는지? 체크 
        if self.snake.positions[0] in self.snake.positions[1:]:
            raise SnakeCollisionException()  

        #뱀 머리가 벽에 충돌되었는지? 체크
        if self.snake.positions[0][0] < 0 or self.snake.positions[0][1] < 0 or self.snake.positions[0][0] >= 20 or self.snake.positions[0][1] >= 20  :
            raise SnakeCollisionException()  


        if self.snake.positions[0] == self.apple.position:
            self.snake.grow()    
            self.put_new_apple()

    def put_new_apple(self):
        self.apple = Apple((random.randint(0, 19), random.randint(0, 19)))
        for position in self.snake.positions:   
            if self.apple.position == position:  
                self.put_new_apple()             
                break


def draw_background(screen):
    background = pygame.Rect((0, 0), (SCREEN_WIDTH, SCREEN_HEIGHT))
    #pygame.draw.rect(screen, WHITE, background)
    screen.blit(bgImg, background)

def draw_block(screen, color, position):
    block = pygame.Rect((position[1] * BLOCK_SIZE, position[0] * BLOCK_SIZE),
                        (BLOCK_SIZE, BLOCK_SIZE))
    pygame.draw.rect(screen, color, block)


def draw_image_block(screen, img, position):
    block = pygame.Rect((position[1] * BLOCK_SIZE, position[0] * BLOCK_SIZE),
                        (BLOCK_SIZE, BLOCK_SIZE))
    screen.blit(img, block)
    
    


class SnakeCollisionException(Exception):
    """뱀 충돌 예외"""
    pass


pygame.init()          

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

DIRECTION_ON_KEY = {
    pygame.K_UP: 'north',
    pygame.K_DOWN: 'south',
    pygame.K_LEFT: 'west',
    pygame.K_RIGHT: 'east',
}
block_direction = 'east' 
block_position = [0, 0] 
last_moved_time = datetime.now()
game_status_ing = True

bgImg = pygame.image.load('bg_grass.png')
gameoverImg = pygame.image.load('gameover.png')
circleImg = pygame.image.load('circle.png')
appleImg = pygame.image.load('apple.png')


game_board = GameBoard()

TURN_INTERVAL = timedelta(seconds=0.3)
last_turn_time = datetime.now()

while True:

    if game_status_ing == True:
        draw_background(screen)    
        
    events = pygame.event.get() 
    for event in events:       
        if event.type == pygame.QUIT: 
            exit()     

        if event.type == pygame.KEYDOWN:  
            if event.key in DIRECTION_ON_KEY:
                game_board.snake.turn(DIRECTION_ON_KEY[event.key])
            if game_status_ing == False:
                game_status_ing = True;
                game_board = GameBoard()

    if TURN_INTERVAL < datetime.now() - last_turn_time:        
        try:
            if game_status_ing == True:
                game_board.process_turn()
        except SnakeCollisionException:
            print("Game Over")            
            
            game_status_ing = False
            
            #time.sleep(3) 
            #exit()
        last_turn_time = datetime.now()

    game_board.draw(screen)

    if game_status_ing == False:
        drawPos = pygame.Rect((-60, -60), (250, 250))
        screen.blit(gameoverImg, drawPos)
        font = pygame.font.Font('freesansbold.ttf', 21)
        text = font.render('Press any key to restart game!!', True, GREEN, BLUE)
        textRect = text.get_rect()
        textRect.center = (400 / 2, 400 / 1.5)
        screen.blit(text, textRect)

               
    pygame.display.update()
                
