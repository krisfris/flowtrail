from flowtrail.window import Window
from flowtrail.scene import Scene
from flowtrail.renderer import Renderer
from flowtrail.input import Input
import config


class App:
    def __init__(self):
        config.app = self
        self.done = False

        self.input = Input()
        self.window = Window()
        self.scene = Scene()
        self.renderer = Renderer()

    def update(self):
        self.renderer.update()
        self.window.update()
        self.scene.update()
        self.input.update()

    def run(self):
        while not self.done:
            self.update()
        self.drop()

    def drop(self):
        self.input.drop()
        self.scene.drop()
        self.renderer.drop()
        self.window.drop()

    def quit(self):
        self.done = True


if __name__ == '__main__':
    App().run()
