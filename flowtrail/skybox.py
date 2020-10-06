import glob

import OpenGL
from OpenGL.GL import *
from PIL import Image

import numpy, math, sys, os
import numpy as np
import flowtrail.glutils as glutils

import config
from flowtrail.smartvector import SmartVector


strVS = open('assets/shaders/skybox.vert').read()
strFS = open('assets/shaders/skybox.frag').read()

vertices = [
    -1.0,  1.0, -1.0,
    -1.0, -1.0, -1.0,
     1.0, -1.0, -1.0,
     1.0, -1.0, -1.0,
     1.0,  1.0, -1.0,
    -1.0,  1.0, -1.0,

    -1.0, -1.0,  1.0,
    -1.0, -1.0, -1.0,
    -1.0,  1.0, -1.0,
    -1.0,  1.0, -1.0,
    -1.0,  1.0,  1.0,
    -1.0, -1.0,  1.0,

     1.0, -1.0, -1.0,
     1.0, -1.0,  1.0,
     1.0,  1.0,  1.0,
     1.0,  1.0,  1.0,
     1.0,  1.0, -1.0,
     1.0, -1.0, -1.0,

    -1.0, -1.0,  1.0,
    -1.0,  1.0,  1.0,
     1.0,  1.0,  1.0,
     1.0,  1.0,  1.0,
     1.0, -1.0,  1.0,
    -1.0, -1.0,  1.0,

    -1.0,  1.0, -1.0,
     1.0,  1.0, -1.0,
     1.0,  1.0,  1.0,
     1.0,  1.0,  1.0,
    -1.0,  1.0,  1.0,
    -1.0,  1.0, -1.0,

    -1.0, -1.0, -1.0,
    -1.0, -1.0,  1.0,
     1.0, -1.0, -1.0,
     1.0, -1.0, -1.0,
    -1.0, -1.0,  1.0,
     1.0, -1.0,  1.0
]


class Skybox:
    def __init__(self):
        self.program = glutils.loadShaders(strVS, strFS)

        glUseProgram(self.program)

        self.load_texture()

        self.pMatrixUniform = glGetUniformLocation(self.program, b'projection')
        #self.mvMatrixUniform = glGetUniformLocation(self.program, #b'uMVMatrix')
        self.view_matrix_uniform = glGetUniformLocation(self.program, b'view')

        self.vertex_data = np.array(vertices, np.float32)

    def load_texture(self):
        self.texture_id = glGenTextures(1)
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_CUBE_MAP, self.texture_id)

        skybox_name = 'nightsky'
        l = ['right', 'left', 'top', 'bottom', 'back', 'front']
        files = [glob.glob(f'assets/skyboxes/{skybox_name}/{x}.*')[0] for x in l]
        for i, filename in enumerate(files):
            img = Image.open(filename)
            #img = Image.open(filename).rotate(180).transpose(Image.FLIP_LEFT_RIGHT)
            mode = GL_RGB if img.mode == 'RGB' else GL_RGBA
            glTexImage2D(GL_TEXTURE_CUBE_MAP_POSITIVE_X + i, 0, mode, img.size[0], img.size[1],
                         0, mode, GL_UNSIGNED_BYTE, np.asanyarray(img))

        glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_WRAP_R, GL_CLAMP_TO_EDGE)

        glBindTexture(GL_TEXTURE_CUBE_MAP, 0)

    def update(self):
        glDepthMask(GL_FALSE)
        view_matrix = config.app.scene.camera.get_matrix().copy()
        view_matrix[12] = 0.0
        view_matrix[13] = 0.0
        view_matrix[14] = 0.0


        self.vao = glGenVertexArrays(1)
        glBindVertexArray(self.vao)
        # vertices
        self.vertexBuffer = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vertexBuffer)
        # set buffer data 
        glBufferData(GL_ARRAY_BUFFER, 4*len(self.vertex_data), self.vertex_data, 
                     GL_STREAM_DRAW)
        # enable vertex array
        glEnableVertexAttribArray(0)
        # set buffer data pointer
        stride = 3 * 4
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, stride, None)

        # unbind VAO
        glBindVertexArray(0)

        # use shader
        glUseProgram(self.program)

        # set uniforms

        #pMatrix = glutils.perspective(app.window.fov, app.window.aspect, 0.1, 100.0)
        glUniformMatrix4fv(self.pMatrixUniform, 1, GL_FALSE, config.app.window.pMatrix)
        #glUniformMatrix4fv(self.mvMatrixUniform, 1, GL_FALSE, mvMatrix)
        glUniformMatrix4fv(self.view_matrix_uniform, 1, GL_FALSE, view_matrix)

        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_CUBE_MAP, self.texture_id)

        # bind VAO
        glBindVertexArray(self.vao)
        # draw
        glDrawArrays(GL_TRIANGLES, 0, int(len(self.vertex_data) / 3))

        glDisableVertexAttribArray(0)
        # unbind VAO
        glBindVertexArray(0)
        glDepthMask(GL_TRUE)

    def drop(self):
        glDeleteTextures(1, self.texture_id)
