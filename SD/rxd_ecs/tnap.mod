NEURON {
    SUFFIX tnap
    USEION na READ ena WRITE ina
    RANGE minf, hinf, tauh, ina, gnap
}

ASSIGNED {
    ina (mA/cm2)
    ena (mV)
    v (mV)
    minf hinf tauh
}

PARAMETER {
    :NaP
    gnap = 0.4
    taubar = 10000
    thmp = -40
    sigmp = 6
    thhp = -48
    sighp = -6
    vt = -49
    sig = 6
    phih = 0.05
    F = 96485.309
    pnap = 3e-08
}

STATE {
    h
}

BREAKPOINT {
    SOLVE state METHOD derivimplicit
    ina = 0.001 * (pnap * minf *hinf * h*  (v - ena))
}

INITIAL {
    h = 0.995
}

PROCEDURE rates(v(mV)) {
    minf = 1. / (1. + exp(-(v - thmp) / sigmp))
    hinf = 1. / (1. + exp(-(v - thhp) / sighp))
    tauh = taubar / cosh((v - vt) / (2 * sig))
}

DERIVATIVE state {
    rates(v)
    h' = phih * (hinf - h) / tauh
}

