#pragma once

#include "insts.cuh"

//	SoftMax en Multiple Canneaux

//	x = C * X
//		C - canneaux
//		X - vecteur
//	y = C * X
//		Chaque X sera softmax de son X dans son canal c