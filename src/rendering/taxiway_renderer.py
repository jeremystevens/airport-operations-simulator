import pygame


class TaxiwayRenderer:
    PAVEMENT = (62, 64, 65)
    EDGE = (82, 84, 85)
    CENTERLINE = (215, 185, 55)

    def draw(self, screen, camera, airport):
        """Render all taxiway segments in the airport."""

        for segment in airport.taxiway_segments:
            self._draw_segment(
                screen,
                camera,
                segment,
            )

        self._draw_debug_nodes(
            screen,
            camera,
            airport,
        )

    def _draw_segment(self, screen, camera, segment):
        if not segment.render_surface:
            return

        start = camera.world_to_screen(
            segment.start_node.position
        )

        end = camera.world_to_screen(
            segment.end_node.position
        )

        pavement_width = max(
            1,
            int(segment.width * camera.zoom),
        )

        edge_width = max(
            pavement_width + 2,
            int((segment.width + 8) * camera.zoom),
        )

        # Slightly wider edge/base layer.
        pygame.draw.line(
            screen,
            self.EDGE,
            start,
            end,
            edge_width,
        )

        # Taxiway pavement.
        pygame.draw.line(
            screen,
            self.PAVEMENT,
            start,
            end,
            pavement_width,
        )

        # Yellow centerline.
        centerline_width = max(
            1,
            int(4 * camera.zoom),
        )

        pygame.draw.line(
            screen,
            self.CENTERLINE,
            start,
            end,
            centerline_width,
        )

    def _draw_debug_nodes(self, screen, camera, airport):
        """Temporary markers showing navigation graph nodes."""

        for node in airport.taxiway_nodes.values():
            position = camera.world_to_screen(
                node.position
            )

            radius = max(
                2,
                int(8 * camera.zoom),
            )

            pygame.draw.circle(
                screen,
                (255, 160, 60),
                (int(position.x), int(position.y)),
                radius,
            )
