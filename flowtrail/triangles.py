import OpenGL
from OpenGL.GL import *

import numpy, math, sys, os
import numpy as np
import flowtrail.glutils as glutils

from ctypes import sizeof, c_float, c_void_p, c_uint, string_at

import config
from flowtrail.smartvector import SmartVector


strVS = open('assets/shaders/basic.vert').read()
strFS = open('assets/shaders/basic.frag').read()


class TriangleRenderer:
    def __init__(self):
        self.program = glutils.loadShaders(strVS, strFS)

        glUseProgram(self.program)

        self.pMatrixUniform = glGetUniformLocation(self.program,
                                                   b'projection')
        #self.mvMatrixUniform = glGetUniformLocation(self.program, 
                                                  #b'uMVMatrix')

        self.view_matrix_uniform = glGetUniformLocation(self.program, b'view')
        self.viewpos_uniform = glGetUniformLocation(self.program, b'viewPos')
        self.dirlight_direction_uniform = glGetUniformLocation(self.program, b'dirLight.direction')
        self.dirlight_ambient_uniform = glGetUniformLocation(self.program, b'dirLight.ambient')
        self.dirlight_diffuse_uniform = glGetUniformLocation(self.program, b'dirLight.diffuse')
        self.dirlight_specular_uniform = glGetUniformLocation(self.program, b'dirLight.specular')

        # texture 
        self.tex2D = glGetUniformLocation(self.program, b'tex2D')

        # define triange strip vertices 
        self.datavec = SmartVector()

        self.vao = glGenVertexArrays(1)
        self.vertexBuffer = glGenBuffers(1)

    def update(self):
        # set up vertex array object (VAO)

        view_matrix = config.app.scene.camera.get_matrix()

        self.vertex_data = self.datavec.data()

        glBindVertexArray(self.vao)
        # vertices
        glBindBuffer(GL_ARRAY_BUFFER, self.vertexBuffer)
        # set buffer data 
        glBufferData(GL_ARRAY_BUFFER, 4*len(self.vertex_data), self.vertex_data,
                     GL_STREAM_DRAW)
        # enable vertex array
        glEnableVertexAttribArray(0)
        glEnableVertexAttribArray(1)
        # set buffer data pointer
        stride = 7 * 4
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, stride, None)
        glVertexAttribPointer(1, 4, GL_FLOAT, GL_FALSE, stride, c_void_p(4 * 3))

        # unbind VAO
        glBindVertexArray(0)

        # use shader
        glUseProgram(self.program)

        # set proj matrix
        glUniformMatrix4fv(self.pMatrixUniform, 1, GL_FALSE, config.app.window.pMatrix)

        # set modelview matrix
        #glUniformMatrix4fv(self.mvMatrixUniform, 1, GL_FALSE, mvMatrix)

        glUniformMatrix4fv(self.view_matrix_uniform, 1, GL_FALSE, view_matrix)

        cp = config.app.scene.camera._position
        glUniform3f(self.viewpos_uniform, cp[0], cp[1], cp[2])
        glUniform3f(self.dirlight_direction_uniform, 0.6, 0.3, 1.0)
        glUniform3f(self.dirlight_ambient_uniform, 0.4, 0.4, 0.4)
        glUniform3f(self.dirlight_diffuse_uniform, 0.6, 0.6, 0.6)
        glUniform3f(self.dirlight_specular_uniform, 1.0, 1.0, 1.0)

        # bind VAO
        glBindVertexArray(self.vao)
        # draw
        glDrawArrays(GL_TRIANGLES, 0, int(len(self.vertex_data) / 7))

        glDisableVertexAttribArray(0)
        glDisableVertexAttribArray(1)
        # unbind VAO
        glBindVertexArray(0)

    def drop(self):
        pass
