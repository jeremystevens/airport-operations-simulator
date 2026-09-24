import pygame

from src.aircraft.aircraft import AircraftState
from src.aircraft.profiles import get_aircraft_dimensions

# How far (in world units) Ground looks ahead along an arrival's route
# to decide it has effectively claimed a shared taxiway resource, even
# before it has physically reached the resource's entry point.
CONFLICT_LOOKAHEAD_DISTANCE = 700.0

# Temporary safety margin (world units) added on top of the raw
# geometric half-length/half-wingspan overlap.
SAFETY_MARGIN = 75.0


def taxi_priority(aircraft):
    if aircraft.state == AircraftState.TAXI_IN:
        return 2

    if aircraft.state == AircraftState.TAXI_OUT:
        return 1

    return 0


def safe_hold_clearance(
    waiting_aircraft,
    passing_aircraft,
):
    waiting_dimensions = get_aircraft_dimensions(
        waiting_aircraft
    )

    passing_dimensions = get_aircraft_dimensions(
        passing_aircraft
    )

    return (
        waiting_dimensions["length"] / 2.0
        + passing_dimensions["wingspan"] / 2.0
        + SAFETY_MARGIN
    )


class GroundTrafficController:
    """Owns conflict-group resource arbitration for taxiing aircraft:
    who gets to use a shared bottleneck, who has to hold short of it,
    and when a resource is fully released. AircraftMovementController
    only has to respect aircraft.ground_hold -- it doesn't decide
    priority or manage conflict-group reservations itself.

    The hold/continue decisions themselves are issued as GroundController
    commands and applied through CommandExecutor, so the same authority
    pipeline used for taxi clearances governs this traffic-conflict
    arbitration."""

    def __init__(self, ground_controller, command_executor):
        self.ground_controller = ground_controller
        self.command_executor = command_executor

    def update(self, airport, aircraft_list, dt):
        for aircraft in aircraft_list:
            self._process_pending_release(
                aircraft,
                airport,
            )

        # Process higher-priority aircraft first so an arrival can
        # preempt a departure's advance (lookahead) reservation before
        # the departure's own turn has a chance to lock it back in.
        ordered = sorted(
            aircraft_list,
            key=taxi_priority,
            reverse=True,
        )

        for aircraft in ordered:
            self._update_aircraft(
                aircraft,
                airport,
                aircraft_list,
            )

    def _update_aircraft(
        self,
        aircraft,
        airport,
        aircraft_list,
    ):
        if aircraft.state not in (
            AircraftState.TAXI_IN,
            AircraftState.TAXI_OUT,
        ):
            return

        upcoming = self._upcoming_conflict_group(
            aircraft,
            airport,
        )

        if upcoming is None:
            return

        group_id, entry_distance = upcoming

        if aircraft.reserved_taxiway_conflict == group_id:
            return

        self._maybe_preempt_owner(
            aircraft,
            airport,
            aircraft_list,
            group_id,
            entry_distance,
        )

        blocking_aircraft = self._find_blocking_aircraft(
            aircraft,
            airport,
            aircraft_list,
            group_id,
        )

        if blocking_aircraft is not None:
            required_clearance = safe_hold_clearance(
                aircraft,
                blocking_aircraft,
            )

            if entry_distance <= required_clearance:
                self._apply_hold(
                    aircraft,
                    blocking_aircraft,
                    group_id,
                    airport,
                )

            return

        # No contention. If we were holding, clear that, and if we're
        # close enough to actually need the resource, claim it.
        if aircraft.ground_hold:
            self._clear_hold(aircraft, group_id, airport)

        if entry_distance <= CONFLICT_LOOKAHEAD_DISTANCE:
            if airport.reserve_taxiway_conflict(
                group_id,
                aircraft.flight_id,
            ):
                aircraft.reserved_taxiway_conflict = (
                    group_id
                )

    # ------------------------------------------------------------------
    # Route/geometry helpers
    # ------------------------------------------------------------------

    def _upcoming_conflict_group(self, aircraft, airport):
        """Walk the aircraft's remaining route (cumulative, multi-hop)
        and return (group_id, distance_to_entry) for the first
        conflict-group segment it will cross, or None if its route
        never touches one."""

        if not aircraft.has_route:
            return None

        prev_node_id = aircraft.current_taxiway_node
        prev_position = pygame.Vector2(aircraft.position)
        cumulative = 0.0

        for index in range(
            aircraft.route_index,
            len(aircraft.route),
        ):
            node_id = aircraft.route[index]
            node = airport.taxiway_nodes.get(node_id)

            if node is None:
                return None

            position = pygame.Vector2(node.position)

            if prev_node_id is not None:
                segment = airport.get_taxiway_segment_between(
                    prev_node_id,
                    node_id,
                )

                if (
                    segment is not None
                    and segment.conflict_group is not None
                ):
                    return (
                        segment.conflict_group,
                        cumulative,
                    )

            cumulative += prev_position.distance_to(
                position
            )

            prev_position = position
            prev_node_id = node_id

        return None

    def _aircraft_distance_to_group(
        self,
        aircraft,
        airport,
        group_id,
    ):
        upcoming = self._upcoming_conflict_group(
            aircraft,
            airport,
        )

        if upcoming is None:
            return None

        found_group_id, distance = upcoming

        if found_group_id != group_id:
            return None

        return distance

    def _maybe_preempt_owner(
        self,
        aircraft,
        airport,
        aircraft_list,
        group_id,
        entry_distance,
    ):
        """A lower-priority aircraft may have reserved this resource via
        lookahead before a higher-priority aircraft got close. That's
        fine while it hasn't physically entered the resource yet -- but
        it must not be allowed to keep first-come-first-served ownership
        against a higher-priority aircraft that is now close enough to
        be committed. Once the owner has actually entered, though, it's
        physically inside the corridor and can't be recalled, so it
        keeps the resource regardless of priority."""

        owner_id = airport.get_taxiway_conflict_owner(
            group_id
        )

        if owner_id is None or owner_id == aircraft.flight_id:
            return

        owner = next(
            (
                other
                for other in aircraft_list
                if other.flight_id == owner_id
            ),
            None,
        )

        if owner is None:
            return

        if owner.taxiway_conflict_entered:
            return

        if taxi_priority(aircraft) <= taxi_priority(owner):
            return

        if entry_distance > CONFLICT_LOOKAHEAD_DISTANCE:
            return

        airport.release_taxiway_conflict(
            group_id,
            owner.flight_id,
        )

        owner.reserved_taxiway_conflict = None
        owner.taxiway_conflict_exit_point = None
        owner.taxiway_conflict_entered = False

        self._apply_hold(owner, aircraft, group_id, airport)

    def _find_blocking_aircraft(
        self,
        aircraft,
        airport,
        aircraft_list,
        group_id,
    ):
        owner_id = airport.get_taxiway_conflict_owner(
            group_id
        )

        if owner_id is not None and owner_id != aircraft.flight_id:
            owner = next(
                (
                    other
                    for other in aircraft_list
                    if other.flight_id == owner_id
                ),
                None,
            )

            if owner is not None:
                return owner

        for other in aircraft_list:
            if other is aircraft:
                continue

            if taxi_priority(other) <= taxi_priority(
                aircraft
            ):
                continue

            other_distance = self._aircraft_distance_to_group(
                other,
                airport,
                group_id,
            )

            if (
                other_distance is not None
                and other_distance <= CONFLICT_LOOKAHEAD_DISTANCE
            ):
                return other

        return None

    # ------------------------------------------------------------------
    # Hold / continue / release bookkeeping
    # ------------------------------------------------------------------

    def _apply_hold(
        self,
        aircraft,
        blocking_aircraft,
        group_id,
        airport,
    ):
        if (
            aircraft.ground_hold
            and aircraft.ground_hold_for_aircraft
            == blocking_aircraft.flight_id
        ):
            return

        reason = (
            "opposing_arrival"
            if taxi_priority(blocking_aircraft)
            > taxi_priority(aircraft)
            else "traffic"
        )

        command = self.ground_controller.evaluate_hold_position(
            aircraft,
            reason=reason,
            traffic_id=blocking_aircraft.flight_id,
            resource_id=group_id,
        )

        if command is None:
            return

        executed = self.command_executor.execute(
            command,
            airport,
        )

        if executed:
            print(
                f"[GROUND] {aircraft.flight_id} HOLD POSITION | "
                f"traffic={blocking_aircraft.flight_id} | "
                f"reason={command.reason} | "
                f"resource={group_id}"
            )

    def _clear_hold(self, aircraft, group_id, airport):
        if not aircraft.ground_hold:
            return

        cleared_traffic = aircraft.ground_hold_for_aircraft

        command = self.ground_controller.evaluate_continue_taxi(
            aircraft,
            resource_id=group_id,
        )

        if command is None:
            return

        executed = self.command_executor.execute(
            command,
            airport,
        )

        if executed:
            print(
                f"[GROUND] {aircraft.flight_id} CONTINUE TAXI | "
                f"traffic={cleared_traffic} clear | "
                f"resource={group_id}"
            )

    def _process_pending_release(self, aircraft, airport):
        if aircraft.reserved_taxiway_conflict is None:
            return

        group_id = aircraft.reserved_taxiway_conflict

        if aircraft.taxiway_conflict_exit_point is None:
            if self._still_in_group(
                aircraft,
                airport,
                group_id,
            ):
                aircraft.taxiway_conflict_entered = True
                return

            if not aircraft.taxiway_conflict_entered:
                # Reserved this resource in advance (lookahead) but
                # hasn't physically reached its segments yet -- there
                # is nothing to release.
                return

            boundary_node = airport.taxiway_nodes.get(
                aircraft.current_taxiway_node
            )

            aircraft.taxiway_conflict_exit_point = (
                pygame.Vector2(boundary_node.position)
                if boundary_node is not None
                else pygame.Vector2(aircraft.position)
            )

            return

        traveled = pygame.Vector2(
            aircraft.position
        ).distance_to(
            aircraft.taxiway_conflict_exit_point
        )

        clearance_needed = (
            get_aircraft_dimensions(aircraft)["length"]
            / 2.0
            + SAFETY_MARGIN
        )

        if traveled >= clearance_needed:
            airport.release_taxiway_conflict(
                group_id,
                aircraft.flight_id,
            )

            aircraft.reserved_taxiway_conflict = None
            aircraft.taxiway_conflict_exit_point = None
            aircraft.taxiway_conflict_entered = False

            print(
                f"[GROUND] {aircraft.flight_id} "
                f"CLEAR OF CONFLICT | "
                f"resource={group_id}"
            )

    def _still_in_group(
        self,
        aircraft,
        airport,
        group_id,
    ):
        if not aircraft.has_route:
            return False

        next_node_id = aircraft.current_route_node

        if aircraft.current_taxiway_node == next_node_id:
            return False

        segment = airport.get_taxiway_segment_between(
            aircraft.current_taxiway_node,
            next_node_id,
        )

        return (
            segment is not None
            and segment.conflict_group == group_id
        )
