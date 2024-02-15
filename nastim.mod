NEURON {
	POINT_PROCESS nastim
	USEION na WRITE ina
	RANGE del, dur, amp, ina
	:NONSPECIFIC_CURRENT i
}

UNITS {
	(nA) = (nanoamp)
}

PARAMETER {
	del (ms)
	dur (ms)
	amp (nA)
}

ASSIGNED { ina (nA) }

INITIAL {
	ina = 0
}


BREAKPOINT {
	at_time(del)
	at_time(del+dur)
	if (t < del + dur && t > del) {
		ina = -amp
	}else{
		ina = 0
	}
}
