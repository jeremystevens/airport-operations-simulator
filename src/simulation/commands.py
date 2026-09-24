from dataclasses import dataclass


@dataclass(frozen=True)
class LineUpAndWaitClearance:
    aircraft_id: str
    runway_name: str
    hold_node_id: str
    runway_entry_node_id: str
    lineup_node_id: str
    runway_heading: float


@dataclass(frozen=True)
class TakeoffClearance:
    aircraft_id: str
    runway_name: str
    runway_heading: float


@dataclass(frozen=True)
class LandingClearance:
    aircraft_id: str
    runway_name: str
    runway_heading: float
