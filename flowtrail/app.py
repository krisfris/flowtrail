from flowtrail.window import Window
from flowtrail.scene import Scene
from flowtrail.renderer import Renderer
from flowtrail.input import Input
from flowtrail.physics import Physics
import config


class App:
    def __init__(self):
        config.app = self
        self.done = False

        self.input = Input()
        self.window = Window()
        self.scene = Scene()
        self.renderer = Renderer()
        self.physics = Physics()

    def update(self):
        self.renderer.update()
        self.window.update()
        self.scene.update()
        self.input.update()
        self.physics.update()

    def run(self):
        while not self.done:
            self.update()
        self.drop()

    def drop(self):
        self.physics.drop()
        self.input.drop()
        self.scene.drop()
        self.renderer.drop()
        self.window.drop()

    def quit(self):
        self.done = True


if __name__ == '__main__':
    App().run()
