import pygame
import sys


class Disc(pygame.sprite.Sprite):
    HEIGHT = 20

    def __init__(self, centerx, bottom, width, height=HEIGHT) -> None:
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.rect = pygame.Rect(0, 0, width, height)
        self.rect.bottom = bottom
        self.rect.centerx = centerx
        self.color_primary = pygame.Color("Orchid")
        self.color_secondary = pygame.Color("DarkViolet")

    def update(self):
        radius = self.HEIGHT // 2
        border = 2
        # Обводка
        pygame.draw.rect(
            self.image,
            self.color_secondary,
            (radius, 0, self.rect.width - 2 * radius, self.HEIGHT),
        )
        pygame.draw.circle(self.image, self.color_secondary, (radius, radius), radius)
        pygame.draw.circle(self.image, self.color_secondary, (self.rect.width - radius, radius), radius)

        # Заполнение
        pygame.draw.rect(
            self.image,
            self.color_primary,
            (radius, border, self.rect.width - 2 * radius, self.HEIGHT - 2 * border),
        )
        pygame.draw.circle(self.image, self.color_primary, (radius, radius), radius - border)
        pygame.draw.circle(self.image, self.color_primary, (self.rect.width - radius, radius), radius - border)


class Tower(pygame.sprite.Sprite):
    WIDTH = 200
    HEIGHT = 200

    def __init__(self, x, discs_num, is_first=False) -> None:
        super().__init__()
        self.image = pygame.Surface((self.WIDTH, self.HEIGHT))
        self.rect = pygame.Rect(x, 0, self.WIDTH, self.HEIGHT)
        self.rect.bottom = Game.HEIGHT
        self.discs = pygame.sprite.Group()
        self.discs_num = discs_num
        if is_first:
            bottom = self.HEIGHT
            for i in range(self.discs_num):
                self.discs.add(Disc(self.WIDTH // 2, bottom, self.WIDTH - i * Disc.HEIGHT, Disc.HEIGHT))
                bottom -= Disc.HEIGHT
        self.discs.update()

    def update(self):
        rod_width = 10
        self.image.fill(pygame.Color("black"))
        pygame.draw.rect(
            self.image, pygame.Color("darkred"), ((self.rect.width - rod_width) // 2, 0, rod_width, self.rect.height)
        )
        pygame.sprite.Group.draw(self.discs, self.image)


class Game:
    WIDTH, HEIGHT = 600, 400
    def __init__(self) -> None:
        self.discs_num = 8
        self.towers = [Tower(0, self.discs_num, is_first=True), Tower(200, self.discs_num), Tower(400, self.discs_num)]
        self.active_disc = None


if __name__ == "__main__":
    FPS = 30
    game = Game()
    pygame.init()
    screen = pygame.display.set_mode((Game.WIDTH, Game.HEIGHT))
    clock = pygame.time.Clock()

    while True:
        clock.tick(FPS)
        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                sys.exit()
            elif i.type == pygame.MOUSEBUTTONDOWN and i.button == 1:
                mouse_pos_x, mouse_pos_y = pygame.mouse.get_pos()

                for tower in game.towers:
                    if (
                        tower.rect.left < mouse_pos_x < tower.rect.right
                        and tower.rect.top < mouse_pos_y < tower.rect.bottom
                    ):
                        if game.active_disc is None:
                            if len(tower.discs.sprites()) > 0:
                                game.active_disc = tower.discs.sprites()[-1]
                                game.active_disc.color_primary = pygame.Color("MediumSeaGreen")
                                game.active_disc.color_secondary = pygame.Color("SeaGreen")
                                game.active_disc.update()
                        elif (
                            len(tower.discs.sprites()) == 0
                            or len(tower.discs.sprites()) > 0
                            and tower.discs.sprites()[-1].rect.width >= game.active_disc.rect.width
                        ):
                            game.active_disc.kill()
                            game.active_disc.rect.centerx = tower.WIDTH // 2
                            game.active_disc.rect.top = (
                                tower.HEIGHT - game.active_disc.rect.height - Disc.HEIGHT * len(tower.discs.sprites())
                            )
                            tower.discs.add(game.active_disc)
                            game.active_disc.color_primary = pygame.Color("Orchid")
                            game.active_disc.color_secondary = pygame.Color("DarkViolet")
                            game.active_disc.update()
                            game.active_disc = None

        screen.fill(pygame.Color("black"))
        for tower in game.towers:
            tower.update()
            screen.blit(tower.image, tower.rect)

        pygame.display.update()