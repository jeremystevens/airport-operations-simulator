import pygame


class ServiceRoadRenderer:
    ROAD = (88, 90, 88)
    EDGE = (180, 180, 165)
    CENTER = (205, 205, 190)

    def draw(self, screen, camera, airport):
        for segment in airport.service_segments:
            start = camera.world_to_screen(
                segment.start_node.position
            )

            end = camera.world_to_screen(
                segment.end_node.position
            )

            road_width = max(
                2,
                int(34 * camera.zoom),
            )

            pygame.draw.line(
                screen,
                self.ROAD,
                start,
                end,
                road_width,
            )

            pygame.draw.line(
                screen,
                self.EDGE,
                start,
                end,
                max(1, int(2 * camera.zoom)),
            )
