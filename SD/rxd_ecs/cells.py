from neuron import h, crxd as rxd

somaR = 11.0  # soma radius
dendR = 1.4  # dendrite radius
dendL = 100.0  # dendrite length
axonR = 2
axonL = 150
doff = dendL + somaR

class Bask23:
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


        self.somaV = h.Vector()
        self.somaV.record(self.soma(0.5)._ref_v)

        # ---------------dend----------------
        for mechanism_d in ['naf2', 'nap', 'kdr_fs', 'kc_fast', 'ka', 'km', 'k2', 'kahp_slower', 'cal', 'cat', 'ar', 'cad', 'pas']:
            self.dend.insert(mechanism_d)
            #print(mechanism_d)

        self.dend(0.5).naf2.gbar =   0.01
        self.dend(0.5).nap.gbar =   0.0001
        self.dend(0.5).kdr_fs.gbar =   0.01
        self.dend(0.5).kc_fast.gbar =   0.025
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
            cm = 1
           # ek = -100.
            #e = -65.
            #ena = 50.
            #vca = 125.

#n km /
#m ar cal cat k2 kahp_slower ka kc_fast kdr_fs naf2 nap/ k2 ka kdr_fs naf2
#h cat k2 ka naf2/ k2 ka naf2
        #h.topology()
        '''
        {'point_processes': {}, 'density_mechs': {'pas': {'g': [0.001], 'e': [-70.0], 'i': [0.0]}, 
        'k2': {'gbar': [0.0005], 'ik': [0.0], 'm': [0.0], 'h': [0.0]}, 
        'ka': {'gbar': [0.001], 'ik': [0.0], 'mtau': [0.0], 'htau': [0.0], 'alphah': [0.0], 'betah': [0.0], 'alpham': [0.0], 'betam': [0.0], 'm': [0.0], 'h': [0.0]},
         'kdr_fs': {'gbar': [0.4], 'ik': [0.0], 'minf': [0.0], 'mtau': [0.0], 'm': [0.0]}, 
         'naf2': {'fastNa_shift': [0.0], 'a': [0.0], 'b': [0.0], 'c': [0.0], 'd': [0.0], 'gbar': [0.4], 'ina': [0.0], 'minf': [0.0], 'mtau': [0.0], 'df': [0.0], 'm': [0.0], 'h': [0.0]}}, 
         'ions': {'na': {'ena': [50.0], 'nai': [10.0], 'nao': [140.0], 'ina': [0.0], 'dina_dv_': [0.0]}, 'k': {'ek': [-77.0], 'ki': [54.4], 'ko': [2.5], 'ik': [0.0], 'dik_dv_': [0.0]}},
          'morphology': {'L': 150.0, 'diam': [4.0], 'pts3d': [(0.0, 0.0, 2.0, 4.0), (0.0, 0.0, 152.0, 4.0)], 'parent': <cells.Bask23 object at 0x7f83344ffc18>.soma(0), 'trueparent': None}, 'nseg': 1, 'Ra': 100.0, 'cm': [1.0], 'regions': set(), 'species': set(), 'name': '<cells.Bask23 object at 0x7f83344ffc18>.axon', 'hoc_internal_name': '__nrnsec_0x55a88e284920', 'cell': <cells.Bask23 object at 0x7f83344ffc18>}

        '''
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


        self.dendV = h.Vector()
        self.dendV.record(self.dend(0.5)._ref_v)
        self.axonV = h.Vector()
        self.axonV.record(self.axon(0.5)._ref_v)
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
        #------for test-----------
        #self.stim = h.IClamp(self.soma(0.5))
        #self.stim.delay = 50
        #self.stim.dur = 1
        #self.stim.amp = 1
        print(self.id)
        #print(self.axon.psection())

class Axax23: #
    def __init__(self, x, y, z):
        self.id = 2
        self.x = x
        self.y = y
        self.z = z
        self.Excitatory = 1
        self.name = 'superficial interneurons axoaxonic'
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
        self.axon.pt3dadd(x, y, z - axonR, 2.0 * axonR)
        self.axon.pt3dadd(x, y, z - axonR - axonL, 2.0 * axonR)
        self.axon.connect(self.soma, 0, 0)

        self.all = [self.soma, self.dend]
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


        self.somaV = h.Vector()
        self.somaV.record(self.soma(0.5)._ref_v)

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
            cm = 0.9


        self.dendV = h.Vector()
        self.dendV.record(self.dend(0.5)._ref_v)
        self.axonV = h.Vector()
        self.axonV.record(self.axon(0.5)._ref_v)
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
        #------for test-----------
        self.stim = h.IClamp(self.soma(0.5))
        self.stim.delay = 50
        self.stim.dur = 1
        self.stim.amp = 1
        print(self.id)


class LTS23:  #
    def __init__(self, x, y, z):
        self.id = 3
        self.x = x
        self.y = y
        self.z = z
        self.Excitatory = 1
        self.name = 'superficial interneurons low threshold spiking'
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
        self.axon.pt3dadd(x, y, z - axonR, 2.0 * axonR)
        self.axon.pt3dadd(x, y, z - axonR - axonL, 2.0 * axonR)
        self.axon.connect(self.soma, 0, 0)

        
        self.all = [self.soma, self.dend]
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


        self.somaV = h.Vector()
        self.somaV.record(self.soma(0.5)._ref_v)

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
            cm = 1


        self.dendV = h.Vector()
        self.dendV.record(self.dend(0.5)._ref_v)
        self.axonV = h.Vector()
        self.axonV.record(self.axon(0.5)._ref_v)
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
        #------for test-----------
        self.stim = h.IClamp(self.soma(0.5))
        self.stim.delay = 50
        self.stim.dur = 1
        self.stim.amp = 1
        print(self.id)

class Spinstel4:  #
    def __init__(self, x, y, z):
        self.id = 4
        self.x = x
        self.y = y
        self.z = z
        self.Excitatory = -1
        self.name = 'spiny stellate'
        self.soma = h.Section(name='soma', cell=self)
        self.soma.pt3dclear()
        self.soma.pt3dadd(x, y, z + somaR, 2.0 * somaR)
        self.soma.pt3dadd(x, y, z - somaR, 2.0 * somaR)

        self.dend = h.Section(name='dend', cell=self)
        self.dend.pt3dclear()
        self.dend.pt3dadd(x, y, z - somaR, 2.0 * dendR)
        self.dend.pt3dadd(x, y, z - somaR - dendL, 2.0 * dendR)
        self.dend.nseg = 10

        self.axon = h.Section(name='axon', cell=self)
        self.axon.pt3dclear()
        self.axon.pt3dadd(x, y, z - axonR, 2.0 * axonR)
        self.axon.pt3dadd(x, y, z - axonR - axonL, 2.0 * axonR)
        self.axon.connect(self.soma, 0, 0)

        self.dend.connect(self.soma, 1, 0)
        self.all = [self.soma, self.dend]
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


        self.somaV = h.Vector()
        self.somaV.record(self.soma(0.5)._ref_v)

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
            cm = 0.9

        self.dendV = h.Vector()
        self.dendV.record(self.dend(0.5)._ref_v)
        self.axonV = h.Vector()
        self.axonV.record(self.axon(0.5)._ref_v)
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
        #------for test-----------
        self.stim = h.IClamp(self.soma(0.5))
        self.stim.delay = 50
        self.stim.dur = 1
        self.stim.amp = 1
        print(self.id)

class TuftIB5:  #
    def __init__(self, x, y, z):
        self.id = 5
        self.x = x
        self.y = y
        self.z = z
        self.Excitatory = -1
        self.name = 'pyramidal tufted intrinsic bursting'
        self.soma = h.Section(name='soma', cell=self)
        self.soma.pt3dclear()
        self.soma.pt3dadd(x, y, z + somaR, 2.0 * somaR)
        self.soma.pt3dadd(x, y, z - somaR, 2.0 * somaR)

        self.dend = h.Section(name='dend', cell=self)
        self.dend.pt3dclear()
        self.dend.pt3dadd(x, y, z - somaR, 2.0 * dendR)
        self.dend.pt3dadd(x, y, z - somaR - dendL, 2.0 * dendR)
        self.dend.nseg = 10

        self.axon = h.Section(name='axon', cell=self)
        self.axon.pt3dclear()
        self.axon.pt3dadd(x, y, z - axonR, 2.0 * axonR)
        self.axon.pt3dadd(x, y, z - axonR - axonL, 2.0 * axonR)
        self.axon.connect(self.soma, 0, 0)

        self.dend.connect(self.soma, 1, 0)
        self.all = [self.soma, self.dend]
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
        self.soma(0.5).cad.beta  = 0.01
        self.soma(0.5).cad.phi =  4333.33333
        self.soma(0.5).pas.g = 2.E-05
        self.soma(0.5).pas.e = -70
        self.soma.Ra =   250.


        self.somaV = h.Vector()
        self.somaV.record(self.soma(0.5)._ref_v)

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
            cm = 0.9

        self.dendV = h.Vector()
        self.dendV.record(self.dend(0.5)._ref_v)
        self.axonV = h.Vector()
        self.axonV.record(self.axon(0.5)._ref_v)
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
        #------for test-----------
        self.stim = h.IClamp(self.soma(0.5))
        self.stim.delay = 50
        self.stim.dur = 1
        self.stim.amp = 1
        print(self.id)

class TuftRS5:  #
    def __init__(self, x, y, z):
        self.id = 6
        self.x = x
        self.y = y
        self.z = z
        self.Excitatory = -1
        self.name = 'pyramidal tufted regular spiking'
        self.soma = h.Section(name='soma', cell=self)
        self.soma.pt3dclear()
        self.soma.pt3dadd(x, y, z + somaR, 2.0 * somaR)
        self.soma.pt3dadd(x, y, z - somaR, 2.0 * somaR)

        self.dend = h.Section(name='dend', cell=self)
        self.dend.pt3dclear()
        self.dend.pt3dadd(x, y, z - somaR, 2.0 * dendR)
        self.dend.pt3dadd(x, y, z - somaR - dendL, 2.0 * dendR)
        self.dend.nseg = 10

        self.axon = h.Section(name='axon', cell=self)
        self.axon.pt3dclear()
        self.axon.pt3dadd(x, y, z - axonR, 2.0 * axonR)
        self.axon.pt3dadd(x, y, z - axonR - axonL, 2.0 * axonR)
        self.axon.connect(self.soma, 0, 0)

        self.dend.connect(self.soma, 1, 0)
        self.all = [self.soma, self.dend]
        # ---------------soma----------------
        for mechanism_s in ['extracellular', 'naf', 'nap', 'kdr', 'kc', 'ka', 'km', 'kahp_deeppyr', 'k2', 'cal', 'cat', 'ar', 'cad']:
            self.soma.insert(mechanism_s)
            print(mechanism_s)

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


        self.somaV = h.Vector()
        self.somaV.record(self.soma(0.5)._ref_v)

        # ---------------dend----------------
        for mechanism_d in ['naf', 'nap', 'kdr', 'kc', 'ka', 'km', 'kahp_deeppyr', 'k2', 'cal', 'cat', 'ar', 'cad']:
            self.dend.insert(mechanism_d)
            print(mechanism_d)

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

        # ---------------axon----------------
        for mechanism_a in ['naf', 'kdr', 'ka', 'k2', 'km']:
            self.axon.insert(mechanism_a)
            print(mechanism_a)

        self.axon(0.5).naf.gbar = 0.45
        self.axon(0.5).kdr.gbar = 0.45
        self.axon(0.5).ka.gbar = 0.0006
        self.axon(0.5).k2.gbar = 0.0005
        self.axon(0.5).km.gbar = 0.03

        self.dendV = h.Vector()
        self.dendV.record(self.dend(0.5)._ref_v)
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
        #------for test-----------
        self.stim = h.IClamp(self.soma(0.5))
        self.stim.delay = 50
        self.stim.dur = 1
        self.stim.amp = 1
        print(self.id)


class Bask56:  #
    def __init__(self, x, y, z):
        self.id = 7
        self.x = x
        self.y = y
        self.z = z
        self.Excitatory = 1
        self.name = 'deep interneurons basket'
        self.soma = h.Section(name='soma', cell=self)
        self.soma.pt3dclear()
        self.soma.pt3dadd(x, y, z + somaR, 2.0 * somaR)
        self.soma.pt3dadd(x, y, z - somaR, 2.0 * somaR)

        self.dend = h.Section(name='dend', cell=self)
        self.dend.pt3dclear()
        self.dend.pt3dadd(x, y, z - somaR, 2.0 * dendR)
        self.dend.pt3dadd(x, y, z - somaR - dendL, 2.0 * dendR)
        self.dend.nseg = 10

        self.axon = h.Section(name='axon', cell=self)
        self.axon.pt3dclear()
        self.axon.pt3dadd(x, y, z - axonR, 2.0 * axonR)
        self.axon.pt3dadd(x, y, z - axonR - axonL, 2.0 * axonR)
        self.axon.connect(self.soma, 0, 0)

        self.dend.connect(self.soma, 1, 0)
        self.all = [self.soma, self.dend]
        # ---------------soma----------------
        for mechanism_s in ['extracellular','naf2', 'nap', 'kdr_fs', 'kc_fast', 'ka', 'km', 'k2', 'kahp_slower', 'cal', 'cat', 'ar', 'cad']:
            self.soma.insert(mechanism_s)
            print(mechanism_s)

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


        self.somaV = h.Vector()
        self.somaV.record(self.soma(0.5)._ref_v)

        # ---------------dend----------------
        for mechanism_d in ['naf2', 'nap', 'kdr_fs', 'kc_fast', 'ka', 'km', 'k2', 'kahp_slower', 'cal', 'cat', 'ar', 'cad']:
            self.dend.insert(mechanism_d)
            print(mechanism_d)

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
        self.dend(0.5).cad.beta  =   0.05
        self.dend(0.5).cad.phi =   520000.

        # ---------------axon----------------
        for mechanism_a in ['naf2', 'kdr_fs', 'ka', 'k2']:
            self.axon.insert(mechanism_a)
            print(mechanism_a)

        self.axon(0.5).naf2.gbar = 0.4
        self.axon(0.5).kdr_fs.gbar = 0.4
        self.axon(0.5).ka.gbar = 0.001
        self.axon(0.5).k2.gbar = 0.0005

        self.dendV = h.Vector()
        self.dendV.record(self.dend(0.5)._ref_v)
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
        #------for test-----------
        self.stim = h.IClamp(self.soma(0.5))
        self.stim.delay = 50
        self.stim.dur = 1
        self.stim.amp = 1
        print(self.id)


class Axax56:  #
    def __init__(self, x, y, z):
        self.id = 8
        self.x = x
        self.y = y
        self.z = z
        self.Excitatory = 1
        self.name = 'deep interneurons axoaxonic'
        self.soma = h.Section(name='soma', cell=self)
        self.soma.pt3dclear()
        self.soma.pt3dadd(x, y, z + somaR, 2.0 * somaR)
        self.soma.pt3dadd(x, y, z - somaR, 2.0 * somaR)

        self.dend = h.Section(name='dend', cell=self)
        self.dend.pt3dclear()
        self.dend.pt3dadd(x, y, z - somaR, 2.0 * dendR)
        self.dend.pt3dadd(x, y, z - somaR - dendL, 2.0 * dendR)
        self.dend.nseg = 10

        self.axon = h.Section(name='axon', cell=self)
        self.axon.pt3dclear()
        self.axon.pt3dadd(x, y, z - axonR, 2.0 * axonR)
        self.axon.pt3dadd(x, y, z - axonR - axonL, 2.0 * axonR)
        self.axon.connect(self.soma, 0, 0)

        self.dend.connect(self.soma, 1, 0)
        self.all = [self.soma, self.dend]
        # ---------------soma----------------
        for mechanism_s in ['extracellular','naf2', 'nap', 'kdr_fs', 'kc_fast', 'ka', 'km', 'k2', 'kahp_slower', 'cal', 'cat', 'ar', 'cad']:
            self.soma.insert(mechanism_s)
            print(mechanism_s)

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


        self.somaV = h.Vector()
        self.somaV.record(self.soma(0.5)._ref_v)

        # ---------------dend----------------
        for mechanism_d in ['naf2', 'nap', 'kdr_fs', 'kc_fast', 'ka', 'km', 'k2', 'kahp_slower', 'cal', 'cat', 'ar', 'cad']:
            self.dend.insert(mechanism_d)
            print(mechanism_d)

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
        self.dend(0.5).cad.beta  =   0.05
        self.dend(0.5).cad.phi =   520000.

        # ---------------axon----------------
        for mechanism_a in ['naf2', 'kdr_fs', 'ka', 'k2']:
            self.axon.insert(mechanism_a)
            print(mechanism_a)

        self.axon(0.5).naf2.gbar = 0.4
        self.axon(0.5).kdr_fs.gbar = 0.4
        self.axon(0.5).ka.gbar = 0.001
        self.axon(0.5).k2.gbar = 0.0005

        self.dendV = h.Vector()
        self.dendV.record(self.dend(0.5)._ref_v)
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
        #------for test-----------
        self.stim = h.IClamp(self.soma(0.5))
        self.stim.delay = 50
        self.stim.dur = 1
        self.stim.amp = 1
        print(self.id)


class LTS56:  #
    def __init__(self, x, y, z):
        self.id = 9
        self.x = x
        self.y = y
        self.z = z
        self.Excitatory = 1
        self.name ='deep interneurons low threshold spiking'
        self.soma = h.Section(name='soma', cell=self)
        self.soma.pt3dclear()
        self.soma.pt3dadd(x, y, z + somaR, 2.0 * somaR)
        self.soma.pt3dadd(x, y, z - somaR, 2.0 * somaR)

        self.dend = h.Section(name='dend', cell=self)
        self.dend.pt3dclear()
        self.dend.pt3dadd(x, y, z - somaR, 2.0 * dendR)
        self.dend.pt3dadd(x, y, z - somaR - dendL, 2.0 * dendR)
        self.dend.nseg = 10

        self.axon = h.Section(name='axon', cell=self)
        self.axon.pt3dclear()
        self.axon.pt3dadd(x, y, z - axonR, 2.0 * axonR)
        self.axon.pt3dadd(x, y, z - axonR - axonL, 2.0 * axonR)
        self.axon.connect(self.soma, 0, 0)

        self.dend.connect(self.soma, 1, 0)
        self.all = [self.soma, self.dend]
        # ---------------soma----------------
        for mechanism_s in ['extracellular','naf2', 'nap', 'kdr_fs', 'kc_fast', 'ka', 'km', 'k2', 'kahp_slower', 'cal', 'cat', 'ar', 'cad']:
            self.soma.insert(mechanism_s)
            print(mechanism_s)

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


        self.somaV = h.Vector()
        self.somaV.record(self.soma(0.5)._ref_v)

        # ---------------dend----------------
        for mechanism_d in ['naf2', 'nap', 'kdr_fs', 'kc_fast', 'ka', 'km', 'k2', 'kahp_slower', 'cal', 'cat', 'ar', 'cad']:
            self.dend.insert(mechanism_d)
            print(mechanism_d)

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
        self.dend(0.5).cad.beta  =   0.05
        self.dend(0.5).cad.phi =   520000.

        # ---------------axon----------------
        for mechanism_a in ['naf2', 'kdr_fs', 'ka', 'k2']:
            self.axon.insert(mechanism_a)
            print(mechanism_a)

        self.axon(0.5).naf2.gbar = 0.4
        self.axon(0.5).kdr_fs.gbar = 0.4
        self.axon(0.5).ka.gbar = 0.001
        self.axon(0.5).k2.gbar = 0.0005

        self.dendV = h.Vector()
        self.dendV.record(self.dend(0.5)._ref_v)
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
        #------for test-----------
        self.stim = h.IClamp(self.soma(0.5))
        self.stim.delay = 50
        self.stim.dur = 1
        self.stim.amp = 1
        print(self.id)


class NontuftRS6:  #
    def __init__(self, x, y, z):
        self.id = 10
        self.x = x
        self.y = y
        self.z = z
        self.Excitatory = -1
        self.name ='pyramidal nontufted regular spiking'
        self.soma = h.Section(name='soma', cell=self)
        self.soma.pt3dclear()
        self.soma.pt3dadd(x, y, z + somaR, 2.0 * somaR)
        self.soma.pt3dadd(x, y, z - somaR, 2.0 * somaR)

        self.dend = h.Section(name='dend', cell=self)
        self.dend.pt3dclear()
        self.dend.pt3dadd(x, y, z - somaR, 2.0 * dendR)
        self.dend.pt3dadd(x, y, z - somaR - dendL, 2.0 * dendR)
        self.dend.nseg = 10

        self.axon = h.Section(name='axon', cell=self)
        self.axon.pt3dclear()
        self.axon.pt3dadd(x, y, z - axonR, 2.0 * axonR)
        self.axon.pt3dadd(x, y, z - axonR - axonL, 2.0 * axonR)
        self.axon.connect(self.soma, 0, 0)

        self.dend.connect(self.soma, 1, 0)
        self.all = [self.soma, self.dend]
        # ---------------soma----------------
        for mechanism_s in ['extracellular','napf', 'naf2', 'kdr_fs', 'kc', 'ka', 'km', 'k2', 'kahp_slower', 'cal', 'cat_a', 'ar', 'cad']:
            self.soma.insert(mechanism_s)
            print(mechanism_s)

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


        self.somaV = h.Vector()
        self.somaV.record(self.soma(0.5)._ref_v)

        # ---------------dend----------------
        for mechanism_d in ['naf2', 'napf', 'kdr_fs', 'kc', 'ka', 'km', 'k2', 'kahp_slower', 'cal', 'cat_a', 'ar', 'cad']:
            self.dend.insert(mechanism_d)
            print(mechanism_d)

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

        # ---------------axon----------------
        for mechanism_a in ['naf2', 'kdr_fs', 'ka', 'k2']:
            self.axon.insert(mechanism_a)
            print(mechanism_a)

        self.axon(0.5).naf2.gbar = 0.4
        self.axon(0.5).kdr_fs.gbar = 0.4
        self.axon(0.5).ka.gbar = 0.001
        self.axon(0.5).k2.gbar = 0.0005

        self.dendV = h.Vector()
        self.dendV.record(self.dend(0.5)._ref_v)
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
        #------for test-----------
        self.stim = h.IClamp(self.soma(0.5))
        self.stim.delay = 50
        self.stim.dur = 1
        self.stim.amp = 1
        print(self.id)

