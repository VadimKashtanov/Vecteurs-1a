#pragma once

#include "meta.cuh"
#include "espace.cuh"

typedef struct {
	//	Parametres
	uint PARAMS;
	uint * params;

	//	Dar
	uint   Xs;	//assert(x[i]->Y == y->X[i])
	uint * X ;

	//	Sorties
	uint P;	//	Poids
	uint Y;	//	Sorties
	uint L;	//	Dérivés Locales ou autre

	//	Espaces
	Espace_t * y;

	//	Poids et Dérivés Locales
	float *  p__d;	//P
	float *  l__d;	//MEGA_T * GRAND_T * L
	float * dp__d;	//P
} Inst_t;

typedef Inst_t* (*cree_inst_f)(uint PARAMS, char ** params);
typedef void    (*inst_f_f   )(Inst_t * inst, Espace_t ** entree, uint * ts__d, uint mega_t);
typedef void    (*inst_f     )(Inst_t * inst);

#define INSTS 0

extern cree_inst_f     cree_inst[INSTS];
extern inst_f      _liberer_inst[INSTS];
extern inst_f_f          _f_inst[INSTS];
extern inst_f_f         _df_inst[INSTS];