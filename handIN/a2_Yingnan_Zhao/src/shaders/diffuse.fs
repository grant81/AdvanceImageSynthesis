#version 330 core

#define PI 3.14159265359f

uniform vec3 camPos;
uniform vec3 lightPos;
uniform vec3 lightIntensity;
uniform vec3 albedo;
in vec3 vNormal;
in vec3 vPos;
out vec3 diffuseColor;

void main() {
	// TODO: Implement this
	vec3 wo = vPos-camPos;
	vec3 wi = lightPos-vPos;
	float thetao = dot(normalize(-wo),vNormal);
	float thetai = dot(normalize(wi),vNormal);
	if(thetai<=0.0||thetao<=0.0){
		diffuseColor = vec3(0);
	}
	else{
		vec3 val = albedo/PI*thetai;
		diffuseColor= val*lightIntensity/pow(length(vPos-lightPos),2);
	}
	
	
}