TITLE nachan
: 29-07-01 update weer terug naar geleidbaarheden ipv
: permeabiliteiten.
: Natrium kanaal m^3*h 
:  
: uit: Traub et al.
: A branching dendritic model of a rodent CA3
: pyramidal neurone.

UNITS {
	(mV) =	(millivolt)
	(mA) =	(milliamp)
}

INDEPENDENT {t FROM 0 TO 1 WITH 100 (ms)}

NEURON {
	SUFFIX nachan
	USEION na READ ena WRITE ina
	RANGE gnabar, ina, interval, freq, n, firing, qna
	GLOBAL shiftm, shifth, scaletaum, scaletauh
}

UNITS {
	PI		= (pi) (1)
	:FARADAY = 96520 (coul)
	:R = 8.3134 (joule/degC)
	:FARADAY	= (faraday) (coulomb)
	FARADAY		= 96485.309 (coul)
	R = (k-mole) (joule/degC)
}

PARAMETER {
	celsius=36	(degC)
	gnabar=1e-3	(mho/cm2)	: default max. perm.
	shiftm=0	(mV)		: shift activatie
	shifth=0	(mV)		: shift inactivatie
	scaletaum=1	(mV)
	scaletauh=1	(mV)
}

ASSIGNED { 
	ina	(mA/cm2)
	v	(mV)
	ena	(mV)
	dt	(ms)
	diam	(um)
	freq
	interval
	n
	firing
}

STATE { ma mb ha hb qna }		: fraction of states, ma=fraction in open state.

BREAKPOINT {
	SOLVE nastate METHOD sparse
	ina = gnabar*ma*ma*ma*ha*(v-ena)
}

INITIAL {
	ma=m_inf(v)
	ha=h_inf(v)
	mb=1-ma
	hb=1-ha
	freq = 0
	n = 0
	interval = 0
	firing = 0
	qna = 0
	ina = gnabar*ma*ma*ma*ha*(v-ena)
}

LOCAL a1,a2,b1,b2

KINETIC nastate {
	COMPARTMENT diam*diam*PI/4 { qna }

	telspike()
	a1 = m_a(v)
	a2 = m_b(v)
	b1 = h_a(v)
	b2 = h_b(v)
	~ mb <-> ma (a1, a2)
	~ hb <-> ha (b1, b2)
	CONSERVE ma + mb = 1
	CONSERVE ha + hb = 1
	~ qna << (-ina*PI*diam*(1e4)/FARADAY)
}

PROCEDURE telspike() {
	if ( (ma*ma*ma*ha >.01) && !firing ) {
	  n=n+1
	  if (n>1) {
	    freq=1000/interval
	  }
	  firing=1
	  interval=0
	}
	if ( (ma*ma*ma*ha <.01 ) && firing ) {
	  firing = 0
	}
	interval = interval + dt/2
}
	
FUNCTION m_a(v(mV)) {
	TABLE DEPEND shiftm, scaletaum FROM -150 TO 150 WITH 301
	m_a=scaletauh*0.32*(13.1-v-70-shiftm) / (exp((13.1-v-70-shiftm)/4)-1) :was scaletauh, fout dus
}

FUNCTION m_b(v(mV)) {
	TABLE DEPEND shiftm, scaletaum FROM -150 TO 150 WITH 301
	m_b=scaletaum*0.28*(v-40.1+70+shiftm)/(exp((v-40.1+70+shiftm)/5)-1)	
}

FUNCTION h_a(v(mV)) {
	TABLE DEPEND shifth, scaletauh FROM -150 TO 150 WITH 301
	h_a = scaletauh*0.128*exp((17-v-70-shifth)/18)
}

FUNCTION h_b(v(mV)) {
	TABLE DEPEND shifth, scaletauh FROM -150 TO 150 WITH 301
	h_b = scaletauh*4/(1+exp((40-v-70-shifth)/5))
}

FUNCTION m_inf(v(mV)) {
	m_inf = m_a(v)/(m_a(v)+m_b(v))
}

FUNCTION h_inf(v(mV)) {
	h_inf = h_a(v)/(h_a(v)+h_b(v))
}

FUNCTION window(v(mV)) {
	window=gnabar*m_inf(v)^3*h_inf(v)*(v-ena)
}
