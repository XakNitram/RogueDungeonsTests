#! ../venv/Scripts/python.exe
import pyglet
from system_test.system import System
from system_test.textures import *


# ****** Globals ******
resolution = {"width": 1024, "height": 800}
window = pyglet.window.Window(**resolution, caption="SystemTest", vsync=True)
width, height = window.width, window.height


# ****** Game Objects ******
system = System(window)
system.add_atlas("textures/stone.png", stone_descriptor)
system.add_atlas("textures/coal.png", coal_descriptor)
system.add_loose_texture("textures/shadow_left.png", "shadow_left")
system.add_loose_texture("textures/shadow_corner.png", "shadow_corner")
system.add_loose_texture("textures/air.png", "air")
system.add_loose_texture("textures/pickaxe.png", "miner")


@window.event
def on_draw():
    window.clear()
    system.draw()


def update(dt):
    system.update(dt)


if __name__ == '__main__':
    pyglet.clock.schedule_interval(update, 1/60)
    pyglet.app.run()
