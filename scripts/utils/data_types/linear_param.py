import math

class LinearParam:
    def __init__(self):
        self.initial_number = 0
        self.step = 0

    def calculate_linear_value(self, level):
        value = self.initial_number + self.step * level
        return math.floor(value + 0.5)
