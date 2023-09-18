import sys

from player import Player, HealthBar
from settings import *
from enemies import EnemiesKick, EnemiesPunch
import csv


class World:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Escape The Copper Mine District")
        self.clock = pygame.time.Clock()

        # sprite groups
        self.player_group = pygame.sprite.Group()
        self.enemy_group = pygame.sprite.Group()

        self.player = Player((350, 450), SCALE, SPEED, self.enemy_group)
        # self.health_bar = HealthBar(10, 10, self.player.health, self.player.health)

        # load world tiles and data
        self.world = [] # processed tiles
        self.world_data = [] # number assigned to each tile
        for row in range(ROWS):
            r = [-1] * COLUMNS
            self.world_data.append(r)

        with open(f'tiles and background/world grid/WorldGrid 2.csv', newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            for x, row in enumerate(reader):
                for y, tile in enumerate(row):
                    self.world_data[x][y] = int(tile)

        # load background tiles and images
        self.background = [] # loads the processed tiles
        self.background_data = [] # number assigned to each tile in bg
        self.img_list = [] # loads all the tiles images
        for x in range(TILE_BG_TYPES):
            img = pygame.image.load(f'tiles and background/tiles/{x}.png').convert_alpha()
            img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
            self.img_list.append(img)

        for row in range(ROWS):
            r = [-1] * COLUMNS
            self.background_data.append(r)
        with open(f'tiles and background/background grid/BackGroundTiles.csv', newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            for x, row in enumerate(reader):
                for y, tile in enumerate(row):
                    self.background_data[x][y] = int(tile)

        self.process_bg_data(self.background_data)
        self.process_world_data(self.world_data)

    def process_bg_data(self, data):
        for z, row in enumerate(data):
            for c, tile in enumerate(row):
                img = self.img_list[tile]
                img_rect = img.get_rect()
                img_rect.x = c * TILE_SIZE
                img_rect.y = z * TILE_SIZE
                tile_data = (img, img_rect)
                self.background.append(tile_data)

    def draw_background(self):
        self.screen.fill(BACKGROUND)
        for tile in self.background:
            self.screen.blit(tile[0], tile[1])

    def process_world_data(self, data):
        for z, row in enumerate(data):
            for c, tile in enumerate(row):
                if tile == 0:
                    self.player = Player((c * TILE_SIZE, z * TILE_SIZE), SCALE, SPEED, self.enemy_group)
                    self.health_bar = HealthBar(10, 10, self.player.health, self.player.health)
                if tile == 1:
                    enemy = EnemiesPunch('Punk', (c * TILE_SIZE, z * TILE_SIZE), SCALE, SPEED - 50, self.player)
                    self.enemy_group.add(enemy)
                elif tile == 2:
                    enemy = EnemiesPunch('BigGuy', (c * TILE_SIZE, z * TILE_SIZE), SCALE, SPEED - 50, self.player)
                    self.enemy_group.add(enemy)

    def run(self):
        while 1:
            self.draw_background()
            # self.health_bar.draw(self.player.health, self.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            dt = self.clock.tick() / 1000

            self.player.update(dt)
            self.player.draw(self.screen)

            for enemy in self.enemy_group:
                enemy.update(dt)
                enemy.draw(self.screen)
                # pygame.draw.rect(self.screen, RED, enemy.vision)
                # pygame.draw.rect(self.screen, GREEN, enemy.hit_box)
            # self.enemy_group.draw(self.screen)
            # self.enemy_group.update(dt)

            pygame.display.update()


game = World()
game.run()


