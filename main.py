import sys
import pygame

from Scripts.entities import PhysicsEnity
# lấy class Physics_enity từ entities trong Scripts
from Scripts.utils import load_image, load_images
from Scripts.tilemap import Tilemap


class Game:
    def __init__(self):
        pygame.init()

        pygame.display.set_caption("Ninja game")
        # viết 1 caption cho cửa sổ của game
        self.screen = pygame.display.set_mode((640, 480))
        # tạo màn hình để chạy game
        self.display = pygame.Surface((320, 240))
        self.clock = pygame.time.Clock()
        # thiết lập 1 clock có khả năng giới hạn fps cho game
        self.movement = [False,False]
        # gắn việc di chuyển thành false

        self.assets = {
            'decor' : load_images('tiles/decor'),
            'grass' : load_images('tiles/grass'),
            'large_decor' : load_images('tiles/large_decor'),
            'stone' : load_images('tiles/stone'),
            'player' : load_image('entities/player.png')
        }
        # gán hình ảnh vào môi đối tượng

        self.player = PhysicsEnity(self,'player',(50, 50),(8, 15))
        #gắn player vs hàm chạy cơ bản
        self.tilemap = Tilemap(self,tile_size=16)

    def run(self):
        while True:
            self.display.fill((14,219,248))
            #tô màu cho màn hình trò chơi

            self.tilemap.render(self.display)

            self.player.update(self.tilemap,(self.movement[1] - self.movement[0], 0))
            self.player.render(self.display)

            print(self.tilemap.physics_rects_around(self.player.pos))


            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            # đây là câu lệnh dùng để di chuyển con trỏ chuột cũng như 1 câu lệnh có khả năng thoát màn hình trò chơi
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        self.movement[0] = True
                    if event.key == pygame.K_d:
                        self.movement[1] = True
                    if event.key == pygame.K_w:
                        self.player.velocity[1] = -3
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_a:
                        self.movement[0] = False
                    if event.key == pygame.K_d:
                        self.movement[1] = False

            # toàn bộ hàm này để đọc khi di chuyển key và gắn nó thành true and false
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0,0))
            pygame.display.update()
            self.clock.tick(60)
Game().run()


