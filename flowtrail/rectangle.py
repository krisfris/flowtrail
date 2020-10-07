import numpy as np

import flowtrail.transformations as transformations
import config


vertices = np.array([
    0, 0, 0,
    0, 0, 0, 1,
    0, -1, 0,
    0, 0, 0, 1,
    1, -1, 0,
    0, 0, 0, 1,
    1, -1, 0,
    0, 0, 0, 1,
    1, 0, 0,
    0, 0, 0, 1,
    0, 0, 0,
    0, 0, 0, 1,
], np.float32)


def scale_matrix_3d(size):
    return np.array([[size[0], 0, 0], [0, size[1], 0], [0, 0, size[2]]])


def scale_matrix_2d(size):
    return scale_matrix_3d(np.concatenate((size, [0])))


class Rectangle:
    def __init__(self):
        self.position = (0,) * 3
        self.size = (10,) * 2
        self.color = (0, 1, 0, 1)
        self.rotation = (1, 0, 0, 0)

        self.handle = config.app.renderer.triangle_renderer.datavec.register(vertices.size)

    def update(self):
        data = np.copy(vertices)
        m_rot = transformations.quaternion_matrix(self.rotation)[:-1, :-1]
        m_scale = scale_matrix_2d(self.size)

        for i in range(0, len(data), 7):
            data[i:i+3] = np.matmul(m_rot, np.matmul(m_scale, data[i:i+3])) + self.position
            data[i+3:i+7] = self.color

        config.app.renderer.triangle_renderer.datavec.update_data(self.handle, data)

    def drop(self):
        config.app.renderer.triangle_renderer.datavec.erase(self.handle)


if __name__ == '__main__':
    from flowtrail.app import App
    app = App()
    r = Rectangle()
    r.update()
    app.run()
