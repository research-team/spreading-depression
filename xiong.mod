TITLE xiong

COMMENT
Extracellular concentrations of Ca21 change
rapidly and transiently in the brain during excitatory synaptic
activity. To test whether such changes in Ca21 can play a
signaling role we examined the effects of rapidly lowering
Ca21 on the excitability of acutely isolated CA1 and cultured
hippocampal neurons. Reducing Ca21 excited and depolarized
neurons by activating a previously undescribed nonselective
cation channel. This channel had a single-channel conductance
of 36 pS, and its frequency of opening was inversely
proportional to the concentration of Ca21. The inhibition of
gating of this channel was sensitive to ionic strength but
independent of membrane potential. The ability of this channel
to sense Ca21 provides a novel mechanism whereby
neurons can respond to alterations in the extracellular concentration
of this key signaling ion.
uit: 
Proc. Natl. Acad. Sci. USA
Vol. 94, pp. 7012 7017, June 1997
Neurobiology
Extracellular calcium sensed by a novel cation channel in
hippocampal neurons
Z.-G. XIONG, W.-Y. LU, AND J. F. MACDONALD

ENDCOMMENT

NEURON {
	SUFFIX xiong
	USEION k READ ko, ki, ek WRITE ik
	USEION na READ nai, nao, ena WRITE ina
	USEION ca READ cao
	GLOBAL tauavg, rmax, ec50, Nh, n
	RANGE ik, ina, g, gpresent, itot
}

UNITS {
	(molar) = 	(1/liter)
	(mV) =	(millivolt)
	(mA) =	(milliamp)
	(mM) =	(millimolar)
	FARADAY	= (faraday) (coulomb)
	:FARADAY		= 96485.309 (coul)
	R = (k-mole) (joule/degC)
}

:INDEPENDENT {t FROM 0 TO 1 WITH 100 (ms)}

PARAMETER {
	celsius		(degC)
	g=1e-3	(mho/cm2)
	tau_ina=100	(ms)
	tau_act=992	(ms)
	rmax=1
	ec50=.145	(mM) : 1/2 - max. dosage: was .39 in eerste artikel xiong. deze waarde komt uit vervolg studie met lamotrigine uit 2001
	Nh=1.4		: hill coefficient
	n=4		: gates voor asymmetrie in tau's
	tauavg=300	(ms) : jbf-tau, ziet er aardig uit.
}

ASSIGNED { 
	v	(mV)	
	ina	(mA/cm2)
	ik	(mA/cm2)
	ena	(mV)
	ek	(mV)
	cao	(mM)
	ki
	ko
	nai
	nao
	gpresent
	itot
}

STATE { m }

BREAKPOINT {
	SOLVE gatestate METHOD cnexp
	gpresent=g*m^n
	ina = gpresent*(v-ena)
	ik = gpresent*(v-ek)
	itot=ik+ina
}

INITIAL {
	m=hill(cao)
	gpresent=g*m^n
	ina = gpresent*(v-ena)
	ik = gpresent*(v-ek)
	itot=ik+ina
}

DERIVATIVE gatestate {
	m' = ( (hill(cao)-m)/tauavg )
}

FUNCTION hill(co) {
	TABLE DEPEND rmax, ec50, Nh, n FROM 0 TO 15 WITH 150
	hill = (rmax/(1+(co/ec50)^Nh))^(1/n)
}

FUNCTION ghk(v(mV), ci(mM), co(mM)) (.001 coul/cm3) {
	LOCAL z, eci, eco
	z = (1e-3)*1*FARADAY*v/(R*(celsius+273.11247574))
	eco = co*efun(z)
	eci = ci*efun(-z)
	ghk = (.001)*1*FARADAY*(eci - eco)
}

FUNCTION efun(z) {
	if (fabs(z) < 1e-4) {
		efun = 1 - z/2
	}else{
		efun = z/(exp(z) - 1)
	}
}
