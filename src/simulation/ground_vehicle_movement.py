import math

import pygame

from src.aircraft.profiles import get_aircraft_dimensions
from src.simulation.turnaround_service import ServiceType
from src.vehicles.ground_vehicle import GroundVehicleState

# Aircraft-relative working area for each ground service, expressed as a
# fraction of aircraft length (longitudinal_factor, positive = toward the
# nose, negative = toward the tail) and a side ("left"/"right", aircraft-
# relative -- not tied to any particular gate's compass orientation).
# get_fuel_service_position() predates this and is left alone (its
# existing behavior matches longitudinal_factor=0.05, side="left" here,
# confirmed by the numbers already in use); get_baggage_service_position()
# is the first to actually read from it.
SERVICE_ZONE_CONFIG = {
    ServiceType.FUEL: {
        "longitudinal_factor": 0.05,
        "side": "left",
    },
    ServiceType.BAGGAGE: {
        "longitudinal_factor": -0.45,
        "side": "left",
    },
}


def _service_side_vector(right, side):
    if side == "right":
        return right

    if side == "left":
        return -right

    raise ValueError(f"Unknown service zone side: {side}")


def get_fuel_service_position(
    aircraft,
    truck_clearance=55.0,
    longitudinal_offset=15.0,
):
    dimensions = get_aircraft_dimensions(aircraft)

    heading_radians = math.radians(aircraft.heading)

    forward = pygame.Vector2(
        math.sin(heading_radians),
        -math.cos(heading_radians),
    )

    right = pygame.Vector2(-forward.y, forward.x)

    lateral_offset = (
        dimensions["wingspan"] / 2.0 + truck_clearance
    )

    # Fuel trucks service from the aircraft's left side, matching the
    # side our fuel staging nodes (FUEL_A4, etc.) are laid out on.
    return (
        pygame.Vector2(aircraft.position)
        - right * lateral_offset
        + forward * longitudinal_offset
    )


def get_baggage_service_position(
    aircraft,
    tractor_clearance=45.0,
):
    dimensions = get_aircraft_dimensions(aircraft)
    zone = SERVICE_ZONE_CONFIG[ServiceType.BAGGAGE]

    heading_radians = math.radians(aircraft.heading)

    forward = pygame.Vector2(
        math.sin(heading_radians),
        -math.cos(heading_radians),
    )

    right = pygame.Vector2(-forward.y, forward.x)
    side_vector = _service_side_vector(right, zone["side"])

    lateral_offset = (
        dimensions["wingspan"] / 2.0 + tractor_clearance
    )

    longitudinal_offset = (
        dimensions["length"] * zone["longitudinal_factor"]
    )

    return (
        pygame.Vector2(aircraft.position)
        + side_vector * lateral_offset
        + forward * longitudinal_offset
    )


def is_service_position_safe(aircraft, position):
    dimensions = get_aircraft_dimensions(aircraft)

    minimum_clearance = (
        max(dimensions["length"], dimensions["wingspan"])
        / 2.0
    )

    distance = pygame.Vector2(position).distance_to(
        pygame.Vector2(aircraft.position)
    )

    return distance >= minimum_clearance


def is_baggage_consist_safe(aircraft, tractor):
    if not is_service_position_safe(
        aircraft,
        tractor.position,
    ):
        return False

    for cart in tractor.carts:
        if not is_service_position_safe(
            aircraft,
            cart.position,
        ):
            return False

    return True


def find_blocking_service_vehicle(
    airport,
    vehicle,
    target_position,
    minimum_clearance=100.0,
):
    target_position = pygame.Vector2(target_position)

    for other in airport.ground_vehicles:
        if other is vehicle:
            continue

        if not other.active:
            continue

        if (
            target_position.distance_to(
                pygame.Vector2(other.position)
            )
            < minimum_clearance
        ):
            return other

        for cart in getattr(other, "carts", []):
            if (
                target_position.distance_to(
                    pygame.Vector2(cart.position)
                )
                < minimum_clearance
            ):
                return other

    return None


def is_service_vehicle_clear(
    airport,
    vehicle,
    target_position,
    minimum_clearance=100.0,
):
    return (
        find_blocking_service_vehicle(
            airport,
            vehicle,
            target_position,
            minimum_clearance,
        )
        is None
    )


def find_consist_blocking_vehicle(
    airport,
    tractor,
    minimum_clearance=100.0,
):
    points = [pygame.Vector2(tractor.position)]

    points += [
        pygame.Vector2(cart.position)
        for cart in getattr(tractor, "carts", [])
    ]

    for point in points:
        blocker = find_blocking_service_vehicle(
            airport,
            tractor,
            point,
            minimum_clearance,
        )

        if blocker is not None:
            return blocker

    return None


def has_connected_service_vehicle(airport, aircraft_id):
    return any(
        vehicle.assigned_aircraft_id == aircraft_id
        and vehicle.state
        in (
            GroundVehicleState.CONNECTED,
            GroundVehicleState.SERVICING,
            GroundVehicleState.DISCONNECTING,
        )
        for vehicle in airport.ground_vehicles
    )


def dispatch_ground_vehicle(
    vehicle,
    aircraft,
    route,
    destination,
):
    if vehicle.state != GroundVehicleState.PARKED:
        return False

    if not route:
        return False

    vehicle.assign_aircraft(aircraft)

    vehicle.assign_route(
        route,
        final_target=destination,
    )

    vehicle.state = GroundVehicleState.DISPATCHED
    vehicle.active = True

    return True


class GroundVehicleMovementController:
    def __init__(
        self,
        drive_speed=65.0,
        turn_rate=180.0,
    ):
        self.drive_speed = float(drive_speed)
        self.turn_rate = float(turn_rate)

    def move_toward(
        self,
        vehicle,
        target,
        dt,
        speed=None,
    ):
        if speed is None:
            speed = self.drive_speed

        position = pygame.Vector2(
            vehicle.position
        )

        target = pygame.Vector2(target)

        offset = target - position
        distance = offset.length()

        if distance < 1.0:
            vehicle.position = target
            vehicle.speed = 0.0
            return True

        direction = offset.normalize()

        target_heading = (
            math.degrees(
                math.atan2(
                    direction.x,
                    -direction.y,
                )
            )
            % 360.0
        )

        vehicle.heading = self._turn_toward(
            vehicle.heading,
            target_heading,
            self.turn_rate * dt,
        )

        movement = speed * dt
        vehicle.speed = speed

        if movement >= distance:
            vehicle.position = target
            vehicle.speed = 0.0
            return True

        vehicle.position = (
            position
            + direction * movement
        )

        return False

    def update_route(
        self,
        vehicle,
        airport,
        dt,
    ):
        if not vehicle.has_route:
            vehicle.speed = 0.0
            return False

        node_id = vehicle.current_route_node
        target_node = airport.service_nodes[
            node_id
        ]

        arrived = self.move_toward(
            vehicle,
            target_node.position,
            dt,
        )

        if not arrived:
            return False

        vehicle.route_index += 1

        if vehicle.route_index >= len(vehicle.route):
            vehicle.speed = 0.0
            return True

        return False

    @staticmethod
    def _turn_toward(
        current,
        target,
        max_change,
    ):
        difference = (
            target - current + 180.0
        ) % 360.0 - 180.0

        if abs(difference) <= max_change:
            return target

        if difference > 0:
            return (
                current + max_change
            ) % 360.0

        return (
            current - max_change
        ) % 360.0
