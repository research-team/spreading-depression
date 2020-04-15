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


        #h.topology()

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

