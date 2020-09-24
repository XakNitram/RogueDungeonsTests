import pyglet
from combat_test.simples import StatefulPiece, TexturedObject
from combat_test.globals import Index
from vectors import Vector


size = 16


"""
Can't move forward with this until the board is sorted out.
"""
# TODO: Give movers names so that players can make stories


class Mover(StatefulPiece):
    states = StatefulPiece.states + ['moving']
    transitions = StatefulPiece.transitions + [
        ['move', '*', 'moving']
    ]

    def __init__(
            self, system, index: Index, texture: pyglet.image.TextureRegion,
            batch: pyglet.graphics.Batch = None, group: pyglet.graphics.Group = None,
            *, initial_state: str = 'startup'
    ):
        super().__init__(index, initial_state=initial_state)

        self.texture = TexturedObject(
            texture, Vector(*index) * size, batch=batch,
            group=group, usage='dynamic'
        )
        self.system = system
        self.board = system.board
        self.range = 3

    def handle_moving(self, dt):
        pass

    def move(self, i, j, dt):
        abs_pos = self.board.get_abs_pos


class Human(Mover):
    states = Mover.states + []
    transitions = Mover.transitions + []

    def __init__(
            self, system, index: Index, texture: pyglet.image.TextureRegion,
            batch: pyglet.graphics.Batch = None, group: pyglet.graphics.Group = None,
            *, initial_state: str = 'startup'
    ):
        super().__init__(system, index, texture, batch, group, initial_state=initial_state)


class Miner(Human):
    states = Human.states + []
    transitions = Human.transitions + []

    def __init__(self, system, index: Index):
        texture: pyglet.image.TextureRegion = system.textures['green_mage']
        super().__init__(system, index, texture, initial_state='startup')


class Fighter(Human):
    states = Human.states + []
    transitions = Human.transitions + []

    def __init__(self, system, index: Index):
        texture: pyglet.image.TextureRegion = system.textures['green_mage']
        super().__init__(system, index, texture, initial_state='startup')
