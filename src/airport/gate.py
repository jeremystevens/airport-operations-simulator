import pygame


class Gate:
    def __init__(
        self,
        gate_id,
        terminal_id,
        position,
        heading=180,
        max_aircraft_size="narrowbody",
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

    def __repr__(self):
        return (
            f"Gate("
            f"id='{self.gate_id}', "
            f"terminal='{self.terminal_id}', "
            f"position={tuple(self.position)}, "
            f"heading={self.heading}, "
            f"max_size='{self.max_aircraft_size}', "
            f"available={self.available}"
            f")"
        )
