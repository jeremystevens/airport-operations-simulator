from src.aircraft.aircraft import AircraftState
from src.simulation.commands import (
    LandingClearance,
    LineUpAndWaitClearance,
    TakeoffClearance,
)
from src.simulation.pathfinding import find_taxiway_path


class CommandExecutor:
    def execute(
        self,
        command,
        airport,
    ):
        if isinstance(
            command,
            LineUpAndWaitClearance,
        ):
            return self._execute_line_up(
                command,
                airport,
            )

        if isinstance(
            command,
            TakeoffClearance,
        ):
            return self._execute_takeoff(
                command,
                airport,
            )

        if isinstance(
            command,
            LandingClearance,
        ):
            return self._execute_landing(
                command,
                airport,
            )

        raise TypeError(
            f"Unsupported command: {type(command).__name__}"
        )

    def _execute_line_up(
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
            command.lineup_node_id,
        )

        if not route:
            return False

        runway.occupied = True

        aircraft.assign_route(
            route,
            destination=command.lineup_node_id,
        )

        aircraft.set_state(
            AircraftState.LINE_UP
        )

        return True

    def _execute_takeoff(
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

        # Revalidate immediately before execution.
        if aircraft.state != AircraftState.LINE_UP:
            return False

        if not runway.occupied:
            return False

        aircraft.heading = command.runway_heading
        aircraft.set_state(
            AircraftState.TAKEOFF
        )

        return True

    def _execute_landing(
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

        # Revalidate immediately before execution.
        if aircraft.state != AircraftState.APPROACH:
            return False

        if runway.occupied:
            return False

        aircraft.heading = command.runway_heading
        aircraft.set_state(
            AircraftState.LANDING
        )

        runway.occupied = True

        return True
