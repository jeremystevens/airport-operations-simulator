import pygame

from src.aircraft.aircraft import AircraftSize


class AircraftRenderer:
    BODY = (225, 228, 230)
    BODY_EDGE = (125, 130, 135)
    COCKPIT = (55, 70, 80)

    NAV_RED = (220, 55, 55)
    NAV_GREEN = (55, 210, 90)

    AIRCRAFT_PROFILES = {
        AircraftSize.LIGHT: {
            "length": 150,
            "wingspan": 190,
            "fuselage_ratio": 0.10,
            "engine_scale": 0.0,
            "engine_count": 0,
        },

        AircraftSize.BUSINESS: {
            "length": 210,
            "wingspan": 190,
            "fuselage_ratio": 0.10,
            "engine_scale": 0.65,
            "engine_count": 2,
        },

        AircraftSize.REGIONAL: {
            "length": 250,
            "wingspan": 235,
            "fuselage_ratio": 0.11,
            "engine_scale": 0.75,
            "engine_count": 2,
        },

        AircraftSize.NARROWBODY: {
            "length": 300,
            "wingspan": 280,
            "fuselage_ratio": 0.12,
            "engine_scale": 1.0,
            "engine_count": 2,
        },

        AircraftSize.WIDEBODY: {
            "length": 390,
            "wingspan": 380,
            "fuselage_ratio": 0.17,
            "engine_scale": 1.35,
            "engine_count": 2,
        },

        AircraftSize.SUPERHEAVY: {
            "length": 430,
            "wingspan": 440,
            "fuselage_ratio": 0.19,
            "engine_scale": 1.45,
            "engine_count": 4,
        },
    }

    def draw(self, screen, camera, aircraft):
        profile = self.AIRCRAFT_PROFILES[
            aircraft.size
        ]

        length = profile["length"]
        wingspan = profile["wingspan"]

        # Draw at a useful resolution and rotate afterward.
        # Sized to the aircraft's own dimensions so nothing
        # gets clipped before rotation, with margin to spare.
        surface_size = int(max(length, wingspan) * 1.3)

        aircraft_surface = pygame.Surface(
            (surface_size, surface_size),
            pygame.SRCALPHA,
        )

        center = pygame.Vector2(
            surface_size / 2,
            surface_size / 2,
        )

        self._draw_silhouette(
            aircraft_surface,
            center,
            length,
            wingspan,
            profile,
        )

        # Base silhouette points north.
        # Aviation heading 0 = north, 90 = east.
        rotated = pygame.transform.rotate(
            aircraft_surface,
            -aircraft.heading,
        )

        # Camera zoom applies after aircraft rotation.
        display_width = max(
            1,
            int(rotated.get_width() * camera.zoom),
        )

        display_height = max(
            1,
            int(rotated.get_height() * camera.zoom),
        )

        rotated = pygame.transform.smoothscale(
            rotated,
            (display_width, display_height),
        )

        screen_position = camera.world_to_screen(
            aircraft.position
        )

        rect = rotated.get_rect(
            center=(
                int(screen_position.x),
                int(screen_position.y),
            )
        )

        screen.blit(rotated, rect)

    def _draw_silhouette(
        self,
        surface,
        center,
        length,
        wingspan,
        profile,
    ):
        cx = center.x
        cy = center.y

        nose_y = cy - length / 2
        tail_y = cy + length / 2

        # Main fuselage.
        fuselage_width = length * profile["fuselage_ratio"]

        body_rect = pygame.Rect(
            cx - fuselage_width / 2,
            nose_y + length * 0.08,
            fuselage_width,
            length * 0.82,
        )

        pygame.draw.rect(
            surface,
            self.BODY,
            body_rect,
            border_radius=max(
                2,
                int(fuselage_width / 2),
            ),
        )

        # Rounded / pointed nose.
        pygame.draw.polygon(
            surface,
            self.BODY,
            [
                (cx, nose_y),
                (
                    cx - fuselage_width / 2,
                    nose_y + length * 0.15,
                ),
                (
                    cx + fuselage_width / 2,
                    nose_y + length * 0.15,
                ),
            ],
        )

        # Main swept wings.
        wing_y = cy - length * 0.03

        pygame.draw.polygon(
            surface,
            self.BODY,
            [
                (cx, wing_y - length * 0.12),
                (
                    cx - wingspan / 2,
                    wing_y + length * 0.12,
                ),
                (
                    cx - wingspan * 0.08,
                    wing_y + length * 0.18,
                ),
                (cx, wing_y + length * 0.10),
                (
                    cx + wingspan * 0.08,
                    wing_y + length * 0.18,
                ),
                (
                    cx + wingspan / 2,
                    wing_y + length * 0.12,
                ),
            ],
        )

        # Horizontal stabilizers.
        stabilizer_y = tail_y - length * 0.16
        stabilizer_span = wingspan * 0.38

        pygame.draw.polygon(
            surface,
            self.BODY,
            [
                (
                    cx,
                    stabilizer_y - length * 0.06,
                ),
                (
                    cx - stabilizer_span / 2,
                    stabilizer_y + length * 0.05,
                ),
                (
                    cx,
                    stabilizer_y + length * 0.03,
                ),
                (
                    cx + stabilizer_span / 2,
                    stabilizer_y + length * 0.05,
                ),
            ],
        )

        # Engine nacelles.
        engine_count = profile["engine_count"]

        if engine_count > 0:
            engine_radius = max(
                3,
                int(
                    length
                    * 0.045
                    * profile["engine_scale"]
                ),
            )

            engine_y = wing_y + length * 0.08

            if engine_count == 2:
                engine_offsets = [
                    -wingspan * 0.23,
                    wingspan * 0.23,
                ]

            elif engine_count == 4:
                engine_offsets = [
                    -wingspan * 0.34,
                    -wingspan * 0.17,
                    wingspan * 0.17,
                    wingspan * 0.34,
                ]

            else:
                engine_offsets = []

            for offset in engine_offsets:
                engine_x = cx + offset

                pygame.draw.ellipse(
                    surface,
                    self.BODY_EDGE,
                    pygame.Rect(
                        engine_x - engine_radius,
                        engine_y - engine_radius * 1.4,
                        engine_radius * 2,
                        engine_radius * 2.8,
                    ),
                )

        # Cockpit windows.
        pygame.draw.ellipse(
            surface,
            self.COCKPIT,
            pygame.Rect(
                cx - fuselage_width * 0.32,
                nose_y + length * 0.09,
                fuselage_width * 0.64,
                length * 0.045,
            ),
        )

        # Navigation lights.
        light_radius = max(
            2,
            int(length * 0.018),
        )

        pygame.draw.circle(
            surface,
            self.NAV_RED,
            (
                int(cx - wingspan / 2),
                int(wing_y + length * 0.12),
            ),
            light_radius,
        )

        pygame.draw.circle(
            surface,
            self.NAV_GREEN,
            (
                int(cx + wingspan / 2),
                int(wing_y + length * 0.12),
            ),
            light_radius,
        )
