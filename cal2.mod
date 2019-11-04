TITLE l-calcium channel
: l-type calcium channel


UNITS {
	(mA) = (milliamp)
	(mV) = (millivolt)

	FARADAY = 96520 (coul)
	R = 8.3134 (joule/degC)
	KTOMV = .0853 (mV/degC)
}

PARAMETER {
	v (mV)
	celsius 	(degC)
	gcalbar=.003 (mho/cm2)
	ki=.001 (mM)
	cai (mM)
	cao (mM)
        tfa=1
        shiftm=10
        scaletau=.333333
}


NEURON {
	SUFFIX cal
	USEION ca READ cai,cao, eca WRITE ica VALENCE 2
        RANGE gcalbar,cai, ica
        GLOBAL minf ,tau, shiftm, scaletau
}

STATE {
	m
}

ASSIGNED {
	ica	(mA/cm2)
        gcal	(mho/cm2)
        minf
        tau	(ms)
        eca	(mV)
}

INITIAL {
	rate(v)
	m = minf
}

BREAKPOINT {
	SOLVE state METHOD cnexp
	gcal = gcalbar*m*m*h2(cai)
	ica = gcal*(v-eca) :ghk(v,cai,cao)

}

FUNCTION h2(cai(mM)) {
	h2 = ki/(ki+cai)
}


FUNCTION ghk(v(mV), ci(mM), co(mM)) (mV) {
        LOCAL nu,f

        f = KTF(celsius)/2
        nu = v/f
        ghk=-f*(1. - (ci/co)*exp(nu))*efun(nu)
}

FUNCTION KTF(celsius (DegC)) (mV) {
        KTF = ((25./293.15)*(celsius + 273.15))
}


FUNCTION efun(z) {
	if (fabs(z) < 1e-4) {
		efun = 1 - z/2
	}else{
		efun = z/(exp(z) - 1)
	}
}

FUNCTION alp(v(mV)) (1/ms) {
	TABLE DEPEND shiftm, scaletau FROM -150 TO 150 WITH 200
	alp = scaletau*15.69*(-1.0*v-shiftm+81.5)/(exp((-1.0*v-shiftm+81.5)/10.0)-1.0)
}

FUNCTION bet(v(mV)) (1/ms) {
	TABLE DEPEND shiftm, scaletau FROM -150 TO 150 WITH 200
	bet = scaletau*0.29*exp((-v-shiftm)/10.86)
}

DERIVATIVE state {  
        rate(v)
        m' = (minf - m)/tau
}

PROCEDURE rate(v (mV)) { :callable from hoc
        LOCAL a
        a = alp(v)
        tau = 1/(tfa*(a + bet(v)))
        minf = tfa*a*tau
}
 













