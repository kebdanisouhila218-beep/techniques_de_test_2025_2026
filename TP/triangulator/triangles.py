import struct
from typing import List, Tuple

class Triangles:
    def __init__(self, vertices: List[Tuple[float, float]], triangles: List[Tuple[int, int, int]]):
        self.vertices = vertices
        self.triangles = triangles

    def to_bytes(self) -> bytes:
        # Partie 1 : vertices (comme un PointSet)
        data = struct.pack("I", len(self.vertices))
        for x, y in self.vertices:
            data += struct.pack("ff", x, y)
        # Partie 2 : triangles
        data += struct.pack("I", len(self.triangles))
        for t in self.triangles:
            data += struct.pack("III", t[0], t[1], t[2])
        return data