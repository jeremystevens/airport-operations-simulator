class Airport:
    def __init__(
        self,
        name,
        code,
        world_width,
        world_height,
        property_width,
        property_height,
    ):
        self.name = name
        self.code = code

        self.world_width = world_width
        self.world_height = world_height

        self.property_width = property_width
        self.property_height = property_height

        self.runways = []

        self.taxiway_nodes = {}
        self.taxiway_segments = []

        self.terminals = []

        self.aprons = []

        self.aircraft = []

        self.ground_vehicles = []

        self.service_nodes = {}
        self.service_segments = []

        self.taxiway_conflict_owners = {}

    def add_runway(self, runway):
        self.runways.append(runway)

    def add_aircraft(self, aircraft):
        self.aircraft.append(aircraft)

    def add_ground_vehicle(self, vehicle):
        self.ground_vehicles.append(vehicle)

    def add_taxiway_node(self, node):
        self.taxiway_nodes[node.node_id] = node

    def add_taxiway_segment(self, segment):
        self.taxiway_segments.append(segment)

    def get_taxiway_segment_between(
        self,
        node_a_id,
        node_b_id,
    ):
        for segment in self.taxiway_segments:
            ids = {
                segment.start_node.node_id,
                segment.end_node.node_id,
            }

            if ids == {
                node_a_id,
                node_b_id,
            }:
                return segment

        return None

    def get_taxiway_conflict_owner(
        self,
        group_id,
    ):
        return self.taxiway_conflict_owners.get(
            group_id
        )

    def reserve_taxiway_conflict(
        self,
        group_id,
        aircraft_id,
    ):
        owner = self.get_taxiway_conflict_owner(
            group_id
        )

        if owner is not None and owner != aircraft_id:
            return False

        self.taxiway_conflict_owners[group_id] = (
            aircraft_id
        )

        return True

    def release_taxiway_conflict(
        self,
        group_id,
        aircraft_id,
    ):
        owner = self.get_taxiway_conflict_owner(
            group_id
        )

        if owner != aircraft_id:
            return False

        del self.taxiway_conflict_owners[group_id]
        return True

    def add_terminal(self, terminal):
        self.terminals.append(terminal)

    def add_apron(self, apron):
        self.aprons.append(apron)

    def add_service_node(self, node):
        self.service_nodes[node.node_id] = node

    def add_service_segment(self, segment):
        self.service_segments.append(segment)

    def __repr__(self):
        return (
            f"Airport("
            f"name='{self.name}', "
            f"code='{self.code}', "
            f"world={self.world_width}x{self.world_height}, "
            f"property={self.property_width}x{self.property_height}"
            f")"
        )
