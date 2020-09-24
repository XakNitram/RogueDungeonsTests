from typing import Tuple, Generator
from time import perf_counter_ns, perf_counter

from pyglet.sprite import Sprite
from transitions import Machine
from globals import Uninitialized

__all__ = ("SimpleSystem", "SimpleBoard", "SimplePiece")


class SimpleSystem:
    FRAME_LOAD_PERCENT = 1/2  # of a frame

    states = ["startup", 'loading']
    transitions = [
        ['load', '*', 'loading'],
        ['resume', 'loading', 'startup']
    ]

    def __init__(self, initial_state: str = "startup"):
        self.state: Uninitialized[str] = None
        self._machine = Machine(
            model=self, states=self.states,
            transitions=self.transitions,
            initial=initial_state
        )
        self._loading_generator: Uninitialized[Generator] = None
        self._load_start = 0.

    def update(self, dt):
        handler_name = "handle" + "_" + self.state
        if hasattr(self, handler_name):
            handler = getattr(self, handler_name)
            handler(dt)

    def start_load(self, gen: Generator = None):
        self._loading_generator = gen
        self._load_start = perf_counter()
        self.load()

    def handle_loading(self, dt):
        max_time = dt * self.FRAME_LOAD_PERCENT
        start = perf_counter_ns()

        for _ in self._loading_generator:
            current = perf_counter_ns()

            if (current - start) * pow(10, -9) > max_time:
                return
        self._loading_generator = None
        print(perf_counter() - self._load_start)
        self.resume()


class SimpleBoard:
    """Container for Pieces"""

    __slots__ = ("width", "height", "xoff", "yoff")

    def __init__(self, width, height, xoff, yoff):
        self.width = width
        self.height = height

        self.xoff = xoff
        self.yoff = yoff

    @property
    def size(self) -> Tuple[int, ...]:
        return self.width, self.height

    @property
    def offset(self) -> Tuple[int, ...]:
        return self.xoff, self.yoff

    def is_within_bounds(self, pair) -> bool:
        """Test whether the pair exists in the bounds of the board"""
        return all(0 <= i < bound for i, bound in zip(pair, self.size))

    def convert_to_board_coords(self, x, y):
        return x + self.xoff, y + self.yoff

    def update(self, dt):
        """Update the board"""
        raise NotImplementedError

    def draw(self):
        """Draw the board"""
        raise NotImplementedError


class SimplePiece:
    __slots__ = (
        "board", "batch", "x", "y", "i", "j", "level", "bound",
        "board_width", "board_height", "board_depth",
        "sprite", "_rendering"
    )

    def __init__(
            self, board: SimpleBoard, batch, pos: Tuple[float, float],
            index: Tuple[int, int], depth, bound: Tuple[int, int, int],
    ):
        self.board = board
        self.batch = batch

        self.sprite: Sprite = None
        self._rendering = True

        self.x, self.y = 0, 0
        self.pos = pos

        self.i, self.j = 0, 0
        self.index = index
        self.level = depth

        self.bound = bound
        self.board_width, self.board_height, self.board_depth = bound

    def __repr__(self):
        return str(type(self).__name__)

    @property
    def pos(self) -> Tuple[float, float]:
        return self.x, self.y

    @pos.setter
    def pos(self, v: Tuple[float, float]):
        self.x, self.y = v
        if self.sprite is not None:
            self.sprite.update(self.x, self.y)

    @property
    def index(self) -> Tuple[int, int]:
        return self.i, self.j

    @index.setter
    def index(self, v: Tuple[int, int]):
        self.i, self.j = v

    def is_rendering(self):
        return bool(self._rendering)

    def enable_rendering(self):
        self._rendering = True
        self.sprite.visible = True

    def disable_rendering(self):
        self._rendering = False
        self.sprite.visible = False

    def draw(self):
        raise NotImplementedError
