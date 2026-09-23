import math

import pygame

from src.aircraft.aircraft import AircraftState


class PushbackController:
    def __init__(self, pushback_speed=35.0):
        self.pushback_speed = float(pushback_speed)

    def start(
        self,
        aircraft,
        gate,
        target_node,
        tug,
    ):
        if aircraft.state != AircraftState.AT_GATE:
            raise RuntimeError(
                f"{aircraft.flight_id} must be AT_GATE "
                f"before pushback"
            )

        if gate.aircraft_id != aircraft.flight_id:
            raise RuntimeError(
                f"Gate {gate.gate_id} does not contain "
                f"{aircraft.flight_id}"
            )

        aircraft.pushback_target = target_node.node_id
        aircraft.pushback_speed = self.pushback_speed
        aircraft.speed = self.pushback_speed
        aircraft.state = AircraftState.PUSHBACK

        tug.assign_aircraft(aircraft)
        tug.active = True

    def update(
        self,
        aircraft,
        airport,
        tug,
        dt,
    ):
        if aircraft.state != AircraftState.PUSHBACK:
            return False

        if aircraft.pushback_target is None:
            return False

        target_node = airport.taxiway_nodes[
            aircraft.pushback_target
        ]

        position = pygame.Vector2(
            aircraft.position
        )

        target = pygame.Vector2(
            target_node.position
        )

        offset = target - position
        distance = offset.length()

        movement = (
            aircraft.pushback_speed * dt
        )

        if distance < 1.0 or movement >= distance:
            aircraft.position = (
                target.x,
                target.y,
            )

            aircraft.speed = 0.0
            aircraft.pushback_speed = 0.0
            aircraft.pushback_target = None

            self._position_tug(
                aircraft,
                tug,
            )

            return True

        direction = offset.normalize()

        position += direction * movement

        aircraft.position = (
            position.x,
            position.y,
        )

        self._position_tug(
            aircraft,
            tug,
        )

        return False

    @staticmethod
    def _position_tug(aircraft, tug):
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

        tug_offset = 235.0

        tug.position = (
            aircraft_position
            + forward * tug_offset
        )

        tug.heading = aircraft.heading
        tug.speed = aircraft.speed
