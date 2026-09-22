# Airport Operations Simulator

A top-down airport operations simulation built with Python and Pygame.

The project aims to simulate a living airport where aircraft arrive, land,
taxi, park at gates or cargo stands, receive ground services, push back,
depart, and contribute to persistent airport statistics.

## Current Status

Early development — Phase 0: Project Foundation.

Currently implemented:

- Pygame application foundation
- 1280x720 simulation window
- 60 FPS game loop
- Clean application shutdown

## Planned Features

- Multiple airport layouts and sizes
- Passenger and cargo aircraft
- Functional gates and cargo stands
- Aircraft taxi routing
- Ground service vehicles
- Passenger, baggage, and cargo simulation
- Airport operations HUD and dashboard
- Persistent airport data using SQLite
- Seeded procedural airport generation
- Dynamic weather and time of day
- ATC and pilot text-to-speech radio communications
- Rule-based and eventual AI airport controllers
- Optional remote web dashboard for monitoring a running airport

## Technology

- Python
- Pygame
- SQLite (planned)

## Running

Create and activate a Python virtual environment, install the dependencies,
then run:

```bash
pip install -r requirements.txt
python main.py

