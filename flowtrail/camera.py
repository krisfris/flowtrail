import numpy as np
from functools import lru_cache
import flowtrail.transformations as transformations


@lru_cache(maxsize=1)
def get_view_matrix(position, rotation):
    position_matrix = transformations.translation_matrix(position)
    rotation_matrix = transformations.quaternion_matrix(rotation)
    camera_matrix = transformations.concatenate_matrices(
        position_matrix, rotation_matrix
    )
    view_matrix = transformations.inverse_matrix(camera_matrix)
    m = view_matrix
    return m.astype(np.float32).flatten('F')


class Camera:
    def __init__(self, position=None, rotation=None):
        self._position = position if position is not None else np.array([0, 0, 30], np.float32)
        self._rotation = rotation if rotation is not None else  np.array([1,0,0,0], np.float32)

    def birdseye(self):
        pass

    def set_camera(self, pos, rot):
        self._position = np.array(pos, np.float32)
        self._rotation = np.array(rot, np.float32)

    def copy(self):
        return Camera(self.position, self.rotation)

    @property
    def position(self):
        return np.copy(self._position)

    @position.setter
    def position(self, val):
        self._position = np.array(val, np.float32)

    @property
    def orientation(self):
        return np.copy(self._rotation)

    @orientation.setter
    def orientation(self, val):
        self._rotation = np.array(val, np.float32)

    @property
    def rotation(self):
        return self._rotation

    @rotation.setter
    def rotation(self, val):
        self._rotation = val

    def forward(self, x):
        v = np.array((0.0, 0.0, 0.0, 1.0), np.float32)
        v = transformations.quaternion_multiply(transformations.quaternion_multiply(self._rotation, v),
                                                transformations.quaternion_conjugate(self._rotation))
        self._position += v[1:] * -x

    def right(self, x):
        v = np.array((0.0, 1.0, 0.0, 0.0), np.float32)
        v = transformations.quaternion_multiply(transformations.quaternion_multiply(self._rotation, v),
                                                transformations.quaternion_conjugate(self._rotation))
        self._position += v[1:] * x

    def up(self, x):
        v = np.array((0.0, 0.0, 1.0, 0.0), np.float32)
        v = transformations.quaternion_multiply(transformations.quaternion_multiply(self._rotation, v),
                                                transformations.quaternion_conjugate(self._rotation))
        self._position += v[1:] * x

    def yaw(self, angle):
        q = transformations.quaternion_about_axis(angle, [0, 1, 0])
        q = transformations.quaternion_multiply(q, self._rotation)
        q = q / np.linalg.norm(q)
        self._rotation = q

    def pitch(self, angle):
        q = transformations.quaternion_about_axis(angle, [1, 0, 0])
        q = transformations.quaternion_multiply(self._rotation, q)
        self._rotation = q

    def get_matrix(self):
        return get_view_matrix(tuple(self._position), tuple(self._rotation))

    def get_right(self):
        x = transformations.quaternion_multiply(self._rotation, np.array((1.0, 0, 0, 0)))
        x = x / np.linalg.norm(x)
        return x[:3]

    def get_up(self):
        x = transformations.quaternion_multiply(self._rotation, np.array((0.0, 1.0, 0, 0)))
        x = x / np.linalg.norm(x)
        return x[:3]

    def get_forward(self):
        x = transformations.quaternion_multiply(self._rotation, np.array((0.0, 0.0, -1.0, 0)))
        x = x / np.linalg.norm(x)
        return x[:3]
