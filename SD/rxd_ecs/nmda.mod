TITLE nmda

NEURON {
	SUFFIX nmda
	USEION k READ ko, ki, ek WRITE ik
	USEION na READ nai, nao, ena WRITE ina
	USEION ca READ cai, cao, eca WRITE ica VALENCE 2
	RANGE ik, ina, inanmda, iknmda, icanmda , inmda, binf
}

UNITS {
	(molar) = 	(1/liter)
	(mV) =	(millivolt)
	(mA) =	(milliamp)
	(mM) =	(millimolar)
	:FARADAY	= (faraday) (coulomb)
	F		= 96485.309 (coul)
	R = (k-mole) (joule/degC)
	PI	= (pi)		(1)
}

PARAMETER {
	pnmda=3e-06
	thetat=-10
	trise=2
	tdecay=1
	alphag=.5
	pca=3
	thg=.01
	sigmag=.001
	glut=.0001
}

ASSIGNED { 
	v	(mV)
	ik	(mA/cm2)
	ina	(mA/cm2)
	ica	(mA/cm2)
	ki	(mM)
	ko	(mM)
	ek	(mV)
	nai	(mM)
	nao	(mM)
	ena	(mV)
	cai	(mM)
	cao	(mM)
	eca	(mV)
	diam	(um2)
	inanmda iknmda icanmda inmda binf
}

STATE {
    sg
}

PROCEDURE rates(v(mV)) {
   binf = 1/(1+exp(-(v-thetat)/16.13)) 
}

BREAKPOINT {
	inmda=inanmda+iknmda+icanmda
	ina = inanmda
	ik = iknmda
}

INITIAL {
	sg = 0.
	inanmda=pnmda*sg*binf*F* (v - ena)
	iknmda=pnmda*sg*binf*F*(v - ek)
	icanmda=pca*2*pnmda*sg*binf*F*(v-eca)
}

DERIVATIVE state {
    sg'= -sg / tdecay + alphag * sinfg(glut) * (1-sg)
}

FUNCTION sinfg(x) {
	sinfg=1./(1.+exp(-(x-thg)/sigmag))
}
