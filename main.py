import sys
import pygame

# Nhập các class từ các file script riêng lẻ
from Scripts.entities import PhysicsEnity  # Kiểm tra lại chính tả Entity/Enity
from Scripts.utils import load_image, load_images
from Scripts.tilemap import Tilemap
from Scripts.cloud import Clouds


class Game:
    def __init__(self):
        pygame.init()

        pygame.display.set_caption("Ninja Game")
        self.screen = pygame.display.set_mode((640, 480))

        # Tạo một Surface nhỏ (320x240) rồi phóng to lên (640x480) để tạo hiệu ứng Pixel Art
        self.display = pygame.Surface((320, 240))

        self.clock = pygame.time.Clock()

        # Trạng thái di chuyển: [Trái, Phải]
        self.movement = [False, False]

        # Tải tài nguyên game (Hình ảnh)
        self.assets = {
            'decor': load_images('tiles/decor'),
            'grass': load_images('tiles/grass'),
            'large_decor': load_images('tiles/large_decor'),
            'stone': load_images('tiles/stone'),
            'player': load_image('entities/player.png'),
            'back_ground': load_image('background.png'),
            'clouds': load_images('clouds'),
        }

        # Khởi tạo các đối tượng
        self.clouds = Clouds(self.assets['clouds'], count=16)
        self.player = PhysicsEnity(self, 'player', (50, 50), (8, 15))
        self.tilemap = Tilemap(self, tile_size=16)

        # Biến điều khiển Camera
        self.scroll = [0, 0]

    def run(self):
        while True:
            # 1. Làm sạch màn hình bằng hình nền
            self.display.blit(self.assets['back_ground'], (0, 0))

            # 2. Xử lý Camera Scroll (Lấy vị trí nhân vật làm trung tâm)
            # Công thức: (Vị trí mục tiêu - vị trí hiện tại của camera - nửa màn hình) / độ trễ
            self.scroll[0] += (self.player.rect().centerx - self.display.get_width() / 2 - self.scroll[0]) / 30
            self.scroll[1] += (self.player.rect().centery - self.display.get_height() / 2 - self.scroll[1]) / 30

            # Chuyển scroll về số nguyên để tránh lỗi rung hình khi vẽ
            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))

            # 3. Cập nhật và vẽ Mây
            self.clouds.update()
            self.clouds.render(self.display, offset=render_scroll)

            # 4. Vẽ bản đồ (Tilemap)
            self.tilemap.render(self.display, offset=render_scroll)

            # 5. Cập nhật và vẽ Nhân vật
            # di chuyển ngang = (Phải - Trái) -> Kết quả: 1, -1 hoặc 0
            self.player.update(self.tilemap, (self.movement[1] - self.movement[0], 0))
            self.player.render(self.display, offset=render_scroll)

            # 6. Xử lý sự kiện từ bàn phím/chuột
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:  # Sang trái
                        self.movement[0] = True
                    if event.key == pygame.K_d:  # Sang phải
                        self.movement[1] = True
                    if event.key == pygame.K_w:  # Nhảy
                        self.player.velocity[1] = -3

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_a:
                        self.movement[0] = False
                    if event.key == pygame.K_d:
                        self.movement[1] = False

            # 7. Phóng to màn hình display lên screen để hiển thị
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            pygame.display.update()
            self.clock.tick(60)  # Giới hạn 60 khung hình/giây


if __name__ == "__main__":
    Game().run()