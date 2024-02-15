NEURON {
    SUFFIX tnak
    USEION na READ ena, nai WRITE ina
    USEION k READ ek, ko WRITE ik
    NONSPECIFIC_CURRENT ileak
    RANGE minf, ninf, taun, ipump , phi
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
    thm = -34
    sigm = 5




    : potassium
    gk = 5
    thn = -55.
    sgn = 14.
    taun0 = 5
    taun1 = 27
    thnt = -40
    sn = -12
    phin = .8

    : leak
    gl = 0.3
    el = -70

    : pump
    imax = 5

    pk = 7e-05
    pkl = 4e-07
    pnal = 2e-09
    pna = 1e-05
    F = 96485
    R=8310
    Temp=0


}

STATE {
    n
}

BREAKPOINT {
    SOLVE state METHOD derivimplicit
    ina = 0.001 * (pna * (pow(minf, 3) * (1 - n) + pnal) * F * phi * (ena-ina) +  (3 * ipump))
    ik = 0.001 * (pk * (pow(n, 4) + pkl)* F * (ek-ik) + (-2 * ipump))
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
    :phi = v / (R* Temp/F)

}

DERIVATIVE state {
    rates(v)
    n' = phin * (ninf - n) / taun
}

