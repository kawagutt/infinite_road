import pygame
import math

pygame.init()
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Infinite Road")
clock = pygame.time.Clock()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

segments = []
segment_length = 50
road_width = 1200
segments_count = 80
time = 0


def create_segment(index):
    z = index * segment_length
    curve = math.sin(index * 0.05 + time) * 300
    return {"z": z, "curve": curve}


def project(x, z):
    scale = 600 / (z + 600)
    px = int(WIDTH / 2 + x * scale)
    py = int(HEIGHT / 2 + 200 * scale)  # Fixed height offset
    return px, py


def main():
    global time
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (
                event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
            ):
                running = False

        screen.fill(BLACK)
        segments.clear()

        for i in range(segments_count):
            segments.append(create_segment(i))

        for i in range(len(segments) - 1):
            seg = segments[i]
            next_seg = segments[i + 1]

            # Road segment coordinates
            x1_left = -road_width + seg["curve"]
            x1_right = road_width + seg["curve"]
            z1 = seg["z"]

            x2_left = -road_width + next_seg["curve"]
            x2_right = road_width + next_seg["curve"]
            z2 = next_seg["z"]

            # Draw road
            points = [
                project(x1_left, z1),
                project(x1_right, z1),
                project(x2_right, z2),
                project(x2_left, z2),
            ]
            pygame.draw.polygon(screen, (40, 40, 40), points)

            # Draw lines
            for offset in [-0.7, 0.7]:
                pygame.draw.line(
                    screen,
                    WHITE,
                    project(x1_left + road_width * (1 + offset), z1),
                    project(x2_left + road_width * (1 + offset), z2),
                    2,
                )

        time += 0.01
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
