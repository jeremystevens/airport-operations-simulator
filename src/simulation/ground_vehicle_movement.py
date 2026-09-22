import math

import pygame


class GroundVehicleMovementController:
    def __init__(
        self,
        drive_speed=65.0,
        turn_rate=180.0,
    ):
        self.drive_speed = float(drive_speed)
        self.turn_rate = float(turn_rate)

    def move_toward(
        self,
        vehicle,
        target,
        dt,
    ):
        position = pygame.Vector2(
            vehicle.position
        )

        target = pygame.Vector2(target)

        offset = target - position
        distance = offset.length()

        if distance < 1.0:
            vehicle.position = target
            vehicle.speed = 0.0
            return True

        direction = offset.normalize()

        target_heading = (
            math.degrees(
                math.atan2(
                    direction.x,
                    -direction.y,
                )
            )
            % 360.0
        )

        vehicle.heading = self._turn_toward(
            vehicle.heading,
            target_heading,
            self.turn_rate * dt,
        )

        movement = self.drive_speed * dt
        vehicle.speed = self.drive_speed

        if movement >= distance:
            vehicle.position = target
            vehicle.speed = 0.0
            return True

        vehicle.position = (
            position
            + direction * movement
        )

        return False

    @staticmethod
    def _turn_toward(
        current,
        target,
        max_change,
    ):
        difference = (
            target - current + 180.0
        ) % 360.0 - 180.0

        if abs(difference) <= max_change:
            return target

        if difference > 0:
            return (
                current + max_change
            ) % 360.0

        return (
            current - max_change
        ) % 360.0
