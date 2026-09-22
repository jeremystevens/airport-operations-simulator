from src.aircraft.aircraft import AircraftState
from src.simulation.commands import RunwayEntryClearance
from src.simulation.pathfinding import find_taxiway_path


class CommandExecutor:
    def execute(
        self,
        command,
        airport,
    ):
        if isinstance(
            command,
            RunwayEntryClearance,
        ):
            return self._execute_runway_entry(
                command,
                airport,
            )

        raise TypeError(
            f"Unsupported command: {type(command).__name__}"
        )

    def _execute_runway_entry(
        self,
        command,
        airport,
    ):
        aircraft = next(
            (
                aircraft
                for aircraft in airport.aircraft
                if aircraft.flight_id
                == command.aircraft_id
            ),
            None,
        )

        if aircraft is None:
            raise ValueError(
                f"Unknown aircraft: "
                f"{command.aircraft_id}"
            )

        runway = next(
            (
                runway
                for runway in airport.runways
                if runway.name
                == command.runway_name
            ),
            None,
        )

        if runway is None:
            raise ValueError(
                f"Unknown runway: "
                f"{command.runway_name}"
            )

        # Revalidate at execution time.
        if aircraft.state != AircraftState.HOLD_SHORT:
            return False

        if runway.occupied:
            return False

        route = find_taxiway_path(
            airport,
            command.hold_node_id,
            command.runway_entry_node_id,
        )

        if not route:
            return False

        runway.occupied = True

        aircraft.assign_route(
            route,
            destination=command.runway_entry_node_id,
        )

        aircraft.set_state(
            AircraftState.RUNWAY
        )

        return True
