import math

import pygame


class AircraftMovementController:
    def __init__(
        self,
        taxi_speed=90.0,
        turn_rate=120.0,
    ):
        self.taxi_speed = float(taxi_speed)
        self.turn_rate = float(turn_rate)

    def update(self, aircraft, airport, dt):
        if not aircraft.has_route:
            aircraft.speed = 0.0
            return

        node_id = aircraft.current_route_node
        target_node = airport.taxiway_nodes[node_id]

        position = pygame.Vector2(aircraft.position)
        target = pygame.Vector2(target_node.position)

        offset = target - position
        distance = offset.length()

        # Already at this waypoint.
        if distance < 1.0:
            aircraft.position = (
                target.x,
                target.y,
            )

            self._advance_route(aircraft)
            return

        direction = offset.normalize()

        target_heading = self._direction_to_heading(
            direction
        )

        aircraft.heading = self._turn_toward(
            aircraft.heading,
            target_heading,
            self.turn_rate * dt,
        )

        aircraft.speed = self.taxi_speed

        movement = self.taxi_speed * dt

        if movement >= distance:
            aircraft.position = (
                target.x,
                target.y,
            )

            self._advance_route(aircraft)
        else:
            position += direction * movement

            aircraft.position = (
                position.x,
                position.y,
            )

    def _advance_route(self, aircraft):
        aircraft.route_index += 1

        if aircraft.route_index >= len(aircraft.route):
            aircraft.speed = 0.0

    @staticmethod
    def _direction_to_heading(direction):
        angle = math.degrees(
            math.atan2(
                direction.x,
                -direction.y,
            )
        )

        return angle % 360.0

    @staticmethod
    def _turn_toward(
        current_heading,
        target_heading,
        max_change,
    ):
        difference = (
            target_heading
            - current_heading
            + 180.0
        ) % 360.0 - 180.0

        if abs(difference) <= max_change:
            return target_heading

        if difference > 0:
            return (
                current_heading + max_change
            ) % 360.0

        return (
            current_heading - max_change
        ) % 360.0
