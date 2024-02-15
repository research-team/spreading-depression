NEURON {
	SUFFIX getconc
	USEION na WRITE nai, nao
	USEION  k WRITE  ki,  ko
	USEION cl WRITE cli, clo
	USEION  a WRITE  ai,  ao
	POINTER naig, naog, kig, kog, clig, clog, aig, aog
}

ASSIGNED {
	naig naog kig kog clig clog aig aog
}

STATE { nai nao ki ko cli clo ai ao }

BREAKPOINT {
	:at_time(t) {
	  nai=naig nao=naog ki=kig ko=kog
	  cli=clig clo=clog ai=aig ao=aog
	:}

}
INITIAL {
	at_time(t) {
	  nai=naig nao=naog ki=kig ko=kog
	  cli=clig clo=clog ai=aig ao=aog
	}
}
