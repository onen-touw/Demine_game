import pygame
import sys
import random

FPS = 30
fpsClock = pygame.time.Clock()
pygame.init()
pygame.display.set_caption("Demine_game")
screen_size = (1080, 800)
screen = pygame.display.set_mode(screen_size)

background = pygame.image.load("bg.png")

flag_img = pygame.image.load("flag.png")
flag_img = pygame.transform.scale(flag_img, (20, 20))
# num_1 = pygame.image.load("num_1.png")
# num_1 = pygame.transform.scale(num_1, (10, 10))
# screen.blit(num_1, (0, 0))

screen.blit(background, (0, 0))

WHITE = (255, 255, 255)
mine_fieldSize = 20

empty_field = pygame.image.load("empty.png")
empty_field = pygame.transform.scale(empty_field, (20, 20))

mas = [None] * mine_fieldSize
for i in range(mine_fieldSize):
    mas[i] = [None] * mine_fieldSize

RED = (255, 0, 0)

start_pos = [40, 40]

for i in range(20):
    for j in range(20):
        cir = pygame.draw.circle(screen, WHITE, start_pos, 10, 10)
        start_pos[0] += 30
        mas[i][j] = [cir, 0, 0, 0,
                     0]  # rect(x,y,?,?), bomb(1==true), open(1==true), has_flag(1==true), near_mine(1==True)
    start_pos[1] += 30
    start_pos[0] = 40

# for i in range(20):
#     print(mas[i])


for i in range(len(mas)):
    for j in range(4):
        rand_posI = random.randint(1, 20 - 2)
        rand_posJ = random.randint(1, 20 - 2)
        mas[rand_posI][rand_posJ][1] = 1

for i in range(20):
    print(mas[i])

for i in range(20):
    for j in range(20):
        if mas[i][j][1] == 1:
            # print(mas[i][j][0].x, '   ',mas[i][j][0].y )
            pygame.draw.circle(screen, RED, (mas[i][j][0].x + 10, mas[i][j][0].y + 10,), 10, 10)


def search_around(mas, i, j):
    if i < 1 or i > 18 or j < 1 or j > 18:
        return
    if mas[i][j][1] or mas[i][j][2]:
        return
    if mas[i][j][4] == 1:
        mas[i][j][2] = 1

    if mas[i][j][1] == 0 and mas[i][j][2] == 0 and mas[i][j][3] == 0 and mas[i][j][4] == 0:
        mas[i][j][2] = 1
        # print(mas[i][j]," ", i," ", j)
        search_around(mas, i + 1, j)
        search_around(mas, i - 1, j)
        search_around(mas, i, j + 1)
        search_around(mas, i, j - 1)
    else:
        return


for i in range(1, 20 - 1):
    for j in range(1, 20 - 1):
        if mas[i][j][1] == 0:
            x = mas[i][j][0].x
            y = mas[i][j][0].y
            rad = [
                mas[i][j - 1][1],
                mas[i][j + 1][1],
                mas[i + 1][j][1],
                mas[i + 1][j + 1][1],
                mas[i + 1][j - 1][1],
                mas[i - 1][j][1],
                mas[i - 1][j + 1][1],
                mas[i - 1][j - 1][1]
            ]
            count = 0
            for p in rad:
                if p == 1:
                    count += 1
            # print(count)
            if count > 0:
                img = pygame.image.load(f"num_{count}.png")
                screen.blit(img, (x, y))
                mas[i][j][4] = 1

for i in range(20):
    print(mas[i])
#
screen.blit(flag_img, (0, 0))
#
game = True
while True:
    fpsClock.tick(FPS)
    pos = pygame.mouse.get_pos()


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()



        # if event.type == pygame.MOUSEBUTTONDOWN
        if game:
            for i in range(1, 19):
                for j in range(1, 19):
                    if mas[i][j][0].collidepoint(pos) and event.type == pygame.MOUSEBUTTONDOWN:
                        if mas[i][j][1] == 1:
                            print("bomb")
                        #     проигрыш
                        else:
                            print("ok")
                            search_around(mas, i, j)
                        # рекурсия проверки
                        print(mas[i][j], "down")
    for i in range(1, 19):
        for j in range(1, 19):
            if mas[i][j][2] == 1 and mas[i][j][1] == 0:
                x = mas[i][j][0].x
                y = mas[i][j][0].y
                screen.blit(empty_field, (x, y))
    pygame.display.update()
