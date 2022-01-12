import pygame
import os
import sys
import random


class Meteors(pygame.sprite.Sprite):
    def __init__(self, app):
        pygame.sprite.Sprite.__init__(self)
        self.image = app.load_image("meteorite.png")
        self.rect = self.image.get_rect()
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
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Boundless Space')
        self.fps = 60
        self.all_sprites = pygame.sprite.Group()
        self.meteors_group = pygame.sprite.Group()
        self.player_group = pygame.sprite.Group()
        self.MYEVENTTYPE = 30

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

    def main(self):
        pygame.time.set_timer(self.MYEVENTTYPE, 1000)

        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.terminate()
                if event.type == self.MYEVENTTYPE:
                    self.meteors_group.add(Meteors(self))

            self.screen.fill(pygame.Color('black'))
            self.all_sprites.draw(self.screen)
            self.meteors_group.draw(self.screen)
            self.meteors_group.update(self)
            pygame.display.flip()
            self.clock.tick(self.fps)


if __name__ == '__main__':
    app = App()
    app.main()