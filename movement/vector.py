import math


class Vector2:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
        self.thresh = 0.000001

    def __add__(self, other):
        return Vector2(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector2(self.x - other.x, self.y - other.y)

    def __neg__(self):
        return Vector2(-self.x, -self.y)

    def __mul__(self, scalar):
        return Vector2(self.x * scalar, self.y * scalar)

    def __truediv__(self, scalar):
        return Vector2(self.x / scalar, self.y / scalar) if scalar != 0 else None

    def __eq__(self, other):
        return (
            abs(self.x - other.x) < self.thresh and abs(self.y - other.y) < self.thresh
        )

    def magnitude_squared(self):
        return self.x**2 + self.y**2

    def magnitude(self):
        return math.sqrt(self.magnitude_squared())

    def copy(self):
        return Vector2(self.x, self.y)

    def as_tuple(self):
        return self.x, self.y

    def as_int(self):
        return int(self.x), int(self.y)

    def __str__(self):
        return f"<{self.x}, {self.y}>"
