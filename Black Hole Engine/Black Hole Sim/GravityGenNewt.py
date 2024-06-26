import numpy as np

# Globals
mass_bh = 4e10  # 1.989e30  # Kg
mass_sens = 10
G = 6.67430e-11  # Gravitational Constant


# Class that represents a point in space which is used to calculate the physical effects being acted upon
# that point.
class PointVector:
    def __init__(self, x, y, z, vector):
        self.x = x
        self.y = y
        self.z = z
        self.vector = vector


# This method is used to calculate the gravitational force on a sensor as a vector.
def calculate_gravitational_force(point_vector):
    """
    Calculate the gravitational force on a point near a black hole (simplified model).

    Parameters:
    - point_vector: An instance of PointVector representing the position and vector of the point.
    - mass_bh: Mass of the black hole in kilograms.
    - G: Gravitational constant, default value in m^3 kg^-1 s^-2.

    Returns:
    - Gravitational force as a NumPy array in Newtons.
    """
    # Position vector of the point in space
    position_vector = np.array([point_vector.x, point_vector.y, point_vector.z])

    # Distance from the point to the center of the black hole
    r = np.linalg.norm(position_vector)

    # TODO: Change this to calculated event horizon.
    if r == 0:
        raise ValueError("The point is at the center of the black hole, distance cannot be zero.")

    # Calculate gravitational force magnitude (Newton's law of gravitation)
    # F = G * (m1*m2) / r^2
    force_magnitude = G * mass_bh * mass_sens / r ** 2

    # Direction of the force is toward the black hole, which is opposite the position vector
    force_direction = -position_vector / r

    # Calculate force vector
    force_vector = force_magnitude * force_direction

    return force_vector
