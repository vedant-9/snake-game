#Modules
import pygame 
import random
import os

#Colours
white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)

#Intro
pygame.init()
pygame.mixer.init()
screen_width = 700
screen_height = 400
gamewindow = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption("Snake Game")
font = pygame.font.SysFont(None, 50)
clock = pygame.time.Clock()

#Background Image
bgimg = pygame.image.load("bgimg.jpg")
bgimg = pygame.transform.scale(bgimg, (screen_width, screen_height)).convert_alpha()

#Displaying Score
def text_screen(text, color, x, y):
    screen_text = font.render(text,True,color)
    gamewindow.blit(screen_text, [x, y])

#Plotting Snake
def plot_snake(gamewindow, color , snake_rect_list, snake_size):
    for x,y in snake_rect_list:
        pygame.draw.rect(gamewindow, color , [x, y, snake_size, snake_size])

#Gameloop
def gameloop():
    exit_game = False
    game_over = False
    fps = 30
    snake_x = 40
    snake_y = 40
    snake_size = 10
    init_velocity = 5
    velocity_x = 0
    velocity_y = 0
    food_x = random.randint(20,200)
    food_y = random.randint(20,300)
    score = 1
    snake_length = 1
    snake_rect_list = []
    #For Highscore
    if not os.path.exists("highscore.txt"):
        with open("highscore.txt","w") as f:
            f.write("0")
    with open("highscore.txt","r") as f:
        high_score = f.read()

    while not exit_game:
        if game_over:
            text_screen("GAME OVER Press Enter To Continue!",red,20,150)
            with open("highscore.txt","w") as f:
                f.write(high_score)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        gameloop()
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        velocity_x = init_velocity
                        velocity_y = 0
                    if event.key == pygame.K_LEFT:
                        velocity_x = -init_velocity
                        velocity_y = 0
                    if event.key == pygame.K_UP:
                        velocity_y = -init_velocity
                        velocity_x = 0
                    if event.key == pygame.K_DOWN:
                        velocity_y = init_velocity
                        velocity_x = 0
                    
            snake_x += velocity_x
            snake_y += velocity_y

            if abs(snake_x-food_x)<8 and abs(snake_y-food_y)<8:
                score+=1
                pygame.mixer.music.load('eatsound.mp3')
                pygame.mixer.music.play()
                food_x = random.randint(0,screen_width)
                food_y = random.randint(0,screen_height)
                snake_length += 3
                if score > int(high_score):
                    high_score = str(score)

            gamewindow.fill(white)
            gamewindow.blit(bgimg, (0, 0))
            text_screen("Score: " + str(score)+ " Highscore: " + high_score,blue,5,5)
            pygame.draw.rect(gamewindow, green , [food_x, food_y, snake_size, snake_size])

            snake_rect_list.append([snake_x,snake_y])
            if len(snake_rect_list) > snake_length:
                del snake_rect_list[0]

            if [snake_x,snake_y] in snake_rect_list[:-1]:
                game_over = True
                pygame.mixer.music.load('gameover.mp3')
                pygame.mixer.music.play()
            if snake_x<0 or snake_x>screen_width or snake_y<0 or snake_y>screen_height:
                game_over = True
                pygame.mixer.music.load('gameover.mp3')
                pygame.mixer.music.play()

            plot_snake(gamewindow, red , snake_rect_list, snake_size)
            
        pygame.display.update()
        clock.tick(fps)

    pygame.quit()
    quit()

gameloop()