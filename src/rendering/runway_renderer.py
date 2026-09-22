import pygame


class RunwayRenderer:
    ASPHALT = (48, 50, 52)
    MARKING = (225, 225, 220)
    EDGE = (90, 92, 94)

    def draw(self, screen, camera, runway):
        """Render a runway using its aviation heading."""

        length = max(1, int(runway.length * camera.zoom))
        width = max(1, int(runway.width * camera.zoom))

        runway_surface = pygame.Surface(
            (length, width),
            pygame.SRCALPHA,
        )

        runway_surface.fill(self.ASPHALT)

        self._draw_edges(runway_surface, camera)
        self._draw_centerline(runway_surface, camera)
        self._draw_thresholds(runway_surface, camera)
        self._draw_aiming_points(runway_surface, camera)
        self._draw_designations(runway_surface, camera)

        # Our base surface points east-west.
        # Aviation heading 090 therefore requires zero rotation.
        rotation = 90 - runway.heading

        rotated_surface = pygame.transform.rotate(
            runway_surface,
            rotation,
        )

        center = camera.world_to_screen(runway.center)

        rect = rotated_surface.get_rect(
            center=(int(center.x), int(center.y))
        )

        screen.blit(rotated_surface, rect)

    def _draw_edges(self, surface, camera):
        edge_width = max(1, int(3 * camera.zoom))

        pygame.draw.rect(
            surface,
            self.EDGE,
            surface.get_rect(),
            edge_width,
        )

    def _draw_centerline(self, surface, camera):
        center_y = surface.get_height() // 2

        dash_length = max(1, int(100 * camera.zoom))
        gap_length = max(1, int(80 * camera.zoom))
        margin = max(1, int(200 * camera.zoom))
        line_width = max(1, int(6 * camera.zoom))

        x = margin

        while x < surface.get_width() - margin:
            end_x = min(
                x + dash_length,
                surface.get_width() - margin,
            )

            pygame.draw.line(
                surface,
                self.MARKING,
                (x, center_y),
                (end_x, center_y),
                line_width,
            )

            x += dash_length + gap_length

    def _draw_thresholds(self, surface, camera):
        threshold_offset = int(120 * camera.zoom)
        stripe_length = max(1, int(90 * camera.zoom))
        stripe_width = max(1, int(12 * camera.zoom))
        stripe_gap = max(1, int(10 * camera.zoom))
        stripe_count = 8

        center_y = surface.get_height() // 2

        total_width = (
            stripe_count * stripe_width
            + (stripe_count - 1) * stripe_gap
        )

        start_y = center_y - total_width // 2

        for side in ("left", "right"):
            if side == "left":
                start_x = threshold_offset
            else:
                start_x = (
                    surface.get_width()
                    - threshold_offset
                    - stripe_length
                )

            for i in range(stripe_count):
                y = start_y + i * (stripe_width + stripe_gap)

                pygame.draw.rect(
                    surface,
                    self.MARKING,
                    pygame.Rect(
                        start_x,
                        y,
                        stripe_length,
                        stripe_width,
                    ),
                )

    def _draw_aiming_points(self, surface, camera):
        distance = int(900 * camera.zoom)
        block_length = max(1, int(180 * camera.zoom))
        block_width = max(1, int(22 * camera.zoom))
        block_offset = max(1, int(45 * camera.zoom))

        center_y = surface.get_height() // 2

        positions = (
            distance,
            surface.get_width() - distance,
        )

        for center_x in positions:
            for y_offset in (-block_offset, block_offset):
                pygame.draw.rect(
                    surface,
                    self.MARKING,
                    pygame.Rect(
                        center_x - block_length // 2,
                        center_y + y_offset - block_width // 2,
                        block_length,
                        block_width,
                    ),
                )

    def _draw_designations(self, surface, camera):
        font_size = max(10, int(70 * camera.zoom))
        font = pygame.font.Font(None, font_size)

        left_text = font.render(
            "09",
            True,
            self.MARKING,
        )

        right_text = font.render(
            "27",
            True,
            self.MARKING,
        )

        center_y = surface.get_height() // 2
        offset = int(430 * camera.zoom)

        left_rect = left_text.get_rect(
            center=(offset, center_y)
        )

        right_rect = right_text.get_rect(
            center=(
                surface.get_width() - offset,
                center_y,
            )
        )

        surface.blit(left_text, left_rect)
        surface.blit(right_text, right_rect)
