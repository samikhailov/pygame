import pygame
import sys
from random import choice


class Tile(pygame.sprite.Sprite):
    SIZE = 120

    def __init__(self, text, x, y) -> None:
        super().__init__()
        self.image = pygame.Surface((self.SIZE, self.SIZE))
        self.rect = pygame.Rect(x, y, self.SIZE, self.SIZE)

        self.image.fill(pygame.Color("LightPink"))
        pygame.draw.rect(self.image, pygame.Color("blue"), (0, 0, self.rect.width, self.rect.height), 3)
        pygame.font.init()
        font = pygame.font.Font("resourses/fonts/NotoSansJP-Regular.otf", 24)
        text_surf = font.render(text, True, pygame.Color("blue"))
        self.image.blit(text_surf, (10, 10))

    def move_left(self):
        self.rect.x -= self.SIZE

    def move_up(self):
        self.rect.y -= self.SIZE

    def move_right(self):
        self.rect.x += self.SIZE

    def move_down(self):
        self.rect.y += self.SIZE


class Game:
    WIDTH = 600
    HEIGHT = 600
    ROWS = 5
    COLUMNS = 5

    def __init__(self) -> None:
        self.field = dict()
        for i in range(0, self.ROWS * self.COLUMNS):
            row = i // self.ROWS
            column = i % self.COLUMNS
            self.field[i] = Tile(str(i + 1), column * Tile.SIZE, row * Tile.SIZE)
        self.field[self.ROWS * self.COLUMNS - 1] = None
        self.empty = self.ROWS * self.COLUMNS - 1
        for i in range(10000):
            result = choice([self.move_left, self.move_up, self.move_right, self.move_down])
            result()


    def move_left(self):
        try:
            if self.empty % self.COLUMNS != self.COLUMNS - 1:
                self.field[self.empty + 1].move_left()
                self.field[self.empty + 1], self.field[self.empty] = (
                    self.field[self.empty],
                    self.field[self.empty + 1],
                )
                self.empty += 1
        except KeyError:
            pass

    def move_up(self):
        try:
            self.field[self.empty + self.COLUMNS].move_up()
            self.field[self.empty + self.COLUMNS], self.field[self.empty] = (
                self.field[self.empty],
                self.field[self.empty + self.COLUMNS],
            )
            self.empty += self.COLUMNS
        except KeyError:
            pass

    def move_right(self):
        try:
            if self.empty % self.COLUMNS != 0:
                self.field[self.empty - 1].move_right()
                self.field[self.empty - 1], self.field[self.empty] = (
                    self.field[self.empty],
                    self.field[self.empty - 1],
                )
                self.empty -= 1
        except KeyError:
            pass

    def move_down(self):
        try:
            self.field[self.empty - self.COLUMNS].move_down()
            self.field[self.empty - self.COLUMNS], self.field[self.empty] = (
                self.field[self.empty],
                self.field[self.empty - self.COLUMNS],
            )
            self.empty -= self.COLUMNS
        except KeyError:
            pass

if __name__ == "__main__":
    FPS = 60


    pygame.init()
    game = Game()
    screen = pygame.display.set_mode((game.WIDTH, game.HEIGHT))
    clock = pygame.time.Clock()
    

    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                sys.exit()
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_LEFT:
                    game.move_left()
                elif e.key == pygame.K_UP:
                    game.move_up()
                elif e.key == pygame.K_RIGHT:
                    game.move_right()
                elif e.key == pygame.K_DOWN:
                    game.move_down()


        screen.fill(pygame.Color("black"))
        for tile in game.field.values():
            if tile:
                screen.blit(tile.image, tile.rect)
        clock.tick(FPS)
        pygame.display.update()