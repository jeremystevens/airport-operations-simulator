import math
import pygame

from src.aircraft.aircraft import AircraftState


class AirborneMovementController:
    def __init__(
        self,
        climb_rate=500.0,
        departure_altitude=3000.0,
    ):
        self.climb_rate = climb_rate
        self.departure_altitude = departure_altitude

    def update(
        self,
        aircraft,
        airport,
        dt,
    ):
        if aircraft.state != AircraftState.AIRBORNE:
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

        # Maintain liftoff speed for this first
        # airborne implementation.
        position += (
            forward
            * aircraft.speed
            * dt
        )

        aircraft.position = (
            position.x,
            position.y,
        )

        aircraft.altitude += (
            self.climb_rate * dt
        )

        half_width = (
            airport.world_width / 2.0
        )

        half_height = (
            airport.world_height / 2.0
        )

        outside_world = (
            abs(position.x) > half_width
            or abs(position.y) > half_height
        )

        high_enough = (
            aircraft.altitude
            >= self.departure_altitude
        )

        if outside_world and high_enough:
            aircraft.set_state(
                AircraftState.DEPARTED
            )

            aircraft.speed = 0.0

            return True

        return False
