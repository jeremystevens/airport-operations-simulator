import math

import pygame

from src.aircraft.aircraft import AircraftState


class LandingController:
    def __init__(
        self,
        descent_rate=1200.0,
        touchdown_x=-1800.0,
        braking=2200.0,
        exit_speed=300.0,
        runway_exit_x=700.0,
    ):
        self.descent_rate = descent_rate
        self.touchdown_x = touchdown_x
        self.braking = braking
        self.exit_speed = exit_speed
        self.runway_exit_x = runway_exit_x

    def update(
        self,
        aircraft,
        dt,
    ):
        if aircraft.state == AircraftState.LANDING:
            return self._update_landing(
                aircraft,
                dt,
            )

        if aircraft.state == AircraftState.LANDING_ROLL:
            return self._update_rollout(
                aircraft,
                dt,
            )

        return None

    def _forward_vector(self, aircraft):
        heading_radians = math.radians(
            aircraft.heading
        )

        return pygame.Vector2(
            math.sin(heading_radians),
            -math.cos(heading_radians),
        )

    def _update_landing(
        self,
        aircraft,
        dt,
    ):
        forward = self._forward_vector(
            aircraft
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

        reached_touchdown_zone = (
            position.x >= self.touchdown_x
        )

        if (
            reached_touchdown_zone
            and aircraft.altitude <= 0.0
        ):
            aircraft.altitude = 0.0
            aircraft.set_state(
                AircraftState.LANDING_ROLL
            )

            return "touchdown"

        return None

    def _update_rollout(
        self,
        aircraft,
        dt,
    ):
        aircraft.speed = max(
            0.0,
            aircraft.speed
            - self.braking * dt,
        )

        event = None

        if (
            aircraft.speed <= self.exit_speed
            and not aircraft.runway_exit_ready
        ):
            aircraft.speed = self.exit_speed
            aircraft.runway_exit_ready = True
            event = "exit_speed_reached"

        if aircraft.runway_exit_ready:
            aircraft.speed = self.exit_speed

        forward = self._forward_vector(
            aircraft
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

        if (
            aircraft.runway_exit_ready
            and position.x >= self.runway_exit_x
        ):
            aircraft.position = (
                self.runway_exit_x,
                position.y,
            )

            return "runway_exit"

        return event
