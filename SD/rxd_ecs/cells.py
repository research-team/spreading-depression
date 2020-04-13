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
        self.axon.pt3dadd(x, y, z - axonR, 2.0 * axonR)
        self.axon.pt3dadd(x, y, z - axonR - axonL, 2.0 * axonR)
        self.axon.connect(self.soma, 0, 0)

        self.all = [self.soma, self.dend]
        # ---------------soma----------------
        for mechanism_s in ['extracellular','naf2', 'nap', 'kdr_fs', 'kc_fast', 'ka', 'km', 'k2', 'kahp_slower', 'cal', 'cat', 'ar', 'cad']:
            self.soma.insert(mechanism_s)
            print(mechanism_s)

        self.soma.naf2.gbar = 0.06
        self.soma.nap.gbar = 0.0006
        self.soma.kdr_fs.gbar = 0.1
        self.soma.kc_fast.gbar = 0.025
        self.soma.ka.gbar = 0.001
        self.soma.km.gbar = 0.0005
        self.soma.k2.gbar = 0.0005
        self.soma.kahp_slower.gbar = 0.0001
        self.soma.cal.gbar = 0.0001
        self.soma.cat.gbar = 5.E-05
        self.soma.ar.gbar = 2.5E-05
        self.soma.cad.beta  = 0.02
        self.soma.cad.phi =  260000.


        self.somaV = h.Vector()
        self.somaV.record(self.soma(0.5)._ref_v)

        # ---------------dend----------------
        for mechanism_d in ['naf2', 'nap', 'kdr_fs', 'kc_fast', 'ka', 'km', 'k2', 'kahp_slower', 'cal', 'cat', 'ar', 'cad']:
            self.dend.insert(mechanism_d)
            print(mechanism_d)

        self.dend.naf2.gbar =   0.01
        self.dend.nap.gbar =   0.0001
        self.dend.kdr_fs.gbar =   0.01 
        self.dend.kc_fast.gbar =   0.025
        self.dend.ka.gbar =   0.001
        self.dend.km.gbar =   0.0005
        self.dend.k2.gbar =   0.0005
        self.dend.kahp_slower.gbar =   0.0001
        self.dend.cal.gbar =   0.0002
        self.dend.cat.gbar =   0.002
        self.dend.ar.gbar =   2.5E-05
        self.dend.cad.beta  =   0.05
        self.dend.cad.phi =   520000.

        # ---------------axon----------------
        for mechanism_a in ['naf2', 'kdr_fs', 'ka', 'k2']:
            self.axon.insert(mechanism_a)
            print(mechanism_a)

        self.axon.naf2.gbar = 0.4
        self.axon.kdr_fs.gbar = 0.4
        self.axon.ka.gbar = 0.001
        self.axon.k2.gbar = 0.0005

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
        for mechanism_s in ['extracellular','naf2', 'nap', 'kdr_fs', 'kc_fast', 'ka', 'km', 'k2', 'kahp_slower', 'cal', 'cat', 'ar', 'cad']:
            self.soma.insert(mechanism_s)
            print(mechanism_s)

        self.soma.naf2.gbar = 0.06
        self.soma.nap.gbar = 0.0006
        self.soma.kdr_fs.gbar = 0.1
        self.soma.kc_fast.gbar = 0.025
        self.soma.ka.gbar = 0.001
        self.soma.km.gbar = 0.0005
        self.soma.k2.gbar = 0.0005
        self.soma.kahp_slower.gbar = 0.0001
        self.soma.cal.gbar = 0.0001
        self.soma.cat.gbar = 5.E-05
        self.soma.ar.gbar = 2.5E-05
        self.soma.cad.beta  = 0.02
        self.soma.cad.phi =  260000.


        self.somaV = h.Vector()
        self.somaV.record(self.soma(0.5)._ref_v)

        # ---------------dend----------------
        for mechanism_d in ['naf2', 'nap', 'kdr_fs', 'kc_fast', 'ka', 'km', 'k2', 'kahp_slower', 'cal', 'cat', 'ar', 'cad']:
            self.dend.insert(mechanism_d)
            print(mechanism_d)

        self.dend.naf2.gbar =   0.06
        self.dend.nap.gbar =   0.0006
        self.dend.kdr_fs.gbar =   0.01 
        self.dend.kc_fast.gbar =   0.025
        self.dend.ka.gbar =   0.001
        self.dend.km.gbar =   0.0005
        self.dend.k2.gbar =   0.0005
        self.dend.kahp_slower.gbar =   0.0001
        self.dend.cal.gbar =   0.0001
        self.dend.cat.gbar =   5.E-05
        self.dend.ar.gbar =   2.5E-05
        self.dend.cad.beta  =   0.05
        self.dend.cad.phi =   520000.

        # ---------------axon----------------
        for mechanism_a in ['naf2', 'kdr_fs', 'ka', 'k2']:
            self.axon.insert(mechanism_a)
            print(mechanism_a)

        self.axon.naf2.gbar = 0.4
        self.axon.kdr_fs.gbar = 0.4
        self.axon.ka.gbar = 0.001
        self.axon.k2.gbar = 0.0005
        
        self.dendV = h.Vector()
        self.dendV.record(self.dend(0.5)._ref_v)
        self.k_vec = h.Vector().record(self.dend(0.5)._ref_ik)
        self.na_vec = h.Vector().record(self.dend(0.5)._ref_ina)
        self.na_concentration = h.Vector().record(self.dend(0.5)._ref_nai)
        self.k_concentration = h.Vector().record(self.dend(0.5)._ref_ki)      
        self.v_vec = h.Vector().record(self.soma(0.5)._ref_vext[0])
        self.cyt = rxd.Region(self.all, name='cyt', nrn_region='i', dx=1.0, geometry=rxd.FractionalVolume(0.9, surface_fraction=1.0))
        self.na = rxd.Species([self.cyt], name='na', charge=1, d=1.0, initial=10)
        self.k = rxd.Species([self.cyt], name='k', charge=1, d=1.0, initial=148)
        self.k_i= self.k[self.cyt]
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
        for mechanism_s in ['extracellular','naf2', 'nap', 'kdr_fs', 'kc_fast', 'ka', 'km', 'k2', 'kahp_slower', 'cal', 'cat', 'ar', 'cad']:
            self.soma.insert(mechanism_s)
            print(mechanism_s)

        self.soma.naf2.gbar = 0.06
        self.soma.nap.gbar = 0.0006
        self.soma.kdr_fs.gbar = 0.1
        self.soma.kc_fast.gbar = 0.025
        self.soma.ka.gbar = 0.001
        self.soma.km.gbar = 0.0005
        self.soma.k2.gbar = 0.0005
        self.soma.kahp_slower.gbar = 0.0001
        self.soma.cal.gbar = 0.0001
        self.soma.cat.gbar = 5.E-05
        self.soma.ar.gbar = 2.5E-05
        self.soma.cad.beta  = 0.02
        self.soma.cad.phi =  260000.


        self.somaV = h.Vector()
        self.somaV.record(self.soma(0.5)._ref_v)

        # ---------------dend----------------
        for mechanism_d in ['naf2', 'nap', 'kdr_fs', 'kc_fast', 'ka', 'km', 'k2', 'kahp_slower', 'cal', 'cat', 'ar', 'cad']:
            self.dend.insert(mechanism_d)
            print(mechanism_d)

        self.dend.naf2.gbar =   0.06
        self.dend.nap.gbar =   0.0006
        self.dend.kdr_fs.gbar =   0.01 
        self.dend.kc_fast.gbar =   0.025
        self.dend.ka.gbar =   0.001
        self.dend.km.gbar =   0.0005
        self.dend.k2.gbar =   0.0005
        self.dend.kahp_slower.gbar =   0.0001
        self.dend.cal.gbar =   0.0001
        self.dend.cat.gbar =   5.E-05
        self.dend.ar.gbar =   2.5E-05
        self.dend.cad.beta  =   0.05
        self.dend.cad.phi =   520000.

        # ---------------axon----------------
        for mechanism_a in ['naf2', 'kdr_fs', 'ka', 'k2']:
            self.axon.insert(mechanism_a)
            print(mechanism_a)

        self.axon.naf2.gbar = 0.4
        self.axon.kdr_fs.gbar = 0.4
        self.axon.ka.gbar = 0.001
        self.axon.k2.gbar = 0.0005

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

        self.dend.connect(self.soma, 1, 0)
        self.all = [self.soma, self.dend]
        # ---------------soma----------------
        for mechanism_s in ['extracellular','naf2', 'napf_spinstell', 'kdr_fs', 'kc_fast', 'ka', 'km', 'k2', 'kahp_slower', 'cal', 'cat', 'ar', 'cad']:
            self.soma.insert(mechanism_s)
            print(mechanism_s)

        self.soma.naf2.gbar = 0.15
        self.soma.napf_spinstell.gbar = 0.00015
        self.soma.kdr_fs.gbar = 0.1
        self.soma.kc_fast.gbar = 0.01
        self.soma.ka.gbar = 0.03
        self.soma.km.gbar = 0.00375
        self.soma.k2.gbar = 0.0001
        self.soma.kahp_slower.gbar = 0.0001
        self.soma.cal.gbar = 0.0005
        self.soma.cat.gbar = 0.0001
        self.soma.ar.gbar = 0.00025
        self.soma.cad.beta  = 0.02
        self.soma.cad.phi =  260000.


        self.somaV = h.Vector()
        self.somaV.record(self.soma(0.5)._ref_v)

        # ---------------dend----------------
        for mechanism_d in ['naf2', 'napf_spinstell', 'kdr_fs', 'kc_fast', 'ka', 'km', 'k2', 'kahp_slower', 'cal', 'cat', 'ar', 'cad']:
            self.dend.insert(mechanism_d)
            print(mechanism_d)

        self.dend.naf2.gbar =   0.075
        self.dend.napf_spinstell.gbar = 7.5E-05
        self.dend.kdr_fs.gbar =   0.075
        self.dend.kc_fast.gbar =   0.01
        self.dend.ka.gbar =   0.03
        self.dend.km.gbar =   0.00375
        self.dend.k2.gbar =   0.0001
        self.dend.kahp_slower.gbar =   0.0001
        self.dend.cal.gbar =   0.0005
        self.dend.cat.gbar =   0.0001
        self.dend.ar.gbar =   0.00025
        self.dend.cad.beta  =   0.05
        self.dend.cad.phi =   260000.

        # ---------------axon----------------
        for mechanism_a in ['naf2', 'kdr_fs', 'ka', 'k2']:
            self.axon.insert(mechanism_a)
            print(mechanism_a)

        self.axon.naf2.gbar = 0.4
        self.axon.kdr_fs.gbar = 0.4
        self.axon.ka.gbar = 0.002
        self.axon.k2.gbar = 0.0001

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

        self.dend.connect(self.soma, 1, 0)
        self.all = [self.soma, self.dend]
        # ---------------soma----------------
        for mechanism_s in ['extracellular','naf', 'nap', 'kdr', 'kc', 'ka_ib', 'km', 'kahp_deeppyr', 'k2', 'cal', 'cat', 'ar', 'cad']:
            self.soma.insert(mechanism_s)
            print(mechanism_s)

        self.soma.naf.gbar = 0.2
        self.soma.nap.gbar = 0.0008
        self.soma.kdr.gbar = 0.17
        self.soma.kc.gbar = 0.008
        self.soma.ka_ib.gbar = 0.02
        self.soma.km.gbar = 0.0085
        self.soma.k2.gbar = 0.0005
        self.soma.kahp_deeppyr.gbar = 0.0002
        self.soma.cal.gbar = 0.0004
        self.soma.cat.gbar = 0.0001
        self.soma.ar.gbar = 0.0001
        self.soma.cad.beta  = 0.01
        self.soma.cad.phi =  4333.33333


        self.somaV = h.Vector()
        self.somaV.record(self.soma(0.5)._ref_v)

        # ---------------dend----------------
        for mechanism_d in ['naf', 'nap', 'kdr', 'kc', 'ka_ib', 'km', 'k2', 'kahp_deeppyr', 'cal', 'cat', 'ar', 'cad']:
            self.dend.insert(mechanism_d)
            print(mechanism_d)

        self.dend.naf.gbar =   0.075
        self.dend.nap.gbar = 0.0003
        self.dend.kdr.gbar =   0.075
        self.dend.kc.gbar =   0.008
        self.dend.ka_ib.gbar =   0.008
        self.dend.km.gbar =   0.00375
        self.dend.k2.gbar =   0.0005
        self.dend.kahp_deeppyr.gbar =   0.0002
        self.dend.cal.gbar =   0.0004
        self.dend.cat.gbar =   0.0001
        self.dend.ar.gbar =   0.0001
        self.dend.cad.beta  =   0.02
        self.dend.cad.phi =   86666.6667

        # ---------------axon----------------
        for mechanism_a in ['naf', 'kdr', 'ka_ib', 'km']:
            self.axon.insert(mechanism_a)
            print(mechanism_a)

        self.axon.naf.gbar = 0.45
        self.axon.kdr.gbar = 0.45
        self.axon.ka_ib.gbar = 0.0006
        self.axon.km.gbar = 0.03

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

        self.dend.connect(self.soma, 1, 0)
        self.all = [self.soma, self.dend]
        # ---------------soma----------------
        for mechanism_s in ['extracellular', 'naf', 'nap', 'kdr', 'kc', 'ka', 'km', 'kahp_deeppyr', 'k2', 'cal', 'cat', 'ar', 'cad']:
            self.soma.insert(mechanism_s)
            print(mechanism_s)

        self.dend.naf.gbar =   0.02
        self.dend.nap.gbar = 0.0008
        self.dend.kdr.gbar =   0.17
        self.dend.kc.gbar =   0.008
        self.dend.ka.gbar =   0.02
        self.dend.km.gbar =   0.0085
        self.dend.k2.gbar =   0.0005
        self.dend.kahp_deeppyr.gbar =   0.0002
        self.dend.cal.gbar =   0.0004
        self.dend.cat.gbar =   0.0001
        self.dend.ar.gbar =   0.0001
        self.dend.cad.beta  =   0.02
        self.dend.cad.phi =   4333.33333


        self.somaV = h.Vector()
        self.somaV.record(self.soma(0.5)._ref_v)

        # ---------------dend----------------
        for mechanism_d in ['naf', 'nap', 'kdr', 'kc', 'ka', 'km', 'kahp_deeppyr', 'k2', 'cal', 'cat', 'ar', 'cad']:
            self.dend.insert(mechanism_d)
            print(mechanism_d)

        self.dend.naf.gbar =   0.075
        self.dend.nap.gbar = 0.0003
        self.dend.kdr.gbar =   0.075
        self.dend.kc.gbar =   0.008
        self.dend.ka_ib.gbar =   0.008
        self.dend.km.gbar =   0.0136
        self.dend.k2.gbar =   0.0005
        self.dend.kahp_deeppyr.gbar =   0.0002
        self.dend.cal.gbar =   0.0004
        self.dend.cat.gbar =   0.0001
        self.dend.ar.gbar =   0.0001
        self.dend.cad.beta  =   0.02
        self.dend.cad.phi =   86666.6667

        # ---------------axon----------------
        for mechanism_a in ['naf', 'kdr', 'ka', 'k2', 'km']:
            self.axon.insert(mechanism_a)
            print(mechanism_a)

        self.axon.naf.gbar = 0.45
        self.axon.kdr.gbar = 0.45
        self.axon.ka.gbar = 0.0006
        self.axon.k2.gbar = 0.0005
        self.axon.km.gbar = 0.03 

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

        self.dend.connect(self.soma, 1, 0)
        self.all = [self.soma, self.dend]
        # ---------------soma----------------
        for mechanism_s in ['extracellular','naf2', 'nap', 'kdr_fs', 'kc_fast', 'ka', 'km', 'k2', 'kahp_slower', 'cal', 'cat', 'ar', 'cad']:
            self.soma.insert(mechanism_s)
            print(mechanism_s)

        self.soma.naf2.gbar = 0.06
        self.soma.nap.gbar = 0.0006
        self.soma.kdr_fs.gbar = 0.1
        self.soma.kc_fast.gbar = 0.025
        self.soma.ka.gbar = 0.001
        self.soma.km.gbar = 0.0005
        self.soma.k2.gbar = 0.0005
        self.soma.kahp_slower.gbar = 0.0001
        self.soma.cal.gbar = 0.0001
        self.soma.cat.gbar = 5.E-05
        self.soma.ar.gbar = 2.5E-05
        self.soma.cad.beta  = 0.02
        self.soma.cad.phi =  260000.


        self.somaV = h.Vector()
        self.somaV.record(self.soma(0.5)._ref_v)

        # ---------------dend----------------
        for mechanism_d in ['naf2', 'nap', 'kdr_fs', 'kc_fast', 'ka', 'km', 'k2', 'kahp_slower', 'cal', 'cat', 'ar', 'cad']:
            self.dend.insert(mechanism_d)
            print(mechanism_d)

        self.dend.naf2.gbar =   0.06
        self.dend.nap.gbar = 0.0006
        self.dend.kdr_fs.gbar =   0.1
        self.dend.kc_fast.gbar =   0.025
        self.dend.ka.gbar =   0.001
        self.dend.km.gbar =   0.0005
        self.dend.k2.gbar =   0.0005
        self.dend.kahp_slower.gbar =   0.0001
        self.dend.cal.gbar =   0.0001
        self.dend.cat.gbar =   5.E-05
        self.dend.ar.gbar =   2.5E-05
        self.dend.cad.beta  =   0.05
        self.dend.cad.phi =   520000.

        # ---------------axon----------------
        for mechanism_a in ['naf2', 'kdr_fs', 'ka', 'k2']:
            self.axon.insert(mechanism_a)
            print(mechanism_a)

        self.axon.naf2.gbar = 0.4
        self.axon.kdr_fs.gbar = 0.4
        self.axon.ka.gbar = 0.001
        self.axon.k2.gbar = 0.0005

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

        self.dend.connect(self.soma, 1, 0)
        self.all = [self.soma, self.dend]
        # ---------------soma----------------
        for mechanism_s in ['extracellular','naf2', 'nap', 'kdr_fs', 'kc_fast', 'ka', 'km', 'k2', 'kahp_slower', 'cal', 'cat', 'ar', 'cad']:
            self.soma.insert(mechanism_s)
            print(mechanism_s)

        self.soma.naf2.gbar = 0.06
        self.soma.nap.gbar = 0.0006
        self.soma.kdr_fs.gbar = 0.1
        self.soma.kc_fast.gbar = 0.025
        self.soma.ka.gbar = 0.001
        self.soma.km.gbar = 0.0005
        self.soma.k2.gbar = 0.0005
        self.soma.kahp_slower.gbar = 0.0001
        self.soma.cal.gbar = 0.0001
        self.soma.cat.gbar = 5.E-05
        self.soma.ar.gbar = 2.5E-05
        self.soma.cad.beta  = 0.02
        self.soma.cad.phi =  260000.


        self.somaV = h.Vector()
        self.somaV.record(self.soma(0.5)._ref_v)

        # ---------------dend----------------
        for mechanism_d in ['naf2', 'nap', 'kdr_fs', 'kc_fast', 'ka', 'km', 'k2', 'kahp_slower', 'cal', 'cat', 'ar', 'cad']:
            self.dend.insert(mechanism_d)
            print(mechanism_d)

        self.dend.naf2.gbar =   0.06
        self.dend.nap.gbar = 0.0006
        self.dend.kdr_fs.gbar =   0.1
        self.dend.kc_fast.gbar =   0.025
        self.dend.ka.gbar =   0.001
        self.dend.km.gbar =   0.0005
        self.dend.k2.gbar =   0.0005
        self.dend.kahp_slower.gbar =   0.0001
        self.dend.cal.gbar =   0.0001
        self.dend.cat.gbar =   5.E-05
        self.dend.ar.gbar =   2.5E-05
        self.dend.cad.beta  =   0.05
        self.dend.cad.phi =   520000.

        # ---------------axon----------------
        for mechanism_a in ['naf2', 'kdr_fs', 'ka', 'k2']:
            self.axon.insert(mechanism_a)
            print(mechanism_a)

        self.axon.naf2.gbar = 0.4
        self.axon.kdr_fs.gbar = 0.4
        self.axon.ka.gbar = 0.001
        self.axon.k2.gbar = 0.0005

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

        self.dend.connect(self.soma, 1, 0)
        self.all = [self.soma, self.dend]
        # ---------------soma----------------
        for mechanism_s in ['extracellular','naf2', 'nap', 'kdr_fs', 'kc_fast', 'ka', 'km', 'k2', 'kahp_slower', 'cal', 'cat', 'ar', 'cad']:
            self.soma.insert(mechanism_s)
            print(mechanism_s)

        self.soma.naf2.gbar = 0.06
        self.soma.nap.gbar = 0.0006
        self.soma.kdr_fs.gbar = 0.1
        self.soma.kc_fast.gbar = 0.025
        self.soma.ka.gbar = 0.001
        self.soma.km.gbar = 0.0005
        self.soma.k2.gbar = 0.0005
        self.soma.kahp_slower.gbar = 0.0001
        self.soma.cal.gbar = 0.0001
        self.soma.cat.gbar = 5.E-05
        self.soma.ar.gbar = 2.5E-05
        self.soma.cad.beta  = 0.02
        self.soma.cad.phi =  260000.


        self.somaV = h.Vector()
        self.somaV.record(self.soma(0.5)._ref_v)

        # ---------------dend----------------
        for mechanism_d in ['naf2', 'nap', 'kdr_fs', 'kc_fast', 'ka', 'km', 'k2', 'kahp_slower', 'cal', 'cat', 'ar', 'cad']:
            self.dend.insert(mechanism_d)
            print(mechanism_d)

        self.dend.naf2.gbar =   0.06
        self.dend.nap.gbar = 0.0006
        self.dend.kdr_fs.gbar =   0.1
        self.dend.kc_fast.gbar =   0.025
        self.dend.ka.gbar =   0.001
        self.dend.km.gbar =   0.0005
        self.dend.k2.gbar =   0.0005
        self.dend.kahp_slower.gbar =   0.0001
        self.dend.cal.gbar =   0.0001
        self.dend.cat.gbar =   5.E-05
        self.dend.ar.gbar =   2.5E-05
        self.dend.cad.beta  =   0.05
        self.dend.cad.phi =   520000.

        # ---------------axon----------------
        for mechanism_a in ['naf2', 'kdr_fs', 'ka', 'k2']:
            self.axon.insert(mechanism_a)
            print(mechanism_a)

        self.axon.naf2.gbar = 0.4
        self.axon.kdr_fs.gbar = 0.4
        self.axon.ka.gbar = 0.001
        self.axon.k2.gbar = 0.0005

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

        self.dend.connect(self.soma, 1, 0)
        self.all = [self.soma, self.dend]
        # ---------------soma----------------
        for mechanism_s in ['extracellular','napf', 'naf2', 'kdr_fs', 'kc', 'ka', 'km', 'k2', 'kahp_slower', 'cal', 'cat_a', 'ar', 'cad']:
            self.soma.insert(mechanism_s)
            print(mechanism_s)

        self.soma.naf2.gbar = 0.06
        self.soma.napf.gbar = 0.0006
        self.soma.kdr_fs.gbar = 0.06
        self.soma.ka.gbar = 0.005
        self.soma.km.gbar = 0.0005
        self.soma.kc.gbar = 0.01
        self.soma.k2.gbar = 0.0005
        self.soma.kahp_slower.gbar = 0.0001
        self.soma.cal.gbar = 0.0001
        self.soma.cat_a.gbar = 5.E-05
        self.soma.ar.gbar = 2.5E-05
        self.soma.cad.beta  = 0.02
        self.soma.cad.phi =  10400.


        self.somaV = h.Vector()
        self.somaV.record(self.soma(0.5)._ref_v)

        # ---------------dend----------------
        for mechanism_d in ['naf2', 'napf', 'kdr_fs', 'kc', 'ka', 'km', 'k2', 'kahp_slower', 'cal', 'cat_a', 'ar', 'cad']:
            self.dend.insert(mechanism_d)
            print(mechanism_d)

        self.dend.naf2.gbar =   0.06
        self.dend.napf.gbar = 0.0006
        self.dend.kdr_fs.gbar =   0.06
        self.dend.kc.gbar =   0.01
        self.dend.ka.gbar =   0.005
        self.dend.km.gbar =   0.0005
        self.dend.k2.gbar =   0.0005
        self.dend.kahp_slower.gbar =   0.0001
        self.dend.cal.gbar =   0.0005
        self.dend.cat.gbar =   5.E-05
        self.dend.ar.gbar =   2.5E-05
        self.dend.cad.beta  =   0.05
        self.dend.cad.phi =   260000.

        # ---------------axon----------------
        for mechanism_a in ['naf2', 'kdr_fs', 'ka', 'k2']:
            self.axon.insert(mechanism_a)
            print(mechanism_a)

        self.axon.naf2.gbar = 0.4
        self.axon.kdr_fs.gbar = 0.4
        self.axon.ka.gbar = 0.001
        self.axon.k2.gbar = 0.0005

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

