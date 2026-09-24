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


@dataclass(frozen=True)
class TaxiClearance:
    aircraft_id: str
    route: tuple[str, ...]
    destination: str


@dataclass(frozen=True)
class HoldPosition:
    aircraft_id: str
    reason: str
    traffic_id: str | None = None
    resource_id: str | None = None


@dataclass(frozen=True)
class ContinueTaxi:
    aircraft_id: str
    resource_id: str | None = None
