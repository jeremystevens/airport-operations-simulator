import pygame

from src.aircraft.aircraft import AircraftSize


class Gate:
    def __init__(
        self,
        gate_id,
        terminal_id,
        position,
        heading=180,
        max_aircraft_size=AircraftSize.NARROWBODY,
    ):
        self.gate_id = gate_id
        self.terminal_id = terminal_id

        self.position = pygame.Vector2(position)
        self.heading = heading

        self.max_aircraft_size = max_aircraft_size

        self.occupied = False
        self.reserved = False
        self.aircraft_id = None

    @property
    def available(self):
        return not self.occupied and not self.reserved

    def can_accept(self, aircraft):
        return (
            self.available
            and aircraft.size <= self.max_aircraft_size
        )

    def reserve(self, aircraft_id):
        if not self.available:
            return False

        self.reserved = True
        self.aircraft_id = aircraft_id
        return True

    def occupy(self, aircraft):
        if (
            self.occupied
            and self.aircraft_id != aircraft.flight_id
        ):
            raise RuntimeError(
                f"Gate {self.gate_id} is already occupied"
            )

        if (
            self.reserved
            and self.aircraft_id != aircraft.flight_id
        ):
            raise RuntimeError(
                f"Gate {self.gate_id} is reserved for "
                f"another aircraft"
            )

        if aircraft.size > self.max_aircraft_size:
            raise ValueError(
                f"Aircraft {aircraft.flight_id} is too large "
                f"for Gate {self.gate_id}"
            )

        self.occupied = True
        self.reserved = False
        self.aircraft_id = aircraft.flight_id

    def release(self):
        self.occupied = False
        self.reserved = False
        self.aircraft_id = None

    def __repr__(self):
        return (
            f"Gate("
            f"id='{self.gate_id}', "
            f"terminal='{self.terminal_id}', "
            f"position={tuple(self.position)}, "
            f"heading={self.heading}, "
            f"max_size='{self.max_aircraft_size.name.lower()}', "
            f"available={self.available}"
            f")"
        )
