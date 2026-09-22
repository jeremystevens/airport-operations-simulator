import heapq


def find_taxiway_path(airport, start_node_id, end_node_id):
    """Find the shortest taxiway path between two nodes."""

    if start_node_id not in airport.taxiway_nodes:
        raise ValueError(f"Unknown start node: {start_node_id}")

    if end_node_id not in airport.taxiway_nodes:
        raise ValueError(f"Unknown end node: {end_node_id}")

    adjacency = {
        node_id: []
        for node_id in airport.taxiway_nodes
    }

    for segment in airport.taxiway_segments:
        start_id = segment.start_node.node_id
        end_id = segment.end_node.node_id

        adjacency[start_id].append(
            (end_id, segment.length)
        )

        adjacency[end_id].append(
            (start_id, segment.length)
        )

    distances = {
        node_id: float("inf")
        for node_id in airport.taxiway_nodes
    }

    previous = {}

    distances[start_node_id] = 0.0

    queue = [
        (0.0, start_node_id)
    ]

    while queue:
        current_distance, current_id = heapq.heappop(queue)

        if current_distance > distances[current_id]:
            continue

        if current_id == end_node_id:
            break

        for neighbor_id, segment_length in adjacency[current_id]:
            new_distance = current_distance + segment_length

            if new_distance < distances[neighbor_id]:
                distances[neighbor_id] = new_distance
                previous[neighbor_id] = current_id

                heapq.heappush(
                    queue,
                    (new_distance, neighbor_id),
                )

    if distances[end_node_id] == float("inf"):
        return []

    path = []
    current_id = end_node_id

    while current_id != start_node_id:
        path.append(current_id)
        current_id = previous[current_id]

    path.append(start_node_id)
    path.reverse()

    return path
