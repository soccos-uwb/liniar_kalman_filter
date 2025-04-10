import numpy as np
from ekf_uwb import EKF_UWB_3D
from scipy.interpolate import interp1d


def run_filter_pipeline(raw_data, anchors, initial_state, dt=0.1, process_noise=1, measurement_noise=5):
    distance_by_anchor = {aid: {} for aid in range(1, 4)}
    for t, aid, dist in raw_data:
        seconds = t.total_seconds()
        distance_by_anchor[aid][seconds] = dist

    min_time = min(min(anchor_times.keys()) for anchor_times in distance_by_anchor.values())
    max_time = max(max(anchor_times.keys()) for anchor_times in distance_by_anchor.values())
    regular_times = np.arange(min_time, max_time, dt)

    # Интерполяция
    interp_distances = {}
    for aid in range(1, 4):
        t_vals = np.array(sorted(distance_by_anchor[aid].keys()))
        d_vals = np.array([distance_by_anchor[aid][t] for t in t_vals])
        f_interp = interp1d(t_vals, d_vals, kind='linear', bounds_error=False, fill_value="extrapolate")
        interp_distances[aid] = f_interp(regular_times)

    ekf = EKF_UWB_3D(dt=dt, process_noise=process_noise, measurement_noise=measurement_noise,
                     initial_state=initial_state, anchors=anchors)

    positions = []
    filtered_distances = [[] for _ in range(3)]

    for i in range(len(regular_times)):
        ekf.predict()
        current_measurements = [interp_distances[aid][i] for aid in range(1, 4)]
        ekf.update(current_measurements)
        state = ekf.get_state()
        positions.append(state)

        for j, (ax, ay, az) in enumerate(anchors):
            dist = np.linalg.norm([state[0] - ax, state[2] - ay, state[4] - az])
            filtered_distances[j].append(dist)

    return positions, regular_times, interp_distances, filtered_distances, distance_by_anchor