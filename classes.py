import threading

import pygame, math, time
from PIL import Image, ImageFilter


class floor(pygame.sprite.Sprite):
    def __init__(self, id_, pos, player, check=False, next_level=None):
        super().__init__()
        self.image_id = id_
        self.pos = pos
        self.check = check
        self.player = player
        self.ni = pygame.transform.scale(pygame.image.load(f".\\assets\\images\\floors\\floor{self.image_id}.png").convert_alpha(), (320, 180))
        self.image = pygame.surface.Surface(self.ni.size).convert_alpha()
        self.image.fill((0, 0, 0, 0))
        self.image.blit(self.ni, self.ni.get_rect())
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.centerx = self.pos[0]
        self.rect.centery = self.pos[1]
        self.is_bloomed = False
        self.next_level = next_level

    def bloom(self):
        def bloom_():
            self.bi = pygame.transform.scale(pygame.image.load(f".\\assets\\images\\floors\\floor{self.image_id}-bloom.png").convert_alpha(), (320, 180))
            rect = self.bi.get_rect()
            # rect.x -= 40
            # rect.y -= 25.5
            for i in range(0, 255, 15):
                self.bi.set_alpha(i)
                self.image = pygame.surface.Surface(self.ni.size).convert_alpha()
                self.image.fill((0, 0, 0, 0))
                self.image.blit(self.ni, self.ni.get_rect())
                self.image.blit(self.bi, rect)
                self.update()
                time.sleep(0.01)
            pygame.mixer.Sound("assets/sounds/effect/piano-low.mp3").play()
            if self.image_id == 2 and self.next_level is not None:
                time.sleep(2)
                self.next_level()

        threading.Thread(target=bloom_, args=()).start()

    def update(self):
        self.rect.centerx = self.player.x + self.pos[0]
        self.rect.centery = self.player.y + self.pos[1]
        if self.check:
            if pygame.sprite.collide_mask(self, self.player) is not None and not self.is_bloomed:
                self.check = False
                self.is_bloomed = True
                self.bloom()


class player(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(".\\assets\\images\\player\\player-1.png").convert_alpha(), (50, 50))
        # self.image = pygame.surface.Surface((50, 50))
        # pygame.draw.rect(self.image, (255, 255, 255), (0, 0, 50, 50))
        self.rect = self.image.get_rect()
        self.rect.centerx = pos[0]
        self.rect.centery = pos[1]
        self.mask = pygame.mask.from_surface(self.image)
        self.jumping = False
        self.moving = False
        self.x = 0
        self.y = 0

    def skin(self, id_):
        self.image = pygame.transform.scale(pygame.image.load(f".\\assets\\images\\player\\player-{id_}.png").convert_alpha(), (50, 50))

    def move(self, x, g: pygame.sprite.Group):
        def move_(x, g):
            self.moving = True
            self.x -= x
            clock = pygame.time.Clock()
            self.moving = False
            if not self.jumping:
                self.jumping = True
                lock = True
                o = 0
                while lock:
                    for i in g:
                        for j in i.sprites():
                            if pygame.sprite.collide_mask(self, j) is not None:
                                if j.image_id == 3:
                                    self.x = 0
                                    self.y = 200
                                    self.down(g)
                                if j.rect.centery >= self.rect.centery:
                                    lock = False
                                    break
                    self.y -= min(o, 10)
                    o += 0.3
                    clock.tick(60)
                self.jumping = False

        if not self.moving:
            threading.Thread(target=move_, args=(x, g)).start()

    def jump(self, l, g: pygame.sprite.Group):
        def jump_(l, g):
            self.jumping = True
            clock = pygame.time.Clock()
            for i in range(-l * 2, 0 + 1):
                self.y -= i / 5
                clock.tick(60)
            lock = True
            o = 1
            while lock:
                for i in g:
                    for j in i.sprites():
                        if pygame.sprite.collide_mask(self, j) is not None:
                            if j.image_id == 3:
                                self.x = 0
                                self.y = 200
                                self.down(g)
                            if j.rect.centery >= self.rect.centery:
                                lock = False
                                break
                self.y -= min(o, 10)
                o += 0.3
                clock.tick(60)
            self.jumping = False

        if not self.jumping:
            threading.Thread(target=jump_, args=(l, g)).start()

    def down(self, g: pygame.sprite.Group):
        def down_(g: pygame.sprite.Group):
            clock = pygame.time.Clock()
            lock = True
            o = 1
            while lock:
                for i in g:
                    for j in i.sprites():
                        if pygame.sprite.collide_mask(self, j) is not None:
                            if j.image_id == 3:
                                self.x = 0
                                self.y = 200
                                lock = False
                                self.down(g)
                                break
                            if j.rect.centery >= self.rect.centery:
                                lock = False
                                break
                self.y -= min(o, 10)
                o += 0.3
                clock.tick(60)

        threading.Thread(target=down_, args=(g,)).start()


class whiteBoom(pygame.sprite.Sprite):
    def __init__(self, center, size):
        super().__init__()
        self.size = size
        self.center = center
        self.image = pygame.surface.Surface(self.size).convert_alpha()
        self.image.fill((0, 0, 0, 0), (0, 0, self.size[0], self.size[1]))
        self.rect = self.image.get_rect()
        self.rect.center = center

    def boom(self, b):
        def boom_(b):
            clock = pygame.time.Clock()
            for i in range(0, max(self.image.width, self.image.height) + 1, 40):
                self.image = pygame.surface.Surface(self.size).convert_alpha()
                self.image.fill((0, 0, 0, 0), (0, 0, self.size[0], self.size[1]))
                self.rect = self.image.get_rect()
                self.rect.center = self.center
                pygame.draw.circle(self.image, (255, 255, 255, 100), self.rect.center, i)
                clock.tick(60)
            time.sleep(2)
            b.show()
            for i in range(max(self.image.width, self.image.height), 0 - 1, -40):
                self.image = pygame.surface.Surface(self.size).convert_alpha()
                self.image.fill((0, 0, 0, 0), (0, 0, self.size[0], self.size[1]))
                self.rect = self.image.get_rect()
                self.rect.center = self.center
                pygame.draw.circle(self.image, (255, 255, 255, 100), self.rect.center, i)
                clock.tick(60)

        threading.Thread(target=boom_, args=(b,)).start()


class background(pygame.sprite.Sprite):
    def __init__(self, size):
        super().__init__()
        self.size = size
        self.image = pygame.surface.Surface(self.size).convert_alpha()
        # self.image = pygame.transform.scale(pygame.image.load("assets/images/backgrounds/day-mountain.png").convert_alpha(), self.size)
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0
        self.showing = False
        self.alpha = 0
        self.o = pygame.transform.scale(pygame.image.load("assets/images/backgrounds/space-moon.png").convert_alpha(), self.size)

    def update(self) -> None:
        if self.showing:
            if self.alpha < 255:
                self.image = pygame.surface.Surface(self.size).convert_alpha()
                self.o.set_alpha(self.alpha)
                self.image.blit(self.o, (0, 0))
                self.alpha += 5

    def show(self):
        self.showing = True

    def setBackground(self, name):
        self.image = pygame.surface.Surface(self.size).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0
        self.showing = False
        self.alpha = 0
        self.image = pygame.transform.scale(pygame.image.load(f"assets/images/backgrounds/{name}.png").convert_alpha(), self.size)
