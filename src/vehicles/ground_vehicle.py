from enum import Enum

import pygame


class GroundVehicleType(Enum):
    PUSHBACK_TUG = "pushback_tug"
    BAGGAGE_TRACTOR = "baggage_tractor"
    FUEL_TRUCK = "fuel_truck"
    CATERING_TRUCK = "catering_truck"
    SERVICE_VAN = "service_van"


class GroundVehicleState(Enum):
    PARKED = "parked"
    DISPATCHED = "dispatched"
    APPROACHING = "approaching"
    CONNECTED = "connected"
    SERVICING = "servicing"
    PUSHING = "pushing"
    RETURNING = "returning"


class GroundVehicle:
    def __init__(
        self,
        vehicle_id,
        vehicle_type,
        position=(0.0, 0.0),
        heading=0.0,
    ):
        self.vehicle_id = vehicle_id
        self.vehicle_type = vehicle_type
        self.position = pygame.Vector2(position)
        self.heading = float(heading)
        self.speed = 0.0

        self.active = False
        self.assigned_aircraft_id = None

        self.state = GroundVehicleState.PARKED
        self.home_position = pygame.Vector2(position)

        self.route = []
        self.route_index = 0

        self.final_target = None

        self.service_elapsed = 0.0

    def assign_aircraft(self, aircraft):
        self.assigned_aircraft_id = (
            aircraft.flight_id
        )

    def clear_assignment(self):
        self.assigned_aircraft_id = None

    def assign_route(self, route, final_target=None):
        self.route = list(route)
        self.route_index = 0
        self.final_target = final_target

    def clear_route(self):
        self.route = []
        self.route_index = 0

    @property
    def has_route(self):
        return (
            bool(self.route)
            and self.route_index < len(self.route)
        )

    @property
    def current_route_node(self):
        if not self.has_route:
            return None

        return self.route[self.route_index]

    def __repr__(self):
        return (
            f"GroundVehicle("
            f"id='{self.vehicle_id}', "
            f"type='{self.vehicle_type.value}', "
            f"position={tuple(self.position)}, "
            f"heading={self.heading}, "
            f"active={self.active}, "
            f"aircraft='{self.assigned_aircraft_id}'"
            f")"
        )
