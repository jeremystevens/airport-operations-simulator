import pygame


class FacilityRenderer:
    APRON = (112, 112, 108)
    APRON_EDGE = (145, 145, 138)

    TERMINAL = (82, 88, 92)
    TERMINAL_EDGE = (150, 155, 158)

    GATE_LINE = (225, 190, 55)
    GATE_LABEL = (235, 235, 230)
    GATE_STOP = (220, 215, 195)

    def draw(self, screen, camera, airport):
        for apron in airport.aprons:
            self._draw_apron(screen, camera, apron)

        for terminal in airport.terminals:
            self._draw_terminal(screen, camera, terminal)

        for terminal in airport.terminals:
            for gate in terminal.gates:
                self._draw_gate(screen, camera, gate)

    def _world_rect(self, camera, center, width, height):
        top_left = camera.world_to_screen(
            (
                center.x - width / 2,
                center.y - height / 2,
            )
        )

        bottom_right = camera.world_to_screen(
            (
                center.x + width / 2,
                center.y + height / 2,
            )
        )

        return pygame.Rect(
            int(top_left.x),
            int(top_left.y),
            int(bottom_right.x - top_left.x),
            int(bottom_right.y - top_left.y),
        )

    def _draw_apron(self, screen, camera, apron):
        rect = self._world_rect(
            camera,
            apron.center,
            apron.width,
            apron.height,
        )

        pygame.draw.rect(
            screen,
            self.APRON,
            rect,
        )

        pygame.draw.rect(
            screen,
            self.APRON_EDGE,
            rect,
            max(1, int(2 * camera.zoom)),
        )

    def _draw_terminal(self, screen, camera, terminal):
        rect = self._world_rect(
            camera,
            terminal.center,
            terminal.width,
            terminal.height,
        )

        pygame.draw.rect(
            screen,
            self.TERMINAL,
            rect,
        )

        pygame.draw.rect(
            screen,
            self.TERMINAL_EDGE,
            rect,
            max(1, int(3 * camera.zoom)),
        )

    def _draw_gate(self, screen, camera, gate):
        """Draw an aircraft parking stand."""

        gate_position = camera.world_to_screen(
            gate.position
        )

        # Lead-in line begins north of the parking position.
        lead_start = camera.world_to_screen(
            (
                gate.position.x,
                gate.position.y - 300,
            )
        )

        pygame.draw.line(
            screen,
            self.GATE_LINE,
            lead_start,
            gate_position,
            max(1, int(4 * camera.zoom)),
        )

        # Aircraft stop bar.
        stop_half_width = 45

        stop_left = camera.world_to_screen(
            (
                gate.position.x - stop_half_width,
                gate.position.y,
            )
        )

        stop_right = camera.world_to_screen(
            (
                gate.position.x + stop_half_width,
                gate.position.y,
            )
        )

        pygame.draw.line(
            screen,
            self.GATE_STOP,
            stop_left,
            stop_right,
            max(1, int(6 * camera.zoom)),
        )

        self._draw_gate_label(
            screen,
            camera,
            gate,
        )

    def _draw_gate_label(self, screen, camera, gate):
        font_size = max(
            10,
            int(42 * camera.zoom),
        )

        font = pygame.font.Font(
            None,
            font_size,
        )

        label = font.render(
            gate.gate_id,
            True,
            self.GATE_LABEL,
        )

        position = camera.world_to_screen(
            (
                gate.position.x + 70,
                gate.position.y + 35,
            )
        )

        rect = label.get_rect(
            topleft=(
                int(position.x),
                int(position.y),
            )
        )

        screen.blit(label, rect)
