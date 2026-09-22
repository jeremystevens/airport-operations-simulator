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
    ):
        self.segment_id = segment_id

        self.start_node = start_node
        self.end_node = end_node

        self.name = name
        self.width = width

        self.occupied = False

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
