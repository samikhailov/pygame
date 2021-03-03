import sys
import pygame
from menu import Button
from game import Game


class State:

    SCREEN_GAME = 1
    SCREEN_MENU = 2
    SCREEN_PAUSE = 3

    WIDTH = 600
    HEIGHT = 700

    FPS = 60

    def __init__(self) -> None:
        pygame.init()
        self.screen_type = self.SCREEN_MENU
        self.tile_columns = 3
        self.tile_rows = 3
        self.image_path = Game.IMAGE_PATH_1

    def set_tile_colunms_rows(self, tile_columns, tile_rows) -> None:
        """Установка количества и размера пазлов по строкам и столбцам"""
        pass


def is_mouse_on_rect(rect) -> bool:
    mouse_pos = pygame.mouse.get_pos()
    if (rect.left < mouse_pos[0] < rect.right) and (rect.top < mouse_pos[1] < rect.bottom):
        return True


if __name__ == "__main__":
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (142, 22, 0)
    GRAY = (200, 200, 200)
    state = State()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((state.WIDTH, state.HEIGHT))

    # Экраны меню setup
    if state.screen_type == State.SCREEN_MENU or state.screen_type == State.SCREEN_PAUSE:
        # SCREEN_MENU
        button_size_1 = Button(Button.SIZE_3X3, 100, 80, x=25, y=25, text="3x3", is_selected=True)
        active_button_size = button_size_1
        button_size_2 = Button(Button.SIZE_4X4, 100, 80, x=150, y=25, text="4x4")
        button_size_3 = Button(Button.SIZE_5X5, 100, 80, x=275, y=25, text="5x5")
        size_sprites = pygame.sprite.Group()
        size_sprites.add(button_size_1, button_size_2, button_size_3)

        button_image_1 = Button(Button.IMAGE_1, 100, 100, x=25, y=200, image_path="image_1_thumb.jpg", is_selected=True)
        active_button_image = button_image_1
        button_image_2 = Button(Button.IMAGE_2, 100, 100, x=150, y=200, image_path="image_2_thumb.jpg")
        image_sprites = pygame.sprite.Group()
        image_sprites.add(button_image_1, button_image_2)

        button_start = Button(Button.START, 200, 80, x=275, y=375, text="Играть")

        # SCREEN_PAUSE
        button_resume = Button(Button.RESUME, 300, 80, x=25, y=25, text="Продолжить")
        button_new_game = Button(Button.NEW_GAME, 300, 80, x=25, y=225, text="Новая игра")
        button_exit = Button(Button.EXIT, 300, 80, x=25, y=425, text="Выход")

    # Начало цикла
    while 1:
        # Экран меню loop
        if state.screen_type == State.SCREEN_MENU:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    sys.exit()
                elif e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                    for button in size_sprites:
                        if is_mouse_on_rect(button.rect):
                            active_button_size.is_selected = False
                            button.is_selected = True
                            active_button_size = button

                            if active_button_size.button == Button.SIZE_3X3:
                                state.tile_columns = 3
                                state.tile_rows = 3
                            elif active_button_size.button == Button.SIZE_4X4:
                                state.tile_columns = 4
                                state.tile_rows = 4
                            elif active_button_size.button == Button.SIZE_5X5:
                                state.tile_columns = 5
                                state.tile_rows = 5

                    for button in image_sprites:
                        if is_mouse_on_rect(button.rect):
                            active_button_image.is_selected = False
                            button.is_selected = True
                            active_button_image = button

                            if active_button_image.button == Button.IMAGE_1:
                                state.image_path = Game.IMAGE_PATH_1
                            elif active_button_image.button == Button.IMAGE_2:
                                state.image_path = Game.IMAGE_PATH_2

                    if is_mouse_on_rect(button_start.rect):
                        state.screen_type = State.SCREEN_GAME
                        game = Game(state)
                        button_back = Button(Button.BACK, 200, 80, x=275, y=600, text="Назад")
                        continue

            screen.fill(BLACK)
            size_sprites.update()
            size_sprites.draw(screen)
            image_sprites.update()
            image_sprites.draw(screen)
            screen.blit(button_start.image, button_start.rect)

        # Экран паузы loop
        elif state.screen_type == State.SCREEN_PAUSE:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    sys.exit()
                elif e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                    if is_mouse_on_rect(button_resume.rect):
                        state.screen_type = State.SCREEN_GAME
                    elif is_mouse_on_rect(button_new_game.rect):
                        state.screen_type = State.SCREEN_MENU
                    elif is_mouse_on_rect(button_exit.rect):
                        sys.exit()
            screen.fill(BLACK)
            screen.blit(button_resume.image, button_resume.rect)
            screen.blit(button_new_game.image, button_new_game.rect)
            screen.blit(button_exit.image, button_exit.rect)

        # Экран игры loop
        elif state.screen_type == State.SCREEN_GAME:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    sys.exit()

                # Нажатие
                elif e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                    if not game.is_won:
                        for tile in game.tiles_shuffled:
                            if is_mouse_on_rect(tile.rect):
                                game.active_tile = tile
                                game.dump_active_tile = tile.copy()
                    if is_mouse_on_rect(button_back.rect):
                        state.screen_type = State.SCREEN_PAUSE
                        continue

                # Отжатие
                elif e.type == pygame.MOUSEBUTTONUP and game.active_tile and not game.is_won:
                    if is_mouse_on_rect(game.rect) and pygame.mouse.get_focused():
                        game.active_tile.rect.x = (
                            game.active_tile.rect.centerx // game._tile_column_size
                        ) * game._tile_column_size
                        game.active_tile.rect.y = (
                            game.active_tile.rect.centery // game._tile_row_size
                        ) * game._tile_row_size
                        for tile in game.tiles_shuffled:
                            if tile != game.active_tile and is_mouse_on_rect(tile.rect):
                                tile.rect.x, game.dump_active_tile.rect.x = game.dump_active_tile.rect.x, tile.rect.x
                                tile.rect.y, game.dump_active_tile.rect.y = game.dump_active_tile.rect.y, tile.rect.y

                        if set([(i.image, i.rect.x, i.rect.y) for i in game.tiles_shuffled]) == set(
                            [(i.image, i.rect.x, i.rect.y) for i in game.tiles_reference]
                        ):
                            game.is_won = True
                    else:
                        # game.active_tile = game.dump_active_tile
                        game.active_tile.rect = game.dump_active_tile.rect
                        game.active_tile = None

            # Перемещение
            if (
                pygame.mouse.get_pressed()[0]
                and game.active_tile
                and game.is_won is False
                and is_mouse_on_rect(game.rect)
                and pygame.mouse.get_focused()
            ):
                mouse_pos = pygame.mouse.get_pos()
                game.active_tile.rect.x = mouse_pos[0] - game.active_tile.rect.width // 2
                game.active_tile.rect.y = mouse_pos[1] - game.active_tile.rect.height // 2

            # Отрисовка
            screen.fill(BLACK)
            game.surf.fill(BLACK)
            game.tiles_shuffled.draw(game.surf)
            if game.active_tile:
                game.surf.blit(game.active_tile.image, game.active_tile.rect)
            screen.blit(game.surf, game.rect)
            screen.blit(button_back.image, button_back.rect)

            # Сообщение о победе
            if game.is_won is True:
                font = pygame.font.SysFont("arial", 36)
                text = font.render("Победа!", True, BLACK)
                screen.blit(text, (10, 50))

        pygame.display.update()
        clock.tick(state.FPS)
