import math

import pygame

from src.aircraft.aircraft import AircraftState


class AircraftMovementController:
    def __init__(
        self,
        taxi_speed=90.0,
        turn_rate=120.0,
    ):
        self.taxi_speed = float(taxi_speed)
        self.turn_rate = float(turn_rate)

    def update(self, aircraft, airport, dt):
        if aircraft.ground_hold:
            aircraft.speed = 0.0
            return

        if not aircraft.has_route:
            aircraft.speed = 0.0
            return

        node_id = aircraft.current_route_node
        target_node = airport.taxiway_nodes[node_id]

        position = pygame.Vector2(aircraft.position)
        target = pygame.Vector2(target_node.position)

        offset = target - position
        distance = offset.length()

        segment = self._segment_for_hop(
            aircraft,
            airport,
            node_id,
        )

        if segment is not None and not self._ensure_reserved(
            aircraft,
            segment,
        ):
            aircraft.speed = 0.0
            return

        # Already at this waypoint.
        if distance < 1.0:
            aircraft.position = (
                target.x,
                target.y,
            )

            self._arrive_at_node(
                aircraft,
                airport,
                node_id,
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

            self._arrive_at_node(
                aircraft,
                airport,
                node_id,
            )

            self._advance_route(aircraft)
        else:
            position += direction * movement

            aircraft.position = (
                position.x,
                position.y,
            )

    def _reservations_apply(self, aircraft):
        return aircraft.state in (
            AircraftState.TAXI_IN,
            AircraftState.TAXI_OUT,
        )

    def _segment_for_hop(
        self,
        aircraft,
        airport,
        node_id,
    ):
        if not self._reservations_apply(aircraft):
            return None

        if aircraft.current_taxiway_node is None:
            return None

        if aircraft.current_taxiway_node == node_id:
            return None

        return airport.get_taxiway_segment_between(
            aircraft.current_taxiway_node,
            node_id,
        )

    def _ensure_reserved(self, aircraft, segment):
        if (
            aircraft.reserved_taxiway_segment
            == segment.segment_id
        ):
            return True

        if not segment.reserve(aircraft.flight_id):
            if (
                aircraft.waiting_for_taxiway
                != segment.segment_id
            ):
                aircraft.waiting_for_taxiway = (
                    segment.segment_id
                )

                print(
                    f"[GROUND] {aircraft.flight_id} "
                    f"HOLDING FOR TAXIWAY | "
                    f"segment={segment.segment_id} | "
                    f"occupied_by={segment.occupied_by}"
                )

            return False

        aircraft.reserved_taxiway_segment = (
            segment.segment_id
        )

        if aircraft.waiting_for_taxiway is not None:
            print(
                f"[GROUND] {aircraft.flight_id} "
                f"RESUMING TAXI | "
                f"segment={segment.segment_id}"
            )

            aircraft.waiting_for_taxiway = None

        return True

    def _arrive_at_node(
        self,
        aircraft,
        airport,
        node_id,
    ):
        if aircraft.reserved_taxiway_segment is not None:
            held_segment = next(
                (
                    segment
                    for segment in airport.taxiway_segments
                    if segment.segment_id
                    == aircraft.reserved_taxiway_segment
                ),
                None,
            )

            if held_segment is not None:
                held_segment.release(aircraft.flight_id)

            aircraft.reserved_taxiway_segment = None

        aircraft.current_taxiway_node = node_id

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
