
import pygame
import sys
import pygame.time
import pygame.freetype
import random
import threading

from pygame.mixer_music import queue

pygame.init()

screen = pygame.display.set_mode((500, 700))
Font = pygame.freetype.Font('Sunflower.otf', 30)
Font_2 = pygame.freetype.Font(None, 50)
image = pygame.image.load('images/11.png').convert_alpha()
new_image = pygame.transform.scale(image, (500, 700))  # creating image
image_menu = pygame.image.load("images/меню.png").convert_alpha()
button_NG = pygame.Rect(70, 45, 360, 95) # расположение кнопки "новая игра"
button_exit = pygame.Rect(70, 150, 360, 100) # расположение кнопки "выход"
ifWin = None # isWin - who is a winner (False - bot, True - player, None = Nobody)
pygame.mixer.music.load('sound/Fon_music.mp3')
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.05)

sound1 = pygame.mixer.Sound('sound/otskok.ogg')
sound2 = pygame.mixer.Sound('sound/udar.mp3')
sound3 = pygame.mixer.Sound('sound/propusk.mp3')
sound4 = pygame.mixer.Sound('sound/proigrysh.mp3')
sound5 = pygame.mixer.Sound('sound/game-won.mp3')

def show_back():
    screen.blit(new_image, (0, 0))


# движение бота
def bot_mov():
    if Ball.centerx > Bot.centerx and Ball.centery < 300:
        Bot.x += 3
    if Ball.centerx < Bot.centerx and Ball.centery < 300:
        Bot.x -= 3


clock = pygame.time.Clock()
FPS = 60
menu = True

# создаём ракетки и мяч
Player = pygame.rect.Rect(205, 680, 100, 10)
Bot = pygame.rect.Rect(205, 10, 100, 10)
Ball = pygame.rect.Rect(245, 340, 20, 20)



# скорость мяча и игрока
player_mov = 0
Ball_x = random.choice([-3, 3, 4, -4])
Ball_y = random.choice([-3, 3, 4, -4])


def show_menu():
    global screen
    global image_menu
    global menu

    while menu:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if button_NG.collidepoint(event.pos):
                    print("Start new game!")
                    menu = False

                if button_exit.collidepoint(event.pos):
                    print("Exit!")
                    sys.exit()

        screen.blit(image_menu, (0, 0))
        pygame.display.flip()
        clock.tick(FPS)

def initBall():
    global Ball_x
    global Ball_y

    pygame.time.delay(2000)
    Ball_x = random.choice([-3, 3, 4, -4])
    Ball_y = random.choice([-3, 3, 4, -4])

def raund_begine():
    global Ball
    global Ball_y
    global Ball_x
    global ifWin

    Ball_x = 0
    Ball_y = 0
    Ball = pygame.rect.Rect(245, 340, 20, 20)

    if count_bot == 10:
        ifWin = False
    elif count_player == 10:
        ifWin = True

    else:
        threading.Thread(target=initBall, daemon=True).start()


# счётчик очков
count_player = 0
count_bot = 0
ifSoundPlay = False

def updateGame():
    global menu, count_player, count_bot, ifWin
    pygame.display.flip()
    pygame.time.delay(2000)

    count_player = 0
    count_bot = 0
    menu = True
    ifWin = None

    raund_begine()


while True:
    if menu:
        show_menu()
        continue

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_mov -= 4
            if event.key == pygame.K_RIGHT:
                player_mov += 4
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                player_mov = 0
            if event.key == pygame.K_RIGHT:
                player_mov = 0


    # крайние положения движения плеера
    if 0 <= Player.x + player_mov <= 400:
        Player.x += player_mov

    # проверка на пропуск мяча
    if Ball.centery > 700:
        count_bot += 1
        sound3.play()
        sound3.set_volume(0.1)
        raund_begine()

    if Ball.centery < 0:
        count_player += 1
        sound3.play()
        sound3.set_volume(0.1)
        raund_begine()

    # полёт мяча
    Ball.x -= Ball_x
    Ball.y += Ball_y

    # отскок мяча правый край
    if Ball.x >= 480:
        Ball_x = -Ball_x
        sound1.play()
        sound1.set_volume(0.1)

    # отскок мяча левый край
    if Ball.x <= 0:
        Ball_x = -Ball_x
        sound1.play()
        sound1.set_volume(0.1)

    # отскок мяча от игроков
    if Ball.colliderect(Player) or Ball.colliderect(Bot):
        if random.choice([True, False]):
            Ball_y += random.choice([0.1, 0.2, 0.3])
            Ball_x = -Ball_x
        if random.choice([True, False]):
            Ball_x += random.choice([1, 2, -1, -2])
        sound2.play()
        sound2.set_volume(0.1)
        Ball_y = -Ball_y

    show_back()
    Font.render_to(screen, (20, 20), f'Player: {count_player}', (255, 255, 255))
    Font.render_to(screen, (20, 40), f'Bot: {count_bot}', (255, 255, 255))
    bot_mov()
    pygame.draw.rect(screen, (20, 200, 20), Player)
    pygame.draw.rect(screen, (255, 0, 0), Bot)
    pygame.draw.ellipse(screen, (255, 255, 255), Ball)

    if ifWin == False:
        Font_2.render_to(screen, (90, 350), " You lose :(", (255, 0, 0))
        updateGame()

        if not ifSoundPlay:
            ifSoundPlay = True
            sound4.play()
            sound4.set_volume(0.1)

    elif ifWin == True:
        pygame.time.delay(2000)
        Font_2.render_to(screen, (10, 350), " You are WINNER :)", (0, 255, 0))
        updateGame()

        if not ifSoundPlay:
            ifSoundPlay = True
            sound5.play()
            sound5.set_volume(0.1)

    pygame.display.flip()
    clock.tick(FPS)
