from src.aircraft.aircraft import AircraftSize

# Physical footprint used for ground-conflict geometry (world units).
# These mirror AircraftRenderer.AIRCRAFT_PROFILES' length/wingspan values
# so simulation and rendering agree on aircraft size. They're duplicated
# here rather than imported from the renderer because simulation code
# should not depend on rendering modules; if the renderer's numbers ever
# change, update both.
AIRCRAFT_DIMENSIONS = {
    AircraftSize.LIGHT: {
        "length": 150.0,
        "wingspan": 190.0,
    },
    AircraftSize.BUSINESS: {
        "length": 210.0,
        "wingspan": 190.0,
    },
    AircraftSize.REGIONAL: {
        "length": 250.0,
        "wingspan": 235.0,
    },
    AircraftSize.NARROWBODY: {
        "length": 300.0,
        "wingspan": 280.0,
    },
    AircraftSize.WIDEBODY: {
        "length": 390.0,
        "wingspan": 380.0,
    },
    AircraftSize.SUPERHEAVY: {
        "length": 430.0,
        "wingspan": 440.0,
    },
}


def get_aircraft_dimensions(aircraft):
    return AIRCRAFT_DIMENSIONS.get(
        aircraft.size,
        AIRCRAFT_DIMENSIONS[AircraftSize.NARROWBODY],
    )
