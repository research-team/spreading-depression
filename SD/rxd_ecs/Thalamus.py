from neuron import h
h.load_file('batch_.hoc')
class thalamus_cell:
    def __init__(self, x, y, z,num):
        self.x = x
        self.y = y
        self.z = z
        self.Excitatory = 0
        self.all = h.SectionList()

        self.soma = h.Section(name='soma', cell=self)
        self.all.append(sec=self.soma)

        self.dend = h.Section(name='dend', cell=self)
        self.dend.nseg = 10
        self.dend.connect(self.soma(1))
        self.all.append(sec=self.dend)

        self.axon = h.Section(name='axon', cell=self)
        self.axon.connect(self.soma(0))
        self.all.append(sec=self.axon)

        self._ncs = []
        self.number = num
        self.cells = {}

        self.dend1 = h.Section(name='dend1', cell=self)
        self.dend1.nseg = 10
        self.dend1.connect(self.soma(0))

        self.dend2 = h.Section(name='dend2', cell=self)
        self.dend2.nseg = 10
        self.dend2.connect(self.soma(0.5))

        self.dend3 = h.Section(name='dend3', cell=self)
        self.dend3.nseg = 10
        self.dend3.connect(self.soma(1))

        self.dend4 = h.Section(name='dend4', cell=self)
        self.dend4.nseg = 10
        self.dend4.connect(self.soma(0.8))

        self.dends = [self.dend1, self.dend, self.dend2, self.dend3, self.dend4]

        for sec in self.dends:
            self.all.append(sec=sec)
        '''
                for d in self.dends:
            synE = h.AMPA(d(0.5))
            synE.tau = 1
            synE.e = 30
            self.synlistex.append(synE)
        '''
        self.AMPA_syns = []
        self.NMDA_syns = []
        self.GABA_syns = []

        self.netcons = []

        self._synapses()

    def _synapses(self):
        for d in self.dends:
            for i in range(50):
                synI = h.GABAA(d(0.5))
                synI.tau = 0.3
                synI.e = -30
                self.GABA_syns.append(synI)
                synE = h.AMPA(d(0.5))
                synE.tau = 1
                synE.e = 50
                self.AMPA_syns.append(synE)
                synE = h.NMDA1(d(0.5))
                self.NMDA_syns.append(synE)