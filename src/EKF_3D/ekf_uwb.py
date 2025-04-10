import numpy as np


class EKF_UWB_3D:
    def __init__(self, dt: float, process_noise: float, measurement_noise: float,
                 initial_state: list[float], anchors: list[tuple[float, float, float]]):
        self.dt = dt
        self.x = np.array(initial_state, dtype=float)
        self.P = np.eye(6) * 100
        self.Q = np.eye(6) * process_noise
        self.R = np.eye(3) * measurement_noise
        self.anchors = np.array(anchors)

    def predict(self):
        F = np.array([[1, self.dt, 0, 0, 0, 0],
                      [0, 1, 0, 0, 0, 0],
                      [0, 0, 1, self.dt, 0, 0],
                      [0, 0, 0, 1, 0, 0],
                      [0, 0, 0, 0, 1, self.dt],
                      [0, 0, 0, 0, 0, 1]])

        self.x = F @ self.x
        self.P = F @ self.P @ F.T + self.Q

    def update(self, measured_distances):
        x, vx, y, vy, z, vz = self.x
        h = np.array([
            np.sqrt((x - ax) ** 2 + (y - ay) ** 2 + (z - az) ** 2)
            for ax, ay, az in self.anchors
        ])

        epsilon = 1e-6
        H = np.array([
            [(x - ax) / (hi + epsilon), 0, (y - ay) / (hi + epsilon), 0, (z - az) / (hi + epsilon), 0]
            for (ax, ay, az), hi in zip(self.anchors, h)
        ])

        y_residual = np.array(measured_distances) - h
        S = H @ self.P @ H.T + self.R
        K = self.P @ H.T @ np.linalg.inv(S) if np.linalg.det(S) != 0 else np.zeros((6, 3))

        self.x += (K @ y_residual).flatten()
        self.P = (np.eye(6) - K @ H) @ self.P

    def get_state(self):
        return self.x.copy()