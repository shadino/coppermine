import os
from settings import *
from timers import Timer


class EnemiesPunch(pygame.sprite.Sprite):
    def __init__(self, enemy_type, pos, scale, speed, player):
        super().__init__()
        self.update_time = pygame.time.get_ticks()

        # enemy animation and speeд
        self.flip = False
        self.speed = speed
        self.animation_list = []
        self.animation_masks = []
        self.action = 0
        self.frame_index = 0

        # enemy health and alive status
        self.alive = True
        self.health = 150
        self.max_health = self.health
        self.punched = False
        self.kicked = False
        self.speed = speed

        self.player = player

        # AI variables
        self.ai_moving_right = True
        self.ai_moving_left = False
        self.counter = 0
        self.idle_time = 0
        self.stunned = 0
        self.attack_cd = 1000

        self.enemy_type = enemy_type

        animation_types = ['Idle', 'Walk', 'Punch', 'Hurt', 'Death']
        for animation in animation_types:
            # new list for every animation
            temp_list = []
            temp_list2 = []
            # number of files in animation
            num_of_frames = len(os.listdir(f"sprites/Enemies/Enemies Punch/{enemy_type}/{animation}"))
            for i in range(num_of_frames):
                image = pygame.image.load(f'sprites/Enemies/Enemies Punch/{enemy_type}/{animation}/{i}.png').convert_alpha()
                image = pygame.transform.scale(image, (image.get_width() * scale, image.get_height() * scale))
                mask = pygame.mask.from_surface(image)
                temp_list.append(image)
                temp_list2.append(mask)
            self.animation_list.append(temp_list)
            self.animation_masks.append(temp_list2)

        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect(center=pos)
        self.mask = self.animation_masks[self.action][self.frame_index]
        self.mask_image = self.mask.to_surface()

        self.direction = pygame.math.Vector2(1, 0)
        self.pos = pygame.math.Vector2(self.rect.center)
        self.vision = pygame.Rect(0, 0, 150, 20)
        self.hit_box = pygame.Rect(0, 0, 40, 20)

        # timers
        self.timers = {
            'Punch': Timer(300, self.punch),
            'Hit': Timer(150, self.is_hit)
        }

    def punch(self):
        if pygame.sprite.collide_mask(self, self.player):
            if self.player.alive:
                self.player.timers['Hit'].activate()

    def is_hit(self):
        if self.punched:
            self.health -= 25
            self.stunned = 1000
            self.punched = False
        elif self.kicked:
            self.health -= 50
            self.kicked = False
        # self.health -= 25
        # print(self.health)
        if self.health <= 0:
            self.alive = False
            print(self.alive)
            print("target is dead")

    def move(self, dt):
        # normalize a vector+
        if self.direction.magnitude() > 0:
            self.direction = self.direction.normalize()

        self.pos += self.direction * self.speed * dt
        self.rect.center = self.pos

        if self.enemy_type == 'Punk':
            if self.direction.x == -1:
                self.flip = False
            else:
                self.flip = True
        # else:
        #     if self.direction.x == -1:
        #         self.flip = True
        #     else:
        #         self.flip = False
        #
        # print(self.direction)

    def enemy_ai(self):
        if self.alive and self.player.alive:
            if self.direction.x != 0 and random.randint(1, 1000) == 1:
                self.direction.x = 0
                self.idle_time = 1000

            if self.vision.colliderect(self.player.rect):
                self.direction.x = 0
                if self.enemy_type == 'Punk' and self.ai_moving_right:
                    self.flip = True
                else:
                    self.flip = False
                # if self.enemy_type == 'BigGuy' and self.ai_moving_left:
                #     self.flip = False
                # else:
                #     self.flip = True
                self.hit_box.center = (self.rect.center + 10 * self.direction)
                if self.hit_box.colliderect(self.player.rect):
                    self.attack_cd -= 1
                    self.stunned -= 1
                    if self.attack_cd <= 0 and self.stunned <= 0:
                        self.timers['Punch'].activate()
                        self.attack_cd = 1000

            else:
                if self.direction.x != 0:
                    if self.direction.x == 1:
                        self.ai_moving_right = True
                    else:
                        self.ai_moving_right = False
                    self.ai_moving_left = not self.ai_moving_right
                    self.counter += 1
                    self.vision.center = (self.rect.center + 75 * self.direction)

                    if self.counter > PATROL_TIMER:
                        self.direction.x *= -1
                        self.counter *= -1
                else:
                    self.idle_time -= 1
                    if self.idle_time <= 0:
                        self.direction.x = 1

        # if self.enemy_type == 'Punk' and self.ai_moving_right:
        #     self.flip = True
        # else:
        #     self.flip = False
        # if self.enemy_type == 'BigGuy' and self.ai_moving_right:
        #     self.flip = False
        # else:
        #     self.flip = True

        # if self.enemy_type == 'Punk':
        #     if self.direction.x == -1:
        #         self.flip = False
        #     else:
        #         self.flip = True
        # if self.enemy_type == 'BigGuy':
        #     if self.direction.x == -1:
        #         self.flip = True
        #     else:
        #         self.flip = False

    def get_action(self):
        if self.direction.magnitude() == 0:
            self.action = 0

        if self.direction.magnitude() != 0:
            self.action = 1

        if self.timers['Punch'].active:
            self.action = 2

        if self.timers['Hit'].active:
            self.action = 3

        if self.alive is False:
            self.health = 0
            self.speed = 0
            self.action = 4

    def update_action(self, new_action):
        if new_action != self.action:
            self.action = new_action
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def update_animation(self):

        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        if self.frame_index >= len(self.animation_list[self.action]):
            if self.action == 4:
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:
                self.frame_index = 0

        self.image = self.animation_list[self.action][int(self.frame_index)]
        self.mask = self.animation_masks[self.action][int(self.frame_index)]

    def update_timers(self):
        for timers in self.timers.values():
            timers.update()

    def update(self, dt):
        self.get_action()
        self.update_animation()
        self.update_timers()
        self.move(dt)
        self.enemy_ai()

    def draw(self, surface):
        surface.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)

        # mask_surface = pygame.Surface(self.mask.get_size(), pygame.SRCALPHA)
        # mask_surface.fill((255, 255, 255, 100))  # Fill with a semi-transparent white color
        # surface.blit(mask_surface, self.rect.topleft)


class EnemiesKick(pygame.sprite.Sprite):
    def __init__(self, enemy_type, pos, scale, speed):
        super().__init__()
        self.update_time = pygame.time.get_ticks()

        self.enemy_type = enemy_type
        self.flip = False
        self.speed = speed
        self.animation_list = []
        self.action = 0
        self.frame_index = 0

        animation_types = ['Idle', 'Walk', 'Kick', 'Hurt', 'Death']
        for animation in animation_types:
            # new list for every animation
            temp_list = []
            # number of files in animation
            num_of_frames = len(os.listdir(f"sprites/Enemies/Enemies Kick/{enemy_type}/{animation}"))
            for i in range(num_of_frames):
                image = pygame.image.load(f'sprites/Enemies/Enemies Kick/{enemy_type}/{animation}/{i}.png').convert_alpha()
                image = pygame.transform.scale(image, (image.get_width() * scale, image.get_height() * scale))
                temp_list.append(image)
            self.animation_list.append(temp_list)

        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect(center=pos)

        self.direction = pygame.math.Vector2()
        self.pos = pygame.math.Vector2(self.rect.center)
        self.speed = speed

    def enemy_ai(self):
        pass

    def update_animation(self):

        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        if self.frame_index >= len(self.animation_list[self.action]):
            self.frame_index = 0

        self.image = self.animation_list[self.action][int(self.frame_index)]

    def update(self, dt):
        self.update_animation()

    def draw(self, surface):
        surface.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)


