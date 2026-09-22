import pygame


class Apron:
    def __init__(
        self,
        apron_id,
        name,
        center,
        width,
        height,
        apron_type="passenger",
    ):
        self.apron_id = apron_id
        self.name = name

        self.center = pygame.Vector2(center)

        self.width = width
        self.height = height
        self.apron_type = apron_type

    def __repr__(self):
        return (
            f"Apron("
            f"id='{self.apron_id}', "
            f"name='{self.name}', "
            f"center={tuple(self.center)}, "
            f"size={self.width}x{self.height}, "
            f"type='{self.apron_type}'"
            f")"
        )
