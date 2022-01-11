import pygame
import os
import sys
import random


class Hero(pygame.sprite.Sprite):
    def __init__(self, app, pos):
        super().__init__(app.all_sprites)
        self.image = app.load_image("spaceship.png")
        self.rect = self.image.get_rect()
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
        self.player_group = pygame.sprite.Group()
        self.hero = Hero(self, (180, 670))
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

            self.screen.fill(pygame.Color('black'))
            self.all_sprites.draw(self.screen)
            pygame.display.flip()
            self.clock.tick(self.fps)

    def start_screen(self):
        intro_text = "               Boundless Space"
        intro_txt = "           Press any button or click the mouse"
        intro_t = "                          to start the game"

        fon = pygame.transform.scale(self.load_image('fon.jpg'), (self.width, self.height))
        self.screen.blit(fon, (0, 0))
        font = pygame.font.Font(None, 45)

        string_rendered = font.render(intro_text, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        intro_rect.top = 250
        intro_rect.x = 10
        self.screen.blit(string_rendered, intro_rect)

        font = pygame.font.Font(None, 30)
        string_rendered = font.render(intro_txt, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        intro_rect.top = 400
        intro_rect.x = 10
        self.screen.blit(string_rendered, intro_rect)

        font = pygame.font.Font(None, 30)
        string_rendered = font.render(intro_t, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        intro_rect.top = 430
        intro_rect.x = 10
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
