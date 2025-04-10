from src.EKF_1D.data_prac import log_to_nplist
from run_ekf import run_ekf
from plot_result import plot_results

# Параметры
dt = 0.1  # Временной шаг (в секундах)
process_noise = 0.01  # Шум процесса
measurement_noise = 10.0  # Шум измерений
initial_state = [0.0, 0.1]  # Начальное состояние [x, vx]
anchor_x = 0.0  # Координата anchor по x

# Массив измерений расстояний
measured_distances = log_to_nplist("../../data/data_1D/uwb/rotate.log",
                                   json_address="../../data/data_1D/uwb/rotate.json")

# Запуск EKF
estimated_positions, estimated_velocities = (
    run_ekf(measured_distances, dt, process_noise, measurement_noise, initial_state, anchor_x))

# Визуализация результатов
plot_results(measured_distances, estimated_positions, estimated_velocities, dt)
