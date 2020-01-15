NEURON {
    SUFFIX kleak
    USEION k READ ek WRITE ik
    RANGE ik 
}

UNITS { 
	(mV) = (millivolt)  (mA) = (milliamp)
	PI		= (pi) (1)
	FARADAY		= 96485.309 (coul)
}

ASSIGNED {
    ik (mA/cm2)
    ek (mV)
    v (mV)
    diam (um)
}

PARAMETER {
    gk	= 1e-5 (mho/cm2)
}

BREAKPOINT {
    ik = gk * (v - ek)
}




