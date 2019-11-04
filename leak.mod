TITLE leak

NEURON {
	SUFFIX leak
	USEION k READ ek WRITE ik
	USEION na READ ena WRITE ina
	USEION cl READ ecl WRITE icl VALENCE -1
	USEION a READ ea WRITE ia VALENCE -1
	RANGE gk, ik, gcl, icl, ga, ia, gna, ina
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
	gcl	= 1e-4 (mho/cm2)
	ga	= 0 (mho/cm2)
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
	icl = gcl*(v-ecl)
	ia = ga*(v-ea)
	SOLVE integreer METHOD sparse
}
STATE { qk qna qcl qa }

INITIAL {
	ik = gk*(v-ek)
	ina = gna*(v-ena)
	icl = gcl*(v-ecl)
	ia = ga*(v-ea)
	qk = 0
	qna = 0
	qcl = 0
	qa = 0
}

KINETIC integreer {
	
	COMPARTMENT diam*diam*PI/4 { qna qk qcl qa}
	
	~ qna << ((-ina*diam )*PI*(1e4)/FARADAY )
	~ qk  << (( -ik*diam )*PI*(1e4)/FARADAY )
	~ qcl << ((-icl*diam )*PI*(1e4)/FARADAY )
	~ qa  << (( -ia*diam )*PI*(1e4)/FARADAY )

}

FUNCTION itot(v(mV)) {
	itot=gk*(v-ek)+gna*(v-ena)+gcl*(v-ecl)+ga*(v-ea)
}

PROCEDURE stromen() {
}