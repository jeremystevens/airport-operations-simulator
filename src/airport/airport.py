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

    def add_runway(self, runway):
        self.runways.append(runway)

    def add_taxiway_node(self, node):
        self.taxiway_nodes[node.node_id] = node

    def add_taxiway_segment(self, segment):
        self.taxiway_segments.append(segment)

    def __repr__(self):
        return (
            f"Airport("
            f"name='{self.name}', "
            f"code='{self.code}', "
            f"world={self.world_width}x{self.world_height}, "
            f"property={self.property_width}x{self.property_height}"
            f")"
        )
