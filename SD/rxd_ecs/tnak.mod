NEURON {
    SUFFIX tnak
    USEION na READ ena, nai WRITE ina
    USEION k READ ek, ko WRITE ik
    NONSPECIFIC_CURRENT ileak
    RANGE minf, ninf, taun, ipump, phi
    RANGE imax, gk, taun
}

ASSIGNED {
    ina (mA/cm2)
    ena (mV)
    ek (mV)
    ik (mA/cm2)
    ileak (mA/cm2)
    nai (mM)
    ko (mM)
    minf ninf taun ipump phi
}

PARAMETER {
    : fast sodium
    gna =  180
    thm = -34.
    sigm = 5.

    pna=1e-05
    pnal=2e-09

    : potassium IK
    gk = 5
    thn = -55.
    sgn = 14.
    taun0 = .05
    taun1 = .27
    thnt = -40
    sn = -12
    phin = .8

    pk = 7e-05
    pkl = 4e-07


    : leak in neo
    gl = 0.3
    el = -70

    : pump
    imax = 10

    :Gas constant, temperature, Faraday's constant
    R=8310
    Temp=310.0
    F = 96485.309
}

STATE {
    n
}

BREAKPOINT {
    SOLVE state METHOD derivimplicit
    ina = 0.001 * (gna *  ((pow(minf, 3) )* (1-n) + pnal)  * (v - ena)  + (3 * ipump))
    :0.001 * (gna * pow(minf, 3) * (1 - n) * (v - ena) + 3 * ipump)
    ik = 0.001  * (gk * ( pow(n, 4) + pkl) *(v - ek)  - (2 * ipump))
    :0.001 * (gk * pow(n, 4) * (v - ek) - 2 * ipump)
    ileak = 0.001 * (gl * (v - el))
}

INITIAL {
    n = 0.144
}

PROCEDURE rates(v(mV)) {
    minf = 1. / (1. + exp(-(v - thm) / sigm))
    ninf = 1. / (1. + exp(-(v - thn) / sgn))
    taun = taun0 + taun1 / (1 + exp(-(v - thnt) / sn))
    ipump = imax / (pow(1 + 2. / ko, 2) * pow(1 + 7.7 / nai, 3))

    
}

DERIVATIVE state {
    rates(v)
    n' = phin * (ninf - n) / taun
}

