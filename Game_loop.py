import pygame
import random
from fighters import Fighter1, Fighter2


class S3Gamers:
    def __init__(self):
        pygame.init()
        self.stage = random.randint(0, 2)
        print(self.stage)
        # Game Window Creation
        self.SCREEN_WIDTH = 1000
        self.SCREEN_HEIGHT = 600
        self.clock = pygame.time.Clock()
        self.FPS = 60
        self.GREEN = (0, 255, 0)
        self.RED = (255, 0, 0)
        self.GOLD = (255, 215, 0)

        self.CHARACTER_SIZEx = 300
        self.CHARACTER_SIZEy = 317
        self.CHARACTER_SCALE = 1.2
        self.CHARACTER_OFFSET = [110, 50]
        self.WARRIOR_DATA = [self.CHARACTER_SIZEx, self.CHARACTER_SIZEy, self.CHARACTER_SCALE, self.CHARACTER_OFFSET]

        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption('S3 FIGHTERS')

        # Background
        if self.stage == 0:
            self.bg = pygame.image.load('assets/graphics/backgrounds/background.jpg').convert_alpha()
        elif self.stage == 1:
            self.bg = pygame.image.load('assets/graphics/backgrounds/background2.jpg').convert_alpha()
        elif self.stage == 2:
            self.bg = pygame.image.load('assets/graphics/backgrounds/background3.jpg').convert_alpha()

        # Load Sprites
        self.kurt = pygame.image.load("assets/graphics/characters/Kurt/sprites/whole_sheet.png").convert_alpha()
        # Steps in animations
        self.CHARACTER_FRAMES = [4, 6, 4, 4, 4, 4, 4, 4, 1]

        # Character Hit Box
        self.player1 = Fighter1(100, 290, self.WARRIOR_DATA, self.kurt, self.CHARACTER_FRAMES)
        self.player2 = Fighter2(750, 290, self.WARRIOR_DATA, self.kurt, self.CHARACTER_FRAMES)

        # Looping The Window
        run = True
        while run:
            self.clock.tick(self.FPS)

            # draw the Bg
            self.draw_bg()

            # draw health
            self.draw_hp_bar(self.player1.hp, 20, 20)
            self.draw_hp_bar(self.player2.hp, 580, 20)

            # Movements
            self.player1.move_character(self.SCREEN_WIDTH, self.SCREEN_HEIGHT, self.screen, self.player2)
            self.player2.move_character(self.SCREEN_WIDTH, self.SCREEN_HEIGHT, self.screen, self.player1)

            # animations
            self.player1.update_animate()
            self.player2.update_animate()

            # Draw Character
            self.player1.draw_character(self.screen)
            self.player2.draw_character(self.screen)

            # Exit Code
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

            # Update
            pygame.display.update()

        # Exit
        pygame.quit()

    # Putting the bg
    def draw_bg(self):
        self.bg2 = pygame.transform.scale(self.bg, (self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.screen.blit(self.bg2, (0, 0))

    def draw_hp_bar(self, health, x, y):
        self.hp_ratio = health/100
        pygame.draw.rect(self.screen, self.GOLD, (x - 5, y - 5, 410, 40))
        pygame.draw.rect(self.screen, self.RED, (x, y, 400, 30))
        pygame.draw.rect(self.screen, self.GREEN, (x, y, 400*self.hp_ratio, 30))




test_run = S3Gamers()