from src.aircraft.aircraft import AircraftState
from src.simulation.commands import (
    LineUpAndWaitClearance,
    TakeoffClearance,
)


class TowerController:
    def __init__(self):
        self.enabled = True

    def evaluate_line_up(
        self,
        aircraft,
        runway,
        hold_node_id,
        runway_entry_node_id,
    ):
        if not self.enabled:
            return None

        if aircraft.state != AircraftState.HOLD_SHORT:
            return None

        if runway.occupied:
            return None

        return LineUpAndWaitClearance(
            aircraft_id=aircraft.flight_id,
            runway_name=runway.name,
            hold_node_id=hold_node_id,
            runway_entry_node_id=runway_entry_node_id,
            lineup_node_id="LINEUP_09",
            runway_heading=90.0,
        )

    def evaluate_takeoff(
        self,
        aircraft,
        runway,
        runway_heading,
    ):
        if not self.enabled:
            return None

        if aircraft.state != AircraftState.LINE_UP:
            return None

        if not runway.occupied:
            return None

        return TakeoffClearance(
            aircraft_id=aircraft.flight_id,
            runway_name=runway.name,
            runway_heading=runway_heading,
        )
