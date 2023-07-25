import pygame



class P1Controls:
    def __init__(self, character):
        pygame.init()
        self.character = character
        self.logo = pygame.image.load('assets/graphics/p1.png').convert_alpha()
        self.hp = 100  # Health of the Character
        self.alive = True  # Check if the Character is Alive
        self.rectStand = pygame.Rect((100, 280, 100, 300))  # Hit box Standing
        self.vel_y = 0  # Y Velocity / Position
        self.blocking = False  # Crouch Checker
        self.jumping = False  # Jumping Checker
        self.movements = 0  # Movement Checker


    def draw_player1(self, surface):
        surface.blit(pygame.transform.scale(self.logo, (406*0.5, 448*0.5)), (self.rectStand.x - 50, self.rectStand.y - 190))
        pygame.draw.rect(surface, (255, 0, 0), self.rectStand)
        self.character.draw(surface, self.rectStand)


    def movement_player1(self, screen_width, screen_height):
        # Movement variables
        self.SPEED = 10
        self.GRAVITY = 2
        self.dx = 0
        self.dy = 0

        # Getting the pressed Button
        self.key = pygame.key.get_pressed()



        if self.key[pygame.K_a]:
            self.blocking = False
            self.dx -= self.SPEED
            self.movements = 1
            print("1 Walking Left")
        if self.key[pygame.K_d]:
            self.blocking = False
            self.dx = self.SPEED
            self.movements = 2
            print("1 Walking Right")
        if self.key[pygame.K_w] and self.jumping == False:
            self.blocking = False
            self.jumping = True
            self.vel_y = -35
            self.movements = 3
            self.rectStand.update(self.rectStand.left, self.rectStand.top, 100, 150)
            print("1 Jumping")
        if self.key[pygame.K_s]:
            self.blocking = True
            print("1 Blocking")
            self.movements = 4


            # self.rectStand.update(self.rectStand.left, self.rectStand.bottom, 100, 300)

        # Gravity Physics
        self.vel_y += self.GRAVITY
        self.dy += self.vel_y

        # Stage Limit
        if self.rectStand.left + self.dx < 0:
            self.dx = 0 - self.rectStand.left

        if self.rectStand.right + self.dx > screen_width:
            self.dx = screen_width - self.rectStand.right

        if self.rectStand.bottom + self.dy > screen_height - 10:
            self.vel_y = 0
            self.jumping = False
            self.rectStand.update(self.rectStand.left, self.rectStand.top, 100, 300)
            self.dy = screen_height - 10 - self.rectStand.bottom


        # Update Position
        self.rectStand.x += self.dx
        self.rectStand.y += self.dy



















