import config


class Fps:
    def __init__(self):
        super(Fps, self).__init__()
        self.paused = False
        self.rotate_speed = 0.02
        self.move_speed = 1.0

    @property
    def cam(self):
        return config.app.scene.camera

    def pause(self):
        self.paused = True

    def unpause(self):
        self.paused = False

    def mouse_scroll(self, x, value):
        if self.paused:
            return
        self.cam.forward(value)

    def key_down(self, key):
        if self.paused:
            return
        if key == 32:
            self.move_speed = 10.0
            self.rotate_speed = 0.04

    def key_up(self, key):
        if self.paused:
            return
        if key == 32:
            self.move_speed = 0.1
            self.rotate_speed = 0.01

    def update(self):
        if self.paused:
            return
        keys = config.app.input.keys
        if 65 in keys:
            self.cam.right(-self.move_speed)
        if 68 in keys:
            self.cam.right(self.move_speed)
        if 87 in keys:
            self.cam.forward(self.move_speed)
        if 83 in keys:
            self.cam.forward(-self.move_speed)
        if 262 in keys:
            self.cam.yaw(-self.rotate_speed)
        if 263 in keys:
            self.cam.yaw(self.rotate_speed)
        if 265 in keys:
            self.cam.pitch(self.rotate_speed)
        if 264 in keys:
            self.cam.pitch(-self.rotate_speed)
        if 324 in keys:
            self.cam.right(-self.move_speed * 8)
        if 326 in keys:
            self.cam.right(self.move_speed * 8)
        if 322 in keys:
            self.cam.up(-self.move_speed * 8)
        if 266 in keys:
            self.cam.up(self.move_speed * 16)
        if 328 in keys:
            self.cam.up(self.move_speed * 8)
        if 267 in keys:
            self.cam.up(-self.move_speed * 16)
        if 321 in keys:
            self.cam.up(-self.move_speed * 8)
            self.cam.right(-self.move_speed * 8)
        if 323 in keys:
            self.cam.up(-self.move_speed * 8)
            self.cam.right(self.move_speed * 8)
        if 327 in keys:
            self.cam.up(self.move_speed * 8)
            self.cam.right(-self.move_speed * 8)
        if 329 in keys:
            self.cam.up(self.move_speed * 8)
            self.cam.right(self.move_speed * 8)
