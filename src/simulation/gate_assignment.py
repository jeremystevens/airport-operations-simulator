class GateAssignmentController:
    def find_gate(
        self,
        aircraft,
        airport,
    ):
        candidates = []

        for terminal in airport.terminals:
            for gate in terminal.gates:
                if gate.can_accept(aircraft):
                    candidates.append(gate)

        if not candidates:
            return None

        candidates.sort(
            key=lambda gate: (
                gate.position.distance_to(
                    aircraft.position
                ),
                gate.gate_id,
            )
        )

        return candidates[0]
