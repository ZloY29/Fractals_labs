import random
import pygame
from math import floor
from collections import deque
from pygame import gfxdraw


def GetGoodRandom(heights: list[int], left: int, right: int, roughness: int):
    center = (left + right + 1) // 2
    idx = 0
    while heights[center] <= 0 or heights[center] >= 600:
        idx += 1
        heights[center] = (heights[left] + heights[right]) // 2 + \
                          roughness * (right - left + 1) * random.randint(-1, 1)
        if idx == 100:
            if heights[center] == 0:
                heights[center] = 1
            else:
                heights[center] = 599

def renderHeights(screen, heights, zoom, vertical_shift):
    for i, height in enumerate(heights):
        x = int(i * zoom)
        y = int((height - vertical_shift) * zoom)
        if 0 <= y < 600:
            gfxdraw.pixel(screen, x, y, (255, 255, 255))

def MidPointCounter(imageWidth, heights, roughness):
    q = deque()
    q.append((imageWidth - 601, imageWidth - 1, roughness))
    while len(q) != 0:
        left, right, randomness = q.popleft()
        center = (left + right + 1) // 2
        GetGoodRandom(heights, left, right, roughness)
        if right - left > 2:
            q.append((left, center, floor(randomness // 2)))
            q.append((center, right, floor(randomness // 2)))

def reset_heights(heights):
    _start = heights[0]
    _end = heights[599]
    heights.clear()
    heights.extend([0] * 600)
    heights[0] = _start
    heights[599] = _end

def main():
    roughness = 0.2
    flag = False
    iterator = 0
    is_iterator_moving_right = False
    is_iterator_moving_left = False
    is_moving_up = False
    is_moving_down = False
    
    is_zoom_in = False
    is_zoom_out = False
    
    zoom = 1.0
    vertical_shift = 0
    
    imageWidth = 600
    heights = [0] * imageWidth
    heights[0] = random.randint(0, 256)
    heights[imageWidth - 1] = heights[0]
    pygame.init()
    screen = pygame.display.set_mode((600, 600))
    screen.fill((0, 0, 0))
    MidPointCounter(imageWidth, heights, roughness)
    renderHeights(screen, heights[imageWidth - 600:imageWidth - 1], zoom, vertical_shift)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    is_iterator_moving_right = True
                if event.key == pygame.K_LEFT:
                    is_iterator_moving_left = True
                if event.key == pygame.K_w:
                    if roughness < 1:
                        reset_heights(heights)
                        imageWidth = 600
                        iterator = 0
                        flag = False
                        roughness += 0.05
                        print(roughness)
                        MidPointCounter(imageWidth, heights, roughness)
                if event.key == pygame.K_s:
                    if roughness > 0:
                        reset_heights(heights)
                        imageWidth = 600
                        iterator = 0
                        flag = False
                        roughness -= 0.05
                        print(roughness)
                        MidPointCounter(imageWidth, heights, roughness)
                if event.key == pygame.K_EQUALS or event.key == pygame.K_PLUS:
                    is_zoom_in = True
                if event.key == pygame.K_MINUS:
                    is_zoom_out = True
                if event.key == pygame.K_UP:
                    is_moving_up = True
                if event.key == pygame.K_DOWN:
                    is_moving_down = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    is_iterator_moving_right = False
                if event.key == pygame.K_LEFT:
                    is_iterator_moving_left = False
                if event.key == pygame.K_EQUALS or event.key == pygame.K_PLUS:
                    is_zoom_in = False
                if event.key == pygame.K_MINUS:
                    is_zoom_out = False
                if event.key == pygame.K_UP:
                    is_moving_up = False
                if event.key == pygame.K_DOWN:
                    is_moving_down = False
        
        if is_zoom_in:
            zoom += 0.005
            print('Zooming In:', zoom)
        
        if is_zoom_out:
            zoom -= 0.005
            if zoom < 0.1:
                zoom = 0.1
            print('Zooming Out:', zoom)
                
        if is_iterator_moving_right:
            iterator += 1
            flag = False
        if is_iterator_moving_left:
            if iterator > 0:
                iterator -= 1

        if is_moving_up:
            vertical_shift -= 1
        if is_moving_down:
            vertical_shift += 1

        if iterator % 600 == 0 and not flag:
            imageWidth += 600
            heights.extend([0] * 600)
            heights[imageWidth - 1] = heights[0] + (roughness * 600 * random.randint(-1, 1)) % 600
            MidPointCounter(imageWidth, heights, roughness)
            flag = True

        screen.fill((0, 0, 0))
        renderHeights(screen, heights[0 + iterator:imageWidth - 1 + iterator], zoom, vertical_shift)
        pygame.display.update()

if __name__ == "__main__":
    main()