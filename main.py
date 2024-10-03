import threading
import time

import pygame, sys, os
import classes, rread, lread

WIDTH, HEIGHT = 1400, 800
CENTER = (WIDTH / 2, HEIGHT / 2)
EVENTS_ = [False, False]
LEVELS = [None]
LEVEL = 1
FLOORS = [pygame.sprite.Group()]
FLOORS_SHOW = [True]

for i in range(1, len(os.listdir(".\\assets\\levels\\")) + 1):
    LEVELS.append(lread.readLevel(i))

def init():
    global clock, trees, screen, players, player, effects, background, floors2
    pygame.init()

    # screen = pygame.display.set_mode((700, 500))
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("leave")

    clock = pygame.time.Clock()
    trees = pygame.sprite.Group()
    for i in range(len(os.listdir(".\\assets\\levels"))):
        FLOORS.append(pygame.sprite.Group())
        FLOORS_SHOW.append(False)
    players = pygame.sprite.Group()
    effects = pygame.sprite.Group()
    background = pygame.sprite.Group(classes.background((WIDTH, HEIGHT)))

    player = classes.player((CENTER[0], CENTER[1]-10))
    players.add(player)

    pygame.mixer.music.load("assets/sounds/background/noise.mp3")
    pygame.mixer.music.set_volume(0.1)

    def init_floors():
        for i in LEVELS[1]['floors']:
            FLOORS[LEVEL - 1].add(classes.floor(i['id'], (CENTER[0] + i['x'], CENTER[1] + -i['y']), player, i['bloom'], next_level))
        for i in LEVELS[1]['floors_l']:
            FLOORS[LEVEL].add(classes.floor(i['id'], (CENTER[0] + i['x'], CENTER[1] + -i['y']), player, i['bloom'], next_level))

    def init_effect():
        global white_boom
        white_boom = classes.whiteBoom(CENTER, (WIDTH, HEIGHT))
        effects.add(white_boom)

    init_floors()
    init_effect()

    pygame.mixer.music.play(-1)

def draw():
    global trees, players, effects, screen, background
    screen.fill((0, 0, 0))
    # screen.fill((155, 155, 155))

    background.update()
    background.draw(screen)

    for i in range(len(FLOORS)):
        FLOORS[i].update()
        if FLOORS_SHOW[i]:
            FLOORS[i].draw(screen)

    # trees.update()
    # trees.draw(screen)

    players.update()
    players.draw(screen)

    effects.update()
    effects.draw(screen)

def move():
    global player
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        player.move(-5, FLOORS)
    if keys[pygame.K_d]:
        player.move(5, FLOORS)

def events():
    def runevent(l):
        for i in LEVELS[l]['event']:
            if i['type'] == "sleep":
                time.sleep(i['value'])
            elif i['type'] == 'white_boom':
                white_boom.boom(background.sprites()[0])
            elif i['type'] == 'sound':
                pygame.mixer.Sound(f"assets/sounds/effect/{i['value']}.mp3").play()
            elif i['type'] == 'music':
                pygame.mixer.music.load(f"assets/sounds/background/{i['value']}.mp3")
            elif i['type'] == 'music_volume':
                pygame.mixer.music.set_volume(i['value'])
            elif i['type'] == 'play_music':
                pygame.mixer.music.play(-1)
            elif i['type'] == 'sevent':
                EVENTS_[i['value']] = not EVENTS_[i['value']]
            elif i['type'] == 'show':
                FLOORS_SHOW[i['value']] = not FLOORS_SHOW[i['value']]
            elif i['type'] == 'skin':
                player.skin(i['value'])

    if not EVENTS_[0]:
        for i in FLOORS[0]:
            if i.is_bloomed:
                pass
            else:
                break
        else:
            EVENTS_[0] = not EVENTS_[0]
            threading.Thread(target=runevent, args=(1,)).start()
            pygame.display.set_caption("LastStar[lsr]")

def next_level():
    global LEVEL, FLOORS_SHOW
    if LEVEL < len(LEVELS) - 1:
        LEVEL += 1
        for i in range(LEVEL):
            for j in FLOORS[i]:
                j.kill()
        for i in range(len(FLOORS_SHOW)):
            FLOORS_SHOW[i] = False
        FLOORS_SHOW.append(False)
        FLOORS_SHOW[LEVEL] = True
        FLOORS.append(pygame.sprite.Group())
        for i in LEVELS[LEVEL]['floors']:
            FLOORS[LEVEL].add(classes.floor(i['id'], (CENTER[0] + i['x'], CENTER[1] + -i['y']), player, i['bloom'], next_level))
        background.sprites()[0].setBackground(LEVELS[LEVEL]['background'])
        player.x = 0
        player.y = 200
        player.down(FLOORS)
        return
    else:
        pass

init()

while True:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE or event.key == pygame.K_w:
                player.jump(25, FLOORS)
            if event.key == pygame.K_k:
                player.x = 0
                player.y = 200
                player.down(FLOORS)
        if event.type == pygame.QUIT:
            pygame.quit()
            os._exit(0)
    events()
    move()
    draw()
    pygame.display.update()
    clock.tick(60)