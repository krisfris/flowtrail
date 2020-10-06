import os
import numpy as np
from collections import namedtuple
from PIL import Image
import OpenGL
from OpenGL.GL import *

from flowtrail import glfw
import flowtrail.glutils as glutils
import config


WindowState = namedtuple(
    'WindowState', ['is_fullscreen', 'x', 'y', 'width', 'height']
)


def load_window_icon_image():
    img = Image.open('assets/images/icon.png')
    img.load()
    data = np.asarray(img, dtype='int32')
    width, height, depth = data.shape
    image = glfw.GLFWimage()
    image.wrap((width, height, data))
    return image


class Window:
    def __init__(self):
        # save current working directory
        cwd = os.getcwd()

        # initialize glfw - this changes cwd
        glfw.glfwInit()

        # restore cwd
        os.chdir(cwd)

        # version hints
        glfw.glfwWindowHint(glfw.GLFW_CONTEXT_VERSION_MAJOR, 3)
        glfw.glfwWindowHint(glfw.GLFW_CONTEXT_VERSION_MINOR, 3)
        glfw.glfwWindowHint(glfw.GLFW_OPENGL_FORWARD_COMPAT, GL_TRUE)
        glfw.glfwWindowHint(glfw.GLFW_OPENGL_PROFILE,
                            glfw.GLFW_OPENGL_CORE_PROFILE)
        glfw.glfwWindowHint(glfw.GLFW_SAMPLES, 4)


        window_icon_image = load_window_icon_image()

        # make a window
        self.update_size(860, 640)
        self.win = glfw.glfwCreateWindow(self.width, self.height,
                                         b'flowtrail')

        glfw.glfwSetWindowIcon(self.win, 1, window_icon_image)

        # make context current
        glfw.glfwMakeContextCurrent(self.win)

        #self.onSize(self.win, self.width, self.height)

        # initialize GL
        glViewport(0, 0, self.width, self.height)
        glEnable(GL_DEPTH_TEST)
        #glEnable(GL_COLOR_MATERIAL)
        #glEnable(GL_NORMALIZE)  
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        glClearColor(*config.BACKGROUND_COLOR)

        if glfw.glfwJoystickPresent(0):
            print('Joystick found', 0, glfw.glfwGetJoystickName(0))

        # set callbacks
        glfw.glfwSetWindowSizeCallback(self.win, self.onSize)
        glfw.glfwSetJoystickCallback(self.joystick_callback)

        # exit flag
        self.exitNow = False

        glfw.glfwSetTime(0)
        self.t = 0.0

        self.last_state = None

        glfw.glfwSetKeyCallback(self.win, config.app.input.keyboard)

    def joystick_callback(self, joy, event):
        print(joy, event)
        name = glfw.glfwGetJoystickName(joy)
        if event == glfw.GLFW_CONNECTED:
            print('joystick connected', joy, name)
        elif event == glfw.GLFW_DISCONNECTED:
            print('joystick disconnected', joy, name)

    def set_input_callbacks(self, mouse_button, scroll, key, motion, char):
        glfw.glfwSetMouseButtonCallback(self.win, mouse_button)
        glfw.glfwSetScrollCallback(self.win, scroll)
        glfw.glfwSetKeyCallback(self.win, key)
        glfw.glfwSetCursorPosCallback(self.win, motion)
        glfw.glfwSetCharCallback(self.win, char)

    def fullscreen(self, yes):
        if yes:
            x, y = glfw.glfwGetWindowPos(self.win)
            self.last_state = WindowState(True, x, y, self.width, self.height)

            glfw._glfw.glfwSetWindowMonitor(
                self.win, glfw.glfwGetPrimaryMonitor(), 0, 0, 1600,900, -1
            )
        elif self.last_state is not None:
            _, x, y, w, h = self.last_state
            glfw._glfw.glfwSetWindowMonitor(self.win, 0, x, y, w, h, -1)
            self.last_state = None

    def get_viewport(self):
        viewport = glGetIntegerv(GL_VIEWPORT)
        return np.array(viewport, 'i')

    def is_fullscreen(self):
        return self.last_state and self.last_state.is_fullscreen

    def get_size(self):
        return self.width, self.height

    def update_size(self, width, height):
        self.width = width
        self.height = height
        self.aspect = width/float(height)
        self.fov = 45.0
        self.near = 0.1
        self.far = 1000.0
        self.pMatrix = glutils.perspective(self.fov, self.aspect, self.near, self.far)
        glViewport(0, 0, self.width, self.height)

    def onSize(self, win, width, height):
        self.update_size(width, height)
        config.app.renderer.window_size_changed(width, height)
        config.app.scene.window_size_changed(width, height)

    def update(self):
        # update every x seconds
        currT = glfw.glfwGetTime()
        # clear

#        mvMatrix = glutils.lookAt([0.0, 0.0, -2.0], [0.0, 0.0, 0.0],
#                                  [0.0, 1.0, 0.0])
        #mvMatrix = app.scene.camera.get_matrix()
        #app.renderer.step(self.pMatrix, mvMatrix)

        glfw.glfwSwapBuffers(self.win)
        # Poll for and process events
        glfw.glfwPollEvents()

    def drop(self):
        glfw.glfwTerminate()
