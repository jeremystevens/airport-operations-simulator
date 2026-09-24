from src.aircraft.aircraft import AircraftState
from src.simulation.commands import TaxiClearance


class GroundController:
    def __init__(self, enabled=True):
        self.enabled = enabled

    def evaluate_taxi_clearance(
        self,
        aircraft,
        route,
        destination,
    ):
        if not self.enabled:
            return None

        if aircraft.state not in (
            AircraftState.TAXI_IN,
            AircraftState.TAXI_OUT,
        ):
            return None

        if not route:
            return None

        return TaxiClearance(
            aircraft_id=aircraft.flight_id,
            route=tuple(route),
            destination=destination,
        )
