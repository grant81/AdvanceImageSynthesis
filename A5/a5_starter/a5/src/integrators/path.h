/*
    This file is part of TinyRender, an educative rendering system.

    Designed for ECSE 446/546 Realistic/Advanced Image Synthesis.
    Derek Nowrouzezahrai, McGill University.
*/

#pragma once

TR_NAMESPACE_BEGIN

/**
 * Path tracer integrator
 */
struct PathTracerIntegrator : Integrator {
    explicit PathTracerIntegrator(const Scene& scene) : Integrator(scene) {
        m_isExplicit = scene.config.integratorSettings.pt.isExplicit;
        m_maxDepth = scene.config.integratorSettings.pt.maxDepth;
        m_rrDepth = scene.config.integratorSettings.pt.rrDepth;
        m_rrProb = scene.config.integratorSettings.pt.rrProb;
    }


    v3f renderImplicit(const Ray& ray, Sampler& sampler, SurfaceInteraction& hit) const {
        v3f Li(1.f);
		Ray r = ray;
		int hitEmitter = 0;
		int count = 0;
        // TODO: Implement this
		pathTracer(sampler, hit, Li, count,hitEmitter);
		v3f emission = getEmission(hit);
		if (hitEmitter==0) {
			return v3f(0.f);
		}
        return Li;
    }
	void pathTracer(Sampler& sampler, SurfaceInteraction& hit, v3f& Li, int depth,int& hitEmitter) const{
		if (depth <= m_maxDepth) {
			v3f emission = getEmission(hit);
			if (emission != v3f(0.f) && glm::dot(v3f(0, 0, 1), hit.wo) > 0) {
				Li *= emission;
				hitEmitter = 1;
			}
			else {
				float pdf;
				v3f bsdf = getBSDF(hit)->sample(hit, sampler.next2D(), &pdf);
				Li *= bsdf;
				v3f wi = glm::normalize(hit.frameNs.toWorld(hit.wi));
				Ray next = Ray(hit.p, wi);
				if (scene.bvh->intersect(next, hit)) {
					depth += 1;
					pathTracer(sampler, hit, Li, depth,hitEmitter);
				}
				else {
					Li = v3f(0.f);
				}
			}
		}
		
	}
	v3f indirectTracer(Sampler& sampler, SurfaceInteraction& hit, int depth) const {
		float rusPdf = 1.f;
		if (m_maxDepth == -1) {
			if (depth >= m_rrDepth-1) {
				if (sampler.next() < m_rrProb) {
					rusPdf = m_rrProb;
				}
				else {
					return v3f(0.f);
				}
			}
			v3f emission;
			v3f bsdf;
			float pdf;
			do {
				bsdf = getBSDF(hit)->sample(hit, sampler.next2D(), &pdf);
				v3f wi = glm::normalize(hit.frameNs.toWorld(hit.wi));
				Ray next = Ray(hit.p, wi);
				if (scene.bvh->intersect(next, hit)) {
					emission = getEmission(hit);
				
				}
				else {
					return v3f(0.f);
				}
			} while (emission != v3f(0.f));

			return bsdf /rusPdf * (indirectTracer(sampler, hit, depth+1) + directTracer(sampler, hit));
			
		}
		else {
			if (depth < m_maxDepth-1) {
				v3f emission;
				v3f bsdf;
				float pdf;
				do {
					bsdf = getBSDF(hit)->sample(hit, sampler.next2D(), &pdf);
					v3f wi = glm::normalize(hit.frameNs.toWorld(hit.wi));
					Ray next = Ray(hit.p, wi);
					if (scene.bvh->intersect(next, hit)) {
						emission = getEmission(hit);
						
					}
					else {
						return v3f(0.f);
					}
				} while (emission != v3f(0.f));

				return bsdf * (indirectTracer(sampler, hit, depth+1) + directTracer(sampler, hit));
			}
		}
		
		return v3f(0.f);
	}
	v3f directTracer(Sampler& sampler, SurfaceInteraction& hit) const {
		v3f LiDirect(0.f);
		if (m_maxDepth == 0) {
			return LiDirect;
		}
		else {
			float emPdf;
			size_t id = selectEmitter(sampler.next(), emPdf);
			const Emitter& em = getEmitterByID(id);
			v3f n, pos;
			float pdf;
			sampleEmitterPosition(sampler, em, n, pos, pdf);
			v3f wi = pos - hit.p;
			wi = glm::normalize(wi);
			hit.wi = hit.frameNs.toLocal(wi);
			float cosTheta = glm::dot(-wi,n);
			if (cosTheta < 0) {
				return LiDirect;
			}
			Ray shadowRay = Ray(hit.p, wi);
			SurfaceInteraction shadow;
			if (scene.bvh->intersect(shadowRay, shadow)) {//check if the ray from x was blocked
				v3f emission = getEmission(shadow);
				if (emission != v3f(0.f)) {
					v3f brdf = getBSDF(hit)->eval(hit);
					float jacobian = cosTheta / (glm::distance2(pos, hit.p));
					LiDirect = brdf * emission*jacobian / pdf / emPdf;
				}
			}
		}
		return LiDirect;
	}
    v3f renderExplicit(const Ray& ray, Sampler& sampler, SurfaceInteraction& hit) const {
        v3f Li(0.f);

        // TODO: Implement this
		v3f emission = getEmission(hit);
		if (emission != v3f(0.f)) {
			return emission;
		}
		//handle first light
		v3f LiDirect = directTracer(sampler, hit);
		v3f LiIndirect = indirectTracer(sampler, hit, 0);
		Li = LiDirect + LiIndirect;
        return Li;
    }
	

    v3f render(const Ray& ray, Sampler& sampler) const override {
        Ray r = ray;
        SurfaceInteraction hit;

        if (scene.bvh->intersect(r, hit)) {
            if (m_isExplicit)
                return this->renderExplicit(ray, sampler, hit);
            else
                return this->renderImplicit(ray, sampler, hit);
        }
        return v3f(0.0);
    }

    int m_maxDepth;     // Maximum number of bounces
    int m_rrDepth;      // When to start Russian roulette
    float m_rrProb;     // Russian roulette probability
    bool m_isExplicit;  // Implicit or explicit
};

TR_NAMESPACE_END
