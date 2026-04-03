import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter


def moving_average(data, window_size=5):
    if window_size < 1:
        raise ValueError("window_size must be >= 1")
    kernel = np.ones(window_size) / window_size
    return np.convolve(data, kernel, mode="same")


def simple_kalman_filter_1d(measurements, process_variance=1e-3, measurement_variance=1e-1):
    """
    Very simple 1D Kalman filter for demonstration.
    """
    n = len(measurements)
    estimates = np.zeros(n)

    x_est = measurements[0]
    p_est = 1.0

    for i, z in enumerate(measurements):
        # Predict
        x_pred = x_est
        p_pred = p_est + process_variance

        # Update
        k = p_pred / (p_pred + measurement_variance)
        x_est = x_pred + k * (z - x_pred)
        p_est = (1 - k) * p_pred

        estimates[i] = x_est

    return estimates


def compute_velocity(position, dt):
    return np.gradient(position, dt)


def compute_acceleration(velocity, dt):
    return np.gradient(velocity, dt)


def main():
    np.random.seed(42)

    # Simulated time
    t = np.linspace(0, 10, 200)
    dt = t[1] - t[0]

    # True motion
    true_position = np.sin(t)

    # Noisy measurements
    noisy_position = true_position + np.random.normal(0, 0.15, size=t.shape)

    # Filtering
    ma_position = moving_average(noisy_position, window_size=7)
    sg_position = savgol_filter(noisy_position, window_length=11, polyorder=2)
    kf_position = simple_kalman_filter_1d(noisy_position)

    # Derivatives
    velocity = compute_velocity(kf_position, dt)
    acceleration = compute_acceleration(velocity, dt)

    # Plot position
    plt.figure(figsize=(10, 5))
    plt.plot(t, true_position, label="True Position")
    plt.plot(t, noisy_position, label="Noisy Position")
    plt.plot(t, ma_position, label="Moving Average")
    plt.plot(t, sg_position, label="Savitzky-Golay")
    plt.plot(t, kf_position, label="Kalman Filter")
    plt.xlabel("Time (s)")
    plt.ylabel("Position")
    plt.title("Motion Analysis: Position Filtering")
    plt.legend()
    plt.grid(True)
    plt.show()

    # Plot derivatives
    plt.figure(figsize=(10, 5))
    plt.plot(t, velocity, label="Velocity")
    plt.plot(t, acceleration, label="Acceleration")
    plt.xlabel("Time (s)")
    plt.ylabel("Value")
    plt.title("Motion Analysis: Derived Quantities")
    plt.legend()
    plt.grid(True)
    plt.show()


if __name__ == "__main__":
    main()
