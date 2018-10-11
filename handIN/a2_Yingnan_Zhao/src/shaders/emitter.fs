/*
    This file is part of TinyRender, an educative rendering system.

    Designed for ECSE 446/546 Realistic/Advanced Image Synthesis.
    Derek Nowrouzezahrai, McGill University.
*/

#version 330 core

in vec3 vPos;
in vec3 vNormal;
out vec3 color;

/*
    This fragment shader is only there to suppress warning when
    directly shading an emitter fragment. Do _not_ delete this file.
*/

void main() {
    vec3 a = vec3(vPos);        // Suppress warning
    vec3 b = vec3(vNormal);     // Suppress warning
    color = vec3(1.0,1.0,1.0);
}
