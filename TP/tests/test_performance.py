# tests/test_performance.py

import pytest
import time
from triangulator.triangulator import triangulate

@pytest.mark.performance
def test_performance_small():
    points = [(i, i) for i in range(10)]
    start = time.perf_counter()
    triangles = triangulate(points)
    end = time.perf_counter()
    print(f"Triangulation de 10 points : {end - start:.4f}s")
    assert len(triangles) > 0

@pytest.mark.performance
def test_performance_medium():
    points = [(i, i) for i in range(100)]
    start = time.perf_counter()
    triangles = triangulate(points)
    end = time.perf_counter()
    print(f"Triangulation de 100 points : {end - start:.4f}s")
    assert len(triangles) > 0

@pytest.mark.performance
def test_performance_large():
    points = [(i, i) for i in range(1000)]
    start = time.perf_counter()
    triangles = triangulate(points)
    end = time.perf_counter()
    print(f"Triangulation de 1000 points : {end - start:.4f}s")
    assert len(triangles) > 0