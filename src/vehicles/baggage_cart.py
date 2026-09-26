import pygame


class BaggageCart:
    def __init__(self, cart_id, position=(0.0, 0.0), heading=0.0):
        self.cart_id = cart_id
        self.position = pygame.Vector2(position)
        self.heading = float(heading)
