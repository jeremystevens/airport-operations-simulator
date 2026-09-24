from enum import Enum, IntEnum


class AircraftState(Enum):
    APPROACH = "approach"
    LANDING = "landing"
    LANDING_ROLL = "landing_roll"
    RUNWAY = "runway"
    TAXI_IN = "taxi_in"
    AT_GATE = "at_gate"
    SERVICING = "servicing"
    PUSHBACK = "pushback"
    TAXI_OUT = "taxi_out"
    HOLD_SHORT = "hold_short"
    LINE_UP = "line_up"
    TAKEOFF = "takeoff"
    AIRBORNE = "airborne"
    DEPARTED = "departed"


class AircraftOperation(Enum):
    PASSENGER = "passenger"
    CARGO = "cargo"
    PRIVATE = "private"


class AircraftSize(IntEnum):
    LIGHT = 1
    BUSINESS = 2
    REGIONAL = 3
    NARROWBODY = 4
    WIDEBODY = 5
    SUPERHEAVY = 6


class Aircraft:
    def __init__(
        self,
        flight_id,
        aircraft_type,
        size,
        operation,
        position=(0.0, 0.0),
        heading=0.0,
        passenger_capacity=0,
        passengers=0,
        cargo_kg=0.0,
    ):
        self.flight_id = flight_id
        self.aircraft_type = aircraft_type
        self.size = size
        self.operation = operation

        self.position = (
            float(position[0]),
            float(position[1]),
        )

        self.heading = float(heading)
        self.speed = 0.0
        self.altitude = 0.0

        self.state = AircraftState.AT_GATE
        self.assigned_gate = None

        self.passenger_capacity = int(passenger_capacity)
        self.passengers = int(passengers)
        self.cargo_kg = float(cargo_kg)

        self.route = []
        self.route_index = 0
        self.route_destination = None

        self.pushback_target = None
        self.pushback_speed = 0.0

        self.runway_exit_ready = False

        self.current_taxiway_node = None
        self.reserved_taxiway_segment = None
        self.waiting_for_taxiway = None

        self.reserved_taxiway_conflict = None
        self.waiting_for_taxiway_conflict = None

        # Bookkeeping for the delayed (footprint-based) release of a
        # held conflict resource -- not part of the public API, just
        # tracks where the aircraft was when it left the resource's
        # segments so we know when it has cleared by a safety margin.
        self.taxiway_conflict_exit_point = None

        # True once the aircraft has actually been on one of the
        # reserved conflict group's segments. A reservation made via
        # lookahead (before the aircraft physically reaches the group)
        # must not be mistaken for having already exited it.
        self.taxiway_conflict_entered = False

        self.ground_hold = False
        self.ground_hold_reason = None
        self.ground_hold_for_aircraft = None

    def assign_gate(self, gate):
        self.assigned_gate = gate

    def assign_route(
        self,
        route,
        destination=None,
    ):
        self.route = list(route)
        self.route_index = 0
        self.route_destination = destination

    def clear_route(self):
        self.route = []
        self.route_index = 0
        self.route_destination = None

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

    def set_state(self, state):
        if not isinstance(state, AircraftState):
            raise TypeError("state must be an AircraftState")

        self.state = state

    def __repr__(self):
        return (
            f"Aircraft("
            f"flight_id='{self.flight_id}', "
            f"type='{self.aircraft_type}', "
            f"size='{self.size.name.lower()}', "
            f"operation='{self.operation.value}', "
            f"state='{self.state.value}'"
            f")"
        )
