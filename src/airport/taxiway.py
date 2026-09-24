import pygame


class TaxiwayNode:
    def __init__(self, node_id, position):
        self.node_id = node_id
        self.position = pygame.Vector2(position)

    def __repr__(self):
        return (
            f"TaxiwayNode("
            f"id='{self.node_id}', "
            f"position={tuple(self.position)}"
            f")"
        )


class TaxiwaySegment:
    def __init__(
        self,
        segment_id,
        start_node,
        end_node,
        name,
        width=70,
        render_surface=True,
        conflict_group=None,
    ):
        self.segment_id = segment_id

        self.start_node = start_node
        self.end_node = end_node

        self.name = name
        self.width = width
        self.render_surface = render_surface
        self.conflict_group = conflict_group

        self.occupied = False
        self.occupied_by = None

    def is_available_for(self, aircraft_id):
        return (
            not self.occupied
            or self.occupied_by == aircraft_id
        )

    def reserve(self, aircraft_id):
        if not self.is_available_for(aircraft_id):
            return False

        self.occupied = True
        self.occupied_by = aircraft_id
        return True

    def release(self, aircraft_id):
        if self.occupied_by != aircraft_id:
            return False

        self.occupied = False
        self.occupied_by = None
        return True

    @property
    def length(self):
        return self.start_node.position.distance_to(
            self.end_node.position
        )

    def __repr__(self):
        return (
            f"TaxiwaySegment("
            f"id='{self.segment_id}', "
            f"name='{self.name}', "
            f"start='{self.start_node.node_id}', "
            f"end='{self.end_node.node_id}', "
            f"length={self.length:.1f}"
            f")"
        )
