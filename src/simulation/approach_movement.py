import math
import pygame

from src.aircraft.aircraft import AircraftState


class ApproachMovementController:
    def __init__(
        self,
        descent_rate=450.0,
        threshold_x=-2600.0,
    ):
        self.descent_rate = descent_rate
        self.threshold_x = threshold_x

    def update(
        self,
        aircraft,
        dt,
    ):
        if aircraft.state != AircraftState.APPROACH:
            return False

        heading_radians = math.radians(
            aircraft.heading
        )

        forward = pygame.Vector2(
            math.sin(heading_radians),
            -math.cos(heading_radians),
        )

        position = pygame.Vector2(
            aircraft.position
        )

        position += (
            forward
            * aircraft.speed
            * dt
        )

        aircraft.position = (
            position.x,
            position.y,
        )

        aircraft.altitude = max(
            0.0,
            aircraft.altitude
            - self.descent_rate * dt,
        )

        reached_threshold = (
            aircraft.position[0]
            >= self.threshold_x
        )

        return reached_threshold
