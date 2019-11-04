TITLE transient and low threshold calcium current (T-current)

COMMENT
        *********************************************
        reference:  	Huguenard & McCormick (1992) 
			J.Neurophysiology 68(4), 1373-1383
        found in:       thalamic relay neurons
        *********************************************
	Assembled for MyFirstNEURON by Arthur Houweling
ENDCOMMENT

INDEPENDENT {t FROM 0 TO 1 WITH 1 (ms)}

NEURON {
	SUFFIX cat
	USEION ca READ cai, cao WRITE ica VALENCE 2
        RANGE gcatbar, ica
        GLOBAL shiftm, shifth, tauh
}

UNITS {
	(mA)	= (milliamp)
	(mV)	= (millivolt)
	(mM)	= (milli/liter)
        FARADAY = 96480 (coul)
        R       = 8.314 (volt-coul/degC)
}

PARAMETER {
	celsius		(degC)
	gcatbar= 0.0001	(cm/s)	
	shiftm = 20 (mV)
	shifth = 20 (mV)
	tauh = 40 (ms)
}

STATE {
	m h
}

ASSIGNED {
	ica
	v
	cai	(mM)
	cao	(mM)
	tadjm
	tadjh
}

BREAKPOINT { 
	SOLVE state METHOD cnexp
	ica = gcatbar * m*m*h * ghk(v,cai,cao,2)
}

DERIVATIVE state {
	m'= (m_inf(v)-m) / tau_m(v)
	h'= (h_inf(v)-h) / tauh
}


INITIAL {
	tadjm= 3.55^((celsius-23.5)/10)
	tadjh= 2.8^((celsius-23.5)/10)
	m = m_inf(v)
	h = h_inf(v)
}

FUNCTION ghk( v(mV), ci(mM), co(mM), z)  (millicoul/cm3) { LOCAL e, w
        w = v * (.001) * z*FARADAY / (R*(celsius+273.16))
        if (fabs(w)>1e-4) 
          { e = w / (exp(w)-1) }
        else : denominator is small -> Taylor series
          { e = 1-w/2 }
        ghk = - (.001) * z*FARADAY * (co-ci*exp(w)) * e
}

FUNCTION tau_m(v) {
	tau_m = (1/(exp((v-shiftm+131.6)/-16.7)+exp((v-shiftm+16.8)/18.2)) + 0.612) / tadjm 
}


FUNCTION m_inf(v) {
	m_inf = 1 / (1+exp((v-shiftm+60.5)/-6.2))
}

FUNCTION h_inf(v) {
	h_inf = 1 / (1+exp((v-shifth+84)/4.03)) 
}
