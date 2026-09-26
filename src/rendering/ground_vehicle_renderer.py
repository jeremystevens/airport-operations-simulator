import math

import pygame

from src.vehicles.ground_vehicle import (
    GroundVehicleType,
)


class GroundVehicleRenderer:
    TUG_BODY = (210, 175, 45)
    TUG_CAB = (235, 215, 125)
    TIRE = (30, 30, 30)

    TOWBAR = (190, 190, 175)
    TOWBAR_JOINT = (235, 190, 45)

    FUEL_TANK = (195, 45, 40)
    FUEL_CAB = (225, 130, 125)

    def draw(
        self,
        screen,
        camera,
        vehicle,
    ):
        if (
            vehicle.vehicle_type
            == GroundVehicleType.PUSHBACK_TUG
        ):
            self._draw_tug(
                screen,
                camera,
                vehicle,
            )

        elif (
            vehicle.vehicle_type
            == GroundVehicleType.FUEL_TRUCK
        ):
            self._draw_fuel_truck(
                screen,
                camera,
                vehicle,
            )

    def draw_towbar(
        self,
        screen,
        camera,
        vehicle,
        aircraft,
    ):
        vehicle_position = camera.world_to_screen(
            vehicle.position
        )

        aircraft_position = pygame.Vector2(
            aircraft.position
        )

        heading_radians = math.radians(
            aircraft.heading
        )

        forward = pygame.Vector2(
            math.sin(heading_radians),
            -math.cos(heading_radians),
        )

        # Approximate aircraft nose-gear position.
        nose_gear_position = (
            aircraft_position
            + forward * 115.0
        )

        nose_gear_screen = camera.world_to_screen(
            nose_gear_position
        )

        pygame.draw.line(
            screen,
            self.TOWBAR,
            vehicle_position,
            nose_gear_screen,
            max(
                1,
                int(6 * camera.zoom),
            ),
        )

        pygame.draw.circle(
            screen,
            self.TOWBAR_JOINT,
            (
                int(nose_gear_screen.x),
                int(nose_gear_screen.y),
            ),
            max(
                2,
                int(7 * camera.zoom),
            ),
        )

    def _draw_tug(
        self,
        screen,
        camera,
        vehicle,
    ):
        width = max(
            4,
            int(55 * camera.zoom),
        )

        length = max(
            6,
            int(85 * camera.zoom),
        )

        surface = pygame.Surface(
            (width + 12, length + 12),
            pygame.SRCALPHA,
        )

        rect = pygame.Rect(
            6,
            6,
            width,
            length,
        )

        pygame.draw.rect(
            surface,
            self.TUG_BODY,
            rect,
            border_radius=max(
                1,
                int(5 * camera.zoom),
            ),
        )

        cab_height = max(
            3,
            int(length * 0.28),
        )

        pygame.draw.rect(
            surface,
            self.TUG_CAB,
            pygame.Rect(
                8,
                8,
                max(2, width - 4),
                cab_height,
            ),
        )

        # Simple wheels.
        wheel_width = max(2, int(7 * camera.zoom))
        wheel_height = max(3, int(16 * camera.zoom))

        for x in (2, width + 6):
            pygame.draw.rect(
                surface,
                self.TIRE,
                pygame.Rect(
                    x,
                    int(length * 0.25),
                    wheel_width,
                    wheel_height,
                ),
            )

            pygame.draw.rect(
                surface,
                self.TIRE,
                pygame.Rect(
                    x,
                    int(length * 0.65),
                    wheel_width,
                    wheel_height,
                ),
            )

        rotated = pygame.transform.rotate(
            surface,
            -vehicle.heading,
        )

        position = camera.world_to_screen(
            vehicle.position
        )

        destination = rotated.get_rect(
            center=(
                int(position.x),
                int(position.y),
            )
        )

        screen.blit(
            rotated,
            destination,
        )

    def _draw_fuel_truck(
        self,
        screen,
        camera,
        vehicle,
    ):
        width = max(
            4,
            int(50 * camera.zoom),
        )

        length = max(
            8,
            int(110 * camera.zoom),
        )

        surface = pygame.Surface(
            (width + 12, length + 12),
            pygame.SRCALPHA,
        )

        cab_length = max(
            3,
            int(length * 0.22),
        )

        pygame.draw.rect(
            surface,
            self.FUEL_CAB,
            pygame.Rect(
                6,
                6,
                width,
                cab_length,
            ),
            border_radius=max(
                1,
                int(4 * camera.zoom),
            ),
        )

        pygame.draw.rect(
            surface,
            self.FUEL_TANK,
            pygame.Rect(
                6,
                6 + cab_length,
                width,
                length - cab_length,
            ),
            border_radius=max(
                1,
                int(6 * camera.zoom),
            ),
        )

        wheel_width = max(2, int(6 * camera.zoom))
        wheel_height = max(3, int(14 * camera.zoom))

        for x in (2, width + 6):
            pygame.draw.rect(
                surface,
                self.TIRE,
                pygame.Rect(
                    x,
                    int(length * 0.15),
                    wheel_width,
                    wheel_height,
                ),
            )

            pygame.draw.rect(
                surface,
                self.TIRE,
                pygame.Rect(
                    x,
                    int(length * 0.75),
                    wheel_width,
                    wheel_height,
                ),
            )

        rotated = pygame.transform.rotate(
            surface,
            -vehicle.heading,
        )

        position = camera.world_to_screen(
            vehicle.position
        )

        destination = rotated.get_rect(
            center=(
                int(position.x),
                int(position.y),
            )
        )

        screen.blit(
            rotated,
            destination,
        )
