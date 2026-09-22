import pygame


class Runway:
    def __init__(
        self,
        name,
        center,
        length,
        width,
        heading,
    ):
        self.name = name
        self.center = pygame.Vector2(center)

        self.length = length
        self.width = width
        self.heading = heading

        self.active = True
        self.occupied = False

    def __repr__(self):
        return (
            f"Runway("
            f"name='{self.name}', "
            f"center={tuple(self.center)}, "
            f"length={self.length}, "
            f"width={self.width}, "
            f"heading={self.heading}"
            f")"
        )
