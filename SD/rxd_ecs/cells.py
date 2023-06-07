import logging
import random
from neuron import h

h.load_file('stdlib.hoc')

somaR = 11.0  # soma radius
dendR = 4  # dendrite radius
dendL = 300.0
dendL1 = 300.0
dendL2 = 300.0
dendL3 = 300.0  # dendrite length
axonR = 2
axonL = 100
doff = dendL + somaR


class Cell:
    def __init__(self, x, y, z, num):
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

        self._spike_detector = h.NetCon(self.soma(0.5)._ref_v, None, sec=self.soma)

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

        self.dends = [self.dend, self.dend1, self.dend2, self.dend3, self.dend4]

        for sec in self.dends:
            self.all.append(sec=sec)

        self.AMPA_syns = []
        self.NMDA_syns = []
        self.GABA_syns = []

        self.netcons = []

        self._synapses()

    def _synapses(self):
        for d in self.dends:
            for i in range(50):
                synI = h.GABAA(d(0.5))
                synI.tau = 6  # 0.5  # 0.3
                synI.e = -75
                self.GABA_syns.append(synI)
                synE = h.AMPA(d(0.5))
                synE.tau = 0.8
                self.AMPA_syns.append(synE)
                synE = h.NMDA1(d(0.5))
                self.NMDA_syns.append(synE)

    def subsets(self):
        '''
        NEURON staff
        adds sections in NEURON SectionList
        '''
        self.all = h.SectionList()
        for sec in h.allsec():
            self.all.append(sec=sec)


class Bask23(Cell):
    def __init__(self, x, y, z, num):
        super().__init__(x, y, z, num)
        self.id = 1
        self.Excitatory = -1
        self.name = 'L23 superficial interneurons basket'

        # ---------------soma----------------
        for mechanism_s in ['extracellular', 'naf2',
                            'kdr_fs', 'IKsin', 'hin',
                            'kapin', 'canin', 'kctin',
                            'cadynin', 'nap',
                            'pas']:
            self.soma.insert(mechanism_s)

        self.soma(0.5).naf2.gbar = 0.06  # 0.06  # 0.5
        self.soma(0.5).kdr_fs.gbar = 0.1 * 3  # 0.001
        self.soma(0.5).IKsin.gKsbar = 0.000725 * 0.1
        self.soma(0.5).hin.gbar = 0.00001
        self.soma(0.5).kapin.gkabar = 0.001 * 10  # 0.0032 * 15
        self.soma(0.5).canin.gcalbar = 0.0001  # 0.0003
        self.soma(0.5).kctin.gkcbar = 0.025  # 0.0001
        self.soma(0.5).nap.gnapbar = 0.0006  # missing in this neuron
        self.soma(0.5).pas.g = 0.001
        self.soma(0.5).pas.e = -65  # -70
        self.soma.Ra = 200  # 100

        # ---------------dend----------------
        for mechanism_d in ['Nafin', 'kdrin',
                            'kapin', 'pas', 'nap']:
            self.dend.insert(mechanism_d)
            self.dend1.insert(mechanism_d)
            self.dend2.insert(mechanism_d)
            self.dend3.insert(mechanism_d)
            self.dend4.insert(mechanism_d)

        self.dend(0.5).Nafin.gnafbar = 0.06  # 0.00018 * 10
        self.dend(0.5).kdrin.gkdrbar = 0.1 * 3
        self.dend(0.5).kapin.gkabar = 0.001 * 10  # 0.000032 * 15 * 10
        self.dend(0.5).nap.gnapbar = 0.0006  # 0.000018
        self.dend(0.5).pas.g = 0.01
        self.dend(0.5).pas.e = -65  # -73
        self.dend.Ra = 200  # 150

        self.dend1(0.5).Nafin.gnafbar = 0.06  # 0.00018 * 10
        self.dend1(0.5).kdrin.gkdrbar = 0.1 * 3
        self.dend1(0.5).kapin.gkabar = 0.001 * 10
        self.dend1(0.5).nap.gnapbar = 0.0006
        self.dend1(0.5).pas.g = 0.01
        self.dend1(0.5).pas.e = -65  # -73
        self.dend1.Ra = 200  # 150

        self.dend2(0.5).nap.gnapbar = 0.0001
        self.dend2(0.5).Nafin.gnafbar = 0.01  # 0.00018 * 10
        self.dend2(0.5).kdrin.gkdrbar = 0.01 * 3
        self.dend2(0.5).kapin.gkabar = 0.001 * 10
        self.dend2(0.5).pas.g = 0.01
        self.dend2(0.5).pas.e = -65  # -73
        self.dend2.Ra = 200  # 150

        self.dend3(0.5).nap.gnapbar = 0.0001
        self.dend3(0.5).Nafin.gnafbar = 0.01  # 0.00018 * 10
        self.dend3(0.5).kdrin.gkdrbar = 0.01 * 3
        self.dend3(0.5).kapin.gkabar = 0.001 * 10
        self.dend3(0.5).pas.g = 0.01
        self.dend3(0.5).pas.e = -65  # -73
        self.dend3.Ra = 200  # 150

        self.dend4(0.5).nap.gnapbar = 0.0001
        self.dend4(0.5).Nafin.gnafbar = 0.01  # 0.00018 * 10
        self.dend4(0.5).kdrin.gkdrbar = 0.01 * 3
        self.dend4(0.5).kapin.gkabar = 0.001 * 10
        self.dend4(0.5).pas.g = 0.01
        self.dend4(0.5).pas.e = -65  # -73
        self.dend4.Ra = 200  # 150

        # ---------------axon----------------
        for mechanism_a in ['Nafin', 'kdrin', 'pas']:
            self.axon.insert(mechanism_a)

        self.axon(0.5).Nafin.gnafbar = 0.4  # 0.4  # 0.5
        self.axon(0.5).kdrin.gkdrbar = 0.4 * 2  # 0.001
        self.axon(0.5).pas.g = 0.001  # 0.0002
        self.axon(0.5).pas.e = -65  # -73
        self.axon.Ra = 100
        self.axon.cm = 1.2

        for sec in self.all:
            sec.cm = 1  # 1.2
            sec.ena = 50.
            sec.ek = -100  # -90
            logging.info(sec.psection())
        # ek = -100.
        # e = -65.
        # ena = 50.
        # vca = 125.

        self.k_vec = h.Vector().record(self.soma(0.5)._ref_ik)
        self.na_vec = h.Vector().record(self.soma(0.5)._ref_ina)
        self.na_concentration = h.Vector().record(self.soma(0.5)._ref_nai)
        self.k_concentration = h.Vector().record(self.soma(0.5)._ref_ki)
        self.v_vec = h.Vector().record(self.soma(0.5)._ref_v)


class Axax23(Cell):  #
    def __init__(self, x, y, z, num):
        super().__init__(x, y, z, num)
        self.id = 2
        self.Excitatory = -1
        self.name = 'L23 superficial interneurons axoaxonic'

        # ---------------soma----------------
        for mechanism_s in ['extracellular', 'naf2',
                            'kdrin',
                            'IKsin', 'hin', 'kapin', 'canin',
                            'kctin', 'cadynin',
                            'nap',
                            'pas']:
            self.soma.insert(mechanism_s)

        self.soma(0.5).naf2.gbar = 0.75  # 0.06  # 0.75
        self.soma(0.5).nap.gnapbar = 0.0006
        self.soma(0.5).kdrin.gkdrbar = 0.1  # 0.001
        self.soma(0.5).IKsin.gKsbar = 0.000725 * 0.1
        self.soma(0.5).hin.gbar = 0.00001
        self.soma(0.5).kapin.gkabar = 0.0032 * 15
        self.soma(0.5).canin.gcalbar = 0.0003  # 0.0001  # 0.0003
        self.soma(0.5).kctin.gkcbar = 0.025
        self.soma(0.5).pas.g = 0.002
        self.soma(0.5).pas.e = -65  # -70
        self.soma.Ra = 200  # 100

        # ---------------dend----------------
        for mechanism_d in ['Nafin', 'kdrin', 'kapin', 'pas', 'nap']:
            self.dend.insert(mechanism_d)
            self.dend1.insert(mechanism_d)
            self.dend2.insert(mechanism_d)
            self.dend3.insert(mechanism_d)
            self.dend4.insert(mechanism_d)

        self.dend(0.5).Nafin.gnafbar = 0.06  # 0.00018 * 10
        self.dend(0.5).nap.gnapbar = 0.0006
        self.dend(0.5).kdrin.gkdrbar = 0.1  # 0.018
        self.dend(0.5).kapin.gkabar = 0.001  # 0.000032 #* 15 * 10
        self.dend(0.5).pas.g = 0.01  # 1 / 100
        self.dend(0.5).pas.e = -65  # -73
        self.dend.Ra = 200  # 150

        self.dend1(0.5).Nafin.gnafbar = 0.06  # 0.00018 * 10
        self.dend1(0.5).nap.gnapbar = 0.0006
        self.dend1(0.5).kdrin.gkdrbar = 0.1  # 0.018 * 0.5
        self.dend1(0.5).kapin.gkabar = 0.001  # 0.000032 #* 15 * 10
        self.dend1(0.5).pas.g = 0.01  # 1 / 100
        self.dend1(0.5).pas.e = -65  # -73
        self.dend1.Ra = 200  # 150

        self.dend2(0.5).Nafin.gnafbar = 0.01  # 0.00018 * 10
        self.dend2(0.5).nap.gnapbar = 0.0001
        self.dend2(0.5).kdrin.gkdrbar = 00.01  # .018 * 0.5
        self.dend2(0.5).kapin.gkabar = 0.001  # 0.000032 #* 15 * 10
        self.dend2(0.5).pas.g = 0.01  # 1 / 100
        self.dend2(0.5).pas.e = -65  # -73
        self.dend2.Ra = 200  # 150

        self.dend3(0.5).Nafin.gnafbar = 0.01  # 0.00018 * 10
        self.dend3(0.5).nap.gnapbar = 0.0001
        self.dend3(0.5).kdrin.gkdrbar = 0.01  # 0.018 * 0.5
        self.dend3(0.5).kapin.gkabar = 0.001  # 0.000032 #* 15 * 10
        self.dend3(0.5).pas.g = 0.01  # 1 / 100
        self.dend3(0.5).pas.e = -65  # -73
        self.dend3.Ra = 200  # 150

        self.dend4(0.5).Nafin.gnafbar = 0.01  # 0.00018 * 10
        self.dend4(0.5).nap.gnapbar = 0.0001
        self.dend4(0.5).kdrin.gkdrbar = 0.0001  # 0.018 * 0.5
        self.dend4(0.5).kapin.gkabar = 0.001  # 0.000032 #* 15 * 10
        self.dend4(0.5).pas.g = 0.01  # 1 / 100
        self.dend4(0.5).pas.e = -65  # -73
        self.dend4.Ra = 200  # 150

        for mechanism_a in ['Nafin', 'kdrin', 'pas']:
            self.axon.insert(mechanism_a)

        self.axon(0.5).Nafin.gnafbar = 0.4
        self.axon(0.5).kdrin.gkdrbar = 0.4  # 0.001
        self.axon(0.5).pas.g = 0.001  # 0.0002
        self.axon(0.5).pas.e = -65  # -73
        self.axon.Ra = 100
        self.axon.cm = 1.2

        for sec in self.all:
            sec.cm = 1  # 0.9
            sec.ena = 50.
            sec.ek = -100.
            # sec.eca =   125.

        self.k_vec = h.Vector().record(self.soma(0.5)._ref_ik)
        self.na_vec = h.Vector().record(self.soma(0.5)._ref_ina)
        self.na_concentration = h.Vector().record(self.soma(0.5)._ref_nai)
        self.k_concentration = h.Vector().record(self.soma(0.5)._ref_ki)

        self.v_vec = h.Vector().record(self.soma(0.5)._ref_v)


class LTS23(Cell):  #
    def __init__(self, x, y, z, num):
        super().__init__(x, y, z, num)
        self.id = 3
        self.Excitatory = -1
        self.name = 'L23 superficial interneurons low threshold spiking'

        # ---------------soma----------------
        for mechanism_s in ['extracellular', 'Nafin',
                            'kdrin', 'IKsin', 'hin', 'kapin', 'canin',
                            'kctin', 'cadynin',
                            'nap',
                            'pas']:
            self.soma.insert(mechanism_s)

        self.soma(0.5).Nafin.gnafbar = 0.45  # 0.06  # 0.45
        self.soma(0.5).kdrin.gkdrbar = 0.1 * 5  # 0.0001
        self.soma(0.5).IKsin.gKsbar = 0.000725 * 0.1
        self.soma(0.5).hin.gbar = 0.00001
        self.soma(0.5).kapin.gkabar = 0.0032 * 15  # 0.001  # 0.0032 * 15
        self.soma(0.5).canin.gcalbar = 0.0003  # 0.0001  # 0.0003
        self.soma(0.5).kctin.gkcbar = 0.025 * 5  # 0.0001
        self.soma(0.5).pas.g = 0.001  # 1 / 100
        self.soma(0.5).pas.e = -65  # -73
        self.soma.Ra = 200.  # 150
        self.soma.cm = 1.2
        self.soma(0.5).nap.gnapbar = 0.0006  # 0.000018

        # ---------------dend----------------
        for mechanism_d in ['Nafin', 'kdrin', 'kapin', 'pas', 'nap']:
            self.dend.insert(mechanism_d)
            self.dend1.insert(mechanism_d)
            self.dend2.insert(mechanism_d)
            self.dend3.insert(mechanism_d)
            self.dend4.insert(mechanism_d)

        self.dend(0.5).Nafin.gnafbar = 0.06  # 0.0018 * 5
        self.dend(0.5).kdrin.gkdrbar = 0.1 * 5  # 0.018
        self.dend(0.5).kapin.gkabar = 0.001 * 5  # 0.000032 #* 15 * 10
        self.dend(0.5).nap.gnapbar = 0.0006  # 0.000018
        self.dend(0.5).pas.g = 0.01  # 1 / 100
        self.dend(0.5).pas.e = -65  # -73
        self.dend.Ra = 200  # 150

        self.dend1(0.5).Nafin.gnafbar = 0.06  # 0.0018 * 5
        self.dend1(0.5).kdrin.gkdrbar = 0.1 * 5  # 0.018 * 0.5
        self.dend1(0.5).kapin.gkabar = 0.001 * 5  # 0.000032 #* 15 * 10
        self.dend1(0.5).pas.g = 0.02  # 1 / 100
        self.dend1(0.5).pas.e = -65  # -73
        self.dend1.Ra = 200  # 150
        self.dend1(0.5).nap.gnapbar = 0.0006  # 0.000018

        self.dend2(0.5).Nafin.gnafbar = 0.01  # 0.0018 * 5
        self.dend2(0.5).kdrin.gkdrbar = 0.01 * 5  # 0.018 * 0.5
        self.dend2(0.5).kapin.gkabar = 0.001 * 5  # 0.000032 #* 15 * 10
        self.dend2(0.5).pas.g = 0.02  # 1 / 100
        self.dend2(0.5).pas.e = -65  # -73
        self.dend2.Ra = 200  # 150
        self.dend2(0.5).nap.gnapbar = 0.0001  # 0.000018

        self.dend3(0.5).Nafin.gnafbar = 0.01  # 0.0018 * 5
        self.dend3(0.5).kdrin.gkdrbar = 0.01 * 5  # 0.018 * 0.5
        self.dend3(0.5).kapin.gkabar = 0.001 * 5  # 0.000032 #* 15 * 10
        self.dend3(0.5).pas.g = 0.02  # 1 / 100
        self.dend3(0.5).pas.e = -65  # -73
        self.dend3.Ra = 200  # 150
        self.dend3(0.5).nap.gnapbar = 0.0001  # 0.000018

        self.dend4(0.5).Nafin.gnafbar = 0.01  # 0.0018 * 5
        self.dend4(0.5).kdrin.gkdrbar = 0.01 * 5  # 0.018 * 0.5
        self.dend4(0.5).kapin.gkabar = 0.001 * 5  # 0.000032 #* 15 * 10
        self.dend4(0.5).pas.g = 0.02  # 1 / 100
        self.dend4(0.5).pas.e = -65  # -73
        self.dend4.Ra = 200  # 150
        self.dend4(0.5).nap.gnapbar = 0.0001  # 0.000018

        self.vd1 = h.Vector().record(self.dend(0.5)._ref_ina_Nafin)
        # self.vd2 = h.Vector().record(self.dend(0.5)._ref_ina_napf_spinstell)
        self.vd3 = h.Vector().record(self.dend(0.5)._ref_ik_kdrin)
        self.vd4 = h.Vector().record(self.dend(0.5)._ref_ik_kapin)

        # ---------------axon----------------
        for mechanism_a in ['Nafin', 'kdrin', 'pas']:
            self.axon.insert(mechanism_a)

        self.axon(0.5).Nafin.gnafbar = 0.4
        self.axon(0.5).kdrin.gkdrbar = 0.4 * 2  # 0.001
        self.axon(0.5).pas.g = 0.01  # 0.001  # 0.0002
        self.axon(0.5).pas.e = -65  # -73
        self.axon.Ra = 100
        self.axon.cm = 1.2

        for sec in self.all:
            sec.cm = 1
            sec.ena = 50.
            sec.ek = -100

        self.k_vec = h.Vector().record(self.soma(0.5)._ref_ik)
        self.na_vec = h.Vector().record(self.soma(0.5)._ref_ina)
        self.na_concentration = h.Vector().record(self.soma(0.5)._ref_nai)
        self.k_concentration = h.Vector().record(self.soma(0.5)._ref_ki)
        self.v_vec = h.Vector().record(self.soma(0.5)._ref_v)


class Spinstel4(Cell):  #
    def __init__(self, x, y, z, num):
        super().__init__(x, y, z, num)
        self.id = 4
        self.Excitatory = 1
        self.name = 'L4 spiny stellate'

        for mechanism_s in ['extracellular', 'Nafin',
                            'nap', 'calc', 'cal', 'can',
                            'car', 'cat', 'kdr_fs', 'IKs', 'ka',
                            'h',
                            'kca', 'ican', 'cadyn',
                            'pas']:
            self.soma.insert(mechanism_s)

        self.soma(0.5).Nafin.gnafbar = 0.15 * 3  # 0.018 * 3
        self.soma(0.5).nap.gnapbar = 0.00015  # 0.000018
        self.soma(0.5).calc.gcabar = 0.0001 * 0.1
        self.soma(0.5).cal.gcalbar = 0.0005  # 0.0001 * 0.3
        self.soma(0.5).can.gcabar = 0.0002 * 0.1
        self.soma(0.5).car.gcabar = 0.000001 * 0.3 * 0.1
        self.soma(0.5).cat.gcatbar = 0.0001  # 0.0002 * 0.3 * 0.1
        self.soma(0.5).kdr_fs.gbar = 0.1 * 5  # 0.018 * 0.3
        self.soma(0.5).IKs.gKsbar = 0.0012 * 0.5
        self.soma(0.5).ka.gbar = 0.0007 * 5
        self.soma(0.5).kca.gbar = 0.1  # 0.005 * 5
        self.soma(0.5).h.gbar = 1.8e-5 * 0.5
        self.soma(0.5).ican.gbar = 0.001 * 0.07 * 0
        self.soma(0.5).pas.g = 0.001
        self.soma(0.5).pas.e = -65
        self.soma.Ra = 250.  # 100

        self.v1 = h.Vector().record(self.soma(0.5)._ref_ina_Nafin)

        # ---------------dend----------------
        for mechanism_d in ['Nafin', 'nap', 'calc',
                            'cal', 'can', 'car', 'cat',
                            'kdr_fs', 'IKs', 'ka', 'h', 'kca', 'ican',
                            'cadyn', 'pas']:
            self.dend.insert(mechanism_d)
            self.dend1.insert(mechanism_d)
            self.dend2.insert(mechanism_d)
            self.dend3.insert(mechanism_d)
            self.dend4.insert(mechanism_d)

        self.dend(0.5).Nafin.gnafbar = 0.075 * 10  # 0.018 * 0.1
        self.dend(0.5).nap.gnapbar = 7.5E-05  # 0.000018
        self.dend(0.5).calc.gcabar = 0.0001 * 0.1  #
        self.dend(0.5).cal.gcalbar = 0.0005  # 0.0001 * 0.3  #
        self.dend(0.5).can.gcabar = 0.0002 * 0.3
        self.dend(0.5).car.gcabar = 0.000001 * 0.3 * 0.1 * 0.3  #
        self.dend(0.5).cat.gcatbar = 0.0001  # 0.0002 * 0.3 * 0.1  #
        self.dend(0.5).kdr_fs.gbar = 0.075 * 5  # 0.018 * 0.09
        self.dend(0.5).IKs.gKsbar = 0.0012
        self.dend(0.5).ka.gbar = 0.03 * 5  # 0.0007
        self.dend(0.5).kca.gbar = 0.01 * 5  # 0.005 * 5 * 0.001  #
        self.dend(0.5).h.gbar = 1.8e-5 * 0.5  #
        self.dend(0.5).ican.gbar = 0.001 * 0.07 * 0.1  #
        self.dend(0.5).pas.g = 0.01
        self.dend(0.5).pas.e = -65
        self.dend.Ra = 250  # 150

        self.dend1(0.5).Nafin.gnafbar = 0.075 * 10  # 0.018 * 0.4
        self.dend1(0.5).nap.gnapbar = 7.5E-05  # 0.000018  # * 3
        self.dend1(0.5).calc.gcabar = 0.0001 * 0.1  #
        self.dend1(0.5).cal.gcalbar = 0.0005  # 0.0001 * 0.3  #
        self.dend1(0.5).can.gcabar = 0.0002 * 0.3
        self.dend1(0.5).car.gcabar = 0.000001 * 0.3 * 0.1 * 0.3  #
        self.dend1(0.5).cat.gcatbar = 0.0001  # 0.0002 * 0.3 * 0.1  #
        self.dend1(0.5).kdr_fs.gbar = 0.075 * 5  # 0.018 * 0.09
        self.dend1(0.5).IKs.gKsbar = 0.0012
        self.dend1(0.5).ka.gbar = 0.002 * 5  # 0.0007
        self.dend1(0.5).kca.gbar = 0.01 * 5  # 0.005 * 5 * 0.0001  #
        self.dend1(0.5).h.gbar = 1.8e-5 * 0.5  #
        self.dend1(0.5).ican.gbar = 0.001 * 0.07 * 0.1  #
        self.dend1(0.5).pas.g = 0.01
        self.dend1(0.5).pas.e = -65
        self.dend1.Ra = 250  # 150

        self.dend2(0.5).Nafin.gnafbar = 0.005 * 10  # 0.018 * 0.1
        self.dend2(0.5).nap.gnapbar = 5.E-06  # 0.000018
        self.dend2(0.5).calc.gcabar = 0.0001 * 0.1  #
        self.dend2(0.5).cal.gcalbar = 0.0005  # 0.0001 * 0.3  #
        self.dend2(0.5).can.gcabar = 0.0002 * 0.3
        self.dend2(0.5).car.gcabar = 0.000001 * 0.3 * 0.1 * 0.3  #
        self.dend2(0.5).cat.gcatbar = 0.0001  # 0.0002 * 0.3 * 0.1  #
        self.dend2(0.5).kdr_fs.gbar = 0.018 * 0.09 * 5
        self.dend2(0.5).IKs.gKsbar = 0.0012
        self.dend2(0.5).ka.gbar = 0.002 * 5  # 0.0007
        self.dend2(0.5).kca.gbar = 0.01 * 5  # 0.005 * 5 * 0.001  #
        self.dend2(0.5).h.gbar = 1.8e-5 * 0.5  #
        self.dend2(0.5).ican.gbar = 0.001 * 0.07 * 0.1  #
        self.dend2(0.5).pas.g = 0.01
        self.dend2(0.5).pas.e = -65
        self.dend2.Ra = 250  # 150

        self.dend3(0.5).Nafin.gnafbar = 0.005 * 10  # 0.018 * 0.1
        self.dend3(0.5).nap.gnapbar = 5.E-06  # 0.000018
        self.dend3(0.5).calc.gcabar = 0.0001 * 0.1  #
        self.dend3(0.5).cal.gcalbar = 0.0005  # 0.0001 * 0.3  #
        self.dend3(0.5).can.gcabar = 0.0002 * 0.3
        self.dend3(0.5).car.gcabar = 0.000001 * 0.3 * 0.1 * 0.3  #
        self.dend3(0.5).cat.gcatbar = 0.0001  # 0.0002 * 0.3 * 0.1  #
        self.dend3(0.5).kdr_fs.gbar = 0.018 * 0.09 * 5
        self.dend3(0.5).IKs.gKsbar = 0.0012
        self.dend3(0.5).ka.gbar = 0.002 * 5  # 0.0007
        self.dend3(0.5).kca.gbar = 0.005 * 5 * 0.001 * 5  #
        self.dend3(0.5).h.gbar = 1.8e-5 * 0.5  #
        self.dend3(0.5).ican.gbar = 0.001 * 0.07 * 0.1  #
        self.dend3(0.5).pas.g = 0.01
        self.dend3(0.5).pas.e = -65
        self.dend3.Ra = 250  # 150

        self.dend4(0.5).Nafin.gnafbar = 0.005 * 10  # 0.018 * 0.1
        self.dend4(0.5).nap.gnapbar = 5.E-06  # 0.000018
        self.dend4(0.5).calc.gcabar = 0.0001 * 0.1  #
        self.dend4(0.5).cal.gcalbar = 0.0005  # 0.0001 * 0.3  #
        self.dend4(0.5).can.gcabar = 0.0002 * 0.3
        self.dend4(0.5).car.gcabar = 0.000001 * 0.3 * 0.1 * 0.3  #
        self.dend4(0.5).cat.gcatbar = 0.0001  # 0.0002 * 0.3 * 0.1  #
        self.dend4(0.5).kdr_fs.gbar = 0.018 * 0.09 * 5
        self.dend4(0.5).IKs.gKsbar = 0.0012
        self.dend4(0.5).ka.gbar = 0.002 * 5  # 0.0007
        self.dend4(0.5).kca.gbar = 0.005 * 5 * 0.001 * 5  #
        self.dend4(0.5).h.gbar = 1.8e-5 * 0.5  #
        self.dend4(0.5).ican.gbar = 0.001 * 0.07 * 0.1  #
        self.dend4(0.5).pas.g = 0.01
        self.dend4(0.5).pas.e = -65
        self.dend4.Ra = 250  # 150

        for mechanism_a in ['Nafin', 'kdrin',
                            'pas']:
            self.axon.insert(mechanism_a)

        self.axon(0.5).Nafin.gnafbar = 0.4
        self.axon(0.5).kdrin.gkdrbar = 0.4  # 0.001
        self.axon(0.5).pas.g = 0.001  # 0.0002
        self.axon(0.5).pas.e = -65  # -73
        self.axon.Ra = 100
        self.axon.cm = 1.2

        for sec in self.all:
            sec.cm = 0.9
            sec.ena = 50.
            sec.ek = -100.  # -95.

        self.k_vec = h.Vector().record(self.soma(0.5)._ref_ik)
        self.na_vec = h.Vector().record(self.soma(0.5)._ref_ina)
        self.na_concentration = h.Vector().record(self.soma(0.5)._ref_nai)
        self.k_concentration = h.Vector().record(self.soma(0.5)._ref_ki)
        self.v_vec = h.Vector().record(self.soma(0.5)._ref_v)


class EpilepsySpinstel4(Cell):  #
    def __init__(self, x, y, z, num):
        super().__init__(x, y, z, num)
        self.id = 4
        self.Excitatory = 1
        self.name = 'spiny stellate'

        for mechanism_s in ['extracellular', 'naf2_cc', 'pas', 'napf_spinstell', 'kdr_fs_cc', 'kc_fast_cc', 'ka_cc',
                            'km_cc', 'k2_cc', 'kahp_slower', 'cal_cc', 'cat_cc', 'ar', 'cad_cc']:
            self.soma.insert(mechanism_s)

        self.soma(0.5).naf2_cc.gbar = 0.65
        self.soma(0.5).napf_spinstell.gbar = 0.0002
        self.soma(0.5).kdr_fs_cc.gbar = 0.1 * 10
        self.soma(0.5).kc_fast_cc.gbar = 0.001 * 10
        self.soma(0.5).ka_cc.gbar = 0.03
        self.soma(0.5).km_cc.gbar = 0.00375
        self.soma(0.5).k2_cc.gbar = 0.0001
        self.soma(0.5).kahp_slower.gbar = 0.0001
        self.soma(0.5).cal_cc.gbar = 0.0005
        self.soma(0.5).cat_cc.gbar = 0.0001
        self.soma(0.5).ar.gbar = 0.00025
        self.soma(0.5).cad_cc.beta = 0.02
        self.soma(0.5).cad_cc.phi = 260000.
        self.soma(0.5).pas.g = 0.001
        self.soma(0.5).pas.e = -65
        self.soma.Ra = 150.

        # ---------------dend----------------
        for mechanism_d in ['naf2_cc', 'napf_spinstell', 'pas', 'kdr_fs_cc', 'kc_fast_cc', 'ka_cc', 'km_cc', 'k2_cc',
                            'kahp_slower', 'cal_cc', 'cat_cc', 'ar', 'cad_cc']:
            self.dend.insert(mechanism_d)
            self.dend1.insert(mechanism_d)
            self.dend2.insert(mechanism_d)
            self.dend3.insert(mechanism_d)
            self.dend4.insert(mechanism_d)
            # print(mechanism_d)

        self.dend(0.5).naf2_cc.gbar = 0.0075
        self.dend(0.5).napf_spinstell.gbar = 7.5E-05 / 100
        self.dend(0.5).kdr_fs_cc.gbar = 0.0075
        self.dend(0.5).kc_fast_cc.gbar = 0.01
        self.dend(0.5).ka_cc.gbar = 0.03
        self.dend(0.5).km_cc.gbar = 0.00375
        self.dend(0.5).k2_cc.gbar = 0.0001
        self.dend(0.5).kahp_slower.gbar = 0.0001
        self.dend(0.5).cal_cc.gbar = 0.0005
        self.dend(0.5).cat_cc.gbar = 0.0001
        self.dend(0.5).ar.gbar = 0.00025
        self.dend(0.5).cad_cc.beta = 0.05
        self.dend(0.5).cad_cc.phi = 260000.
        self.dend(0.5).pas.g = 0.02
        self.dend(0.5).pas.e = -65
        self.dend.Ra = 250.

        self.dend1(0.5).naf2_cc.gbar = 0.0075
        self.dend1(0.5).napf_spinstell.gbar = 7.5E-05 / 100
        self.dend1(0.5).kdr_fs_cc.gbar = 0.0075
        self.dend1(0.5).kc_fast_cc.gbar = 0.01
        self.dend1(0.5).ka_cc.gbar = 0.03
        self.dend1(0.5).km_cc.gbar = 0.00375
        self.dend1(0.5).k2_cc.gbar = 0.0001
        self.dend1(0.5).kahp_slower.gbar = 0.0001
        self.dend1(0.5).cal_cc.gbar = 0.0005
        self.dend1(0.5).cat_cc.gbar = 0.0001
        self.dend1(0.5).ar.gbar = 0.00025
        self.dend1(0.5).cad_cc.beta = 0.05
        self.dend1(0.5).cad_cc.phi = 260000.
        self.dend1(0.5).pas.g = 0.02
        self.dend1(0.5).pas.e = -65
        self.dend1.Ra = 250.

        self.dend2(0.5).naf2_cc.gbar = 0.0075
        self.dend2(0.5).napf_spinstell.gbar = 7.5E-05 / 100
        self.dend2(0.5).kdr_fs_cc.gbar = 0.0075
        self.dend2(0.5).kc_fast_cc.gbar = 0.01
        self.dend2(0.5).ka_cc.gbar = 0.03
        self.dend2(0.5).km_cc.gbar = 0.00375
        self.dend2(0.5).k2_cc.gbar = 0.0001
        self.dend2(0.5).kahp_slower.gbar = 0.0001
        self.dend2(0.5).cal_cc.gbar = 0.0005
        self.dend2(0.5).cat_cc.gbar = 0.0001
        self.dend2(0.5).ar.gbar = 0.00025
        self.dend2(0.5).cad_cc.beta = 0.05
        self.dend2(0.5).cad_cc.phi = 260000.
        self.dend2(0.5).pas.g = 0.02
        self.dend2(0.5).pas.e = -65
        self.dend2.Ra = 250.

        self.dend3(0.5).naf2_cc.gbar = 0.0075
        self.dend3(0.5).napf_spinstell.gbar = 7.5E-05 / 100
        self.dend3(0.5).kdr_fs_cc.gbar = 0.0075
        self.dend3(0.5).kc_fast_cc.gbar = 0.01
        self.dend3(0.5).ka_cc.gbar = 0.03
        self.dend3(0.5).km_cc.gbar = 0.00375
        self.dend3(0.5).k2_cc.gbar = 0.0001
        self.dend3(0.5).kahp_slower.gbar = 0.0001
        self.dend3(0.5).cal_cc.gbar = 0.0005
        self.dend3(0.5).cat_cc.gbar = 0.0001
        self.dend3(0.5).ar.gbar = 0.00025
        self.dend3(0.5).cad_cc.beta = 0.05
        self.dend3(0.5).cad_cc.phi = 260000.
        self.dend3(0.5).pas.g = 0.02
        self.dend3(0.5).pas.e = -65
        self.dend3.Ra = 250.

        self.dend4(0.5).naf2_cc.gbar = 0.0075
        self.dend4(0.5).napf_spinstell.gbar = 7.5E-05 / 100
        self.dend4(0.5).kdr_fs_cc.gbar = 0.0075
        self.dend4(0.5).kc_fast_cc.gbar = 0.01
        self.dend4(0.5).ka_cc.gbar = 0.03
        self.dend4(0.5).km_cc.gbar = 0.00375
        self.dend4(0.5).k2_cc.gbar = 0.0001
        self.dend4(0.5).kahp_slower.gbar = 0.0001
        self.dend4(0.5).cal_cc.gbar = 0.0005
        self.dend4(0.5).cat_cc.gbar = 0.0001
        self.dend4(0.5).ar.gbar = 0.00025
        self.dend4(0.5).cad_cc.beta = 0.05
        self.dend4(0.5).cad_cc.phi = 260000.
        self.dend4(0.5).pas.g = 0.02
        self.dend4(0.5).pas.e = -65
        self.dend4.Ra = 250.

        # self.vd1 = h.Vector().record(self.dend(0.5)._ref_ina_naf2)
        # self.vd2 = h.Vector().record(self.dend(0.5)._ref_ina_napf_spinstell)
        # self.vd3 = h.Vector().record(self.dend(0.5)._ref_ik_kdr_fs)
        # self.vd4 = h.Vector().record(self.dend(0.5)._ref_ik_ka)
        # self.vd5 = h.Vector().record(self.dend(0.5)._ref_ik_kc_fast)
        # self.vd7 = h.Vector().record(self.dend(0.5)._ref_ik_k2)
        # self.vd8 = h.Vector().record(self.dend(0.5)._ref_ik_kahp_slower)
        # self.vd9 = h.Vector().record(self.dend(0.5)._ref_ica_cal)

        # ---------------axon----------------
        for mechanism_a in ['naf2_cc', 'kdr_fs_cc', 'ka_cc', 'k2_cc', 'pas']:
            self.axon.insert(mechanism_a)
            # print(mechanism_a)

        self.axon(0.5).naf2_cc.gbar = 0.1 * 4
        self.axon(0.5).kdr_fs_cc.gbar = 0.9
        self.axon(0.5).ka_cc.gbar = 0.002
        self.axon(0.5).k2_cc.gbar = 0.1
        self.axon(0.5).pas.g = 0.01
        self.axon(0.5).pas.e = -65
        self.axon.Ra = 100.

        for sec in self.all:
            sec.cm = 0.9
            sec.ena = 50.
            sec.ek = -90

        self.k_vec = h.Vector().record(self.soma(0.5)._ref_ik)
        self.na_vec = h.Vector().record(self.soma(0.5)._ref_ina)
        self.na_concentration = h.Vector().record(self.soma(0.5)._ref_nai)
        self.k_concentration = h.Vector().record(self.soma(0.5)._ref_ki)
        self.v_vec = h.Vector().record(self.soma(0.5)._ref_v)


class LTS4(Cell):
    def __init__(self, x, y, z, num):
        super().__init__(x, y, z, num)
        self.id = 16
        self.Excitatory = -1
        self.name = 'L4 superficial interneurons low threshold spiking'

        # ---------------soma----------------
        for mechanism_s in ['extracellular', 'Nafin', 'kdrin', 'IKsin', 'hin', 'kapin', 'canin', 'kctin', 'cadynin',
                            'pas']:
            self.soma.insert(mechanism_s)

        self.soma(0.5).Nafin.gnafbar = 0.5
        self.soma(0.5).kdrin.gkdrbar = 0.001 * 100
        self.soma(0.5).IKsin.gKsbar = 0.000725 * 0.1
        self.soma(0.5).hin.gbar = 0.00001
        self.soma(0.5).kapin.gkabar = 0.0032 * 15
        self.soma(0.5).canin.gcalbar = 0.0003
        self.soma(0.5).kctin.gkcbar = 0.0001
        self.soma(0.5).pas.g = 0.0002
        self.soma(0.5).pas.e = -70
        self.soma.Ra = 100

        # ---------------dend----------------
        for mechanism_d in ['Nafin', 'kdrin', 'kapin', 'pas', 'nap']:
            self.dend.insert(mechanism_d)
            self.dend1.insert(mechanism_d)
            self.dend2.insert(mechanism_d)
            self.dend3.insert(mechanism_d)
            self.dend4.insert(mechanism_d)

            # print(mechanism_d)

        # self.dend(0.5).naf2.gbar =   0.2
        self.dend(0.5).Nafin.gnafbar = 0.00018 * 100
        self.dend(0.5).kdrin.gkdrbar = 0.018
        self.dend(0.5).kapin.gkabar = 0.000032 * 15 * 100
        self.dend(0.5).nap.gnapbar = 0.000018 * 100
        self.dend(0.5).pas.g = 1 / 100
        self.dend(0.5).pas.e = -73
        self.dend.Ra = 150

        self.dend1(0.5).Nafin.gnafbar = 0.00018 * 100
        self.dend1(0.5).kdrin.gkdrbar = 0.018 * 0.5
        self.dend1(0.5).kapin.gkabar = 0.000032 * 15 * 100
        self.dend1(0.5).pas.g = 1 / 100
        self.dend1(0.5).pas.e = -73
        self.dend1.Ra = 150
        self.dend1(0.5).nap.gnapbar = 0.000018 * 100

        self.dend2(0.5).Nafin.gnafbar = 0.00018 * 100
        self.dend2(0.5).kdrin.gkdrbar = 0.018 * 0.5
        self.dend2(0.5).kapin.gkabar = 0.000032 * 15 * 100
        self.dend2(0.5).pas.g = 1 / 100
        self.dend2(0.5).pas.e = -73
        self.dend2.Ra = 150
        self.dend2(0.5).nap.gnapbar = 0.000018 * 100

        self.dend3(0.5).Nafin.gnafbar = 0.00018 * 100
        self.dend3(0.5).kdrin.gkdrbar = 0.018 * 0.5
        self.dend3(0.5).kapin.gkabar = 0.000032 * 15 * 100
        self.dend3(0.5).pas.g = 1 / 100
        self.dend3(0.5).pas.e = -73
        self.dend3.Ra = 150
        self.dend3(0.5).nap.gnapbar = 0.000018 * 100

        self.dend4(0.5).Nafin.gnafbar = 0.00018 * 100
        self.dend4(0.5).kdrin.gkdrbar = 0.018 * 0.5
        self.dend4(0.5).kapin.gkabar = 0.000032 * 15 * 100
        self.dend4(0.5).pas.g = 1 / 100
        self.dend4(0.5).pas.e = -73
        self.dend4.Ra = 150
        self.dend4(0.5).nap.gnapbar = 0.000018 * 100

        self.vd1 = h.Vector().record(self.dend(0.5)._ref_ina_Nafin)
        # self.vd2 = h.Vector().record(self.dend(0.5)._ref_ina_napf_spinstell)
        self.vd3 = h.Vector().record(self.dend(0.5)._ref_ik_kdrin)
        self.vd4 = h.Vector().record(self.dend(0.5)._ref_ik_kapin)

        # ---------------axon----------------
        for mechanism_a in ['Nafin', 'kdrin', 'pas']:
            self.axon.insert(mechanism_a)

        self.axon(0.5).Nafin.gnafbar = 0.4
        self.axon(0.5).kdrin.gkdrbar = 0.4 #0.001
        self.axon(0.5).pas.g = 0.0002
        self.axon(0.5).pas.e = -73
        self.axon.Ra = 100
        self.axon.cm = 1.2

        for sec in self.all:
            sec.cm = 1.2
            # sec.cm = 0.9
            sec.ena = 50.
            sec.ek = -90
        self.k_vec = h.Vector().record(self.soma(0.5)._ref_ik)
        self.na_vec = h.Vector().record(self.soma(0.5)._ref_ina)
        self.na_concentration = h.Vector().record(self.soma(0.5)._ref_nai)
        self.k_concentration = h.Vector().record(self.soma(0.5)._ref_ki)
        self.v_vec = h.Vector().record(self.soma(0.5)._ref_v)


class TuftIB5(Cell):
    def __init__(self, x, y, z, num):
        super().__init__(x, y, z, num)
        self.id = 5
        self.Excitatory = 1
        self.name = 'L56 pyramidal tufted intrinsic bursting'

        # ---------------soma----------------
        for mechanism_s in ['extracellular', 'Naf',
                            'napf', 'kdr',
                            'kc', 'ka_ib', 'km_cc',
                            'k2_cc',
                            'kahp_deeppyr', 'cal_cc',
                            'cat_a',
                            'ar', 'cad_cc', 'pas']:
            self.soma.insert(mechanism_s)

        self.soma(0.5).Naf.gnafbar = 0.6  # 0.2  # 0.6
        self.soma(0.5).napf.gbar = 0.0008  # 0.00006
        self.soma(0.5).kdr.gkdrbar = 0.5  # 0.17  # 0.5
        self.soma(0.5).kc.gbar = 0.008 * 2  # 0.01
        self.soma(0.5).ka_ib.gbar = 0.02  # 0.005
        self.soma(0.5).km_cc.gbar = 0.0085 * 1.4  # 0.02  # 0.0005
        self.soma(0.5).k2_cc.gbar = 0.0005  # 0.0085  # 0.0005
        self.soma(0.5).kahp_deeppyr.gbar = 0.0002  # 0.0001
        self.soma(0.5).cal_cc.gbar = 0.004  # 0.0001
        self.soma(0.5).cat_a.gbar = 0.0001  # 5.E-05
        self.soma(0.5).ar.gbar = 0.0001  # 2.5E-05
        self.soma(0.5).cad_cc.beta = 0.02  # 0.01  # 0.02
        self.soma(0.5).cad_cc.phi = 4333.33333  # 0.01  # 10400.
        self.soma(0.5).pas.e = -70
        self.soma(0.5).pas.g = 0.001
        self.soma.Ra = 250.  # 100.

        # ---------------dend----------------
        for mechanism_d in ['Naf', 'napf', 'kdr_thlms',
                            'kc', 'ka_ib', 'km', 'k2',
                            'kahp_deeppyr', 'cal_thlms',
                            'cat_a', 'ar', 'cad', 'pas']:
            self.dend.insert(mechanism_d)
            self.dend1.insert(mechanism_d)
            self.dend2.insert(mechanism_d)
            self.dend3.insert(mechanism_d)
            self.dend4.insert(mechanism_d)

        self.dend(0.5).Naf.gnafbar = 0.1  # 0.075  # 0.1 level 2 in model db
        self.dend(0.5).napf.gbar = 0.0003 * 0.2  # 0.0002
        self.dend(0.5).kdr_thlms.gbar = 0.075
        self.dend(0.5).kc.gbar = 0.012 * 2  # 0.008  # 0.012
        self.dend(0.5).ka_ib.gbar = 0.03  # 0.008  # 0.03
        self.dend(0.5).km.gbar = 0.0136 * 1.4  # 0 #// 0.0005
        self.dend(0.5).k2.gbar = 0.0005  # 0.002
        self.dend(0.5).kahp_deeppyr.gbar = 0.0002
        self.dend(0.5).cal_thlms.gbar = 0.004  # 0.0005
        self.dend(0.5).cat_a.gbar = 0.0001  # 0.0005
        self.dend(0.5).ar.gbar = 0.0001  # 0.00025
        self.dend(0.5).cad.beta = 0.02
        self.dend(0.5).cad.phi = 86666.6667  # 52000.
        self.dend(0.5).pas.g = 1 / 100
        self.dend(0.5).pas.e = -70
        self.dend.Ra = 250  # 175

        self.dend1(0.5).Naf.gnafbar = 0.1  # 0.015  # 0.1 level 3 in modeldb
        self.dend1(0.5).napf.gbar = 6.E-05 * 0.2  # 0.0002
        self.dend1(0.5).kdr_thlms.gbar = 0.075
        self.dend1(0.5).kc.gbar = 0.012 * 2  # 0.00025  # 0.012
        self.dend1(0.5).ka_ib.gbar = 0.006  # 0.0006  # 0.006  # 0.03
        self.dend1(0.5).km.gbar = 0.0136 * 1.4  # 0  # // 0.0005
        self.dend1(0.5).k2.gbar = 0.0005  # 0.002
        self.dend1(0.5).kahp_deeppyr.gbar = 0.0002
        self.dend1(0.5).cal_thlms.gbar = 0.004  # 0.0005
        self.dend1(0.5).cat_a.gbar = 0.0005  # 0.0001  # 0.0005
        self.dend1(0.5).ar.gbar = 0.00025  # 0.0001  # 0.00025
        self.dend1(0.5).cad.beta = 0.075  # 0.02
        self.dend1(0.5).cad.phi = 86666.6667  # 52000.
        self.dend1(0.5).pas.g = 1 / 100
        self.dend1(0.5).pas.e = -70
        self.dend1.Ra = 250  # 175

        self.dend2(0.5).Naf.gnafbar = 0.1  # 0.015  # 0.1 level 4 in model db
        self.dend2(0.5).napf.gbar = 6.E-05 * 0.2  # 0.0002
        self.dend2(0.5).kdr_thlms.gbar = 0.075
        self.dend2(0.5).kc.gbar = 0.012 * 2  # 0.00025  # 0.012
        self.dend2(0.5).ka_ib.gbar = 0.03  # 0.0006  # 0.03
        self.dend2(0.5).km.gbar = 0.0136 * 1.4  # 0  # // 0.0005
        self.dend2(0.5).k2.gbar = 0.002  # 0.0005  # 0.002
        self.dend2(0.5).kahp_deeppyr.gbar = 0.0002
        self.dend2(0.5).cal_thlms.gbar = 0.004  # 0.0005
        self.dend2(0.5).cat_a.gbar = 0.0005  # 0.0001  # 0.0005
        self.dend2(0.5).ar.gbar = 0.00025  # 0.0001  # 0.00025
        self.dend2(0.5).cad.beta = 0.075  # 0.02
        self.dend2(0.5).cad.phi = 86666.6667  # 52000.
        self.dend2(0.5).pas.g = 1 / 100
        self.dend2(0.5).pas.e = -70
        self.dend2.Ra = 250  # 175

        self.dend3(0.5).Naf.gnafbar = 0.15  # 0.1 level 5 in modeldb
        self.dend3(0.5).napf.gbar = 0.0006 * 0.2  # 0.0002
        self.dend3(0.5).kdr_thlms.gbar = 0.12  # 0.075
        self.dend3(0.5).kc.gbar = 0.012 * 2  # 0.008  # 0.012
        self.dend3(0.5).ka_ib.gbar = 0.03  # 0.008  # 0.03
        self.dend3(0.5).km.gbar = 0.0136 * 1.4  # 0  # // 0.0005
        self.dend3(0.5).k2.gbar = 0.002  # 0.0005  # 0.002
        self.dend3(0.5).kahp_deeppyr.gbar = 0.0002
        self.dend3(0.5).cal_thlms.gbar = 0.004  # 0.0005
        self.dend3(0.5).cat_a.gbar = 0.0005  # 0.0001  # 0.0005
        self.dend3(0.5).ar.gbar = 0.00025  # 0.0001  # 0.00025
        self.dend3(0.5).cad.beta = 0.075  # 0.02
        self.dend3(0.5).cad.phi = 86666.6667  # 52000.
        self.dend3(0.5).pas.g = 1 / 100
        self.dend3(0.5).pas.e = -70
        self.dend3.Ra = 250  # 175

        self.dend4(0.5).Naf.gnafbar = 0.1  # 0.075  # 0.1 level 6 in modeldb
        self.dend4(0.5).napf.gbar = 0.0003 * 0.2  # 0.0002
        self.dend4(0.5).kdr_thlms.gbar = 0.075
        self.dend4(0.5).kc.gbar = 0.012 * 2  # 0.008  # 0.012
        self.dend4(0.5).ka_ib.gbar = 0.03  # 0.008  # 0.03
        self.dend4(0.5).km.gbar = 0.0136 * 1.4  # 0  # // 0.0005
        self.dend4(0.5).k2.gbar = 0.002  # 0.0005  # 0.002
        self.dend4(0.5).kahp_deeppyr.gbar = 0.0002
        self.dend4(0.5).cal_thlms.gbar = 0.004  # 0.0005
        self.dend4(0.5).cat_a.gbar = 0.0005  # 0.0001  # 0.0005
        self.dend4(0.5).ar.gbar = 0.0001  # 0.00025
        self.dend4(0.5).cad.beta = 0.075  # 0.02
        self.dend4(0.5).cad.phi = 86666.6667  # 52000.
        self.dend4(0.5).pas.g = 1 / 100
        self.dend4(0.5).pas.e = -70
        self.dend4.Ra = 250  # 175

        # ---------------axon----------------
        for mechanism_a in ['Nafin', 'kdrin', 'pas']:
            self.axon.insert(mechanism_a)

        self.axon(0.5).Nafin.gnafbar = 0.45  # 0.4
        self.axon(0.5).kdrin.gkdrbar = 0.45  # 0.001
        self.axon(0.5).pas.g = 0.001  # 0.005
        self.axon(0.5).pas.e = -70
        self.axon.Ra = 100.
        self.axon.cm = 1.2

        for sec in self.all:
            sec.cm = 0.9
            sec.ena = 50.
            sec.ek = -95

        self.k_vec = h.Vector().record(self.soma(0.5)._ref_ik)
        self.na_vec = h.Vector().record(self.soma(0.5)._ref_ina)
        self.na_concentration = h.Vector().record(self.soma(0.5)._ref_nai)
        self.k_concentration = h.Vector().record(self.soma(0.5)._ref_ki)
        self.v_vec = h.Vector().record(self.soma(0.5)._ref_v)


class EpilepsyTuftIB5(Cell):
    def __init__(self, x, y, z, num):
        super().__init__(x, y, z, num)
        self.id = 5
        self.Excitatory = 1
        self.name = 'pyramidal tufted intrinsic bursting'

        # ---------------soma----------------
        for mechanism_s in ['extracellular', 'naf2_cc', 'pas', 'napf_spinstell', 'kdr_fs_cc', 'kc_fast_cc', 'ka_cc',
                            'km_cc', 'k2_cc', 'kahp_slower', 'cal_cc', 'cat_cc', 'ar', 'cad_cc']:
            self.soma.insert(mechanism_s)
        # print(mechanism_s)

        self.soma(0.5).naf2_cc.gbar = 0.65
        self.soma(0.5).napf_spinstell.gbar = 0.0002
        self.soma(0.5).kdr_fs_cc.gbar = 0.1 * 10
        self.soma(0.5).kc_fast_cc.gbar = 0.001 * 10
        self.soma(0.5).ka_cc.gbar = 0.03
        self.soma(0.5).km_cc.gbar = 0.00375
        self.soma(0.5).k2_cc.gbar = 0.0001
        self.soma(0.5).kahp_slower.gbar = 0.0001
        self.soma(0.5).cal_cc.gbar = 0.0005
        self.soma(0.5).cat_cc.gbar = 0.0001
        self.soma(0.5).ar.gbar = 0.00025
        self.soma(0.5).cad_cc.beta = 0.02
        self.soma(0.5).cad_cc.phi = 260000.
        self.soma(0.5).pas.g = 0.001
        self.soma(0.5).pas.e = -65
        self.soma.Ra = 150.

        # ---------------dend----------------
        for mechanism_d in ['naf2_cc', 'napf_spinstell', 'pas', 'kdr_fs_cc', 'kc_fast_cc', 'ka_cc', 'km_cc', 'k2_cc',
                            'kahp_slower', 'cal_cc', 'cat_cc', 'ar', 'cad_cc']:
            self.dend.insert(mechanism_d)
            self.dend1.insert(mechanism_d)
            self.dend2.insert(mechanism_d)
            self.dend3.insert(mechanism_d)
            self.dend4.insert(mechanism_d)
            # print(mechanism_d)

        self.dend(0.5).naf2_cc.gbar = 0.0075
        self.dend(0.5).napf_spinstell.gbar = 7.5E-05 / 100
        self.dend(0.5).kdr_fs_cc.gbar = 0.0075
        self.dend(0.5).kc_fast_cc.gbar = 0.01
        self.dend(0.5).ka_cc.gbar = 0.03
        self.dend(0.5).km_cc.gbar = 0.00375
        self.dend(0.5).k2_cc.gbar = 0.0001
        self.dend(0.5).kahp_slower.gbar = 0.0001
        self.dend(0.5).cal_cc.gbar = 0.0005
        self.dend(0.5).cat_cc.gbar = 0.0001
        self.dend(0.5).ar.gbar = 0.00025
        self.dend(0.5).cad_cc.beta = 0.05
        self.dend(0.5).cad_cc.phi = 260000.
        self.dend(0.5).pas.g = 0.02
        self.dend(0.5).pas.e = -65
        self.dend.Ra = 250.

        self.dend1(0.5).naf2_cc.gbar = 0.0075
        self.dend1(0.5).napf_spinstell.gbar = 7.5E-05 / 100
        self.dend1(0.5).kdr_fs_cc.gbar = 0.0075
        self.dend1(0.5).kc_fast_cc.gbar = 0.01
        self.dend1(0.5).ka_cc.gbar = 0.03
        self.dend1(0.5).km_cc.gbar = 0.00375
        self.dend1(0.5).k2_cc.gbar = 0.0001
        self.dend1(0.5).kahp_slower.gbar = 0.0001
        self.dend1(0.5).cal_cc.gbar = 0.0005
        self.dend1(0.5).cat_cc.gbar = 0.0001
        self.dend1(0.5).ar.gbar = 0.00025
        self.dend1(0.5).cad_cc.beta = 0.05
        self.dend1(0.5).cad_cc.phi = 260000.
        self.dend1(0.5).pas.g = 0.02
        self.dend1(0.5).pas.e = -65
        self.dend1.Ra = 250.

        self.dend2(0.5).naf2_cc.gbar = 0.0075
        self.dend2(0.5).napf_spinstell.gbar = 7.5E-05 / 100
        self.dend2(0.5).kdr_fs_cc.gbar = 0.0075
        self.dend2(0.5).kc_fast_cc.gbar = 0.01
        self.dend2(0.5).ka_cc.gbar = 0.03
        self.dend2(0.5).km_cc.gbar = 0.00375
        self.dend2(0.5).k2_cc.gbar = 0.0001
        self.dend2(0.5).kahp_slower.gbar = 0.0001
        self.dend2(0.5).cal_cc.gbar = 0.0005
        self.dend2(0.5).cat_cc.gbar = 0.0001
        self.dend2(0.5).ar.gbar = 0.00025
        self.dend2(0.5).cad_cc.beta = 0.05
        self.dend2(0.5).cad_cc.phi = 260000.
        self.dend2(0.5).pas.g = 0.02
        self.dend2(0.5).pas.e = -65
        self.dend2.Ra = 250.

        self.dend3(0.5).naf2_cc.gbar = 0.0075
        self.dend3(0.5).napf_spinstell.gbar = 7.5E-05 / 100
        self.dend3(0.5).kdr_fs_cc.gbar = 0.0075
        self.dend3(0.5).kc_fast_cc.gbar = 0.01
        self.dend3(0.5).ka_cc.gbar = 0.03
        self.dend3(0.5).km_cc.gbar = 0.00375
        self.dend3(0.5).k2_cc.gbar = 0.0001
        self.dend3(0.5).kahp_slower.gbar = 0.0001
        self.dend3(0.5).cal_cc.gbar = 0.0005
        self.dend3(0.5).cat_cc.gbar = 0.0001
        self.dend3(0.5).ar.gbar = 0.00025
        self.dend3(0.5).cad_cc.beta = 0.05
        self.dend3(0.5).cad_cc.phi = 260000.
        self.dend3(0.5).pas.g = 0.02
        self.dend3(0.5).pas.e = -65
        self.dend3.Ra = 250.

        self.dend4(0.5).naf2_cc.gbar = 0.0075
        self.dend4(0.5).napf_spinstell.gbar = 7.5E-05 / 100
        self.dend4(0.5).kdr_fs_cc.gbar = 0.0075
        self.dend4(0.5).kc_fast_cc.gbar = 0.01
        self.dend4(0.5).ka_cc.gbar = 0.03
        self.dend4(0.5).km_cc.gbar = 0.00375
        self.dend4(0.5).k2_cc.gbar = 0.0001
        self.dend4(0.5).kahp_slower.gbar = 0.0001
        self.dend4(0.5).cal_cc.gbar = 0.0005
        self.dend4(0.5).cat_cc.gbar = 0.0001
        self.dend4(0.5).ar.gbar = 0.00025
        self.dend4(0.5).cad_cc.beta = 0.05
        self.dend4(0.5).cad_cc.phi = 260000.
        self.dend4(0.5).pas.g = 0.02
        self.dend4(0.5).pas.e = -65
        self.dend4.Ra = 250.

        # self.vd1 = h.Vector().record(self.dend(0.5)._ref_ina_naf2)
        # self.vd2 = h.Vector().record(self.dend(0.5)._ref_ina_napf_spinstell)
        # self.vd3 = h.Vector().record(self.dend(0.5)._ref_ik_kdr_fs)
        # self.vd4 = h.Vector().record(self.dend(0.5)._ref_ik_ka)
        # self.vd5 = h.Vector().record(self.dend(0.5)._ref_ik_kc_fast)
        # self.vd7 = h.Vector().record(self.dend(0.5)._ref_ik_k2)
        # self.vd8 = h.Vector().record(self.dend(0.5)._ref_ik_kahp_slower)
        # self.vd9 = h.Vector().record(self.dend(0.5)._ref_ica_cal)

        # ---------------axon----------------
        for mechanism_a in ['naf2_cc', 'kdr_fs_cc', 'ka_cc', 'k2_cc', 'pas']:
            self.axon.insert(mechanism_a)
            # print(mechanism_a)

        self.axon(0.5).naf2_cc.gbar = 0.1 * 4
        self.axon(0.5).kdr_fs_cc.gbar = 0.9
        self.axon(0.5).ka_cc.gbar = 0.002
        self.axon(0.5).k2_cc.gbar = 0.1
        self.axon(0.5).pas.g = 0.01
        self.axon(0.5).pas.e = -65
        self.axon.Ra = 100.

        for sec in self.all:
            sec.cm = 0.9
            sec.ena = 50.
            sec.ek = -90

        # self.dend1(0.5).Nafin.gnafbar = 0.00018 * 10
        # self.dend1(0.5).kdrin.gkdrbar = 0.00018 * 0.5
        # self.dend1(0.5).kapin.gkabar = 0.000032 #* 15 * 10
        # self.dend1(0.5).pas.g = 1 / 100
        # self.dend1(0.5).pas.e = -73
        # self.dend1.Ra = 150
        # self.dend1(0.5).nap.gnapbar = 0.000018
        #
        # self.dend2(0.5).Nafin.gnafbar = 0.00018 * 10
        # self.dend2(0.5).kdrin.gkdrbar = 0.00018 * 0.5
        # self.dend2(0.5).kapin.gkabar = 0.000032 #* 15 * 10
        # self.dend2(0.5).pas.g = 1 / 100
        # self.dend2(0.5).pas.e = -73
        # self.dend2.Ra = 150
        # self.dend2(0.5).nap.gnapbar = 0.000018
        #
        # self.dend3(0.5).Nafin.gnafbar = 0.0018 * 10
        # self.dend3(0.5).kdrin.gkdrbar = 0.00018 * 0.5
        # self.dend3(0.5).kapin.gkabar = 0.000032 #* 15 * 10
        # self.dend3(0.5).pas.g = 1 / 100
        # self.dend3(0.5).pas.e = -73
        # self.dend3.Ra = 150
        # self.dend3(0.5).nap.gnapbar = 0.000018
        #
        # self.dend4(0.5).Nafin.gnafbar = 0.0018 * 10
        # self.dend4(0.5).kdrin.gkdrbar = 0.0018 * 0.5
        # self.dend4(0.5).kapin.gkabar = 0.000032 #* 15 * 10
        # self.dend4(0.5).pas.g = 1 / 100
        # self.dend4(0.5).pas.e = -73
        # self.dend4.Ra = 150
        # self.dend4(0.5).nap.gnapbar = 0.000018

        # ---------------axon----------------

        self.k_vec = h.Vector().record(self.soma(0.5)._ref_ik)
        self.na_vec = h.Vector().record(self.soma(0.5)._ref_ina)
        self.na_concentration = h.Vector().record(self.soma(0.5)._ref_nai)
        self.k_concentration = h.Vector().record(self.soma(0.5)._ref_ki)
        self.v_vec = h.Vector().record(self.soma(0.5)._ref_v)

        # self.cyt = rxd.Region(self.all, name='cyt', nrn_region='i', dx=1.0,
        #                       geometry=rxd.FractionalVolume(0.9, surface_fraction=1.0))
        # self.na = rxd.Species([self.cyt], name='na', charge=1, d=1.0, initial=10)
        # self.k = rxd.Species([self.cyt], name='k', charge=1, d=1.0, initial=148)
        # self.k_i = self.k[self.cyt]
        # self.ca = rxd.Species([self.cyt], d=0.08, name='ca', charge=2, initial=1.e-4, atolscale=1e-6)

        # ------for test-----------
        # self.stim = h.IClamp(self.soma(0.5))
        # self.stim.delay = 50
        # self.stim.dur = 1
        # self.stim.amp = 1
        # print(self.id)


class TuftRS5(Cell):  #
    def __init__(self, x, y, z, num):
        super().__init__(x, y, z, num)
        self.id = 6
        self.Excitatory = 1
        self.name = 'L56 pyramidal tufted regular spiking'

        for mechanism_s in ['extracellular', 'Naf',
                            'pas', 'nap',
                            'kdr', 'kc',
                            'ka_cc', 'km_cc', 'k2_cc',
                            'kahp_deeppyr',
                            'cal_cc', 'cat_a', 'ar',
                            'cad_cc']:
            self.soma.insert(mechanism_s)

        self.soma(0.5).Naf.gnafbar = 0.2
        self.soma(0.5).nap.gnapbar = 0.0008 * 0.2
        self.soma(0.5).kdr.gkdrbar = 0.17
        self.soma(0.5).ka_cc.gbar = 0.02  # 0.005
        self.soma(0.5).km_cc.gbar = 0.0085  # 0.0005
        self.soma(0.5).kc.gbar = 0.008 * 3.6  # 0.01
        self.soma(0.5).k2_cc.gbar = 0.0005
        self.soma(0.5).kahp_deeppyr.gbar = 0.0002  # 0.0001
        self.soma(0.5).cal_cc.gbar = 0.004 * 0.4  # 0.0001
        self.soma(0.5).cat_a.gbar = 0.0001  # 5.E-05
        self.soma(0.5).ar.gbar = 0.0001  # 2.5E-05
        self.soma(0.5).cad_cc.beta = 0.01  # 0.02
        self.soma(0.5).cad_cc.phi = 4333.33333  # 10400.
        self.soma(0.5).pas.e = -70
        self.soma(0.5).pas.g = 0.001
        self.soma.Ra = 250.  # 100.

        for mechanism_d in ['Naf',
                            'nap',
                            'kdr_thlms', 'ka', 'kc',
                            'km', 'k2', 'kahp_deeppyr',
                            'cal_thlms',
                            'cat_a', 'ar', 'cad', 'pas']:
            self.dend.insert(mechanism_d)
            self.dend1.insert(mechanism_d)
            self.dend2.insert(mechanism_d)
            self.dend3.insert(mechanism_d)
            self.dend4.insert(mechanism_d)

        self.dend(0.5).Naf.gnafbar = 0.075
        self.dend(0.5).nap.gnapbar = 0.0003 * 0.2
        self.dend(0.5).kdr_thlms.gbar = 0.075  # 0.075
        self.dend(0.5).kc.gbar = 0.008 * 3.6  # 0.012
        self.dend(0.5).ka.gbar = 0.008  # 0.03
        self.dend(0.5).km.gbar = 0.0136  # 0 #// 0.0005
        self.dend(0.5).k2.gbar = 0.0005  # 0.002
        self.dend(0.5).kahp_deeppyr.gbar = 0.0002
        self.dend(0.5).cal_thlms.gbar = 0.004 * 0.4  # 0.0005
        self.dend(0.5).cat_a.gbar = 0.0001  # 0.0005
        self.dend(0.5).ar.gbar = 0.0001  # 0.00025
        self.dend(0.5).cad.beta = 0.02
        self.dend(0.5).cad.phi = 86666.6667  # 52000.
        self.dend(0.5).pas.g = 1 / 100
        self.dend(0.5).pas.e = -70
        self.dend.Ra = 250  # 175

        self.dend1(0.5).Naf.gnafbar = 0.015
        self.dend1(0.5).nap.gnapbar = 6.E-05
        self.dend1(0.5).kc.gbar = 0.00025 * 3.6  # 0.012
        self.dend1(0.5).ka.gbar = 0.0006  # 0.03
        self.dend1(0.5).km.gbar = 0.0136  # 0  # // 0.0005
        self.dend1(0.5).k2.gbar = 0.0005  # 0.002
        self.dend1(0.5).kahp_deeppyr.gbar = 0.0002
        self.dend1(0.5).cal_thlms.gbar = 0.004 * 0.4  # 0.0005
        self.dend1(0.5).cat_a.gbar = 0.0001  # 0.0005
        self.dend1(0.5).ar.gbar = 0.0001  # 0.00025
        self.dend1(0.5).cad.beta = 0.075  # 0.02
        self.dend1(0.5).cad.phi = 86666.6667  # 52000.
        self.dend1(0.5).pas.g = 1 / 100
        self.dend1(0.5).pas.e = -70
        self.dend1.Ra = 250  # 175

        self.dend2(0.5).Naf.gnafbar = 0.015
        self.dend2(0.5).nap.gnapbar = 6.E-05
        self.dend2(0.5).kc.gbar = 0.00025 * 3.6  # 0.012
        self.dend2(0.5).ka.gbar = 0.0006  # 0.03
        self.dend2(0.5).km.gbar = 0.0136  # 0  # // 0.0005
        self.dend2(0.5).k2.gbar = 0.0005  # 0.002
        self.dend2(0.5).cal_thlms.gbar = 0.004 * 0.4  # 0.0005
        self.dend2(0.5).cat_a.gbar = 0.0001  # 0.0005
        self.dend2(0.5).kahp_deeppyr.gbar = 0.0002
        self.dend2(0.5).ar.gbar = 0.0001  # 0.00025
        self.dend2(0.5).cad.beta = 0.075  # 0.02
        self.dend2(0.5).cad.phi = 86666.6667  # 52000.
        self.dend2(0.5).pas.g = 1 / 100
        self.dend2(0.5).pas.e = -70
        self.dend2.Ra = 250  # 175

        self.dend3(0.5).Naf.gnafbar = 0.015
        self.dend3(0.5).nap.gnapbar = 0.0006 * 0.2
        self.dend3(0.5).kdr_thlms.gbar = 0.12
        self.dend3(0.5).kc.gbar = 0.008 * 3.6  # 0.012
        self.dend3(0.5).ka.gbar = 0.008  # 0.03
        self.dend3(0.5).km.gbar = 0  # // 0.0005
        self.dend3(0.5).k2.gbar = 0.0005  # 0.002
        self.dend3(0.5).cal_thlms.gbar = 0.004 * 0.4  # 0.0005
        self.dend3(0.5).cat_a.gbar = 0.0001  # 0.0005
        self.dend3(0.5).kahp_deeppyr.gbar = 0.0002
        self.dend3(0.5).ar.gbar = 0.0001  # 0.00025
        self.dend3(0.5).cad.beta = 0.075  # 0.02
        self.dend3(0.5).cad.phi = 86666.6667  # 52000.
        self.dend3(0.5).pas.g = 1 / 100
        self.dend3(0.5).pas.e = -70
        self.dend3.Ra = 250  # 175

        self.dend3(0.5).Naf.gnafbar = 0.075
        self.dend3(0.5).nap.gnapbar = 0.0003 * 0.2
        self.dend3(0.5).kdr_thlms.gbar = 0.075
        self.dend4(0.5).kc.gbar = 0.008 * 3.6  # 0.012
        self.dend4(0.5).ka.gbar = 0.008  # 0.03
        self.dend4(0.5).km.gbar = 0.0136  # 0  # // 0.0005
        self.dend4(0.5).k2.gbar = 0.0005  # 0.002
        self.dend4(0.5).cal_thlms.gbar = 0.004 * 0.4  # 0.0005
        self.dend4(0.5).cat_a.gbar = 0.0001  # 0.0005
        self.dend4(0.5).kahp_deeppyr.gbar = 0.0002
        self.dend4(0.5).ar.gbar = 0.0001  # 0.00025
        self.dend4(0.5).cad.beta = 0.075  # 0.02
        self.dend4(0.5).cad.phi = 86666.6667  # 52000.
        self.dend4(0.5).pas.g = 1 / 100
        self.dend4(0.5).pas.e = -70
        self.dend4.Ra = 250  # 175

        # ---------------axon----------------
        for mechanism_a in ['Nafin', 'kdrin',
                            'pas']:
            self.axon.insert(mechanism_a)

        self.axon(0.5).Nafin.gnafbar = 0.45  # 0.4
        self.axon(0.5).kdrin.gkdrbar = 0.45  # 0.001
        self.axon(0.5).pas.g = 0.001  # 0.005
        self.axon(0.5).pas.e = -70
        self.axon.Ra = 100.
        self.axon.cm = 1.2

        for sec in self.all:
            sec.cm = 0.9
            sec.ena = 50.
            sec.ek = -95

        self.k_vec = h.Vector().record(self.soma(0.5)._ref_ik)
        self.na_vec = h.Vector().record(self.soma(0.5)._ref_ina)
        self.na_concentration = h.Vector().record(self.soma(0.5)._ref_nai)
        self.k_concentration = h.Vector().record(self.soma(0.5)._ref_ki)
        self.v_vec = h.Vector().record(self.soma(0.5)._ref_v)


class EpilepsyTuftRS5(Cell):  #
    def __init__(self, x, y, z, num):
        super().__init__(x, y, z, num)
        self.id = 6
        self.Excitatory = 1
        self.name = 'pyramidal tufted regular spiking'

        # ---------------soma----------------
        for mechanism_s in ['extracellular', 'naf2_cc', 'pas', 'napf_spinstell', 'kdr_fs_cc', 'kc_fast_cc', 'ka_cc',
                            'km_cc', 'k2_cc', 'kahp_slower', 'cal_cc', 'cat_cc', 'ar', 'cad_cc']:
            self.soma.insert(mechanism_s)
        # print(mechanism_s)

        self.soma(0.5).naf2_cc.gbar = 0.65
        self.soma(0.5).napf_spinstell.gbar = 0.0002
        self.soma(0.5).kdr_fs_cc.gbar = 0.1 * 10
        self.soma(0.5).kc_fast_cc.gbar = 0.001 * 10
        self.soma(0.5).ka_cc.gbar = 0.03
        self.soma(0.5).km_cc.gbar = 0.00375
        self.soma(0.5).k2_cc.gbar = 0.0001
        self.soma(0.5).kahp_slower.gbar = 0.0001
        self.soma(0.5).cal_cc.gbar = 0.0005
        self.soma(0.5).cat_cc.gbar = 0.0001
        self.soma(0.5).ar.gbar = 0.00025
        self.soma(0.5).cad_cc.beta = 0.02
        self.soma(0.5).cad_cc.phi = 260000.
        self.soma(0.5).pas.g = 0.001
        self.soma(0.5).pas.e = -65
        self.soma.Ra = 150.

        # ---------------dend----------------
        for mechanism_d in ['naf2_cc', 'napf_spinstell', 'pas', 'kdr_fs_cc', 'kc_fast_cc', 'ka_cc', 'km_cc', 'k2_cc',
                            'kahp_slower', 'cal_cc', 'cat_cc', 'ar', 'cad_cc']:
            self.dend.insert(mechanism_d)
            self.dend1.insert(mechanism_d)
            self.dend2.insert(mechanism_d)
            self.dend3.insert(mechanism_d)
            self.dend4.insert(mechanism_d)
            # print(mechanism_d)

        self.dend(0.5).naf2_cc.gbar = 0.0075
        self.dend(0.5).napf_spinstell.gbar = 7.5E-05 / 100
        self.dend(0.5).kdr_fs_cc.gbar = 0.0075
        self.dend(0.5).kc_fast_cc.gbar = 0.01
        self.dend(0.5).ka_cc.gbar = 0.03
        self.dend(0.5).km_cc.gbar = 0.00375
        self.dend(0.5).k2_cc.gbar = 0.0001
        self.dend(0.5).kahp_slower.gbar = 0.0001
        self.dend(0.5).cal_cc.gbar = 0.0005
        self.dend(0.5).cat_cc.gbar = 0.0001
        self.dend(0.5).ar.gbar = 0.00025
        self.dend(0.5).cad_cc.beta = 0.05
        self.dend(0.5).cad_cc.phi = 260000.
        self.dend(0.5).pas.g = 0.02
        self.dend(0.5).pas.e = -65
        self.dend.Ra = 250.

        self.dend1(0.5).naf2_cc.gbar = 0.0075
        self.dend1(0.5).napf_spinstell.gbar = 7.5E-05 / 100
        self.dend1(0.5).kdr_fs_cc.gbar = 0.0075
        self.dend1(0.5).kc_fast_cc.gbar = 0.01
        self.dend1(0.5).ka_cc.gbar = 0.03
        self.dend1(0.5).km_cc.gbar = 0.00375
        self.dend1(0.5).k2_cc.gbar = 0.0001
        self.dend1(0.5).kahp_slower.gbar = 0.0001
        self.dend1(0.5).cal_cc.gbar = 0.0005
        self.dend1(0.5).cat_cc.gbar = 0.0001
        self.dend1(0.5).ar.gbar = 0.00025
        self.dend1(0.5).cad_cc.beta = 0.05
        self.dend1(0.5).cad_cc.phi = 260000.
        self.dend1(0.5).pas.g = 0.02
        self.dend1(0.5).pas.e = -65
        self.dend1.Ra = 250.

        self.dend2(0.5).naf2_cc.gbar = 0.0075
        self.dend2(0.5).napf_spinstell.gbar = 7.5E-05 / 100
        self.dend2(0.5).kdr_fs_cc.gbar = 0.0075
        self.dend2(0.5).kc_fast_cc.gbar = 0.01
        self.dend2(0.5).ka_cc.gbar = 0.03
        self.dend2(0.5).km_cc.gbar = 0.00375
        self.dend2(0.5).k2_cc.gbar = 0.0001
        self.dend2(0.5).kahp_slower.gbar = 0.0001
        self.dend2(0.5).cal_cc.gbar = 0.0005
        self.dend2(0.5).cat_cc.gbar = 0.0001
        self.dend2(0.5).ar.gbar = 0.00025
        self.dend2(0.5).cad_cc.beta = 0.05
        self.dend2(0.5).cad_cc.phi = 260000.
        self.dend2(0.5).pas.g = 0.02
        self.dend2(0.5).pas.e = -65
        self.dend2.Ra = 250.

        self.dend3(0.5).naf2_cc.gbar = 0.0075
        self.dend3(0.5).napf_spinstell.gbar = 7.5E-05 / 100
        self.dend3(0.5).kdr_fs_cc.gbar = 0.0075
        self.dend3(0.5).kc_fast_cc.gbar = 0.01
        self.dend3(0.5).ka_cc.gbar = 0.03
        self.dend3(0.5).km_cc.gbar = 0.00375
        self.dend3(0.5).k2_cc.gbar = 0.0001
        self.dend3(0.5).kahp_slower.gbar = 0.0001
        self.dend3(0.5).cal_cc.gbar = 0.0005
        self.dend3(0.5).cat_cc.gbar = 0.0001
        self.dend3(0.5).ar.gbar = 0.00025
        self.dend3(0.5).cad_cc.beta = 0.05
        self.dend3(0.5).cad_cc.phi = 260000.
        self.dend3(0.5).pas.g = 0.02
        self.dend3(0.5).pas.e = -65
        self.dend3.Ra = 250.

        self.dend4(0.5).naf2_cc.gbar = 0.0075
        self.dend4(0.5).napf_spinstell.gbar = 7.5E-05 / 100
        self.dend4(0.5).kdr_fs_cc.gbar = 0.0075
        self.dend4(0.5).kc_fast_cc.gbar = 0.01
        self.dend4(0.5).ka_cc.gbar = 0.03
        self.dend4(0.5).km_cc.gbar = 0.00375
        self.dend4(0.5).k2_cc.gbar = 0.0001
        self.dend4(0.5).kahp_slower.gbar = 0.0001
        self.dend4(0.5).cal_cc.gbar = 0.0005
        self.dend4(0.5).cat_cc.gbar = 0.0001
        self.dend4(0.5).ar.gbar = 0.00025
        self.dend4(0.5).cad_cc.beta = 0.05
        self.dend4(0.5).cad_cc.phi = 260000.
        self.dend4(0.5).pas.g = 0.02
        self.dend4(0.5).pas.e = -65
        self.dend4.Ra = 250.

        # self.vd1 = h.Vector().record(self.dend(0.5)._ref_ina_naf2)
        # self.vd2 = h.Vector().record(self.dend(0.5)._ref_ina_napf_spinstell)
        # self.vd3 = h.Vector().record(self.dend(0.5)._ref_ik_kdr_fs)
        # self.vd4 = h.Vector().record(self.dend(0.5)._ref_ik_ka)
        # self.vd5 = h.Vector().record(self.dend(0.5)._ref_ik_kc_fast)
        # self.vd7 = h.Vector().record(self.dend(0.5)._ref_ik_k2)
        # self.vd8 = h.Vector().record(self.dend(0.5)._ref_ik_kahp_slower)
        # self.vd9 = h.Vector().record(self.dend(0.5)._ref_ica_cal)

        # ---------------axon----------------
        for mechanism_a in ['naf2_cc', 'kdr_fs_cc', 'ka_cc', 'k2_cc', 'pas']:
            self.axon.insert(mechanism_a)
            # print(mechanism_a)

        self.axon(0.5).naf2_cc.gbar = 0.1 * 4
        self.axon(0.5).kdr_fs_cc.gbar = 0.9
        self.axon(0.5).ka_cc.gbar = 0.002
        self.axon(0.5).k2_cc.gbar = 0.1
        self.axon(0.5).pas.g = 0.01
        self.axon(0.5).pas.e = -65
        self.axon.Ra = 100.

        for sec in self.all:
            sec.cm = 0.9
            sec.ena = 50.
            sec.ek = -90

        self.k_vec = h.Vector().record(self.soma(0.5)._ref_ik)
        self.na_vec = h.Vector().record(self.soma(0.5)._ref_ina)
        self.na_concentration = h.Vector().record(self.soma(0.5)._ref_nai)
        self.k_concentration = h.Vector().record(self.soma(0.5)._ref_ki)
        self.v_vec = h.Vector().record(self.soma(0.5)._ref_v)

        # self.cyt = rxd.Region(self.all, name='cyt', nrn_region='i', dx=1.0,
        #                       geometry=rxd.FractionalVolume(0.9, surface_fraction=1.0))
        # self.na = rxd.Species([self.cyt], name='na', charge=1, d=1.0, initial=10)
        # self.k = rxd.Species([self.cyt], name='k', charge=1, d=1.0, initial=148)
        # self.k_i = self.k[self.cyt]
        # self.ca = rxd.Species([self.cyt], d=0.08, name='ca', charge=2, initial=1.e-4, atolscale=1e-6)

        # ------for test-----------
        # self.stim = h.IClamp(self.soma(0.5))
        # self.stim.delay = 50
        # self.stim.dur = 1
        # self.stim.amp = 1
        # print(self.id)


class Bask56(Cell):
    def __init__(self, x, y, z, num):
        super().__init__(x, y, z, num)
        self.id = 7
        self.Excitatory = -1
        self.name = 'L56 deep interneurons basket'

        # ---------------soma----------------
        for mechanism_s in ['extracellular', 'Nafin',
                            'kdrin',
                            # 'IKsin', 'hin',
                            'kapin', 'canin', 'kctin',
                            'cadynin',
                            'nap',
                            'pas']:
            self.soma.insert(mechanism_s)

        self.soma(0.5).Nafin.gnafbar = 0.06  # 0.45
        self.soma(0.5).nap.gnapbar = 0.0006  # 0.000018
        self.soma(0.5).kdrin.gkdrbar = 0.1  # 0.001
        self.soma(0.5).kapin.gkabar = 0.001  # 0.0032 * 15
        self.soma(0.5).canin.gcalbar = 0.0003
        self.soma(0.5).kctin.gkcbar = 0.025  # 0.0001
        self.soma(0.5).pas.g = 0.001
        self.soma(0.5).pas.e = -65  # -70
        self.soma.Ra = 200.  # 100

        # ---------------dend----------------
        for mechanism_d in ['Nafin', 'kdrin', 'kapin', 'pas', 'nap']:
            self.dend.insert(mechanism_d)
            self.dend1.insert(mechanism_d)
            self.dend2.insert(mechanism_d)
            self.dend3.insert(mechanism_d)
            self.dend4.insert(mechanism_d)

        self.dend(0.5).Nafin.gnafbar = 0.06  # 0.018 * 10
        self.dend(0.5).kdrin.gkdrbar = 0.1  # 0.018
        self.dend(0.5).kapin.gkabar = 0.001  # 0.000032  # * 15 * 10
        self.dend(0.5).nap.gnapbar = 0.0006  # 0.000018
        self.dend(0.5).pas.g = 0.01
        self.dend(0.5).pas.e = -65  # -73
        self.dend.Ra = 200  # 150

        self.dend1(0.5).Nafin.gnafbar = 0.06  # 0.018 * 10
        self.dend1(0.5).kdrin.gkdrbar = 0.1  # 0.018 * 0.5
        self.dend1(0.5).kapin.gkabar = 0.001  # 0.000032  # * 15 * 10
        self.dend1(0.5).pas.g = 0.01
        self.dend1(0.5).pas.e = -65  # -73
        self.dend1.Ra = 200  # 150
        self.dend1(0.5).nap.gnapbar = 0.0006  # 0.000018

        self.dend2(0.5).Nafin.gnafbar = 0.06  # 0.018 * 10
        self.dend2(0.5).kdrin.gkdrbar = 0.01  # 0.018 * 0.5
        self.dend2(0.5).kapin.gkabar = 0.001  # 0.000032  # * 15 * 10
        self.dend2(0.5).pas.g = 0.01
        self.dend2(0.5).pas.e = -65  # -73
        self.dend2.Ra = 200  # 150
        self.dend2(0.5).nap.gnapbar = 0.0001  # 0.000018

        self.dend3(0.5).Nafin.gnafbar = 0.01  # 0.018 * 10
        self.dend3(0.5).kdrin.gkdrbar = 0.01  # 0.018 * 0.5
        self.dend3(0.5).kapin.gkabar = 0.001  # 0.000032  # * 15 * 10
        self.dend3(0.5).pas.g = 0.01
        self.dend3(0.5).pas.e = -65  # -73
        self.dend3.Ra = 200  # 150
        self.dend3(0.5).nap.gnapbar = 0.0001  # 0.000018

        self.dend4(0.5).Nafin.gnafbar = 0.01  # 0.018 * 10
        self.dend4(0.5).kdrin.gkdrbar = 0.01  # 0.018 * 0.5
        self.dend4(0.5).kapin.gkabar = 0.001  # 0.000032  # * 15 * 10
        self.dend4(0.5).pas.g = 0.01
        self.dend4(0.5).pas.e = -65  # -73
        self.dend4.Ra = 200  # 150
        self.dend4(0.5).nap.gnapbar = 0.0001  # 0.000018

        # ---------------axon----------------
        for mechanism_a in ['Nafin', 'kdrin',
                            'pas']:
            self.axon.insert(mechanism_a)

        self.axon(0.5).Nafin.gnafbar = 0.4
        self.axon(0.5).kdrin.gkdrbar = 0.4  # 0.001
        self.axon(0.5).pas.g = 0.01  # 0.0002
        self.axon(0.5).pas.e = -65  # -73
        self.axon.Ra = 100
        self.axon.cm = 1.2

        for sec in self.all:
            sec.cm = 1
            sec.ena = 50.
            sec.ek = -100.

        self.k_vec = h.Vector().record(self.soma(0.5)._ref_ik)
        self.na_vec = h.Vector().record(self.soma(0.5)._ref_ina)
        self.na_concentration = h.Vector().record(self.soma(0.5)._ref_nai)
        self.k_concentration = h.Vector().record(self.soma(0.5)._ref_ki)
        self.v_vec = h.Vector().record(self.soma(0.5)._ref_v)


class Axax56(Cell):  #
    def __init__(self, x, y, z, num):
        super().__init__(x, y, z, num)
        self.id = 8
        self.Excitatory = -1
        self.name = 'L56 deep interneurons axoaxonic'

        # ---------------soma----------------
        for mechanism_s in ['extracellular', 'naf2_cc',
                            'pas',
                            'napf_spinstell',
                            'kdr_fs_cc', 'kc_fast_cc',
                            'ka_cc',
                            'km_cc', 'k2_cc', 'kahp_slower', 'cat_cc', 'ar',
                            'cal_cc',
                            'cad_cc']:
            self.soma.insert(mechanism_s)

        self.soma(0.5).naf2_cc.gbar = 0.65
        self.soma(0.5).napf_spinstell.gbar = 0.0006  # 0.0002
        self.soma(0.5).kdr_fs_cc.gbar = 0.1  # 0.1 * 10
        self.soma(0.5).kc_fast_cc.gbar = 0.025 * 2  # 0.001 * 10
        self.soma(0.5).ka_cc.gbar = 0.03 * 2
        self.soma(0.5).km_cc.gbar = 0.0005 * 2  # 0.00375
        self.soma(0.5).k2_cc.gbar = 0.0005 * 2  # 0.0001
        self.soma(0.5).kahp_slower.gbar = 0.0001
        self.soma(0.5).cal_cc.gbar = 0.0001  # 0.0005
        self.soma(0.5).cat_cc.gbar = 5.E-05  # 0.0001
        self.soma(0.5).ar.gbar = 2.5E-05  # 0.00025
        self.soma(0.5).cad_cc.beta = 0.02
        self.soma(0.5).cad_cc.phi = 260000.
        self.soma(0.5).pas.g = 0.001
        self.soma(0.5).pas.e = -65
        self.soma.Ra = 200.  # 150.

        # ---------------dend----------------
        for mechanism_d in ['naf2_cc', 'napf_spinstell',
                            'pas', 'kdr_fs_cc', 'kc_fast_cc',
                            'ka_cc',
                            'km_cc', 'k2_cc',
                            'kahp_slower', 'cat_cc', 'ar',
                            'cal_cc', 'cad_cc']:
            self.dend.insert(mechanism_d)
            self.dend1.insert(mechanism_d)
            self.dend2.insert(mechanism_d)
            self.dend3.insert(mechanism_d)
            self.dend4.insert(mechanism_d)

        self.dend(0.5).naf2_cc.gbar = 0.06  # 0.0075
        self.dend(0.5).napf_spinstell.gbar = 0.0006  # 7.5E-05 / 100
        self.dend(0.5).kdr_fs_cc.gbar = 0.1  # 0.0075
        self.dend(0.5).kc_fast_cc.gbar = 0.025 * 2  # 0.01
        self.dend(0.5).ka_cc.gbar = 0.03 * 2
        self.dend(0.5).km_cc.gbar = 0.0005 * 2  # 0.00375
        self.dend(0.5).k2_cc.gbar = 0.0005 * 2  # 0.0001
        self.dend(0.5).kahp_slower.gbar = 0.0001
        self.dend(0.5).cal_cc.gbar = 0.0001  # 0.0005
        self.dend(0.5).cat_cc.gbar = 5E-05  # 0.0001
        self.dend(0.5).ar.gbar = 2.5E-05  # 0.00025
        self.dend(0.5).cad_cc.beta = 0.05
        self.dend(0.5).cad_cc.phi = 520000.  # 260000.
        self.dend(0.5).pas.g = 0.01
        self.dend(0.5).pas.e = -65
        self.dend.Ra = 200  # 250.

        self.dend1(0.5).naf2_cc.gbar = 0.06  # 0.0075
        self.dend1(0.5).napf_spinstell.gbar = 0.0006  # 7.5E-05 / 100
        self.dend1(0.5).kdr_fs_cc.gbar = 0.1  # 0.0075
        self.dend1(0.5).kc_fast_cc.gbar = 0.025 * 2  # 0.01
        self.dend1(0.5).ka_cc.gbar = 0.03 * 2
        self.dend1(0.5).km_cc.gbar = 0.0005 * 2  # 0.00375
        self.dend1(0.5).k2_cc.gbar = 0.0005 * 2  # 0.0001
        self.dend1(0.5).kahp_slower.gbar = 0.0001
        self.dend1(0.5).cal_cc.gbar = 0.0001  # 0.0005
        self.dend1(0.5).cat_cc.gbar = 5E-05  # 0.0001
        self.dend1(0.5).ar.gbar = 2.5E-05  # 0.00025
        self.dend1(0.5).cad_cc.beta = 0.05
        self.dend1(0.5).cad_cc.phi = 520000.  # 260000.
        self.dend1(0.5).pas.g = 0.01
        self.dend1(0.5).pas.e = -65
        self.dend1.Ra = 200  # 250.

        self.dend2(0.5).naf2_cc.gbar = 0.06  # 0.0075
        self.dend2(0.5).napf_spinstell.gbar = 0.0006  # 0.0001  # 7.5E-05 / 100
        self.dend2(0.5).kdr_fs_cc.gbar = 0.1  # 0.0075
        self.dend2(0.5).kc_fast_cc.gbar = 0.025 * 2  # 0.01
        self.dend2(0.5).ka_cc.gbar = 0.03 * 2
        self.dend2(0.5).km_cc.gbar = 0.0005 * 2  # 0.00375
        self.dend2(0.5).k2_cc.gbar = 0.0005 * 2  # 0.0001
        self.dend2(0.5).kahp_slower.gbar = 0.0001
        self.dend2(0.5).cal_cc.gbar = 0.0001  # 0.0005
        self.dend2(0.5).cat_cc.gbar = 5E-05  # 0.0001
        self.dend2(0.5).ar.gbar = 2.5E-05  # 0.00025
        self.dend2(0.5).cad_cc.beta = 0.05
        self.dend2(0.5).cad_cc.phi = 520000.  # 260000.
        self.dend2(0.5).pas.g = 0.01
        self.dend2(0.5).pas.e = -65
        self.dend2.Ra = 200  # 250.

        self.dend3(0.5).naf2_cc.gbar = 0.01  # 0.0075
        self.dend3(0.5).napf_spinstell.gbar = 0.0001  # 7.5E-05 / 100
        self.dend3(0.5).kdr_fs_cc.gbar = 0.01  # 0.0075
        self.dend3(0.5).kc_fast_cc.gbar = 0.025 * 2  # 0.01
        self.dend3(0.5).ka_cc.gbar = 0.03 * 2
        self.dend3(0.5).km_cc.gbar = 0.0005 * 2  # 0.00375
        self.dend3(0.5).k2_cc.gbar = 0.0005 * 2  # 0.0001
        self.dend3(0.5).kahp_slower.gbar = 0.0001
        self.dend3(0.5).cal_cc.gbar = 0.0002  # 0.0005
        self.dend3(0.5).cat_cc.gbar = 0.002  # 0.0001
        self.dend3(0.5).ar.gbar = 2.5E-05  # 0.00025
        self.dend3(0.5).cad_cc.beta = 0.05
        self.dend3(0.5).cad_cc.phi = 520000.  # 260000.
        self.dend3(0.5).pas.g = 0.01
        self.dend3(0.5).pas.e = -65
        self.dend3.Ra = 200  # 250.

        self.dend4(0.5).naf2_cc.gbar = 0.01  # 0.0075
        self.dend4(0.5).napf_spinstell.gbar = 0.0001  # 7.5E-05 / 100
        self.dend4(0.5).kdr_fs_cc.gbar = 0.01  # 0.0075
        self.dend4(0.5).kc_fast_cc.gbar = 0.025 * 2  # 0.01
        self.dend4(0.5).ka_cc.gbar = 0.03 * 2
        self.dend4(0.5).km_cc.gbar = 0.0005 * 2  # 0.00375
        self.dend4(0.5).k2_cc.gbar = 0.0005 * 2  # 0.0001
        self.dend4(0.5).kahp_slower.gbar = 0.0001
        self.dend4(0.5).cal_cc.gbar = 0.0002  # 0.0005
        self.dend4(0.5).cat_cc.gbar = 0.002  # 0.0001
        self.dend4(0.5).ar.gbar = 2.5E-05  # 0.00025
        self.dend4(0.5).cad_cc.beta = 0.05
        self.dend4(0.5).cad_cc.phi = 520000.  # 260000.
        self.dend4(0.5).pas.g = 0.01
        self.dend4(0.5).pas.e = -65
        self.dend4.Ra = 200  # 250.

        # ---------------axon----------------
        for mechanism_a in ['Nafin', 'kdrin', 'pas']:
            self.axon.insert(mechanism_a)

        self.axon(0.5).Nafin.gnafbar = 0.1 * 4
        self.axon(0.5).kdrin.gkdrbar = 0.45  # 0.9
        self.axon(0.5).pas.g = 0.01
        self.axon(0.5).pas.e = -65
        self.axon.Ra = 100.

        for sec in self.all:
            sec.cm = 1.  # 0.9
            sec.ena = 50.
            sec.ek = -100

        self.k_vec = h.Vector().record(self.soma(0.5)._ref_ik)
        self.na_vec = h.Vector().record(self.soma(0.5)._ref_ina)
        self.na_concentration = h.Vector().record(self.soma(0.5)._ref_nai)
        self.k_concentration = h.Vector().record(self.soma(0.5)._ref_ki)
        self.v_vec = h.Vector().record(self.soma(0.5)._ref_v)


class LTS56(Cell):  #
    def __init__(self, x, y, z, num):
        super().__init__(x, y, z, num)
        self.id = 9
        self.Excitatory = -1
        self.name = 'L56 deep interneurons low threshold spiking'

        # ---------------soma----------------
        for mechanism_s in ['extracellular', 'Nafin',
                            'kdrin',
                            # 'IKsin', 'hin',
                            'kapin',
                            'canin', 'kctin', 'cadynin',
                            'pas']:
            self.soma.insert(mechanism_s)

        self.soma(0.5).Nafin.gnafbar = 0.06  # 0.25
        self.soma(0.5).kdrin.gkdrbar = 0.1  # 0.001
        self.soma(0.5).kapin.gkabar = 0.001  # 0.0032 * 15
        self.soma(0.5).canin.gcalbar = 0.0001  # 0.0003
        self.soma(0.5).kctin.gkcbar = 0.025  # 0.0001
        self.soma(0.5).pas.g = 0.001  # 0.0002
        self.soma(0.5).pas.e = -65  # -70
        self.soma.Ra = 200

        # ---------------dend----------------
        for mechanism_d in ['Nafin', 'kdrin', 'kapin', 'pas', 'nap']:
            self.dend.insert(mechanism_d)
            self.dend1.insert(mechanism_d)
            self.dend2.insert(mechanism_d)
            self.dend3.insert(mechanism_d)
            self.dend4.insert(mechanism_d)

        self.dend(0.5).Nafin.gnafbar = 0.06  # 0.018 * 10
        self.dend(0.5).kdrin.gkdrbar = 0.1 * 2  # 0.018
        self.dend(0.5).kapin.gkabar = 0.001 * 2  # 0.000032  # * 15 * 10
        self.dend(0.5).nap.gnapbar = 0.0006  # 0.000018
        self.dend(0.5).pas.g = 1 / 100
        self.dend(0.5).pas.e = -65  # -73
        self.dend.Ra = 200  # 150

        self.dend1(0.5).Nafin.gnafbar = 0.06  # 0.018 * 5
        self.dend1(0.5).kdrin.gkdrbar = 0.1 * 2  # 0.018 * 0.5
        self.dend1(0.5).kapin.gkabar = 0.001 * 2  # 0.000032  # * 15 * 10
        self.dend1(0.5).pas.g = 1 / 100
        self.dend1(0.5).pas.e = -65  # -73
        self.dend1.Ra = 200  # 150
        self.dend1(0.5).nap.gnapbar = 0.0006  # 0.000018

        self.dend2(0.5).Nafin.gnafbar = 0.01  # 0.018 * 5
        self.dend2(0.5).kdrin.gkdrbar = 0.01 * 2  # 0.018 * 0.5
        self.dend2(0.5).kapin.gkabar = 0.001 * 2  # 0.000032  # * 15 * 10
        self.dend2(0.5).pas.g = 1 / 100
        self.dend2(0.5).pas.e = -65  # -73
        self.dend2.Ra = 200  # 150
        self.dend2(0.5).nap.gnapbar = 0.0001  # 0.000018

        self.dend3(0.5).Nafin.gnafbar = 0.01  # 0.018 * 5
        self.dend3(0.5).kdrin.gkdrbar = 0.01 * 2  # 0.018 * 0.5
        self.dend3(0.5).kapin.gkabar = 0.001 * 2  # 0.000032  # * 15 * 10
        self.dend3(0.5).pas.g = 1 / 100
        self.dend3(0.5).pas.e = -65  # -73
        self.dend3.Ra = 200  # 150
        self.dend3(0.5).nap.gnapbar = 0.0001  # 0.000018

        self.dend4(0.5).Nafin.gnafbar = 0.01  # 0.018 * 5
        self.dend4(0.5).kdrin.gkdrbar = 0.01 * 2  # 0.018 * 0.5
        self.dend4(0.5).kapin.gkabar = 0.001 * 2  # 0.000032  # * 15 * 10
        self.dend4(0.5).pas.g = 1 / 100
        self.dend4(0.5).pas.e = -65  # -73
        self.dend4.Ra = 200  # 150
        self.dend4(0.5).nap.gnapbar = 0.0001  # 0.000018

        # ---------------axon----------------
        for mechanism_a in ['Nafin', 'kdrin', 'pas']:
            self.axon.insert(mechanism_a)

        self.axon(0.5).Nafin.gnafbar = 0.4
        self.axon(0.5).kdrin.gkdrbar = 0.4  # 0.001
        self.axon(0.5).pas.g = 0.001  # 0.0002
        self.axon(0.5).pas.e = -65  # -73
        self.axon.Ra = 100
        self.axon.cm = 1.2

        for sec in self.all:
            sec.cm = 1
            sec.ena = 50.
            sec.ek = -100.

        self.k_vec = h.Vector().record(self.soma(0.5)._ref_ik)
        self.na_vec = h.Vector().record(self.soma(0.5)._ref_ina)
        self.na_concentration = h.Vector().record(self.soma(0.5)._ref_nai)
        self.k_concentration = h.Vector().record(self.soma(0.5)._ref_ki)
        self.v_vec = h.Vector().record(self.soma(0.5)._ref_v)


class NontuftRS6(Cell):  #
    def __init__(self, x, y, z, num):
        super().__init__(x, y, z, num)
        self.id = 10
        self.Excitatory = 1
        self.name = 'L56 pyramidal nontufted regular spiking'

        # ---------------soma----------------
        for mechanism_s in ['extracellular', 'napf', 'pas',
                            # 'naf2_cc', 'kdr_fs_cc',
                            'Naf', 'kdr',
                            'kc',
                            'ka_cc', 'km_cc', 'k2_cc',
                            'kahp_deeppyr', 'cal_cc', 'cat_a', 'ar', 'cad_cc']:
            self.soma.insert(mechanism_s)

        self.soma(0.5).Naf.gnafbar = 0.2  # 0.6
        self.soma(0.5).napf.gbar = 0.0008  # 0.00006
        self.soma(0.5).kdr.gkdrbar = 0.17  # 0.5
        self.soma(0.5).ka_cc.gbar = 0.119  # 0.005
        self.soma(0.5).km_cc.gbar = 0.0042  # 0.0005
        self.soma(0.5).kc.gbar = 0.0075 * 2  # 0.01
        self.soma(0.5).k2_cc.gbar = 0.0001  # 0.0005
        self.soma(0.5).kahp_deeppyr.gbar = 0.0002
        self.soma(0.5).cal_cc.gbar = 0.0002  # 0.0001
        self.soma(0.5).cat_a.gbar = 0.0001  # 5.E-05
        self.soma(0.5).ar.gbar = 0.00025  # 2.5E-05
        self.soma(0.5).cad_cc.beta = 0.01  # 0.02
        self.soma(0.5).cad_cc.phi = 13000.  # 10400.
        self.soma(0.5).pas.e = -70
        self.soma(0.5).pas.g = 0.001
        self.soma.Ra = 250.  # 100.

        # ---------------dend----------------
        for mechanism_d in ['Naf', 'napf',
                            # 'naf_tcr', 'napf_tcr',
                            'kdr_thlms', 'ka', 'kc',
                            'km', 'k2', 'kahp_deeppyr', 'cal_thlms',
                            'cat_thlms', 'ar', 'cad', 'pas']:
            self.dend.insert(mechanism_d)
            self.dend1.insert(mechanism_d)
            self.dend2.insert(mechanism_d)
            self.dend3.insert(mechanism_d)
            self.dend4.insert(mechanism_d)

        self.dend(0.5).Naf.gnafbar = 0.075  # 0.1
        self.dend(0.5).napf.gbar = 0.0003  # 0.0002
        self.dend(0.5).kdr_thlms.gbar = 0.075
        self.dend(0.5).kc.gbar = 0.0075 * 2  # 0.012
        self.dend(0.5).ka.gbar = 0.0136  # 0.03
        self.dend(0.5).km.gbar = 0.0042  # 0 #// 0.0005
        self.dend(0.5).k2.gbar = 0.0001  # 0.002
        self.dend(0.5).cal_thlms.gbar = 0.0002  # 0.0005
        self.dend(0.5).cat_thlms.gbar = 0.0001  # 0.0005
        self.dend(0.5).kahp_deeppyr.gbar = 0.0002
        self.dend(0.5).ar.gbar = 0.00025
        self.dend(0.5).cad.beta = 0.05  # 0.02
        self.dend(0.5).cad.phi = 65000  # 52000.
        self.dend(0.5).pas.g = 1 / 100
        self.dend(0.5).pas.e = -70
        self.dend.Ra = 250  # 175

        self.dend1(0.5).Naf.gnafbar = 0.005  # 0.1
        self.dend1(0.5).napf.gbar = 2.E-05  # 0.0002
        self.dend1(0.5).kdr_thlms.gbar = 0.075
        self.dend1(0.5).kc.gbar = 0.012 * 2
        self.dend1(0.5).ka.gbar = 0.0136  # 0.03
        self.dend1(0.5).km.gbar = 0.0042  # 0  # // 0.0005
        self.dend1(0.5).k2.gbar = 0.0001  # 0.002
        self.dend1(0.5).cal_thlms.gbar = 0.0002  # 0.0005
        self.dend1(0.5).kahp_deeppyr.gbar = 0.0002
        self.dend1(0.5).cat_thlms.gbar = 0.0001  # 0.0005
        self.dend1(0.5).ar.gbar = 0.00025
        self.dend1(0.5).cad.beta = 0.05  # 0.02
        self.dend1(0.5).cad.phi = 65000.  # 52000.
        self.dend1(0.5).pas.g = 1 / 100
        self.dend1(0.5).pas.e = -70
        self.dend1.Ra = 250  # 175

        self.dend2(0.5).Naf.gnafbar = 0.005  # 0.1
        self.dend2(0.5).napf.gbar = 2.E-05  # 0.0002
        self.dend2(0.5).kdr_thlms.gbar = 0.075
        self.dend2(0.5).kc.gbar = 0.012 * 2
        self.dend2(0.5).ka.gbar = 0.0136  # 0.03
        self.dend2(0.5).km.gbar = 0.0042  # 0  # // 0.0005
        self.dend2(0.5).k2.gbar = 0.0001  # 0.002
        self.dend2(0.5).cal_thlms.gbar = 0.0002  # 0.0005
        self.dend2(0.5).cat_thlms.gbar = 0.0001  # 0.0005
        self.dend2(0.5).kahp_deeppyr.gbar = 0.0002
        self.dend2(0.5).ar.gbar = 0.00025
        self.dend2(0.5).cad.beta = 0.05  # 0.02
        self.dend2(0.5).cad.phi = 65000.  # 52000.
        self.dend2(0.5).pas.g = 1 / 100
        self.dend2(0.5).pas.e = -70
        self.dend2.Ra = 250  # 175

        self.dend3(0.5).Naf.gnafbar = 0.15  # 0.1
        self.dend3(0.5).napf.gbar = 0.0006  # 0.0002
        self.dend3(0.5).kdr_thlms.gbar = 0.12  # 0.075
        self.dend3(0.5).kc.gbar = 0.0075 * 2  # 0.012
        self.dend3(0.5).ka.gbar = 0.119  # 0.03
        self.dend3(0.5).km.gbar = 0.0042  # 0  # // 0.0005
        self.dend3(0.5).k2.gbar = 0.0001  # 0.002
        self.dend3(0.5).cal_thlms.gbar = 0.0002  # 0.0005
        self.dend3(0.5).cat_thlms.gbar = 0.0001  # 0.0005
        self.dend3(0.5).ar.gbar = 0.00025
        self.dend3(0.5).kahp_deeppyr.gbar = 0.0002
        self.dend3(0.5).cad.beta = 0.05  # 0.02
        self.dend3(0.5).cad.phi = 65000.  # 52000.
        self.dend3(0.5).pas.g = 1 / 100
        self.dend3(0.5).pas.e = -70
        self.dend3.Ra = 250  # 175

        self.dend4(0.5).Naf.gnafbar = 0.075  # 0.1
        self.dend4(0.5).napf.gbar = 0.0003  # 0.0002
        self.dend4(0.5).kdr_thlms.gbar = 0.075  # 0.075
        self.dend4(0.5).kc.gbar = 0.0075 * 2  # 0.012
        self.dend4(0.5).ka.gbar = 0.0136  # 0.03
        self.dend4(0.5).km.gbar = 0.0042  # 0  # // 0.0005
        self.dend4(0.5).k2.gbar = 0.0001  # 0.002
        self.dend4(0.5).cal_thlms.gbar = 0.0002  # 0.0005
        self.dend4(0.5).cat_thlms.gbar = 0.0001  # 0.0005
        self.dend4(0.5).kahp_deeppyr.gbar = 0.0002
        self.dend4(0.5).ar.gbar = 0.00025
        self.dend4(0.5).cad.beta = 0.05  # 0.02
        self.dend4(0.5).cad.phi = 65000.  # 52000.
        self.dend4(0.5).pas.g = 1 / 100
        self.dend4(0.5).pas.e = -70
        self.dend4.Ra = 250  # 175

        # ---------------axon----------------
        for mechanism_a in ['Nafin', 'kdrin', 'pas']:
            self.axon.insert(mechanism_a)

        self.axon(0.5).Nafin.gnafbar = 0.45  # 0.4
        self.axon(0.5).kdrin.gkdrbar = 0.45  # 0.001
        self.axon(0.5).pas.g = 0.001  # 0.005
        self.axon(0.5).pas.e = -70
        self.axon.Ra = 100.
        self.axon.cm = 1.2

        for sec in self.all:
            sec.cm = 0.9
            sec.ena = 50.
            sec.ek = -95

        self.k_vec = h.Vector().record(self.soma(0.5)._ref_ik)
        self.na_vec = h.Vector().record(self.soma(0.5)._ref_ina)
        self.na_concentration = h.Vector().record(self.soma(0.5)._ref_nai)
        self.k_concentration = h.Vector().record(self.soma(0.5)._ref_ki)
        self.v_vec = h.Vector().record(self.soma(0.5)._ref_v)


class EpilepsyNontuftRS6(Cell):  #
    def __init__(self, x, y, z, num):
        super().__init__(x, y, z, num)
        self.id = 10
        self.Excitatory = 1
        self.name = 'pyramidal nontufted regular spiking'

        # ---------------soma----------------
        # for mechanism_s in ['extracellular', 'Nafin', 'kdrin', 'IKsin', 'hin', 'kapin', 'canin', 'kctin', 'cadynin',
        #                    'pas']:
        #    self.soma.insert(mechanism_s)
        #
        # self.soma(0.5).Nafin.gnafbar = 0.5
        # self.soma(0.5).kdrin.gkdrbar = 0.001
        # self.soma(0.5).IKsin.gKsbar = 0.000725 * 0.1
        # self.soma(0.5).hin.gbar = 0.00001
        # self.soma(0.5).kapin.gkabar = 0.0032 * 15
        # self.soma(0.5).canin.gcalbar = 0.0003
        # self.soma(0.5).kctin.gkcbar = 0.0001
        # self.soma(0.5).pas.g = 0.0002
        # self.soma(0.5).pas.e = -70
        # self.soma.Ra = 100
        ##self.soma(0.5).nap.gnapbar = 0.018
        #
        # self.v1 = h.Vector().record(self.soma(0.5)._ref_ina_Nafin)
        ## self.v2 = h.Vector().record(self.soma(0.5)._ref_ina_nap)
        # self.v3 = h.Vector().record(self.soma(0.5)._ref_ik_kdrin)
        # self.v4 = h.Vector().record(self.soma(0.5)._ref_ik_IKsin)
        ## self.v5 = h.Vector().record(self.soma(0.5)._ref_ik_kc_fast)
        ## self.v6 = h.Vector().record(self.soma(0.5)._ref_ik_km)
        ## self.v7 = h.Vector().record(self.soma(0.5)._ref_ik_k2)
        ## self.v8 = h.Vector().record(self.soma(0.5)._ref_ik_kahp_slower)
        ## self.v9 = h.Vector().record(self.soma(0.5)._ref_ica_cal)
        #
        ## ---------------dend----------------
        # for mechanism_d in ['Nafin', 'kdrin', 'kapin', 'pas', 'nap']:
        #    self.dend.insert(mechanism_d)
        #    self.dend1.insert(mechanism_d)
        #    self.dend2.insert(mechanism_d)
        #    self.dend3.insert(mechanism_d)
        #    self.dend4.insert(mechanism_d)
        #
        #    # print(mechanism_d)
        #
        ## self.dend(0.5).naf2.gbar =   0.2
        # self.dend(0.5).Nafin.gnafbar = 0.00018 * 10
        # self.dend(0.5).kdrin.gkdrbar = 0.018
        # self.dend(0.5).kapin.gkabar = 0.000032 * 15 * 10
        # self.dend(0.5).nap.gnapbar = 0.000018
        # self.dend(0.5).pas.g = 1 / 100
        # self.dend(0.5).pas.e = -73
        # self.dend.Ra = 150
        #
        # self.dend1(0.5).Nafin.gnafbar = 0.00018 * 10
        # self.dend1(0.5).kdrin.gkdrbar = 0.018 * 0.5
        # self.dend1(0.5).kapin.gkabar = 0.000032 * 15 * 10
        # self.dend1(0.5).pas.g = 1 / 100
        # self.dend1(0.5).pas.e = -73
        # self.dend1.Ra = 150
        # self.dend1(0.5).nap.gnapbar = 0.000018
        #
        # self.dend2(0.5).Nafin.gnafbar = 0.00018 * 10
        # self.dend2(0.5).kdrin.gkdrbar = 0.018 * 0.5
        # self.dend2(0.5).kapin.gkabar = 0.000032 * 15 * 10
        # self.dend2(0.5).pas.g = 1 / 100
        # self.dend2(0.5).pas.e = -73
        # self.dend2.Ra = 150
        # self.dend2(0.5).nap.gnapbar = 0.000018
        #
        # self.dend3(0.5).Nafin.gnafbar = 0.00018 * 10
        # self.dend3(0.5).kdrin.gkdrbar = 0.018 * 0.5
        # self.dend3(0.5).kapin.gkabar = 0.000032 * 15 * 10
        # self.dend3(0.5).pas.g = 1 / 100
        # self.dend3(0.5).pas.e = -73
        # self.dend3.Ra = 150
        # self.dend3(0.5).nap.gnapbar = 0.000018
        #
        # self.dend4(0.5).Nafin.gnafbar = 0.00018 * 10
        # self.dend4(0.5).kdrin.gkdrbar = 0.018 * 0.5
        # self.dend4(0.5).kapin.gkabar = 0.000032 * 15 * 10
        # self.dend4(0.5).pas.g = 1 / 100
        # self.dend4(0.5).pas.e = -73
        # self.dend4.Ra = 150
        # self.dend4(0.5).nap.gnapbar = 0.000018
        #
        # self.vd1 = h.Vector().record(self.dend(0.5)._ref_ina_Nafin)
        ## self.vd2 = h.Vector().record(self.dend(0.5)._ref_ina_napf_spinstell)
        # self.vd3 = h.Vector().record(self.dend(0.5)._ref_ik_kdrin)
        # self.vd4 = h.Vector().record(self.dend(0.5)._ref_ik_kapin)
        #
        ## ---------------axon----------------
        # for mechanism_a in ['Nafin', 'kdrin', 'pas']:
        #    self.axon.insert(mechanism_a)
        #    # print(mechanism_a)
        #
        # self.axon(0.5).Nafin.gnafbar = 0.5
        # self.axon(0.5).kdrin.gkdrbar = 0.001
        # self.axon(0.5).pas.g = 0.0002
        # self.axon(0.5).pas.e = -73
        # self.axon.Ra = 100
        # self.axon.cm = 1.2
        #
        # for sec in self.all:
        #    sec.cm = 1.2
        #   # sec.cm = 0.9
        #    sec.ena = 50.
        #    sec.ek = -90
        for mechanism_s in ['extracellular', 'naf2_cc', 'pas', 'napf_spinstell', 'kdr_fs_cc', 'kc_fast_cc', 'ka_cc',
                            'km_cc', 'k2_cc', 'kahp_slower', 'cal_cc', 'cat_cc', 'ar', 'cad_cc']:
            self.soma.insert(mechanism_s)
        # print(mechanism_s)

        self.soma(0.5).naf2_cc.gbar = 0.65
        self.soma(0.5).napf_spinstell.gbar = 0.0002
        self.soma(0.5).kdr_fs_cc.gbar = 0.1 * 10
        self.soma(0.5).kc_fast_cc.gbar = 0.001 * 10
        self.soma(0.5).ka_cc.gbar = 0.03
        self.soma(0.5).km_cc.gbar = 0.00375
        self.soma(0.5).k2_cc.gbar = 0.0001
        self.soma(0.5).kahp_slower.gbar = 0.0001
        self.soma(0.5).cal_cc.gbar = 0.0005
        self.soma(0.5).cat_cc.gbar = 0.0001
        self.soma(0.5).ar.gbar = 0.00025
        self.soma(0.5).cad_cc.beta = 0.02
        self.soma(0.5).cad_cc.phi = 260000.
        self.soma(0.5).pas.g = 0.001
        self.soma(0.5).pas.e = -65
        self.soma.Ra = 150.

        # ---------------dend----------------
        for mechanism_d in ['naf2_cc', 'napf_spinstell', 'pas', 'kdr_fs_cc', 'kc_fast_cc', 'ka_cc', 'km_cc', 'k2_cc',
                            'kahp_slower', 'cal_cc', 'cat_cc', 'ar', 'cad_cc']:
            self.dend.insert(mechanism_d)
            self.dend1.insert(mechanism_d)
            self.dend2.insert(mechanism_d)
            self.dend3.insert(mechanism_d)
            self.dend4.insert(mechanism_d)
            # print(mechanism_d)

        self.dend(0.5).naf2_cc.gbar = 0.0075
        self.dend(0.5).napf_spinstell.gbar = 7.5E-05 / 100
        self.dend(0.5).kdr_fs_cc.gbar = 0.0075
        self.dend(0.5).kc_fast_cc.gbar = 0.01
        self.dend(0.5).ka_cc.gbar = 0.03
        self.dend(0.5).km_cc.gbar = 0.00375
        self.dend(0.5).k2_cc.gbar = 0.0001
        self.dend(0.5).kahp_slower.gbar = 0.0001
        self.dend(0.5).cal_cc.gbar = 0.0005
        self.dend(0.5).cat_cc.gbar = 0.0001
        self.dend(0.5).ar.gbar = 0.00025
        self.dend(0.5).cad_cc.beta = 0.05
        self.dend(0.5).cad_cc.phi = 260000.
        self.dend(0.5).pas.g = 0.02
        self.dend(0.5).pas.e = -65
        self.dend.Ra = 250.

        self.dend1(0.5).naf2_cc.gbar = 0.0075
        self.dend1(0.5).napf_spinstell.gbar = 7.5E-05 / 100
        self.dend1(0.5).kdr_fs_cc.gbar = 0.0075
        self.dend1(0.5).kc_fast_cc.gbar = 0.01
        self.dend1(0.5).ka_cc.gbar = 0.03
        self.dend1(0.5).km_cc.gbar = 0.00375
        self.dend1(0.5).k2_cc.gbar = 0.0001
        self.dend1(0.5).kahp_slower.gbar = 0.0001
        self.dend1(0.5).cal_cc.gbar = 0.0005
        self.dend1(0.5).cat_cc.gbar = 0.0001
        self.dend1(0.5).ar.gbar = 0.00025
        self.dend1(0.5).cad_cc.beta = 0.05
        self.dend1(0.5).cad_cc.phi = 260000.
        self.dend1(0.5).pas.g = 0.02
        self.dend1(0.5).pas.e = -65
        self.dend1.Ra = 250.

        self.dend2(0.5).naf2_cc.gbar = 0.0075
        self.dend2(0.5).napf_spinstell.gbar = 7.5E-05 / 100
        self.dend2(0.5).kdr_fs_cc.gbar = 0.0075
        self.dend2(0.5).kc_fast_cc.gbar = 0.01
        self.dend2(0.5).ka_cc.gbar = 0.03
        self.dend2(0.5).km_cc.gbar = 0.00375
        self.dend2(0.5).k2_cc.gbar = 0.0001
        self.dend2(0.5).kahp_slower.gbar = 0.0001
        self.dend2(0.5).cal_cc.gbar = 0.0005
        self.dend2(0.5).cat_cc.gbar = 0.0001
        self.dend2(0.5).ar.gbar = 0.00025
        self.dend2(0.5).cad_cc.beta = 0.05
        self.dend2(0.5).cad_cc.phi = 260000.
        self.dend2(0.5).pas.g = 0.02
        self.dend2(0.5).pas.e = -65
        self.dend2.Ra = 250.

        self.dend3(0.5).naf2_cc.gbar = 0.0075
        self.dend3(0.5).napf_spinstell.gbar = 7.5E-05 / 100
        self.dend3(0.5).kdr_fs_cc.gbar = 0.0075
        self.dend3(0.5).kc_fast_cc.gbar = 0.01
        self.dend3(0.5).ka_cc.gbar = 0.03
        self.dend3(0.5).km_cc.gbar = 0.00375
        self.dend3(0.5).k2_cc.gbar = 0.0001
        self.dend3(0.5).kahp_slower.gbar = 0.0001
        self.dend3(0.5).cal_cc.gbar = 0.0005
        self.dend3(0.5).cat_cc.gbar = 0.0001
        self.dend3(0.5).ar.gbar = 0.00025
        self.dend3(0.5).cad_cc.beta = 0.05
        self.dend3(0.5).cad_cc.phi = 260000.
        self.dend3(0.5).pas.g = 0.02
        self.dend3(0.5).pas.e = -65
        self.dend3.Ra = 250.

        self.dend4(0.5).naf2_cc.gbar = 0.0075
        self.dend4(0.5).napf_spinstell.gbar = 7.5E-05 / 100
        self.dend4(0.5).kdr_fs_cc.gbar = 0.0075
        self.dend4(0.5).kc_fast_cc.gbar = 0.01
        self.dend4(0.5).ka_cc.gbar = 0.03
        self.dend4(0.5).km_cc.gbar = 0.00375
        self.dend4(0.5).k2_cc.gbar = 0.0001
        self.dend4(0.5).kahp_slower.gbar = 0.0001
        self.dend4(0.5).cal_cc.gbar = 0.0005
        self.dend4(0.5).cat_cc.gbar = 0.0001
        self.dend4(0.5).ar.gbar = 0.00025
        self.dend4(0.5).cad_cc.beta = 0.05
        self.dend4(0.5).cad_cc.phi = 260000.
        self.dend4(0.5).pas.g = 0.02
        self.dend4(0.5).pas.e = -65
        self.dend4.Ra = 250.

        # self.vd1 = h.Vector().record(self.dend(0.5)._ref_ina_naf2)
        # self.vd2 = h.Vector().record(self.dend(0.5)._ref_ina_napf_spinstell)
        # self.vd3 = h.Vector().record(self.dend(0.5)._ref_ik_kdr_fs)
        # self.vd4 = h.Vector().record(self.dend(0.5)._ref_ik_ka)
        # self.vd5 = h.Vector().record(self.dend(0.5)._ref_ik_kc_fast)
        # self.vd7 = h.Vector().record(self.dend(0.5)._ref_ik_k2)
        # self.vd8 = h.Vector().record(self.dend(0.5)._ref_ik_kahp_slower)
        # self.vd9 = h.Vector().record(self.dend(0.5)._ref_ica_cal)

        # ---------------axon----------------
        for mechanism_a in ['naf2_cc', 'kdr_fs_cc', 'ka_cc', 'k2_cc', 'pas']:
            self.axon.insert(mechanism_a)
            # print(mechanism_a)

        self.axon(0.5).naf2_cc.gbar = 0.1 * 4
        self.axon(0.5).kdr_fs_cc.gbar = 0.9
        self.axon(0.5).ka_cc.gbar = 0.002
        self.axon(0.5).k2_cc.gbar = 0.1
        self.axon(0.5).pas.g = 0.01
        self.axon(0.5).pas.e = -65
        self.axon.Ra = 100.

        for sec in self.all:
            sec.cm = 0.9
            sec.ena = 50.
            sec.ek = -90
        # self.dend1(0.5).Nafin.gnafbar = 0.00018 * 10
        # self.dend1(0.5).kdrin.gkdrbar = 0.00018 * 0.5
        # self.dend1(0.5).kapin.gkabar = 0.000032 #* 15 * 10
        # self.dend1(0.5).pas.g = 1 / 100
        # self.dend1(0.5).pas.e = -73
        # self.dend1.Ra = 150
        # self.dend1(0.5).nap.gnapbar = 0.000018
        #
        # self.dend2(0.5).Nafin.gnafbar = 0.00018 * 10
        # self.dend2(0.5).kdrin.gkdrbar = 0.00018 * 0.5
        # self.dend2(0.5).kapin.gkabar = 0.000032 #* 15 * 10
        # self.dend2(0.5).pas.g = 1 / 100
        # self.dend2(0.5).pas.e = -73
        # self.dend2.Ra = 150
        # self.dend2(0.5).nap.gnapbar = 0.000018
        #
        # self.dend3(0.5).Nafin.gnafbar = 0.0018 * 10
        # self.dend3(0.5).kdrin.gkdrbar = 0.00018 * 0.5
        # self.dend3(0.5).kapin.gkabar = 0.000032 #* 15 * 10
        # self.dend3(0.5).pas.g = 1 / 100
        # self.dend3(0.5).pas.e = -73
        # self.dend3.Ra = 150
        # self.dend3(0.5).nap.gnapbar = 0.000018
        #
        # self.dend4(0.5).Nafin.gnafbar = 0.0018 * 10
        # self.dend4(0.5).kdrin.gkdrbar = 0.0018 * 0.5
        # self.dend4(0.5).kapin.gkabar = 0.000032 #* 15 * 10
        # self.dend4(0.5).pas.g = 1 / 100
        # self.dend4(0.5).pas.e = -73
        # self.dend4.Ra = 150
        # self.dend4(0.5).nap.gnapbar = 0.000018

        # ---------------axon----------------

        self.k_vec = h.Vector().record(self.soma(0.5)._ref_ik)
        self.na_vec = h.Vector().record(self.soma(0.5)._ref_ina)
        self.na_concentration = h.Vector().record(self.soma(0.5)._ref_nai)
        self.k_concentration = h.Vector().record(self.soma(0.5)._ref_ki)
        self.v_vec = h.Vector().record(self.soma(0.5)._ref_v)

        # self.cyt = rxd.Region(self.all, name='cyt', nrn_region='i', dx=1.0,
        #                       geometry=rxd.FractionalVolume(0.9, surface_fraction=1.0))
        # self.na = rxd.Species([self.cyt], name='na', charge=1, d=1.0, initial=10)
        # self.k = rxd.Species([self.cyt], name='k', charge=1, d=1.0, initial=148)
        # self.k_i = self.k[self.cyt]
        # self.ca = rxd.Species([self.cyt], d=0.08, name='ca', charge=2, initial=1.e-4, atolscale=1e-6)
        # ------for test-----------
        # self.stim = h.IClamp(self.soma(0.5))
        # self.stim.delay = 50
        # self.stim.dur = 1
        # self.stim.amp = 1
    # print(self.id)


class SyppyrFRB(Cell):  #
    def __init__(self, x, y, z, num):
        super().__init__(x, y, z, num)
        self.id = 12
        self.Excitatory = 1
        self.name = 'L23 pyramidal fast rythmic bursting'

        # ---------------soma----------------
        for mechanism_s in ['extracellular', 'Naf', 'nap',
                            # 'calc', 'car', 'can',
                            'cal',
                            'cat', 'kdrpr',
                            # 'IKs', 'h','ican',
                            'ka',
                            'kca', 'cadyn',
                            'pas']:
            self.soma.insert(mechanism_s)

        self.soma(0.5).Naf.gnafbar = 0.15 * 1.25  # 187.5*0.001 #0.018 * 3
        self.soma(0.5).nap.gnapbar = 0.0006 * 0.2  # 0.48*0.001 #0.000018
        self.soma(0.5).cal.gcalbar = 0.001  # 0.0001 * 0.3
        self.soma(0.5).cat.gcatbar = 0.1 * 0.001  # 0.0002 * 0.3 * 0.1
        self.soma(0.5).kdrpr.gkdrbar = 0.1 * 1.25  # 125*0.001 #0.018 * 0.3
        self.soma(0.5).ka.gbar = 30 * 0.001  # 0.0007
        self.soma(0.5).kca.gbar = 4.5 * 0.001 * 1.6  # 0.005 * 5
        self.soma(0.5).pas.g = 0.001
        self.soma(0.5).pas.e = -70  # -65
        self.soma.Ra = 250.  # 100

        # ---------------dend----------------
        for mechanism_d in ['Naf', 'nap',
                            # 'calc', 'car', 'can',
                            'cal', 'cat', 'kdrpr',
                            # 'IKs','h', 'ican',
                            'ka', 'kca',
                            'cadyn', 'pas']:
            self.dend.insert(mechanism_d)
            self.dend1.insert(mechanism_d)
            self.dend2.insert(mechanism_d)
            self.dend3.insert(mechanism_d)
            self.dend4.insert(mechanism_d)

        self.dend(0.5).Naf.gnafbar = 0.075 * 1.25  # 93.75 * 0.001 #0.018 * 0.1
        self.dend(0.5).nap.gnapbar = 0.0003 * 0.2  # 0.24*0.001 #0.000018
        self.dend(0.5).cal.gcalbar = 0.001  # 0.0001 * 0.3  #
        self.dend(0.5).cat.gcatbar = 0.1 * 0.001  # 0.0002 * 0.3 * 0.1  #
        self.dend(0.5).kdrpr.gkdrbar = 0.075 * 1.25  # 93.75*0.001 #0.018 * 0.09
        self.dend(0.5).ka.gbar = 2 * 0.001  # 0.0007
        self.dend(0.5).kca.gbar = 4.5 * 0.001 * 0.4  # 0.005 * 5 * 0.001  #
        self.dend(0.5).pas.g = 0.01
        self.dend(0.5).pas.e = -70  # -65
        self.dend.Ra = 250  # 150

        self.dend1(0.5).Naf.gnafbar = 0.01 * 1.25  # 12.5*0.001 #0.018 * 0.4
        self.dend1(0.5).nap.gnapbar = 0.032 * 0.001 * 0.2  # 0.000018  # * 3
        self.dend1(0.5).cal.gcalbar = 0.001  # 0.0001 * 0.3  #
        self.dend1(0.5).cat.gcatbar = 0.1 * 0.001  # 0.0002 * 0.3 * 0.1  #
        self.dend1(0.5).kdrpr.gkdrbar = 0.005 * 1.25  # 6.25*0.001#0.018 * 0.09
        self.dend1(0.5).ka.gbar = 2 * 0.001  # 0.0007
        self.dend1(0.5).kca.gbar = 0.0075 * 1.6  # 4.5*0.001 #0.005 * 5 * 0.0001  #
        self.dend1(0.5).pas.g = 0.01
        self.dend1(0.5).pas.e = -70  # -65
        self.dend1.Ra = 250  # 150

        self.dend2(0.5).Naf.gnafbar = 0.01 * 1.25  # 12.5*0.001#0.018 * 0.1
        self.dend2(0.5).nap.gnapbar = 4.E-05 * 0.2  # 0.032*0.001 #0.000018
        self.dend2(0.5).cal.gcalbar = 0.001  # 0.0001 * 0.3  #
        self.dend2(0.5).cat.gcatbar = 0.1 * 0.001  # 0.0002 * 0.3 * 0.1  #
        self.dend2(0.5).kdrpr.gkdrbar = 0.005 * 1.25  # 6.25*0.001#0.018 * 0.09
        self.dend2(0.5).ka.gbar = 2 * 0.001  # 0.0007
        self.dend2(0.5).kca.gbar = 0.0075 * 1.6  # 4.5*0.001 #0.005 * 5 * 0.001  #
        self.dend2(0.5).pas.g = 0.01
        self.dend2(0.5).pas.e = -70  # -65
        self.dend2.Ra = 250  # 150

        self.dend3(0.5).Naf.gnafbar = 0.1 * 1.25  # 125*0.001#0.018 * 0.1
        self.dend3(0.5).nap.gnapbar = 0.0004 * 0.2  # 0.32*0.001#0.000018
        self.dend3(0.5).cal.gcalbar = 0.001  # 0.0001 * 0.3  #
        self.dend3(0.5).cat.gcatbar = 0.1 * 0.001  # 0.0002 * 0.3 * 0.1  #
        self.dend3(0.5).kdrpr.gkdrbar = 0.1 * 1.25  # 125*0.001#0.018 * 0.09
        self.dend3(0.5).ka.gbar = 0.03  # 30*0.001#0.0007
        self.dend3(0.5).kca.gbar = 0.0075 * 1.6  # 4.5*0.001 #0.005 * 5 * 0.001  #
        self.dend3(0.5).pas.g = 0.01
        self.dend3(0.5).pas.e = -70  # -65
        self.dend3.Ra = 250  # 150

        self.dend4(0.5).Naf.gnafbar = 0.075 * 1.25  # 93.75*0.001 #0.018 * 0.1
        self.dend4(0.5).nap.gnapbar = 0.0003 * 0.2  # 0.024*0.001 #0.000018
        self.dend4(0.5).cal.gcalbar = 0.001  # 0.0001 * 0.3  #
        self.dend4(0.5).cat.gcatbar = 0.1 * 0.001  # 0.0002 * 0.3 * 0.1  #
        self.dend4(0.5).kdrpr.gkdrbar = 0.075 * 1.25  # 93.75*0.001 #0.018 * 0.09
        self.dend4(0.5).ka.gbar = 2 * 0.001  # 0.0007
        self.dend4(0.5).kca.gbar = 0.0075 * 1.6  # 4.5*0.001 #0.005 * 5 * 0.001  #
        self.dend4(0.5).pas.g = 0.01
        self.dend4(0.5).pas.e = -70  # -65
        self.dend4.Ra = 250  # 150

        # ---------------axon----------------
        for mechanism_a in ['Nafin', 'kdrin', 'pas']:
            self.axon.insert(mechanism_a)

        self.axon(0.5).Nafin.gnafbar = 0.4
        self.axon(0.5).kdrin.gkdrbar = 0.4  # 0.001
        self.axon(0.5).pas.g = 0.001  # 0.0002
        self.axon(0.5).pas.e = -70  # -73
        self.axon.Ra = 100
        self.axon.cm = 1.2

        for sec in self.all:
            sec.cm = 0.9
            sec.ena = 50.
            sec.ek = -95.

        self.k_vec = h.Vector().record(self.soma(0.5)._ref_ik)
        self.na_vec = h.Vector().record(self.soma(0.5)._ref_ina)
        self.na_concentration = h.Vector().record(self.soma(0.5)._ref_nai)
        self.k_concentration = h.Vector().record(self.soma(0.5)._ref_ki)
        self.v_vec = h.Vector().record(self.soma(0.5)._ref_v)


class SyppyrRS(Cell):  #
    def __init__(self, x, y, z, num):
        super().__init__(x, y, z, num)
        self.id = 13
        self.Excitatory = 1
        self.name = 'L23 pyramidal regular spiking'

        # ---------------soma----------------
        for mechanism_s in ['extracellular', 'Naf', 'nap',
                            # 'calc', 'car', 'can',
                            'cal', 'cat',
                            # 'IKs',  'ican','h',
                            'kdrpr', 'ka',
                            'kca', 'ar',
                            'cadyn', 'pas']:
            self.soma.insert(mechanism_s)

        self.soma(0.5).Naf.gnafbar = 1.25 * 0.15  # 187.5*0.001 # 0.018 * 3
        self.soma(0.5).nap.gnapbar = 0.0006  # 0.12*0.001 #0.000018
        self.soma(0.5).cal.gcalbar = 0.001  # 0.0001 * 0.3
        self.soma(0.5).cat.gcatbar = 0.1 * 0.001  # 0.0002 * 0.3 * 0.1
        self.soma(0.5).kdrpr.gkdrbar = 1.25 * 0.1  # 125*0.001 #0.018 * 0.3
        self.soma(0.5).ka.gbar = 30 * 0.001  # 0.0007
        self.soma(0.5).kca.gbar = 0.0075  # 12*0.001#0.005 * 5
        self.soma(0.5).ar.gbar = 0.00025
        self.soma(0.5).pas.g = 0.001
        self.soma(0.5).pas.e = -70  # -65
        self.soma.Ra = 250.  # 100

        # ---------------dend----------------
        for mechanism_d in ['Naf', 'nap', 'cal',
                            # 'can', 'car', 'calc',
                            'cat',
                            'kdrpr', 'ka',
                            # 'IKs',  'h','ican',
                            'kca', 'ar', 'cadyn', 'pas']:
            self.dend.insert(mechanism_d)
            self.dend1.insert(mechanism_d)
            self.dend2.insert(mechanism_d)
            self.dend3.insert(mechanism_d)
            self.dend4.insert(mechanism_d)

        self.dend(0.5).Naf.gnafbar = 1.25 * 0.075  # 93.75*0.001 #0.018 * 0.1
        self.dend(0.5).nap.gnapbar = 0.0003  # 0.06 #0.000018
        self.dend(0.5).cal.gcalbar = 0.001  # 0.0001 * 0.3  #
        self.dend(0.5).cat.gcatbar = 0.1 * 0.001  # 0.0002 * 0.3 * 0.1  #
        self.dend(0.5).kdrpr.gkdrbar = 1.25 * 0.075  # 93.75*0.001 #0.018 * 0.09
        self.dend(0.5).ka.gbar = 2 * 0.001  # 0.0007
        self.dend(0.5).kca.gbar = 0.0075  # 12*0.001 #0.005 * 5 * 0.001  #
        self.dend(0.5).ar.gbar = 0.00025
        self.dend(0.5).pas.g = 0.01
        self.dend(0.5).pas.e = -70  # -65
        self.dend.Ra = 250  # 150

        self.dend1(0.5).Naf.gnafbar = 1.25 * 0.01  # 12.5*0.001#0.018 * 0.4
        self.dend1(0.5).nap.gnapbar = 4.E-05  # 0.008*0.001 #0.000018  # * 3
        self.dend1(0.5).cal.gcalbar = 0.001  # 0.0001 * 0.3  #
        self.dend1(0.5).cat.gcatbar = 0.1 * 0.001  # 0.0002 * 0.3 * 0.1  #
        self.dend1(0.5).kdrpr.gkdrbar = 1.25 * 0.005  # 6.25*0.001 #0.018 * 0.09
        self.dend1(0.5).ka.gbar = 2 * 0.001  # 0.0007
        self.dend1(0.5).kca.gbar = 0.0075  # 12*0.001 #0.005 * 5 * 0.0001  #
        self.dend1(0.5).ar.gbar = 0.00025
        self.dend1(0.5).pas.g = 0.01
        self.dend1(0.5).pas.e = -70  # -65
        self.dend1.Ra = 250  # 150

        self.dend2(0.5).Naf.gnafbar = 1.25 * 0.01  # 12/5*0.001 #0.018 * 0.1
        self.dend2(0.5).nap.gnapbar = 4.E-05  # 0.008*0.001 #0.000018
        self.dend2(0.5).cal.gcalbar = 0.001  # 0.0001 * 0.3  #
        self.dend2(0.5).cat.gcatbar = 0.1 * 0.001  # 0.0002 * 0.3 * 0.1  #
        self.dend2(0.5).kdrpr.gkdrbar = 1.25 * 0.005  # 6.25*0.001#0.018 * 0.09
        self.dend2(0.5).ka.gbar = 2 * 0.001  # 0.0007
        self.dend2(0.5).kca.gbar = 0.0075  # 12*0.001 #0.005 * 5 * 0.001  #
        self.dend2(0.5).ar.gbar = 0.00025
        self.dend2(0.5).pas.g = 0.01
        self.dend2(0.5).pas.e = -70  # -65
        self.dend2.Ra = 250  # 150

        self.dend3(0.5).Naf.gnafbar = 1.25 * 0.1  # 125*0.001 #0.018 * 0.1
        self.dend3(0.5).nap.gnapbar = 0.0004  # 0.08*0.001 #0.000018
        self.dend3(0.5).cal.gcalbar = 0.001  # 0.0001 * 0.3  #
        self.dend3(0.5).cat.gcatbar = 0.0001  # 0.01*0.001 #0.0002 * 0.3 * 0.1  #
        self.dend3(0.5).kdrpr.gkdrbar = 1.25 * 0.1  # 125*0.001 #0.018 * 0.09
        self.dend3(0.5).ka.gbar = 30 * 0.001  # 0.0007
        self.dend3(0.5).kca.gbar = 0.0075  # 12*0.001 #0.005 * 5 * 0.001  #
        self.dend3(0.5).ar.gbar = 0.00025
        self.dend3(0.5).pas.g = 0.01
        self.dend3(0.5).pas.e = -70  # -65
        self.dend3.Ra = 250  # 150

        self.dend4(0.5).Naf.gnafbar = 1.25 * 0.075  # 93.75*0.001 #0.018 * 0.1
        self.dend4(0.5).nap.gnapbar = 0.0003  # 0.06*0.001 #0.000018
        self.dend4(0.5).cal.gcalbar = 0.001  # 0.0001 * 0.3  #
        self.dend4(0.5).cat.gcatbar = 0.1 * 0.001  # 0.0002 * 0.3 * 0.1  #
        self.dend4(0.5).kdrpr.gkdrbar = 1.25 * 0.075  # 93.75*0.001 #0.018 * 0.09
        self.dend4(0.5).ka.gbar = 2 * 0.001  # 0.0007
        self.dend4(0.5).kca.gbar = 0.0075  # 12*0.001 #0.005 * 5 * 0.001  #
        self.dend4(0.5).ar.gbar = 0.00025
        self.dend4(0.5).pas.g = 0.01
        self.dend4(0.5).pas.e = -70  # -65
        self.dend4.Ra = 250  # 150

        # ---------------axon----------------
        for mechanism_a in ['Nafin', 'kdrin', 'pas']:
            self.axon.insert(mechanism_a)

        self.axon(0.5).Nafin.gnafbar = 0.4
        self.axon(0.5).kdrin.gkdrbar = 0.4  # 0.001
        self.axon(0.5).pas.g = 0.001  # 0.0002
        self.axon(0.5).pas.e = -70  # -73
        self.axon.Ra = 100
        self.axon.cm = 1.2

        for sec in self.all:
            sec.cm = 0.9
            sec.ena = 50.
            sec.ek = -95.

        self.k_vec = h.Vector().record(self.soma(0.5)._ref_ik)
        self.na_vec = h.Vector().record(self.soma(0.5)._ref_ina)
        self.na_concentration = h.Vector().record(self.soma(0.5)._ref_nai)
        self.k_concentration = h.Vector().record(self.soma(0.5)._ref_ki)
        self.v_vec = h.Vector().record(self.soma(0.5)._ref_v)


class EpilepsySyppyrFRB(Cell):  #
    def __init__(self, x, y, z, num):
        super().__init__(x, y, z, num)
        self.id = 12
        self.Excitatory = 1
        self.name = 'pyramidal fast rythmic bursting'
        # self.soma.nseg = 1+2*int(somaR*2/40)

        # ---------------soma----------------
        for mechanism_s in ['extracellular', 'naf2_cc', 'pas', 'napf_spinstell', 'kdr_fs_cc', 'kc_fast_cc', 'ka_cc',
                            'km_cc', 'k2_cc', 'kahp_slower', 'cal_cc', 'cat_cc', 'ar', 'cad_cc']:
            self.soma.insert(mechanism_s)

        self.soma(0.5).naf2_cc.gbar = 0.65
        self.soma(0.5).napf_spinstell.gbar = 0.0002
        self.soma(0.5).kdr_fs_cc.gbar = 0.1 * 10
        self.soma(0.5).kc_fast_cc.gbar = 0.001 * 10
        self.soma(0.5).ka_cc.gbar = 0.03
        self.soma(0.5).km_cc.gbar = 0.00375
        self.soma(0.5).k2_cc.gbar = 0.0001
        self.soma(0.5).kahp_slower.gbar = 0.0001
        self.soma(0.5).cal_cc.gbar = 0.0005
        self.soma(0.5).cat_cc.gbar = 0.0001
        self.soma(0.5).ar.gbar = 0.00025
        self.soma(0.5).cad_cc.beta = 0.02
        self.soma(0.5).cad_cc.phi = 260000.
        self.soma(0.5).pas.g = 0.01  # 0.001
        self.soma(0.5).pas.e = -65
        self.soma.Ra = 150.

        # ---------------dend----------------
        for mechanism_d in ['naf2_cc', 'napf_spinstell', 'pas', 'kdr_fs_cc', 'kc_fast_cc', 'ka_cc', 'km_cc', 'k2_cc',
                            'kahp_slower', 'cal_cc', 'cat_cc', 'ar', 'cad_cc']:
            self.dend.insert(mechanism_d)
            self.dend1.insert(mechanism_d)
            self.dend2.insert(mechanism_d)
            self.dend3.insert(mechanism_d)
            self.dend4.insert(mechanism_d)

        self.dend(0.5).naf2_cc.gbar = 0.0075
        self.dend(0.5).napf_spinstell.gbar = 7.5E-05 / 100
        self.dend(0.5).kdr_fs_cc.gbar = 0.0075
        self.dend(0.5).kc_fast_cc.gbar = 0.01
        self.dend(0.5).ka_cc.gbar = 0.03
        self.dend(0.5).km_cc.gbar = 0.00375
        self.dend(0.5).k2_cc.gbar = 0.0001
        self.dend(0.5).kahp_slower.gbar = 0.0001
        self.dend(0.5).cal_cc.gbar = 0.0005
        self.dend(0.5).cat_cc.gbar = 0.0001
        self.dend(0.5).ar.gbar = 0.00025
        self.dend(0.5).cad_cc.beta = 0.05
        self.dend(0.5).cad_cc.phi = 260000.
        self.dend(0.5).pas.g = 0.02
        self.dend(0.5).pas.e = -65
        self.dend.Ra = 250.

        self.dend1(0.5).naf2_cc.gbar = 0.0075
        self.dend1(0.5).napf_spinstell.gbar = 7.5E-05 / 100
        self.dend1(0.5).kdr_fs_cc.gbar = 0.0075
        self.dend1(0.5).kc_fast_cc.gbar = 0.01
        self.dend1(0.5).ka_cc.gbar = 0.03
        self.dend1(0.5).km_cc.gbar = 0.00375
        self.dend1(0.5).k2_cc.gbar = 0.0001
        self.dend1(0.5).kahp_slower.gbar = 0.0001
        self.dend1(0.5).cal_cc.gbar = 0.0005
        self.dend1(0.5).cat_cc.gbar = 0.0001
        self.dend1(0.5).ar.gbar = 0.00025
        self.dend1(0.5).cad_cc.beta = 0.05
        self.dend1(0.5).cad_cc.phi = 260000.
        self.dend1(0.5).pas.g = 0.02
        self.dend1(0.5).pas.e = -65
        self.dend1.Ra = 250.

        self.dend2(0.5).naf2_cc.gbar = 0.0075
        self.dend2(0.5).napf_spinstell.gbar = 7.5E-05 / 100
        self.dend2(0.5).kdr_fs_cc.gbar = 0.0075
        self.dend2(0.5).kc_fast_cc.gbar = 0.01
        self.dend2(0.5).ka_cc.gbar = 0.03
        self.dend2(0.5).km_cc.gbar = 0.00375
        self.dend2(0.5).k2_cc.gbar = 0.0001
        self.dend2(0.5).kahp_slower.gbar = 0.0001
        self.dend2(0.5).cal_cc.gbar = 0.0005
        self.dend2(0.5).cat_cc.gbar = 0.0001
        self.dend2(0.5).ar.gbar = 0.00025
        self.dend2(0.5).cad_cc.beta = 0.05
        self.dend2(0.5).cad_cc.phi = 260000.
        self.dend2(0.5).pas.g = 0.02
        self.dend2(0.5).pas.e = -65
        self.dend2.Ra = 250.

        self.dend3(0.5).naf2_cc.gbar = 0.0075
        self.dend3(0.5).napf_spinstell.gbar = 7.5E-05 / 100
        self.dend3(0.5).kdr_fs_cc.gbar = 0.0075
        self.dend3(0.5).kc_fast_cc.gbar = 0.01
        self.dend3(0.5).ka_cc.gbar = 0.03
        self.dend3(0.5).km_cc.gbar = 0.00375
        self.dend3(0.5).k2_cc.gbar = 0.0001
        self.dend3(0.5).kahp_slower.gbar = 0.0001
        self.dend3(0.5).cal_cc.gbar = 0.0005
        self.dend3(0.5).cat_cc.gbar = 0.0001
        self.dend3(0.5).ar.gbar = 0.00025
        self.dend3(0.5).cad_cc.beta = 0.05
        self.dend3(0.5).cad_cc.phi = 260000.
        self.dend3(0.5).pas.g = 0.02
        self.dend3(0.5).pas.e = -65
        self.dend3.Ra = 250.

        self.dend4(0.5).naf2_cc.gbar = 0.0075
        self.dend4(0.5).napf_spinstell.gbar = 7.5E-05 / 100
        self.dend4(0.5).kdr_fs_cc.gbar = 0.0075
        self.dend4(0.5).kc_fast_cc.gbar = 0.01
        self.dend4(0.5).ka_cc.gbar = 0.03
        self.dend4(0.5).km_cc.gbar = 0.00375
        self.dend4(0.5).k2_cc.gbar = 0.0001
        self.dend4(0.5).kahp_slower.gbar = 0.0001
        self.dend4(0.5).cal_cc.gbar = 0.0005
        self.dend4(0.5).cat_cc.gbar = 0.0001
        self.dend4(0.5).ar.gbar = 0.00025
        self.dend4(0.5).cad_cc.beta = 0.05
        self.dend4(0.5).cad_cc.phi = 260000.
        self.dend4(0.5).pas.g = 0.02
        self.dend4(0.5).pas.e = -65
        self.dend4.Ra = 250.

        # ---------------axon----------------
        for mechanism_a in ['naf2_cc', 'kdr_fs_cc', 'ka_cc', 'k2_cc', 'pas']:
            self.axon.insert(mechanism_a)

        self.axon(0.5).naf2_cc.gbar = 0.1 * 4
        self.axon(0.5).kdr_fs_cc.gbar = 0.9
        self.axon(0.5).ka_cc.gbar = 0.002
        self.axon(0.5).k2_cc.gbar = 0.1
        self.axon(0.5).pas.g = 0.01
        self.axon(0.5).pas.e = -65
        self.axon.Ra = 100.

        for sec in self.all:
            sec.cm = 0.9
            sec.ena = 50.
            sec.ek = -90

        self.k_vec = h.Vector().record(self.soma(0.5)._ref_ik)
        self.na_vec = h.Vector().record(self.soma(0.5)._ref_ina)
        self.na_concentration = h.Vector().record(self.soma(0.5)._ref_nai)
        self.k_concentration = h.Vector().record(self.soma(0.5)._ref_ki)
        self.v_vec = h.Vector().record(self.soma(0.5)._ref_v)


class EpilepsySyppyrRS(Cell):  #
    def __init__(self, x, y, z, num):
        super().__init__(x, y, z, num)
        self.id = 13
        self.Excitatory = 1
        self.name = 'pyramidal regular spiking'

        # ---------------soma----------------
        for mechanism_s in ['extracellular', 'naf2_cc', 'pas', 'napf_spinstell', 'kdr_fs_cc', 'kc_fast_cc', 'ka_cc',
                            'km_cc', 'k2_cc', 'kahp_slower', 'cal_cc', 'cat_cc', 'ar', 'cad_cc']:
            self.soma.insert(mechanism_s)

        self.soma(0.5).naf2_cc.gbar = 0.65
        self.soma(0.5).napf_spinstell.gbar = 0.0002
        self.soma(0.5).kdr_fs_cc.gbar = 0.1 * 10
        self.soma(0.5).kc_fast_cc.gbar = 0.001 * 10
        self.soma(0.5).ka_cc.gbar = 0.03
        self.soma(0.5).km_cc.gbar = 0.00375
        self.soma(0.5).k2_cc.gbar = 0.0001
        self.soma(0.5).kahp_slower.gbar = 0.0001
        self.soma(0.5).cal_cc.gbar = 0.0005
        self.soma(0.5).cat_cc.gbar = 0.0001
        self.soma(0.5).ar.gbar = 0.00025
        self.soma(0.5).cad_cc.beta = 0.02
        self.soma(0.5).cad_cc.phi = 260000.
        self.soma(0.5).pas.g = 0.001
        self.soma(0.5).pas.e = -65
        self.soma.Ra = 150.

        # ---------------dend----------------
        for mechanism_d in ['naf2_cc', 'napf_spinstell', 'pas', 'kdr_fs_cc', 'kc_fast_cc', 'ka_cc', 'km_cc', 'k2_cc',
                            'kahp_slower', 'cal_cc', 'cat_cc', 'ar', 'cad_cc']:
            self.dend.insert(mechanism_d)
            self.dend1.insert(mechanism_d)
            self.dend2.insert(mechanism_d)
            self.dend3.insert(mechanism_d)
            self.dend4.insert(mechanism_d)

        self.dend(0.5).naf2_cc.gbar = 0.0075
        self.dend(0.5).napf_spinstell.gbar = 7.5E-05 / 100
        self.dend(0.5).kdr_fs_cc.gbar = 0.0075
        self.dend(0.5).kc_fast_cc.gbar = 0.01
        self.dend(0.5).ka_cc.gbar = 0.03
        self.dend(0.5).km_cc.gbar = 0.00375
        self.dend(0.5).k2_cc.gbar = 0.0001
        self.dend(0.5).kahp_slower.gbar = 0.0001
        self.dend(0.5).cal_cc.gbar = 0.0005
        self.dend(0.5).cat_cc.gbar = 0.0001
        self.dend(0.5).ar.gbar = 0.00025
        self.dend(0.5).cad_cc.beta = 0.05
        self.dend(0.5).cad_cc.phi = 260000.
        self.dend(0.5).pas.g = 0.02
        self.dend(0.5).pas.e = -65
        self.dend.Ra = 250.

        self.dend1(0.5).naf2_cc.gbar = 0.0075
        self.dend1(0.5).napf_spinstell.gbar = 7.5E-05 / 100
        self.dend1(0.5).kdr_fs_cc.gbar = 0.0075
        self.dend1(0.5).kc_fast_cc.gbar = 0.01
        self.dend1(0.5).ka_cc.gbar = 0.03
        self.dend1(0.5).km_cc.gbar = 0.00375
        self.dend1(0.5).k2_cc.gbar = 0.0001
        self.dend1(0.5).kahp_slower.gbar = 0.0001
        self.dend1(0.5).cal_cc.gbar = 0.0005
        self.dend1(0.5).cat_cc.gbar = 0.0001
        self.dend1(0.5).ar.gbar = 0.00025
        self.dend1(0.5).cad_cc.beta = 0.05
        self.dend1(0.5).cad_cc.phi = 260000.
        self.dend1(0.5).pas.g = 0.02
        self.dend1(0.5).pas.e = -65
        self.dend1.Ra = 250.

        self.dend2(0.5).naf2_cc.gbar = 0.0075
        self.dend2(0.5).napf_spinstell.gbar = 7.5E-05 / 100
        self.dend2(0.5).kdr_fs_cc.gbar = 0.0075
        self.dend2(0.5).kc_fast_cc.gbar = 0.01
        self.dend2(0.5).ka_cc.gbar = 0.03
        self.dend2(0.5).km_cc.gbar = 0.00375
        self.dend2(0.5).k2_cc.gbar = 0.0001
        self.dend2(0.5).kahp_slower.gbar = 0.0001
        self.dend2(0.5).cal_cc.gbar = 0.0005
        self.dend2(0.5).cat_cc.gbar = 0.0001
        self.dend2(0.5).ar.gbar = 0.00025
        self.dend2(0.5).cad_cc.beta = 0.05
        self.dend2(0.5).cad_cc.phi = 260000.
        self.dend2(0.5).pas.g = 0.02
        self.dend2(0.5).pas.e = -65
        self.dend2.Ra = 250.

        self.dend3(0.5).naf2_cc.gbar = 0.0075
        self.dend3(0.5).napf_spinstell.gbar = 7.5E-05 / 100
        self.dend3(0.5).kdr_fs_cc.gbar = 0.0075
        self.dend3(0.5).kc_fast_cc.gbar = 0.01
        self.dend3(0.5).ka_cc.gbar = 0.03
        self.dend3(0.5).km_cc.gbar = 0.00375
        self.dend3(0.5).k2_cc.gbar = 0.0001
        self.dend3(0.5).kahp_slower.gbar = 0.0001
        self.dend3(0.5).cal_cc.gbar = 0.0005
        self.dend3(0.5).cat_cc.gbar = 0.0001
        self.dend3(0.5).ar.gbar = 0.00025
        self.dend3(0.5).cad_cc.beta = 0.05
        self.dend3(0.5).cad_cc.phi = 260000.
        self.dend3(0.5).pas.g = 0.02
        self.dend3(0.5).pas.e = -65
        self.dend3.Ra = 250.

        self.dend4(0.5).naf2_cc.gbar = 0.0075
        self.dend4(0.5).napf_spinstell.gbar = 7.5E-05 / 100
        self.dend4(0.5).kdr_fs_cc.gbar = 0.0075
        self.dend4(0.5).kc_fast_cc.gbar = 0.01
        self.dend4(0.5).ka_cc.gbar = 0.03
        self.dend4(0.5).km_cc.gbar = 0.00375
        self.dend4(0.5).k2_cc.gbar = 0.0001
        self.dend4(0.5).kahp_slower.gbar = 0.0001
        self.dend4(0.5).cal_cc.gbar = 0.0005
        self.dend4(0.5).cat_cc.gbar = 0.0001
        self.dend4(0.5).ar.gbar = 0.00025
        self.dend4(0.5).cad_cc.beta = 0.05
        self.dend4(0.5).cad_cc.phi = 260000.
        self.dend4(0.5).pas.g = 0.02
        self.dend4(0.5).pas.e = -65
        self.dend4.Ra = 250.

        # ---------------axon----------------
        for mechanism_a in ['naf2_cc', 'kdr_fs_cc', 'ka_cc', 'k2_cc', 'pas']:
            self.axon.insert(mechanism_a)

        self.axon(0.5).naf2_cc.gbar = 0.1 * 4
        self.axon(0.5).kdr_fs_cc.gbar = 0.9
        self.axon(0.5).ka_cc.gbar = 0.002
        self.axon(0.5).k2_cc.gbar = 0.1
        self.axon(0.5).pas.g = 0.01
        self.axon(0.5).pas.e = -65
        self.axon.Ra = 100.

        for sec in self.all:
            sec.cm = 0.9
            sec.ena = 50.
            sec.ek = -90

        self.k_vec = h.Vector().record(self.soma(0.5)._ref_ik)
        self.na_vec = h.Vector().record(self.soma(0.5)._ref_ina)
        self.na_concentration = h.Vector().record(self.soma(0.5)._ref_nai)
        self.k_concentration = h.Vector().record(self.soma(0.5)._ref_ki)
        self.v_vec = h.Vector().record(self.soma(0.5)._ref_v)


# ============Thalamus=============


class TCR(Cell):  #
    def __init__(self, x, y, z, num):
        super().__init__(x, y, z, num)
        self.id = 14
        self.Excitatory = 1
        self.name = 'thalamocortical relay'

        # ---------------soma----------------
        for mechanism_s in ['extracellular', 'naf_tcr', 'napf_tcr', 'kdr',
                            'kc', 'ka_cc', 'km_cc', 'k2_cc',
                            'kahp_slower', 'cal_cc', 'cat_a',
                            'ar', 'cad_cc', 'pas']:
            self.soma.insert(mechanism_s)

        self.soma(0.5).naf_tcr.gbar = 0.6  # 0.1  # 0.6
        self.soma(0.5).napf_tcr.gbar = 0.0002  # 0.00006
        self.soma(0.5).kdr.gkdrbar = 0.75  # 0.5
        self.soma(0.5).kc.gbar = 0.01
        self.soma(0.5).ka_cc.gbar = 0.03  # 0.005
        self.soma(0.5).km_cc.gbar = 0.0005
        self.soma(0.5).k2_cc.gbar = 0.002  # 0.0005
        self.soma(0.5).kahp_slower.gbar = 0  # 5.E-05
        self.soma(0.5).cal_cc.gbar = 0.0005  # 0.0001
        self.soma(0.5).cat_a.gbar = 0.0005  # 5.E-05
        self.soma(0.5).ar.gbar = 0.00025  # 2.5E-05
        self.soma(0.5).cad_cc.beta = 0.02
        self.soma(0.5).cad_cc.phi = 52000.  # 10400.
        self.soma(0.5).pas.e = -70
        self.soma(0.5).pas.g = 0.001
        self.soma.Ra = 175.  # 100.

        # ---------------dend----------------
        for mechanism_d in ['naf_tcr', 'napf_tcr', 'kdr_thlms',
                            'ka', 'kc', 'km', 'k2', 'kahp_slower',
                            'cal_thlms',
                            'cat_thlms', 'ar', 'cad', 'pas']:
            self.dend.insert(mechanism_d)
            self.dend1.insert(mechanism_d)
            self.dend2.insert(mechanism_d)
            self.dend3.insert(mechanism_d)
            self.dend4.insert(mechanism_d)

        self.dend(0.5).naf_tcr.gbar = 0.1
        self.dend(0.5).napf_tcr.gbar = 0.0002
        self.dend(0.5).kdr_thlms.gbar = 0.05  # 0.075
        self.dend(0.5).kc.gbar = 0.012
        self.dend(0.5).ka.gbar = 0.03
        self.dend(0.5).km.gbar = 0.0005
        self.dend(0.5).k2.gbar = 0.002
        self.dend(0.5).cal_thlms.gbar = 0.0005
        self.dend(0.5).cat_thlms.gbar = 0.005  # 0.0005
        self.dend(0.5).ar.gbar = 0.0005  # 0.00025
        self.dend(0.5).cad.beta = 0.05  # 0.02
        self.dend(0.5).cad.phi = 104000.  # 52000.
        self.dend(0.5).pas.g = 1 / 100
        self.dend(0.5).pas.e = -70
        self.dend.Ra = 175

        self.dend1(0.5).naf_tcr.gbar = 0.1  # 0.005  # 0.1
        self.dend1(0.5).napf_tcr.gbar = 0.0002  # 1.E-05  # 0.0002
        self.dend1(0.5).kdr_thlms.gbar = 0.075
        self.dend1(0.5).kc.gbar = 0.02  # 0.012
        self.dend1(0.5).ka.gbar = 0.001  # 0.03
        self.dend1(0.5).km.gbar = 0  # // 0.0005
        self.dend1(0.5).k2.gbar = 0.002
        self.dend1(0.5).cal_thlms.gbar = 0.00025  # 0.0005
        self.dend1(0.5).cat_thlms.gbar = 0.003  # 0.0005
        self.dend1(0.5).ar.gbar = 0.0003  # 0.00025
        self.dend1(0.5).cad.beta = 0.05  # 0.02
        self.dend1(0.5).cad.phi = 104000.  # 52000.
        self.dend1(0.5).pas.g = 1 / 100
        self.dend1(0.5).pas.e = -70
        self.dend1.Ra = 175

        self.dend2(0.5).naf_tcr.gbar = 0.1  # 0.005  # 0.1
        self.dend2(0.5).napf_tcr.gbar = 0.0002  # 1.E-05  # 0.0002
        self.dend2(0.5).kdr_thlms.gbar = 0.075
        self.dend2(0.5).kc.gbar = 0.02  # 0.012
        self.dend2(0.5).ka.gbar = 0.001  # 0.03
        self.dend2(0.5).km.gbar = 0  # // 0.0005
        self.dend2(0.5).k2.gbar = 0.002
        self.dend2(0.5).cal_thlms.gbar = 0.00025  # 0.0005
        self.dend2(0.5).cat_thlms.gbar = 0.0005
        self.dend2(0.5).ar.gbar = 0.0003  # 0.00025
        self.dend2(0.5).cad.beta = 0.05  # 0.02
        self.dend2(0.5).cad.phi = 104000.  # 52000.
        self.dend2(0.5).pas.g = 1 / 100
        self.dend2(0.5).pas.e = -70
        self.dend2.Ra = 175

        self.dend3(0.5).naf_tcr.gbar = 0.1  # 0.005  # 0.1
        self.dend3(0.5).napf_tcr.gbar = 0.0002  # 1.E-05  # 0.0002
        self.dend3(0.5).kdr_thlms.gbar = 0.075
        self.dend3(0.5).kc.gbar = 0.02  # 0.012
        self.dend3(0.5).ka.gbar = 0.001  # 0.03
        self.dend3(0.5).km.gbar = 0  # // 0.0005
        self.dend3(0.5).k2.gbar = 0.002
        self.dend3(0.5).cal_thlms.gbar = 0.00025  # 0.0005
        self.dend3(0.5).cat_thlms.gbar = 0.0005
        self.dend3(0.5).ar.gbar = 0.0003  # 0.00025
        self.dend3(0.5).cad.beta = 0.05  # 0.02
        self.dend3(0.5).cad.phi = 104000  # .52000.
        self.dend3(0.5).pas.g = 1 / 100
        self.dend3(0.5).pas.e = -70
        self.dend3.Ra = 175

        self.dend4(0.5).naf_tcr.gbar = 0.1
        self.dend4(0.5).napf_tcr.gbar = 0.0002  # 1.E-05  # 0.0002
        self.dend4(0.5).kdr_thlms.gbar = 0.075
        self.dend4(0.5).kc.gbar = 0.012
        self.dend4(0.5).ka.gbar = 0.03
        self.dend4(0.5).km.gbar = 0  # // 0.0005
        self.dend4(0.5).k2.gbar = 0.002
        self.dend4(0.5).cal_thlms.gbar = 0.0005
        self.dend4(0.5).cat_thlms.gbar = 0.0005
        self.dend4(0.5).ar.gbar = 0.00025
        self.dend4(0.5).cad.beta = 0.02
        self.dend4(0.5).cad.phi = 104000.  # 52000.
        self.dend4(0.5).pas.g = 1 / 100
        self.dend4(0.5).pas.e = -70
        self.dend4.Ra = 175

        # ---------------axon----------------
        for mechanism_a in ['Nafin', 'kdrin', 'pas']:
            self.axon.insert(mechanism_a)

        self.axon(0.5).Nafin.gnafbar = 0.4
        self.axon(0.5).kdrin.gkdrbar = 0.4  # 0.001
        self.axon(0.5).pas.g = 0.001  # 0.005
        self.axon(0.5).pas.e = -70
        self.axon.Ra = 100
        self.axon.cm = 1.2

        for sec in self.all:
            sec.cm = 0.9
            sec.ena = 50.
            sec.ek = -95
            # sec.cm = 4.65
            # sec.Ra = 65.22
            # sec.pas.e = -85.15087381998698

        self.k_vec = h.Vector().record(self.soma(0.5)._ref_ik)
        self.na_vec = h.Vector().record(self.soma(0.5)._ref_ina)
        self.na_concentration = h.Vector().record(self.soma(0.5)._ref_nai)
        self.k_concentration = h.Vector().record(self.soma(0.5)._ref_ki)
        self.v_vec = h.Vector().record(self.soma(0.5)._ref_v)


class nRT(Cell):  #
    def __init__(self, x, y, z, num):
        super().__init__(x, y, z, num)
        self.id = 15
        self.Excitatory = -1
        self.name = 'nucleus reticularis'

        # ---------------soma----------------
        for mechanism_s in ['extracellular', 'naf2', 'napf', 'kdr_fs',
                            'kc', 'ka', 'km', 'k2',
                            'kahp_slower', 'cal_thlms',
                            'cat_a', 'ar', 'cad', 'pas']:
            self.soma.insert(mechanism_s)

        self.soma(0.5).naf2.gbar = 0.06  # 0.4
        self.soma(0.5).napf.gbar = 0.0006
        self.soma(0.5).kdr_fs.gbar = 0.06  # 0.4
        self.soma(0.5).kc.gbar = 0.01
        self.soma(0.5).ka.gbar = 0.005  # 0.001
        self.soma(0.5).km.gbar = 0.0005
        self.soma(0.5).k2.gbar = 0.0005
        self.soma(0.5).kahp_slower.gbar = 0.0001
        self.soma(0.5).cal_thlms.gbar = 0.0005
        self.soma(0.5).cat_a.gbar = 5.E-05
        self.soma(0.5).ar.gbar = 2.5E-05
        self.soma(0.5).cad.beta = 0.02
        self.soma(0.5).cad.phi = 10400.
        self.soma(0.5).pas.g = 1 / 100  # 3.78787879E-05
        self.soma(0.5).pas.e = -75
        self.soma.Ra = 250.

        # ---------------dend----------------
        for mechanism_d in ['naf2', 'napf', 'kdr_fs',
                            'kc', 'ka', 'km', 'k2',
                            'kahp_slower', 'cal_thlms',
                            'cat_a', 'ar', 'cad', 'pas']:
            self.dend.insert(mechanism_d)
            self.dend1.insert(mechanism_d)
            self.dend2.insert(mechanism_d)
            self.dend3.insert(mechanism_d)
            self.dend4.insert(mechanism_d)

        self.dend(0.5).naf2.gbar = 0.06
        self.dend(0.5).napf.gbar = 0.0006
        self.dend(0.5).kdr_fs.gbar = 0.06
        self.dend(0.5).kc.gbar = 0.01
        self.dend(0.5).ka.gbar = 0.005
        self.dend(0.5).km.gbar = 0.0005
        self.dend(0.5).k2.gbar = 0.0005
        self.dend(0.5).kahp_slower.gbar = 0.0001
        self.dend(0.5).cal_thlms.gbar = 0.0005
        self.dend(0.5).cat_a.gbar = 5.E-05
        self.dend(0.5).ar.gbar = 2.5E-05
        self.dend(0.5).cad.beta = 0.05  # 0.02
        self.dend(0.5).cad.phi = 260000.  # 10400.
        self.dend(0.5).pas.g = 1 / 100
        self.dend(0.5).pas.e = -75
        self.dend.Ra = 250

        self.dend1(0.5).naf2.gbar = 0.06
        self.dend1(0.5).napf.gbar = 0.0006
        self.dend1(0.5).kdr_fs.gbar = 0.06
        self.dend1(0.5).kc.gbar = 0.01
        self.dend1(0.5).ka.gbar = 0.005
        self.dend1(0.5).km.gbar = 0.0005
        self.dend1(0.5).k2.gbar = 0.0005
        self.dend1(0.5).kahp_slower.gbar = 0.0001
        self.dend1(0.5).cal_thlms.gbar = 0.0005
        self.dend1(0.5).cat_a.gbar = 5.E-05
        self.dend1(0.5).ar.gbar = 2.5E-05
        self.dend1(0.5).cad.beta = 0.02
        self.dend1(0.5).cad.phi = 260000.  # 10400.
        self.dend1(0.5).pas.g = 1 / 100
        self.dend1(0.5).pas.e = -75
        self.dend1.Ra = 250

        self.dend2(0.5).naf2.gbar = 0.01  # 0.06
        self.dend2(0.5).napf.gbar = 0.0001  # 0.0006
        self.dend2(0.5).kdr_fs.gbar = 0.01  # 0.06
        self.dend2(0.5).kc.gbar = 0.01
        self.dend2(0.5).ka.gbar = 0.001  # 0.005
        self.dend2(0.5).km.gbar = 0.0005
        self.dend2(0.5).k2.gbar = 0.0005
        self.dend2(0.5).kahp_slower.gbar = 0.0001
        self.dend2(0.5).cal_thlms.gbar = 0.0005
        self.dend2(0.5).cat_a.gbar = 0.002  # 5.E-05
        self.dend2(0.5).ar.gbar = 2.5E-05
        self.dend2(0.5).cad.beta = 0.05  # 0.02
        self.dend2(0.5).cad.phi = 260000.  # 10400.
        self.dend2(0.5).pas.g = 1 / 100
        self.dend2(0.5).pas.e = -75
        self.dend2.Ra = 250

        self.dend3(0.5).naf2.gbar = 0.01  # 0.06
        self.dend3(0.5).napf.gbar = 0.0001  # 0.0006
        self.dend3(0.5).kdr_fs.gbar = 0.01  # 0.06
        self.dend3(0.5).kc.gbar = 0.01
        self.dend3(0.5).ka.gbar = 0.001  # 0.005
        self.dend3(0.5).km.gbar = 0.0005
        self.dend3(0.5).k2.gbar = 0.0005
        self.dend3(0.5).kahp_slower.gbar = 0.0001
        self.dend3(0.5).cal_thlms.gbar = 0.0005
        self.dend3(0.5).cat_a.gbar = 0.002  # 5.E-05
        self.dend3(0.5).ar.gbar = 2.5E-05
        self.dend3(0.5).cad.beta = 0.05  # 0.02
        self.dend3(0.5).cad.phi = 260000.  # 10400.
        self.dend3(0.5).pas.g = 1 / 100
        self.dend3(0.5).pas.e = -75
        self.dend3.Ra = 250

        self.dend4(0.5).naf2.gbar = 0.01  # 0.06
        self.dend4(0.5).napf.gbar = 0.0001  # 0.0006
        self.dend4(0.5).kdr_fs.gbar = 0.01  # 0.06
        self.dend4(0.5).kc.gbar = 0.01
        self.dend4(0.5).ka.gbar = 0.001  # 0.005
        self.dend4(0.5).km.gbar = 0.0005
        self.dend4(0.5).k2.gbar = 0.0005
        self.dend4(0.5).kahp_slower.gbar = 0.0001
        self.dend4(0.5).cal_thlms.gbar = 0.0005
        self.dend4(0.5).cat_a.gbar = 0.002  # 5.E-05
        self.dend4(0.5).ar.gbar = 2.5E-05
        self.dend4(0.5).cad.beta = 0.05  # 0.02
        self.dend4(0.5).cad.phi = 260000.  # 10400.
        self.dend4(0.5).pas.g = 1 / 100
        self.dend4(0.5).pas.e = -75
        self.dend4.Ra = 250

        # ---------------axon----------------
        for mechanism_a in ['Nafin', 'kdrin', 'pas']:
            self.axon.insert(mechanism_a)

        self.axon(0.5).Nafin.gnafbar = 0.4
        self.axon(0.5).kdrin.gkdrbar = 0.4  # 0.001
        self.axon(0.5).pas.g = 0.001  # 0.0002
        self.axon(0.5).pas.e = -75  # -70
        self.axon.Ra = 100
        self.axon.cm = 1.2

        for sec in self.all:
            sec.cm = 1.  # 0.9
            sec.ena = 50.
            sec.ek = -100  # -95

        self.k_vec = h.Vector().record(self.soma(0.5)._ref_ik)
        self.na_vec = h.Vector().record(self.soma(0.5)._ref_ina)
        self.na_concentration = h.Vector().record(self.soma(0.5)._ref_nai)
        self.k_concentration = h.Vector().record(self.soma(0.5)._ref_ki)
        self.v_vec = h.Vector().record(self.soma(0.5)._ref_v)
