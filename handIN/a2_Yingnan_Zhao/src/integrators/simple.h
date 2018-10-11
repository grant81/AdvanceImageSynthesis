/*
    This file is part of TinyRender, an educative rendering system.

    Designed for ECSE 446/546 Realistic/Advanced Image Synthesis.
    Derek Nowrouzezahrai, McGill University.
*/

#pragma once

TR_NAMESPACE_BEGIN

/**
 * Simple direct illumination integrator.
 */
struct SimpleIntegrator : Integrator {
    explicit SimpleIntegrator(const Scene& scene) : Integrator(scene) { }

    v3f render(const Ray& ray, Sampler& sampler) const override {
        v3f Li(0.f);
        // TODO: Implement this
		v3f position = scene.getFirstLightPosition();
		v3f intensity = scene.getFirstLightIntensity();
		SurfaceInteraction i;
		SurfaceInteraction shadow;
		if (scene.bvh->intersect(ray, i)) {
			v3f x = i.p;
			v3f lightDir = glm::normalize(position - x);
			Ray shadowRay = Ray(x, lightDir);
			shadowRay.max_t = glm::length(position - x);//distance between x and light position
			if (scene.bvh->intersect(shadowRay, shadow)) {//check if the ray from x was blocked
				return Li;
			}
			else {
				i.wi = i.frameNs.toLocal(lightDir);
				v3f bsdf = getBSDF(i)->eval(i);
				v3f Lo = intensity / glm::length2(x - position);
				Li = bsdf * Lo;
				return Li;
			}
			
		}
		else {
			return Li;
		}
        
    }
};

TR_NAMESPACE_END