#version 330 core

layout(location = 0) in vec3 position;
layout(location = 1) in vec2 uv;

out vec3 worldPos;
out vec2 texCoords;
void main()
{
	texCoords = uv;
	gl_Position = vec4(position,1.f);
	worldPos = position;
}
