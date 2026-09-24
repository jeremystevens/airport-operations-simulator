from src.aircraft.aircraft import AircraftState
from src.simulation.commands import (
    ContinueTaxi,
    HoldPosition,
    LandingClearance,
    LineUpAndWaitClearance,
    TakeoffClearance,
    TaxiClearance,
)
from src.simulation.pathfinding import find_taxiway_path


class CommandExecutor:
    def _find_aircraft(
        self,
        airport,
        aircraft_id,
    ):
        return next(
            (
                aircraft
                for aircraft in airport.aircraft
                if aircraft.flight_id == aircraft_id
            ),
            None,
        )

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

        if isinstance(command, TaxiClearance):
            return self._execute_taxi_clearance(
                command,
                airport,
            )

        if isinstance(command, HoldPosition):
            return self._execute_hold_position(
                command,
                airport,
            )

        if isinstance(command, ContinueTaxi):
            return self._execute_continue_taxi(
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

    def _execute_taxi_clearance(
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
            return False

        if aircraft.state not in (
            AircraftState.TAXI_IN,
            AircraftState.TAXI_OUT,
        ):
            return False

        if not command.route:
            return False

        for node_id in command.route:
            if node_id not in airport.taxiway_nodes:
                return False

        if command.destination not in airport.taxiway_nodes:
            return False

        aircraft.assign_route(
            list(command.route),
            destination=command.destination,
        )

        return True

    def _execute_hold_position(
        self,
        command,
        airport,
    ):
        aircraft = self._find_aircraft(
            airport,
            command.aircraft_id,
        )

        if aircraft is None:
            return False

        if aircraft.state not in (
            AircraftState.TAXI_IN,
            AircraftState.TAXI_OUT,
        ):
            return False

        if aircraft.ground_hold:
            return False

        aircraft.ground_hold = True
        aircraft.ground_hold_reason = command.reason
        aircraft.ground_hold_for_aircraft = (
            command.traffic_id
        )
        aircraft.speed = 0.0

        return True

    def _execute_continue_taxi(
        self,
        command,
        airport,
    ):
        aircraft = self._find_aircraft(
            airport,
            command.aircraft_id,
        )

        if aircraft is None:
            return False

        if aircraft.state not in (
            AircraftState.TAXI_IN,
            AircraftState.TAXI_OUT,
        ):
            return False

        if not aircraft.ground_hold:
            return False

        if command.resource_id is not None:
            owner = airport.get_taxiway_conflict_owner(
                command.resource_id
            )

            if (
                owner is not None
                and owner != aircraft.flight_id
            ):
                return False

        aircraft.ground_hold = False
        aircraft.ground_hold_reason = None
        aircraft.ground_hold_for_aircraft = None

        return True
