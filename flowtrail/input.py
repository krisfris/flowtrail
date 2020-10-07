import flowtrail.glfw as glfw
import config


class Input:
    def __init__(self):
        self.keys = set()

    def key_down(self, key, scancode, mods):
        if key == glfw.GLFW_KEY_ESCAPE:
            config.app.quit()

    def key_up(self, key, scancode, mods):
        pass

    def update(self):
        pass

    def drop(self):
        pass

    def keyboard(self, win, key, scancode, action, mods):
        if action == glfw.GLFW_PRESS or action == glfw.GLFW_REPEAT:
            self.keys.add(key)
            self.key_down(key, scancode, mods)
        elif action == 0:
            self.keys.remove(key)
            self.key_up(key, scancode, mods)
