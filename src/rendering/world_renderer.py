import pygame

from src.rendering.runway_renderer import RunwayRenderer
from src.rendering.taxiway_renderer import TaxiwayRenderer


class WorldRenderer:
    def __init__(self):
        self.grid_spacing = 200
        self.grid_extent = 2000
        self.runway_renderer = RunwayRenderer()
        self.taxiway_renderer = TaxiwayRenderer()

    def draw(self, screen, camera, airport):
        """Render the simulation world."""

        self._draw_world_background(screen, camera, airport)
        self._draw_airport_property(screen, camera, airport)

        for runway in airport.runways:
            self.runway_renderer.draw(
                screen,
                camera,
                runway,
            )

        self.taxiway_renderer.draw(
            screen,
            camera,
            airport,
        )

        self._draw_debug_grid(screen, camera, airport)
        self._draw_world_origin(screen, camera)

    def _draw_world_background(self, screen, camera, airport):
        """Draw the physical bounds of the airport world."""

        half_width = airport.world_width / 2
        half_height = airport.world_height / 2

        top_left = camera.world_to_screen(
            (-half_width, -half_height)
        )

        bottom_right = camera.world_to_screen(
            (half_width, half_height)
        )

        width = bottom_right.x - top_left.x
        height = bottom_right.y - top_left.y

        world_rect = pygame.Rect(
            int(top_left.x),
            int(top_left.y),
            int(width),
            int(height),
        )

        pygame.draw.rect(
            screen,
            (50, 72, 48),
            world_rect,
        )

    def _draw_airport_property(self, screen, camera, airport):
        """Draw the airport property boundary."""

        half_width = airport.property_width / 2
        half_height = airport.property_height / 2

        top_left = camera.world_to_screen(
            (-half_width, -half_height)
        )

        bottom_right = camera.world_to_screen(
            (half_width, half_height)
        )

        property_rect = pygame.Rect(
            int(top_left.x),
            int(top_left.y),
            int(bottom_right.x - top_left.x),
            int(bottom_right.y - top_left.y),
        )

        pygame.draw.rect(
            screen,
            (60, 78, 58),
            property_rect,
        )

        pygame.draw.rect(
            screen,
            (115, 130, 105),
            property_rect,
            max(1, int(camera.zoom * 2)),
        )

    def _draw_debug_grid(self, screen, camera, airport):
        half_width = int(airport.world_width / 2)
        half_height = int(airport.world_height / 2)

        for x in range(
            -half_width,
            half_width + 1,
            self.grid_spacing,
        ):
            start = camera.world_to_screen((x, -half_height))
            end = camera.world_to_screen((x, half_height))

            pygame.draw.line(
                screen,
                (65, 85, 62),
                start,
                end,
                1,
            )

        for y in range(
            -half_height,
            half_height + 1,
            self.grid_spacing,
        ):
            start = camera.world_to_screen((-half_width, y))
            end = camera.world_to_screen((half_width, y))

            pygame.draw.line(
                screen,
                (65, 85, 62),
                start,
                end,
                1,
            )

    def _draw_world_origin(self, screen, camera):
        origin = camera.world_to_screen((0, 0))

        pygame.draw.circle(
            screen,
            (255, 80, 80),
            (int(origin.x), int(origin.y)),
            12,
        )
