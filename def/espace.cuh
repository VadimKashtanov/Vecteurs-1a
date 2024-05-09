#pragma once

typedef struct {
	uint       Y;
	//
	float *  y__d;	//MEGA_T * GRAND_T * Y
	float * dy__d;	//MEGA_T * GRAND_T * Y
} Espace_t;

Espace_t * espace_cree   (uint Y, uint T   );
void       espace_liberer(Espace_t * espace);