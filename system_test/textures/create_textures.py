from typing import Iterator, Tuple
from functools import partial
import pyglet


def load_atlas(t: str) -> Iterator[Tuple[str, pyglet.image.TextureRegion]]:
    atlas = pyglet.resource.image("{}.png".format(t))
    names = pyglet.resource.file("{}_names.txt".format(t), "r")

    strip = lambda x: str.rstrip(x, "\n")

    for atlas_index, name in enumerate(map(strip, names)):
        mult, rem = divmod(atlas_index, atlas.width // 16)
        region = mult * 16, rem * 16, 16, 16
        yield name, region


def write_dict(var: str, file, dic: dict):
    # redefine print
    write = partial(print, file=file)

    write(var + " = {")
    for key, region in dic.items():
        # coords = item.x, item.y, item.width, item.height
        write("    ", repr(key), ": ", repr(region), ",", sep="")
    write("}")


with open("textures.py", "w") as dfile:
    write = partial(print, file=dfile)

    write('__all__ = ("stone_descriptor", "coal_descriptor")\n')

    texture_map = {}
    texture_map.update(load_atlas("stone"))
    write_dict("stone_descriptor", dfile, texture_map)

    write()

    texture_map = {}
    texture_map.update(load_atlas("coal"))
    write_dict("coal_descriptor", dfile, texture_map)
