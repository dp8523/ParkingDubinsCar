import math
from control import Control


class State:
    """
    stores actual values of the state variables
    """
    def __init__(self, x, y, alpha, v):
        self.x = x
        self.y = y
        self.alpha = alpha
        self.v = v

    def next_state(self, gamma, beta, h):
        next_x = self.x + h * (self.v * math.cos(self.alpha))
        next_y = self.y + h * (self.v * math.sin(self.alpha))
        next_alpha = self.alpha + h * gamma
        next_v = self.v + h * beta
        return State(next_x, next_y, next_alpha, next_v)

    def is_feasible(self) -> bool:
        if self.x <= -4 and self.y > 3:
            return True
        if (-4 < self.x < 4) and self.y > -1:
            return True
        if self.x >= 4 and self.y > 3:
            return True
        return False
