import math

import pygame

from src.aircraft.aircraft import (
    Aircraft,
    AircraftOperation,
    AircraftSize,
    AircraftState,
)
from src.airport.airport import Airport
from src.airport.runway import Runway
from src.airport.apron import Apron
from src.airport.gate import Gate
from src.airport.service_road import (
    ServiceNode,
    ServiceSegment,
)
from src.airport.taxiway import TaxiwayNode, TaxiwaySegment
from src.airport.terminal import Terminal
from src.rendering.camera import Camera
from src.rendering.world_renderer import WorldRenderer
from src.simulation.aircraft_movement import (
    AircraftMovementController,
)
from src.simulation.clock import SimulationClock
from src.simulation.ground_vehicle_movement import (
    GroundVehicleMovementController,
)
from src.simulation.pathfinding import find_taxiway_path
from src.simulation.pushback import PushbackController
from src.simulation.service_pathfinding import (
    find_service_path,
)
from src.vehicles.ground_vehicle import (
    GroundVehicle,
    GroundVehicleState,
    GroundVehicleType,
)


WIDTH = 1280
HEIGHT = 720
FPS = 60


def get_tug_connect_position(
    aircraft,
    offset=215.0,
):
    heading_radians = math.radians(
        aircraft.heading
    )

    forward = pygame.Vector2(
        math.sin(heading_radians),
        -math.cos(heading_radians),
    )

    return (
        pygame.Vector2(aircraft.position)
        + forward * offset
    )


def main():
    pygame.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Airport Operations Simulator")

    clock = pygame.time.Clock()

    camera = Camera(WIDTH, HEIGHT)
    world_renderer = WorldRenderer()

    simulation_clock = SimulationClock(6, 0)

    aircraft_movement = AircraftMovementController(
        taxi_speed=90.0
    )

    pushback_controller = PushbackController(
        pushback_speed=35.0
    )

    ground_vehicle_movement = (
        GroundVehicleMovementController()
    )

    airport = Airport(
        name="Redwood International Airport",
        code="RWI",
        world_width=12000,
        world_height=8000,
        property_width=7000,
        property_height=4500,
    )

    runway_09_27 = Runway(
        name="09/27",
        center=(0, 0),
        length=5200,
        width=180,
        heading=90,
    )

    airport.add_runway(runway_09_27)

    alpha_west = TaxiwayNode("A_WEST", (-2500, 500))
    alpha_1 = TaxiwayNode("A1", (-2350, 500))
    alpha_2 = TaxiwayNode("A2", (-900, 500))
    alpha_center = TaxiwayNode("A_CENTER", (0, 500))
    alpha_3 = TaxiwayNode("A3", (900, 500))
    alpha_4 = TaxiwayNode("A4", (2350, 500))
    alpha_east = TaxiwayNode("A_EAST", (2500, 500))

    for node in (
        alpha_west,
        alpha_1,
        alpha_2,
        alpha_center,
        alpha_3,
        alpha_4,
        alpha_east,
    ):
        airport.add_taxiway_node(node)

    runway_a1 = TaxiwayNode("RWY_A1", (-2350, 90))
    runway_a2 = TaxiwayNode("RWY_A2", (-700, 90))
    runway_a3 = TaxiwayNode("RWY_A3", (700, 90))
    runway_a4 = TaxiwayNode("RWY_A4", (2350, 90))

    for node in (
        runway_a1,
        runway_a2,
        runway_a3,
        runway_a4,
    ):
        airport.add_taxiway_node(node)

    alpha_segments = [
        TaxiwaySegment(
            "A_01",
            alpha_west,
            alpha_1,
            "A",
        ),
        TaxiwaySegment(
            "A_02",
            alpha_1,
            alpha_2,
            "A",
        ),
        TaxiwaySegment(
            "A_03",
            alpha_2,
            alpha_center,
            "A",
        ),
        TaxiwaySegment(
            "A_03B",
            alpha_center,
            alpha_3,
            "A",
        ),
        TaxiwaySegment(
            "A_04",
            alpha_3,
            alpha_4,
            "A",
        ),
        TaxiwaySegment(
            "A_05",
            alpha_4,
            alpha_east,
            "A",
        ),
    ]

    for segment in alpha_segments:
        airport.add_taxiway_segment(segment)

    runway_connectors = [
        TaxiwaySegment(
            "A1_RWY",
            alpha_1,
            runway_a1,
            "A1",
        ),
        TaxiwaySegment(
            "A2_RWY",
            alpha_2,
            runway_a2,
            "A2",
        ),
        TaxiwaySegment(
            "A3_RWY",
            alpha_3,
            runway_a3,
            "A3",
        ),
        TaxiwaySegment(
            "A4_RWY",
            alpha_4,
            runway_a4,
            "A4",
        ),
    ]

    for segment in runway_connectors:
        airport.add_taxiway_segment(segment)

    terminal_1 = Terminal(
        terminal_id="T1",
        name="Terminal 1",
        center=(0, 1500),
        width=2200,
        height=500,
    )

    airport.add_terminal(terminal_1)

    terminal_1_gates = [
        Gate(
            "A1",
            "T1",
            (-750, 1150),
            max_aircraft_size=AircraftSize.NARROWBODY,
        ),
        Gate(
            "A2",
            "T1",
            (-250, 1150),
            max_aircraft_size=AircraftSize.WIDEBODY,
        ),
        Gate(
            "A3",
            "T1",
            (250, 1150),
            max_aircraft_size=AircraftSize.WIDEBODY,
        ),
        Gate(
            "A4",
            "T1",
            (750, 1150),
            max_aircraft_size=AircraftSize.NARROWBODY,
        ),
    ]

    for gate in terminal_1_gates:
        terminal_1.add_gate(gate)

    rw428 = Aircraft(
        flight_id="RW428",
        aircraft_type="Aero 320",
        size=AircraftSize.NARROWBODY,
        operation=AircraftOperation.PASSENGER,
        position=(-750, 1150),
        heading=180,
        passenger_capacity=186,
        passengers=164,
    )

    rw428.assign_gate(terminal_1_gates[0])
    rw428.set_state(AircraftState.AT_GATE)

    terminal_1_gates[0].occupy(rw428)

    airport.add_aircraft(rw428)

    tug_01 = GroundVehicle(
        vehicle_id="TUG-01",
        vehicle_type=GroundVehicleType.PUSHBACK_TUG,
        position=(-850, 1200),
        heading=180,
    )

    airport.add_ground_vehicle(tug_01)

    rw901 = Aircraft(
        flight_id="RW901",
        aircraft_type="Aero 350",
        size=AircraftSize.WIDEBODY,
        operation=AircraftOperation.PASSENGER,
        position=(250, 1150),
        heading=180,
        passenger_capacity=325,
        passengers=287,
    )

    rw901.assign_gate(terminal_1_gates[2])
    rw901.set_state(AircraftState.AT_GATE)

    terminal_1_gates[2].occupy(rw901)

    airport.add_aircraft(rw901)

    apron_center = TaxiwayNode(
        "APRON_CENTER",
        (0, 800),
    )

    gate_a1_node = TaxiwayNode(
        "GATE_A1",
        (-750, 850),
    )

    gate_a2_node = TaxiwayNode(
        "GATE_A2",
        (-250, 850),
    )

    gate_a3_node = TaxiwayNode(
        "GATE_A3",
        (250, 850),
    )

    gate_a4_node = TaxiwayNode(
        "GATE_A4",
        (750, 850),
    )

    for node in (
        apron_center,
        gate_a1_node,
        gate_a2_node,
        gate_a3_node,
        gate_a4_node,
    ):
        airport.add_taxiway_node(node)

    airport.add_taxiway_segment(
        TaxiwaySegment(
            "APRON_ENTRY",
            alpha_center,
            apron_center,
            "APRON",
            width=60,
        )
    )

    apron_segments = [
        TaxiwaySegment(
            "APRON_A1_A2",
            gate_a1_node,
            gate_a2_node,
            "APRON",
            width=60,
        ),
        TaxiwaySegment(
            "APRON_A2_CENTER",
            gate_a2_node,
            apron_center,
            "APRON",
            width=60,
        ),
        TaxiwaySegment(
            "APRON_CENTER_A3",
            apron_center,
            gate_a3_node,
            "APRON",
            width=60,
        ),
        TaxiwaySegment(
            "APRON_A3_A4",
            gate_a3_node,
            gate_a4_node,
            "APRON",
            width=60,
        ),
    ]

    for segment in apron_segments:
        airport.add_taxiway_segment(segment)

    gate_stop_nodes = [
        TaxiwayNode("A1_STOP", (-750, 1150)),
        TaxiwayNode("A2_STOP", (-250, 1150)),
        TaxiwayNode("A3_STOP", (250, 1150)),
        TaxiwayNode("A4_STOP", (750, 1150)),
    ]

    for node in gate_stop_nodes:
        airport.add_taxiway_node(node)

    gate_connections = [
        TaxiwaySegment(
            "GATE_A1_LEAD",
            gate_a1_node,
            gate_stop_nodes[0],
            "GATE",
            width=40,
        ),
        TaxiwaySegment(
            "GATE_A2_LEAD",
            gate_a2_node,
            gate_stop_nodes[1],
            "GATE",
            width=40,
        ),
        TaxiwaySegment(
            "GATE_A3_LEAD",
            gate_a3_node,
            gate_stop_nodes[2],
            "GATE",
            width=40,
        ),
        TaxiwaySegment(
            "GATE_A4_LEAD",
            gate_a4_node,
            gate_stop_nodes[3],
            "GATE",
            width=40,
        ),
    ]

    for segment in gate_connections:
        airport.add_taxiway_segment(segment)

    terminal_1_apron = Apron(
        apron_id="T1_APRON",
        name="Terminal 1 Apron",
        center=(0, 1050),
        width=2800,
        height=1000,
        apron_type="passenger",
    )

    airport.add_apron(terminal_1_apron)

    service_west = ServiceNode(
        "SERVICE_WEST",
        (-1050, 1225),
    )

    service_a1 = ServiceNode(
        "SERVICE_A1",
        (-850, 1225),
    )

    service_a2 = ServiceNode(
        "SERVICE_A2",
        (-350, 1225),
    )

    service_a3 = ServiceNode(
        "SERVICE_A3",
        (350, 1225),
    )

    service_a4 = ServiceNode(
        "SERVICE_A4",
        (850, 1225),
    )

    service_east = ServiceNode(
        "SERVICE_EAST",
        (1050, 1225),
    )

    for node in (
        service_west,
        service_a1,
        service_a2,
        service_a3,
        service_a4,
        service_east,
    ):
        airport.add_service_node(node)

    service_segments = [
        ServiceSegment(
            "SERVICE_01",
            service_west,
            service_a1,
        ),
        ServiceSegment(
            "SERVICE_02",
            service_a1,
            service_a2,
        ),
        ServiceSegment(
            "SERVICE_03",
            service_a2,
            service_a3,
        ),
        ServiceSegment(
            "SERVICE_04",
            service_a3,
            service_a4,
        ),
        ServiceSegment(
            "SERVICE_05",
            service_a4,
            service_east,
        ),
    ]

    for segment in service_segments:
        airport.add_service_segment(segment)

    tug_a1_home = ServiceNode(
        "TUG_A1_HOME",
        (-850, 1200),
    )

    tug_a1_connect = ServiceNode(
        "TUG_A1_CONNECT",
        (-750, 1225),
    )

    for node in (
        tug_a1_home,
        tug_a1_connect,
    ):
        airport.add_service_node(node)

    airport.add_service_segment(
        ServiceSegment(
            "TUG_A1_HOME_SPUR",
            service_a1,
            tug_a1_home,
        )
    )

    airport.add_service_segment(
        ServiceSegment(
            "TUG_A1_CONNECT_SPUR",
            service_a1,
            tug_a1_connect,
        )
    )

    dispatch_route = find_service_path(
        airport,
        "TUG_A1_HOME",
        "TUG_A1_CONNECT",
    )

    tug_01.assign_route(
        dispatch_route
    )

    tug_01.assign_aircraft(rw428)
    tug_01.active = True
    tug_01.state = (
        GroundVehicleState.DISPATCHED
    )

    font = pygame.font.Font(None, 28)

    running = True

    while running:
        dt = clock.tick(FPS) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            camera.handle_event(event)

        camera.update(dt)

        simulation_clock.update(dt)

        if tug_01.state == GroundVehicleState.DISPATCHED:

            if tug_01.has_route:
                route_complete = (
                    ground_vehicle_movement.update_route(
                        tug_01,
                        airport,
                        dt,
                    )
                )

                if route_complete:
                    tug_01.final_target = (
                        get_tug_connect_position(
                            rw428
                        )
                    )

            elif tug_01.final_target is not None:
                connected = (
                    ground_vehicle_movement.move_toward(
                        tug_01,
                        tug_01.final_target,
                        dt,
                    )
                )

                if connected:
                    tug_01.final_target = None

                    pushback_controller.start(
                        rw428,
                        terminal_1_gates[0],
                        airport.taxiway_nodes["GATE_A1"],
                        tug_01,
                    )

                    tug_01.state = (
                        GroundVehicleState.PUSHING
                    )

        if tug_01.state == GroundVehicleState.PUSHING:
            pushback_complete = (
                pushback_controller.update(
                    rw428,
                    airport,
                    tug_01,
                    dt,
                )
            )

            if pushback_complete:
                terminal_1_gates[0].release()

                tug_01.clear_assignment()
                tug_01.clear_route()

                tug_01.final_target = (
                    airport.service_nodes[
                        "TUG_A1_CONNECT"
                    ].position
                )

                tug_01.state = (
                    GroundVehicleState.RETURNING
                )

                rw428_departure_route = (
                    find_taxiway_path(
                        airport,
                        "GATE_A1",
                        "RWY_A1",
                    )
                )

                rw428.assign_route(
                    rw428_departure_route
                )

                rw428.set_state(
                    AircraftState.TAXI_OUT
                )

        if tug_01.state == GroundVehicleState.RETURNING:

            if tug_01.final_target is not None:
                reached_service_lane = (
                    ground_vehicle_movement.move_toward(
                        tug_01,
                        tug_01.final_target,
                        dt,
                    )
                )

                if reached_service_lane:
                    tug_01.final_target = None

                    return_route = (
                        find_service_path(
                            airport,
                            "TUG_A1_CONNECT",
                            "TUG_A1_HOME",
                        )
                    )

                    tug_01.assign_route(
                        return_route
                    )

            elif tug_01.has_route:
                returned = (
                    ground_vehicle_movement.update_route(
                        tug_01,
                        airport,
                        dt,
                    )
                )

                if returned:
                    tug_01.state = (
                        GroundVehicleState.PARKED
                    )

                    tug_01.active = False

        aircraft_movement.update(
            rw428,
            airport,
            dt,
        )

        screen.fill((20, 24, 28))

        world_renderer.draw(screen, camera, airport)

        airport_text = font.render(
            f"{airport.code} - {airport.name.upper()}",
            True,
            (220, 225, 230),
        )

        time_text = font.render(
            f"DAY {simulation_clock.day}  |  {simulation_clock.get_time_string()}",
            True,
            (180, 190, 200),
        )

        screen.blit(airport_text, (20, 20))
        screen.blit(time_text, (20, 50))

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
