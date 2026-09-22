class SimulationClock:
    def __init__(self, start_hour=6, start_minute=0):
        self.seconds_per_sim_minute = 1.0

        self.total_minutes = (
            start_hour * 60
            + start_minute
        )

        self.accumulator = 0.0
        self.paused = False

    def update(self, dt):
        if self.paused:
            return

        self.accumulator += dt

        while self.accumulator >= self.seconds_per_sim_minute:
            self.accumulator -= self.seconds_per_sim_minute
            self.total_minutes += 1

    @property
    def hour(self):
        return (self.total_minutes // 60) % 24

    @property
    def minute(self):
        return self.total_minutes % 60

    @property
    def day(self):
        return self.total_minutes // (24 * 60) + 1

    def get_time_string(self):
        return f"{self.hour:02d}:{self.minute:02d}"

    def toggle_pause(self):
        self.paused = not self.paused
