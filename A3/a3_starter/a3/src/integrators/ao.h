/*
    This file is part of TinyRender, an educative rendering system.

    Designed for ECSE 446/546 Realistic/Advanced Image Synthesis.
    Derek Nowrouzezahrai, McGill University.
*/

#pragma once

TR_NAMESPACE_BEGIN
/**
 * Ambient occlusion integrator
 */
#define AO_SPHERE 1
#define AO_HEMISPHERE 2
#define AO_COSINE 3
struct AOIntegrator : Integrator {
    explicit AOIntegrator(const Scene& scene) : Integrator(scene) { }

    v3f render(const Ray& ray, Sampler& sampler) const override {
		int pdfSelection = AO_COSINE;
        v3f Li(0.f);
	    // TODO: Implement this
		v3f position = scene.getFirstLightPosition();
		v3f intensity = scene.getFirstLightIntensity();
		SurfaceInteraction i;
		SurfaceInteraction shadow;
		if (scene.bvh->intersect(ray, i)) {
			//solve MC AO
			v3f x = i.p;
			v3f wi;
			float pdf;

			if (pdfSelection == AO_SPHERE) {
				wi = Warp::squareToUniformSphere(sampler.next2D());
				pdf = Warp::squareToUniformSpherePdf();
			}
			else if (pdfSelection == AO_HEMISPHERE) {
				wi = Warp::squareToUniformHemisphere(sampler.next2D());
				pdf = Warp::squareToUniformHemispherePdf(wi);
			}
			else {
				wi = Warp::squareToCosineHemisphere(sampler.next2D());
				pdf = Warp::squareToCosineHemispherePdf(wi);
			}
			
			float cosi = fmax(wi.z, 0);
			wi = glm::normalize(i.frameNs.toWorld(wi));
			Ray shadowRay = Ray(x, wi);
			shadowRay.max_t = scene.aabb.getBSphere().radius/2;//distance between x and light position
			if (scene.bvh->intersect(shadowRay, shadow)) {//check if the ray from x was blocked
				return Li;
			}
			else {
				Li = v3f(INV_PI*cosi / pdf);
				return Li;
			}

		}

        return Li;
    }
};

TR_NAMESPACE_END