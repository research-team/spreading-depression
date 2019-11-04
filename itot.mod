TITLE tot



NEURON {
	SUFFIX tot
	USEION na READ ina
	USEION k  READ ik
	USEION cl READ icl VALENCE -1
	USEION ca READ ica VALENCE 2
        RANGE i, imem
}

UNITS {
	(mA)	= (milliamp)
	(mV)	= (millivolt)
	(mM)	= (milli/liter)
        FARADAY = 96480 (coul)
        R       = 8.314 (volt-coul/degC)
	PI	= (pi) (1)     
}



ASSIGNED { 
	i	(mA/cm2)
	imem	(nA)
	ina	(mA/cm2)
	ik	(mA/cm2)
	icl	(mA/cm2)
	ica	(mA/cm2)
	diam	(um)
	L	(um)
}

BREAKPOINT {
	imem=ik+ina+icl+ica
	i=imem*diam*PI
}
	