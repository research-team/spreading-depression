from neuron import h, crxd as rxd

somaR = 11.0  # soma radius
dendR = 1.4  # dendrite radius
dendL = 100.0  # dendrite length
doff = dendL + somaR

class Bask23:
    def __init__(self, x, y, z):
        self.id = 1
        self.x = x
        self.y = y
        self.z = z
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
        for mechanism_s in ['extracellular','Nasoma', 'Ksoma']:
            self.soma.insert(mechanism_s)

        self.somaV = h.Vector()
        self.somaV.record(self.soma(0.5)._ref_v)

        # ---------------dend----------------
        for mechanism_d in ['Nadend', 'Kdend']:
            self.dend.insert(mechanism_d)

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

class Axax23: #
    def __init__(self, x, y, z):
        self.id = 2
        self.x = x
        self.y = y
        self.z = z
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
        #---------------soma----------------
        for mechanism_s in ['extracellular','Nasoma', 'Ksoma']:
            self.soma.insert(mechanism_s)

        self.somaV = h.Vector()
        self.somaV.record(self.soma(0.5)._ref_v)
        
        #---------------dend----------------
        for mechanism_d in [ 'Nadend', 'Kdend']:
            self.dend.insert(mechanism_d)
        
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
        #self.stim = h.IClamp(self.soma(0.5))
        #self.stim.delay = 50
        #self.stim.dur = 1
        #self.stim.amp = 1


class LTS23:  #
    def __init__(self, x, y, z):
        self.id = 3
        self.x = x
        self.y = y
        self.z = z
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
        for mechanism_s in ['extracellular','Nasoma', 'Ksoma']:
            self.soma.insert(mechanism_s)

        self.somaV = h.Vector()
        self.somaV.record(self.soma(0.5)._ref_v)

        # ---------------dend----------------
        for mechanism_d in ['Nadend', 'Kdend']:
            self.dend.insert(mechanism_d)

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
        # self.stim = h.IClamp(self.soma(0.5))
        # self.stim.delay = 50
        # self.stim.dur = 1
        # self.stim.amp = 1

class Spinstel4:  #
    def __init__(self, x, y, z):
        self.id = 4
        self.x = x
        self.y = y
        self.z = z
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
        for mechanism_s in ['extracellular','Nasoma', 'Ksoma']:
            self.soma.insert(mechanism_s)

        self.somaV = h.Vector()
        self.somaV.record(self.soma(0.5)._ref_v)

        # ---------------dend----------------
        for mechanism_d in ['Nadend', 'Kdend']:
            self.dend.insert(mechanism_d)

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
        # self.stim = h.IClamp(self.soma(0.5))
        # self.stim.delay = 50
        # self.stim.dur = 1
        # self.stim.amp = 1

class TuftIB5:  #
    def __init__(self, x, y, z):
        self.id = 5
        self.x = x
        self.y = y
        self.z = z
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
        for mechanism_s in ['extracellular','Nasoma', 'Ksoma']:
            self.soma.insert(mechanism_s)

        self.somaV = h.Vector()
        self.somaV.record(self.soma(0.5)._ref_v)

        # ---------------dend----------------
        for mechanism_d in ['Nadend', 'Kdend']:
            self.dend.insert(mechanism_d)

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
        # self.stim = h.IClamp(self.soma(0.5))
        # self.stim.delay = 50
        # self.stim.dur = 1
        # self.stim.amp = 1

class TuftRS5:  #
    def __init__(self, x, y, z):
        self.id = 6
        self.x = x
        self.y = y
        self.z = z
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
        for mechanism_s in ['extracellular','Nasoma', 'Ksoma']:
            self.soma.insert(mechanism_s)

        self.somaV = h.Vector()
        self.somaV.record(self.soma(0.5)._ref_v)

        # ---------------dend----------------
        for mechanism_d in ['Nadend', 'Kdend']:
            self.dend.insert(mechanism_d)

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
        # self.stim = h.IClamp(self.soma(0.5))
        # self.stim.delay = 50
        # self.stim.dur = 1
        # self.stim.amp = 1


class Bask56:  #
    def __init__(self, x, y, z):
        self.id = 7
        self.x = x
        self.y = y
        self.z = z
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
        for mechanism_s in ['extracellular','Nasoma', 'Ksoma']:
            self.soma.insert(mechanism_s)

        self.somaV = h.Vector()
        self.somaV.record(self.soma(0.5)._ref_v)

        # ---------------dend----------------
        for mechanism_d in ['Nadend', 'Kdend']:
            self.dend.insert(mechanism_d)

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
        # self.stim = h.IClamp(self.soma(0.5))
        # self.stim.delay = 50
        # self.stim.dur = 1
        # self.stim.amp = 1


class Axax56:  #
    def __init__(self, x, y, z):
        self.id = 8
        self.x = x
        self.y = y
        self.z = z
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
        for mechanism_s in ['extracellular','Nasoma', 'Ksoma']:
            self.soma.insert(mechanism_s)

        self.somaV = h.Vector()
        self.somaV.record(self.soma(0.5)._ref_v)

        # ---------------dend----------------
        for mechanism_d in ['Nadend', 'Kdend']:
            self.dend.insert(mechanism_d)

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
        # self.stim = h.IClamp(self.soma(0.5))
        # self.stim.delay = 50
        # self.stim.dur = 1
        # self.stim.amp = 1


class LTS56:  #
    def __init__(self, x, y, z):
        self.id = 9
        self.x = x
        self.y = y
        self.z = z
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
        for mechanism_s in ['extracellular','Nasoma', 'Ksoma']:
            self.soma.insert(mechanism_s)

        self.somaV = h.Vector()
        self.somaV.record(self.soma(0.5)._ref_v)

        # ---------------dend----------------
        for mechanism_d in ['Nadend', 'Kdend']:
            self.dend.insert(mechanism_d)

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
        # self.stim = h.IClamp(self.soma(0.5))
        # self.stim.delay = 50
        # self.stim.dur = 1
        # self.stim.amp = 1


class NontuftRS6:  #
    def __init__(self, x, y, z):
        self.id = 10
        self.x = x
        self.y = y
        self.z = z
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
        for mechanism_s in ['extracellular','Nasoma', 'Ksoma']:
            self.soma.insert(mechanism_s)

        self.somaV = h.Vector()
        self.somaV.record(self.soma(0.5)._ref_v)

        # ---------------dend----------------
        for mechanism_d in ['Nadend', 'Kdend']:
            self.dend.insert(mechanism_d)

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
        # self.stim = h.IClamp(self.soma(0.5))
        # self.stim.delay = 50
        # self.stim.dur = 1
        # self.stim.amp = 1

