from typing import Iterator, Tuple
from functools import partial
import pyglet


def load_atlas(t: str) -> Iterator[Tuple[str, pyglet.image.TextureRegion]]:
    atlas = pyglet.resource.image("{}.png".format(t))
    names = pyglet.resource.file("{}_names.txt".format(t), "r")

    strip = lambda x: str.rstrip(x, "\n")

    for atlas_index, name in enumerate(map(strip, names)):
        mult, rem = divmod(atlas_index, atlas.width // 16)

        left = mult * 16
        top = rem * 16

        texture = atlas.get_region(
            left, top, 16, 16
        )
        yield name, texture


def write_dict(var: str, file, dic: dict):
    # redefine print
    write = partial(print, file=file)

    write(var + " = {")
    for key, item in dic.items():
        coords = item.x, item.y, item.width, item.height
        write("    ", repr(key), ": ", repr(coords), ",", sep="")
    write("}")


with open("textures.py", "w") as dfile:
    dfile.write('__all__ = ("stone_descriptor", "coal_descriptor")\n\n')

    texture_map = {}
    texture_map.update(load_atlas("stone"))
    write_dict("stone_descriptor", dfile, texture_map)

    dfile.write("\n")

    texture_map = {}
    texture_map.update(load_atlas("coal"))
    write_dict("coal_descriptor", dfile, texture_map)
