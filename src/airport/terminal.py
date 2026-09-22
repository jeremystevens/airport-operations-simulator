import pygame


class Terminal:
    def __init__(
        self,
        terminal_id,
        name,
        center,
        width,
        height,
    ):
        self.terminal_id = terminal_id
        self.name = name

        self.center = pygame.Vector2(center)

        self.width = width
        self.height = height

        self.gates = []

    def add_gate(self, gate):
        self.gates.append(gate)

    def __repr__(self):
        return (
            f"Terminal("
            f"id='{self.terminal_id}', "
            f"name='{self.name}', "
            f"center={tuple(self.center)}, "
            f"size={self.width}x{self.height}, "
            f"gates={len(self.gates)}"
            f")"
        )
