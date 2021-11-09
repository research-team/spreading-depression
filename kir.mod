TITLE kir
COMMENT
potassium inward rectifier after geukes foppen en siegenbeek
simply, with no time dynamics. (instantanous kinetics)
ENDCOMMENT

NEURON {
	SUFFIX kir
	USEION na READ nao
	USEION k READ ko, ek WRITE ik
	USEION cl READ clo VALENCE -1
	RANGE gbar, ik, qk
	GLOBAL vs
}

UNITS {
	(molar) = (1/liter)
	(mV) =	(millivolt)
	(mA) =	(milliamp)
	(mM) =	(millimolar)
	:FARADAY	= (faraday) (coulomb)
	FARADAY		= 96485.309 (coul)
	R = (k-mole) (joule/degC)
	PI		= (pi) (1)
}

STATE { qk }

PARAMETER {
	gbar	= 0	(mho/cm2)
	vs	= 1	:voltage-dependency factor in boltzmann equation was 4
	vh	= 0 (mV)	:halfmaximal activation relative to ek was -10
}

ASSIGNED { 
	ik	(mA/cm2)
	v	(mV)
	ek	(mV)
	ko 	(mM)
	nao	(mM)
	clo	(mM)
	diam	(um)
}

BREAKPOINT {
	ik = gbar*pkir((v), ko, ek)*(v-ek)
	SOLVE kaccum METHOD sparse
}

KINETIC kaccum {
	COMPARTMENT diam*diam*PI/4 { qna qk }
	~ qk <<  ( -ik*PI*diam*(1e4)/FARADAY)
}

FUNCTION pkir(vm,kout,erev) {
	pkir = 1 / ( sqrt(kout) * (1+exp((vm-vh-erev)/vs)) )
}
