import pygame


class KurtVillamor:
    def __init__(self):
        """
        One of the S3's Great Goliaths, The keeper of the fire and the guardian of Flames. Kurt protects the lands with his own might and twisted humor. His style was inspired
        by his idol in his favorite fiction which is the Cat War 2 - which Littler (The main Antagonist) burn his enemies alive.

         ' I want to give my enemies a chance to see Kobe Bryant in person '

        """

        self.CHARACTER_SHEET = pygame.image.load('assets/graphics/characters/Kurt/sprites/kurt.png')  # Sprite sheet
        self.CHARACTER_FRAMES = [6, 1, 1, 4, 8, 4, 2, 2, 2, 2, 3, 2]  # Character Frames as a list
        self.animation = self.load_images(self.CHARACTER_SHEET, self.CHARACTER_FRAMES)  # Get all the frames in the frame sheet
        self.action = 4  # Actions available ; 0 = Walking; 1: Hit while Block; 2: Blocking; 3: Dead; 4: Idle; 5:Jump; 6:lk; 7: lp; 8: Projectile; 9: Launching 8; 10: rk; 11: rp
        self.frame_index = 0  # frames where the loop is in
        self.image = self.animation[self.action][self.frame_index]  # Original Image
        self.update_time = pygame.time.get_ticks()  # Update time


    def load_images(self, sprite_sheet, animation_steps):  # Loop to get all the frames in the Sprite sheet
        # get animation steps in the sprite sheet
        self.animation_list = []
        for y, animation in enumerate(animation_steps):
            self.temp_img_list = []
            for x in range(animation):
                self.temp_img = sprite_sheet.subsurface(x * 300, y * 317, 300, 317)
                self.temp_img_list.append(pygame.transform.scale(self.temp_img, (350, 350)))
            self.animation_list.append(self.temp_img_list)
        return self.animation_list

    def draw(self, surface, rect):  # Drawing The sprite easier with the guide of the hit box
        surface.blit(self.image, (rect.x - 120, rect.y - 30))






