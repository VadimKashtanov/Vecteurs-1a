#pragma once

#include "meta.cuh"
#include "espace.cuh"

#define  D(y,c) (powf(y - sng(c), 2)/2)
#define dD(y,c) (powf(y - sng(c), 1)  )

#define K(y,c)  (powf(c*100, 1.0))//(powf(c*4, 1.0))

#define  S(y,c) ( D(y,c) * K(y,c))
#define dS(y,c) (dD(y,c) * K(y,c))

typedef struct {
	//
	uint X;
	uint Y;
	uint T;

	//	Espaces
	Espace_t * entree;
	Espace_t * sortie;
} BTCUSDT_t;

BTCUSDT_t * cree_btcusdt();
void  liberer_btcusdt(BTCUSDT_t * btcusdt);
//
float *  pourcent_btcusdt(BTCUSDT_t * btcusdt, Espace_t * y, uint * ts__d, float coef_puissance);
//
float  f_btcusdt(BTCUSDT_t * btcusdt, Espace_t * y, uint * ts__d);
void  df_btcusdt(BTCUSDT_t * btcusdt, Espace_t * y, uint * ts__d);