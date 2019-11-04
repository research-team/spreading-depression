COMMENT
hzclamp is een aanpassing op:

	Periodic SEClamp
	Based on $NEURONHOME/src/nrnoc/svclmp.mod
	3/27/2000

Alleen is dit een periodieke currentclamp met een trillingstijd 
van 2*dt. Per dt verandert de te injecteren stroom van 0*amp.i
naar 2*amp.i zodat de total geinjecteerde stroom niet verschilt
van de reguliere current clamp, 1*amp.i.

Wij gebruikten de hzclamp om de invloed van de currentclamp en de 
celrespons op het extracellulaire veld te scheiden. waarschijnlijk
werkt deze stimulator in 'CVODE'-mode, m.a.w. de variabele tijdstap
integrator maar is in deze mode nog niet getest.

veel succes, 
Hans Kager, 20-6-2000

netto geen stroom injectie, geen problemen meer met electroneutraliteit


SEClamp:
Although this model appears to work properly, we cannot guarantee 
the absence of bugs, subtle or otherwise.  It is provided as a 
convenience to NEURON users who may wish to try or modify it for 
their own applications.
--Ted Carnevale

ENDCOMMENT

NEURON {
	POINT_PROCESS Hzclamp
	ELECTRODE_CURRENT i
:	NONSPECIFIC_CURRENT i
	RANGE del, dur, amp, freq, width, i, telpulse, stand
}

UNITS {
	(nA) = (nanoamp)
	(uS) = (micromho)
}

PARAMETER {
	del (ms)
	dur (ms)	<0,1e9>
	amp (nA)
	dt (ms)
	freq	(1/s)
	width	(ms)
}

ASSIGNED {
	i (nA)
	i_amp (nA)
	telpulse
	stand
	notify
}

INITIAL {
	i_amp = 0
	stand = 0
	telpulse = 0
	notify=del
}

BREAKPOINT {
	SOLVE state METHOD after_cvode
	at_time(notify)
	i = i_amp
}

PROCEDURE state() {
	if (t <= del + dur && t >= del) {
	  if (telpulse/(freq/1000) < t-del && t-del <= telpulse/(freq/1000)+width ) {
	    notify = del + telpulse/(freq/1000)+width
	    i_amp=amp
	    stand=1 
	  } else if (stand == 1 ) {
	    stand = 0
	    telpulse = telpulse + 1
	    i_amp = 0
	    notify = del + telpulse/(freq/1000)
	  } else {
	    i_amp = 0
	  }
	}else{
	  i_amp = 0
	}
}
