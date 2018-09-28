#version 330 core
#define PI 3.14159265359f
uniform vec3 camPos;
uniform vec3 lightPos;
uniform vec3 lightIntensity;
uniform vec3 albedo;
uniform vec3 rho_s;
uniform vec3 rho_d;
uniform float exponent;
in vec3 vNormal;
in vec3 vPos;
out vec3 phongColor;
void main() {
	// TODO: Implement this
	vec3 wo = normalize(vPos -camPos);
	vec3 wi = normalize(lightPos-vPos);
	float thetai = dot(wi,normalize(vNormal));
	float thetao = dot(-wo,normalize(vNormal));
	if(thetai<=0.f||thetao<=0.f){
		phongColor = vec3(0.f);
	}
	else{
		vec3 wr = reflect(wi,normalize(vNormal));
		float cosa = max(dot(wr,wo),0.f);
		vec3 phong = rho_d/PI + rho_s*(exponent+2)/2/PI*pow(cosa,exponent);
		phongColor = phong*thetai*lightIntensity/pow(length(vPos-lightPos),2);
	}	
}