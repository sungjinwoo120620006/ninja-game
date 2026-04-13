import os
import sys
import math
import random

import pygame

from Scripts.utils import load_image, load_images, Animation, load_sprite_sheet
from Scripts.entities import PhysicsEntity, Player1, Enemy , Figher
from Scripts.tilemap import Tilemap
from Scripts.cloud import Clouds
from Scripts.particle import Particle
from Scripts.spark import Spark
# from Scripts.tilemap2 import TiledMap2

class Game:
    def __init__(self):
        pygame.init() # Khởi tạo tất cả các module của pygame

        pygame.display.set_caption('ninja game') # Đặt tên cửa sổ game
        self.screen = pygame.display.set_mode((640, 480)) # Cửa sổ thực tế hiển thị
        # Surface vẽ game ở độ phân giải thấp (320x240) để tạo hiệu ứng Pixel Art
        self.display = pygame.Surface((320, 240), pygame.SRCALPHA)
        # Surface thứ 2 để vẽ nền và xử lý các hiệu ứng hậu kỳ
        self.display_2 = pygame.Surface((320, 240))

        self.clock = pygame.time.Clock() # Bộ đếm thời gian để kiểm soát FPS

        self.movement = [False, False] # Trạng thái bấm phím di chuyển [Trái, Phải]

        # Từ điển chứa toàn bộ tài nguyên hình ảnh của Game
        self.assets = {
            'decor': load_images('tiles/decor'),
            'grass': load_images('tiles/grass'),
            'large_decor': load_images('tiles/large_decor'),
            'stone': load_images('tiles/stone'),
            'player': load_image('entities/player.png'),
            'background': load_image('background.png'),
            'clouds': load_images('clouds'),
            # Các Animation được khởi tạo với độ trễ khung hình (img_dur)
            'enemy/idle': Animation(load_images('entities/enemy/idle'), img_dur=6),
            'enemy/run': Animation(load_images('entities/enemy/run'), img_dur=4),
            'player/idle': Animation(load_images('entities/player/idle'), img_dur=6),
            'player/run': Animation(load_images('entities/player/run'), img_dur=4),
            'player/jump': Animation(load_images('entities/player/jump')),
            'player/slide': Animation(load_images('entities/player/slide')),
            'player/wall_slide': Animation(load_images('entities/player/wall_slide')),
            'particle/leaf': Animation(load_images('particles/leaf'), img_dur=20, loop=False),
            'particle/particle': Animation(load_images('particles/particle'), img_dur=6, loop=False),
            'gun': load_image('gun.png'),
            'projectile': load_image('projectile.png'),
            'gotoku/idle': Animation(load_sprite_sheet('entities/special_enemy/Gotoku/IDLE.png', 128), img_dur=6,
                                      loop=False),
            'gotoku/attack_1': Animation(load_sprite_sheet('entities/special_enemy/Gotoku/ATTACK_1.png', 128), img_dur=6,
                                      loop=False),
            'gotoku/attack_2': Animation(load_sprite_sheet('entities/special_enemy/Gotoku/ATTACK_2.png', 128), img_dur=6,
                                     loop=False),
            'gotoku/attack_3': Animation(load_sprite_sheet('entities/special_enemy/Gotoku/ATTACK_3.png', 128), img_dur=6,
                                     loop=False),
            'gotoku/dead': Animation(load_sprite_sheet('entities/special_enemy/Gotoku/DEAD.png', 128), img_dur=6,
                                     loop=False),
            'gotoku/hurt': Animation(load_sprite_sheet('entities/special_enemy/Gotoku/HURT.png', 128), img_dur=6,
                                     loop=False),
            'gotoku/walk': Animation(load_sprite_sheet('entities/special_enemy/Gotoku/WALK.png', 128), img_dur=6,
                                     loop=False),
            'onre/idle': Animation(load_sprite_sheet('entities/special_enemy/Onre/IDLE.png', 128), img_dur=6,
                                     loop=False),
            'onre/attack_1': Animation(load_sprite_sheet('entities/special_enemy/Onre/ATTACK_1.png', 128),
                                         img_dur=6,
                                         loop=False),
            'onre/attack_2': Animation(load_sprite_sheet('entities/special_enemy/Onre/ATTACK_2.png', 128),
                                         img_dur=6,
                                         loop=False),
            'onre/attack_3': Animation(load_sprite_sheet('entities/special_enemy/Onre/ATTACK_3.png', 128),
                                         img_dur=6,
                                         loop=False),
            'onre/dead': Animation(load_sprite_sheet('entities/special_enemy/Onre/DEAD.png', 128), img_dur=6,
                                     loop=False),
            'onre/hurt': Animation(load_sprite_sheet('entities/special_enemy/Onre/HURT.png', 128), img_dur=6,
                                     loop=False),
            'onre/walk': Animation(load_sprite_sheet('entities/special_enemy/Onre/WALK.png', 128), img_dur=6,
                                   loop=False),
            'yurei/idle': Animation(load_sprite_sheet('entities/special_enemy/Yurei/IDLE.png', 128), img_dur=6,
                                   loop=False),
            'yurei/attack_1': Animation(load_sprite_sheet('entities/special_enemy/Yurei/ATTACK_1.png', 128),
                                       img_dur=6,
                                       loop=False),
            'yurei/attack_2': Animation(load_sprite_sheet('entities/special_enemy/Yurei/ATTACK_2.png', 128),
                                       img_dur=6,
                                       loop=False),
            'yurei/attack_3': Animation(load_sprite_sheet('entities/special_enemy/Yurei/ATTACK_3.png', 128),
                                       img_dur=6,
                                       loop=False),
            'yurei/dead': Animation(load_sprite_sheet('entities/special_enemy/Yurei/DEAD.png', 128), img_dur=6,
                                   loop=False),
            'yurei/hurt': Animation(load_sprite_sheet('entities/special_enemy/Yurei/HURT.png', 128), img_dur=6,
                                   loop=False),
            'yurei/walk': Animation(load_sprite_sheet('entities/special_enemy/Yurei/WALK.png', 128), img_dur=6,
                                   loop=False),
            'samurai/idle': Animation(load_sprite_sheet('entities/special_enemy/Samurai/IDLE.png', 128), img_dur=6,
                                    loop=False),
            'samurai/attack_1': Animation(load_sprite_sheet('entities/special_enemy/Samurai/ATTACK_1.png', 128),
                                        img_dur=6,
                                        loop=False),
            'samurai/attack_2': Animation(load_sprite_sheet('entities/special_enemy/Samurai/ATTACK_2.png', 128),
                                        img_dur=6,
                                        loop=False),
            'samurai/attack_3': Animation(load_sprite_sheet('entities/special_enemy/Samurai/ATTACK_3.png', 128),
                                        img_dur=6,
                                        loop=False),
            'samurai/dead': Animation(load_sprite_sheet('entities/special_enemy/Samurai/DEAD.png', 128), img_dur=6,
                                    loop=False),
            'samurai/hurt': Animation(load_sprite_sheet('entities/special_enemy/Samurai/HURT.png', 128), img_dur=6,
                                    loop=False),
            'samurai/walk': Animation(load_sprite_sheet('entities/special_enemy/Samurai/WALK.png', 128), img_dur=6,
                                    loop=False),
            'fighter/idle': Animation(load_sprite_sheet('entities/special_enemy/Fighter/IDLE.png', 128), img_dur=6,
                                    loop=False),
            'fighter/attack_1': Animation(load_sprite_sheet('entities/special_enemy/Fighter/ATTACK_1.png', 128),
                                        img_dur=6,
                                        loop=False),
            'fighter/attack_2': Animation(load_sprite_sheet('entities/special_enemy/Fighter/ATTACK_2.png', 128),
                                        img_dur=6,
                                        loop=False),
            'fighter/attack_3': Animation(load_sprite_sheet('entities/special_enemy/Fighter/ATTACK_3.png', 128),
                                        img_dur=6,
                                        loop=False),
            'fighter/dead': Animation(load_sprite_sheet('entities/special_enemy/Fighter/DEAD.png', 128), img_dur=6,
                                    loop=False),
            'fighter/hurt': Animation(load_sprite_sheet('entities/special_enemy/Fighter/HURT.png', 128), img_dur=6,
                                    loop=False),
            'fighter/walk': Animation(load_sprite_sheet('entities/special_enemy/Fighter/WALK.png', 128), img_dur=6,
                                    loop=False),
            'shinobi/idle': Animation(load_sprite_sheet('entities/special_enemy/Shinobi/IDLE.png', 128), img_dur=6,
                                    loop=False),
            'shinobi/attack_1': Animation(load_sprite_sheet('entities/special_enemy/Shinobi/ATTACK_1.png', 128),
                                        img_dur=6,
                                        loop=False),
            'shinobi/attack_2': Animation(load_sprite_sheet('entities/special_enemy/Shinobi/ATTACK_2.png', 128),
                                        img_dur=6,
                                        loop=False),
            'shinobi/attack_3': Animation(load_sprite_sheet('entities/special_enemy/Shinobi/ATTACK_3.png', 128),
                                        img_dur=6,
                                        loop=False),
            'shinobi/dead': Animation(load_sprite_sheet('entities/special_enemy/Shinobi/DEAD.png', 128), img_dur=6,
                                    loop=False),
            'shinobi/hurt': Animation(load_sprite_sheet('entities/special_enemy/Shinobi/HURT.png', 128), img_dur=6,
                                    loop=False),
            'shinobi/walk': Animation(load_sprite_sheet('entities/special_enemy/Shinobi/WALK.png', 128), img_dur=6,
                                    loop=False),
        }

        # Hệ thống âm thanh và thiết lập âm lượng cho từng loại SFX
        self.sfx = {
            'jump': pygame.mixer.Sound('data/sfx/jump.wav'),
            'dash': pygame.mixer.Sound('data/sfx/dash.wav'),
            'hit': pygame.mixer.Sound('data/sfx/hit.wav'),
            'shoot': pygame.mixer.Sound('data/sfx/shoot.wav'),
            'ambience': pygame.mixer.Sound('data/sfx/ambience.wav'),
        }
        self.sfx['ambience'].set_volume(0.2)
        # ... thiết lập âm lượng cho các âm thanh khác

        self.clouds = Clouds(self.assets['clouds'], count=16) # Tạo 16 đám mây ngẫu nhiên
        self.player = Player1(self, (50, 50), (8, 15)) # Tạo nhân vật (vị trí, kích thước)

        self.tilemap = Tilemap(self, tile_size=16) # Quản lý bản đồ gạch 16x16 pixel
        self.draw_health_bar(self.display, (10, 10), self.player.health, self.player.max_health)
        self.draw_mana_bar(self.display, (10, 17), self.player.mana, self.player.max_mana)

        self.level = 0 # Chỉ số màn chơi hiện tại
        self.load_level(self.level) # Tải màn chơi đầu tiên
        self.screenshake = 0 # Biến quản lý cường độ rung màn hình
    def draw_health_bar(self,surf,pos,health,maxhealth):
            width = 50
            height = 5
            ratio = health / maxhealth
            pygame.draw.rect(surf,(50 ,0 ,0), (pos[0],pos[1],width,height))
            pygame.draw.rect(surf, (255, 0, 0), (pos[0], pos[1], int(width * ratio), height))
            pygame.draw.rect(surf,(255 ,255, 255),(pos[0],pos[1],width,height),1)

    def draw_mana_bar(self, surf, pos, mana, max_mana):
        if max_mana <= 0:
            return
        width = 50
        height = 5
        ratio = max(0, min(1, mana / max_mana)) if max_mana > 0 else 0
        pygame.draw.rect(surf, (0, 0, 50), (pos[0], pos[1], width, height))
        pygame.draw.rect(surf, (0, 150, 255), (pos[0], pos[1], int(width * ratio), height))
        pygame.draw.rect(surf, (255, 255, 255), (pos[0], pos[1], width, height), 1)

    def load_level(self, map_id):
        self.tilemap.load('data/maps/' + str(map_id) + '.json') # Đọc file map JSON

        # Trích xuất các cây từ tilemap để tạo nơi rơi lá
        self.leaf_spawners = []
        for tree in self.tilemap.extract([('large_decor', 2)], keep=True):
            # Tạo một vùng Rect xung quanh tán cây để lá rơi ra trong vùng đó
            self.leaf_spawners.append(pygame.Rect(4 + tree['pos'][0], 4 + tree['pos'][1], 23, 13))

        # Trích xuất vị trí đặt Player và Enemy từ dữ liệu Map
        self.enemies = []
        for spawner in self.tilemap.extract([('spawners', 0), ('spawners', 1)]):
            if spawner['variant'] == 0: # Variant 0 là người chơi
                self.player.pos = spawner['pos']
                self.player.air_time = 0
            else: # Các variant khác là kẻ thù
                self.enemies.append(Enemy(self, spawner['pos'], (8, 15)))

        self.projectiles = [] # Danh sách đạn đang bay
        self.particles = []   # Danh sách các hạt bụi/lá
        self.sparks = []      # Danh sách tia lửa

        self.scroll = [0, 0]  # Tọa độ camera
        self.dead = 0         # Trạng thái chết (0 là sống, >0 là đang đếm ngược hồi sinh)
        self.transition = -30 # Hiệu ứng chuyển màn (số âm là đang mở màn)



    def run(self):
        pygame.mixer.music.load('data/music.wav')  # Nhạc nền
        pygame.mixer.music.play(-1)  # Chạy lặp vô hạn
        self.sfx['ambience'].play(-1)  # Âm thanh môi trường

        while True:
            # Xóa màn hình bằng màu trong suốt/đen
            self.display.fill((0, 0, 0, 0))
            self.display_2.blit(self.assets['background'], (0, 0))  # Vẽ hình nền

            self.screenshake = max(0, self.screenshake - 1)  # Giảm dần cường độ rung

            # Nếu diệt sạch địch: Tăng transition để chuyển màn
            if not len(self.enemies):
                self.player.health = self.player.max_health
                self.transition += 1
                if self.transition > 30:
                    self.level = min(self.level + 1, len(os.listdir('data/maps')) - 1)
                    self.load_level(self.level)
            if self.transition < 0:
                self.transition += 1  # Hiệu ứng mở màn dần dần

            # Xử lý khi người chơi chết
            if self.dead:
                self.dead += 1
                if self.dead >= 10:  # Chờ 10 frame rồi mới bắt đầu chuyển màn đen
                    self.transition = min(30, self.transition + 1)
                if self.dead > 40:  # Sau 40 frame thì reset màn chơi
                    self.load_level(self.level)
                    self.player.health = self.player.max_health

            # Camera đuổi theo nhân vật (Smooth Scrolling)
            # Công thức: (Mục tiêu - Vị trí hiện tại) / Độ trễ (30)
            self.scroll[0] += (self.player.rect().centerx - self.display.get_width() / 2 - self.scroll[0]) / 30
            self.scroll[1] += (self.player.rect().centery - self.display.get_height() / 2 - self.scroll[1]) / 30
            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))  # Ép kiểu số nguyên để vẽ không bị nhòe

            # Tạo lá rơi ngẫu nhiên từ các vị trí cây đã lưu
            for rect in self.leaf_spawners:
                if random.random() * 49999 < rect.width * rect.height:
                    pos = (rect.x + random.random() * rect.width, rect.y + random.random() * rect.height)
                    self.particles.append(
                        Particle(self, 'leaf', pos, velocity=[-0.1, 0.3], frame=random.randint(0, 20)))

            self.clouds.update()
            self.clouds.render(self.display_2, offset=render_scroll)
            self.tilemap.render(self.display, offset=render_scroll)

            # Cập nhật và vẽ kẻ thù
            for enemy in self.enemies.copy():
                kill = enemy.update(self.tilemap, (0, 0))
                enemy.render(self.display, offset=render_scroll)
                if kill: self.enemies.remove(enemy)

            # Nếu còn sống thì mới cập nhật người chơi
            if not self.dead:
                self.player.update(self.tilemap, (self.movement[1] - self.movement[0], 0))
                self.player.render(self.display, offset=render_scroll)

            # Xử lý logic Đạn (Projectiles)
            for projectile in self.projectiles.copy():
                projectile[0][0] += projectile[1]  # Di chuyển đạn
                projectile[2] += 1  # Tăng thời gian tồn tại
                img = self.assets['projectile']
                self.display.blit(img, (projectile[0][0] - img.get_width() / 2 - render_scroll[0],
                                        projectile[0][1] - img.get_height() / 2 - render_scroll[1]))

                # Đạn chạm tường
                if self.tilemap.solid_check(projectile[0]):
                    self.projectiles.remove(projectile)
                    for i in range(4):  # Tạo 4 tia lửa khi va chạm
                        self.sparks.append(
                            Spark(projectile[0], random.random() - 0.5 + (math.pi if projectile[1] > 0 else 0),
                                  2 + random.random()))

                # Đạn bay quá lâu (hết tầm)
                elif projectile[2] > 360:
                    self.projectiles.remove(projectile)

                # Đạn trúng người chơi (nếu người chơi không trong trạng thái Dash mạnh)
                elif abs(self.player.dashing) < 50:
                    if self.player.rect().collidepoint(projectile[0]):
                        self.projectiles.remove(projectile)
                        self.player.health -= 20
                        self.sfx['hit'].play()
                        self.screenshake = max(16, self.screenshake)  # Rung mạnh màn hình
                        for i in range(30):  # Hiệu ứng máu văng bằng Spark và Particle
                            angle = random.random() * math.pi * 2
                            speed = random.random() * 5
                            self.sparks.append(Spark(self.player.rect().center, angle, 2 + random.random()))
                            self.particles.append(Particle(self, 'particle', self.player.rect().center,
                                                           velocity=[math.cos(angle + math.pi) * speed * 0.5,
                                                                     math.sin(angle + math.pi) * speed * 0.5],
                                                           frame=random.randint(0, 7)))
                        if self.player.health <= 0:
                            self.dead += 1

            # Cập nhật và vẽ tia lửa
            for spark in self.sparks.copy():
                kill = spark.update()
                spark.render(self.display, offset=render_scroll)
                if kill: self.sparks.remove(spark)

            # Tạo hiệu ứng đổ bóng đen cho mọi vật thể (Silhouette)
            display_mask = pygame.mask.from_surface(self.display)
            display_sillhouette = display_mask.to_surface(setcolor=(0, 0, 0, 180), unsetcolor=(0, 0, 0, 0))
            for offset in [(-1, 0), (1, 0), (0, -1), (0, 1)]:  # Vẽ bóng lệch 4 hướng
                self.display_2.blit(display_sillhouette, offset)

            # Cập nhật và vẽ Hạt (lá cây, bụi)
            for particle in self.particles.copy():
                kill = particle.update()
                # Hiệu ứng lá bay đung đưa theo hình sin
                if particle.type == 'leaf':
                    particle.pos[0] += math.sin(particle.animation.frame * 0.035) * 0.3
                particle.render(self.display, offset=render_scroll)
                if kill: self.particles.remove(particle)
                self.draw_health_bar(self.display, (10, 10), self.player.health, self.player.max_health)
                self.draw_mana_bar(self.display, (10, 17), self.player.mana, self.player.max_mana)


            # Xử lý sự kiện bàn phím
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a: self.movement[0] = True
                    if event.key == pygame.K_d: self.movement[1] = True
                    if event.key == pygame.K_w:
                        if self.player.jump(): self.sfx['jump'].play()
                    if event.key == pygame.K_j: self.player.dash()
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_a: self.movement[0] = False
                    if event.key == pygame.K_d: self.movement[1] = False

            # Vẽ hiệu ứng vòng tròn chuyển màn
            if self.transition:
                transition_surf = pygame.Surface(self.display.get_size())
                pygame.draw.circle(transition_surf, (255, 255, 255),
                                   (self.display.get_width() // 2, self.display.get_height() // 2),
                                   (30 - abs(self.transition)) * 8)
                transition_surf.set_colorkey((255, 255, 255))  # Làm trong suốt màu trắng để tạo lỗ hổng
                self.display.blit(transition_surf, (0, 0))

            # Lồng display vào display_2
            self.display_2.blit(self.display, (0, 0))

            # Tính toán rung màn hình và vẽ lên cửa sổ thực tế
            screenshake_offset = (random.random() * self.screenshake - self.screenshake / 2,
                                  random.random() * self.screenshake - self.screenshake / 2)
            self.screen.blit(pygame.transform.scale(self.display_2, self.screen.get_size()), screenshake_offset)
            pygame.display.update()
            self.clock.tick(60)  # Giới hạn 60 FPS
Game().run()