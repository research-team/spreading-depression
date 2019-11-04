TITLE calcium pump 
COMMENT
uit aren borgdorff's proefschrift pagina 30:
V(ca2+i)=Vmax/(1+Km/Ca2+)^h
met Vmax = 352uM/s, Km = 6.9 uM and h=1.1

zie parameters ook in PARAMETER-box
pomp uit granule cellen met gemiddelde diam= 11.1 +/- 0.15 um
Om de granule cel-specifieke waarde Voor Vmax te gebruiken in 
een CA1 cel moet het omgezet worden in algemenere eenheid, nl.
van uM/s naar i/um2:

diam was 11.1 um -> r=5.55 um ->
opp=387 um en inhoud = 716 um3, -> inhoud/opp = r/3 = 1.85 um



ENDCOMMENT

NEURON {
	SUFFIX capump
	USEION ca READ cai WRITE ica	
	RANGE ica, scale
	GLOBAL Vmax, Km, hill, Vconv, carest
}

UNITS {
	(mA) = (milliamp)
	(mV) = (millivolt)
	FARADAY = (faraday) (coulombs)

}

PARAMETER {
	Vmax = 352 (uM/s) 		: units of Borgdorff
	vol_surf_ratio = 1.85 (um) 	: assume r=5.55 um and sphere
	Km = .0069 (mM)			: 6.9 uM
	hill = 1			: hill is 1.1, no significant diff from 1
	scale = 1e-4
}

ASSIGNED {
	ica (mA/cm2)
        cai (mM) 
	Vconv
	carest
}

INITIAL {
	VERBATIM
	cai = _ion_cai;
	carest = _ion_cai;
	ENDVERBATIM
	ica =  pumprate(cai)*scale	
}

BREAKPOINT {
	ica =  pumprate(cai)*scale
}

FUNCTION pumprate (ci) {
	Vconv = Vmax*vol_surf_ratio*FARADAY*2*(1e-4)
	if (fabs(ci-carest) < 1e-7) {
	  pumprate = (ci-carest)*Vconv/Km
	}else{
	  pumprate = Vconv/(1+Km/(ci-carest))
	}
}