# Airport Operations Simulator

Airport Operations Simulator is a work-in-progress airport simulation game built in Python with Pygame.

The goal is to create a living airport where aircraft arrive, land, taxi to their gates, receive ground services, load passengers and cargo, push back, taxi to the runway, and depart again — while the airport continues operating around them.

Rather than scripting aircraft along predetermined animations, the project is being built around an actual simulation. Aircraft have destinations and states, taxi routes are calculated through the airport, gates can become occupied, runways can be busy, and controllers make decisions about how traffic should move.

The project is still early in development, but the airport is already starting to come alive.

## What Works So Far

The simulator currently includes a functional airport with:

- A runway with markings, thresholds, taxiway connections, and runway occupancy.
- A taxiway network with route finding.
- A terminal, apron, gates, and jet bridges.
- Different aircraft sizes and recognizable top-down aircraft graphics.
- Arriving and departing aircraft operating at the same time.
- Aircraft approaches, landings, rollout, and runway exits.
- Taxiing between runways and gates.
- Automatic gate assignment based on availability and aircraft size.
- Pushback operations with a working pushback tug.
- Takeoff rolls, liftoff, climb, and departure from the simulated world.
- Ground traffic control that prevents aircraft from trying to use the same narrow taxiway at the same time.
- Arriving aircraft receiving priority in certain taxiway conflicts while departing aircraft hold safely out of the way.
- Ground and Tower clearances for operations such as landing, taxiing, holding position, continuing taxi, lining up, and takeoff, all issued and validated through a shared controller/command pipeline rather than being applied directly.
- Aircraft turnaround operations at the gate, including deboarding, baggage unloading, fueling, catering, and boarding as real dependencies an aircraft has to wait on rather than a single fixed timer.
- A separate service-road network for airport ground vehicles, kept independent from the taxiway network aircraft use.
- A fully functional fuel truck: it is dispatched from its own depot when an aircraft begins servicing, drives the service-road network, breaks off to approach the aircraft at a position calculated from that aircraft's own size and orientation, connects, actually performs the fueling operation, then disconnects, returns home, and becomes available to service another aircraft.
- A baggage tractor towing a three-cart consist that dispatches from its own staging area, drives the service-road network with the carts trailing naturally through turns, and stages near the aircraft.
- Simulation speed controls for speeding up or slowing down airport operations.
- Camera movement and zoom controls for exploring the airport.

The first ground-service vehicle, the fuel truck, now performs its entire job for real: an aircraft's fuel requirement is only satisfied once the truck has physically reached it and finished fueling, and boarding cannot begin without that. Baggage handling is following the same path — the tractor and its carts can already reach the aircraft, with the physical baggage operation itself coming next.

## Current Airport

Development currently takes place at **Redwood International Airport (RWI)**, our test airport.

RWI gives us a controlled airport where new systems can be built and tested before we start generating larger and more complicated airports.

The long-term plan is not to have just one airport. Airport Operations Simulator is being designed to eventually support airports of different sizes and layouts, including small regional airports, international airports, cargo facilities, multi-runway airports, and much larger hubs.

Procedurally generated airports using seeds are also planned so that a particular airport layout can be recreated later.

## A Living Airport

One of the main goals of the project is to make the airport feel like a place that continues operating whether you are watching a particular aircraft or not.

Eventually an aircraft should be able to complete a full cycle:

**Approach → Landing → Taxi → Gate → Unload → Service → Board → Pushback → Taxi → Takeoff → Departure**

At the same time, other aircraft may be landing, waiting for a runway, taxiing in the opposite direction, receiving ground services, or preparing for departure.

Ground vehicles will also have their own jobs and routes instead of existing only as decoration.

## Air Traffic Control

Airport Operations Simulator is being designed with separate Ground and Tower operations.

Controllers can issue instructions such as:

- Cleared to land
- Taxi to gate
- Hold position
- Continue taxi
- Line up and wait
- Cleared for takeoff

Aircraft still have to obey the physical rules of the simulation. A clearance does not allow an aircraft to drive through another airplane or use an occupied runway.

In the future, these same events are planned to produce spoken pilot and controller radio traffic using text-to-speech.

The simulator is also being designed so that airport controllers can eventually be controlled in different ways. The normal simulator will always be able to operate the airport itself, while future options may allow an AI controller or even the player to take over certain positions.

## Planned Features

There is a lot more planned for the project, including:

- Baggage tractors that actually load and unload baggage at the aircraft, plus functional catering trucks, buses, maintenance vehicles, and emergency vehicles.
- Passenger, baggage, and cargo movement.
- Cargo terminals and cargo-only aircraft operations.
- More aircraft types, including regional aircraft, widebodies, private aircraft, cargo aircraft, and very large aircraft.
- Multiple terminals and much larger airports.
- Multiple and intersecting runways.
- Weather, wind, day/night operations, and airport lighting.
- More detailed Ground and Tower control.
- Pilot and controller radio voices.
- Airport statistics, flight boards, passenger totals, cargo totals, delays, and graphs.
- Saved airports and airport history.
- A title screen for selecting, creating, and continuing airports.
- Seed-based airport generation.
- Different airport sizes and styles.
- Surrounding terrain, roads, neighborhoods, water, forests, and other scenery.
- Aircraft approaching and departing through the surrounding world.
- A remote web dashboard for watching airport operations from another device.
- Optional AI-controlled airport operations.

The long-term goal is for airports to become busy systems where aircraft, passengers, cargo, vehicles, gates, runways, and controllers all affect one another.

## Development Status

Airport Operations Simulator is under active development.

Right now development is focused on **aircraft turnaround and ground-service vehicles**. Aircraft can already complete arrivals, taxi to dynamically assigned gates, go through their turnaround process, and departing traffic can operate at the same time.

Ground-service vehicles are being migrated one at a time from simulated timers to actually performing their jobs. The fuel truck was the first to make this transition and now handles its entire task for real, from dispatch through fueling to returning home. The baggage tractor and its cart consist are partway through the same migration — they can already dispatch and drive to the aircraft, and giving them the same real ownership of the baggage task that the fuel truck has for fueling is the next step, followed by catering.

Expect things to change frequently while the simulation systems are being built.

## Running the Project

Python and Pygame are required.

Clone the repository:

```bash
git clone https://github.com/jeremystevens/airport-operations-simulator.git
cd airport-operations-simulator
```

Create a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

Install the requirements:

```bash
pip install -r requirements.txt
```

Run the simulator:

```bash
python main.py
```

## Controls

Current development controls include:

- **WASD / Arrow Keys** — Move the camera
- **Mouse Wheel** — Zoom in and out
- **[** — Slow down the simulation
- **]** — Speed up the simulation

Additional controls and user interface features will be added as development continues.

## Why I'm Building It

I've always liked simulations where you can watch lots of independent systems interact with each other.

Airports are especially interesting because even something as simple as getting one airplane from a runway to a gate involves runways, taxiways, gates, controllers, vehicles, passengers, timing, and other aircraft.

This project is an attempt to build that kind of airport from the ground up and see how far the simulation can go.

It's a learning project, an experiment, and hopefully eventually a pretty fun airport to watch.

## Contributing

The project is still changing quickly, so the internal code and structure are likely to continue evolving.

Contributions, ideas, bug reports, and suggestions are welcome.

A more detailed developer guide covering the simulator's architecture and technical systems is planned as the project becomes more established.

## License

A license has not been selected yet.
