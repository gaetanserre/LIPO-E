import numpy as np


class Function:
    def __init__(self) -> None:
        self.bounds = np.array([(0, 1), (0, 1)])
        self.k = 1.5

        self.radius = 0.5
        self.diam = np.sqrt(2)

    def __call__(self, x: np.ndarray) -> float:
        return -np.sqrt((x[0] - np.pi / 16) ** 2 + (x[1] - np.pi / 16) ** 2)
