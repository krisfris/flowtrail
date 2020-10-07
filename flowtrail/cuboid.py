import math
import numpy as np

from flowtrail.rectangle import Rectangle
import flowtrail.transformations as transformations


class Cuboid:
    def __init__(self):
        self.size = (10, 10, 10)
        self.position = (0, 0, 0)
        self.rotation = (1, 0, 0, 0)
        self.color = (1, 0, 0, 1)

        self.rects = [Rectangle() for _ in range(6)]

    def update_rotation(self):
        self.rects[1].rotation = transformations.quaternion_about_axis(math.pi, (0, 1, 0))
        self.rects[2].rotation = transformations.quaternion_about_axis(math.pi * 0.5, (0, 1, 0))
        self.rects[3].rotation = transformations.quaternion_about_axis(math.pi * 1.5, (0, 1, 0))
        self.rects[4].rotation = transformations.quaternion_about_axis(math.pi * 0.5, (1, 0, 0))
        self.rects[5].rotation = transformations.quaternion_about_axis(math.pi * 1.5, (1, 0, 0))

    def update_color(self):
        for rect in self.rects:
            rect.color = self.color

    def update_position_and_size(self):
        self.rects[0].size = (self.size[0], self.size[1])
        self.rects[1].size = (self.size[0], self.size[1])
        self.rects[2].size = (self.size[2], self.size[1])
        self.rects[3].size = (self.size[2], self.size[1])
        self.rects[4].size = (self.size[0], self.size[2])
        self.rects[5].size = (self.size[0], self.size[2])

        rect_offset_vecs = np.array([
            [0, 0, 0],
            [-self.size[0], 0, self.size[2]],
            [0, 0, self.size[0]],
            [-self.size[2], 0, 0],
            [0, 0, self.size[1]],
            [0, self.size[2], 0]
        ], np.float32)

        for i, rect in enumerate(self.rects):
            rect_rot = rect.rotation
            rect.position = transformations.rotate_vector(
                rect_rot, rect_offset_vecs[i]
            ) + self.position

    def apply_updates(self):
        for rect in self.rects:
            rect.update()

    def update(self):
        self.update_rotation()
        self.update_color()
        self.update_position_and_size()
        self.apply_updates()

    def drop(self):
        for rect in self.rects:
            rect.drop()


if __name__ == '__main__':
    from flowtrail.app import App
    app = App()
    c = Cuboid()
    c.update()
    app.run()
