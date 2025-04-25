import pygame
import random
import numpy as np

SIZE = 513  # Размер карты (должен быть 2^n + 1)
MAX_HEIGHT = 255
MIN_HEIGHT = 0
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

def diamond_square(size, roughness):
    map = np.zeros((size, size), dtype=float)

    map[0, 0] = random.uniform(MIN_HEIGHT, MAX_HEIGHT)
    map[0, size-1] = random.uniform(MIN_HEIGHT, MAX_HEIGHT)
    map[size-1, 0] = random.uniform(MIN_HEIGHT, MAX_HEIGHT)
    map[size-1, size-1] = random.uniform(MIN_HEIGHT, MAX_HEIGHT)
    
    step_size = size - 1
    
    while step_size > 1:
        half_step = step_size // 2
        
        # Square шаг
        for x in range(0, size-1, step_size):
            for y in range(0, size-1, step_size):
                avg = (map[x, y] + map[x + step_size, y] + map[x, y + step_size] + map[x + step_size, y + step_size]) / 4.0
                offset = random.uniform(-roughness, roughness)
                map[x + half_step, y + half_step] = avg + offset

        # Diamond шаг
        for x in range(0, size, half_step):
            for y in range((x + half_step) % step_size, size, step_size):
                avg = (
                    map[(x - half_step + size) % size, y] +
                    map[(x + half_step) % size, y] +
                    map[x, (y - half_step + size) % size] +
                    map[x, (y + half_step) % size]
                ) / 4.0
                offset = random.uniform(-roughness, roughness)
                map[x, y] = avg + offset
                
                # Обработка краевых случаев
                if x == 0:
                    map[size - 1, y] = map[x, y]
                if y == 0:
                    map[x, size - 1] = map[x, y]
        
        step_size //= 2
        roughness /= 2.0

    return map

def normalize_map(map):
    min_val = map.min()
    max_val = map.max()
    norm_map = (map - min_val) / (max_val - min_val) * 255
    return norm_map.astype(np.uint8)

def generate_color_map(norm_map):
    color_map = np.zeros((norm_map.shape[0], norm_map.shape[1], 3), dtype=np.uint8)
    
    for x in range(norm_map.shape[0]):
        for y in range(norm_map.shape[1]):
            height = norm_map[x, y]
            if height == 0:
                color_map[x, y] = (0, 0, 0)  # Черный для уровня воды
            else:
                if height < 128:
                    blue_value = int(height * 2)  # Чем ближе к уровню суши, тем ярче синий
                    color_map[x, y] = (0, 0, blue_value)
                else:
                    green_value = int((height - 128) * 2)  # Чем выше, тем светлее зеленый
                    green_value = min(255, green_value + 50)
                    color_map[x, y] = (0, green_value, 0)  # Зеленый для суши
    
    return color_map


def draw_height_indicator(screen, norm_map, position):
    font = pygame.font.SysFont(None, 24)
    
    for i in range(0, 256, 16):
        if i == 0:
            color = (0, 0, 0)
        else:
            if i < 128:
                blue_value = int(i * 2)
                color = (0, 0, blue_value)
            else:
                green_value = int((i - 128) * 2)
                green_value = min(255, green_value + 50)
                color = (0, green_value, 0)
        
        pygame.draw.rect(screen, color, (*position, 20, 16))
        text = font.render(str(i), True, (255, 255, 255))
        screen.blit(text, (position[0] + 25, position[1]))
        position = (position[0], position[1] + 16)


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Diamond-Square Algorithm')
    roughness = 256.0
    terrain = diamond_square(SIZE, roughness)
    norm_terrain = normalize_map(terrain)
    color_terrain = generate_color_map(norm_terrain)

    # Создание поверхности для отображения
    terrain_surface = pygame.surfarray.make_surface(color_terrain)
    terrain_rect = terrain_surface.get_rect()

    offset_x, offset_y = 0, 0
    scale = 1

    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_PLUS or event.key == pygame.K_EQUALS:
                    scale = min(4, scale + 0.1)
                elif event.key == pygame.K_MINUS:
                    scale = max(0.1, scale - 0.1)
                elif event.key == pygame.K_UP:
                    offset_y += 50
                elif event.key == pygame.K_DOWN:
                    offset_y -= 50
                elif event.key == pygame.K_LEFT:
                    offset_x += 50
                elif event.key == pygame.K_RIGHT:
                    offset_x -= 50

        screen.fill((0, 0, 0))
        scaled_surface = pygame.transform.scale(terrain_surface, 
            (int(terrain_rect.width * scale), int(terrain_rect.height * scale)))
        screen.blit(scaled_surface, (offset_x, offset_y))

        draw_height_indicator(screen, norm_terrain, (SCREEN_WIDTH - 150, 10))

        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()

if __name__ == "__main__":
    main()