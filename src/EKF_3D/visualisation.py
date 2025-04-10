import numpy as np
import matplotlib.pyplot as plt


def visualize_results(positions, regular_times, interp_distances, filtered_distances, raw_distances_by_anchor):
    pos = np.array(positions)

    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111, projection='3d')
    ax.plot(pos[:, 0], pos[:, 2], pos[:, 4], label='EKF Trajectory', color='blue')
    ax.set_title("EKF 3D Trajectory")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    ax.legend()
    plt.tight_layout()
    plt.savefig("../../data/data_3D/plt_3D.png")
    plt.show()

    for i in range(3):
        fig, ax2 = plt.subplots(figsize=(8, 4))

        # Interpolated data
        ax2.plot(regular_times, interp_distances[i + 1], label=f"Anchor {i + 1} Interpolated", alpha=0.7)

        # Filtered data
        ax2.plot(regular_times, filtered_distances[i], label=f"Anchor {i + 1} Filtered", linewidth=2)

        # Raw data
        raw_times = sorted(raw_distances_by_anchor[i + 1].keys())
        raw_vals = [raw_distances_by_anchor[i + 1][t] for t in raw_times]
        ax2.scatter(raw_times, raw_vals, label=f"Anchor {i + 1} Raw", color='black', s=10, alpha=0.6, marker='x')

        ax2.set_xlabel("Time (s)")
        ax2.set_ylabel("Distance (m)")
        ax2.legend()
        ax2.set_title(f"Distance to Anchor {i + 1}")
        plt.tight_layout()
        plt.savefig(f"../../data/data_3D/plt_anchor_{i+1}.png")
        plt.show()
