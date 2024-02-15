TITLE leak

NEURON {
	SUFFIX leak
	USEION k READ ek WRITE ik
	USEION na READ ena WRITE ina
	RANGE gk, ik, gcl, icl, ia, gna, ina
	RANGE qk, qna, qcl, qa
}

UNITS { 
	(mV) = (millivolt)  (mA) = (milliamp)
	PI		= (pi) (1)
	FARADAY		= 96485.309 (coul)
}

PARAMETER {
	gk	= 1e-5 (mho/cm2)
	gna	= 1e-5 (mho/cm2)
	
}

ASSIGNED {
	v (mV)
	ik (mA/cm2)
	ek (mV)
	ina (mA/cm2)
	ena (mV)
	icl (mA/cm2)
	ecl (mV)
	ia (mA/cm2)
	ea (mV)
	diam (um)
}

BREAKPOINT {
	:SOLVE stromen METHOD after_cvode
	ik = gk*(v-ek)
	ina = gna*(v-ena)
	:SOLVE integreer METHOD sparse
}
STATE { qk qna qcl qa }

INITIAL {
	ik = 0
	ina = 0
	qk = 0
	qna = 0
}

KINETIC integreer {
	
	COMPARTMENT diam*diam*PI/4 { qna qk qcl qa}
	
	~ qna << ((-ina*diam )*PI*(1e4)/FARADAY )
	~ qk  << (( -ik*diam )*PI*(1e4)/FARADAY )
}


