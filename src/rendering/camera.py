import pygame


class Camera:
    def __init__(
        self,
        screen_width,
        screen_height,
        initial_zoom=0.19,
    ):
        self.screen_width = screen_width
        self.screen_height = screen_height

        self.position = pygame.Vector2(0, 0)
        self.zoom = initial_zoom
        self.min_zoom = 0.10
        self.max_zoom = 4.00
        self.zoom_step = 0.15

        self.move_speed = 600.0

    def world_to_screen(self, world_position):
        """Convert a position in the simulation world to screen coordinates."""

        world_position = pygame.Vector2(world_position)

        screen_x = (
            (world_position.x - self.position.x) * self.zoom
            + self.screen_width / 2
        )

        screen_y = (
            (world_position.y - self.position.y) * self.zoom
            + self.screen_height / 2
        )

        return pygame.Vector2(screen_x, screen_y)

    def handle_event(self, event):
        """Handle camera-specific input events."""

        if event.type == pygame.MOUSEWHEEL:
            if event.y > 0:
                self.zoom *= 1.0 + self.zoom_step

            elif event.y < 0:
                self.zoom /= 1.0 + self.zoom_step

            self.zoom = max(
                self.min_zoom,
                min(self.zoom, self.max_zoom),
            )

    def update(self, dt):
        """Move the camera using WASD or arrow keys."""

        keys = pygame.key.get_pressed()

        direction = pygame.Vector2()

        if keys[pygame.K_w] or keys[pygame.K_UP]:
            direction.y -= 1

        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            direction.y += 1

        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            direction.x -= 1

        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            direction.x += 1

        if direction.length_squared() > 0:
            direction = direction.normalize()

            self.position += (
                direction
                * self.move_speed
                * dt
                / self.zoom
            )
