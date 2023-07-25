import pygame
from player1_controls import P1Controls
from player2_controls import P2Controls
from character_kurt import KurtVillamor


class MainGame:
    def __init__(self):
        pygame.init()

        # Game Window Creation
        self.SCREEN_WIDTH = 1000
        self.SCREEN_HEIGHT = 600
        self.clock = pygame.time.Clock()
        self.FPS = 60
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption('S3-Clash!')

        # Background
        self.bg = pygame.image.load('assets/graphics/backgrounds/background5.jpg').convert_alpha()

        # Health Border
        self.hp_bar = pygame.image.load('assets/graphics/health_bar.png').convert_alpha()

        # Ground
        self.ground = pygame.image.load('assets/graphics/backgrounds/ground.jpg').convert_alpha()

        self.ch1 = KurtVillamor()  # Character Kurt

        self.control1 = P1Controls(self.ch1)
        self.control2 = P2Controls(self.ch1)



        run = True
        while run:
            self.clock.tick(self.FPS)


            self.draw_bg()
            self.draw_hp_bar()
            self.hp_indicator(self.control1.hp, 46, 30)  # Player 1 Health
            self.hp_indicator(100, 560, 30)  # Player 2 Health
            self.draw_ground()

            self.control1.draw_player1(self.screen)
            self.control1.movement_player1(self.SCREEN_WIDTH, self.SCREEN_HEIGHT)

            self.control2.draw_player1(self.screen)
            self.control2.movement_player1(self.SCREEN_WIDTH, self.SCREEN_HEIGHT)







            # Exit Code
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

            # Update
            pygame.display.update()

            # Exit
        pygame.quit()

    def draw_bg(self):
        self.bg2 = pygame.transform.scale(self.bg, (self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.screen.blit(self.bg2, (0, 0))

    def draw_hp_bar(self):
        self.hp_bar2 = pygame.transform.scale(self.hp_bar, (950, 150))
        self.screen.blit(self.hp_bar2, (20, -30))

    def hp_indicator(self, hp, x, y):
        self.hp_ratio = hp/100
        self.hp = pygame.draw.rect(self.screen, (0, 255, 0), (x, y, self.hp_ratio*385, 30))


    def draw_ground(self):
        self.ground2 = pygame.transform.scale(self.ground, (self.SCREEN_WIDTH, 200))
        self.screen.blit(self.ground2, (0, 590))

run = MainGame()