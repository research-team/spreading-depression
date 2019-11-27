TITLE ip3 + Ca
COMMENT
		*********************************
    in Astrocyte

		*********************************
ENDCOMMENT

NEURON {
    RANGE Ca, h, IP3, t
:?   USEION ip3 READ iip3 WRITE ip3i
    GLOBAl a_2, c_1, Ca_free, d_1, d_2, d_3, d_4, d_5, kappa_delta, K_3, K_pi, K_D, K_ER, K_p, K_PLCdelta, K_R, r_bar_5P, r_C, r_L, v_bar_beta, v_bar_delta, v_ER    
}


UNITS {
  	(molar) = (1/liter)
  	(mM)    = (millimolar)
  	(uM)    = (micromolar)
  	(um)    = (micron)
  	(mA)    = (milliamp)
  	FARADAY = (faraday)  (coulomb)
  	PI      = (pi)       (1)
}

PARAMETER {
  	a_2 = 0.2          : 1/(uM s)\n",
    c_1 = 0.185        : 1\n",
    Ca_free = 2        : uM\n",
    d_1 = 0.13         : uM\n",
    d_2 = 1.049        : uM\n",
    d_3 = 0.9434       : uM\n",
    d_5 = 0.08234      : uM\n",
    kappa_delta = 1.5  : uM\n",
    K_3 = 1            : uM\n",
    K_pi = 0.6         : uM \n",
    K_D = 0.7          : uM\n",
    K_ER = 0.1         : uM or 0.05 uM\n",
    K_p = 10           : uM\n",
    K_PLCdelta = 0.1   : uM\n",
    K_R = 1.3          : uM\n",
    r_bar_5P = 0.04    : 1/s or 0.05 1/s\n",
    r_C = 6            : 1/s\n",
    r_L = 0.11         : 1/s\n",
    v_bar_3K = 2       : uM/s\n",
    v_bar_beta = 0.2   : uM/s or 0.5 uM/s\n",
    v_bar_delta = 0.02 : uM/s or 0.05 uM/s\n",
    v_ER = 0.9         : uM/s"
}

FUNCTION do{
    LOCAL J_leak, J_pump, K_gamma, m_infty, n_infty, Q_2, tau_h, v_3K, v_delta,  v_glu, h_infty,  J_chan, dCa_per_dt, dh_per_dt, dIP3_per_dt, deriv
    J_leak = r_L * (Ca_free - (1 + c_1) * Ca)

    J_pump = v_ER * Ca^2 / (Ca^2 + K_ER^2)
            
    K_gamma = K_R * (1 + K_p / K_R * Ca / (Ca + K_pi))

    m_infty = IP3 / (IP3 + d_1)

    n_infty = Ca / (Ca + d_5)

    Q_2 = d_2 * (IP3 + d_1) / (IP3 + d_3)

    tau_h = 1 / (a_2 * (Q_2 + Ca))

    v_3K = v_bar_3K * Ca^4 / (Ca^4 + K_D^4) * IP3 / (IP3 + K_3)

    v_delta = v_bar_delta / (1 + IP3/kappa_delta) * Ca^2 / (Ca^2 + K_PLCdelta^2)

    v_glu = v_bar_beta * t^0.7 / t^0.7 + K_gamma^0.7)

    h_infty = Q_2 / (Q_2 + Ca) 

    J_chan = r_C * m_infty^3 * n_infty^3 * h^3  * (Ca_free - (1 + c_1) * Ca)    
    
    : dx/dt
    dCa_per_dt = J_chan + J_leak - J_pump
    dh_per_dt = (h_infty - h) / tau_h
    dIP3_per_dt = v_glu + v_delta - v_3K - r_bar_5P * IP3
    
    deriv = [dCa_per_dt, dh_per_dt, dIP3_per_dt]
    : ? return deriv
}









