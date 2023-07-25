import pygame


class Fighter1:
    def __init__(self, x, y, data, spite_sheet, animation_steps):
        self.width = data[0]
        self.height = data[1]
        self.scale = data[2]
        self.offset = data[3]
        self.animation_list = self.load_images(spite_sheet, animation_steps)
        self.action = 0  # Actions available ; 0 = Walking; 1: Hit while Block; 2: Blocking; 3: Dead; 4: Idle; 5:Jump; 6:lk; 7: lp; 8: Projectile; 9: Launching 8; 10: rk; 11: rp
        self.frame_index = 0
        self.image = self.animation_list[self.action][self.frame_index]
        self.update_time = pygame.time.get_ticks()
        self.hp = 100
        self.alive = True
        self.rect = pygame.Rect((x, y, 100, 300))
        self.vel_y = 0
        self.hit = False
        self.flip = False
        self.run = False
        self.jump_chk = False
        self.block_chk = False
        self.attacking = False
        self.attack_type = 0

    def load_images(self, sprite_sheet, animation_steps):
        # get animation steps in the sprite sheet
        self.animation_list = []
        for y, animation in enumerate(animation_steps):
            self.temp_img_list = []
            for x in range(animation):
                self.temp_img = sprite_sheet.subsurface(x*self.width, y*self.height, self.width, self.height)
                self.temp_img_list.append(pygame.transform.scale(self.temp_img, (self.width * self.scale, self.height * self.scale)))
            self.animation_list.append(self.temp_img_list)
        return self.animation_list


    def draw_character(self, surface):
        self.img = pygame.transform.flip(self.image, self.flip, False)
        pygame.draw.rect(surface, (0, 128, 0), self.rect)
        surface.blit(self.img, (self.rect.x - self.offset[0], self.rect.y - self.offset[1]))

    def move_character(self, screen_width, screen_height, surface, target):
        self.SPEED = 10
        self.GRAVITY = 2
        self.dx = 0
        self.dy = 0
        self.run = False
        self.attack_type = 0

        # Pressing Key
        self.key = pygame.key.get_pressed()


        if self.alive == True:
            if self.key[pygame.K_a] and self.block_chk == False:
                self.dx -= self.SPEED
                self.run = True
            if self.key[pygame.K_d] and self.block_chk == False:
                self.dx = self.SPEED
                self.run = True
            if self.key[pygame.K_w] and self.jump_chk == False and self.block_chk == False:
                self.vel_y = -35
                self.jump_chk = True
            if self.key[pygame.K_s]:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        self.block_chk = True
                    if event.type == pygame.KEYUP:
                        self.block_chk = False


        if self.attacking == False  and self.alive == True:
            # Basic Attacks
            if self.key[pygame.K_t]:
                self.lower_punch(surface, target)

            if self.key[pygame.K_y]:
                self.upper_punch(surface, target)

            if self.key[pygame.K_g]:
                self.upper_kick(surface, target)

            if self.key[pygame.K_h]:
                self.lower_kick(surface, target)


        # Gravity Physics
        self.vel_y += self.GRAVITY
        self.dy += self.vel_y

        # Movement Limitations
        if self.rect.left + self.dx < 0:
            self.dx = 0 - self.rect.left

        if self.rect.right + self.dx > screen_width:
            self.dx = screen_width - self.rect.right

        if self.rect.bottom + self.dy > screen_height - 10:
            self.vel_y = 0
            self.jump_chk = False
            self.dy = screen_height - 10 - self.rect.bottom

        # Always Face to Face
        if target.rect.centerx > self.rect.centerx:
            self.flip = False
        else:
            self.flip = True

        # update
        self.rect.x += self.dx
        self.rect.y += self.dy

    def update_animate(self):
        if self.hit == True:
            self.update_action(8)
        elif self.hp <= 0:
            self.hp = 0
            self.alive = False
            self.update_action(7)
        elif self.attacking == True:
            if self.attack_type == 1:
                self.update_action(4)
            elif self.attack_type == 2:
                self.update_action(2)
            elif self.attack_type == 3:
                self.update_action(3)
            elif self.attack_type == 4:
                self.update_action(5)

        elif self.jump_chk == True:
            self.update_action(6)
        elif self.run == True:
            self.update_action(1)
        else:
            self.update_action(0)

        self.animation_time = 100
        self.image = self.animation_list[self.action][self.frame_index]
        if pygame.time.get_ticks() - self.update_time > self.animation_time:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()
        if self.frame_index >= len(self.animation_list[self.action]):
            if self.alive == False:
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:
                self.frame_index = 0
                if self.action == 2 or self.action == 3 or self.action == 4 or self.action == 5:
                    self.attacking = False
                if self.action == 8:
                    self.hit = False
                    self.attacking = False

    def update_action(self, new_action):
        if new_action != self.action:
            self.action = new_action
            self.frame_index = 0
            pygame.time.get_ticks()


    def upper_punch(self, surface, target):
        self.attacking = True
        self.attack_type = 1
        self.attack_up1 = pygame.Rect(self.rect.centerx - (2 * self.rect.width * self.flip), self.rect.y, 2*self.rect.width, self.rect.height/2)
        pygame.draw.rect(surface, (255, 0, 0), self.attack_up1)
        if self.attack_up1.colliderect(target.rect):
            target.hit = True
            target.hp -= 5



    def lower_punch(self, surface, target):
        self.attacking = True
        self.attack_type = 2
        self.attack_lp = pygame.Rect(self.rect.centerx - (2 * self.rect.width * self.flip), self.rect.y, 1.5 * self.rect.width, self.rect.height / 2)
        pygame.draw.rect(surface, (0, 0, 255), self.attack_lp)
        if self.attack_lp.colliderect(target.rect):
            target.hit = True
            target.hp -= 2



    def upper_kick(self, surface, target):
        self.attacking = True
        self.attack_type = 3
        self.attack_uk = pygame.Rect(self.rect.centerx - (2 * self.rect.width * self.flip), self.rect.centery, 2 * self.rect.width, self.rect.height / 2)
        pygame.draw.rect(surface, (0, 0, 255), self.attack_uk)
        if self.attack_uk.colliderect(target.rect):
            target.hit = True
            target.hp -= 5



    def lower_kick(self, surface, target):
        self.attacking = True
        self.attack_type = 4
        self.attack_lk = pygame.Rect(self.rect.centerx - (2 * self.rect.width * self.flip), self.rect.centery, 2 * self.rect.width, self.rect.height / 2)
        pygame.draw.rect(surface, (255, 0, 0), self.attack_lk)
        if self.attack_lk.colliderect(target.rect):
            target.hit = True
            target.hp -= 2


class Fighter2:
    def __init__(self, x, y, data, spite_sheet, animation_steps):
        self.width = data[0]
        self.height = data[1]
        self.scale = data[2]
        self.offset = data[3]
        self.animation_list = self.load_images(spite_sheet, animation_steps)
        self.action = 0  # 0 = Idle, 1 = Run, 2 = lp, 3= lk, 4 = up, 5 = uk, 6 = jump, 7 = die
        self.frame_index = 0
        self.image = self.animation_list[self.action][self.frame_index]
        self.update_time = pygame.time.get_ticks()
        self.hp = 100
        self.alive = True
        self.rect = pygame.Rect((x, y, 100, 300))
        self.vel_y = 0
        self.hit = False
        self.flip = False
        self.run = False
        self.jump_chk = False
        self.block_chk = False
        self.attacking = False
        self.attack_type = 0

    def load_images(self, sprite_sheet, animation_steps):
        # get animation steps in the sprite sheet
        self.animation_list = []
        for y, animation in enumerate(animation_steps):
            self.temp_img_list = []
            for x in range(animation):
                self.temp_img = sprite_sheet.subsurface(x*self.width, y*self.height, self.width, self.height)
                self.temp_img_list.append(pygame.transform.scale(self.temp_img, (self.width * self.scale, self.height * self.scale)))
            self.animation_list.append(self.temp_img_list)
        return self.animation_list


    def draw_character(self, surface):
        self.img = pygame.transform.flip(self.image, self.flip, False)
        pygame.draw.rect(surface, (0, 128, 0), self.rect)
        surface.blit(self.img, (self.rect.x - self.offset[0], self.rect.y - self.offset[1]))

    def move_character(self, screen_width, screen_height, surface, target):
        self.SPEED = 10
        self.GRAVITY = 2
        self.dx = 0
        self.dy = 0
        self.run = False
        self.attack_type = 0

        # Pressing Key
        self.key = pygame.key.get_pressed()

        if self.alive == True:
            if self.key[pygame.K_LEFT] and self.block_chk == False:
                self.dx -= self.SPEED
                self.run = True
            if self.key[pygame.K_RIGHT] and self.block_chk == False:
                self.dx = self.SPEED
                self.run = True
            if self.key[pygame.K_UP] and self.jump_chk == False and self.block_chk == False:
                self.vel_y = -35
                self.jump_chk = True
            if self.key[pygame.K_DOWN]:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        self.block_chk = True
                    if event.type == pygame.KEYUP:
                        self.block_chk = False


        if self.attacking == False and self.alive == True:
            # Basic Attacks
            if self.key[pygame.K_KP4]:
                self.lower_punch(surface, target)

            if self.key[pygame.K_KP5]:
                self.upper_punch(surface, target)

            if self.key[pygame.K_KP1]:
                self.upper_kick(surface, target)

            if self.key[pygame.K_KP2]:
                self.lower_kick(surface, target)


        # Gravity Physics
        self.vel_y += self.GRAVITY
        self.dy += self.vel_y

        # Movement Limitations
        if self.rect.left + self.dx < 0:
            self.dx = 0 - self.rect.left

        if self.rect.right + self.dx > screen_width:
            self.dx = screen_width - self.rect.right

        if self.rect.bottom + self.dy > screen_height - 10:
            self.vel_y = 0
            self.jump_chk = False
            self.dy = screen_height - 10 - self.rect.bottom

        # Always Face to Face
        if target.rect.centerx > self.rect.centerx:
            self.flip = False
        else:
            self.flip = True

        # update
        self.rect.x += self.dx
        self.rect.y += self.dy

    def update_animate(self):
        if self.hit == True:
            self.update_action(8)
        elif self.hp <= 0:
            self.hp = 0
            self.alive = False
            self.update_action(7)
        elif self.attacking == True:
            if self.attack_type == 1:
                self.update_action(4)
            elif self.attack_type == 2:
                self.update_action(2)
            elif self.attack_type == 3:
                self.update_action(3)
            elif self.attack_type == 4:
                self.update_action(5)
        elif self.jump_chk == True:
            self.update_action(6)
        elif self.run == True:
            self.update_action(1)
        else:
            self.update_action(0)

        self.animation_time = 100
        self.image = self.animation_list[self.action][self.frame_index]
        if pygame.time.get_ticks() - self.update_time > self.animation_time:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()
        if self.frame_index >= len(self.animation_list[self.action]):
            if self.alive == False:
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:
                self.frame_index = 0
                if self.action == 2 or self.action == 3 or self.action == 4 or self.action == 5:
                    self.attacking = False
                if self.action == 8:
                    self.hit = False
                    self.attacking = False

    def update_action(self, new_action):
        if new_action != self.action:
            self.action = new_action
            self.frame_index = 0
            pygame.time.get_ticks()


    def upper_punch(self, surface, target):
        self.attacking = True
        self.attack_type = 1
        self.attack_up1 = pygame.Rect(self.rect.centerx - (2 * self.rect.width * self.flip), self.rect.y, 2*self.rect.width, self.rect.height/2)
        pygame.draw.rect(surface, (255, 0, 0), self.attack_up1)
        if self.attack_up1.colliderect(target.rect):
            target.hit = True
            target.hp -= 5



    def lower_punch(self, surface, target):
        self.attacking = True
        self.attack_type = 2
        self.attack_lp = pygame.Rect(self.rect.centerx - (2 * self.rect.width * self.flip), self.rect.y, 1.5 * self.rect.width, self.rect.height / 2)
        pygame.draw.rect(surface, (0, 0, 255), self.attack_lp)
        if self.attack_lp.colliderect(target.rect):
            target.hit = True
            target.hp -= 2



    def upper_kick(self, surface, target):
        self.attacking = True
        self.attack_type = 3
        self.attack_uk = pygame.Rect(self.rect.centerx - (2 * self.rect.width * self.flip), self.rect.centery, 2 * self.rect.width, self.rect.height / 2)
        pygame.draw.rect(surface, (0, 0, 255), self.attack_uk)
        if self.attack_uk.colliderect(target.rect):
            target.hit = True
            target.hp -= 5



    def lower_kick(self, surface, target):
        self.attacking = True
        self.attack_type = 4
        self.attack_lk = pygame.Rect(self.rect.centerx - (2 * self.rect.width * self.flip), self.rect.centery, 2 * self.rect.width, self.rect.height / 2)
        pygame.draw.rect(surface, (255, 0, 0), self.attack_lk)
        if self.attack_lk.colliderect(target.rect):
            target.hit = True
            target.hp -= 2



