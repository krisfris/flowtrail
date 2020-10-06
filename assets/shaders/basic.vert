#version 330 core

layout(location = 0) in vec3 aVert;
layout(location = 1) in vec4 color;

//uniform mat4 uMVMatrix;
uniform mat4 projection;
uniform mat4 view;

out vec4 thePosition;
smooth out vec4 theColor;

void main() {
    gl_Position = projection * view * vec4(aVert, 1.0); 
    thePosition = vec4(aVert, 1.0);
    theColor = color;
}
