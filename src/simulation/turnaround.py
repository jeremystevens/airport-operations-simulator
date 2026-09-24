from src.aircraft.aircraft import AircraftState


class TurnaroundController:
    def __init__(
        self,
        deboarding_time=10.0,
        unloading_time=8.0,
        servicing_time=15.0,
        boarding_time=12.0,
    ):
        self.deboarding_time = deboarding_time
        self.unloading_time = unloading_time
        self.servicing_time = servicing_time
        self.boarding_time = boarding_time

    def start(self, aircraft):
        if aircraft.state != AircraftState.AT_GATE:
            return False

        if aircraft.turnaround_started:
            return False

        aircraft.turnaround_started = True
        aircraft.turnaround_timer = 0.0
        aircraft.set_state(
            AircraftState.DEBOARDING
        )

        return True

    def update(self, aircraft, dt):
        if aircraft.state not in (
            AircraftState.DEBOARDING,
            AircraftState.UNLOADING,
            AircraftState.SERVICING,
            AircraftState.BOARDING,
        ):
            return None

        aircraft.turnaround_timer += dt

        if (
            aircraft.state
            == AircraftState.DEBOARDING
            and aircraft.turnaround_timer
            >= self.deboarding_time
        ):
            self._transition(
                aircraft,
                AircraftState.UNLOADING,
            )
            return "unloading"

        if (
            aircraft.state
            == AircraftState.UNLOADING
            and aircraft.turnaround_timer
            >= self.unloading_time
        ):
            self._transition(
                aircraft,
                AircraftState.SERVICING,
            )
            return "servicing"

        if (
            aircraft.state
            == AircraftState.SERVICING
            and aircraft.turnaround_timer
            >= self.servicing_time
        ):
            self._transition(
                aircraft,
                AircraftState.BOARDING,
            )
            return "boarding"

        if (
            aircraft.state
            == AircraftState.BOARDING
            and aircraft.turnaround_timer
            >= self.boarding_time
        ):
            self._transition(
                aircraft,
                AircraftState.READY_FOR_PUSHBACK,
            )
            return "ready_for_pushback"

        return None

    def _transition(
        self,
        aircraft,
        new_state,
    ):
        aircraft.turnaround_timer = 0.0
        aircraft.set_state(new_state)
