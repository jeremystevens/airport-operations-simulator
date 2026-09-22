class Airport:
    def __init__(
        self,
        name,
        code,
        world_width,
        world_height,
    ):
        self.name = name
        self.code = code

        self.world_width = world_width
        self.world_height = world_height

    def __repr__(self):
        return (
            f"Airport("
            f"name='{self.name}', "
            f"code='{self.code}', "
            f"world={self.world_width}x{self.world_height}"
            f")"
        )
