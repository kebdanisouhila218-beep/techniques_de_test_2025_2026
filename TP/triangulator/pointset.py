import struct
from typing import List, Tuple

class PointSet:
    def __init__(self, points: List[Tuple[float, float]]):
        self.points = points

    def to_bytes(self) -> bytes:
        data = struct.pack("I", len(self.points))
        for x, y in self.points:
            data += struct.pack("ff", x, y)
        return data

    @classmethod
    def from_bytes(cls, data: bytes) -> "PointSet":
        num_points = struct.unpack("I", data[:4])[0]
        points = []
        offset = 4
        for _ in range(num_points):
            x, y = struct.unpack("ff", data[offset:offset+8])
            points.append((x, y))
            offset += 8
        return cls(points)