import math
def normalize_vector(vector):
    x, y = vector
    magnitude = math.sqrt(x**2 + y**2)
    normalized_x = x / magnitude
    normalized_y = y / magnitude
    return normalized_x, normalized_y

def normalize_range(minValue, maxValue, inputValue, scalar=1, high_to_low=False):
    range  =(inputValue - minValue)
    normalized_value = (range / (maxValue - minValue)) * scalar
    if high_to_low:
        normalized_value = scalar - normalized_value
    return max(0, min(normalized_value, scalar))