import typing as t
import dataclasses

@dataclasses.dataclass
class IntVector2:
    """A data structure that houses integer coordinates in the form (x, y)."""
    x: int
    y: int

    @classmethod
    def from_tuple(cls, data: t.Tuple[int, int]) -> "IntVector2":
        """Returns an instance of this class using data from a tuple."""
        return IntVector2(data[0], data[1])

@dataclasses.dataclass
class CollisionData:
    """A data structure that houses primitive collision data."""
    left: bool
    right: bool
    top: bool
    bottom: bool
