import pygame


class HUD:
    def __init__(self):
        self.font = pygame.font.Font(
            None,
            28,
        )

        self.small_font = pygame.font.Font(
            None,
            20,
        )

    def draw(
        self,
        screen,
        airport,
        simulation_clock,
        camera,
    ):
        self._draw_airport_info(
            screen,
            airport,
            simulation_clock,
        )

        self._draw_sim_speed(
            screen,
            simulation_clock,
        )

        self._draw_zoom(
            screen,
            camera,
        )

    def _draw_airport_info(
        self,
        screen,
        airport,
        simulation_clock,
    ):
        airport_text = self.font.render(
            f"{airport.code} - {airport.name.upper()}",
            True,
            (220, 225, 230),
        )

        time_text = self.font.render(
            f"DAY {simulation_clock.day}  |  {simulation_clock.get_time_string()}",
            True,
            (180, 190, 200),
        )

        screen.blit(airport_text, (20, 20))
        screen.blit(time_text, (20, 50))

    def _draw_sim_speed(
        self,
        screen,
        simulation_clock,
    ):
        speed_text = self.small_font.render(
            f"SIM {simulation_clock.time_scale:g}x",
            True,
            (220, 220, 210),
        )

        rect = speed_text.get_rect(
            bottomright=(
                screen.get_width() - 12,
                screen.get_height() - 12 - 22,
            )
        )

        screen.blit(
            speed_text,
            rect,
        )

    def _draw_zoom(
        self,
        screen,
        camera,
    ):
        text = self.small_font.render(
            f"ZOOM {camera.zoom:.2f}x",
            True,
            (220, 220, 210),
        )

        rect = text.get_rect(
            bottomright=(
                screen.get_width() - 12,
                screen.get_height() - 12,
            )
        )

        screen.blit(
            text,
            rect,
        )
