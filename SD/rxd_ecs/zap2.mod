    COMMENT
    izap.mod
    Delivers an oscillating current that starts at t = del >= 0.
    The frequency of the oscillation increases linearly with time
    from f0 at t == del to f1 at t == del + dur,
    where both del and dur are > 0.
    Uses event delivery system to ensure compatibility with adaptive integration.
    12/4/2008 NTC
    ENDCOMMENT

    NEURON {
      POINT_PROCESS Izap2
      RANGE del, dur,amp,  i
      ELECTRODE_CURRENT i
    }

    UNITS {
      (nA) = (nanoamp)
      PI = (pi) (1)
    }

    PARAMETER {
      del (ms)
      dur (ms)
      amp (nA)
    }

    ASSIGNED {
      i (nA)
      on (1)
      osc (1)
    }

    INITIAL {
      i = 0
      on = 0

      if (del<0) { del=0 }
      if (dur<0) { dur=0 }

      : do nothing if dur == 0
      if (dur>0) {
        net_send(del, 1)  : to turn it on and start frequency ramp
        net_send(del+dur, 1)  : to stop frequency ramp, freezing frequency at f1
      }
    }


    BREAKPOINT {
      osc = 0
      if (on==0) {
        i = 0
      } else {
	single_osc(t,1)
	single_osc(t,2)
	single_osc(t,3)
	single_osc(t,4)
	single_osc(t,5)
	:single_osc(t,6)
	:single_osc(t,7)
	:single_osc(t,8)
	:single_osc(t,9)
	:single_osc(t,10)


        i = amp * osc
      }
    }

PROCEDURE  single_osc(t,n){
	osc = osc + pow(2,n*(1.5 -2))*sin(pow(2,n)*(t - del)*0.001+n)		
	}

    NET_RECEIVE (w) {
      : respond only to self-events with flag > 0
      if (flag == 1) {
        if (on==0) {
          on = 1  : turn it on
        } else {
          on = 0  : turn it off
        }
      }
    }


