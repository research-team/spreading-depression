TITLE ka
: Kalium stroom type A 
: twee gates met elk twee toestanden: open of dicht
: 
: uit: Traub et al.
: A branching dendritic model of a rodent CA3
: pyramidal neurone.



UNITS {
	(molar) = (1/liter)
	(mV) =	(millivolt)
	(mA) =	(milliamp)
	(mM) =	(millimolar)
}

INDEPENDENT {t FROM 0 TO 1 WITH 100 (ms)}

NEURON {
	SUFFIX ka
	USEION k READ ek WRITE ik
	RANGE gkbar, ik, qk
	GLOBAL shiftm, shifth
}

UNITS {
	PI		= (pi) (1)
	FARADAY		= 96485.309 (coul)
	R = (k-mole) (joule/degC)
}

PARAMETER {
	celsius		(degC)
	gkbar=1e-3	(cm/s)		: Maximum Permeability .2e-3*5 hans
	shiftm = 0	(mV)
	shifth = 0	(mV)
}

ASSIGNED { 
	ik	(mA/cm2)
	v	(mV)	
	ek	(mV)
	diam	(um)
}

STATE { am ac bm bc qk }			: fraction of states, m=fraction in open state.

BREAKPOINT {
	SOLVE kstate METHOD sparse
	ik = gkbar*am*am*bm*(v-ek)
}

INITIAL {
	am=a_inf(v)
	ac=1-am
	bm=b_inf(v)
	bc=1-bm
	qk=0
	ik = gkbar*am*am*bm*(v-ek)

}

LOCAL a1,a2,b1,b2

KINETIC kstate {
	a1 = a_m(v)
	a2 = a_c(v)
	b1 = b_m(v)
	b2 = b_c(v)
	~ ac <-> am (a1, a2)
	~ bc <-> bm (b1, b2)
	
	CONSERVE am + ac = 1
	CONSERVE bm + bc = 1
	
	COMPARTMENT diam*diam*PI/4 { qk }
	~ qk << ((-ik*diam )*PI*(1e4)/FARADAY )
}

FUNCTION a_m(v(mV)) {
	LOCAL shift
	TABLE DEPEND shiftm FROM -150 TO 150 WITH 200
	shift=-30+shiftm
	a_m=0.02*(13.1-v-70-shift)/(exp((13.1-v-70-shift)/10)-1)
}

FUNCTION a_c(v(mV)) {
	LOCAL shift
	TABLE DEPEND shiftm FROM -150 TO 150 WITH 200
	shift=-30+shiftm
	a_c=0.0175*(v-40.1+70+shift)/(exp((v-40.1+70+shift)/10)-1)	
}

FUNCTION b_m(v(mV)) {
	TABLE DEPEND shifth FROM -150 TO 150 WITH 200
	b_m = 0.016*exp((-13-v-70-shifth)/18)
}

FUNCTION b_c(v(mV)) {
	TABLE DEPEND shifth FROM -150 TO 150 WITH 200
	b_c = 0.5/(1+exp((10.1-v-70-shifth)/5))
}

FUNCTION a_inf(v(mV)) {
        a_inf = a_m(v) / ( a_m(v) + a_c(v) )
}

FUNCTION b_inf(v(mV)) {
        b_inf = b_m(v) / ( b_m(v) + b_c(v) )
}

FUNCTION window(v(mV)) {
	window=gkbar*a_inf(v)*a_inf(v)*b_inf(v)*(v-ek)
}

FUNCTION ghk(v(mV), ci(mM), co(mM)) (.001 coul/cm3) {
	LOCAL z, eci, eco
	z = (1e-3)*1*FARADAY*v/(R*(celsius+273.11247574))
	eco = co*efun(z)
	eci = ci*efun(-z)
	:high kao charge moves inward, mogelijke fouten vanwege oorsprong Ca(2+)!
	:negative potential charge moves inward
	ghk = (.001)*1*FARADAY*(eci - eco)
}

FUNCTION efun(z) {
	if (fabs(z) < 1e-4) {
		efun = 1 - z/2
	}else{
		efun = z/(exp(z) - 1)
	}
}
