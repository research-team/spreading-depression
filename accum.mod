TITLE accum
COMMENT
ionaccumulatie met Ca2+ buffer, osmotische drukverschillen en meer
tau_accum heeft een grote inivloed op de simulatieduur.
ENDCOMMENT

NEURON {
	POINT_PROCESS accum
	USEION na READ ina, nao, nai WRITE nai, nao, ina
	USEION k READ ik, ko, ki WRITE ki, ko, ik
	USEION cl READ icl, clo, cli WRITE cli, clo, icl  VALENCE -1
	USEION  a READ ia, ao, ai WRITE ai, ao VALENCE -1
	USEION ca READ ica, cao, cai WRITE cai, cao, ica VALENCE 2

	RANGE osmin, electin, osmout, electout, osmglia, electglia
	RANGE volin, volout, volglia, deltan, deltaglia :,tau
	RANGE qnai, qnao, qcai, qcao, qki, qcli, qai,  qko, qclo, qao
	RANGE qnag, nag, qcag, cag, qkg, gckg, qag, kg, clg, ag, k1buf, k2buf, tau
	RANGE setina, setik, seticl, ica_pump, totca, setvolglia, setvolout
	POINTER diamg, inag, ikg, iclg, iag :, icag no ca2+ in glia
	GLOBAL setnag, setkg, setclg, setag, setcag, TotalBuffer, Kd, minvolisvf
}

UNITS	{
	(um3)		= (liter/1e15)
	(mV)		= (millivolt)
	(mA)		= (milliamp)
	FARADAY		= 96485.309 (coul)
	(molar)		= (1/liter)
	(mM)		= (millimolar)
	PI		= (pi) (1)
	R = (k-mole) (joule/degC)
}

PARAMETER {
	Difna = 1.33	(um2/ms)
	Difk = 1.96	(um2/ms)
	Difcl = 2.03	(um2/ms)
	Difca = 0.6	(um2/ms) : moet nog aangepast!
	tau = 100	(ms)

	k1buf = 20	(/mM-ms) : Yamada et al. 1989
	k2buf = .5 	(/ms)
	TotalBuffer = 1.562 (mM)
	Kd = .008	(mM)

	setvolin=1
	setvolout=1
	setvolglia=1
	minvolisvf=.04

	setnag
	setkg
	setclg
	setag
	setcag
	method=0
}

ASSIGNED {
	ina		(mA/cm2)
	ik		(mA/cm2)
	icl		(mA/cm2)
	ia		(mA/cm2)
	ica		(mA/cm2)
	inag		(mA/cm2)
	ikg		(mA/cm2)
	iclg		(mA/cm2)
	iag		(mA/cm2)
	:icag		(mA/cm2)
	osmin		(mM)
	electin		(mM)
	osmout		(mM)
	electout	(mM)
	osmglia		(mM)
	electglia	(mM)
	diam		(um)
	diamg		(um)

	B0		(mM)
	naflux[3]
	clflux[3]
	 aflux[3]
	 kflux[3]
	caflux[3]
	deltan
	deltag
	nai ki ai cli cai
	nao ko ao clo cao
	nag kg ag clg cag
	volin volout volglia
	qki qko qkg qnai
	qnao qnag qai qao
	qag qcli qclo qclg qcai qcao qcag
}

STATE { na[3] k[3] a[3] cl[3] ca[2] (mM) <1e-4> vol[3] CaBuffer  Buffer pump (mol/cm2) pumpca  (mol/cm2) catot }
LOCAL b, c, d

BREAKPOINT {
	SOLVE state METHOD sparse

}

INITIAL {
	na[0]=nai
	na[1]=nao
	na[2]=setnag
	cl[0]=cli
	cl[1]=clo
	cl[2]=setclg
	k[0]=ki
	k[1]=ko
	k[2]=setkg
	a[0]=ai
	a[1]=ao
	a[2]=setag
	ca[0]=cai
	ca[1]=cao
	ca[2]=setcag

	:BUFFER
	:Kd = k1buf/k2buf
	B0 = TotalBuffer/(1 + Kd*cai)
	Buffer = B0
	CaBuffer = TotalBuffer - B0
	catot = cai*(1+(TotalBuffer/(cai+Kd)))

	vol[0]=setvolin
	vol[1]=setvolout
	vol[2]=setvolglia

	volin=vol[0] volout=vol[1] volglia=vol[2]
	nag=na[2] kg=k[2] clg=cl[2] ag=a[2] cag=ca[2]

	osmin   = nai + ki + cli + ai + cai
	osmout  = nao + ko + clo + ao + cao
	osmglia = nag + kg + clg + ag + cag

	electin   = nai + ki - cli - ai + cai*2
	electout  = nao + ko - clo - ao + cao*2
	electglia = nag + kg - clg - ag + cag*2

	qnai=na[0]*vol[0] qnao=na[1]*vol[1] qnag=na[2]*vol[2]
	qcai=ca[0]*vol[0] qcao=ca[1]*vol[1] qcag=ca[2]*vol[2]
	qcli=cl[0]*vol[0] qclo=cl[1]*vol[1] qclg=cl[2]*vol[2]
	qki=k[0]*vol[0] qko=k[1]*vol[1] qkg=k[2]*vol[2]
	qai=a[0]*vol[0] qao=a[1]*vol[1] qag=a[2]*vol[2]
}

KINETIC state {
	deltan = (nai + ki + cli + ai + cai - nao - ko - clo - ao - cao )/tau
	deltag = (nag + kg + clg + ag + cag - nao - ko - clo - ao - cao )/tau

	IF (vol[1]<=minvolisvf&&deltan>0) {
	  deltan=0
	}
	IF (vol[1]<=minvolisvf&&deltag>0) {
	  deltag=0
	}
	IF (method==0) {
	~ vol[0] <-> vol[1]  ( deltan/(diam*diam*PI/4), -deltan/(diam*diam*PI/4) )
	~ vol[1] <-> vol[2]  (-deltag/(diam*diam*PI/4),  deltag/(diam*diam*PI/4) )
	} ELSE {
	~ vol[0] << ( deltan/(diam*diam*PI/4) )
	~ vol[1] << ((-deltan-deltag)/(diam*diam*PI/4) )
	~ vol[2] << ( (deltag)/(diam*diam*PI/4) )
	}

	COMPARTMENT i, vol[i]*diam*diam*PI/4 { na k cl a ca }
	COMPARTMENT vol[0]*diam*diam*PI/4 { catot } :CaBuffer Buffer

	LONGITUDINAL_DIFFUSION i, Difna*diam*diam*PI*vol[i]/4 { na }
	LONGITUDINAL_DIFFUSION i,  Difk*diam*diam*PI*vol[i]/4 { k  }
	LONGITUDINAL_DIFFUSION i, Difcl*diam*diam*PI*vol[i]/4 { cl }
	LONGITUDINAL_DIFFUSION i, Difca*diam*diam*PI*vol[i]/4 { ca }

	naflux[0] = -deltan*na[0] - (ina*diam)*PI*(1e4)/FARADAY
	caflux[0] = -deltan*catot - ((ica)*diam)*PI*(1e4)/(FARADAY*2)
	clflux[0] = -deltan*cl[0] - (icl*diam)*PI*(1e4)/FARADAY*-1 :valence =-1
	 kflux[0] = -deltan* k[0] - ( ik*diam)*PI*(1e4)/FARADAY
	 aflux[0] = -deltan* a[0]
	naflux[1] =  (deltan+deltag)*na[1] + (ina*diam+inag*diamg)*PI*(1e4)/FARADAY
	caflux[1] =  (deltan+deltag)*ca[1] + ((ica)*diam+0*diamg)*PI*(1e4)/(FARADAY*2)  : icag = 0 geen ca2+ in glia
	clflux[1] =  (deltan+deltag)*cl[1] + (icl*diam+iclg*diamg)*PI*(1e4)/FARADAY*-1 :valence =-1
	 kflux[1] =  (deltan+deltag)* k[1] + ( ik*diam+ ikg*diamg)*PI*(1e4)/FARADAY
	 aflux[1] =  (deltan+deltag)* a[1]
	naflux[2] = -deltag*na[2] - (inag*diamg)*PI*(1e4)/FARADAY
:	caflux[2] = -deltag*ca[2] - (icag*diamg)*PI*(1e4)/(FARADAY*2) : geen ca2+ in glia
	caflux[2] = 0
	clflux[2] = -deltag*cl[2] - (iclg*diamg)*PI*(1e4)/FARADAY*-1 :valence =-1
	 kflux[2] = -deltag* k[2] - ( ikg*diamg)*PI*(1e4)/FARADAY
	 aflux[2] = -deltag* a[2]

	:bufflux   = -deltan*Buffer - k1buf*ca[0]*Buffer + k2buf*CaBuffer
	:cabufflux = -deltan*CaBuffer + k1buf*ca[0]*Buffer - k2buf*CaBuffer
	:~ ca[0] + Buffer <-> CaBuffer (k1buf, k2buf)

	:~ Buffer << ( bufflux )
	:~CaBuffer<< ( cabufflux )
	:~  ca[0] << ( caflux[0] )


	~  na[0] << ( naflux[0] )
	~  catot << ( caflux[0] )
  	~   k[0] << (  kflux[0] )
	~  cl[0] << ( clflux[0] )
	~   a[0] << (  aflux[0] )
	~  na[1] << ( naflux[1] )
	~  ca[1] << ( caflux[1] )
	~   k[1] << (  kflux[1] )
	~  cl[1] << ( clflux[1] )
	~   a[1] << (  aflux[1] )
	~  na[2] << ( naflux[2] )
	~  ca[2] << ( caflux[2] )
	~   k[2] << (  kflux[2] )
	~  cl[2] << ( clflux[2] )
	~   a[2] << (  aflux[2] )

	b=TotalBuffer*setvolin/vol[0]-catot+Kd
	c=-Kd*catot
	d=b*b-4*c
	cai=(-b+sqrt(d))/(2)
	CaBuffer = catot-cai
	Buffer = TotalBuffer*setvolin/vol[0] - CaBuffer

	volin=vol[0] volout=vol[1] volglia=vol[2]

	nai=na[0] nao=na[1] nag=na[2]
	cao=ca[1] cag=ca[2] :cai zie boven
	cli=cl[0] clo=cl[1] clg=cl[2]
	ki=k[0] ko=k[1] kg=k[2]
	ai=a[0] ao=a[1] ag=a[2]

	osmin   = nai + ki + cli + ai + cai
	osmout  = nao + ko + clo + ao + cao
	osmglia = nag + kg + clg + ag + cag

	electin   = nai + ki - cli - ai + cai*2
	electout  = nao + ko - clo - ao + cao*2
	electglia = nag + kg - clg - ag + cag*2

	qnai=na[0]*vol[0] qnao=na[1]*vol[1] qnag=na[2]*vol[2]
	qcai=ca[0]*vol[0] qcao=ca[1]*vol[1] qcag=ca[2]*vol[2]
	qcli=cl[0]*vol[0] qclo=cl[1]*vol[1] qclg=cl[2]*vol[2]
	qki=k[0]*vol[0] qko=k[1]*vol[1] qkg=k[2]*vol[2]
	qai=a[0]*vol[0] qao=a[1]*vol[1] qag=a[2]*vol[2]

}

:1)stromen met opp/inhoud
:2)difcoefs
:3)conc ai=1?
:4)volumes