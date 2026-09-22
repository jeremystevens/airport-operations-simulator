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

    def add_runway(self, runway):
        self.runways.append(runway)

    def __repr__(self):
        return (
            f"Airport("
            f"name='{self.name}', "
            f"code='{self.code}', "
            f"world={self.world_width}x{self.world_height}, "
            f"property={self.property_width}x{self.property_height}"
            f")"
        )
