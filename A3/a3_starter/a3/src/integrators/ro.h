/*
    This file is part of TinyRender, an educative rendering system.

    Designed for ECSE 446/546 Realistic/Advanced Image Synthesis.
    Derek Nowrouzezahrai, McGill University.
*/

#pragma once
#include <random>

TR_NAMESPACE_BEGIN

/**
 * Reflection occlusion integrator
 */
struct ROIntegrator : Integrator {

    float m_exponent;

    explicit ROIntegrator(const Scene& scene) : Integrator(scene) {
        m_exponent = scene.config.integratorSettings.ro.exponent;
    }

    inline v3f reflect(const v3f& d) const {
        return v3f(-d.x, -d.y, d.z);
    }

    v3f render(const Ray& ray, Sampler& sampler) const override {
        v3f Li(0.f);
		// TODO: Implement this
		SurfaceInteraction i;
		SurfaceInteraction shadow;
		if (scene.bvh->intersect(ray, i)) {
			
			v3f x = i.p;
			v3f	wi = Warp::squareToPhongLobe(sampler.next2D(), m_exponent);
			float pdf = Warp::squareToPhongLobePdf(wi, m_exponent);
			v3f wo = i.wo; 
			v3f wr = reflect(wo);
			wi = glm::toMat4(glm::quat(v3f(0, 0, 1), wr)) * v4f(wi, 1);//??
			float cosalpha = fmax(glm::dot(glm::normalize(wr), glm::normalize(wi)), 0.f);
			wi = glm::normalize(wi);
			float cosi = fmax(wi.z, 0);
			Ray shadowRay = Ray(x, i.frameNs.toWorld(wi));
			if (scene.bvh->intersect(shadowRay, shadow)) {//check if the ray from x was blocked
				return v3f(0);
			}
			else {

				Li = v3f((m_exponent + 2) *INV_TWOPI*fmax(pow(cosalpha, m_exponent), 0)*cosi / pdf);
				return Li;
			}

		}
		
		return Li;
	
    }
};

TR_NAMESPACE_END