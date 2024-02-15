NEURON {
    SUFFIX kleak
    USEION k READ ek WRITE ik
    USEION na READ ena WRITE ina
    RANGE gk, ik, gcl, icl, ga, ia, gna, ina
    RANGE qk, qna, qcl, qa 
}

UNITS { 
    (mV) = (millivolt)  (mA) = (milliamp)
    PI      = (pi) (1)
    FARADAY     = 96485.309 (coul)
}

PARAMETER {
    gk  = 1e-5 (mho/cm2)
    gna = 1e-5 (mho/cm2)
}

ASSIGNED {
    v (mV)
    ik (mA/cm2)
    ek (mV)
    ina (mA/cm2)
    ena (mV)
    icl (mA/cm2)
    ecl (mV)
    ia (mA/cm2)
    ea (mV)
    diam (um)
}

BREAKPOINT {
    ik = gk*(v-ek)
    ina = gna*(v-ena)
    
}

INITIAL {
    ik = gk*(v-ek)
    ina = gna*(v-ena)
}




