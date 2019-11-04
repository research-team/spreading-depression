from neuron import h, gui
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as pyplot
import math
#neuron.load_mechanisms("./mod")
from fiber import fiber

def set_recording_vectors(compartment):
    ''' recording voltage
    Parameters
    ----------
    compartment: NEURON section
        compartment for recording 
    Returns
    -------
    v_vec: h.Vector()
        recorded voltage
    t_vec: h.Vector()

        recorded time
    '''
    v_vec = h.Vector()   # Membrane potential vector at compartment
    t_vec = h.Vector()        # Time stamp vector
    v_vec.record(compartment(0.5)._ref_v)
    t_vec.record(h._ref_t)
    return v_vec, t_vec

def addpointers(cell, glia):
    for sec in cell.all:
        for sec_g in glia.all:
            h.setpointer(sec._ref_inag_accum, 'ina', sec_g)
            h.setpointer(sec._ref_icag_accum, 'ica', sec_g)
            h.setpointer(sec._ref_iclg_accum, 'icl', sec_g)
            h.setpointer(sec._ref_iag_accum, 'ia', sec_g)
            h.setpointer(sec._ref_diamg_accum, 'diam', sec_g)
            h.setpointer(sec_g._ref_kog_getconc, 'ko', sec)
            h.setpointer(sec_g._ref_naog_getconc, 'nao', sec)
            h.setpointer(sec_g._ref_caog_getconc, 'cao', sec)
            h.setpointer(sec_g._ref_clog_getconc, 'clo', sec)
            h.setpointer(sec_g._ref_aog_getconc, 'ao', sec)
            h.setpointer(sec_g._ref_kig_getconc, 'kg_accum', sec)
            h.setpointer(sec_g._ref_naig_getconc, 'nag_accum', sec)
            h.setpointer(sec_g._ref_caig_getconc, 'cag_accum', sec)
            h.setpointer(sec_g._ref_clig_getconc, 'clg_accum', sec)
            h.setpointer(sec_g._ref_aig_getconc, 'ag_accum', sec)

def balance(cell, vinit=-55):
    ''' voltage balance
    Parameters
    ----------
    cell: NEURON cell
        cell for balance
    vinit: int (mV)
        initialized voltage
    '''
    for sec in cell.all:
        if ((-(sec.ina_nattxs + sec.ina_navv1p8 + sec.ina_Nav1_3 + sec.ina_nakpump) / (vinit - sec.ena)) < 0):
            sec.pumpina_extrapump = -(sec.ina_nattxs + sec.ina_navv1p8 + sec.ina_Nav1_3 + sec.ina_nakpump)
        else:
            sec.gnaleak_leak = -(sec.ina_nattxs + sec.ina_navv1p8 + sec.ina_Nav1_3 + sec.ina_nakpump) / (vinit - sec.ena)

        if ((-(sec.ik_kdr + sec.ik_nakpump + sec.ik_kap + sec.ik_kad) / (vinit - sec.ek)) < 0):
            sec.pumpik_extrapump = -(sec.ik_kdr + sec.ik_nakpump + sec.ik_kap + sec.ik_kad)
        else:
            sec.gkleak_leak = -(sec.ik_kdr + sec.ik_nakpump + sec.ik_kap + sec.ik_kad) / (vinit - sec.ek)

def init(cell, glia, vinit=-70, vglia=-88):
    ''' simulation control 
    Parameters
    ----------
    cell: NEURON cell
        cell for simulation
    tstop: int (ms)
        simulation time
    vinit: int (mV)
        initialized voltage
    '''
    h.finitialize()
    for sec in cell.all:
        sec.v = vinit
    for sec in glia.all:
      sec.v = vglia
      sec.nai = setnag_accum
      sec.ki = setkg_accum
      sec.cli = setclg_accum
      sec.ai = setag_accum
    
    h.fcurrent()
    

def simulate():
    h.frecord_init()
    h.tstop = tstop
    h.run()

def show_output(v_vec, t_vec):
    ''' show graphs 
    Parameters
    ----------
    v_vec: h.Vector()
        recorded voltage
    t_vec: h.Vector()
        recorded time
    '''
    dend_plot = pyplot.plot(t_vec, v_vec)
    pyplot.xlabel('time (ms)')
    pyplot.ylabel('mV')

if __name__ == '__main__':
    cell = fiber(False)
    glia = fiber(True)
    addpointers(cell,glia)
    for sec in h.allsec():
        h.psection(sec=sec) #show parameters of each section
    # branch_vec, t_vec = set_recording_vectors(cell.branch)
    # simulate(cell, glia)
    # show_output(branch_vec, t_vec)
    # pyplot.show()