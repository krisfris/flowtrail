from OpenGL.GL import *
from flowtrail.triangles import TriangleRenderer
from flowtrail.skybox import Skybox


class Renderer:
    def __init__(self):
        self.triangle_renderer = TriangleRenderer()
        self.skybox = Skybox()

    def window_size_changed(self, w, h):
        pass

    def update(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        self.skybox.update()
        self.triangle_renderer.update()

    def drop(self):
        self.triangle_renderer.drop()
