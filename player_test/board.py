from random import randint, randrange, random
from typing import List, Tuple, Optional, Iterable, Union
from collections import namedtuple
from math import sqrt, floor, cos, sin, tau, degrees
from enum import Enum

import pyglet
from pyglet.resource import image as load_image
from transitions import Machine
from vectors import Vector
from simples import *

# ****** Globals ******
Number = Union[int, float]
Position = Tuple[Number, Number]
Offset = namedtuple("Offset", "x, y")
size = 32  # px
texture_map = {}


# ****** Load Textures ******
def load_atlas(t: str) -> Iterable[Tuple[str, pyglet.image.TextureRegion]]:
    atlas = pyglet.resource.image("tiles/{}_atlas.png".format(t))
    names = pyglet.resource.file("tiles/{}_atlas_names.txt".format(t), "r")

    strip = lambda x: str.rstrip(x, "\n")

    for atlas_index, name in enumerate(map(strip, names)):
        mult, rem = divmod(atlas_index, atlas.width // 16)

        left = mult * 16
        top = rem * 16

        texture = atlas.get_region(
            left, top, 16, 16
        )
        yield name, texture


texture_map.update(load_atlas("stone"))
texture_map.update(
    {
        # air textures
        # "bottom_addition": load_image("tiles/wall_02.png"),
        # "bottom_addition_02": load_image("tiles/wall_01.png"),
        "shadow_left": load_image("tiles/shadow_left.png"),
        "shadow_corner": load_image("tiles/shadow_corner.png"),
        "air": load_image("tiles/air.png"),

        # skirt textures
        "skirt": load_image("tiles/skirt.png"),

        # miner textures
        "miner": load_image("tiles/pickaxe.png")
    }
)


pyglet.gl.glTexParameteri(
        pyglet.gl.GL_TEXTURE_2D,
        pyglet.gl.GL_TEXTURE_MAG_FILTER,
        pyglet.gl.GL_NEAREST
)

pyglet.gl.glBlendFunc(
    pyglet.gl.GL_SRC_ALPHA,
    pyglet.gl.GL_ONE_MINUS_SRC_ALPHA
)

for key in texture_map.keys():
    img = texture_map[key]
    texture = img.get_texture()
    texture.width = size
    texture.height = size

floors = pyglet.graphics.OrderedGroup(0)
blocks = pyglet.graphics.OrderedGroup(1)
miners = pyglet.graphics.OrderedGroup(2)


class Board(SimpleBoard):
    def __init__(self, width, height, xoff, yoff):
        super().__init__(width, height, xoff, yoff)

        self.batch = pyglet.graphics.Batch()
        self.blocks: List[List[Block]] = [[None] * height for _ in range(width)]

        for i in range(width):
            for j in range(height):
                pos = i * size + xoff, j * size

    def update(self, dt):
        pass

    def draw(self):
        pass


class Block(SimplePiece):
    START_HEALTH = 1.

    def __init__(
            self, board: Board, batch: pyglet.graphics.Batch,
            pos: Tuple[float, float], index: Tuple[int, int], depth: int,
            bound: Tuple[int, int, int]
    ):
        super().__init__(board, batch, pos, index, depth, bound)
        self.health = self.START_HEALTH
        self.type = "stone"

        self.texture_index = randrange(3) + 1
        self.current_texture = f"full_{self.texture_index:0>2}"
        self.sprite = pyglet.sprite.Sprite(
            texture_map[self.current_texture],
            *pos, batch=batch, group=blocks
        )

    def update(self, dt):
        pass

    def draw(self):
        pass


class Player:
    pass
