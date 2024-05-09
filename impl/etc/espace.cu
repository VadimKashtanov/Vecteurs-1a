#include "espace.cuh"

#include "../../impl_template/tmpl_etc.cu"

Espace_t * espace_cree   (uint Y, uint T) {
	Espace_t * ret = alloc<Espace_t>(1);
	//
	ret->      Y =       Y;
	ret-> y__d = cudalloc<float>(T * Y);
	ret->dy__d = cudalloc<float>(T * Y);
	//
	return ret;
};

void espace_liberer(Espace_t * espace) {
	cudafree<float>(espace-> y__d);
	cudafree<float>(espace->dy__d);
	free(espace);
};