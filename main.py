import pygame

from src.airport.airport import Airport
from src.airport.runway import Runway
from src.airport.taxiway import TaxiwayNode, TaxiwaySegment
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
        property_width=7000,
        property_height=4500,
    )

    runway_09_27 = Runway(
        name="09/27",
        center=(0, 0),
        length=5200,
        width=180,
        heading=90,
    )

    airport.add_runway(runway_09_27)

    alpha_west = TaxiwayNode("A_WEST", (-2500, 500))
    alpha_1 = TaxiwayNode("A1", (-2350, 500))
    alpha_2 = TaxiwayNode("A2", (-900, 500))
    alpha_3 = TaxiwayNode("A3", (900, 500))
    alpha_4 = TaxiwayNode("A4", (2350, 500))
    alpha_east = TaxiwayNode("A_EAST", (2500, 500))

    for node in (
        alpha_west,
        alpha_1,
        alpha_2,
        alpha_3,
        alpha_4,
        alpha_east,
    ):
        airport.add_taxiway_node(node)

    runway_a1 = TaxiwayNode("RWY_A1", (-2350, 90))
    runway_a2 = TaxiwayNode("RWY_A2", (-700, 90))
    runway_a3 = TaxiwayNode("RWY_A3", (700, 90))
    runway_a4 = TaxiwayNode("RWY_A4", (2350, 90))

    for node in (
        runway_a1,
        runway_a2,
        runway_a3,
        runway_a4,
    ):
        airport.add_taxiway_node(node)

    alpha_segments = [
        TaxiwaySegment(
            "A_01",
            alpha_west,
            alpha_1,
            "A",
        ),
        TaxiwaySegment(
            "A_02",
            alpha_1,
            alpha_2,
            "A",
        ),
        TaxiwaySegment(
            "A_03",
            alpha_2,
            alpha_3,
            "A",
        ),
        TaxiwaySegment(
            "A_04",
            alpha_3,
            alpha_4,
            "A",
        ),
        TaxiwaySegment(
            "A_05",
            alpha_4,
            alpha_east,
            "A",
        ),
    ]

    for segment in alpha_segments:
        airport.add_taxiway_segment(segment)

    runway_connectors = [
        TaxiwaySegment(
            "A1_RWY",
            alpha_1,
            runway_a1,
            "A1",
        ),
        TaxiwaySegment(
            "A2_RWY",
            alpha_2,
            runway_a2,
            "A2",
        ),
        TaxiwaySegment(
            "A3_RWY",
            alpha_3,
            runway_a3,
            "A3",
        ),
        TaxiwaySegment(
            "A4_RWY",
            alpha_4,
            runway_a4,
            "A4",
        ),
    ]

    for segment in runway_connectors:
        airport.add_taxiway_segment(segment)

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

        world_renderer.draw(screen, camera, airport)

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
