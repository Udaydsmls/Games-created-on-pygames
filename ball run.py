import pygame
import random

pygame.init()

WIN_WIDTH = 700
WIN_HEIGHT = 600
STAT_FONT = pygame.font.SysFont("comicsans", 20)


class Ball:
    X_move = 10
    X_VEL = 0

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.xm = self.X_move
        self.xvel = self.X_VEL
        self.tick_count = 0
        self.hitbox = (self.x - 20, self.y - 20, 40, 40)

    def move(self):
        self.tick_count += 1
        if self.tick_count > 5:
            self.x = self.x
        else:
            self.x = self.x + self.xvel

    def left(self):
        self.tick_count = 0
        if self.x > 120:
            self.xvel = (-self.xm)
        else:
            self.xvel = 0

    def right(self):
        self.tick_count = 0
        if self.x < 480:
            self.xvel = self.xm
        else:
            self.xvel = 0

    def draw(self, win):
        pygame.draw.circle(win, (0, 255, 249), (self.x, self.y), 20)
        self.hitbox = (self.x - 20, self.y - 20, 40, 40)
        pygame.draw.rect(win, (255, 255, 255), self.hitbox, 2)


class Block:
    VEL = 5

    def __init__(self):
        self.x = random.choice((145, 250, 355, 460))
        self.y = -200
        self.z = random.randrange(50, 200)
        self.vel = self.VEL
        self.hitbox = (self.x, self.y, 100, self.z)

    def draw(self, win):
        self.hitbox = (self.x, self.y, 100, self.z)
        pygame.draw.rect(win, (255, 69, 0), (self.x, self.y, 100, self.z))
        pygame.draw.rect(win, (255, 255, 255), self.hitbox, 2)

        '''
        pygame.draw.polygon(win, (255, 0, 255),
                            (((self.y - 31800 / 33) * (-11 / 40) + 5, self.y),
                             (((self.y + self.z) - 31800 / 33) * (-11 / 40) + 5, (self.y + self.z)),
                             (((self.y + self.z) - 31800 / 33) * (-11 / 40) + 80, (self.y + self.z)),
                             ((self.y - 31800 / 33) * (-11 / 40) + 80, self.y)))
        '''

    def move(self):
        self.y += self.vel


def draw_window(ball, blocks, score, sharingan):
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))

    win.fill((0, 189, 255))

    # pygame.draw.polygon(win, (0, 0, 0), ((100, 600), (275, 0), (325, 0), (500, 600)))
    text = STAT_FONT.render("Score: " + str(score), 1, (0, 0, 0))
    t = STAT_FONT.render("Slow_mo: " + str(sharingan), 1, (0, 0, 0))
    win.blit(text, (WIN_WIDTH - 10 - text.get_width(), 10))
    win.blit(t, (WIN_WIDTH - 625 - text.get_width(), 10))

    pygame.draw.rect(win, (255, 255, 255), (130, 0, 440, 600))
    for block in blocks:
        block.draw(win)

    ball.draw(win)
    pygame.display.update()


def main():
    ball = Ball(300, 500)
    blocks = [Block()]
    score = 0
    SLOW_MO = 5
    x = 30
    y = 1
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(x)
        events = pygame.event.poll()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        block_passed = False
        for block in blocks:
            block.move()
            if ball.y < block.hitbox[1] + block.hitbox[3]:
                if block.hitbox[0] < ball.x - 20 < block.hitbox[0] + block.hitbox[2] or\
                        block.hitbox[0] + block.hitbox[2] > ball.x + 20 > block.hitbox[0]:
                    run = False
            if block.y == 250:
                blocks.append(Block())
            if block.y > ball.y + 30:
                blocks.remove(block)
                block_passed = True

        if block_passed:
            score += 1
            SLOW_MO += 0.1
            x += y

        if x >= 60:
            y = 1

        ball.move()

        if events.type == pygame.KEYDOWN:
            if events.key == pygame.K_d:
                ball.right()
            if events.key == pygame.K_a:
                ball.left()
            if events.key == pygame.K_s:
                if SLOW_MO >= 1:
                    SLOW_MO -= 1
                    x = 10
                    y += 5

        draw_window(ball, blocks, score, SLOW_MO)


main()

