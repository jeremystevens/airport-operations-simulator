import pygame

from src.rendering.camera import Camera
from src.simulation.clock import SimulationClock


WIDTH = 1280
HEIGHT = 720
FPS = 60


def draw_test_world(screen, camera):
    """Temporary world objects used to test camera movement."""

    # World origin
    origin = camera.world_to_screen((0, 0))

    pygame.draw.circle(
        screen,
        (255, 80, 80),
        (int(origin.x), int(origin.y)),
        12,
    )

    # Temporary world grid
    grid_spacing = 200
    grid_extent = 2000

    for x in range(-grid_extent, grid_extent + 1, grid_spacing):
        start = camera.world_to_screen((x, -grid_extent))
        end = camera.world_to_screen((x, grid_extent))

        pygame.draw.line(
            screen,
            (45, 50, 55),
            start,
            end,
            1,
        )

    for y in range(-grid_extent, grid_extent + 1, grid_spacing):
        start = camera.world_to_screen((-grid_extent, y))
        end = camera.world_to_screen((grid_extent, y))

        pygame.draw.line(
            screen,
            (45, 50, 55),
            start,
            end,
            1,
        )


def main():
    pygame.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Airport Operations Simulator")

    clock = pygame.time.Clock()

    camera = Camera(WIDTH, HEIGHT)

    simulation_clock = SimulationClock(6, 0)

    font = pygame.font.Font(None, 28)

    running = True

    while running:
        dt = clock.tick(FPS) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            camera.handle_event(event)

        camera.update(dt)

        simulation_clock.update(dt)

        screen.fill((20, 24, 28))

        draw_test_world(screen, camera)

        time_text = font.render(
            f"DAY {simulation_clock.day}  |  {simulation_clock.get_time_string()}",
            True,
            (220, 225, 230),
        )

        screen.blit(time_text, (20, 20))

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
