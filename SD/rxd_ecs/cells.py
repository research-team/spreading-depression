from neuron import h, crxd as rxd
from neuron.units import ms, mV
somaR = 11.0  # soma radius
dendR = 1.4  # dendrite radius
dendL = 100.0  # dendrite length
axonR = 2
axonL = 150
doff = dendL + somaR

class Cell:
    def __init__(self, x, y, z):
        self.id = 1
        self.x = x
        self.y = y
        self.z = z
        self.Excitatory = 1
        self.name = 'superficial interneurons basket'
        self.soma = h.Section(name='soma', cell=self)
        self.soma.pt3dclear()
        self.soma.pt3dadd(x, y, z + somaR, 2.0 * somaR)
        self.soma.pt3dadd(x, y, z - somaR, 2.0 * somaR)

        self.dend = h.Section(name='dend', cell=self)
        self.dend.pt3dclear()
        self.dend.pt3dadd(x, y, z - somaR, 2.0 * dendR)
        self.dend.pt3dadd(x, y, z - somaR - dendL, 2.0 * dendR)
        self.dend.nseg = 10
        self.dend.connect(self.soma, 1, 0)

        self.axon = h.Section(name='axon', cell=self)
        self.axon.pt3dclear()
        self.axon.pt3dadd(x, y, z + axonR, 2.0 * axonR)
        self.axon.pt3dadd(x, y, z + axonR + axonL, 2.0 * axonR)
        self.axon.connect(self.soma, 0, 1)

        self.all = [self.soma, self.dend]
        self.somaV = h.Vector()
        self.somaV.record(self.soma(0.5)._ref_v)

        self.dendV = h.Vector()
        self.dendV.record(self.dend(0.5)._ref_v)
        self.axonV = h.Vector()
        self.axonV.record(self.axon(0.5)._ref_v)
        
        self._spike_detector = h.NetCon(self.soma(0.5)._ref_v, None, sec=self.soma)
        self.spike_times = h.Vector()
        self._spike_detector.record(self.spike_times)
        
        self._ncs = []
        self.synlistex = []

        self.synE=h.AMPA(self.soma(0.8))
        self.synE.tau = 1
        self.synE.e = 50
        self.synlistex.append(self.synE)

        self.synI=h.GABAA(self.soma(0.8))
        self.synI.tau = 1
        self.synI.e = -50
        self.synlistex.append(self.synI)


        

class Bask23(Cell):
    def __init__(self, x, y, z):
        super().__init__(x , y, z)
        self.id = 1
        self.Excitatory = 1
        self.name = 'superficial interneurons basket'
        
        # ---------------soma----------------
        for mechanism_s in ['extracellular','naf2', 'nap', 'kdr_fs', 'kc_fast', 'ka', 'km', 'k2', 'kahp_slower', 'cal', 'cat', 'ar', 'cad', 'pas']:
            self.soma.insert(mechanism_s)
            #print(mechanism_s)

        self.soma(0.5).naf2.gbar = 0.06
        self.soma(0.5).nap.gbar = 0.0006
        self.soma(0.5).kdr_fs.gbar = 0.1
        self.soma(0.5).kc_fast.gbar = 0
        self.soma(0.5).ka.gbar = 0.001
        self.soma(0.5).km.gbar = 0.0005
        self.soma(0.5).k2.gbar = 0.0005
        self.soma(0.5).kahp_slower.gbar = 0.0001
        self.soma(0.5).cal.gbar = 0.0001
        self.soma(0.5).cat.gbar = 5.E-05
        self.soma(0.5).ar.gbar = 2.5E-05
        self.soma(0.5).cad.beta  = 0.02
        self.soma(0.5).cad.phi =  260000.
        self.soma(0.5).pas.g = 4.E-05
        self.soma.Ra = 200
        self.soma(0.5).ar.erev =  -40.
        self.soma(0.5).pas.e=-65

        # ---------------dend----------------
        for mechanism_d in ['naf2', 'nap', 'kdr_fs', 'kc_fast', 'ka', 'km', 'k2', 'kahp_slower', 'cal', 'cat', 'ar', 'cad', 'pas']:
            self.dend.insert(mechanism_d)
            #print(mechanism_d)

        self.dend(0.5).naf2.gbar =   0.001
        self.dend(0.5).nap.gbar =   0.0001
        self.dend(0.5).kdr_fs.gbar =   0.01
        self.dend(0.5).kc_fast.gbar =   0.000025
        self.dend(0.5).ka.gbar =   0.001
        self.dend(0.5).km.gbar =   0.0005
        self.dend(0.5).k2.gbar =   0.0005
        self.dend(0.5).kahp_slower.gbar =   0.0001
        self.dend(0.5).cal.gbar =   0.0002
        self.dend(0.5).cat.gbar =   0.002
        self.dend(0.5).ar.gbar =   2.5E-05
        self.dend(0.5).cad.beta  =   0.05
        self.dend(0.5).cad.phi =   520000.
        self.dend(0.5).pas.g = 4.E-05
        self.dend.Ra = 200
        self.soma(0.5).ar.erev =  -40.

        # ---------------axon----------------
        for mechanism_a in ['naf2', 'kdr_fs', 'ka', 'k2', 'pas']:
            self.axon.insert(mechanism_a)
            #print(mechanism_a)

        self.axon(0.5).naf2.gbar = 0.4
        self.axon(0.5).kdr_fs.gbar = 0.4
        self.axon(0.5).ka.gbar = 0.001
        self.axon(0.5).k2.gbar = 0.0005
        self.axon(0.5).pas.g = 0.001
        self.axon.Ra = 100

        for sec in self.all:        
            sec.cm = 1
           # ek = -100.
            #e = -65.
            #ena = 50.
            #vca = 125.

        self.n_km = h.Vector().record(self.dend(0.5).km._ref_n)
        self.h_cat = h.Vector().record(self.dend(0.5).cat._ref_h)
        self.h_k2 = h.Vector().record(self.dend(0.5).k2._ref_h)
        self.h_ka = h.Vector().record(self.dend(0.5).ka._ref_h)
        self.h_naf2 = h.Vector().record(self.dend(0.5).naf2._ref_h)
        self.m_ar = h.Vector().record(self.dend(0.5).ar._ref_m)
        self.m_cal = h.Vector().record(self.dend(0.5).cal._ref_m)
        self.m_cat = h.Vector().record(self.dend(0.5).cat._ref_m)
        self.m_k2 = h.Vector().record(self.dend(0.5).k2._ref_m)
        self.m_kahp_slower = h.Vector().record(self.dend(0.5).kahp_slower._ref_m)
        self.m_ka = h.Vector().record(self.dend(0.5).ka._ref_m)
        self.m_kc_fast = h.Vector().record(self.dend(0.5).kc_fast._ref_m)
        self.m_kdr_fs = h.Vector().record(self.dend(0.5).kdr_fs._ref_m)
        self.m_naf2 = h.Vector().record(self.dend(0.5).naf2._ref_m)
        self.m_nap = h.Vector().record(self.dend(0.5).nap._ref_m)

        self.nmh_list_dend =[self.n_km, self.h_cat, self.h_k2, self.h_ka, self.h_naf2, self.m_ar, self.m_cal, 
                            self.m_cat, self.m_k2, self.m_kahp_slower, self.m_ka, self.m_kc_fast, self.m_kdr_fs, self.m_naf2, self.m_nap ]

        self.m_k2_axon = h.Vector().record(self.axon(0.5).k2._ref_m)
        self.m_ka_axon = h.Vector().record(self.axon(0.5).ka._ref_m)
        self.m_kdr_fs_axon = h.Vector().record(self.axon(0.5).kdr_fs._ref_m)
        self.m_naf2_axon = h.Vector().record(self.axon(0.5).naf2._ref_m)
        self.h_k2_axon = h.Vector().record(self.axon(0.5).k2._ref_h)
        self.h_ka_axon = h.Vector().record(self.axon(0.5).ka._ref_h)
        self.h_naf2_axon = h.Vector().record(self.axon(0.5).naf2._ref_h)

        self.nmh_list_axon = [self.m_k2_axon, self.m_ka_axon, self.m_kdr_fs_axon, self.m_naf2_axon, self.h_k2_axon, self.h_ka_axon,self.h_naf2_axon]

        self.k_vec = h.Vector().record(self.dend(0.5)._ref_ik)
        self.na_vec = h.Vector().record(self.dend(0.5)._ref_ina)
        self.na_concentration = h.Vector().record(self.dend(0.5)._ref_nai)
        self.k_concentration = h.Vector().record(self.dend(0.5)._ref_ki)
        self.v_vec = h.Vector().record(self.soma(0.5)._ref_vext[0])
        self.cyt = rxd.Region(self.all, name='cyt', nrn_region='i', dx=1.0,
                               geometry=rxd.FractionalVolume(0.9, surface_fraction=1.0))
        self.na = rxd.Species([self.cyt], name='na', charge=1, d=1.0, initial=10)
        self.k = rxd.Species([self.cyt], name='k', charge=1, d=1.0, initial=148)
        self.k_i = self.k[self.cyt]

        self.ca = rxd.Species([self.cyt], d=0.08, name='ca', charge=2, initial=1.e-4, atolscale=1e-6)
        #self.cl_vec = h.Vector().record(self.soma(0.5)._ref_icl)
        #self.cl_concentration = h.Vector().record(self.soma(0.5)._ref_cli) 

    def conect(self, target):
            self.nc = h.NetCon(self.soma(0.5)._ref_v, target.synE, sec=self.soma)
            self.nc.weight[0] = 10
            self.nc.delay = 5
            target._ncs.append(self.nc)

        #------for test-----------
        #self.stim = h.IClamp(self.soma(0.5))
        #self.stim.delay = 50
        #self.stim.dur = 1
        #self.stim.amp = 1
        #print(self.id)
        #print(self.axon.psection())

class Axax23(Cell): #
    def __init__(self, x, y, z):
        super().__init__(x , y, z)
        self.id = 2
        self.Excitatory = 1
        self.name = 'superficial interneurons axoaxonic'
        # ---------------soma----------------
        for mechanism_s in ['extracellular','naf2', 'nap', 'kdr_fs', 'kc_fast', 'ka', 'km', 'k2', 'kahp_slower', 'cal', 'cat', 'ar', 'cad', 'pas']:
            self.soma.insert(mechanism_s)
            #print(mechanism_s)

        self.soma(0.5).naf2.gbar = 0.06
        self.soma(0.5).nap.gbar = 0.0006
        self.soma(0.5).kdr_fs.gbar = 0.1
        self.soma(0.5).kc_fast.gbar = 0.025
        self.soma(0.5).ka.gbar = 0.001
        self.soma(0.5).km.gbar = 0.0005
        self.soma(0.5).k2.gbar = 0.0005
        self.soma(0.5).kahp_slower.gbar = 0.0001
        self.soma(0.5).cal.gbar = 0.0001
        self.soma(0.5).cat.gbar = 5.E-05
        self.soma(0.5).ar.gbar = 2.5E-05
        self.soma(0.5).cad.beta  = 0.02
        self.soma(0.5).cad.phi =  260000.
        self.soma(0.5).pas.g = 2.E-05
        self.soma(0.5).pas.e = -65
        self.soma.Ra =   250.

        # ---------------dend----------------
        for mechanism_d in ['naf2', 'nap', 'kdr_fs', 'kc_fast', 'ka', 'km', 'k2', 'kahp_slower', 'cal', 'cat', 'ar', 'cad', 'pas']:
            self.dend.insert(mechanism_d)
            #print(mechanism_d)

        self.dend(0.5).naf2.gbar =   0.06
        self.dend(0.5).nap.gbar =   0.0006
        self.dend(0.5).kdr_fs.gbar =   0.01
        self.dend(0.5).kc_fast.gbar =   0.025
        self.dend(0.5).ka.gbar =   0.001
        self.dend(0.5).km.gbar =   0.0005
        self.dend(0.5).k2.gbar =   0.0005
        self.dend(0.5).kahp_slower.gbar =   0.0001
        self.dend(0.5).cal.gbar =   0.0001
        self.dend(0.5).cat.gbar =   5.E-05
        self.dend(0.5).ar.gbar =   2.5E-05
        self.dend(0.5).cad.beta  =   0.05
        self.dend(0.5).cad.phi =   520000.
        self.dend(0.5).pas.g = 2.E-05
        self.dend(0.5).pas.e = -65
        self.dend.Ra =   250.


        # ---------------axon----------------
        for mechanism_a in ['naf2', 'kdr_fs', 'ka', 'k2', 'pas']:
            self.axon.insert(mechanism_a)
            #print(mechanism_a)

        self.axon(0.5).naf2.gbar = 0.4
        self.axon(0.5).kdr_fs.gbar = 0.4
        self.axon(0.5).ka.gbar = 0.001
        self.axon(0.5).k2.gbar = 0.0005
        self.axon(0.5).pas.g = 0.001
        self.axon(0.5).pas.e = -65
        self.axon.Ra = 100.
        
        for sec in self.all:        
            sec.cm = 0.9
            sec.ena =   50.
            #sec.eca =   125.

        self.k_vec = h.Vector().record(self.dend(0.5)._ref_ik)
        self.na_vec = h.Vector().record(self.dend(0.5)._ref_ina)
        self.na_concentration = h.Vector().record(self.dend(0.5)._ref_nai)
        self.k_concentration = h.Vector().record(self.dend(0.5)._ref_ki)

        self.v_vec = h.Vector().record(self.soma(0.5)._ref_vext[0])
        self.cyt = rxd.Region(self.all, name='cyt', nrn_region='i', dx=1.0, geometry=rxd.FractionalVolume(0.9, surface_fraction=1.0))
        self.na = rxd.Species([self.cyt], name='na', charge=1, d=1.0, initial=10)
        self.k = rxd.Species([self.cyt], name='k', charge=1, d=1.0, initial=148)
        self.k_i= self.k[self.cyt]
        self.v_vec = h.Vector().record(self.soma(0.5)._ref_vext[0])
        self.ca = rxd.Species([self.cyt], d=0.08, name='ca', charge=2, initial=1.e-4, atolscale=1e-6)
        #------for test-----------
        #self.stim = h.IClamp(self.soma(0.5))
        #self.stim.delay = 50
        #self.stim.dur = 1
        #self.stim.amp = 1
        #print(self.id)
    def conect(self, target):
            self.nc = h.NetCon(self.soma(0.5)._ref_v, target.synE, sec=self.soma)
            self.nc.weight[0] = 10
            self.nc.delay = 5
            target._ncs.append(self.nc)


class LTS23(Cell):  #
    def __init__(self, x, y, z):
        super().__init__(x , y, z)
        self.id = 3
        self.Excitatory = 1
        self.name = 'superficial interneurons low threshold spiking'
        # ---------------soma----------------
        for mechanism_s in ['extracellular','naf2', 'nap', 'kdr_fs', 'kc_fast', 'ka', 'km', 'k2', 'kahp_slower', 'cal', 'cat', 'ar', 'cad', 'pas']:
            self.soma.insert(mechanism_s)
            #print(mechanism_s)

        self.soma(0.5).naf2.gbar = 0.06
        self.soma(0.5).nap.gbar = 0.0006
        self.soma(0.5).kdr_fs.gbar = 0.1
        self.soma(0.5).kc_fast.gbar = 0.025
        self.soma(0.5).ka.gbar = 0.001
        self.soma(0.5).km.gbar = 0.0005
        self.soma(0.5).k2.gbar = 0.0005
        self.soma(0.5).kahp_slower.gbar = 0.0001
        self.soma(0.5).cal.gbar = 0.0001
        self.soma(0.5).cat.gbar = 5.E-05
        self.soma(0.5).ar.gbar = 2.5E-05
        self.soma(0.5).cad.beta  = 0.02
        self.soma(0.5).cad.phi =  260000.
        self.soma(0.5).pas.g = 4.E-05
        self.soma(0.5).pas.e = -65
        self.soma.Ra =   250.
        # ---------------dend----------------
        for mechanism_d in ['naf2', 'nap', 'kdr_fs', 'kc_fast', 'ka', 'km', 'k2', 'kahp_slower', 'cal', 'cat', 'ar', 'cad', 'pas']:
            self.dend.insert(mechanism_d)
            #print(mechanism_d)

        self.dend(0.5).naf2.gbar =   0.06
        self.dend(0.5).nap.gbar =   0.0006
        self.dend(0.5).kdr_fs.gbar =   0.01
        self.dend(0.5).kc_fast.gbar =   0.025
        self.dend(0.5).ka.gbar =   0.001
        self.dend(0.5).km.gbar =   0.0005
        self.dend(0.5).k2.gbar =   0.0005
        self.dend(0.5).kahp_slower.gbar =   0.0001
        self.dend(0.5).cal.gbar =   0.0001
        self.dend(0.5).cat.gbar =   5.E-05
        self.dend(0.5).ar.gbar =   2.5E-05
        self.dend(0.5).cad.beta  =   0.05
        self.dend(0.5).cad.phi =   520000.
        self.dend(0.5).pas.g = 4.E-05
        self.dend(0.5).pas.e = -65
        self.dend.Ra =   250.

        # ---------------axon----------------
        for mechanism_a in ['naf2', 'kdr_fs', 'ka', 'k2', 'pas']:
            self.axon.insert(mechanism_a)
            #print(mechanism_a)

        self.axon(0.5).naf2.gbar = 0.4
        self.axon(0.5).kdr_fs.gbar = 0.4
        self.axon(0.5).ka.gbar = 0.001
        self.axon(0.5).k2.gbar = 0.0005
        self.axon(0.5).pas.g = 0.001
        self.axon(0.5).pas.e = -65
        self.axon.Ra = 100.

        for sec in self.all:        
            sec.cm = 1
            sec.ena = 50.

        self.k_vec = h.Vector().record(self.dend(0.5)._ref_ik)
        self.na_vec = h.Vector().record(self.dend(0.5)._ref_ina)
        self.na_concentration = h.Vector().record(self.dend(0.5)._ref_nai)
        self.k_concentration = h.Vector().record(self.dend(0.5)._ref_ki)
        self.v_vec = h.Vector().record(self.soma(0.5)._ref_vext[0])
        self.cyt = rxd.Region(self.all, name='cyt', nrn_region='i', dx=1.0,
                              geometry=rxd.FractionalVolume(0.9, surface_fraction=1.0))
        self.na = rxd.Species([self.cyt], name='na', charge=1, d=1.0, initial=10)
        self.k = rxd.Species([self.cyt], name='k', charge=1, d=1.0, initial=148)
        self.k_i = self.k[self.cyt]
        self.ca = rxd.Species([self.cyt], d=0.08, name='ca', charge=2, initial=1.e-4, atolscale=1e-6)
        #------for test-----------
        #self.stim = h.IClamp(self.soma(0.5))
        #self.stim.delay = 50
        #self.stim.dur = 1
        #self.stim.amp = 1
        #print(self.id)
    def conect(self, target):
            self.nc = h.NetCon(self.soma(0.5)._ref_v, target.synE, sec=self.soma)
            self.nc.weight[0] = 10
            self.nc.delay = 5
            target._ncs.append(self.nc)

class Spinstel4(Cell):  #
    def __init__(self, x, y, z):
        super().__init__(x , y, z)
        self.id = 4
        self.Excitatory = -1
        self.name = 'spiny stellate'
        
        # ---------------soma----------------
        for mechanism_s in ['extracellular','naf2', 'pas' ,'napf_spinstell', 'kdr_fs', 'kc_fast', 'ka', 'km', 'k2', 'kahp_slower', 'cal', 'cat', 'ar', 'cad']:
            self.soma.insert(mechanism_s)
            #print(mechanism_s)

        self.soma(0.5).naf2.gbar = 0.15
        self.soma(0.5).napf_spinstell.gbar = 0.00015
        self.soma(0.5).kdr_fs.gbar = 0.1
        self.soma(0.5).kc_fast.gbar = 0.01
        self.soma(0.5).ka.gbar = 0.03
        self.soma(0.5).km.gbar = 0.00375
        self.soma(0.5).k2.gbar = 0.0001
        self.soma(0.5).kahp_slower.gbar = 0.0001
        self.soma(0.5).cal.gbar = 0.0005
        self.soma(0.5).cat.gbar = 0.0001
        self.soma(0.5).ar.gbar = 0.00025
        self.soma(0.5).cad.beta  = 0.02
        self.soma(0.5).cad.phi =  260000.
        self.soma(0.5).pas.g = 2.E-05
        self.soma(0.5).pas.e = -65
        self.soma.Ra =   250.



        # ---------------dend----------------
        for mechanism_d in ['naf2', 'napf_spinstell','pas', 'kdr_fs', 'kc_fast', 'ka', 'km', 'k2', 'kahp_slower', 'cal', 'cat', 'ar', 'cad']:
            self.dend.insert(mechanism_d)
            #print(mechanism_d)

        self.dend(0.5).naf2.gbar =   0.075
        self.dend(0.5).napf_spinstell.gbar = 7.5E-05
        self.dend(0.5).kdr_fs.gbar =   0.075
        self.dend(0.5).kc_fast.gbar =   0.01
        self.dend(0.5).ka.gbar =   0.03
        self.dend(0.5).km.gbar =   0.00375
        self.dend(0.5).k2.gbar =   0.0001
        self.dend(0.5).kahp_slower.gbar =   0.0001
        self.dend(0.5).cal.gbar =   0.0005
        self.dend(0.5).cat.gbar =   0.0001
        self.dend(0.5).ar.gbar =   0.00025
        self.dend(0.5).cad.beta  =   0.05
        self.dend(0.5).cad.phi =   260000.
        self.dend(0.5).pas.g = 2.E-05
        self.dend(0.5).pas.e = -65
        self.dend.Ra =   250.

        # ---------------axon----------------
        for mechanism_a in ['naf2', 'kdr_fs', 'ka', 'k2', 'pas']:
            self.axon.insert(mechanism_a)
            #print(mechanism_a)

        self.axon(0.5).naf2.gbar = 0.4
        self.axon(0.5).kdr_fs.gbar = 0.4
        self.axon(0.5).ka.gbar = 0.002
        self.axon(0.5).k2.gbar = 0.0001
        self.axon(0.5).pas.g = 0.001
        self.axon(0.5).pas.e = -65
        self.axon.Ra = 100.

        for sec in self.all:        
            sec.cm = 0.9
            sec.ena = 50.

        self.k_vec = h.Vector().record(self.dend(0.5)._ref_ik)
        self.na_vec = h.Vector().record(self.dend(0.5)._ref_ina)
        self.na_concentration = h.Vector().record(self.dend(0.5)._ref_nai)
        self.k_concentration = h.Vector().record(self.dend(0.5)._ref_ki)
        self.v_vec = h.Vector().record(self.soma(0.5)._ref_vext[0])
        self.cyt = rxd.Region(self.all, name='cyt', nrn_region='i', dx=1.0,
                              geometry=rxd.FractionalVolume(0.9, surface_fraction=1.0))
        self.na = rxd.Species([self.cyt], name='na', charge=1, d=1.0, initial=10)
        self.k = rxd.Species([self.cyt], name='k', charge=1, d=1.0, initial=148)
        self.k_i = self.k[self.cyt]
        self.ca = rxd.Species([self.cyt], d=0.08, name='ca', charge=2, initial=1.e-4, atolscale=1e-6)
        #self.cl_vec = h.Vector().record(self.soma(0.5)._ref_icl)
        #self.cl_concentration = h.Vector().record(self.soma(0.5)._ref_cli) 


    def conect(self, target):
        self.nc = h.NetCon(self.soma(0.5)._ref_v, target.synI, sec=self.soma)
        self.nc.weight[0] = 10
        self.nc.delay = 5
        target._ncs.append(self.nc)

        #------for test-----------
        #self.stim = h.IClamp(self.soma(0.5))
        #self.stim.delay = 50
        #self.stim.dur = 1
        #self.stim.amp = 1
        #print(self.id)

class TuftIB5(Cell):  #
    def __init__(self, x, y, z):
        super().__init__(x , y, z)
        self.id = 5
        self.Excitatory = -1
        self.name = 'pyramidal tufted intrinsic bursting'
        
        # ---------------soma----------------
        for mechanism_s in ['extracellular','naf','pas', 'nap', 'kdr', 'kc', 'ka_ib', 'km', 'kahp_deeppyr', 'k2', 'cal', 'cat', 'ar', 'cad']:
            self.soma.insert(mechanism_s)
            #print(mechanism_s)

        self.soma(0.5).naf.gbar = 0.2
        self.soma(0.5).nap.gbar = 0.0008
        self.soma(0.5).kdr.gbar = 0.17
        self.soma(0.5).kc.gbar = 0.008
        self.soma(0.5).ka_ib.gbar = 0.02
        self.soma(0.5).km.gbar = 0.0085
        self.soma(0.5).k2.gbar = 0.0005
        self.soma(0.5).kahp_deeppyr.gbar = 0.0002
        self.soma(0.5).cal.gbar = 0.0004
        self.soma(0.5).cat.gbar = 0.0001
        self.soma(0.5).ar.gbar = 0.0001
        self.soma(0.5).ar.erev =  -40.
        self.soma(0.5).cad.beta  = 0.01
        self.soma(0.5).cad.phi =  4333.33333
        self.soma(0.5).pas.g = 2.E-05
        self.soma(0.5).pas.e = -70
        self.soma.Ra =   250.




        # ---------------dend----------------
        for mechanism_d in ['naf', 'nap','pas', 'kdr', 'kc', 'ka_ib', 'km', 'k2', 'kahp_deeppyr', 'cal', 'cat', 'ar', 'cad']:
            self.dend.insert(mechanism_d)
            #print(mechanism_d)

        self.dend(0.5).naf.gbar =   0.075
        self.dend(0.5).nap.gbar = 0.0003
        self.dend(0.5).kdr.gbar =   0.075
        self.dend(0.5).kc.gbar =   0.008
        self.dend(0.5).ka_ib.gbar =   0.008
        self.dend(0.5).km.gbar =   0.00375
        self.dend(0.5).k2.gbar =   0.0005
        self.dend(0.5).kahp_deeppyr.gbar =   0.0002
        self.dend(0.5).cal.gbar =   0.0004
        self.dend(0.5).cat.gbar =   0.0001
        self.dend(0.5).ar.gbar =   0.0001
        self.dend(0.5).ar.erev =  -40.
        self.dend(0.5).cad.beta  =   0.02
        self.dend(0.5).cad.phi =   86666.6667
        self.dend(0.5).pas.g = 2.E-05
        self.dend(0.5).pas.e = -70
        self.dend.Ra =   250.

        # ---------------axon----------------
        for mechanism_a in ['naf', 'kdr', 'ka_ib', 'km', 'pas']:
            self.axon.insert(mechanism_a)
            #print(mechanism_a)

        self.axon(0.5).naf.gbar = 0.45
        self.axon(0.5).kdr.gbar = 0.45
        self.axon(0.5).ka_ib.gbar = 0.0006
        self.axon(0.5).km.gbar = 0.03
        self.axon(0.5).pas.g = 0.001
        self.axon(0.5).pas.e = -70
        self.axon.Ra = 100.

        for sec in self.all:        
            sec.cm = 0.9
            sec.ena = 50.

        self.k_vec = h.Vector().record(self.dend(0.5)._ref_ik)
        self.na_vec = h.Vector().record(self.dend(0.5)._ref_ina)
        self.na_concentration = h.Vector().record(self.dend(0.5)._ref_nai)
        self.k_concentration = h.Vector().record(self.dend(0.5)._ref_ki)
        self.v_vec = h.Vector().record(self.soma(0.5)._ref_vext[0])
        self.cyt = rxd.Region(self.all, name='cyt', nrn_region='i', dx=1.0,
                              geometry=rxd.FractionalVolume(0.9, surface_fraction=1.0))
        self.na = rxd.Species([self.cyt], name='na', charge=1, d=1.0, initial=10)
        self.k = rxd.Species([self.cyt], name='k', charge=1, d=1.0, initial=148)
        self.k_i = self.k[self.cyt]
        self.ca = rxd.Species([self.cyt], d=0.08, name='ca', charge=2, initial=1.e-4, atolscale=1e-6)

        #------for test-----------
        #self.stim = h.IClamp(self.soma(0.5))
        #self.stim.delay = 50
        #self.stim.dur = 1
        #self.stim.amp = 1
        #print(self.id)
    def conect(self, target):
        self.nc = h.NetCon(self.soma(0.5)._ref_v, target.synI, sec=self.soma)
        self.nc.weight[0] = 10
        self.nc.delay = 5
        target._ncs.append(self.nc)

class TuftRS5(Cell):  #
    def __init__(self, x, y, z):
        super().__init__(x , y, z)
        self.id = 6
        self.Excitatory = -1
        self.name = 'pyramidal tufted regular spiking'
        
        # ---------------soma----------------
        for mechanism_s in ['extracellular', 'pas', 'naf', 'nap', 'kdr', 'kc', 'ka', 'km', 'kahp_deeppyr', 'k2', 'cal', 'cat', 'ar', 'cad']:
            self.soma.insert(mechanism_s)
            #print(mechanism_s)

        self.soma(0.5).naf.gbar =   0.02
        self.soma(0.5).nap.gbar = 0.0008
        self.soma(0.5).kdr.gbar =   0.17
        self.soma(0.5).kc.gbar =   0.008
        self.soma(0.5).ka.gbar =   0.02
        self.soma(0.5).km.gbar =   0.0085
        self.soma(0.5).k2.gbar =   0.0005
        self.soma(0.5).kahp_deeppyr.gbar =   0.0002
        self.soma(0.5).cal.gbar =   0.0004
        self.soma(0.5).cat.gbar =   0.0001
        self.soma(0.5).ar.gbar =   0.0001
        self.soma(0.5).cad.beta  =   0.02
        self.soma(0.5).cad.phi =   4333.33333
        self.soma(0.5).pas.g = 2.E-05
        self.soma(0.5).pas.e = -70.
        self.soma.Ra =   250.

        # ---------------dend----------------
        for mechanism_d in ['naf', 'pas', 'nap', 'kdr', 'kc', 'ka', 'km', 'kahp_deeppyr', 'k2', 'cal', 'cat', 'ar', 'cad']:
            self.dend.insert(mechanism_d)
            #print(mechanism_d)

        self.dend(0.5).naf.gbar =   0.075
        self.dend(0.5).nap.gbar = 0.0003
        self.dend(0.5).kdr.gbar =   0.075
        self.dend(0.5).kc.gbar =   0.008
        self.dend(0.5).ka.gbar =   0.008
        self.dend(0.5).km.gbar =   0.0136
        self.dend(0.5).k2.gbar =   0.0005
        self.dend(0.5).kahp_deeppyr.gbar =   0.0002
        self.dend(0.5).cal.gbar =   0.0004
        self.dend(0.5).cat.gbar =   0.0001
        self.dend(0.5).ar.gbar =   0.0001
        self.dend(0.5).cad.beta  =   0.02
        self.dend(0.5).cad.phi =   86666.6667
        self.dend(0.5).pas.g = 2.E-05
        self.dend(0.5).pas.e =  -70.
        self.dend.Ra =   250.

        # ---------------axon----------------
        for mechanism_a in ['naf', 'kdr', 'ka', 'k2', 'km', 'pas']:
            self.axon.insert(mechanism_a)
            #print(mechanism_a)

        self.axon(0.5).naf.gbar = 0.45
        self.axon(0.5).kdr.gbar = 0.45
        self.axon(0.5).ka.gbar = 0.0006
        self.axon(0.5).k2.gbar = 0.0005
        self.axon(0.5).km.gbar = 0.03
        self.axon(0.5).pas.g = 0.001
        self.axon(0.5).pas.e =  -70.
        self.axon.Ra =   100.

        for sec in self.all:        
            sec.cm = 0.9
            sec.ena = 50.
            sec.ek =  -95.

        self.k_vec = h.Vector().record(self.dend(0.5)._ref_ik)
        self.na_vec = h.Vector().record(self.dend(0.5)._ref_ina)
        self.na_concentration = h.Vector().record(self.dend(0.5)._ref_nai)
        self.k_concentration = h.Vector().record(self.dend(0.5)._ref_ki)
        self.v_vec = h.Vector().record(self.soma(0.5)._ref_vext[0])
        self.cyt = rxd.Region(self.all, name='cyt', nrn_region='i', dx=1.0,
                              geometry=rxd.FractionalVolume(0.9, surface_fraction=1.0))
        self.na = rxd.Species([self.cyt], name='na', charge=1, d=1.0, initial=10)
        self.k = rxd.Species([self.cyt], name='k', charge=1, d=1.0, initial=148)
        self.k_i = self.k[self.cyt]
        self.ca = rxd.Species([self.cyt], d=0.08, name='ca', charge=2, initial=1.e-4, atolscale=1e-6)

        #------for test-----------
        #self.stim = h.IClamp(self.soma(0.5))
        #self.stim.delay = 50
        #self.stim.dur = 1
        #self.stim.amp = 1
        #print(self.id)
    def conect(self, target):
        self.nc = h.NetCon(self.soma(0.5)._ref_v, target.synI, sec=self.soma)
        self.nc.weight[0] = 10
        self.nc.delay = 5
        target._ncs.append(self.nc)


class Bask56(Cell):  #
    def __init__(self, x, y, z):
        super().__init__(x , y, z)
        self.id = 7
        self.Excitatory = 1
        self.name = 'deep interneurons basket'
        # ---------------soma----------------
        for mechanism_s in ['extracellular','naf2', 'pas', 'nap', 'kdr_fs', 'kc_fast', 'ka', 'km', 'k2', 'kahp_slower', 'cal', 'cat', 'ar', 'cad']:
            self.soma.insert(mechanism_s)
            #print(mechanism_s)

        self.soma(0.5).naf2.gbar = 0.06
        self.soma(0.5).nap.gbar = 0.0006
        self.soma(0.5).kdr_fs.gbar = 0.1
        self.soma(0.5).kc_fast.gbar = 0.025
        self.soma(0.5).ka.gbar = 0.001
        self.soma(0.5).km.gbar = 0.0005
        self.soma(0.5).k2.gbar = 0.0005
        self.soma(0.5).kahp_slower.gbar = 0.0001
        self.soma(0.5).cal.gbar = 0.0001
        self.soma(0.5).cat.gbar = 5.E-05
        self.soma(0.5).ar.gbar = 2.5E-05
        self.soma(0.5).ar.erev = -40
        self.soma(0.5).cad.beta  = 0.02
        self.soma(0.5).cad.phi =  260000.
        self.soma(0.5).pas.e = -65
        self.soma(0.5).pas.g = 4.E-05
        self.soma.Ra = 200.

        # ---------------dend----------------
        for mechanism_d in ['naf2', 'pas', 'nap', 'kdr_fs', 'kc_fast', 'ka', 'km', 'k2', 'kahp_slower', 'cal', 'cat', 'ar', 'cad']:
            self.dend.insert(mechanism_d)
            #print(mechanism_d)

        self.dend(0.5).naf2.gbar =   0.06
        self.dend(0.5).nap.gbar = 0.0006
        self.dend(0.5).kdr_fs.gbar =   0.1
        self.dend(0.5).kc_fast.gbar =   0.025
        self.dend(0.5).ka.gbar =   0.001
        self.dend(0.5).km.gbar =   0.0005
        self.dend(0.5).k2.gbar =   0.0005
        self.dend(0.5).kahp_slower.gbar =   0.0001
        self.dend(0.5).cal.gbar =   0.0001
        self.dend(0.5).cat.gbar =   5.E-05
        self.dend(0.5).ar.gbar =   2.5E-05
        self.dend(0.5).ar.erev = -40
        self.dend(0.5).cad.beta  =   0.05
        self.dend(0.5).cad.phi =   520000.
        self.dend(0.5).pas.e = -65
        self.dend(0.5).pas.g = 4.E-05
        self.dend.Ra = 200.

        # ---------------axon----------------
        for mechanism_a in ['naf2', 'kdr_fs', 'ka', 'k2', 'pas']:
            self.axon.insert(mechanism_a)
            #print(mechanism_a)

        self.axon(0.5).naf2.gbar = 0.4
        self.axon(0.5).kdr_fs.gbar = 0.4
        self.axon(0.5).ka.gbar = 0.001
        self.axon(0.5).k2.gbar = 0.0005
        self.axon(0.5).pas.g = 0.001
        self.axon(0.5).pas.e = -65
        self.axon.Ra = 100

        for sec in self.all:        
            sec.cm = 1
            sec.ena = 50.
            sec.ek =  -100.

        self.k_vec = h.Vector().record(self.dend(0.5)._ref_ik)
        self.na_vec = h.Vector().record(self.dend(0.5)._ref_ina)
        self.na_concentration = h.Vector().record(self.dend(0.5)._ref_nai)
        self.k_concentration = h.Vector().record(self.dend(0.5)._ref_ki)
        self.v_vec = h.Vector().record(self.soma(0.5)._ref_vext[0])
        self.cyt = rxd.Region(self.all, name='cyt', nrn_region='i', dx=1.0,
                              geometry=rxd.FractionalVolume(0.9, surface_fraction=1.0))
        self.na = rxd.Species([self.cyt], name='na', charge=1, d=1.0, initial=10)
        self.k = rxd.Species([self.cyt], name='k', charge=1, d=1.0, initial=148)
        self.k_i = self.k[self.cyt]
        self.ca = rxd.Species([self.cyt], d=0.08, name='ca', charge=2, initial=1.e-4, atolscale=1e-6)
        #------for test-----------
        #self.stim = h.IClamp(self.soma(0.5))
        #self.stim.delay = 50
        #self.stim.dur = 1
        #self.stim.amp = 1
        #print(self.id)
    def conect(self, target):
            self.nc = h.NetCon(self.soma(0.5)._ref_v, target.synE, sec=self.soma)
            self.nc.weight[0] = 10
            self.nc.delay = 5
            target._ncs.append(self.nc)


class Axax56(Cell):  #
    def __init__(self, x, y, z):
        super().__init__(x , y, z)
        self.id = 8
        self.Excitatory = 1
        self.name = 'deep interneurons axoaxonic'
        self.soma = h.Section(name='soma', cell=self)
        # ---------------soma----------------
        for mechanism_s in ['extracellular','naf2','pas', 'nap', 'kdr_fs', 'kc_fast', 'ka', 'km', 'k2', 'kahp_slower', 'cal', 'cat', 'ar', 'cad']:
            self.soma.insert(mechanism_s)
            #print(mechanism_s)

        self.soma(0.5).naf2.gbar = 0.06
        self.soma(0.5).nap.gbar = 0.0006
        self.soma(0.5).kdr_fs.gbar = 0.1
        self.soma(0.5).kc_fast.gbar = 0.025
        self.soma(0.5).ka.gbar = 0.001
        self.soma(0.5).km.gbar = 0.0005
        self.soma(0.5).k2.gbar = 0.0005
        self.soma(0.5).kahp_slower.gbar = 0.0001
        self.soma(0.5).cal.gbar = 0.0001
        self.soma(0.5).cat.gbar = 5.E-05
        self.soma(0.5).ar.gbar = 2.5E-05
        self.soma(0.5).ar.erev = -40
        self.soma(0.5).cad.beta  = 0.02
        self.soma(0.5).cad.phi =  260000.
        self.soma(0.5).pas.e = -65
        self.soma(0.5).pas.g = 4.E-05
        self.soma.Ra = 200.


        # ---------------dend----------------
        for mechanism_d in ['naf2', 'pas', 'nap', 'kdr_fs', 'kc_fast', 'ka', 'km', 'k2', 'kahp_slower', 'cal', 'cat', 'ar', 'cad']:
            self.dend.insert(mechanism_d)
            #print(mechanism_d)

        self.dend(0.5).naf2.gbar =   0.06
        self.dend(0.5).nap.gbar = 0.0006
        self.dend(0.5).kdr_fs.gbar =   0.1
        self.dend(0.5).kc_fast.gbar =   0.025
        self.dend(0.5).ka.gbar =   0.001
        self.dend(0.5).km.gbar =   0.0005
        self.dend(0.5).k2.gbar =   0.0005
        self.dend(0.5).kahp_slower.gbar =   0.0001
        self.dend(0.5).cal.gbar =   0.0001
        self.dend(0.5).cat.gbar =   5.E-05
        self.dend(0.5).ar.gbar =   2.5E-05
        self.dend(0.5).ar.erev = -40
        self.dend(0.5).cad.beta  =   0.05
        self.dend(0.5).cad.phi =   520000.
        self.dend(0.5).pas.e = -65
        self.dend(0.5).pas.g = 4.E-05
        self.dend.Ra = 200.

        # ---------------axon----------------
        for mechanism_a in ['naf2', 'kdr_fs', 'ka', 'k2', 'pas']:
            self.axon.insert(mechanism_a)
            #print(mechanism_a)

        self.axon(0.5).naf2.gbar = 0.4
        self.axon(0.5).kdr_fs.gbar = 0.4
        self.axon(0.5).ka.gbar = 0.001
        self.axon(0.5).k2.gbar = 0.0005
        self.axon(0.5).pas.g = 0.001
        self.axon(0.5).pas.e = -65
        self.axon.Ra = 100

        for sec in self.all:        
            sec.cm = 1
            #sec.ena = 50.
            #sec.ek =  -100.

        self.k_vec = h.Vector().record(self.dend(0.5)._ref_ik)
        self.na_vec = h.Vector().record(self.dend(0.5)._ref_ina)
        self.na_concentration = h.Vector().record(self.dend(0.5)._ref_nai)
        self.k_concentration = h.Vector().record(self.dend(0.5)._ref_ki)
        self.v_vec = h.Vector().record(self.soma(0.5)._ref_vext[0])
        self.cyt = rxd.Region(self.all, name='cyt', nrn_region='i', dx=1.0,
                              geometry=rxd.FractionalVolume(0.9, surface_fraction=1.0))
        self.na = rxd.Species([self.cyt], name='na', charge=1, d=1.0, initial=10)
        self.k = rxd.Species([self.cyt], name='k', charge=1, d=1.0, initial=148)
        self.k_i = self.k[self.cyt]
        self.ca = rxd.Species([self.cyt], d=0.08, name='ca', charge=2, initial=1.e-4, atolscale=1e-6)
        
        #------for test-----------
        #self.stim = h.IClamp(self.soma(0.5))
        #self.stim.delay = 50
        #self.stim.dur = 1
        #self.stim.amp = 1
        #print(self.id)
    def conect(self, target):
            self.nc = h.NetCon(self.soma(0.5)._ref_v, target.synE, sec=self.soma)
            self.nc.weight[0] = 10
            self.nc.delay = 5
            target._ncs.append(self.nc)


class LTS56(Cell):  #
    def __init__(self, x, y, z):
        super().__init__(x , y, z)
        self.id = 9
        self.Excitatory = 1
        self.name ='deep interneurons low threshold spiking'
        
        # ---------------soma----------------
        for mechanism_s in ['extracellular','naf2', 'pas', 'nap', 'kdr_fs', 'kc_fast', 'ka', 'km', 'k2', 'kahp_slower', 'cal', 'cat', 'ar', 'cad']:
            self.soma.insert(mechanism_s)
            #print(mechanism_s)

        self.soma(0.5).naf2.gbar = 0.06
        self.soma(0.5).nap.gbar = 0.0006
        self.soma(0.5).kdr_fs.gbar = 0.1
        self.soma(0.5).kc_fast.gbar = 0.025
        self.soma(0.5).ka.gbar = 0.001
        self.soma(0.5).km.gbar = 0.0005
        self.soma(0.5).k2.gbar = 0.0005
        self.soma(0.5).kahp_slower.gbar = 0.0001
        self.soma(0.5).cal.gbar = 0.0001
        self.soma(0.5).cat.gbar = 5.E-05
        self.soma(0.5).ar.gbar = 2.5E-05
        self.soma(0.5).ar.erev = -40
        self.soma(0.5).cad.beta  = 0.02
        self.soma(0.5).cad.phi =  260000.
        self.soma(0.5).pas.e = -65
        self.soma(0.5).pas.g = 4.E-05
        self.soma.Ra = 200.

        # ---------------dend----------------
        for mechanism_d in ['naf2', 'nap', 'pas', 'kdr_fs', 'kc_fast', 'ka', 'km', 'k2', 'kahp_slower', 'cal', 'cat', 'ar', 'cad']:
            self.dend.insert(mechanism_d)
            #print(mechanism_d)

        self.dend(0.5).naf2.gbar =   0.06
        self.dend(0.5).nap.gbar = 0.0006
        self.dend(0.5).kdr_fs.gbar =   0.1
        self.dend(0.5).kc_fast.gbar =   0.025
        self.dend(0.5).ka.gbar =   0.001
        self.dend(0.5).km.gbar =   0.0005
        self.dend(0.5).k2.gbar =   0.0005
        self.dend(0.5).kahp_slower.gbar =   0.0001
        self.dend(0.5).cal.gbar =   0.0001
        self.dend(0.5).cat.gbar =   5.E-05
        self.dend(0.5).ar.gbar =   2.5E-05
        self.soma(0.5).ar.erev = -40
        self.dend(0.5).cad.beta  =   0.05
        self.dend(0.5).cad.phi =   520000.
        self.dend(0.5).pas.e = -65
        self.dend(0.5).pas.g = 4.E-05
        self.dend.Ra = 200.

        # ---------------axon----------------
        for mechanism_a in ['naf2', 'kdr_fs', 'ka', 'k2', 'pas']:
            self.axon.insert(mechanism_a)
            #print(mechanism_a)

        self.axon(0.5).naf2.gbar = 0.4
        self.axon(0.5).kdr_fs.gbar = 0.4
        self.axon(0.5).ka.gbar = 0.001
        self.axon(0.5).k2.gbar = 0.0005
        self.axon(0.5).pas.g = 0.001
        self.axon(0.5).pas.e = -65
        self.axon.Ra = 100

        for sec in self.all:        
            sec.cm = 1
            sec.ena = 50.
            sec.ek =  -100.

        self.k_vec = h.Vector().record(self.dend(0.5)._ref_ik)
        self.na_vec = h.Vector().record(self.dend(0.5)._ref_ina)
        self.na_concentration = h.Vector().record(self.dend(0.5)._ref_nai)
        self.k_concentration = h.Vector().record(self.dend(0.5)._ref_ki)
        self.v_vec = h.Vector().record(self.soma(0.5)._ref_vext[0])
        self.cyt = rxd.Region(self.all, name='cyt', nrn_region='i', dx=1.0,
                              geometry=rxd.FractionalVolume(0.9, surface_fraction=1.0))
        self.na = rxd.Species([self.cyt], name='na', charge=1, d=1.0, initial=10)
        self.k = rxd.Species([self.cyt], name='k', charge=1, d=1.0, initial=148)
        self.k_i = self.k[self.cyt]
        self.ca = rxd.Species([self.cyt], d=0.08, name='ca', charge=2, initial=1.e-4, atolscale=1e-6)
        #------for test-----------
        #self.stim = h.IClamp(self.soma(0.5))
        #self.stim.delay = 50
        #self.stim.dur = 1
        #self.stim.amp = 1
        #print(self.id)
    def conect(self, target):
            self.nc = h.NetCon(self.soma(0.5)._ref_v, target.synE, sec=self.soma)
            self.nc.weight[0] = 10
            self.nc.delay = 5
            target._ncs.append(self.nc)


class NontuftRS6(Cell):  #
    def __init__(self, x, y, z):
        super().__init__(x , y, z)
        self.id = 10
        self.Excitatory = -1
        self.name ='pyramidal nontufted regular spiking'
        
        # ---------------soma----------------
        for mechanism_s in ['extracellular','napf', 'pas', 'naf2', 'kdr_fs', 'kc', 'ka', 'km', 'k2', 'kahp_slower', 'cal', 'cat_a', 'ar', 'cad']:
            self.soma.insert(mechanism_s)
            #print(mechanism_s)

        self.soma(0.5).naf2.gbar = 0.06
        self.soma(0.5).napf.gbar = 0.0006
        self.soma(0.5).kdr_fs.gbar = 0.06
        self.soma(0.5).ka.gbar = 0.005
        self.soma(0.5).km.gbar = 0.0005
        self.soma(0.5).kc.gbar = 0.01
        self.soma(0.5).k2.gbar = 0.0005
        self.soma(0.5).kahp_slower.gbar = 0.0001
        self.soma(0.5).cal.gbar = 0.0001
        self.soma(0.5).cat_a.gbar = 5.E-05
        self.soma(0.5).ar.gbar = 2.5E-05
        self.soma(0.5).cad.beta  = 0.02
        self.soma(0.5).cad.phi =  10400.
        self.soma(0.5).pas.e = -70
        self.soma(0.5).pas.g = 2.E-05
        self.soma.Ra = 250.

        # ---------------dend----------------
        for mechanism_d in ['naf2', 'napf', 'pas', 'kdr_fs', 'kc', 'ka', 'km', 'k2', 'kahp_slower', 'cal', 'cat_a', 'ar', 'cad']:
            self.dend.insert(mechanism_d)
            #print(mechanism_d)

        self.dend(0.5).naf2.gbar =   0.06
        self.dend(0.5).napf.gbar = 0.0006
        self.dend(0.5).kdr_fs.gbar =   0.06
        self.dend(0.5).kc.gbar =   0.01
        self.dend(0.5).ka.gbar =   0.005
        self.dend(0.5).km.gbar =   0.0005
        self.dend(0.5).k2.gbar =   0.0005
        self.dend(0.5).kahp_slower.gbar =   0.0001
        self.dend(0.5).cal.gbar =   0.0005
        self.dend(0.5).cat_a.gbar =   5.E-05
        self.dend(0.5).ar.gbar =   2.5E-05
        self.dend(0.5).cad.beta  =   0.05
        self.dend(0.5).cad.phi =   260000.
        self.dend(0.5).pas.e = -70
        self.dend(0.5).pas.g = 2.E-05
        self.dend.Ra = 250.

        # ---------------axon----------------
        for mechanism_a in ['naf2', 'kdr_fs', 'ka', 'k2', 'pas']:
            self.axon.insert(mechanism_a)
            #print(mechanism_a)

        self.axon(0.5).naf2.gbar = 0.4
        self.axon(0.5).kdr_fs.gbar = 0.4
        self.axon(0.5).ka.gbar = 0.001
        self.axon(0.5).k2.gbar = 0.0005
        self.axon(0.5).pas.g = 0.001
        self.axon(0.5).pas.e = -70
        self.axon.Ra = 100

        for sec in self.all:        
            sec.cm = 0.9
            sec.ena = 50.
            sec.ek =  -95.

        self.k_vec = h.Vector().record(self.dend(0.5)._ref_ik)
        self.na_vec = h.Vector().record(self.dend(0.5)._ref_ina)
        self.na_concentration = h.Vector().record(self.dend(0.5)._ref_nai)
        self.k_concentration = h.Vector().record(self.dend(0.5)._ref_ki)
        self.v_vec = h.Vector().record(self.soma(0.5)._ref_vext[0])
        self.cyt = rxd.Region(self.all, name='cyt', nrn_region='i', dx=1.0,
                              geometry=rxd.FractionalVolume(0.9, surface_fraction=1.0))
        self.na = rxd.Species([self.cyt], name='na', charge=1, d=1.0, initial=10)
        self.k = rxd.Species([self.cyt], name='k', charge=1, d=1.0, initial=148)
        self.k_i = self.k[self.cyt]
        self.ca = rxd.Species([self.cyt], d=0.08, name='ca', charge=2, initial=1.e-4, atolscale=1e-6)
        #------for test-----------
        #self.stim = h.IClamp(self.soma(0.5))
        #self.stim.delay = 50
        #self.stim.dur = 1
        #self.stim.amp = 1
       # print(self.id)
    def conect(self, target):
        self.nc = h.NetCon(self.soma(0.5)._ref_v, target.synI, sec=self.soma)
        self.nc.weight[0] = 10
        self.nc.delay = 5
        target._ncs.append(self.nc)

