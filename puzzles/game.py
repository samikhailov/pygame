import pygame
import random
import cv2


class Tile(pygame.sprite.Sprite):
    def __init__(self, surface, x, y) -> None:
        super().__init__()
        self.image = surface
        self.rect = pygame.Surface.get_rect(self.image)
        self.rect.x, self.rect.y = x, y

    def update(self):
        pass

    def copy(self) -> pygame.sprite.Sprite:
        return Tile(self.image, self.rect.x, self.rect.y)


class Game:
    IMAGE_PATH_1 = "image_1.jpg"
    IMAGE_PATH_2 = "image_2.jpg"

    def __init__(self, state) -> None:
        self._tile_column_size = state.WIDTH // state.tile_columns
        self._tile_row_size = state.WIDTH // state.tile_rows
        self.surf = pygame.Surface((state.WIDTH, state.WIDTH))
        self.rect = pygame.Rect(0, 0, state.WIDTH, state.WIDTH)
        self.tiles_reference: pygame.sprite.Group() = self.get_tiles(state)
        self.tiles_shuffled: pygame.sprite.Group() = self.shuffle()
        self.active_tile: Tile() = None
        self.last_active_tile: Tile() = None
        self.is_won = False

    def get_tiles(self, state) -> pygame.sprite.Group():
        original_img = cv2.imread(state.image_path)
        if original_img.shape[1] < original_img.shape[0]:
            scale = state.WIDTH / original_img.shape[1]
        else:
            scale = state.WIDTH / original_img.shape[0]
        img_width = int(original_img.shape[1] * scale)
        img_height = int(original_img.shape[0] * scale)
        resized_image = cv2.resize(original_img, (img_width, img_height), interpolation=cv2.INTER_AREA)

        tile_sprites = pygame.sprite.Group()

        for x in range(state.tile_columns):
            for y in range(state.tile_rows):
                x1 = x * self._tile_column_size
                x2 = (x + 1) * self._tile_column_size
                y1 = y * self._tile_row_size
                y2 = (y + 1) * self._tile_row_size
                tmp_image = resized_image[y1:y2, x1:x2]
                tmp_pygame_image = pygame.image.frombuffer(tmp_image.tostring(), tmp_image.shape[1::-1], "BGR")
                tile_sprites.add(
                    Tile(
                        tmp_pygame_image,
                        self._tile_column_size * x,
                        self._tile_row_size * y,
                    )
                )
        return tile_sprites

    def shuffle(self) -> pygame.sprite.Group():
        coords = list()
        for i in self.tiles_reference:
            coords.append((i.rect.x, i.rect.y))
        random.shuffle(coords)
        tiles_shuffled = pygame.sprite.Group()
        for index, tile in enumerate(self.tiles_reference):
            tiles_shuffled.add(Tile(tile.image, coords[index][0], coords[index][1]))
        return tiles_shuffled
