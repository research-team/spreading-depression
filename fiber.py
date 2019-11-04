from neuron import h, gui
import math
import random
#neuron.load_mechanisms("./mod")

class fiber(object):
    '''
    fiber class with parameters:
    L: int (mkM)
        length of compartment
    d: float 
        diameter of fiber
    num: int
        number of compartments
    coordinates: dict (updates by position())
        coordinates of each section
    zpozition: int 
        z - coordinate for few cells simulation
    fast_diff: bool
        Is there fast diffusion?
          -Yes: True 
          -No: False
    diffs: list
        list of diffusion mechanisms (NEURON staff)
    recs: list
        list of receptors mechanisms (NEURON staff)
    '''      
    def __init__(self, glia):
        self.glia = glia
        self.diffs = []
        self.recs = []
        self.L = 100
        self.diam = 2
        self.num = 10
        self.create_sections()
        self.build_topology()
        self.build_subsets()
        self.define_geometry()
        self.define_biophysics()
    def create_sections(self):
        '''
        Creates sections (compartments)
        '''
        self.soma = h.Section(name='soma', cell=self)
        self.branch = h.Section(name='branch', cell=self)
        self.stimsec = [h.Section(name='stimsec[%d]' % i) for i in range(self.num)]
    def build_topology(self):
        '''
        Connects sections 
        '''
        self.branch.connect(self.soma(0), 1)
        self.stimsec[0].connect(self.branch(0), 1)
        for i in range(1, len(self.stimsec)):
            self.stimsec[i].connect(self.stimsec[i-1])
    def define_geometry(self):
        '''
        Adds length and diameter to sections
        '''
        for sec in self.stimsec:
            sec.L = self.L # microns
            sec.diam = self.diam # microns
        self.branch.L = self.L
        self.branch.diam = self.diam*2
        self.branch.nseg = 3
        self.soma.L = self.soma.diam = 30
        self.soma.nseg = 3
        h.define_shape() # Translate into 3D points.
    def define_biophysics(self):
        '''
        Adds channels and their parameters 
        '''
        for sec in self.all: # 'all' defined in build_subsets
            sec.Ra = 100  # Axial resistance in Ohm * cm
            sec.cm = 1      # Membrane capacitance in micro Farads / cm^2
            sec.insert('nakpump')
            sec.insert('leak')
            sec.insert('tot')
        if self.glia:
            for sec in self.all:
                sec.insert('getconc')
                sec.insert('kir')
                sec.insert('kdrglia')
                sec.gbar_kir = 0.025
                sec.gkbar_kdrglia = 0.025
                sec.km_k_nakpump = 5
                sec.km_na_nakpump = 10
        else:
            for sec in self.all:
                sec.insert('accum')
                sec.insert('capump')
                sec.insert('nax')
                sec.k1buf_accum = 20
                sec.k2buf_accum = 0.5
                sec.tau_accum = 100
                sec.setvolout_accum = 0.2
                sec.setvolglia_accum = 1
                sec.km_k_nakpump = 2
                sec.km_na_nakpump = 10
                sec.scale_capump = 4e-6
                sec.imax_nax = 3.2

            self.soma.insert("nachan")
            self.soma.insert("nap")
            self.soma.insert("ka")
            self.soma.insert("kdr")
            self.soma.insert("sk")
            self.soma.insert("cal")
            self.soma.insert("cat")
            self.soma.insert("xiong")
            self.soma.gnabar_nachan = 0.4
            self.soma.shiftm_nachan=-10
            self.soma.gnabar_nap = 0.000125
            self.soma.gkbar_ka = 0.2
            self.soma.gkbar_kdr = 0.2
            self.soma.gkbar_sk = 0.001
            self.soma.gcalbar_cal = 0.001
            self.soma.gcatbar_cat = 0.0001
            self.soma.g_xiong = .00

            self.branch.insert("nap")
            self.branch.insert("kdr")
            self.branch.gnabar_nap = 0.001
            self.branch.gkbar_kdr = 1e-6

            for sec in self.stimsec:
                sec.insert('nap')
                sec.insert('kdr')
                sec.insert('sk')
                sec.insert('cal')
                sec.insert('cat')
                sec.insert('xiong')
                sec.insert('nmda')
                sec.gnabar_nap = 0
                sec.gkbar_kdr = 0.5
                sec.gkbar_sk = 0.02
                sec.gcalbar_cal = 0.0001
                sec.gcatbar_cat = 0.0001
                sec.g_xiong = 0.0
                sec.gbar_nmda = 0.0001

    def build_subsets(self):
        '''
        adds sections in NEURON SectionList
        '''
        self.all = h.SectionList()
        for sec in h.allsec():
          self.all.append(sec=sec)  
    def connect2target(self, target):
        '''
        Adds presynapses 
        Parameters
        ----------
        target: NEURON cell
            target neuron 
        Returns
        -------
        nc: NEURON NetCon
            connection between neurons
        '''
        nc = h.NetCon(self.branch(1)._ref_v, target, sec = self.branch)
        nc.threshold = 10
        return nc