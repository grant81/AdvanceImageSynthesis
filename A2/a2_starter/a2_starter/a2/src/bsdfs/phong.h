/*
    This file is part of TinyRender, an educative rendering system.

    Designed for ECSE 446/546 Realistic/Advanced Image Synthesis.
    Derek Nowrouzezahrai, McGill University.
*/

#pragma once

#include "core/core.h"

TR_NAMESPACE_BEGIN

/**
 * Modified Phong reflectance model
 */
struct PhongBSDF : BSDF {

    std::unique_ptr<Texture < v3f>> specularReflectance;
    std::unique_ptr<Texture < v3f>> diffuseReflectance;
    std::unique_ptr<Texture < float>> exponent;
    float specularSamplingWeight;
    float scale;

    PhongBSDF(const WorldData& scene, const Config& config, const size_t& matID) : BSDF(scene, config, matID) {
        const tinyobj::material_t& mat = scene.materials[matID];

        if (mat.specular_texname.empty())
            specularReflectance = std::unique_ptr<Texture<v3f>>(new ConstantTexture3f(glm::make_vec3(mat.specular)));
        else
            specularReflectance = std::unique_ptr<Texture<v3f>>(new BitmapTexture3f(config, mat.specular_texname));

        if (mat.diffuse_texname.empty())
            diffuseReflectance = std::unique_ptr<Texture<v3f>>(new ConstantTexture3f(glm::make_vec3(mat.diffuse)));
        else
            diffuseReflectance = std::unique_ptr<Texture<v3f>>(new BitmapTexture3f(config, mat.diffuse_texname));

        exponent = std::unique_ptr<Texture<float>>(new ConstantTexture1f(mat.shininess));

        //get scale value to ensure energy conservation
        v3f maxValue = specularReflectance->getMax() + diffuseReflectance->getMax();
        float actualMax = max(max(maxValue.x, maxValue.y), maxValue.z);
        scale = actualMax > 1.0f ? 0.99f * (1.0f / actualMax) : 1.0f;

        float dAvg = getLuminance(diffuseReflectance->getAverage() * scale);
        float sAvg = getLuminance(specularReflectance->getAverage() * scale);
        specularSamplingWeight = sAvg / (dAvg + sAvg);

        components.push_back(EGlossyReflection);
        components.push_back(EDiffuseReflection);

        combinedType = 0;
        for (unsigned int component : components)
            combinedType |= component;
    }

    inline v3f reflect(const v3f& d) const {
        return v3f(-d.x, -d.y, d.z);
    }

    v3f eval(const SurfaceInteraction& i) const override {
        v3f val(0.f);
        // TODO: Implement 
		v3f wo = i.wo;
		v3f wi = i.wi;
		if (Frame::cosTheta(wo) <= 0.f || Frame::cosTheta(wi) <= 0) {
			return val;
		}
		float cosWi = Frame::cosTheta(wi);
		float cosWo = Frame::cosTheta(wo);
		v3f diffuseR = diffuseReflectance->eval(worldData,i);
		v3f specularF = specularReflectance->eval(worldData, i);
		float n = exponent->eval(worldData, i);
		//a dot b = |a||b|cos(theta)
		float cosa = fmax(glm::dot(glm::normalize(reflect(wi)), glm::normalize(wo)), 0.f);
		
		val = diffuseR * INV_PI + specularF * (n + 2)*INV_TWOPI*pow(cosa, n);


        return val* cosWi;
    }

    float pdf(const SurfaceInteraction& i) const override {
        float pdf = 0.f;

        return pdf;
    }

    v3f sample(SurfaceInteraction& i, const v2f& _sample, float* pdf) const override {
        v3f val(0.f);

        return val;
    }

    std::string toString() const override { return "Phong"; }
};

TR_NAMESPACE_END