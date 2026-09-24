from src.aircraft.aircraft import AircraftState
from src.simulation.commands import (
    ContinueTaxi,
    HoldPosition,
    TaxiClearance,
)


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

    def evaluate_hold_position(
        self,
        aircraft,
        reason,
        traffic_id=None,
        resource_id=None,
    ):
        if not self.enabled:
            return None

        if aircraft.state not in (
            AircraftState.TAXI_IN,
            AircraftState.TAXI_OUT,
        ):
            return None

        if aircraft.ground_hold:
            return None

        return HoldPosition(
            aircraft_id=aircraft.flight_id,
            reason=reason,
            traffic_id=traffic_id,
            resource_id=resource_id,
        )

    def evaluate_continue_taxi(
        self,
        aircraft,
        resource_id=None,
    ):
        if not self.enabled:
            return None

        if aircraft.state not in (
            AircraftState.TAXI_IN,
            AircraftState.TAXI_OUT,
        ):
            return None

        if not aircraft.ground_hold:
            return None

        return ContinueTaxi(
            aircraft_id=aircraft.flight_id,
            resource_id=resource_id,
        )
