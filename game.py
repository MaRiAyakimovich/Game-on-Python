import pygame
import os
import sys
import random


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = app.load_image("bullet.png ")
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10
        self.counting = 0

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()
            self.counting += 1


class Hero(pygame.sprite.Sprite):
    def __init__(self, app, pos):
        super().__init__(app.all_sprites)
        self.image = app.load_image("spaceship.png")
        self.rect = self.image.get_rect()
        self.radius = 55
        # вычисляем маску для эффективного сравнения
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = pos[0]
        self.rect.y = pos[1]

    def update(self, x, y):
        self.rect.x += x
        self.rect.y += y
        if self.rect.right > app.width:
            self.rect.right = app.width
        if self.rect.left < 0:
            self.rect.left = 0

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        app.all_sprites.add(bullet)
        app.bullets.add(bullet)


class Meteors(pygame.sprite.Sprite):
    def __init__(self, app):
        pygame.sprite.Sprite.__init__(self)
        self.image = app.load_image("meteorite.png")
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * .45 / 2)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = random.randrange(app.width - self.rect.width)
        self.speedy = 5

    def update(self, app):
        self.rect.y += self.speedy
        self.speedy = 5


class App:
    def __init__(self):
        pygame.init()
        pygame.key.set_repeat(10, 50)  # удерживание кнопок влево и вправо
        self.width, self.height = 500, 780
        self.life = 0
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Boundless Space')
        self.fps = 60
        self.all_sprites = pygame.sprite.Group()
        self.meteors_group = pygame.sprite.Group()
        self.player_group = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.hero = Hero(self, (180, 670))
        self.MYEVENTTYPE = 30
        self.counting = 0
        self.tile_width = self.tile_height = 50

    def terminate(self):
        pygame.quit()
        sys.exit()

    def load_image(self, name, colorkey=None):
        fullname = os.path.join('data', name)
        # если файл не существует, то выходим
        if not os.path.isfile(fullname):
            print(f"Файл с изображением '{fullname}' не найден")
            sys.exit()
        image = pygame.image.load(fullname)
        if colorkey is not None:
            image = image.convert()
            if colorkey == -1:
                colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey)
        else:
            image = image.convert_alpha()
        return image

    def count(self, screen, text, size, x, y):
        font_name = pygame.font.match_font('arial')
        font = pygame.font.Font(font_name, size)
        text_surface = font.render(text, True, (255, 255, 255))
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)

    def main(self):
        pygame.time.set_timer(self.MYEVENTTYPE, 1000)

        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.terminate()

                if event.type == pygame.KEYDOWN:
                    key = pygame.key.get_pressed()
                    if key[pygame.K_LEFT]:
                        self.hero.update(-10, 0)
                    if key[pygame.K_RIGHT]:
                        self.hero.update(10, 0)
                    if event.key == pygame.K_SPACE:
                        self.hero.shoot()

                if event.type == self.MYEVENTTYPE:
                    self.meteors_group.add(Meteors(self))

            strike = pygame.sprite.groupcollide(app.meteors_group, app.bullets, True, True)
            for blows in strike:
                m = Meteors(self)
                app.all_sprites.add(m)
                app.meteors_group.add(m)

            blows = pygame.sprite.spritecollide(self.hero, self.meteors_group, False, pygame.sprite.collide_circle)
            if blows:
                self.life += 1
                if self.life == 3:
                    self.terminate()

            self.screen.fill(pygame.Color('black'))
            self.all_sprites.draw(self.screen)
            self.meteors_group.draw(self.screen)
            self.bullets.update()
            self.meteors_group.update(self)
            pygame.display.flip()
            self.clock.tick(self.fps)

            self.screen.fill(pygame.Color('black'))
            self.all_sprites.draw(self.screen)
            self.count(self.screen, str(self.counting), 18, self.width / 2, 10)

    def start_screen(self):
        intro_text = ["", "", "", "", "", "", "", "", "                          Boundless Space", "", "",
                      "           Press any button or click the mouse", "                          to start the game"]

        fon = pygame.transform.scale(self.load_image('fon.jpg'), (self.width, self.height))
        self.screen.blit(fon, (0, 0))
        font = pygame.font.Font(None, 30)
        text_coord = 50
        for line in intro_text:
            string_rendered = font.render(line, 1, pygame.Color('white'))
            intro_rect = string_rendered.get_rect()
            text_coord += 10
            intro_rect.top = text_coord
            intro_rect.x = 10
            text_coord += intro_rect.height
            self.screen.blit(string_rendered, intro_rect)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.terminate()
                elif event.type == pygame.KEYDOWN or \
                        event.type == pygame.MOUSEBUTTONDOWN:
                    return  # начинаем игру

            pygame.display.flip()
            self.clock.tick(self.fps)


if __name__ == '__main__':
    app = App()
    app.start_screen()
    app.main()