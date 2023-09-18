import os
from settings import *
from timers import Timer


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, scale, speed, enemy_group):
        super().__init__()

        self.alive = True

        self.flip = False
        self.speed = speed
        self.health = 100
        self.max_health = self.health

        # Animation variables
        self.animation_list = []
        self.animation_masks = []
        self.action = 0
        self.frame_index = 0

        self.update_time = pygame.time.get_ticks()
        self.enemy_group = enemy_group

        animation_types = ['Idle', 'Walk', 'Punch', 'Kick', 'Hurt']
        for animation in animation_types:
            # new list for every animation
            temp_list = []
            temp_list2 = []
            # number of files in animation
            num_of_frames = len(os.listdir(f"sprites/Player/{animation}"))
            for i in range(num_of_frames):
                image = pygame.image.load(f'sprites/Player/{animation}/{i}.png').convert_alpha()
                image = pygame.transform.scale(image, (image.get_width() * scale, image.get_height() * scale))
                mask = pygame.mask.from_surface(image)
                temp_list.append(image)
                temp_list2.append(mask)
            self.animation_list.append(temp_list)
            self.animation_masks.append(temp_list2)
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect(center=pos)
        self.rect = self.rect.inflate(-50, 0)
        self.mask = self.animation_masks[self.action][self.frame_index]
        self.mask_image = self.mask.to_surface()

        self.direction = pygame.math.Vector2()
        self.pos = pygame.math.Vector2(self.rect.center)
        self.speed = speed

        # timers
        self.timers = {
            'Punch': Timer(300, self.punch_attack),
            'Kick': Timer(500, self.kick_attack),
            'Hit': Timer(150, self.is_hit)
        }

        # attacks
        self.attacking = False

    def input(self):
        keys = pygame.key.get_pressed()
        if not self.timers['Punch'].active:
            # movement
            if keys[pygame.K_UP]:
                self.direction.y = -1
                self.action = 1
            elif keys[pygame.K_DOWN]:
                self.direction.y = 1
                self.action = 1
            else:
                self.direction.y = 0
            if keys[pygame.K_LEFT]:
                self.direction.x = -1
                self.action = 1
                self.flip = True
            elif keys[pygame.K_RIGHT]:
                self.direction.x = 1
                self.action = 1
                self.flip = False
            else:
                self.direction.x = 0

            # attacks
            if keys[pygame.K_d]:
                self.timers['Punch'].activate()
                self.direction = pygame.math.Vector2()
                self.frame_index = 0
            if keys[pygame.K_s]:
                self.timers['Kick'].activate()
                self.direction = pygame.math.Vector2()
                self.frame_index = 0

    def is_hit(self):
        self.health -= 10
        if self.health <= 0:
            self.alive = False

    def punch_attack(self):
        for enemy in self.enemy_group:
            if pygame.sprite.collide_mask(self, enemy):
                if enemy.alive:
                    enemy.punched = True
                    enemy.timers['Hit'].activate()

    def kick_attack(self):
        for enemy in self.enemy_group:
            if pygame.sprite.collide_mask(self, enemy):
                if enemy.alive:
                    enemy.kicked = True
                    enemy.timers['Hit'].activate()

    def move(self, dt):
        # normalize a vector+
        if self.direction.magnitude() > 0:
            self.direction = self.direction.normalize()

        self.pos += self.direction * self.speed * dt
        self.rect.center = self.pos

        # if self.rect.right > WINDOW_WIDTH - SCROLL_THRESH:
        #     # self.rect.x -= self.pos.x
        #     screen_scroll = -self.pos.x

        # return screen_scroll

    def get_action(self):
        if self.direction.magnitude() == 0:
            self.action = 0

        if self.timers['Punch'].active:
            self.action = 2

        if self.timers['Kick'].active:
            self.action = 3

        if self.timers['Hit'].active:
            self.action = 4

    def update_timers(self):
        for timers in self.timers.values():
            timers.update()

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
            self.frame_index = 0

        self.image = self.animation_list[self.action][int(self.frame_index)]
        self.mask = self.animation_masks[self.action][int(self.frame_index)]

    def update(self, dt):
        self.input()
        self.get_action()
        self.update_timers()
        self.move(dt)
        self.update_animation()

    def draw(self, surface):
        surface.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)

        # mask_surface = pygame.Surface(self.mask.get_size(), pygame.SRCALPHA)
        # mask_surface.fill((255, 255, 255, 100))  # Fill with a semi-transparent white color
        # surface.blit(mask_surface, self.rect.topleft)


class HealthBar:
    def __init__(self, x, y, health, max_health):
        self.x = x
        self.y = y
        self.health = health
        self.max_health = max_health

    def draw(self, health, surface):

        self.health = health
        ratio = self.health / self.max_health

        pygame.draw.rect(surface, BLACK, (self.x - 2, self.y - 2, 154, 24))
        pygame.draw.rect(surface, RED, (self.x, self.y, 150, 20))
        pygame.draw.rect(surface, GREEN, (self.x, self.y, 150 * ratio, 20))



