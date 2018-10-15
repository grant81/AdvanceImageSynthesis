/*
    This file is part of TinyRender, an educative PBR system.
    Designed for ECSE 446/546 Realistic Image Synthesis, McGill University.

    Copyright (c) 2018 by Derek Nowrouzezahrai and others.
*/
#version 330 core

// UNIFORMS
// ------------------------------------------------------------------
uniform sampler2D texturePosition;
uniform sampler2D textureNormal;
uniform mat4 projection;

// INPUT/OUTPUT
// ------------------------------------------------------------------
in vec2 texCoords;

out vec3 color;

// CONSTANTS
// ------------------------------------------------------------------
const int N_SAMPLES = 32;
float RADIUS = 0.14;
float BIAS = 0.0;

const float PI = 3.1415926535897932384626433832795;
const float INV_PI = 1.0 / PI;

// RANDOM NUMBER GENERATOR (RNG)
// ------------------------------------------------------------------
float seed;
float oldrand() { return fract( sin( seed++ ) * 43758.5453123 );}

vec4 seedvec;
float rand()
{
    const vec4 q = vec4(1225.0,1585.0,2457.0,2098.0);
    const vec4 r = vec4(1112.0,367.0,92.0,265.0);
    const vec4 a = vec4(3423.0,2646.0,1707.0,1999.0);
    const vec4 m = vec4(4194287.0,4194277.0, 4194191.0, 4194167.0);

    vec4 beta = floor(seedvec / q);
    vec4 p = a * (seedvec- beta * q) - beta * r;
    beta = (sign(-p) + vec4(1.0)) * vec4(0.5) * m;
    seedvec = (p + beta);

    return fract(dot(seedvec / m,  vec4(1.0, -1.0, 1.0, -1.0)));
}

void setRNGSeed()
{
    float w = textureSize(texturePosition,0).x;
    float h = textureSize(texturePosition,0).y;
    seed = (h*gl_FragCoord.x / w + gl_FragCoord.y / h);
    seedvec = vec4(oldrand() * 4194304.0,
                   oldrand() * 4194304.0,
                   oldrand() * 4194304.0,
                   oldrand() * 4194304.0);
}

// UTILS
// ------------------------------------------------------------------

vec3 squareToUniformHemisphere()
{
    // generate a random direction in the hemisphere aligned to z+
    float z = rand();
    float r = sqrt(max(0.0, 1.0 - z*z));
    float phi = 2.0 * PI * rand();
    vec3 v = vec3(r * cos(phi), r * sin(phi), z);
    return v;
}

float squareToUniformHemispherePdf()
{
    return 1.0 / (2.0 * PI);
}

vec3 getTangent(vec3 normal)
{
    vec3 rvec = vec3(rand()*2.0 - 1.0, rand()*2.0 - 1.0, 0.0f); // rotate around z-axis (in tangent space)
    return normalize(rvec - normal * dot(rvec,normal)); // rotate
}

// MAIN
// ------------------------------------------------------------------
void main()
{
    setRNGSeed();

    /**
    * 1) Get the position and normal of the shading point (screen space) from the GBuffer.
    */
	vec4 position = texture(texturePosition,texCoords);
	vec4 normal = texture(textureNormal,texCoords);
    /**
    * 1) Build the shading normal's frame (TBN).
         ( use getTangent() )
    */
	vec3 tangent = normalize(getTangent(normal.xyz));
	vec3 bitangent = cross(normal.xyz,tangent);
	mat3 tbn = mat3(tangent,bitangent,normal);
    /**
    For each sample:
    * 1) Get a sample direction (view space).
    * 2) Align the sample hemisphere to the shading normal.
    * 3) Place the sample at the shading point (use the RADIUS constant).
    * 4) Get the depth value at the sample's position using the depth buffer.
    *    - Project the sample to screen space ie. pixels (NDC).
    *    - Transform the sample in NDC coordinates [-1,1] to texture coordinates [0,1].
    * 5) Check for occlusion using the sample's depth value and the depth value at the sample's position.
         (use some epsilon via the BIAS constant)
    */
	color = vec3(0.0);
	for(int i =0; i< N_SAMPLES;i++ ){
		vec3 wi = squareToUniformHemisphere();
		float pdf = squareToUniformHemispherePdf();
		float cosTheta = wi.z;

		vec3 sample = tbn*wi;
		sample = sample*RADIUS+position.xyz;

		vec4 sampleScreenS =  projection* vec4(sample,1);
		sampleScreenS.xyz /= sampleScreenS.w;
		sampleScreenS.xyz = sampleScreenS.xyz/2+0.5f;
		float sampleDepth = texture(texturePosition,sampleScreenS.xy).z;
		if(sampleDepth >(sample.z+BIAS)){
			color += vec3(INV_PI/pdf*cosTheta);
		}
		
	}
	color /= N_SAMPLES;
	color = 1 - color;
}
