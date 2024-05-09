#include "btcusdt.cuh"

#include "../impl_template/tmpl_etc.cu"

BTCUSDT_t * cree_btcusdt() {
	//
	BTCUSDT_t * ret = (BTCUSDT_t*)malloc(sizeof(BTCUSDT_t));

	//
	FILE * fp = fopen("prixs/dar.bin", "rb");
	ASSERT(fp != 0);
	FREAD(&ret->T, sizeof(uint), 1, fp);
	
	//
	uint LIGNES, N, P;
	FREAD(&LIGNES, sizeof(uint), 1, fp);
	FREAD(&N,      sizeof(uint), 1, fp);
	FREAD(&P,      sizeof(uint), 1, fp);

	//
	ret->X = N * LIGNES;
	ret->Y = P;

	//
	float * x = alloc<float>(ret->T * ret->X);
	FREAD(x, sizeof(float), ret->T * ret->X, fp);
	ret->entree = espace_cree(ret->X, ret->T);
	CONTROLE_CUDA(cudaMemcpy(
		ret->entree->y__d,
		x,
		sizeof(float)*ret->T*ret->X,
		cudaMemcpyHostToDevice
	));
	free(x);

	//
	float * y = alloc<float>(ret->T * ret->Y);
	FREAD(y, sizeof(float), ret->T * ret->Y, fp);
	ret->sortie = espace_cree(ret->Y, ret->T);
	CONTROLE_CUDA(cudaMemcpy(
		ret->sortie->y__d,
		y,
		sizeof(float)*ret->T*ret->Y,
		cudaMemcpyHostToDevice
	));
	free(y);

	//
	fclose(fp);

	//
	return ret;
};

void liberer_btcusdt(BTCUSDT_t * donnee) {
	espace_liberer(donnee->entree);
	espace_liberer(donnee->sortie);
};

//	====================================================

static __global__ void k__pourcent_btcusdt(
	float * somme, float * potentiel,
	float * y, float * p1p0,
	float coef_puissance,
	uint * ts__d,
	uint P)
{
	uint t      = threadIdx.x + blockIdx.x * blockDim.x;
	uint mega_t = threadIdx.y + blockIdx.y * blockDim.y;
	uint p      = threadIdx.z + blockIdx.z * blockDim.z;
	//
	if (t < GRAND_T && mega_t < MEGA_T && p < P) {
		uint _t = ts__d[t] + mega_t;
		//
		uint a_t_il_predit = (sng(p1p0[_t*P + p]) == sng(y[_t*P + p]));
		//
		float _____somme = powf(fabs(p1p0[_t*P + p]), coef_puissance) * a_t_il_predit;
		float _potentiel = powf(fabs(p1p0[_t*P + p]), coef_puissance) * true         ;
		//
		atomicAdd(&somme    [p], _____somme);
		atomicAdd(&potentiel[p], _potentiel);
	}
};

float *  pourcent_btcusdt(BTCUSDT_t * btcusdt, Espace_t * y, uint * ts__d, float coef_puissance) {
	uint P = btcusdt->Y;
	//
	float *     somme__d = cudalloc<float>(P);
	float * potentiel__d = cudalloc<float>(P);
	//
	k__pourcent_btcusdt<<<dim3(KERD(GRAND_T, 32), KERD(MEGA_T, 32), KERD(P, 4)), dim3(32,32,4)>>>(
		somme__d, potentiel__d,
		y->y__d, btcusdt->sortie->y__d,
		coef_puissance,
		ts__d,
		P
	);
	ATTENDRE_CUDA();
	//
	float * somme     = gpu_vers_cpu<float>(    somme__d, P);
	float * potentiel = gpu_vers_cpu<float>(potentiel__d, P);
	//
	float * ret = alloc<float>(P);
	FOR(0, p, P) ret[p] = somme[p] / potentiel[p];
	//
	cudafree<float>(    somme__d);
	cudafree<float>(potentiel__d);
	    free(           somme   );
	    free(       potentiel   );
	//
	return ret;
};

//	====================================================

static __global__ void k__f_btcusdt(
	float * somme_score,
	float * y, float * p1p0,
	uint * ts__d,
	uint P)
{
	uint t      = threadIdx.x + blockIdx.x * blockDim.x;
	uint mega_t = threadIdx.y + blockIdx.y * blockDim.y;
	uint p      = threadIdx.z + blockIdx.z * blockDim.z;
	//
	if (t < GRAND_T && mega_t < MEGA_T && p < P) {
		uint _t = ts__d[t] + mega_t;
		//
		atomicAdd(&somme_score[0], S(y[_t*P + p], p1p0[_t*P + p]));
	}
};

float f_btcusdt(BTCUSDT_t * btcusdt, Espace_t * y, uint * ts__d) {
	uint P = btcusdt->Y;
	//
	float * somme__d = cudalloc<float>(1);
	//
	k__f_btcusdt<<<dim3(KERD(GRAND_T, 32), KERD(MEGA_T, 32), KERD(P, 4)), dim3(32,32,4)>>>(
		somme__d,
		y->y__d, btcusdt->sortie->y__d,
		ts__d,
		P
	);
	ATTENDRE_CUDA();
	//
	float * somme = gpu_vers_cpu<float>(somme__d, 1);
	//
	float score = somme[0] / ((float)(P * GRAND_T * MEGA_T));
	//
	cudafree<float>(somme__d);
	    free       (somme   );
	//
	return score;
};

//	====================================================

static __global__ void k__df_btcusdt(
	float * y, float * p1p0, float * dy,
	uint * ts__d,
	uint P)
{
	uint t      = threadIdx.x + blockIdx.x * blockDim.x;
	uint mega_t = threadIdx.y + blockIdx.y * blockDim.y;
	uint p      = threadIdx.z + blockIdx.z * blockDim.z;
	//
	if (t < GRAND_T && mega_t < MEGA_T && p < P) {
		uint _t = ts__d[t] + mega_t;
		//
		atomicAdd(&dy[_t*P + p], dS(y[_t*P + p], p1p0[_t*P + p]) / (float)(P * MEGA_T * GRAND_T));
	}
};

void df_btcusdt(BTCUSDT_t * btcusdt, Espace_t * y, uint * ts__d) {
	uint P = btcusdt->Y;
	//
	k__df_btcusdt<<<dim3(KERD(GRAND_T, 32), KERD(MEGA_T, 32), KERD(P, 4)), dim3(32,32,4)>>>(
		y->y__d, btcusdt->sortie->y__d, y->dy__d,
		ts__d,
		P
	);
	ATTENDRE_CUDA();
};