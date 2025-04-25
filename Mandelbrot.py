import pygame
import sys


def pixel_to_complex(x, y, width, height, scale, offset_x, offset_y):
    return complex(
        (x - width / 2) / scale - offset_x,
        (y - height / 2) / scale - offset_y
    )


def compute_color(z0, R, N, c):
    z = z0
    for n in range(N):
        if abs(z) > R:
            return (255, 255, 255)
        z = z ** 4 + c
    return (0, 0, 0)


def handle_events(offset_x, offset_y, scale):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            elif event.key == pygame.K_UP:
                offset_y += 0.0001 * scale
            elif event.key == pygame.K_DOWN:
                offset_y -= 0.0001 * scale
            elif event.key == pygame.K_LEFT:
                offset_x += 0.0001 * scale
            elif event.key == pygame.K_RIGHT:
                offset_x -= 0.0001 * scale
            elif event.key == pygame.K_MINUS:
                scale /= 1.3
            elif event.key == pygame.K_EQUALS:
                scale *= 1.3
    return offset_x, offset_y, scale


def main():
    valid_a = False
    while not valid_a:
        try:
            a = float(input("Введите значение параметра a: "))
            if a > 0:
                valid_a = True
            else:
                print("Параметр a должен быть положительным числом.")
        except ValueError:
            print("Ошибка ввода. Введите число.")

    print("Введите комплексное число z0 (в формате a + bj): ")
    valid_z0 = False
    while not valid_z0:
        try:
            real_part = float(input("Введите действительную часть: "))
            imag_part = float(input("Введите мнимую часть: "))
            if -a <= real_part <= a and -a <= imag_part <= a:
                z0 = complex(real_part, imag_part)
                valid_z0 = True
            else:
                print("Значение z0 должно лежать в интервале [-a, a] по каждой из координат.")
        except ValueError:
            print("Ошибка ввода. Введите число.")

    valid_R = False
    while not valid_R:
        try:
            R = float(input("Введите радиус R: "))
            if R > 0:
                valid_R = True
            else:
                print("Радиус должен быть положительным числом.")
        except ValueError:
            print("Ошибка ввода. Введите число.")

    valid_N = False
    while not valid_N:
        try:
            N = int(input("Введите количество итераций N: "))
            if N > 0:
                valid_N = True
            else:
                print("Количество итераций должно быть положительным числом.")
        except ValueError:
            print("Ошибка ввода. Введите целое число.")

    pygame.init()
    width, height = 800, 600
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Mandelbrot Viewer")
    clock = pygame.time.Clock()

    scale = 200
    offset_x, offset_y = 0, 0

    while True:
        offset_x, offset_y, scale = handle_events(offset_x, offset_y, scale)

        screen.fill((0, 0, 0))

        for x in range(width):
            for y in range(height):
                c = pixel_to_complex(x, y, width, height, scale, offset_x, offset_y)
                color = compute_color(z0, R, N, c)
                screen.set_at((x, y), color)
        pygame.image.save(screen, "Mandelbrot_set.jpeg")
        pygame.display.flip()
        clock.tick(0)


if __name__ == "__main__":
    main()
