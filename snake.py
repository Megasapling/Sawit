import pygame
import random
import sys

# Inisialisasi Pygame
pygame.init()

# Konstanta
WIDTH = 600
HEIGHT = 600
GRID_SIZE = 40          # Jumlah sel per baris/kolom
CELL_SIZE = WIDTH // GRID_SIZE  # Ukuran setiap sel (30px)

# Warna
BLACK = (5, 5, 5)
WHITE = (255, 255, 255)
GREEN = (10, 255, 10)
RED = (255, 0, 0)
DARK_GREEN = (0, 150, 0)
GRAY = (100, 110, 110)

# Pengaturan game
BASE_SPEED = 15          # Kecepatan awal (FPS)
SPEED_INCREMENT = 2     # Penambahan kecepatan setiap interval poin
SPEED_INTERVAL = 4      # Setiap berapa poin kecepatan naik

# Setup layar
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 24)

# ==================== FUNGSI ====================
def draw_grid():
    """Gambar grid untuk referensi visual (opsional)"""
    for x in range(0, WIDTH, CELL_SIZE):
        pygame.draw.line(screen, GRAY, (x, 0), (x, HEIGHT), 1)
    for y in range(0, HEIGHT, CELL_SIZE):
        pygame.draw.line(screen, GRAY, (0, y), (WIDTH, y), 1)

def draw_snake(snake_segments):
    """Gambar ular dengan warna gradasi sederhana"""
    for i, segment in enumerate(snake_segments):
        x, y = segment
        rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        # Warna lebih terang untuk kepala
        if i == len(snake_segments) - 1:
            pygame.draw.rect(screen, GREEN, rect)
            pygame.draw.rect(screen, DARK_GREEN, rect, 2)  # outline
        else:
            pygame.draw.rect(screen, DARK_GREEN, rect)
            pygame.draw.rect(screen, GREEN, rect, 1)

def draw_food(food_pos):
    """Gambar makanan (apel)"""
    x, y = food_pos
    rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
    pygame.draw.rect(screen, RED, rect)
    pygame.draw.circle(screen, (200, 0, 0), (x * CELL_SIZE + CELL_SIZE//2, y * CELL_SIZE + CELL_SIZE//2), CELL_SIZE//2 - 2)

def generate_food(snake_segments):
    """Hasilkan posisi makanan baru yang tidak bertumpuk dengan ular"""
    while True:
        x = random.randint(0, GRID_SIZE - 1)
        y = random.randint(0, GRID_SIZE - 1)
        if (x, y) not in snake_segments:
            return (x, y)

def check_collision(snake_segments):
    """Cek apakah kepala ular menabrak dinding atau tubuhnya sendiri"""
    head_x, head_y = snake_segments[-1]
    # Tabrak dinding
    if head_x < 0 or head_x >= GRID_SIZE or head_y < 0 or head_y >= GRID_SIZE:
        return True
    # Tabrak tubuh sendiri (kepala tidak dihitung, jadi cek apakah posisi kepala ada di segment sebelumnya)
    if (head_x, head_y) in snake_segments[:-1]:
        return True
    return False

def display_score(score, speed):
    """Tampilkan skor dan kecepatan di pojok kiri atas"""
    score_text = font.render(f"Score: {score}  Speed: {speed}", True, WHITE)
    screen.blit(score_text, (10, 10))

def game_over_screen(score):
    """Tampilkan layar game over dan tunggu input R untuk restart atau ESC untuk keluar"""
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    screen.blit(overlay, (0, 0))
    
    game_over_font = pygame.font.SysFont("Arial", 48)
    text = game_over_font.render("SKILL ISU", True, RED)
    text_rect = text.get_rect(center=(WIDTH//2, HEIGHT//2 - 40))
    screen.blit(text, text_rect)
    
    score_text = font.render(f"Final Score: {score}", True, WHITE)
    score_rect = score_text.get_rect(center=(WIDTH//2, HEIGHT//2 + 10))
    screen.blit(score_text, score_rect)
    
    restart_text = font.render("Press R to Restart or ESC to Quit", True, WHITE)
    restart_rect = restart_text.get_rect(center=(WIDTH//2, HEIGHT//2 + 60))
    screen.blit(restart_text, restart_rect)
    
    pygame.display.update()
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    waiting = False
                    return True  # restart
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
    return False

# ==================== INISIALISASI GAME ====================
def init_game():
    """Reset semua variabel ke awal"""
    # Urutan dari ekor ke kepala, kepala di ujung kanan (agar gerak kanan aman)
    snake = [(GRID_SIZE//2 - 2, GRID_SIZE//2), (GRID_SIZE//2 - 1, GRID_SIZE//2), (GRID_SIZE//2, GRID_SIZE//2)]
    direction = (1, 0)  # ke kanan
    food = generate_food(snake)
    score = 0
    speed = BASE_SPEED
    return snake, direction, food, score, speed

# ==================== MAIN LOOP ====================
def main():
    snake, direction, food, score, speed = init_game()
    running = True

    while True:
        # Jika game over, tampilkan layar game over
        if not running:
            restart = game_over_screen(score)
            if restart:
                snake, direction, food, score, speed = init_game()
                running = True
            else:
                # Seharusnya sudah keluar di game_over_screen
                pass
            continue

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and direction != (0, 1):  # tidak boleh langsung berbalik arah
                    direction = (0, -1)
                elif event.key == pygame.K_DOWN and direction != (0, -1):
                    direction = (0, 1)
                elif event.key == pygame.K_LEFT and direction != (1, 0):
                    direction = (-1, 0)
                elif event.key == pygame.K_RIGHT and direction != (-1, 0):
                    direction = (1, 0)
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        # Gerakkan ular
        head_x, head_y = snake[-1]
        new_head = (head_x + direction[0], head_y + direction[1])
        snake.append(new_head)

        # Cek apakah makan makanan
        if new_head == food:
            score += 1
            food = generate_food(snake)
            # Ular bertambah panjang (kita sudah menambahkan kepala baru, jadi tidak perlu hapus ekor)

            # Update kecepatan setiap interval poin
            if score % SPEED_INTERVAL == 0:
                speed += SPEED_INCREMENT
        else:
            # Hapus ekor (ular bergerak maju)
            snake.pop(0)

        # Cek tabrakan
        if check_collision(snake):
            running = False

        # Gambar semua elemen
        screen.fill(BLACK)
        draw_grid()
        draw_snake(snake)
        draw_food(food)
        display_score(score, speed)

        pygame.display.update()
        clock.tick(speed)

if __name__ == "__main__":
    main()