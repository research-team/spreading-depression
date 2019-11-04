#include <stdio.h>
#include "hocdec.h"
extern int nrnmpi_myid;
extern int nrn_nobanner_;

extern void _accum_reg(void);
extern void _cal2_reg(void);
extern void _capump_reg(void);
extern void _getconc_reg(void);
extern void _hzclamp_reg(void);
extern void _hzclampna_reg(void);
extern void _it_reg(void);
extern void _itot_reg(void);
extern void _ka_reg(void);
extern void _kdr_reg(void);
extern void _kdrglia_reg(void);
extern void _kir_reg(void);
extern void _leak_reg(void);
extern void _na_reg(void);
extern void _nakpump_reg(void);
extern void _nap_reg(void);
extern void _nastim_reg(void);
extern void _nax_reg(void);
extern void _nmda_reg(void);
extern void _sk_reg(void);
extern void _xiong_reg(void);

void modl_reg(){
  if (!nrn_nobanner_) if (nrnmpi_myid < 1) {
    fprintf(stderr, "Additional mechanisms from files\n");

    fprintf(stderr," accum.mod");
    fprintf(stderr," cal2.mod");
    fprintf(stderr," capump.mod");
    fprintf(stderr," getconc.mod");
    fprintf(stderr," hzclamp.mod");
    fprintf(stderr," hzclampna.mod");
    fprintf(stderr," it.mod");
    fprintf(stderr," itot.mod");
    fprintf(stderr," ka.mod");
    fprintf(stderr," kdr.mod");
    fprintf(stderr," kdrglia.mod");
    fprintf(stderr," kir.mod");
    fprintf(stderr," leak.mod");
    fprintf(stderr," na.mod");
    fprintf(stderr," nakpump.mod");
    fprintf(stderr," nap.mod");
    fprintf(stderr," nastim.mod");
    fprintf(stderr," nax.mod");
    fprintf(stderr," nmda.mod");
    fprintf(stderr," sk.mod");
    fprintf(stderr," xiong.mod");
    fprintf(stderr, "\n");
  }
  _accum_reg();
  _cal2_reg();
  _capump_reg();
  _getconc_reg();
  _hzclamp_reg();
  _hzclampna_reg();
  _it_reg();
  _itot_reg();
  _ka_reg();
  _kdr_reg();
  _kdrglia_reg();
  _kir_reg();
  _leak_reg();
  _na_reg();
  _nakpump_reg();
  _nap_reg();
  _nastim_reg();
  _nax_reg();
  _nmda_reg();
  _sk_reg();
  _xiong_reg();
}
