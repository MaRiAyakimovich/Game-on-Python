import pygame
import os
import sys
import random


class Meteors(pygame.sprite.Sprite):
    def __init__(self, app):
        pygame.sprite.Sprite.__init__(self)
        meteor = Meteors
        self.image = app.load_image("meteorite.png")
        self.rect = self.image.get_rect()
        app.all_sprites.add(meteor)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = random.randrange(app.width - self.rect.width)
        self.rect.y = 50
        self.speedy = 5

    def update(self, app):
        self.rect.y += self.speedy
        self.rect.x = random.randrange(app.width - self.rect.width)
        self.rect.y = 50
        self.speedy = 5


class App:
    def __init__(self):
        #self.player = None
        pygame.init()
        pygame.key.set_repeat(200, 70)  # удерживание кнопок влево и вправо
        self.size = self.width, self.height = 500, 780
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Boundless Space')
        self.fps = 60
        self.all_sprites = pygame.sprite.Group()


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
        pygame.init()
        screen = pygame.display.set_mode(self.size)
        clock = pygame.time.Clock()
        FPS = 60
        meteor = pygame.sprite.Group()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            screen.fill((0, 0, 0))
            meteor.draw(screen)
            meteor.update()
            pygame.display.flip()
            clock.tick(FPS)
        pygame.quit()



if __name__ == '__main__':
    app = App()
    app.main()
