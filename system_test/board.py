from typing import List, Tuple
from random import randrange

from simples import SimpleBoard, SimplePiece
from system_test.globals import *
import pyglet
from opensimplex import OpenSimplex


class Board(SimpleBoard):
    def __init__(self, system, width, height, xoff, yoff):
        super(Board, self).__init__(width, height, xoff, yoff)

        # ****** Board Attributes ******
        self.system = system

        # ****** Initialize Board ******
        self.batch = pyglet.graphics.Batch()
        self.blocks: List[List[Block]] = [[None] * height for _1 in range(width)]

    def populate(self):
        field = OpenSimplex(0)
        for i in range(self.width):
            for j in range(self.height):
                pos = i * 16 * size + self.xoff, j * 16 * size + self.yoff
                block = Block(
                    self, self.batch, pos, (i, j), 0,
                    (self.width, self.height, 1), field
                )
                self.blocks[i][j] = block
                yield

    def update(self, dt):
        pass

    def draw(self):
        self.batch.draw()


class BlockTexture(TexturedObject):
    def __init__(
            self, type: str, index: int, texture: pyglet.image.TextureRegion,
            pos: Position, batch: pyglet.graphics.Batch
    ):
        super().__init__(texture, pos, batch)

        self.type = type
        self.index = index

    def update(self):
        # call get_stone_texture or get_coal_texture based on type here.
        pass

    def get_stone_texture(self, octs: GridDescriptor):
        pass

    def get_coal_texture(self, octs: GridDescriptor):
        pass


class Block(SimplePiece):
    VEIN_SIZE = 5
    IRON_CHANCE = 0.25
    COAL_CHANCE = 0.35

    def spawn(self, field, index):
        i, j = index
        vein_size = self.VEIN_SIZE
        return (field.noise2d(
            i / vein_size, j / vein_size
        ) + 1) / 2

    def __init__(
            self, board: Board, batch, pos: Position,
            index, depth, bound, field: OpenSimplex
    ):
        super().__init__(board, batch, pos, index, depth, bound)
        self.system = board.system
        self.textures = self.system.textures
        texture_index = randrange(3)

        spawn_chance = self.spawn(field, index)
        # if spawn_chance < self.IRON_CHANCE:
        #     texture_name = f"IRON_FLOOR_{texture_index + 1:0>2}"
        if spawn_chance < self.COAL_CHANCE:
            texture_name = f"COAL_FLOOR_{texture_index + 1:0>2}"
        else:
            texture_name = f"STONE_FLOOR_{texture_index + 1:0>2}"

        texture = self.textures[texture_name]
        self.base = BlockTexture("stone", randrange(3), texture, pos, batch)

    def update(self, dt):
        pass

    def draw(self):
        pass
