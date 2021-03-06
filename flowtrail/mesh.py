import numpy as np
import config


class TriangleMesh:
    def __init__(self, data):
        self.data = []
        scale = 1
        pos = [0, 0, -100]
        for a, b, c, colorname in data:
            if colorname == 'green':
                color = [0, 1, 0, 1]
            elif colorname == 'blue':
                color = [0, 0, 1, 1]
            elif colorname == 'yellow':
                color = [1, 1, 0, 1]
            elif colorname == 'grey':
                color = [0.5, 0.5, 0.5, 1]
            else:
                color = [1, 1, 1, 1]
            for x, y, z in [a, b, c]:
                self.data.extend([pos[0] + x * scale, pos[1] + z * scale, pos[2] + y * scale])
                self.data.extend(color)
        self.data = np.array(self.data, np.float32)
        self.render_id = config.app.renderer.triangle_renderer.datavec.register(len(self.data))

    def update(self):
        config.app.renderer.triangle_renderer.datavec.update_data(self.render_id, self.data)

    def drop(self):
        config.app.renderer.triangle_renderer.datavec.erase(self.render_id)

    def hide(self):
        config.app.renderer.triangle_renderer.datavec.zero(self.render_id)

