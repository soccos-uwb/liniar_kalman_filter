from parser import parse_data
from run_ekf_3D import run_filter_pipeline
from plot_result import visualize_results


dt = 0.1
anchor_ids = [1, 2, 3]
anchors = [(0, 0, 0), (2.6, 0.8, -0.7), (-0.4, 1.3, 0.35)]
initial_state = [1, 0, 1, 0, 1, 0]  # x, vx, y, vy, z, vz

parsed_data = parse_data("../../data/data_3D/moving5.log")
positions, regular_times, interp_distances, filtered_distances, distance_by_anchor = run_filter_pipeline(
    parsed_data, anchors, initial_state, dt=dt)

visualize_results(positions, regular_times, interp_distances, filtered_distances, distance_by_anchor)
