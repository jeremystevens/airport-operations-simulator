import math
import pygame

from src.aircraft.aircraft import AircraftState


class TakeoffController:
    def __init__(
        self,
        acceleration=5000.0,
        max_ground_speed=7000.0,
        rotation_speed=3500.0,
    ):
        self.acceleration = acceleration
        self.max_ground_speed = max_ground_speed
        self.rotation_speed = rotation_speed

    def update(
        self,
        aircraft,
        dt,
    ):
        if aircraft.state != AircraftState.TAKEOFF:
            return False

        aircraft.speed = min(
            aircraft.speed
            + self.acceleration * dt,
            self.max_ground_speed,
        )

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

        if aircraft.speed >= self.rotation_speed:
            aircraft.altitude = 1.0
            aircraft.set_state(
                AircraftState.AIRBORNE
            )
            return True

        return False
