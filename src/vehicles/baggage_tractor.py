import math

import pygame

from src.vehicles.ground_vehicle import (
    GroundVehicle,
    GroundVehicleType,
)


def _heading_from_direction(direction):
    return math.degrees(
        math.atan2(direction.x, -direction.y)
    ) % 360.0


class BaggageTractor(GroundVehicle):
    """A GroundVehicle that tows a train of BaggageCart equipment. The
    tractor is the only routed/dispatched vehicle -- carts simply sample
    an older point from the tractor's recent position history, which
    lets them trail naturally through turns instead of snapping into a
    perfectly rigid line behind the tractor's current heading."""

    def __init__(
        self,
        vehicle_id,
        position=(0.0, 0.0),
        heading=0.0,
        cart_spacing=45.0,
        history_seed_points=40,
        history_seed_step=8.0,
    ):
        super().__init__(
            vehicle_id,
            GroundVehicleType.BAGGAGE_TRACTOR,
            position,
            heading,
        )

        self.carts = []
        self.cart_spacing = cart_spacing

        heading_radians = math.radians(heading)

        forward = pygame.Vector2(
            math.sin(heading_radians),
            -math.cos(heading_radians),
        )

        start = pygame.Vector2(position)

        # Seed a synthetic straight tail behind the tractor's starting
        # heading so carts trail correctly from the very first frame,
        # before any real movement history has accumulated.
        self._position_history = [
            start
            - forward
            * history_seed_step
            * (history_seed_points - index)
            for index in range(history_seed_points)
        ]
        self._position_history.append(start)

        self._max_history_length = 400

    def record_position(self):
        current = pygame.Vector2(self.position)

        # While stationary (parked, held for traffic, connected...) don't
        # keep padding the history with duplicate points -- under the
        # bounded cap that would eventually evict the genuine trailing
        # history the carts still need, snapping them onto the tractor.
        if (
            self._position_history
            and self._position_history[-1].distance_to(current)
            < 1e-6
        ):
            return

        self._position_history.append(current)

        if len(self._position_history) > self._max_history_length:
            self._position_history = self._position_history[
                -self._max_history_length:
            ]

    def update_carts(self):
        for index, cart in enumerate(self.carts, start=1):
            distance = self.cart_spacing * index
            position, heading = self._sample_trail(distance)

            cart.position = position
            cart.heading = heading

    def _sample_trail(self, distance_from_end):
        points = self._position_history

        if len(points) < 2:
            return pygame.Vector2(self.position), self.heading

        remaining = distance_from_end

        for index in range(len(points) - 1, 0, -1):
            end_point = points[index]
            start_point = points[index - 1]

            segment_vector = start_point - end_point
            segment_length = segment_vector.length()

            if segment_length < 1e-6:
                continue

            if remaining <= segment_length:
                t = remaining / segment_length
                position = end_point + segment_vector * t

                direction = end_point - start_point
                heading = _heading_from_direction(direction)

                return position, heading

            remaining -= segment_length

        return pygame.Vector2(points[0]), self.heading
