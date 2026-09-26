from dataclasses import dataclass
from enum import Enum

from src.aircraft.aircraft import AircraftState


class ServiceType(Enum):
    BAGGAGE = "baggage"
    FUEL = "fuel"
    CATERING = "catering"


class ServiceStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETE = "complete"


@dataclass
class ServiceTask:
    service_type: ServiceType
    status: ServiceStatus = ServiceStatus.PENDING
    elapsed: float = 0.0

    @property
    def complete(self):
        return self.status == ServiceStatus.COMPLETE


# Temporary development durations, standing in for a real ground-service
# vehicle performing the task -- see 2.5c.
SERVICE_DURATIONS = {
    ServiceType.BAGGAGE: 8.0,
    ServiceType.FUEL: 12.0,
    ServiceType.CATERING: 10.0,
}


def get_service_task(aircraft, service_type):
    for task in aircraft.service_tasks:
        if task.service_type == service_type:
            return task

    return None


def all_services_complete(aircraft):
    return bool(aircraft.service_tasks) and all(
        task.complete for task in aircraft.service_tasks
    )


class ServiceTaskController:
    """Temporary stand-in for real ground-service vehicles (2.5c). Runs
    every required ServiceTask concurrently during SERVICING using sim_dt,
    so service duration scales with simulation speed like everything
    else."""

    def update(self, aircraft, dt):
        if aircraft.state != AircraftState.SERVICING:
            return []

        events = []

        for task in aircraft.service_tasks:
            if task.status == ServiceStatus.PENDING:
                task.status = ServiceStatus.IN_PROGRESS
                events.append(("started", task.service_type))

            if task.status == ServiceStatus.IN_PROGRESS:
                task.elapsed += dt

                if task.elapsed >= SERVICE_DURATIONS[task.service_type]:
                    task.status = ServiceStatus.COMPLETE
                    events.append(("complete", task.service_type))

        return events
