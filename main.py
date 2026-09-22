import pygame

from src.airport.airport import Airport
from src.rendering.camera import Camera
from src.rendering.world_renderer import WorldRenderer
from src.simulation.clock import SimulationClock


WIDTH = 1280
HEIGHT = 720
FPS = 60


def main():
    pygame.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Airport Operations Simulator")

    clock = pygame.time.Clock()

    camera = Camera(WIDTH, HEIGHT)
    world_renderer = WorldRenderer()

    simulation_clock = SimulationClock(6, 0)

    airport = Airport(
        name="Redwood International Airport",
        code="RWI",
        world_width=12000,
        world_height=8000,
    )

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

        world_renderer.draw(screen, camera)

        airport_text = font.render(
            f"{airport.code} - {airport.name.upper()}",
            True,
            (220, 225, 230),
        )

        time_text = font.render(
            f"DAY {simulation_clock.day}  |  {simulation_clock.get_time_string()}",
            True,
            (180, 190, 200),
        )

        screen.blit(airport_text, (20, 20))
        screen.blit(time_text, (20, 50))

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
