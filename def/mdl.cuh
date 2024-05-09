#pragma once

#include "insts.cuh"
#include "btcusdt.cuh"

typedef struct {
	uint   Xs;
	int * pos;	//si pos == -1 => x=donnee
} Connection_t;

typedef struct {
	//	Insts
	uint insts;
	Inst_t       **       inst;
	Connection_t ** connection;

	//	Optimisation
} Mdl_t;