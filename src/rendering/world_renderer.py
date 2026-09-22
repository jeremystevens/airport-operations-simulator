import pygame


class WorldRenderer:
    def __init__(self):
        self.grid_spacing = 200
        self.grid_extent = 2000

    def draw(self, screen, camera):
        """Render the simulation world."""

        self._draw_debug_grid(screen, camera)
        self._draw_world_origin(screen, camera)

    def _draw_debug_grid(self, screen, camera):
        for x in range(
            -self.grid_extent,
            self.grid_extent + 1,
            self.grid_spacing,
        ):
            start = camera.world_to_screen((x, -self.grid_extent))
            end = camera.world_to_screen((x, self.grid_extent))

            pygame.draw.line(
                screen,
                (45, 50, 55),
                start,
                end,
                1,
            )

        for y in range(
            -self.grid_extent,
            self.grid_extent + 1,
            self.grid_spacing,
        ):
            start = camera.world_to_screen((-self.grid_extent, y))
            end = camera.world_to_screen((self.grid_extent, y))

            pygame.draw.line(
                screen,
                (45, 50, 55),
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
