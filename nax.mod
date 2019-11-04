TITLE sodium calcium exchange
: taken from Courtemanche et al Am J Physiol 1998 275:H301

NEURON {
	SUFFIX nax
	USEION ca READ cao, cai WRITE ica
	USEION na READ nao, nai WRITE ina
	RANGE imax, ica, ina , itot
	GLOBAL kna, kca
}

UNITS {
	(mA) = (milliamp)
	(mV) = (millivolt)
	F = (faraday) (coulombs)
	R 	= (k-mole)	(joule/degC)
}

PARAMETER {
	imax	= 3.2       (mA/cm2)
	kna	=  87.5     (mM)
	kca	=  1.38     (mM)
	gamma	= .35		: voltage dependence factor
}

ASSIGNED {
	celsius	(degC)
	v	(mV)
	ica	(mA/cm2)
	ina	(mA/cm2)
	itot	(mA/cm2)
	cao	(mM)
        cai	(mM)
	nao	(mM)
	nai	(mM)
}

BREAKPOINT {
	LOCAL rate
	rate = pumprate(v,nai,nao,cai,cao)
	ina =  3*rate
	ica = -2*rate
	itot=ina+ica
}

FUNCTION pumprate(v,nai,nao,cai,cao) {
	LOCAL q10, Kqa, KB, k
	k = R*(celsius + 273.14)/(F*1e-3)
	q10 = 3^((celsius - 37)/10 (degC))
	Kqa = exp(gamma*v/k)
	KB = exp( (gamma - 1)*v/k)
	pumprate = q10*imax*(Kqa*nai*nai*nai*cao-KB*nao*nao*nao*cai)/((kna*kna*kna + nao*nao*nao)*(kca + cao)*(1 + 0.1*KB))
}