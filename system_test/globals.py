from typing import Optional, Tuple

import pyglet

__all__ = ('size', 'Uninitialized', 'GridDescriptor', 'Position', 'TexturedObject')

# ****** Types ******
Uninitialized = Optional
GridDescriptor = Tuple[
    bool, bool, bool, bool,
    bool, bool, bool, bool
]
Position = Tuple[int, int]

# size = 2
size = 0.125


class TexturedObject:
    def __init__(
            self, texture: pyglet.image.TextureRegion,
            pos: Position, batch: pyglet.graphics.Batch
    ):
        self.pos = pos

        self.sprite = pyglet.sprite.Sprite(
            texture, *pos, batch=batch
        )

    @property
    def texture(self) -> pyglet.image.TextureRegion:
        return self.sprite.image

    @texture.setter
    def texture(self, value: pyglet.image.TextureRegion):
        self.sprite.image = value
