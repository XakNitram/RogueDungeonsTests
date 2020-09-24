from typing import Iterator, List

import pyglet
from transitions import Machine
from combat_test.globals import Index, Uninitialized


class TexturedObject:
    def __init__(
            self, texture, pos, batch=None,
            group=None, usage='dynamic'
    ):
        self._pos = list(pos)

        self.sprite = pyglet.sprite.Sprite(
            texture, *pos, batch=batch,
            group=group, usage=usage
        )

    @property
    def x(self) -> float:
        return self._pos[0]

    @x.setter
    def x(self, value: float):
        self._pos[0] = float(value)

    @property
    def y(self) -> float:
        return self._pos[1]

    @y.setter
    def y(self, value: float):
        self._pos[1] = float(value)

    @property
    def pos(self) -> List:
        return self._pos

    @pos.setter
    def pos(self, v: Iterator):
        self._pos = list(v)
        self.sprite.update(*self.pos)

    @property
    def texture(self) -> pyglet.image.TextureRegion:
        return self.sprite.image

    @texture.setter
    def texture(self, value: pyglet.image.TextureRegion):
        self.sprite.image = value


class SimpleSystem:
    states = ["startup"]
    transitions = []

    def __init__(self, initial_state: str = "startup"):
        self.state: Uninitialized[str] = None
        self._machine = Machine(
            model=self, states=self.states,
            transitions=self.transitions,
            initial=initial_state
        )

    def update(self, dt):
        handler_name = "handle" + "_" + self.state
        if hasattr(self, handler_name):
            handler = getattr(self, handler_name)
            handler(dt)


class Piece:
    def __init__(self, index: Index):
        self._i, self._j = index

    @property
    def index(self):
        return self._i, self._j

    @index.setter
    def index(self, value: Index):
        self._i, self._j = value

    @property
    def i(self) -> int:
        return self._i

    @i.setter
    def i(self, value: int):
        self._i = int(value)

    @property
    def j(self):
        return self._j

    @j.setter
    def j(self, value):
        self._j = int(value)


class StatefulPiece(Piece):
    states = ['startup']
    transitions = []

    def __init__(self, index: Index, *, initial_state: str = 'startup'):
        super().__init__(index)
        self.state: Uninitialized[str] = None
        self._machine = Machine(
            model=self, states=self.states,
            transitions=self.transitions,
            initial=initial_state
        )

    def update(self, dt):
        handler_name = '_'.join(['handle', self.state])
        if hasattr(self, handler_name):
            handler = getattr(self, handler_name)
            handler(dt)
