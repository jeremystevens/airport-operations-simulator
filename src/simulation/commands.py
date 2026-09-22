from dataclasses import dataclass


@dataclass(frozen=True)
class RunwayEntryClearance:
    aircraft_id: str
    runway_name: str
    hold_node_id: str
    runway_entry_node_id: str
