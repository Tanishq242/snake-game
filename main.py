import sys
import random
import pygame

clk = pygame.time.Clock()
pygame.init()
width = 800
height = 500
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Snake Game')
image = pygame.image.load("first.jpg")
bg_image = pygame.transform.scale(image, (800, 500))

x, y = 200, 200
BLACK = (0, 0, 0)
bg_clr = (127, 179, 213)
food_clr = (244, 208, 63)
speed = 1
move = x
ind = 0
temp_x  = 0
temp_y  = 0
food_coord_x = 25 * random.randint(2, 30)
food_coord_y = 25 * random.randint(2, 18)
flag = False
snake_body = [[200, 200], [175, 200]]
direction_flag = [False, False, True, False]


def render_text(size, number, text_pos_x, text_pos_y, txt_color=(255, 255, 255)):
    font = pygame.font.SysFont(None, size)
    ren = font.render(number, True, txt_color)
    screen.blit(ren, (text_pos_x, text_pos_y))


def main_loop(food_x, food_y):
    score = 0
    vertical = False
    horizontal = True
    fps = 2
    rec_score = 50
    msg = None
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # FOR DIRECTION CHANGE OF SNAKE
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and vertical == True:
                    direction_flag[3] = True
                    direction_flag[2] = False
                    direction_flag[1] = False
                    direction_flag[0] = False
                    vertical = False
                    horizontal = True
                elif event.key == pygame.K_RIGHT and vertical == True:
                    direction_flag[2] = True
                    direction_flag[3] = False
                    direction_flag[1] = False
                    direction_flag[0] = False
                    vertical = False
                    horizontal = True
                elif event.key == pygame.K_UP and horizontal == True:
                    direction_flag[0] = True
                    direction_flag[2] = False
                    direction_flag[1] = False
                    direction_flag[3] = False
                    horizontal = False
                    vertical = True
                elif event.key == pygame.K_DOWN and horizontal == True:
                    direction_flag[1] = True
                    direction_flag[0] = False
                    direction_flag[2] = False
                    direction_flag[3] = False
                    horizontal = False
                    vertical = True

        # WHEN FOOD EATEN
        screen.fill(bg_clr)

        # SCORE BAR
        pygame.draw.rect(screen, [33, 47, 61], [0, 0, 800, 30])
        render_text(30, "Score: "+str(score), 5, 5, (255, 255, 255))

        # FOOD
        pygame.draw.rect(screen, food_clr, [food_x, food_y, 20, 20], border_radius=20)

        # SNAKE BODY MOVEMENT
        if direction_flag[0]:
            snake_body.insert(0, [snake_body[0][0], snake_body[0][1] - 25])
        elif direction_flag[1]:
            snake_body.insert(0, [snake_body[0][0], snake_body[0][1] + 25])
        elif direction_flag[2]:
            snake_body.insert(0, [snake_body[0][0] + 25, snake_body[0][1]])
        elif direction_flag[3]:
            snake_body.insert(0, [snake_body[0][0] - 25, snake_body[0][1]])

        # Check if snake eats food
        if snake_body[0][0] == food_x and snake_body[0][1] == food_y:
            pygame.mixer.music.load("food_eat_sound.mp3")
            pygame.mixer.music.play()
            food_x = 25 * random.randint(2, 30)
            food_y = 25 * random.randint(2, 18)
            score += 10
        else:
            snake_body.pop()  # Remove last segment (keep the length constant)

        # FOR SELF COLLISION
        for ind in snake_body[1:]:
            if ind[0] == snake_body[0][0] and ind[1] == snake_body[0][1]:
                msg = "You Collided with own body!"
                end_screen(msg)

        # FOR BORDER COLLISION
        if (snake_body[0][0] > 795 or snake_body[0][0] < 0) or (snake_body[0][1] > 495 or snake_body[0][1] < 25):
            msg = "You Collided with border!"
            end_screen(msg)

        # RENDERING SNAKE
        pygame.draw.rect(screen, [231, 76, 60], [snake_body[0][0], snake_body[0][1], 20, 20])
        for i in snake_body[1:]:
            pygame.draw.rect(screen, BLACK, [i[0], i[1], 20, 20])

        # SCORE RECORDER FOR FPS INCREASE
        if rec_score == score:
            rec_score += 50
            fps += 2

        # print(snake_body)
        pygame.display.update()
        clk.tick(fps)

def end_screen(msg):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    snake_body.clear()
                    snake_body.append([200, 200])
                    snake_body.append([175, 200])
                    main_loop(25 * random.randint(2, 30), 25 * random.randint(2, 18))

        screen.fill([0, 0, 0])
        render_text(70, msg, 80, 150, [255, 255, 255])
        pygame.draw.rect(screen, [243, 156, 18], [320, 400, 150, 40], border_radius=15)
        render_text(30, "Press Enter", 340, 410, [255, 255, 255])
        pygame.display.update()

def intro(photo):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:  # Detect mouse click
                x, y = event.pos  # Get click position
                if (100 < x < 250) and (300 < y < 350):
                    main_loop(food_coord_x, food_coord_y)
                elif (100 < x < 250) and (370 < y <420):
                    pygame.quit()
                    sys.exit()

        screen.blit(photo, [0, 0])
        render_text(100, "SNAKE MANIA", 155, 80)
        pygame.draw.rect(screen, [249, 231, 159], [100, 300, 150, 50], border_radius=15)
        render_text(35, "Start Game", 110, 310, [0, 0, 0])
        pygame.draw.rect(screen, [249, 231, 159], [100, 370, 150, 50], border_radius=15)
        render_text(35, "Quit Game", 110, 383, [0, 0, 0])
        pygame.display.update()



intro(bg_image)
# main_loop(food_coord_x, food_coord_y)
# end_screen("You Collided with own body!")