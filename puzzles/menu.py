import pygame
import sys

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (142, 22, 0)
GRAY = (200, 200, 200)


class Button(pygame.sprite.Sprite):
    START = 1
    BACK = 2
    RESUME = 3
    NEW_GAME = 4
    EXIT = 5
    SIZE_3X3 = 10
    SIZE_4X4 = 11
    SIZE_5X5 = 12
    IMAGE_1 = 21
    IMAGE_2 = 22

    def __init__(self, button, width, height, x=0, y=0, text="", image_path="", is_selected=False) -> None:
        super().__init__()
        self.button = button
        self.is_selected = is_selected
        self.image = pygame.Surface((width, height))
        self.image.fill(WHITE)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        if image_path != "":
            image_surf = pygame.image.load(image_path).convert()
            self.image.blit(image_surf, (0, 0))

        if text != "":
            font = pygame.font.SysFont("arial", 36)
            text = font.render(text, True, RED)
            text_rect = text.get_rect(center=(self.rect.width // 2, self.rect.height // 2))
            self.image.blit(text, text_rect)

    def update(self):
        if self.is_selected == True:
            pygame.draw.rect(self.image, RED, (0, 0, self.rect.width, self.rect.height), 7)
        else:
            pygame.draw.rect(self.image, GRAY, (0, 0, self.rect.width, self.rect.height), 7)
