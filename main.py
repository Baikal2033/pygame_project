import pygame as pg
import random

from pygame.examples.cursors import image_name
from pygame.examples.moveit import WIDTH, HEIGHT

FPS = 60
WIN_WIDTH, WIN_HEIGHT = 1000, 600
WHITE, BLACK, RED, AQUA, GREY = (255, 255, 255), (0, 0, 0), (255, 0, 0), (39, 245, 183), (110, 100, 99)

class Text:
    def __init__(self, text, text_size, text_color, text_pos):
        self.font = pg.font.SysFont(None, text_size)
        self.suft = self.font.render(text, True, text_color)
        self.rect = self.suft.get_rect(center=text_pos)

    def draw(self, screen):
        screen.blit(self.suft, self.rect)


class Basket(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.original_image = pg.image.load(r'images/basket.png').convert_alpha()
        self.image = pg.transform.scale(self.original_image, (self.original_image.get_width() * 1/2, self.original_image.get_height() * 1/2))
        self.rect = self.image.get_rect(center=(500, 400))
        self.speed = 5

    def update(self, dx=0):
        if (self.rect.left + dx * self.speed) > 0 and (self.rect.right + dx * self.speed) < WIN_WIDTH:
            self.rect.x += dx * self.speed

    def draw(self, screen):
        screen.blit(self.image, self.rect)

class Fruit(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        image_path, k = random.choice([('images/fruit/apricot.png', 0.7), ('images/fruit/banana.png', 0.8), ('images/fruit/cherry.png', 0.6),
                                    ('images/fruit/gooseberry.png', 0.8), ('images/fruit/grape.png', 0.7), ('images/fruit/pineapple.png', 0.6),
                                    ('images/fruit/strawberry.png', 0.8)])
        self.image = pg.image.load(image_path).convert_alpha()
        self.image = pg.transform.scale(self.image, (self.image.get_width() * k, self.image.get_height() * k))
        self.rect = self.image.get_rect(center=(random.randint(100, 900), 0))
        self.speed = random.randint(5, 9)

    def update(self):
        if self.rect.top < 1000:
            self.rect.y += self.speed
        else:
            self.kill()

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class Garbage(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        image_path, k = random.choice([('images/garbage/gel.png', 0.3), ('images/garbage/hanger.png', 0.3), ('images/garbage/packet.png', 0.2),
                                    ('images/garbage/paper.png', 0.3), ('images/garbage/peel.png', 0.3), ('images/garbage/pot.png', 0.2),
                                    ('images/garbage/shell.png', 0.3)])
        self.image = pg.image.load(image_path).convert_alpha()
        self.image = pg.transform.scale(self.image, (self.image.get_width() * k, self.image.get_height() * k))
        self.rect = self.image.get_rect(center=(random.randint(100, 900), 0))
        self.speed = random.randint(5, 9)

    def update(self):
        if self.rect.top < 1000:
            self.rect.y += self.speed
        else:
            self.kill()

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class Hearts(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        original_image = pg.image.load(r'images/heart.png').convert_alpha()
        





pg.mixer.pre_init(44100, -16, 1, 512)
pg.init()
screen = pg.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pg.display.set_caption("Игра 'Корзина'")
pg.display.set_icon(pg.image.load(r"images\icon.ico"))
clock = pg.time.Clock()
pg.mixer.music.load("sounds/fon_on_game.mp3")
pg.mixer.music.play()
background = pg.Surface((WIN_WIDTH, WIN_HEIGHT))
background.fill(AQUA)

score = 0
my_text = Text(f"Счёт: {score}", 40, WHITE, (WIN_WIDTH / 2 + 400, WIN_HEIGHT * 1 / 3 - 150))

my_basket = Basket()
cnt = 0
lives = 5
fruit = pg.sprite.Group()
garbage = pg.sprite.Group()

screen.blit(background, (0, 0))
my_basket.draw(screen)
my_text.draw(screen)
pg.display.update()

flag_play = True
while flag_play:
    clock.tick(FPS)

    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            flag_play = False
            break
    if not flag_play:
        break

    cnt += 1
    if cnt == 100:
        rd = random.randint(1, 2)
        if rd == 1:
            fruit.add(Fruit())
        if rd == 2:
            garbage.add(Garbage())
        cnt = 0

    if lives == 0:
        flag_play = False

    if pg.sprite.spritecollideany(my_basket, fruit, collided=pg.sprite.collide_mask):
        fruit.empty()
        score += 1
        my_text = Text(f"Счёт: {score}", 40, WHITE, (WIN_WIDTH / 2 + 400, WIN_HEIGHT * 1 / 3 - 150))

    if pg.sprite.spritecollideany(my_basket, garbage, collided=pg.sprite.collide_mask):
        garbage.empty()
        score += -1
        lives += -1
        my_text = Text(f"Счёт: {score}", 40, WHITE, (WIN_WIDTH / 2 + 400, WIN_HEIGHT * 1 / 3 - 150))

    keys = pg.key.get_pressed()
    if keys[pg.K_LEFT]:
        my_basket.update(dx=-1)
    if keys[pg.K_RIGHT]:
        my_basket.update(dx=1)

    fruit.update()
    garbage.update()

    screen.blit(background, (0, 0))
    fruit.draw(screen)
    garbage.draw(screen)
    my_basket.draw(screen)
    my_text.draw(screen)
    pg.display.update()
