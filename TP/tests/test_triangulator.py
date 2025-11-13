# tests/test_triangulator.py

import pytest
from triangulator.pointset import PointSet
from triangulator.triangles import Triangles
from triangulator.triangulator import triangulate

# --- Tests de conversion PointSet ---

def test_pointset_from_bytes_valid():
    # 2 points : (1.0, 2.0) et (3.0, 4.0)
    data = (
        b'\x02\x00\x00\x00' +  # nombre de points = 2
        b'\x00\x00\x80\x3f' + b'\x00\x00\x00\x40' +  # (1.0, 2.0)
        b'\x00\x00\x40\x40' + b'\x00\x00\x80\x40'     # (3.0, 4.0)
    )
    ps = PointSet.from_bytes(data)
    assert len(ps.points) == 2
    assert ps.points[0] == pytest.approx((1.0, 2.0))
    assert ps.points[1] == pytest.approx((3.0, 4.0))

def test_pointset_to_bytes_roundtrip():
    points = [(1.0, 2.0), (3.0, 4.0)]
    ps = PointSet(points)
    data = ps.to_bytes()
    ps2 = PointSet.from_bytes(data)
    assert ps.points == ps2.points

# --- Tests de triangulation logique ---

def test_triangulate_3_points():
    points = [(0.0, 0.0), (1.0, 0.0), (0.0, 1.0)]
    triangles = triangulate(points)
    # On s’attend à 1 triangle avec 3 indices
    assert len(triangles) == 1
    assert len(triangles[0]) == 3
    assert all(isinstance(i, int) for i in triangles[0])
    # Indices doivent être entre 0 et 2
    assert all(0 <= i < 3 for i in triangles[0])

def test_triangulate_4_points_convex():
    points = [(0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (0.0, 1.0)]
    triangles = triangulate(points)
    assert len(triangles) == 2
    for t in triangles:
        assert len(t) == 3
        assert all(isinstance(i, int) for i in t)
        assert all(0 <= i < 4 for i in t)

# --- Tests d'erreur ---

def test_triangulate_empty_points():
    with pytest.raises(ValueError):
        triangulate([])

def test_triangulate_collinear_points():
    points = [(0.0, 0.0), (1.0, 0.0), (2.0, 0.0)]
    triangles = triangulate(points)
    # On accepte 1 triangle (il sera dégénéré, mais c'est OK pour ce TP)
    assert len(triangles) == 1
    # Optionnel : vérifier que les indices sont valides
    assert all(0 <= i < 3 for i in triangles[0])