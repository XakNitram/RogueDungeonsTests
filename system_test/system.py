from typing import Dict, Iterable, Tuple, Generator, List
from time import perf_counter

from simples import SimpleSystem
from system_test.board import Board
from system_test.globals import *
import pyglet


# ****** Globals ******
# **** Type Aliases ****
AtlasDescriptor = Dict[str, Tuple[int, int, int, int]]
# An AtlasDescriptor is a dictionary of image names and
# a tuple of their x, y, width, and height values in the atlas


def load_atlas(
        atlas: pyglet.image.TextureRegion, positions: AtlasDescriptor
) -> Iterable[Tuple[str, pyglet.image.TextureRegion]]:
    strip = lambda x: str.rstrip(x, "\n")

    for atlas_index, item in enumerate(zip(map(strip, positions.keys()), positions.values())):
        name, position = item
        texture = atlas.get_region(
            *position
        )
        yield name, texture


# move this to another file.
class Progressbar:
    def __init__(self, x, y, width, height, maximum):
        self._x, self._y = x, y
        self.width = width
        self.height = height

        self.border = pyglet.graphics.vertex_list_indexed(
            4,         # vertex count
            (0, 1, 1, 2, 2, 3, 3, 0),  # indices
            ("v2i/static", (x, y, x + width, y, x + width, y + height, x, y + height)),  # vertex data
            ("c3B/static", (
                0xFF, 0x85, 0x1A,
                0xFF, 0x85, 0x1A,
                0xFF, 0x85, 0x1A,
                0xFF, 0x85, 0x1A
            ))   # color data  #FF851A
        )

        self.fill = pyglet.graphics.vertex_list_indexed(
            4,  # vertex count
            (0, 1, 2, 2, 3, 0),  # indices
            ("v2i/dynamic", (x, y, x, y, x, y + height, x, y + height)),  # vertex data
            ("c3B/static", (
                0xFF, 0x85, 0x1A,
                0xFF, 0x85, 0x1A,
                0xFF, 0x85, 0x1A,
                0xFF, 0x85, 0x1A
            ))  # color data  #FF851A
        )

        self.maximum = maximum
        self._value = 0

    @property
    def x(self) -> int:
        return self._x

    @property
    def y(self) -> int:
        return self._y

    @property
    def value(self) -> int:
        return self._value

    @value.setter
    def value(self, val):
        self._value = val

        new_val = int((self.value % self.maximum) * self.width / self.maximum)
        self.fill.vertices[2] = self.x + new_val
        self.fill.vertices[4] = self.x + new_val

    def step(self, step=1):
        self.value += step

    def draw(self):
        self.border.draw(pyglet.gl.GL_LINES)
        self.fill.draw(pyglet.gl.GL_TRIANGLES)


class System(SimpleSystem):
    FRAME_LOAD_PERCENT = 1/2  # percent of frame taken up for loading

    states = SimpleSystem.states + ["running"]
    transitions = SimpleSystem.transitions + [
        ["run", "startup", "running"]
    ]

    def __init__(self, window):
        super().__init__()

        # ****** Attributes ******
        self.window: pyglet.window.Window = window
        self.textures: Dict[str, pyglet.image.TextureRegion] = {}

        # board width setup
        width = int(self.window.width // (16 * size))
        width -= 1
        xoff = (self.window.width - width * (16 * size)) // 2

        # board height setup
        height = int(self.window.height // (16 * size))
        height -= 1
        yoff = (self.window.height - height * (16 * size)) // 2

        self.max_blocks = width * height
        self.board = Board(self, width, height, xoff, yoff)

        pyglet.font.add_file('loose/Deutsch.ttf')
        # pyglet.font.add_file('WashingtonText.ttf')
        self.progressbar = Progressbar(64, 64, window.width - 64 * 2, 16, 100)
        self.progress_text = pyglet.text.Label(
            "", "Deutsch Gothic", 16,
            color=(0xFF, 0x85, 0x1A, 0xFF),
            x=64 + 4, y=84 + 4
        )

        # ****** Texture Loading Variables ******
        self.atlases: List[str] = []
        self.atlas_maps: List[AtlasDescriptor] = []
        self.max_textures: int = 0

        # ****** Stage Checks ******
        self.loaded_textures: bool = False
        self.loaded_board: bool = False
        self.ready_to_run: bool = False

        # ****** Music ******

    def add_atlas(self, file: str, descriptor: AtlasDescriptor):
        self.atlases.append(file)
        self.atlas_maps.append(descriptor)
        self.max_textures += len(descriptor)

    def add_loose_texture(self, file: str, name: str, *, maintain_size=False):
        texture = pyglet.resource.image(file)
        if maintain_size:
            texture.width = int(size * texture.width)
            texture.height = int(size * texture.height)
        self.textures[name] = texture

    def _load_textures(self, *, reload=False):
        self.progressbar.maximum = self.max_textures
        if reload:
            self.progress_text.text = "Reloading Textures"
        else:
            self.progress_text.text = "Loading Textures"

        for index, file in enumerate(self.atlases):
            descriptor = self.atlas_maps[index]
            atlas = pyglet.resource.image(file)
            for name, region in load_atlas(atlas, descriptor):
                self.textures[name] = region
                texture = region.get_texture()
                texture.width = int(size * texture.width)
                texture.height = int(size * texture.height)

                self.progressbar.step()
                yield

        # yield  # have to yield or the following code won't work.

        # finished with loading all atlases
        self.loaded_textures = True

    def _load_board(self):
        self.progressbar.value = 0
        self.progressbar.maximum = self.max_blocks
        self.progress_text.text = "Loading"

        start = perf_counter()
        div = 1
        pers = 0
        flip = False

        for i, _ in enumerate(self.board.populate()):
            current = perf_counter()
            if (current - start) > div:
                if not flip:
                    pers = ((pers + 1) % 4)
                else:
                    pers = ((pers - 1) % 4)
                self.progress_text.text = "Loading" + ("." * pers)
                if pers == 3:
                    flip = True
                elif pers == 0:
                    flip = False
                start = current
            self.progressbar.step()
            yield

        self.loaded_board = True

    def handle_startup(self, dt: float):
        if not len(self.atlases):
            raise Exception("No textures loaded.")

        if not self.loaded_textures:
            self.start_load(self._load_textures())
            # smoothe resized textures
            pyglet.gl.glTexParameteri(
                pyglet.gl.GL_TEXTURE_2D,
                pyglet.gl.GL_TEXTURE_MAG_FILTER,
                pyglet.gl.GL_NEAREST
            )

            pyglet.gl.glBlendFunc(
                pyglet.gl.GL_SRC_ALPHA,
                pyglet.gl.GL_ONE_MINUS_SRC_ALPHA
            )
            return

        if not self.loaded_board:
            self.start_load(self._load_board())
            return

        self.ready_to_run = True

        self.run()

    def handle_running(self, dt: float):
        pass

    def draw(self):
        if self.ready_to_run:
            self.board.draw()
        else:
            self.progress_text.draw()
            self.progressbar.draw()
