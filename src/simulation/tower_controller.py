from src.aircraft.aircraft import AircraftState
from src.simulation.commands import RunwayEntryClearance


class TowerController:
    def __init__(self):
        self.enabled = True

    def evaluate_runway_entry(
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

        return RunwayEntryClearance(
            aircraft_id=aircraft.flight_id,
            runway_name=runway.name,
            hold_node_id=hold_node_id,
            runway_entry_node_id=runway_entry_node_id,
        )
