#!/usr/bin/env python3
"""Generate human-like mouse trajectories and randomized click positions."""

import random
import math
from typing import Tuple, List

def random_point_in_rect(x: float, y: float, w: float, h: float, margin: float = 0.15) -> Tuple[float, float]:
    """Return a point inside the rectangle, avoiding the exact center and edges."""
    mx = w * margin
    my = h * margin
    px = x + mx + random.random() * (w - 2 * mx)
    py = y + my + random.random() * (h - 2 * my)
    # Push away from exact center a bit more
    cx, cy = x + w/2, y + h/2
    if abs(px - cx) < w*0.08 and abs(py - cy) < h*0.08:
        px += random.choice([-1, 1]) * w * 0.12
        py += random.choice([-1, 1]) * h * 0.12
    return px, py

def bezier_curve(start: Tuple[float, float], end: Tuple[float, float], steps: int = 25) -> List[Tuple[float, float]]:
    """Simple cubic bezier with random control points for natural mouse path."""
    x0, y0 = start
    x3, y3 = end
    # Random control points
    x1 = x0 + (x3 - x0) * random.uniform(0.2, 0.5) + random.uniform(-40, 40)
    y1 = y0 + (y3 - y0) * random.uniform(0.1, 0.4) + random.uniform(-30, 30)
    x2 = x0 + (x3 - x0) * random.uniform(0.5, 0.8) + random.uniform(-40, 40)
    y2 = y0 + (y3 - y0) * random.uniform(0.6, 0.9) + random.uniform(-30, 30)

    points = []
    for i in range(steps + 1):
        t = i / steps
        # Cubic bezier
        x = (1-t)**3 * x0 + 3*(1-t)**2 * t * x1 + 3*(1-t)*t**2 * x2 + t**3 * x3
        y = (1-t)**3 * y0 + 3*(1-t)**2 * t * y1 + 3*(1-t)*t**2 * y2 + t**3 * y3
        points.append((x, y))
    return points

def human_delay(base: float = 0.12, variance: float = 0.08) -> float:
    """Return a realistic delay in seconds."""
    return max(0.03, base + random.gauss(0, variance))

if __name__ == "__main__":
    # Quick self-test
    print(random_point_in_rect(100, 200, 180, 32))
    path = bezier_curve((50, 50), (400, 300))
    print(f"Path length: {len(path)} points")
    print(f"Sample delay: {human_delay():.3f}s")
