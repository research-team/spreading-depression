TITLE nmda

COMMENT
NMDA-achtige geleidbaarheid; bewerking van Traub's NMDA gate
in CA3 model van 1991
g(t) factor is hier [k+]o afhankelijk gemaakt

Onvolkomenheid is dat dit mechanisme direct naar de stromen ik en ina
schrijft. Realistischer is het om een mechanisme 'synapse' de passieve
geleidbaarheden gk_leak en gna_leak te veranderen. 
1) Betere meting van de input resistance R_in.
2) 'Extracellular' werkt niet goed samen met pointprocesses. Nl. de netto
transmembraanstroom 'i_membrane' is niet meer nul. 
Omdat een synapse per definitie een 'point process' is i.t.t. 'distributed
process', moet mech syn de waarde van gna_leak in mech leak veranderen.
mbv commando extern.?

bijgewerkt voor calciumgeleidbaarheid
ENDCOMMENT


UNITS {
	(molar) = 	(1/liter)
	(mV) =	(millivolt)
	(mA) =	(milliamp)
	(mM) =	(millimolar)
	:FARADAY	= (faraday) (coulomb)
	FARADAY		= 96485.309 (coul)
	R = (k-mole) (joule/degC)
	PI	= (pi)		(1)
}

INDEPENDENT {t FROM 0 TO 1 WITH 100 (ms)}

NEURON {
	SUFFIX nmda
	USEION k READ ko, ki, ek WRITE ik
	USEION na READ nai, nao, ena WRITE ina
	USEION ca READ cai, cao, eca WRITE ica VALENCE 2
	GLOBAL mg, act_99, act_01, ina_99, ina_01, gbar, tau_ina, tau_act, scaleca
	RANGE ik, ina, itot, ica, qna, qk
}

PARAMETER {
	celsius=36	(degC)
	gbar=1e-3	(mho/cm2)
	tau_ina=2000	(ms)
	tau_act=2	(ms)
	act_99=20	(mM)
	act_01=10	(mM)
	ina_99=3.5	(mM)
	ina_01=10	(mM)
	mg=1.2	(mM)
	scaleca=1
}

ASSIGNED { 
	v	(mV)
	itot	(mA/cm2)
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
}

STATE { ma mb ha hb qna qk }

BREAKPOINT {
	SOLVE synstate METHOD sparse
	ina= gbar*ma*ha*(v-ena)/(1+(mg/3)*exp(-.07*(70+v-60)))   : ghk(v,nai,nao,1)
	ik = gbar*ma*ha*(v-ek) /(1+(mg/3)*exp(-.07*(70+v-60)))   : ghk(v,ki ,ko ,1)
	ica= gbar*scaleca*ma*ha*(v-eca)/(1+(mg/3)*exp(-.07*(70+v-60)))   : ghk(v,cai,cao,2)
	itot=ina+ik+ica
	:ma = 1 - mb
	:ha = 1 - hb
}

INITIAL {
	:SOLVE synstate STEADYSTATE sparse
	ma=m_inf(ko)
	mb=1-ma
	ha=h_inf(ko)
	hb=1-ha
	qna=0
	qk=0
	ina= gbar*ma*ha*(v-ena)/(1+(mg/3)*exp(-.07*(70+v-60))) : ghk(v,nai,nao)
	ik = gbar*ma*ha*(v-ek)/(1+(mg/3)*exp(-.07*(70+v-60)))   : ghk(v,ki,ko)
	ica= gbar*scaleca*ma*ha*(v-eca)/(1+(mg/3)*exp(-.07*(70+v-60)))   : ghk(v,cai,cao,2)
	itot=ina+ik+ica
}

LOCAL a1,a2,b1,b2

KINETIC synstate {
	a1 = m_a(ko)
	a2 = m_b(ko)
	b1 = h_a(ko)
	b2 = h_b(ko)

	~ mb <-> ma	(a1, a2)
	~ hb <-> ha 	(b1, b2)
	:CONSERVE ma + mb = 1
	:CONSERVE ha + hb = 1
	
	COMPARTMENT diam*diam*PI/4 { qna qk }
	~ qna << (-ina*PI*diam*(1e4)/FARADAY)
	~ qk <<  ( -ik*PI*diam*(1e4)/FARADAY)
}

FUNCTION m_a(ko) {
	TABLE DEPEND act_99, act_01, tau_act FROM 0 TO 150 WITH 150
	m_a = m_inf(ko)/tau_act
}

FUNCTION m_b(ko) {
	TABLE DEPEND act_99, act_01, tau_act FROM 0 TO 150 WITH 150
	m_b = (1-m_inf(ko))/tau_act
}
 
FUNCTION m_inf(ko) {
	LOCAL kh, h
	TABLE DEPEND act_99, act_01, tau_act FROM 0 TO 150 WITH 150
	kh=(act_99+act_01)/2
	h=-(kh-act_99)/4.59
	m_inf=1/(1+(exp((kh-ko)/h)))
}

FUNCTION h_a(ko) {
	TABLE DEPEND ina_99, ina_01, tau_ina FROM 0 TO 150 WITH 150
	h_a = h_inf(ko)/tau_ina
}

FUNCTION h_b(ko) {
	TABLE DEPEND ina_99, ina_01, tau_ina FROM 0 TO 150 WITH 150
	h_b = (1-h_inf(ko))/tau_ina
}

FUNCTION h_inf(ko) {
	LOCAL kh, h
	TABLE DEPEND ina_99, ina_01, tau_ina FROM 0 TO 150 WITH 150
	kh=(ina_99+ina_01)/2
	h=-(ina_99-kh)/4.59
	h_inf=1/(1+(exp((ko-kh)/h)))
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

