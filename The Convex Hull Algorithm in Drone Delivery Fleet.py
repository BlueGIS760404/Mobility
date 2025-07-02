import math
from typing import List, Tuple
import matplotlib.pyplot as plt

# Type alias for a point (latitude, longitude)
Point = Tuple[float, float]

def orientation(p: Point, q: Point, r: Point) -> int:
    """Determine orientation of triplet (p, q, r).
    Returns:
     0 --> Collinear
     1 --> Clockwise
     2 --> Counterclockwise
    """
    val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])
    if math.isclose(val, 0):
        return 0
    return 1 if val > 0 else 2

def convex_hull(points: List[Point]) -> List[Point]:
    """Compute the convex hull of a set of points using Graham's scan."""
    if len(points) < 3:
        return points

    # Find the point with the lowest y-coordinate (and leftmost if tied)
    start = min(points, key=lambda p: (p[1], p[0]))
    points.remove(start)

    # Sort points by polar angle with respect to start
    def polar_angle(p: Point) -> float:
        x, y = p[0] - start[0], p[1] - start[1]
        return math.atan2(y, x)

    points.sort(key=polar_angle)

    # Initialize stack with the first two points
    stack = [start, points[0]]

    # Process remaining points
    for point in points[1:]:
        while len(stack) > 1 and orientation(stack[-2], stack[-1], point) != 2:
            stack.pop()
        stack.append(point)

    return stack

# Example: GPS coordinates (latitude, longitude) of delivery hubs
gps_points = [
    (40.7128, -74.0060),  # New York City
    (40.7309, -73.9872),  # Manhattan
    (40.6782, -73.9442),  # Brooklyn
    (40.7831, -73.9712),  # Upper West Side
    (40.7589, -73.9851),  # Times Square
    (40.6413, -73.7781),  # JFK Airport
]

# Compute the convex hull
hull = convex_hull(gps_points)

# Visualize the result
def plot_convex_hull(points: List[Point], hull: List[Point]):
    plt.scatter([p[0] for p in points], [p[1] for p in points], c='blue', label='Points')
    hull.append(hull[0])  # Close the polygon
    plt.plot([p[0] for p in hull], [p[1] for p in hull], 'r-', label='Convex Hull')
    plt.xlabel('Latitude')
    plt.ylabel('Longitude')
    plt.title('Convex Hull of Delivery Hub Locations')
    plt.legend()
    plt.grid(True)
    plt.show()

# Plot the points and convex hull
plot_convex_hull(gps_points, hull)

# Print the convex hull points
print("Convex Hull Points (Geofence Boundary):")
for point in hull:
    print(f"Latitude: {point[0]}, Longitude: {point[1]}")
