import pygame
import os
import random
pygame.font.init()


WIN_HEIGHT = 400
WIN_WIDTH = 600

DINOIMGS = pygame.transform.scale(pygame.image.load
                                  (os.path.join("Dino", "D:/Uday/python game/Dino/Pikachu.png")), (62, 70))
CACTUSIMG = pygame.transform.scale(pygame.image.load
                                   (os.path.join("Dino", "D:/Uday/python game/Dino/CACTUS.png")), (65, 75))
BASEIMG = pygame.transform.scale(pygame.image.load
                                 (os.path.join("Dino", "D:/Uday/python game/Dino/BASE.jpg")), (600, 100))
BGIMG = pygame.image.load(os.path.join("Dino", "D:/Uday/python game/Dino/BGround.png"))
STAT_FONT = pygame.font.SysFont("comicsans", 50)


class Dino:
    IMGS = DINOIMGS

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vel = 0
        self.tick_count = 0
        self.img = self.IMGS
        self.height = self.y

    def jump(self):
        self.height = self.y
        self.tick_count = 0
        self.vel = -10.5

    def move(self):
        self.tick_count += 1

        d = self.vel * self.tick_count + 1.2 * self.tick_count ** 2

        if d > 10:
            d = 10

        if self.y + d > 304:
            self.y = 304
        else:
            self.y = self.y + d

    def draw(self, win):
        win.blit(self.img, (self.x, self.y))

    def get_mask(self):
        return pygame.mask.from_surface(self.img)


class Base:
    VEL = 10
    WIDTH = BASEIMG.get_width()
    IMG = BASEIMG

    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = self.WIDTH

    def move(self):
        self.x1 -= self.VEL
        self.x2 -= self.VEL

        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH

        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH

    def draw(self, win):
        win.blit(self.IMG, (self.x1, self.y))
        win.blit(self.IMG, (self.x2, self.y))


class Cactus:
    VEL = 10

    def __init__(self, x):
        self.x = x
        self.height = 0
        self.bottom = 301
        self.CacTus = CACTUSIMG

        self.passed = False

    def move(self):
        self.x -= self.VEL

    def draw(self, win):
        win.blit(self.CacTus, (self.x, self.bottom))

    def collide(self, dino):
        dino_mask = dino.get_mask()
        bottom_mask = pygame.mask.from_surface(self.CacTus)

        bottom_offset = (self.x - dino.x, self.bottom - round(dino.y))

        b_point = dino_mask.overlap(bottom_mask, bottom_offset)

        if b_point:
            return True

        return False


def draw_window(win, dino, base, cactuss, score):
    win.blit(BGIMG, (0, 0))

    for cactus in cactuss:
        cactus.draw(win)

    text = STAT_FONT.render("Score: " + str(score), 1, (0, 0, 0))
    win.blit(text, (WIN_WIDTH - 10 - text.get_width(), 10))

    base.draw(win)
    dino.draw(win)
    pygame.display.update()


def main():
    dino = Dino(100, 304)
    base = Base(370)
    cactuss = [Cactus(900)]
    score = 0

    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    clock = pygame.time.Clock()

    run = True
    while run:
        events = pygame.event.poll()
        clock.tick(60)
        base.move()
        dino.move()
        if events.type == pygame.KEYDOWN and dino.y >= 304:
            if events.key == pygame.K_UP or events.key == pygame.K_SPACE:
                dino.jump()

        add_cactus = False
        rem = []
        for cactus in cactuss:
            if cactus.collide(dino):
                print(score)
                pygame.quit()

            if not cactus.passed and cactus.x < dino.x:
                cactus.passed = True
                add_cactus = True

            cactus.move()

        if add_cactus:
            score += 1
            x = random.randrange(500, 900)
            cactuss.append(Cactus(x))

        for r in rem:
            cactuss.remove(r)

        draw_window(win, dino, base, cactuss, score)

main()