import pygame
import random
import os

pygame.mixer.init()


pygame.init()
clock = pygame.time.Clock()

#colors
white = (255,255,255)
red = (255,0,0)
black=(0,0,0)

screen_width = 1100
screen_height = 600

#Creating Window
gameWindow=pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption("Ateeb The Snake")
pygame.display.update()
font = pygame.font.SysFont(None, 40)

gameover = pygame.image.load("Gameover.jpg")
gameover = pygame.transform.scale(gameover, (screen_width, screen_height)).convert_alpha()
startimage = pygame.image.load("FirstPage.jpg")
startimage = pygame.transform.scale(startimage, (screen_width, screen_height)).convert_alpha()

bgimg = pygame.image.load("snake.jpg")
bgimg = pygame.transform.scale(bgimg, (screen_width, screen_height)).convert_alpha()


def screen_score(text,color,x,y):
    screen_text=font.render(text, True, color)
    gameWindow.blit(screen_text,[x,y])

def plot_snake(gameWindow,color, snake_list,snake_size):
    for x,y in snake_list:
        pygame.draw.rect(gameWindow, color, [x, y, snake_size, snake_size])

def welcome():
    exit_game = False
    while not exit_game:
        pygame.mixer.music.load("back.mp3")
        pygame.mixer.music.play()
        gameWindow.blit(startimage, (0, 0))
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                exit_game=True
            if event.type == pygame.KEYDOWN:
                if event.key==pygame.K_SPACE:
                    pygame.mixer.music.stop()
                    gameloop()
        pygame.display.update()
        clock.tick(60)
#Game Loop
def gameloop():
    exit_game = False
    game_over = False
    snake_x = 45
    snake_y = 55
    velocity_x = 0
    velocity_y = 0
    snake_size = 10
    fps = 40
    food_x = random.randint(0, screen_width / 2)
    food_y = random.randint(0, screen_height / 2)
    score = 0
    init_velocity = 5
    snake_list = []
    snake_length = 1
    #Check if file exists
    if not (os.path.exists("snake highscore.txt")):
        with open("snake highscore.txt","w") as f:
            f.write("0")
    with open("snake highscore.txt", "r") as f:
        highscore = int(f.read())

    while not exit_game:
        if game_over:
            with open("snake highscore.txt","w") as f:
                f.write(str(highscore))
            gameWindow.fill(white)
            gameWindow.blit(gameover, (0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True
                if event.type == pygame.KEYDOWN:
                    if event.key==pygame.K_RETURN:
                        gameloop()
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True
                if event.type == pygame.KEYDOWN:
                    # Moving the Snake
                    if event.key==pygame.K_RIGHT:
                        velocity_x=init_velocity
                        velocity_y=0
                    if event.key==pygame.K_LEFT:
                        velocity_x=-init_velocity
                        velocity_y=0
                    if event.key==pygame.K_DOWN:
                        velocity_y=init_velocity
                        velocity_x=0
                    if event.key==pygame.K_UP:
                        velocity_y=-init_velocity
                        velocity_x=0
                    if event.key==pygame.K_q:
                        score+=10
            snake_x+=velocity_x
            snake_y+=velocity_y

            if abs(snake_x-food_x) < 6 and abs(snake_y-food_y)<6:
                pygame.mixer.music.load("point.wav")
                pygame.mixer.music.play()
                score += 10
                food_x = random.randint(0, int(screen_width/2))
                food_y = random.randint(0, int(screen_height/2))
                snake_length += 5

                if score>highscore:
                    highscore=score

            gameWindow.fill(white)
            gameWindow.blit(bgimg, (0, 0))
            screen_score(f"Score : {score}", red, 5, 5)
            screen_score(f"Highscore : {highscore}", red, 5, 5+30)
            pygame.draw.rect(gameWindow, red, [food_x, food_y, snake_size, snake_size])

            head=[]
            head.append(snake_x)
            head.append(snake_y)
            snake_list.append(head)

            if len(snake_list) > snake_length:
                del snake_list[0]
            if head in snake_list[:-1]:
                pygame.mixer.music.load("over.mp3")
                pygame.mixer.music.play()
                pygame.mixer.music.load("Game Over1.mp3")
                pygame.mixer.music.play()
                game_over=True
            if snake_x<0 or snake_x>screen_width or snake_y>screen_height or snake_y<0:
                pygame.mixer.music.load("over.mp3")
                pygame.mixer.music.play()
                pygame.mixer.music.load("Game Over1.mp3")
                pygame.mixer.music.play()
                game_over=True

            # pygame.draw.rect(gameWindow, black, [snake_x,snake_y,snake_size,snake_size])
            plot_snake(gameWindow,black, snake_list,snake_size)
        pygame.display.update()
        clock.tick(fps)
    pygame.quit()
    quit()
welcome()


