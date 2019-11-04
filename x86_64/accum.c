/* Created by Language version: 7.5.0 */
/* NOT VECTORIZED */
#define NRN_VECTORIZED 0
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include "scoplib_ansi.h"
#undef PI
#define nil 0
#include "md1redef.h"
#include "section.h"
#include "nrniv_mf.h"
#include "md2redef.h"
 static void _difusfunc(ldifusfunc2_t, _NrnThread*);
 
#if METHOD3
extern int _method3;
#endif

#if !NRNGPU
#undef exp
#define exp hoc_Exp
extern double hoc_Exp(double);
#endif
 
#define nrn_init _nrn_init__accum
#define _nrn_initial _nrn_initial__accum
#define nrn_cur _nrn_cur__accum
#define _nrn_current _nrn_current__accum
#define nrn_jacob _nrn_jacob__accum
#define nrn_state _nrn_state__accum
#define _net_receive _net_receive__accum 
#define state state__accum 
 
#define _threadargscomma_ /**/
#define _threadargsprotocomma_ /**/
#define _threadargs_ /**/
#define _threadargsproto_ /**/
 	/*SUPPRESS 761*/
	/*SUPPRESS 762*/
	/*SUPPRESS 763*/
	/*SUPPRESS 765*/
	 extern double *getarg();
 static double *_p; static Datum *_ppvar;
 
#define t nrn_threads->_t
#define dt nrn_threads->_dt
#define tau _p[0]
#define k1buf _p[1]
#define k2buf _p[2]
#define setvolout _p[3]
#define setvolglia _p[4]
#define osmin _p[5]
#define electin _p[6]
#define osmout _p[7]
#define electout _p[8]
#define osmglia _p[9]
#define electglia _p[10]
#define deltan _p[11]
#define nag _p[12]
#define kg _p[13]
#define ag _p[14]
#define clg _p[15]
#define cag _p[16]
#define volin _p[17]
#define volout _p[18]
#define volglia _p[19]
#define qki _p[20]
#define qko _p[21]
#define qkg _p[22]
#define qnai _p[23]
#define qnao _p[24]
#define qnag _p[25]
#define qai _p[26]
#define qao _p[27]
#define qag _p[28]
#define qcli _p[29]
#define qclo _p[30]
#define qcai _p[31]
#define qcao _p[32]
#define qcag _p[33]
#define na (_p + 34)
#define k (_p + 37)
#define a (_p + 40)
#define cl (_p + 43)
#define ca (_p + 46)
#define vol (_p + 48)
#define CaBuffer _p[51]
#define Buffer _p[52]
#define pump _p[53]
#define pumpca _p[54]
#define catot _p[55]
#define ina _p[56]
#define ik _p[57]
#define icl _p[58]
#define ia _p[59]
#define ica _p[60]
#define B0 _p[61]
#define naflux (_p + 62)
#define clflux (_p + 65)
#define aflux (_p + 68)
#define kflux (_p + 71)
#define caflux (_p + 74)
#define deltag _p[77]
#define nai _p[78]
#define ki _p[79]
#define ai _p[80]
#define cli _p[81]
#define cai _p[82]
#define nao _p[83]
#define ko _p[84]
#define ao _p[85]
#define clo _p[86]
#define cao _p[87]
#define qclg _p[88]
#define Dna (_p + 89)
#define Dk (_p + 92)
#define Da (_p + 95)
#define Dcl (_p + 98)
#define Dca (_p + 101)
#define Dvol (_p + 103)
#define DCaBuffer _p[106]
#define DBuffer _p[107]
#define Dpump _p[108]
#define Dpumpca _p[109]
#define Dcatot _p[110]
#define _g _p[111]
#define _ion_ina	*_ppvar[0]._pval
#define _ion_nao	*_ppvar[1]._pval
#define _ion_nai	*_ppvar[2]._pval
#define _ion_dinadv	*_ppvar[3]._pval
#define _style_na	*((int*)_ppvar[4]._pvoid)
#define _ion_ik	*_ppvar[5]._pval
#define _ion_ko	*_ppvar[6]._pval
#define _ion_ki	*_ppvar[7]._pval
#define _ion_dikdv	*_ppvar[8]._pval
#define _style_k	*((int*)_ppvar[9]._pvoid)
#define _ion_icl	*_ppvar[10]._pval
#define _ion_clo	*_ppvar[11]._pval
#define _ion_cli	*_ppvar[12]._pval
#define _ion_dicldv	*_ppvar[13]._pval
#define _style_cl	*((int*)_ppvar[14]._pvoid)
#define _ion_ia	*_ppvar[15]._pval
#define _ion_ao	*_ppvar[16]._pval
#define _ion_ai	*_ppvar[17]._pval
#define _style_a	*((int*)_ppvar[18]._pvoid)
#define _ion_diadv	*_ppvar[19]._pval
#define _ion_ica	*_ppvar[20]._pval
#define _ion_cao	*_ppvar[21]._pval
#define _ion_cai	*_ppvar[22]._pval
#define _ion_dicadv	*_ppvar[23]._pval
#define _style_ca	*((int*)_ppvar[24]._pvoid)
#define diamg	*_ppvar[25]._pval
#define _p_diamg	_ppvar[25]._pval
#define inag	*_ppvar[26]._pval
#define _p_inag	_ppvar[26]._pval
#define ikg	*_ppvar[27]._pval
#define _p_ikg	_ppvar[27]._pval
#define iclg	*_ppvar[28]._pval
#define _p_iclg	_ppvar[28]._pval
#define iag	*_ppvar[29]._pval
#define _p_iag	_ppvar[29]._pval
#define diam	*_ppvar[30]._pval
 
#if MAC
#if !defined(v)
#define v _mlhv
#endif
#if !defined(h)
#define h _mlhh
#endif
#endif
 
#if defined(__cplusplus)
extern "C" {
#endif
 static int hoc_nrnpointerindex =  25;
 /* external NEURON variables */
 /* declaration of user functions */
 static int _mechtype;
extern void _nrn_cacheloop_reg(int, int);
extern void hoc_register_prop_size(int, int, int);
extern void hoc_register_limits(int, HocParmLimits*);
extern void hoc_register_units(int, HocParmUnits*);
extern void nrn_promote(Prop*, int, int);
extern Memb_func* memb_func;
 extern void _nrn_setdata_reg(int, void(*)(Prop*));
 static void _setdata(Prop* _prop) {
 _p = _prop->param; _ppvar = _prop->dparam;
 }
 static void _hoc_setdata() {
 Prop *_prop, *hoc_getdata_range(int);
 _prop = hoc_getdata_range(_mechtype);
   _setdata(_prop);
 hoc_retpushx(1.);
}
 /* connect user functions to hoc names */
 static VoidFunc hoc_intfunc[] = {
 "setdata_accum", _hoc_setdata,
 0, 0
};
 /* declare global and static user variables */
#define Difca Difca_accum
 double Difca = 0.6;
#define Difcl Difcl_accum
 double Difcl = 2.03;
#define Difk Difk_accum
 double Difk = 1.96;
#define Difna Difna_accum
 double Difna = 1.33;
#define Kd Kd_accum
 double Kd = 0.008;
#define TotalBuffer TotalBuffer_accum
 double TotalBuffer = 1.562;
#define method method_accum
 double method = 0;
#define minvolisvf minvolisvf_accum
 double minvolisvf = 0.04;
#define setvolin setvolin_accum
 double setvolin = 1;
#define setcag setcag_accum
 double setcag = 0;
#define setag setag_accum
 double setag = 0;
#define setclg setclg_accum
 double setclg = 0;
#define setkg setkg_accum
 double setkg = 0;
#define setnag setnag_accum
 double setnag = 0;
 /* some parameters have upper and lower limits */
 static HocParmLimits _hoc_parm_limits[] = {
 0,0,0
};
 static HocParmUnits _hoc_parm_units[] = {
 "Difna_accum", "um2/ms",
 "Difk_accum", "um2/ms",
 "Difcl_accum", "um2/ms",
 "Difca_accum", "um2/ms",
 "TotalBuffer_accum", "mM",
 "Kd_accum", "mM",
 "tau_accum", "ms",
 "k1buf_accum", "/mM-ms",
 "k2buf_accum", "/ms",
 "ca_accum", "mM",
 "pump_accum", "mol/cm2",
 "pumpca_accum", "mol/cm2",
 "osmin_accum", "mM",
 "electin_accum", "mM",
 "osmout_accum", "mM",
 "electout_accum", "mM",
 "osmglia_accum", "mM",
 "electglia_accum", "mM",
 "diamg_accum", "um",
 "inag_accum", "mA/cm2",
 "ikg_accum", "mA/cm2",
 "iclg_accum", "mA/cm2",
 "iag_accum", "mA/cm2",
 0,0
};
 static double Buffer0 = 0;
 static double CaBuffer0 = 0;
 static double a0 = 0;
 static double catot0 = 0;
 static double ca0 = 0;
 static double cl0 = 0;
 static double delta_t = 0.01;
 static double k0 = 0;
 static double na0 = 0;
 static double pumpca0 = 0;
 static double pump0 = 0;
 static double v = 0;
 static double vol0 = 0;
 /* connect global user variables to hoc */
 static DoubScal hoc_scdoub[] = {
 "Difna_accum", &Difna_accum,
 "Difk_accum", &Difk_accum,
 "Difcl_accum", &Difcl_accum,
 "Difca_accum", &Difca_accum,
 "TotalBuffer_accum", &TotalBuffer_accum,
 "Kd_accum", &Kd_accum,
 "setvolin_accum", &setvolin_accum,
 "minvolisvf_accum", &minvolisvf_accum,
 "setnag_accum", &setnag_accum,
 "setkg_accum", &setkg_accum,
 "setclg_accum", &setclg_accum,
 "setag_accum", &setag_accum,
 "setcag_accum", &setcag_accum,
 "method_accum", &method_accum,
 0,0
};
 static DoubVec hoc_vdoub[] = {
 0,0,0
};
 static double _sav_indep;
 static void nrn_alloc(Prop*);
static void  nrn_init(_NrnThread*, _Memb_list*, int);
static void nrn_state(_NrnThread*, _Memb_list*, int);
 static void nrn_cur(_NrnThread*, _Memb_list*, int);
static void  nrn_jacob(_NrnThread*, _Memb_list*, int);
 
static int _ode_count(int);
static void _ode_map(int, double**, double**, double*, Datum*, double*, int);
static void _ode_spec(_NrnThread*, _Memb_list*, int);
static void _ode_matsol(_NrnThread*, _Memb_list*, int);
 
#define _cvode_ieq _ppvar[31]._i
 static void _ode_synonym(int, double**, Datum**);
 static void _ode_matsol_instance1(_threadargsproto_);
 /* connect range variables in _p that hoc is supposed to know about */
 static const char *_mechanism[] = {
 "7.5.0",
"accum",
 "tau_accum",
 "k1buf_accum",
 "k2buf_accum",
 "setvolout_accum",
 "setvolglia_accum",
 0,
 "osmin_accum",
 "electin_accum",
 "osmout_accum",
 "electout_accum",
 "osmglia_accum",
 "electglia_accum",
 "deltan_accum",
 "nag_accum",
 "kg_accum",
 "ag_accum",
 "clg_accum",
 "cag_accum",
 "volin_accum",
 "volout_accum",
 "volglia_accum",
 "qki_accum",
 "qko_accum",
 "qkg_accum",
 "qnai_accum",
 "qnao_accum",
 "qnag_accum",
 "qai_accum",
 "qao_accum",
 "qag_accum",
 "qcli_accum",
 "qclo_accum",
 "qcai_accum",
 "qcao_accum",
 "qcag_accum",
 0,
 "na_accum[3]",
 "k_accum[3]",
 "a_accum[3]",
 "cl_accum[3]",
 "ca_accum[2]",
 "vol_accum[3]",
 "CaBuffer_accum",
 "Buffer_accum",
 "pump_accum",
 "pumpca_accum",
 "catot_accum",
 0,
 "diamg_accum",
 "inag_accum",
 "ikg_accum",
 "iclg_accum",
 "iag_accum",
 0};
 static Symbol* _morphology_sym;
 static Symbol* _na_sym;
 static int _type_ina;
 static Symbol* _k_sym;
 static int _type_ik;
 static Symbol* _cl_sym;
 static int _type_icl;
 static Symbol* _a_sym;
 static int _type_ia;
 static Symbol* _ca_sym;
 static int _type_ica;
 
extern Prop* need_memb(Symbol*);

static void nrn_alloc(Prop* _prop) {
	Prop *prop_ion;
	double *_p; Datum *_ppvar;
 	_p = nrn_prop_data_alloc(_mechtype, 112, _prop);
 	/*initialize range parameters*/
 	tau = 100;
 	k1buf = 20;
 	k2buf = 0.5;
 	setvolout = 1;
 	setvolglia = 1;
 	_prop->param = _p;
 	_prop->param_size = 112;
 	_ppvar = nrn_prop_datum_alloc(_mechtype, 32, _prop);
 	_prop->dparam = _ppvar;
 	/*connect ionic variables to this model*/
 prop_ion = need_memb(_morphology_sym);
 	_ppvar[30]._pval = &prop_ion->param[0]; /* diam */
 prop_ion = need_memb(_na_sym);
  _type_ina = prop_ion->_type;
 nrn_check_conc_write(_prop, prop_ion, 1);
 nrn_check_conc_write(_prop, prop_ion, 0);
 nrn_promote(prop_ion, 3, 0);
 	_ppvar[0]._pval = &prop_ion->param[3]; /* ina */
 	_ppvar[1]._pval = &prop_ion->param[2]; /* nao */
 	_ppvar[2]._pval = &prop_ion->param[1]; /* nai */
 	_ppvar[3]._pval = &prop_ion->param[4]; /* _ion_dinadv */
 	_ppvar[4]._pvoid = (void*)(&(prop_ion->dparam[0]._i)); /* iontype for na */
 prop_ion = need_memb(_k_sym);
  _type_ik = prop_ion->_type;
 nrn_check_conc_write(_prop, prop_ion, 1);
 nrn_check_conc_write(_prop, prop_ion, 0);
 nrn_promote(prop_ion, 3, 0);
 	_ppvar[5]._pval = &prop_ion->param[3]; /* ik */
 	_ppvar[6]._pval = &prop_ion->param[2]; /* ko */
 	_ppvar[7]._pval = &prop_ion->param[1]; /* ki */
 	_ppvar[8]._pval = &prop_ion->param[4]; /* _ion_dikdv */
 	_ppvar[9]._pvoid = (void*)(&(prop_ion->dparam[0]._i)); /* iontype for k */
 prop_ion = need_memb(_cl_sym);
  _type_icl = prop_ion->_type;
 nrn_check_conc_write(_prop, prop_ion, 1);
 nrn_check_conc_write(_prop, prop_ion, 0);
 nrn_promote(prop_ion, 3, 0);
 	_ppvar[10]._pval = &prop_ion->param[3]; /* icl */
 	_ppvar[11]._pval = &prop_ion->param[2]; /* clo */
 	_ppvar[12]._pval = &prop_ion->param[1]; /* cli */
 	_ppvar[13]._pval = &prop_ion->param[4]; /* _ion_dicldv */
 	_ppvar[14]._pvoid = (void*)(&(prop_ion->dparam[0]._i)); /* iontype for cl */
 prop_ion = need_memb(_a_sym);
  _type_ia = prop_ion->_type;
 nrn_check_conc_write(_prop, prop_ion, 1);
 nrn_check_conc_write(_prop, prop_ion, 0);
 nrn_promote(prop_ion, 3, 0);
 	_ppvar[15]._pval = &prop_ion->param[3]; /* ia */
 	_ppvar[16]._pval = &prop_ion->param[2]; /* ao */
 	_ppvar[17]._pval = &prop_ion->param[1]; /* ai */
 	_ppvar[18]._pvoid = (void*)(&(prop_ion->dparam[0]._i)); /* iontype for a */
 	_ppvar[19]._pval = &prop_ion->param[4]; /* _ion_diadv */
 prop_ion = need_memb(_ca_sym);
  _type_ica = prop_ion->_type;
 nrn_check_conc_write(_prop, prop_ion, 1);
 nrn_check_conc_write(_prop, prop_ion, 0);
 nrn_promote(prop_ion, 3, 0);
 	_ppvar[20]._pval = &prop_ion->param[3]; /* ica */
 	_ppvar[21]._pval = &prop_ion->param[2]; /* cao */
 	_ppvar[22]._pval = &prop_ion->param[1]; /* cai */
 	_ppvar[23]._pval = &prop_ion->param[4]; /* _ion_dicadv */
 	_ppvar[24]._pvoid = (void*)(&(prop_ion->dparam[0]._i)); /* iontype for ca */
 
}
 static void _initlists();
  /* some states have an absolute tolerance */
 static Symbol** _atollist;
 static HocStateTolerance _hoc_state_tol[] = {
 "ca_accum", 0.0001,
 0,0
};
 static void _update_ion_pointer(Datum*);
 extern Symbol* hoc_lookup(const char*);
extern void _nrn_thread_reg(int, int, void(*)(Datum*));
extern void _nrn_thread_table_reg(int, void(*)(double*, Datum*, Datum*, _NrnThread*, int));
extern void hoc_register_tolerance(int, HocStateTolerance*, Symbol***);
extern void _cvode_abstol( Symbol**, double*, int);

 void _accum_reg() {
	int _vectorized = 0;
  _initlists();
 	ion_reg("na", -10000.);
 	ion_reg("k", -10000.);
 	ion_reg("cl", -1.0);
 	ion_reg("a", -1.0);
 	ion_reg("ca", 2.0);
 	_morphology_sym = hoc_lookup("morphology");
 	_na_sym = hoc_lookup("na_ion");
 	_k_sym = hoc_lookup("k_ion");
 	_cl_sym = hoc_lookup("cl_ion");
 	_a_sym = hoc_lookup("a_ion");
 	_ca_sym = hoc_lookup("ca_ion");
 	register_mech(_mechanism, nrn_alloc,nrn_cur, nrn_jacob, nrn_state, nrn_init, hoc_nrnpointerindex, 0);
 _mechtype = nrn_get_mechtype(_mechanism[1]);
     _nrn_setdata_reg(_mechtype, _setdata);
     _nrn_thread_reg(_mechtype, 2, _update_ion_pointer);
  hoc_register_prop_size(_mechtype, 112, 32);
  hoc_register_dparam_semantics(_mechtype, 0, "na_ion");
  hoc_register_dparam_semantics(_mechtype, 1, "na_ion");
  hoc_register_dparam_semantics(_mechtype, 2, "na_ion");
  hoc_register_dparam_semantics(_mechtype, 3, "na_ion");
  hoc_register_dparam_semantics(_mechtype, 4, "#na_ion");
  hoc_register_dparam_semantics(_mechtype, 5, "k_ion");
  hoc_register_dparam_semantics(_mechtype, 6, "k_ion");
  hoc_register_dparam_semantics(_mechtype, 7, "k_ion");
  hoc_register_dparam_semantics(_mechtype, 8, "k_ion");
  hoc_register_dparam_semantics(_mechtype, 9, "#k_ion");
  hoc_register_dparam_semantics(_mechtype, 10, "cl_ion");
  hoc_register_dparam_semantics(_mechtype, 11, "cl_ion");
  hoc_register_dparam_semantics(_mechtype, 12, "cl_ion");
  hoc_register_dparam_semantics(_mechtype, 13, "cl_ion");
  hoc_register_dparam_semantics(_mechtype, 14, "#cl_ion");
  hoc_register_dparam_semantics(_mechtype, 15, "a_ion");
  hoc_register_dparam_semantics(_mechtype, 16, "a_ion");
  hoc_register_dparam_semantics(_mechtype, 17, "a_ion");
  hoc_register_dparam_semantics(_mechtype, 18, "#a_ion");
  hoc_register_dparam_semantics(_mechtype, 19, "a_ion");
  hoc_register_dparam_semantics(_mechtype, 20, "ca_ion");
  hoc_register_dparam_semantics(_mechtype, 21, "ca_ion");
  hoc_register_dparam_semantics(_mechtype, 22, "ca_ion");
  hoc_register_dparam_semantics(_mechtype, 23, "ca_ion");
  hoc_register_dparam_semantics(_mechtype, 24, "#ca_ion");
  hoc_register_dparam_semantics(_mechtype, 25, "pointer");
  hoc_register_dparam_semantics(_mechtype, 26, "pointer");
  hoc_register_dparam_semantics(_mechtype, 27, "pointer");
  hoc_register_dparam_semantics(_mechtype, 28, "pointer");
  hoc_register_dparam_semantics(_mechtype, 29, "pointer");
  hoc_register_dparam_semantics(_mechtype, 31, "cvodeieq");
  hoc_register_dparam_semantics(_mechtype, 30, "diam");
 	nrn_writes_conc(_mechtype, 0);
 	hoc_register_cvode(_mechtype, _ode_count, _ode_map, _ode_spec, _ode_matsol);
 	hoc_register_tolerance(_mechtype, _hoc_state_tol, &_atollist);
 	hoc_register_synonym(_mechtype, _ode_synonym);
 	hoc_register_ldifus1(_difusfunc);
 	hoc_register_var(hoc_scdoub, hoc_vdoub, hoc_intfunc);
 	ivoc_help("help ?1 accum /Users/sulgod/spreading-depression/x86_64/accum.mod\n");
 hoc_register_limits(_mechtype, _hoc_parm_limits);
 hoc_register_units(_mechtype, _hoc_parm_units);
 }
 static double FARADAY = 96485.309;
 static double PI = 3.14159;
 static double R = 8.3145;
 static double _zb , _zc , _zd ;
static int _reset;
static char *modelname = "accum";

static int error;
static int _ninits = 0;
static int _match_recurse=1;
static void _modl_cleanup(){ _match_recurse=1;}
 extern double *_getelm();
 
#define _MATELM1(_row,_col)	*(_getelm(_row + 1, _col + 1))
 
#define _RHS1(_arg) _coef1[_arg + 1]
 static double *_coef1;
 
#define _linmat1  1
 static void* _sparseobj1;
 static void* _cvsparseobj1;
 
static int _ode_spec1(_threadargsproto_);
/*static int _ode_matsol1(_threadargsproto_);*/
 static int _slist1[18], _dlist1[18]; static double *_temp1;
 static int state();
 
static int state ()
 {_reset=0;
 {
   double b_flux, f_flux, _term; int _i;
 {int _i; double _dt1 = 1.0/dt;
for(_i=0;_i<18;_i++){
  	_RHS1(_i) = -_dt1*(_p[_slist1[_i]] - _p[_dlist1[_i]]);
	_MATELM1(_i, _i) = _dt1;
      
}  
_RHS1(3) *= ( vol [ 0 ] * diam * diam * PI / 4.0) ;
_MATELM1(3, 3) *= ( vol [ 0 ] * diam * diam * PI / 4.0);  
for (_i=0; _i < 3; _i++) {
  	_RHS1(_i + 0) *= ( vol [ ((int) _i ) ] * diam * diam * PI / 4.0) ;
_MATELM1(_i + 0, _i + 0) *= ( vol [ ((int) _i ) ] * diam * diam * PI / 4.0);  } 
for (_i=0; _i < 2; _i++) {
  	_RHS1(_i + 4) *= ( vol [ ((int) _i ) ] * diam * diam * PI / 4.0) ;
_MATELM1(_i + 4, _i + 4) *= ( vol [ ((int) _i ) ] * diam * diam * PI / 4.0);  } 
for (_i=0; _i < 3; _i++) {
  	_RHS1(_i + 6) *= ( vol [ ((int) _i ) ] * diam * diam * PI / 4.0) ;
_MATELM1(_i + 6, _i + 6) *= ( vol [ ((int) _i ) ] * diam * diam * PI / 4.0);  } 
for (_i=0; _i < 3; _i++) {
  	_RHS1(_i + 9) *= ( vol [ ((int) _i ) ] * diam * diam * PI / 4.0) ;
_MATELM1(_i + 9, _i + 9) *= ( vol [ ((int) _i ) ] * diam * diam * PI / 4.0);  } 
for (_i=0; _i < 3; _i++) {
  	_RHS1(_i + 12) *= ( vol [ ((int) _i ) ] * diam * diam * PI / 4.0) ;
_MATELM1(_i + 12, _i + 12) *= ( vol [ ((int) _i ) ] * diam * diam * PI / 4.0);  } }
 deltan = ( nai + ki + cli + ai + cai - nao - ko - clo - ao - cao ) / tau ;
   deltag = ( nag + kg + clg + ag + cag - nao - ko - clo - ao - cao ) / tau ;
   if ( vol [ 1 ] <= minvolisvf  && deltan > 0.0 ) {
     deltan = 0.0 ;
     }
   if ( vol [ 1 ] <= minvolisvf  && deltag > 0.0 ) {
     deltag = 0.0 ;
     }
   if ( method  == 0.0 ) {
     /* ~ vol [ 0 ] <-> vol [ 1 ] ( deltan / ( diam * diam * PI / 4.0 ) , - deltan / ( diam * diam * PI / 4.0 ) )*/
 f_flux =  deltan / ( diam * diam * PI / 4.0 ) * vol [ 0] ;
 b_flux =  - deltan / ( diam * diam * PI / 4.0 ) * vol [ 1] ;
 _RHS1( 15 +  0) -= (f_flux - b_flux);
 _RHS1( 15 +  1) += (f_flux - b_flux);
 
 _term =  deltan / ( diam * diam * PI / 4.0 ) ;
 _MATELM1( 15 +  0 ,15 +  0)  += _term;
 _MATELM1( 15 +  1 ,15 +  0)  -= _term;
 _term =  - deltan / ( diam * diam * PI / 4.0 ) ;
 _MATELM1( 15 +  0 ,15 +  1)  -= _term;
 _MATELM1( 15 +  1 ,15 +  1)  += _term;
 /*REACTION*/
  /* ~ vol [ 1 ] <-> vol [ 2 ] ( - deltag / ( diam * diam * PI / 4.0 ) , deltag / ( diam * diam * PI / 4.0 ) )*/
 f_flux =  - deltag / ( diam * diam * PI / 4.0 ) * vol [ 1] ;
 b_flux =  deltag / ( diam * diam * PI / 4.0 ) * vol [ 2] ;
 _RHS1( 15 +  1) -= (f_flux - b_flux);
 _RHS1( 15 +  2) += (f_flux - b_flux);
 
 _term =  - deltag / ( diam * diam * PI / 4.0 ) ;
 _MATELM1( 15 +  1 ,15 +  1)  += _term;
 _MATELM1( 15 +  2 ,15 +  1)  -= _term;
 _term =  deltag / ( diam * diam * PI / 4.0 ) ;
 _MATELM1( 15 +  1 ,15 +  2)  -= _term;
 _MATELM1( 15 +  2 ,15 +  2)  += _term;
 /*REACTION*/
  }
   else {
     /* ~ vol [ 0 ] < < ( deltan / ( diam * diam * PI / 4.0 ) )*/
 f_flux = b_flux = 0.;
 _RHS1( 15 +  0) += (b_flux =   ( deltan / ( diam * diam * PI / 4.0 ) ) );
 /*FLUX*/
  /* ~ vol [ 1 ] < < ( ( - deltan - deltag ) / ( diam * diam * PI / 4.0 ) )*/
 f_flux = b_flux = 0.;
 _RHS1( 15 +  1) += (b_flux =   ( ( - deltan - deltag ) / ( diam * diam * PI / 4.0 ) ) );
 /*FLUX*/
  /* ~ vol [ 2 ] < < ( ( deltag ) / ( diam * diam * PI / 4.0 ) )*/
 f_flux = b_flux = 0.;
 _RHS1( 15 +  2) += (b_flux =   ( ( deltag ) / ( diam * diam * PI / 4.0 ) ) );
 /*FLUX*/
  }
   /* COMPARTMENT _li , vol [ ((int) _i ) ] * diam * diam * PI / 4.0 {
     na k cl a ca }
   */
 /* COMPARTMENT vol [ 0 ] * diam * diam * PI / 4.0 {
     catot }
   */
 /* LONGITUDINAL_DIFFUSION _li , Difna * diam * diam * PI * vol [ ((int) _i ) ] / 4.0 {
     na }
   */
 /* LONGITUDINAL_DIFFUSION _li , Difk * diam * diam * PI * vol [ ((int) _i ) ] / 4.0 {
     k }
   */
 /* LONGITUDINAL_DIFFUSION _li , Difcl * diam * diam * PI * vol [ ((int) _i ) ] / 4.0 {
     cl }
   */
 /* LONGITUDINAL_DIFFUSION _li , Difca * diam * diam * PI * vol [ ((int) _i ) ] / 4.0 {
     ca }
   */
 naflux [ 0 ] = - deltan * na [ 0 ] - ( ina * diam ) * PI * ( 1e4 ) / FARADAY ;
   caflux [ 0 ] = - deltan * catot - ( ( ica ) * diam ) * PI * ( 1e4 ) / ( FARADAY * 2.0 ) ;
   clflux [ 0 ] = - deltan * cl [ 0 ] - ( icl * diam ) * PI * ( 1e4 ) / FARADAY * - 1.0 ;
   kflux [ 0 ] = - deltan * k [ 0 ] - ( ik * diam ) * PI * ( 1e4 ) / FARADAY ;
   aflux [ 0 ] = - deltan * a [ 0 ] ;
   naflux [ 1 ] = ( deltan + deltag ) * na [ 1 ] + ( ina * diam + inag * diamg ) * PI * ( 1e4 ) / FARADAY ;
   caflux [ 1 ] = ( deltan + deltag ) * ca [ 1 ] + ( ( ica ) * diam + 0.0 * diamg ) * PI * ( 1e4 ) / ( FARADAY * 2.0 ) ;
   clflux [ 1 ] = ( deltan + deltag ) * cl [ 1 ] + ( icl * diam + iclg * diamg ) * PI * ( 1e4 ) / FARADAY * - 1.0 ;
   kflux [ 1 ] = ( deltan + deltag ) * k [ 1 ] + ( ik * diam + ikg * diamg ) * PI * ( 1e4 ) / FARADAY ;
   aflux [ 1 ] = ( deltan + deltag ) * a [ 1 ] ;
   naflux [ 2 ] = - deltag * na [ 2 ] - ( inag * diamg ) * PI * ( 1e4 ) / FARADAY ;
   caflux [ 2 ] = 0.0 ;
   clflux [ 2 ] = - deltag * cl [ 2 ] - ( iclg * diamg ) * PI * ( 1e4 ) / FARADAY * - 1.0 ;
   kflux [ 2 ] = - deltag * k [ 2 ] - ( ikg * diamg ) * PI * ( 1e4 ) / FARADAY ;
   aflux [ 2 ] = - deltag * a [ 2 ] ;
   /* ~ na [ 0 ] < < ( naflux [ 0 ] )*/
 f_flux = b_flux = 0.;
 _RHS1( 12 +  0) += (b_flux =   ( naflux [ 0 ] ) );
 /*FLUX*/
  /* ~ catot < < ( caflux [ 0 ] )*/
 f_flux = b_flux = 0.;
 _RHS1( 3) += (b_flux =   ( caflux [ 0 ] ) );
 /*FLUX*/
  /* ~ k [ 0 ] < < ( kflux [ 0 ] )*/
 f_flux = b_flux = 0.;
 _RHS1( 9 +  0) += (b_flux =   ( kflux [ 0 ] ) );
 /*FLUX*/
  /* ~ cl [ 0 ] < < ( clflux [ 0 ] )*/
 f_flux = b_flux = 0.;
 _RHS1( 6 +  0) += (b_flux =   ( clflux [ 0 ] ) );
 /*FLUX*/
  /* ~ a [ 0 ] < < ( aflux [ 0 ] )*/
 f_flux = b_flux = 0.;
 _RHS1( 0 +  0) += (b_flux =   ( aflux [ 0 ] ) );
 /*FLUX*/
  /* ~ na [ 1 ] < < ( naflux [ 1 ] )*/
 f_flux = b_flux = 0.;
 _RHS1( 12 +  1) += (b_flux =   ( naflux [ 1 ] ) );
 /*FLUX*/
  /* ~ ca [ 1 ] < < ( caflux [ 1 ] )*/
 f_flux = b_flux = 0.;
 _RHS1( 4 +  1) += (b_flux =   ( caflux [ 1 ] ) );
 /*FLUX*/
  /* ~ k [ 1 ] < < ( kflux [ 1 ] )*/
 f_flux = b_flux = 0.;
 _RHS1( 9 +  1) += (b_flux =   ( kflux [ 1 ] ) );
 /*FLUX*/
  /* ~ cl [ 1 ] < < ( clflux [ 1 ] )*/
 f_flux = b_flux = 0.;
 _RHS1( 6 +  1) += (b_flux =   ( clflux [ 1 ] ) );
 /*FLUX*/
  /* ~ a [ 1 ] < < ( aflux [ 1 ] )*/
 f_flux = b_flux = 0.;
 _RHS1( 0 +  1) += (b_flux =   ( aflux [ 1 ] ) );
 /*FLUX*/
  /* ~ na [ 2 ] < < ( naflux [ 2 ] )*/
 f_flux = b_flux = 0.;
 _RHS1( 12 +  2) += (b_flux =   ( naflux [ 2 ] ) );
 /*FLUX*/
  /* ~ ca [ 2 ] < < ( caflux [ 2 ] )*/
 f_flux = b_flux = 0.;
 _RHS1( 4 +  2) += (b_flux =   ( caflux [ 2 ] ) );
 /*FLUX*/
  /* ~ k [ 2 ] < < ( kflux [ 2 ] )*/
 f_flux = b_flux = 0.;
 _RHS1( 9 +  2) += (b_flux =   ( kflux [ 2 ] ) );
 /*FLUX*/
  /* ~ cl [ 2 ] < < ( clflux [ 2 ] )*/
 f_flux = b_flux = 0.;
 _RHS1( 6 +  2) += (b_flux =   ( clflux [ 2 ] ) );
 /*FLUX*/
  /* ~ a [ 2 ] < < ( aflux [ 2 ] )*/
 f_flux = b_flux = 0.;
 _RHS1( 0 +  2) += (b_flux =   ( aflux [ 2 ] ) );
 /*FLUX*/
  _zb = TotalBuffer * setvolin / vol [ 0 ] - catot + Kd ;
   _zc = - Kd * catot ;
   _zd = _zb * _zb - 4.0 * _zc ;
   cai = ( - _zb + sqrt ( _zd ) ) / ( 2.0 ) ;
   CaBuffer = catot - cai ;
   Buffer = TotalBuffer * setvolin / vol [ 0 ] - CaBuffer ;
   volin = vol [ 0 ] ;
   volout = vol [ 1 ] ;
   volglia = vol [ 2 ] ;
   nai = na [ 0 ] ;
   nao = na [ 1 ] ;
   nag = na [ 2 ] ;
   cao = ca [ 1 ] ;
   cag = ca [ 2 ] ;
   cli = cl [ 0 ] ;
   clo = cl [ 1 ] ;
   clg = cl [ 2 ] ;
   ki = k [ 0 ] ;
   ko = k [ 1 ] ;
   kg = k [ 2 ] ;
   ai = a [ 0 ] ;
   ao = a [ 1 ] ;
   ag = a [ 2 ] ;
   osmin = nai + ki + cli + ai + cai ;
   osmout = nao + ko + clo + ao + cao ;
   osmglia = nag + kg + clg + ag + cag ;
   electin = nai + ki - cli - ai + cai * 2.0 ;
   electout = nao + ko - clo - ao + cao * 2.0 ;
   electglia = nag + kg - clg - ag + cag * 2.0 ;
   qnai = na [ 0 ] * vol [ 0 ] ;
   qnao = na [ 1 ] * vol [ 1 ] ;
   qnag = na [ 2 ] * vol [ 2 ] ;
   qcai = ca [ 0 ] * vol [ 0 ] ;
   qcao = ca [ 1 ] * vol [ 1 ] ;
   qcag = ca [ 2 ] * vol [ 2 ] ;
   qcli = cl [ 0 ] * vol [ 0 ] ;
   qclo = cl [ 1 ] * vol [ 1 ] ;
   qclg = cl [ 2 ] * vol [ 2 ] ;
   qki = k [ 0 ] * vol [ 0 ] ;
   qko = k [ 1 ] * vol [ 1 ] ;
   qkg = k [ 2 ] * vol [ 2 ] ;
   qai = a [ 0 ] * vol [ 0 ] ;
   qao = a [ 1 ] * vol [ 1 ] ;
   qag = a [ 2 ] * vol [ 2 ] ;
     } return _reset;
 }
 
/*CVODE ode begin*/
 static int _ode_spec1() {_reset=0;{
 double b_flux, f_flux, _term; int _i;
 {int _i; for(_i=0;_i<18;_i++) _p[_dlist1[_i]] = 0.0;}
 deltan = ( nai + ki + cli + ai + cai - nao - ko - clo - ao - cao ) / tau ;
 deltag = ( nag + kg + clg + ag + cag - nao - ko - clo - ao - cao ) / tau ;
 if ( vol [ 1 ] <= minvolisvf  && deltan > 0.0 ) {
   deltan = 0.0 ;
   }
 if ( vol [ 1 ] <= minvolisvf  && deltag > 0.0 ) {
   deltag = 0.0 ;
   }
 if ( method  == 0.0 ) {
   /* ~ vol [ 0 ] <-> vol [ 1 ] ( deltan / ( diam * diam * PI / 4.0 ) , - deltan / ( diam * diam * PI / 4.0 ) )*/
 f_flux =  deltan / ( diam * diam * PI / 4.0 ) * vol [ 0] ;
 b_flux =  - deltan / ( diam * diam * PI / 4.0 ) * vol [ 1] ;
 Dvol [ 0] -= (f_flux - b_flux);
 Dvol [ 1] += (f_flux - b_flux);
 
 /*REACTION*/
  /* ~ vol [ 1 ] <-> vol [ 2 ] ( - deltag / ( diam * diam * PI / 4.0 ) , deltag / ( diam * diam * PI / 4.0 ) )*/
 f_flux =  - deltag / ( diam * diam * PI / 4.0 ) * vol [ 1] ;
 b_flux =  deltag / ( diam * diam * PI / 4.0 ) * vol [ 2] ;
 Dvol [ 1] -= (f_flux - b_flux);
 Dvol [ 2] += (f_flux - b_flux);
 
 /*REACTION*/
  }
 else {
   /* ~ vol [ 0 ] < < ( deltan / ( diam * diam * PI / 4.0 ) )*/
 f_flux = b_flux = 0.;
 Dvol [ 0] += (b_flux =   ( deltan / ( diam * diam * PI / 4.0 ) ) );
 /*FLUX*/
  /* ~ vol [ 1 ] < < ( ( - deltan - deltag ) / ( diam * diam * PI / 4.0 ) )*/
 f_flux = b_flux = 0.;
 Dvol [ 1] += (b_flux =   ( ( - deltan - deltag ) / ( diam * diam * PI / 4.0 ) ) );
 /*FLUX*/
  /* ~ vol [ 2 ] < < ( ( deltag ) / ( diam * diam * PI / 4.0 ) )*/
 f_flux = b_flux = 0.;
 Dvol [ 2] += (b_flux =   ( ( deltag ) / ( diam * diam * PI / 4.0 ) ) );
 /*FLUX*/
  }
 /* COMPARTMENT _li , vol [ ((int) _i ) ] * diam * diam * PI / 4.0 {
   na k cl a ca }
 */
 /* COMPARTMENT vol [ 0 ] * diam * diam * PI / 4.0 {
   catot }
 */
 /* LONGITUDINAL_DIFFUSION _li , Difna * diam * diam * PI * vol [ ((int) _i ) ] / 4.0 {
   na }
 */
 /* LONGITUDINAL_DIFFUSION _li , Difk * diam * diam * PI * vol [ ((int) _i ) ] / 4.0 {
   k }
 */
 /* LONGITUDINAL_DIFFUSION _li , Difcl * diam * diam * PI * vol [ ((int) _i ) ] / 4.0 {
   cl }
 */
 /* LONGITUDINAL_DIFFUSION _li , Difca * diam * diam * PI * vol [ ((int) _i ) ] / 4.0 {
   ca }
 */
 naflux [ 0 ] = - deltan * na [ 0 ] - ( ina * diam ) * PI * ( 1e4 ) / FARADAY ;
 caflux [ 0 ] = - deltan * catot - ( ( ica ) * diam ) * PI * ( 1e4 ) / ( FARADAY * 2.0 ) ;
 clflux [ 0 ] = - deltan * cl [ 0 ] - ( icl * diam ) * PI * ( 1e4 ) / FARADAY * - 1.0 ;
 kflux [ 0 ] = - deltan * k [ 0 ] - ( ik * diam ) * PI * ( 1e4 ) / FARADAY ;
 aflux [ 0 ] = - deltan * a [ 0 ] ;
 naflux [ 1 ] = ( deltan + deltag ) * na [ 1 ] + ( ina * diam + inag * diamg ) * PI * ( 1e4 ) / FARADAY ;
 caflux [ 1 ] = ( deltan + deltag ) * ca [ 1 ] + ( ( ica ) * diam + 0.0 * diamg ) * PI * ( 1e4 ) / ( FARADAY * 2.0 ) ;
 clflux [ 1 ] = ( deltan + deltag ) * cl [ 1 ] + ( icl * diam + iclg * diamg ) * PI * ( 1e4 ) / FARADAY * - 1.0 ;
 kflux [ 1 ] = ( deltan + deltag ) * k [ 1 ] + ( ik * diam + ikg * diamg ) * PI * ( 1e4 ) / FARADAY ;
 aflux [ 1 ] = ( deltan + deltag ) * a [ 1 ] ;
 naflux [ 2 ] = - deltag * na [ 2 ] - ( inag * diamg ) * PI * ( 1e4 ) / FARADAY ;
 caflux [ 2 ] = 0.0 ;
 clflux [ 2 ] = - deltag * cl [ 2 ] - ( iclg * diamg ) * PI * ( 1e4 ) / FARADAY * - 1.0 ;
 kflux [ 2 ] = - deltag * k [ 2 ] - ( ikg * diamg ) * PI * ( 1e4 ) / FARADAY ;
 aflux [ 2 ] = - deltag * a [ 2 ] ;
 /* ~ na [ 0 ] < < ( naflux [ 0 ] )*/
 f_flux = b_flux = 0.;
 Dna [ 0] += (b_flux =   ( naflux [ 0 ] ) );
 /*FLUX*/
  /* ~ catot < < ( caflux [ 0 ] )*/
 f_flux = b_flux = 0.;
 Dcatot += (b_flux =   ( caflux [ 0 ] ) );
 /*FLUX*/
  /* ~ k [ 0 ] < < ( kflux [ 0 ] )*/
 f_flux = b_flux = 0.;
 Dk [ 0] += (b_flux =   ( kflux [ 0 ] ) );
 /*FLUX*/
  /* ~ cl [ 0 ] < < ( clflux [ 0 ] )*/
 f_flux = b_flux = 0.;
 Dcl [ 0] += (b_flux =   ( clflux [ 0 ] ) );
 /*FLUX*/
  /* ~ a [ 0 ] < < ( aflux [ 0 ] )*/
 f_flux = b_flux = 0.;
 Da [ 0] += (b_flux =   ( aflux [ 0 ] ) );
 /*FLUX*/
  /* ~ na [ 1 ] < < ( naflux [ 1 ] )*/
 f_flux = b_flux = 0.;
 Dna [ 1] += (b_flux =   ( naflux [ 1 ] ) );
 /*FLUX*/
  /* ~ ca [ 1 ] < < ( caflux [ 1 ] )*/
 f_flux = b_flux = 0.;
 Dca [ 1] += (b_flux =   ( caflux [ 1 ] ) );
 /*FLUX*/
  /* ~ k [ 1 ] < < ( kflux [ 1 ] )*/
 f_flux = b_flux = 0.;
 Dk [ 1] += (b_flux =   ( kflux [ 1 ] ) );
 /*FLUX*/
  /* ~ cl [ 1 ] < < ( clflux [ 1 ] )*/
 f_flux = b_flux = 0.;
 Dcl [ 1] += (b_flux =   ( clflux [ 1 ] ) );
 /*FLUX*/
  /* ~ a [ 1 ] < < ( aflux [ 1 ] )*/
 f_flux = b_flux = 0.;
 Da [ 1] += (b_flux =   ( aflux [ 1 ] ) );
 /*FLUX*/
  /* ~ na [ 2 ] < < ( naflux [ 2 ] )*/
 f_flux = b_flux = 0.;
 Dna [ 2] += (b_flux =   ( naflux [ 2 ] ) );
 /*FLUX*/
  /* ~ ca [ 2 ] < < ( caflux [ 2 ] )*/
 f_flux = b_flux = 0.;
 Dca [ 2] += (b_flux =   ( caflux [ 2 ] ) );
 /*FLUX*/
  /* ~ k [ 2 ] < < ( kflux [ 2 ] )*/
 f_flux = b_flux = 0.;
 Dk [ 2] += (b_flux =   ( kflux [ 2 ] ) );
 /*FLUX*/
  /* ~ cl [ 2 ] < < ( clflux [ 2 ] )*/
 f_flux = b_flux = 0.;
 Dcl [ 2] += (b_flux =   ( clflux [ 2 ] ) );
 /*FLUX*/
  /* ~ a [ 2 ] < < ( aflux [ 2 ] )*/
 f_flux = b_flux = 0.;
 Da [ 2] += (b_flux =   ( aflux [ 2 ] ) );
 /*FLUX*/
  _zb = TotalBuffer * setvolin / vol [ 0 ] - catot + Kd ;
 _zc = - Kd * catot ;
 _zd = _zb * _zb - 4.0 * _zc ;
 cai = ( - _zb + sqrt ( _zd ) ) / ( 2.0 ) ;
 CaBuffer = catot - cai ;
 Buffer = TotalBuffer * setvolin / vol [ 0 ] - CaBuffer ;
 volin = vol [ 0 ] ;
 volout = vol [ 1 ] ;
 volglia = vol [ 2 ] ;
 nai = na [ 0 ] ;
 nao = na [ 1 ] ;
 nag = na [ 2 ] ;
 cao = ca [ 1 ] ;
 cag = ca [ 2 ] ;
 cli = cl [ 0 ] ;
 clo = cl [ 1 ] ;
 clg = cl [ 2 ] ;
 ki = k [ 0 ] ;
 ko = k [ 1 ] ;
 kg = k [ 2 ] ;
 ai = a [ 0 ] ;
 ao = a [ 1 ] ;
 ag = a [ 2 ] ;
 osmin = nai + ki + cli + ai + cai ;
 osmout = nao + ko + clo + ao + cao ;
 osmglia = nag + kg + clg + ag + cag ;
 electin = nai + ki - cli - ai + cai * 2.0 ;
 electout = nao + ko - clo - ao + cao * 2.0 ;
 electglia = nag + kg - clg - ag + cag * 2.0 ;
 qnai = na [ 0 ] * vol [ 0 ] ;
 qnao = na [ 1 ] * vol [ 1 ] ;
 qnag = na [ 2 ] * vol [ 2 ] ;
 qcai = ca [ 0 ] * vol [ 0 ] ;
 qcao = ca [ 1 ] * vol [ 1 ] ;
 qcag = ca [ 2 ] * vol [ 2 ] ;
 qcli = cl [ 0 ] * vol [ 0 ] ;
 qclo = cl [ 1 ] * vol [ 1 ] ;
 qclg = cl [ 2 ] * vol [ 2 ] ;
 qki = k [ 0 ] * vol [ 0 ] ;
 qko = k [ 1 ] * vol [ 1 ] ;
 qkg = k [ 2 ] * vol [ 2 ] ;
 qai = a [ 0 ] * vol [ 0 ] ;
 qao = a [ 1 ] * vol [ 1 ] ;
 qag = a [ 2 ] * vol [ 2 ] ;
 for (_i=0; _i < 3; _i++) { _p[_dlist1[_i + 0]] /= ( vol [ ((int) _i ) ] * diam * diam * PI / 4.0);}
 _p[_dlist1[3]] /= ( vol [ 0 ] * diam * diam * PI / 4.0);
 for (_i=0; _i < 2; _i++) { _p[_dlist1[_i + 4]] /= ( vol [ ((int) _i ) ] * diam * diam * PI / 4.0);}
 for (_i=0; _i < 3; _i++) { _p[_dlist1[_i + 6]] /= ( vol [ ((int) _i ) ] * diam * diam * PI / 4.0);}
 for (_i=0; _i < 3; _i++) { _p[_dlist1[_i + 9]] /= ( vol [ ((int) _i ) ] * diam * diam * PI / 4.0);}
 for (_i=0; _i < 3; _i++) { _p[_dlist1[_i + 12]] /= ( vol [ ((int) _i ) ] * diam * diam * PI / 4.0);}
   } return _reset;
 }
 
/*CVODE matsol*/
 static int _ode_matsol1() {_reset=0;{
 double b_flux, f_flux, _term; int _i;
   b_flux = f_flux = 0.;
 {int _i; double _dt1 = 1.0/dt;
for(_i=0;_i<18;_i++){
  	_RHS1(_i) = _dt1*(_p[_dlist1[_i]]);
	_MATELM1(_i, _i) = _dt1;
      
}  
_RHS1(3) *= ( vol [ 0 ] * diam * diam * PI / 4.0) ;
_MATELM1(3, 3) *= ( vol [ 0 ] * diam * diam * PI / 4.0);  
for (_i=0; _i < 3; _i++) {
  	_RHS1(_i + 0) *= ( vol [ ((int) _i ) ] * diam * diam * PI / 4.0) ;
_MATELM1(_i + 0, _i + 0) *= ( vol [ ((int) _i ) ] * diam * diam * PI / 4.0);  } 
for (_i=0; _i < 2; _i++) {
  	_RHS1(_i + 4) *= ( vol [ ((int) _i ) ] * diam * diam * PI / 4.0) ;
_MATELM1(_i + 4, _i + 4) *= ( vol [ ((int) _i ) ] * diam * diam * PI / 4.0);  } 
for (_i=0; _i < 3; _i++) {
  	_RHS1(_i + 6) *= ( vol [ ((int) _i ) ] * diam * diam * PI / 4.0) ;
_MATELM1(_i + 6, _i + 6) *= ( vol [ ((int) _i ) ] * diam * diam * PI / 4.0);  } 
for (_i=0; _i < 3; _i++) {
  	_RHS1(_i + 9) *= ( vol [ ((int) _i ) ] * diam * diam * PI / 4.0) ;
_MATELM1(_i + 9, _i + 9) *= ( vol [ ((int) _i ) ] * diam * diam * PI / 4.0);  } 
for (_i=0; _i < 3; _i++) {
  	_RHS1(_i + 12) *= ( vol [ ((int) _i ) ] * diam * diam * PI / 4.0) ;
_MATELM1(_i + 12, _i + 12) *= ( vol [ ((int) _i ) ] * diam * diam * PI / 4.0);  } }
 deltan = ( nai + ki + cli + ai + cai - nao - ko - clo - ao - cao ) / tau ;
 deltag = ( nag + kg + clg + ag + cag - nao - ko - clo - ao - cao ) / tau ;
 if ( vol [ 1 ] <= minvolisvf  && deltan > 0.0 ) {
 deltan = 0.0 ;
 }
 if ( vol [ 1 ] <= minvolisvf  && deltag > 0.0 ) {
 deltag = 0.0 ;
 }
 if ( method  == 0.0 ) {
 /* ~ vol [ 0 ] <-> vol [ 1 ] ( deltan / ( diam * diam * PI / 4.0 ) , - deltan / ( diam * diam * PI / 4.0 ) )*/
 _term =  deltan / ( diam * diam * PI / 4.0 ) ;
 _MATELM1( 15 +  0 ,15 +  0)  += _term;
 _MATELM1( 15 +  1 ,15 +  0)  -= _term;
 _term =  - deltan / ( diam * diam * PI / 4.0 ) ;
 _MATELM1( 15 +  0 ,15 +  1)  -= _term;
 _MATELM1( 15 +  1 ,15 +  1)  += _term;
 /*REACTION*/
  /* ~ vol [ 1 ] <-> vol [ 2 ] ( - deltag / ( diam * diam * PI / 4.0 ) , deltag / ( diam * diam * PI / 4.0 ) )*/
 _term =  - deltag / ( diam * diam * PI / 4.0 ) ;
 _MATELM1( 15 +  1 ,15 +  1)  += _term;
 _MATELM1( 15 +  2 ,15 +  1)  -= _term;
 _term =  deltag / ( diam * diam * PI / 4.0 ) ;
 _MATELM1( 15 +  1 ,15 +  2)  -= _term;
 _MATELM1( 15 +  2 ,15 +  2)  += _term;
 /*REACTION*/
  }
 else {
 /* ~ vol [ 0 ] < < ( deltan / ( diam * diam * PI / 4.0 ) )*/
 /*FLUX*/
  /* ~ vol [ 1 ] < < ( ( - deltan - deltag ) / ( diam * diam * PI / 4.0 ) )*/
 /*FLUX*/
  /* ~ vol [ 2 ] < < ( ( deltag ) / ( diam * diam * PI / 4.0 ) )*/
 /*FLUX*/
  }
 /* COMPARTMENT _li , vol [ ((int) _i ) ] * diam * diam * PI / 4.0 {
 na k cl a ca }
 */
 /* COMPARTMENT vol [ 0 ] * diam * diam * PI / 4.0 {
 catot }
 */
 /* LONGITUDINAL_DIFFUSION _li , Difna * diam * diam * PI * vol [ ((int) _i ) ] / 4.0 {
 na }
 */
 /* LONGITUDINAL_DIFFUSION _li , Difk * diam * diam * PI * vol [ ((int) _i ) ] / 4.0 {
 k }
 */
 /* LONGITUDINAL_DIFFUSION _li , Difcl * diam * diam * PI * vol [ ((int) _i ) ] / 4.0 {
 cl }
 */
 /* LONGITUDINAL_DIFFUSION _li , Difca * diam * diam * PI * vol [ ((int) _i ) ] / 4.0 {
 ca }
 */
 naflux [ 0 ] = - deltan * na [ 0 ] - ( ina * diam ) * PI * ( 1e4 ) / FARADAY ;
 caflux [ 0 ] = - deltan * catot - ( ( ica ) * diam ) * PI * ( 1e4 ) / ( FARADAY * 2.0 ) ;
 clflux [ 0 ] = - deltan * cl [ 0 ] - ( icl * diam ) * PI * ( 1e4 ) / FARADAY * - 1.0 ;
 kflux [ 0 ] = - deltan * k [ 0 ] - ( ik * diam ) * PI * ( 1e4 ) / FARADAY ;
 aflux [ 0 ] = - deltan * a [ 0 ] ;
 naflux [ 1 ] = ( deltan + deltag ) * na [ 1 ] + ( ina * diam + inag * diamg ) * PI * ( 1e4 ) / FARADAY ;
 caflux [ 1 ] = ( deltan + deltag ) * ca [ 1 ] + ( ( ica ) * diam + 0.0 * diamg ) * PI * ( 1e4 ) / ( FARADAY * 2.0 ) ;
 clflux [ 1 ] = ( deltan + deltag ) * cl [ 1 ] + ( icl * diam + iclg * diamg ) * PI * ( 1e4 ) / FARADAY * - 1.0 ;
 kflux [ 1 ] = ( deltan + deltag ) * k [ 1 ] + ( ik * diam + ikg * diamg ) * PI * ( 1e4 ) / FARADAY ;
 aflux [ 1 ] = ( deltan + deltag ) * a [ 1 ] ;
 naflux [ 2 ] = - deltag * na [ 2 ] - ( inag * diamg ) * PI * ( 1e4 ) / FARADAY ;
 caflux [ 2 ] = 0.0 ;
 clflux [ 2 ] = - deltag * cl [ 2 ] - ( iclg * diamg ) * PI * ( 1e4 ) / FARADAY * - 1.0 ;
 kflux [ 2 ] = - deltag * k [ 2 ] - ( ikg * diamg ) * PI * ( 1e4 ) / FARADAY ;
 aflux [ 2 ] = - deltag * a [ 2 ] ;
 /* ~ na [ 0 ] < < ( naflux [ 0 ] )*/
 /*FLUX*/
  /* ~ catot < < ( caflux [ 0 ] )*/
 /*FLUX*/
  /* ~ k [ 0 ] < < ( kflux [ 0 ] )*/
 /*FLUX*/
  /* ~ cl [ 0 ] < < ( clflux [ 0 ] )*/
 /*FLUX*/
  /* ~ a [ 0 ] < < ( aflux [ 0 ] )*/
 /*FLUX*/
  /* ~ na [ 1 ] < < ( naflux [ 1 ] )*/
 /*FLUX*/
  /* ~ ca [ 1 ] < < ( caflux [ 1 ] )*/
 /*FLUX*/
  /* ~ k [ 1 ] < < ( kflux [ 1 ] )*/
 /*FLUX*/
  /* ~ cl [ 1 ] < < ( clflux [ 1 ] )*/
 /*FLUX*/
  /* ~ a [ 1 ] < < ( aflux [ 1 ] )*/
 /*FLUX*/
  /* ~ na [ 2 ] < < ( naflux [ 2 ] )*/
 /*FLUX*/
  /* ~ ca [ 2 ] < < ( caflux [ 2 ] )*/
 /*FLUX*/
  /* ~ k [ 2 ] < < ( kflux [ 2 ] )*/
 /*FLUX*/
  /* ~ cl [ 2 ] < < ( clflux [ 2 ] )*/
 /*FLUX*/
  /* ~ a [ 2 ] < < ( aflux [ 2 ] )*/
 /*FLUX*/
  _zb = TotalBuffer * setvolin / vol [ 0 ] - catot + Kd ;
 _zc = - Kd * catot ;
 _zd = _zb * _zb - 4.0 * _zc ;
 cai = ( - _zb + sqrt ( _zd ) ) / ( 2.0 ) ;
 CaBuffer = catot - cai ;
 Buffer = TotalBuffer * setvolin / vol [ 0 ] - CaBuffer ;
 volin = vol [ 0 ] ;
 volout = vol [ 1 ] ;
 volglia = vol [ 2 ] ;
 nai = na [ 0 ] ;
 nao = na [ 1 ] ;
 nag = na [ 2 ] ;
 cao = ca [ 1 ] ;
 cag = ca [ 2 ] ;
 cli = cl [ 0 ] ;
 clo = cl [ 1 ] ;
 clg = cl [ 2 ] ;
 ki = k [ 0 ] ;
 ko = k [ 1 ] ;
 kg = k [ 2 ] ;
 ai = a [ 0 ] ;
 ao = a [ 1 ] ;
 ag = a [ 2 ] ;
 osmin = nai + ki + cli + ai + cai ;
 osmout = nao + ko + clo + ao + cao ;
 osmglia = nag + kg + clg + ag + cag ;
 electin = nai + ki - cli - ai + cai * 2.0 ;
 electout = nao + ko - clo - ao + cao * 2.0 ;
 electglia = nag + kg - clg - ag + cag * 2.0 ;
 qnai = na [ 0 ] * vol [ 0 ] ;
 qnao = na [ 1 ] * vol [ 1 ] ;
 qnag = na [ 2 ] * vol [ 2 ] ;
 qcai = ca [ 0 ] * vol [ 0 ] ;
 qcao = ca [ 1 ] * vol [ 1 ] ;
 qcag = ca [ 2 ] * vol [ 2 ] ;
 qcli = cl [ 0 ] * vol [ 0 ] ;
 qclo = cl [ 1 ] * vol [ 1 ] ;
 qclg = cl [ 2 ] * vol [ 2 ] ;
 qki = k [ 0 ] * vol [ 0 ] ;
 qko = k [ 1 ] * vol [ 1 ] ;
 qkg = k [ 2 ] * vol [ 2 ] ;
 qai = a [ 0 ] * vol [ 0 ] ;
 qao = a [ 1 ] * vol [ 1 ] ;
 qag = a [ 2 ] * vol [ 2 ] ;
   } return _reset;
 }
 
/*CVODE end*/
 
static int _ode_count(int _type){ return 18;}
 
static void _ode_spec(_NrnThread* _nt, _Memb_list* _ml, int _type) {
   Datum* _thread;
   Node* _nd; double _v; int _iml, _cntml;
  _cntml = _ml->_nodecount;
  _thread = _ml->_thread;
  for (_iml = 0; _iml < _cntml; ++_iml) {
    _p = _ml->_data[_iml]; _ppvar = _ml->_pdata[_iml];
    _nd = _ml->_nodelist[_iml];
    v = NODEV(_nd);
  ina = _ion_ina;
  nao = _ion_nao;
  nai = _ion_nai;
  nai = _ion_nai;
  nao = _ion_nao;
  ik = _ion_ik;
  ko = _ion_ko;
  ki = _ion_ki;
  ki = _ion_ki;
  ko = _ion_ko;
  icl = _ion_icl;
  clo = _ion_clo;
  cli = _ion_cli;
  cli = _ion_cli;
  clo = _ion_clo;
  ia = _ion_ia;
  ao = _ion_ao;
  ai = _ion_ai;
  ai = _ion_ai;
  ao = _ion_ao;
  ica = _ion_ica;
  cao = _ion_cao;
  cai = _ion_cai;
  cai = _ion_cai;
  cao = _ion_cao;
     _ode_spec1 ();
  _ion_nai = nai;
  _ion_nao = nao;
   _ion_ki = ki;
  _ion_ko = ko;
   _ion_cli = cli;
  _ion_clo = clo;
   _ion_ai = ai;
  _ion_ao = ao;
  _ion_cai = cai;
  _ion_cao = cao;
  }}
 
static void _ode_map(int _ieq, double** _pv, double** _pvdot, double* _pp, Datum* _ppd, double* _atol, int _type) { 
 	int _i; _p = _pp; _ppvar = _ppd;
	_cvode_ieq = _ieq;
	for (_i=0; _i < 18; ++_i) {
		_pv[_i] = _pp + _slist1[_i];  _pvdot[_i] = _pp + _dlist1[_i];
		_cvode_abstol(_atollist, _atol, _i);
	}
 }
 static void _ode_synonym(int _cnt, double** _pp, Datum** _ppd) { 
 	int _i; 
	for (_i=0; _i < _cnt; ++_i) {_p = _pp[_i]; _ppvar = _ppd[_i];
 _ion_nai =  na [ 0 ] ;
 _ion_nao =  na [ 1 ] ;
 _ion_ki =  k [ 0 ] ;
 _ion_ko =  k [ 1 ] ;
 _ion_cli =  cl [ 0 ] ;
 _ion_clo =  cl [ 1 ] ;
 _ion_ai =  a [ 0 ] ;
 _ion_ao =  a [ 1 ] ;
 _ion_cai =  ( - _zb + sqrt ( _zd ) ) / ( 2.0 ) ;
 _ion_cao =  ca [ 1 ] ;
 }}
 
static void _ode_matsol_instance1(_threadargsproto_) {
 _cvode_sparse(&_cvsparseobj1, 18, _dlist1, _p, _ode_matsol1, &_coef1);
 }
 
static void _ode_matsol(_NrnThread* _nt, _Memb_list* _ml, int _type) {
   Datum* _thread;
   Node* _nd; double _v; int _iml, _cntml;
  _cntml = _ml->_nodecount;
  _thread = _ml->_thread;
  for (_iml = 0; _iml < _cntml; ++_iml) {
    _p = _ml->_data[_iml]; _ppvar = _ml->_pdata[_iml];
    _nd = _ml->_nodelist[_iml];
    v = NODEV(_nd);
  ina = _ion_ina;
  nao = _ion_nao;
  nai = _ion_nai;
  nai = _ion_nai;
  nao = _ion_nao;
  ik = _ion_ik;
  ko = _ion_ko;
  ki = _ion_ki;
  ki = _ion_ki;
  ko = _ion_ko;
  icl = _ion_icl;
  clo = _ion_clo;
  cli = _ion_cli;
  cli = _ion_cli;
  clo = _ion_clo;
  ia = _ion_ia;
  ao = _ion_ao;
  ai = _ion_ai;
  ai = _ion_ai;
  ao = _ion_ao;
  ica = _ion_ica;
  cao = _ion_cao;
  cai = _ion_cai;
  cai = _ion_cai;
  cao = _ion_cao;
 _ode_matsol_instance1(_threadargs_);
 }}
 extern void nrn_update_ion_pointer(Symbol*, Datum*, int, int);
 static void _update_ion_pointer(Datum* _ppvar) {
   nrn_update_ion_pointer(_na_sym, _ppvar, 0, 3);
   nrn_update_ion_pointer(_na_sym, _ppvar, 1, 2);
   nrn_update_ion_pointer(_na_sym, _ppvar, 2, 1);
   nrn_update_ion_pointer(_na_sym, _ppvar, 3, 4);
   nrn_update_ion_pointer(_k_sym, _ppvar, 5, 3);
   nrn_update_ion_pointer(_k_sym, _ppvar, 6, 2);
   nrn_update_ion_pointer(_k_sym, _ppvar, 7, 1);
   nrn_update_ion_pointer(_k_sym, _ppvar, 8, 4);
   nrn_update_ion_pointer(_cl_sym, _ppvar, 10, 3);
   nrn_update_ion_pointer(_cl_sym, _ppvar, 11, 2);
   nrn_update_ion_pointer(_cl_sym, _ppvar, 12, 1);
   nrn_update_ion_pointer(_cl_sym, _ppvar, 13, 4);
   nrn_update_ion_pointer(_a_sym, _ppvar, 15, 3);
   nrn_update_ion_pointer(_a_sym, _ppvar, 16, 2);
   nrn_update_ion_pointer(_a_sym, _ppvar, 17, 1);
   nrn_update_ion_pointer(_a_sym, _ppvar, 19, 4);
   nrn_update_ion_pointer(_ca_sym, _ppvar, 20, 3);
   nrn_update_ion_pointer(_ca_sym, _ppvar, 21, 2);
   nrn_update_ion_pointer(_ca_sym, _ppvar, 22, 1);
   nrn_update_ion_pointer(_ca_sym, _ppvar, 23, 4);
 }
 static void* _difspace1;
extern double nrn_nernst_coef();
static double _difcoef1(int _i, double* _p, Datum* _ppvar, double* _pdvol, double* _pdfcdc, Datum* _thread, _NrnThread* _nt) {
   *_pdvol =  vol [ ((int) _i ) ] * diam * diam * PI / 4.0 ; *_pdfcdc=0.;
   return Difna * diam * diam * PI * vol [ ((int) _i ) ] / 4.0 ;
}
 static void* _difspace2;
extern double nrn_nernst_coef();
static double _difcoef2(int _i, double* _p, Datum* _ppvar, double* _pdvol, double* _pdfcdc, Datum* _thread, _NrnThread* _nt) {
   *_pdvol =  vol [ ((int) _i ) ] * diam * diam * PI / 4.0 ; *_pdfcdc=0.;
   return Difk * diam * diam * PI * vol [ ((int) _i ) ] / 4.0 ;
}
 static void* _difspace3;
extern double nrn_nernst_coef();
static double _difcoef3(int _i, double* _p, Datum* _ppvar, double* _pdvol, double* _pdfcdc, Datum* _thread, _NrnThread* _nt) {
   *_pdvol =  vol [ ((int) _i ) ] * diam * diam * PI / 4.0 ; *_pdfcdc=0.;
   return Difcl * diam * diam * PI * vol [ ((int) _i ) ] / 4.0 ;
}
 static void* _difspace4;
extern double nrn_nernst_coef();
static double _difcoef4(int _i, double* _p, Datum* _ppvar, double* _pdvol, double* _pdfcdc, Datum* _thread, _NrnThread* _nt) {
   *_pdvol =  vol [ ((int) _i ) ] * diam * diam * PI / 4.0 ; *_pdfcdc=0.;
   return Difca * diam * diam * PI * vol [ ((int) _i ) ] / 4.0 ;
}
 static void _difusfunc(ldifusfunc2_t _f, _NrnThread* _nt) {int _i;
  for (_i=0; _i < 3; ++_i) (*_f)(_mechtype, _difcoef1, &_difspace1, _i,  34, 89 , _nt);
  for (_i=0; _i < 3; ++_i) (*_f)(_mechtype, _difcoef2, &_difspace2, _i,  37, 92 , _nt);
  for (_i=0; _i < 3; ++_i) (*_f)(_mechtype, _difcoef3, &_difspace3, _i,  43, 98 , _nt);
  for (_i=0; _i < 2; ++_i) (*_f)(_mechtype, _difcoef4, &_difspace4, _i,  46, 101 , _nt);
 }

static void initmodel() {
  int _i; double _save;_ninits++;
 _save = t;
 t = 0.0;
{
  Buffer = Buffer0;
  CaBuffer = CaBuffer0;
 for (_i=0; _i<3; _i++) a[_i] = a0;
  catot = catot0;
 for (_i=0; _i<2; _i++) ca[_i] = ca0;
 for (_i=0; _i<3; _i++) cl[_i] = cl0;
 for (_i=0; _i<3; _i++) k[_i] = k0;
 for (_i=0; _i<3; _i++) na[_i] = na0;
  pumpca = pumpca0;
  pump = pump0;
 for (_i=0; _i<3; _i++) vol[_i] = vol0;
 {
   na [ 0 ] = nai ;
   na [ 1 ] = nao ;
   na [ 2 ] = setnag ;
   cl [ 0 ] = cli ;
   cl [ 1 ] = clo ;
   cl [ 2 ] = setclg ;
   k [ 0 ] = ki ;
   k [ 1 ] = ko ;
   k [ 2 ] = setkg ;
   a [ 0 ] = ai ;
   a [ 1 ] = ao ;
   a [ 2 ] = setag ;
   ca [ 0 ] = cai ;
   ca [ 1 ] = cao ;
   ca [ 2 ] = setcag ;
   B0 = TotalBuffer / ( 1.0 + Kd * cai ) ;
   Buffer = B0 ;
   CaBuffer = TotalBuffer - B0 ;
   catot = cai * ( 1.0 + ( TotalBuffer / ( cai + Kd ) ) ) ;
   vol [ 0 ] = setvolin ;
   vol [ 1 ] = setvolout ;
   vol [ 2 ] = setvolglia ;
   volin = vol [ 0 ] ;
   volout = vol [ 1 ] ;
   volglia = vol [ 2 ] ;
   nag = na [ 2 ] ;
   kg = k [ 2 ] ;
   clg = cl [ 2 ] ;
   ag = a [ 2 ] ;
   cag = ca [ 2 ] ;
   osmin = nai + ki + cli + ai + cai ;
   osmout = nao + ko + clo + ao + cao ;
   osmglia = nag + kg + clg + ag + cag ;
   electin = nai + ki - cli - ai + cai * 2.0 ;
   electout = nao + ko - clo - ao + cao * 2.0 ;
   electglia = nag + kg - clg - ag + cag * 2.0 ;
   qnai = na [ 0 ] * vol [ 0 ] ;
   qnao = na [ 1 ] * vol [ 1 ] ;
   qnag = na [ 2 ] * vol [ 2 ] ;
   qcai = ca [ 0 ] * vol [ 0 ] ;
   qcao = ca [ 1 ] * vol [ 1 ] ;
   qcag = ca [ 2 ] * vol [ 2 ] ;
   qcli = cl [ 0 ] * vol [ 0 ] ;
   qclo = cl [ 1 ] * vol [ 1 ] ;
   qclg = cl [ 2 ] * vol [ 2 ] ;
   qki = k [ 0 ] * vol [ 0 ] ;
   qko = k [ 1 ] * vol [ 1 ] ;
   qkg = k [ 2 ] * vol [ 2 ] ;
   qai = a [ 0 ] * vol [ 0 ] ;
   qao = a [ 1 ] * vol [ 1 ] ;
   qag = a [ 2 ] * vol [ 2 ] ;
   }
  _sav_indep = t; t = _save;

}
}

static void nrn_init(_NrnThread* _nt, _Memb_list* _ml, int _type){
Node *_nd; double _v; int* _ni; int _iml, _cntml;
#if CACHEVEC
    _ni = _ml->_nodeindices;
#endif
_cntml = _ml->_nodecount;
for (_iml = 0; _iml < _cntml; ++_iml) {
 _p = _ml->_data[_iml]; _ppvar = _ml->_pdata[_iml];
#if CACHEVEC
  if (use_cachevec) {
    _v = VEC_V(_ni[_iml]);
  }else
#endif
  {
    _nd = _ml->_nodelist[_iml];
    _v = NODEV(_nd);
  }
 v = _v;
  ina = _ion_ina;
  nao = _ion_nao;
  nai = _ion_nai;
  nai = _ion_nai;
  nao = _ion_nao;
  ik = _ion_ik;
  ko = _ion_ko;
  ki = _ion_ki;
  ki = _ion_ki;
  ko = _ion_ko;
  icl = _ion_icl;
  clo = _ion_clo;
  cli = _ion_cli;
  cli = _ion_cli;
  clo = _ion_clo;
  ia = _ion_ia;
  ao = _ion_ao;
  ai = _ion_ai;
  ai = _ion_ai;
  ao = _ion_ao;
  ica = _ion_ica;
  cao = _ion_cao;
  cai = _ion_cai;
  cai = _ion_cai;
  cao = _ion_cao;
 initmodel();
  _ion_nai = nai;
  _ion_nao = nao;
   nrn_wrote_conc(_na_sym, (&(_ion_nao)) - 2, _style_na);
  _ion_ki = ki;
  _ion_ko = ko;
   nrn_wrote_conc(_k_sym, (&(_ion_ko)) - 2, _style_k);
  _ion_cli = cli;
  _ion_clo = clo;
   nrn_wrote_conc(_cl_sym, (&(_ion_clo)) - 2, _style_cl);
  _ion_ai = ai;
  _ion_ao = ao;
  nrn_wrote_conc(_a_sym, (&(_ion_ao)) - 2, _style_a);
  _ion_cai = cai;
  _ion_cao = cao;
   nrn_wrote_conc(_ca_sym, (&(_ion_cao)) - 2, _style_ca);
}}

static double _nrn_current(double _v){double _current=0.;v=_v;{ {
   }
 _current += ina;
 _current += ik;
 _current += icl;
 _current += ica;

} return _current;
}

static void nrn_cur(_NrnThread* _nt, _Memb_list* _ml, int _type){
Node *_nd; int* _ni; double _rhs, _v; int _iml, _cntml;
#if CACHEVEC
    _ni = _ml->_nodeindices;
#endif
_cntml = _ml->_nodecount;
for (_iml = 0; _iml < _cntml; ++_iml) {
 _p = _ml->_data[_iml]; _ppvar = _ml->_pdata[_iml];
#if CACHEVEC
  if (use_cachevec) {
    _v = VEC_V(_ni[_iml]);
  }else
#endif
  {
    _nd = _ml->_nodelist[_iml];
    _v = NODEV(_nd);
  }
  ina = _ion_ina;
  nao = _ion_nao;
  nai = _ion_nai;
  nai = _ion_nai;
  nao = _ion_nao;
  ik = _ion_ik;
  ko = _ion_ko;
  ki = _ion_ki;
  ki = _ion_ki;
  ko = _ion_ko;
  icl = _ion_icl;
  clo = _ion_clo;
  cli = _ion_cli;
  cli = _ion_cli;
  clo = _ion_clo;
  ia = _ion_ia;
  ao = _ion_ao;
  ai = _ion_ai;
  ai = _ion_ai;
  ao = _ion_ao;
  ica = _ion_ica;
  cao = _ion_cao;
  cai = _ion_cai;
  cai = _ion_cai;
  cao = _ion_cao;
if (_nt->_vcv) { _ode_spec1(); }
 _g = _nrn_current(_v + .001);
 	{ double _dica;
 double _dicl;
 double _dik;
 double _dina;
  _dina = ina;
  _dik = ik;
  _dicl = icl;
  _dica = ica;
 _rhs = _nrn_current(_v);
  _ion_dinadv += (_dina - ina)/.001 ;
  _ion_dikdv += (_dik - ik)/.001 ;
  _ion_dicldv += (_dicl - icl)/.001 ;
  _ion_dicadv += (_dica - ica)/.001 ;
 	}
 _g = (_g - _rhs)/.001;
  _ion_nai = nai;
  _ion_nao = nao;
  _ion_ina += ina ;
  _ion_ki = ki;
  _ion_ko = ko;
  _ion_ik += ik ;
  _ion_cli = cli;
  _ion_clo = clo;
  _ion_icl += icl ;
  _ion_ai = ai;
  _ion_ao = ao;
  _ion_cai = cai;
  _ion_cao = cao;
  _ion_ica += ica ;
#if CACHEVEC
  if (use_cachevec) {
	VEC_RHS(_ni[_iml]) -= _rhs;
  }else
#endif
  {
	NODERHS(_nd) -= _rhs;
  }
 
}}

static void nrn_jacob(_NrnThread* _nt, _Memb_list* _ml, int _type){
Node *_nd; int* _ni; int _iml, _cntml;
#if CACHEVEC
    _ni = _ml->_nodeindices;
#endif
_cntml = _ml->_nodecount;
for (_iml = 0; _iml < _cntml; ++_iml) {
 _p = _ml->_data[_iml];
#if CACHEVEC
  if (use_cachevec) {
	VEC_D(_ni[_iml]) += _g;
  }else
#endif
  {
     _nd = _ml->_nodelist[_iml];
	NODED(_nd) += _g;
  }
 
}}

static void nrn_state(_NrnThread* _nt, _Memb_list* _ml, int _type){
Node *_nd; double _v = 0.0; int* _ni; int _iml, _cntml;
double _dtsav = dt;
if (secondorder) { dt *= 0.5; }
#if CACHEVEC
    _ni = _ml->_nodeindices;
#endif
_cntml = _ml->_nodecount;
for (_iml = 0; _iml < _cntml; ++_iml) {
 _p = _ml->_data[_iml]; _ppvar = _ml->_pdata[_iml];
 _nd = _ml->_nodelist[_iml];
#if CACHEVEC
  if (use_cachevec) {
    _v = VEC_V(_ni[_iml]);
  }else
#endif
  {
    _nd = _ml->_nodelist[_iml];
    _v = NODEV(_nd);
  }
 v=_v;
{
  ina = _ion_ina;
  nao = _ion_nao;
  nai = _ion_nai;
  nai = _ion_nai;
  nao = _ion_nao;
  ik = _ion_ik;
  ko = _ion_ko;
  ki = _ion_ki;
  ki = _ion_ki;
  ko = _ion_ko;
  icl = _ion_icl;
  clo = _ion_clo;
  cli = _ion_cli;
  cli = _ion_cli;
  clo = _ion_clo;
  ia = _ion_ia;
  ao = _ion_ao;
  ai = _ion_ai;
  ai = _ion_ai;
  ao = _ion_ao;
  ica = _ion_ica;
  cao = _ion_cao;
  cai = _ion_cai;
  cai = _ion_cai;
  cao = _ion_cao;
 { error = sparse(&_sparseobj1, 18, _slist1, _dlist1, _p, &t, dt, state,&_coef1, _linmat1);
 if(error){fprintf(stderr,"at line 102 in file accum.mod:\n\n"); nrn_complain(_p); abort_run(error);}
    if (secondorder) {
    int _i;
    for (_i = 0; _i < 18; ++_i) {
      _p[_slist1[_i]] += dt*_p[_dlist1[_i]];
    }}
 }  _ion_nai = nai;
  _ion_nao = nao;
   _ion_ki = ki;
  _ion_ko = ko;
   _ion_cli = cli;
  _ion_clo = clo;
   _ion_ai = ai;
  _ion_ao = ao;
  _ion_cai = cai;
  _ion_cao = cao;
 }}
 dt = _dtsav;
}

static void terminal(){}

static void _initlists() {
 int _i; static int _first = 1;
  if (!_first) return;
 for(_i=0;_i<3;_i++){_slist1[0+_i] = (a + _i) - _p;  _dlist1[0+_i] = (Da + _i) - _p;}
 _slist1[3] = &(catot) - _p;  _dlist1[3] = &(Dcatot) - _p;
 for(_i=0;_i<2;_i++){_slist1[4+_i] = (ca + _i) - _p;  _dlist1[4+_i] = (Dca + _i) - _p;}
 for(_i=0;_i<3;_i++){_slist1[6+_i] = (cl + _i) - _p;  _dlist1[6+_i] = (Dcl + _i) - _p;}
 for(_i=0;_i<3;_i++){_slist1[9+_i] = (k + _i) - _p;  _dlist1[9+_i] = (Dk + _i) - _p;}
 for(_i=0;_i<3;_i++){_slist1[12+_i] = (na + _i) - _p;  _dlist1[12+_i] = (Dna + _i) - _p;}
 for(_i=0;_i<3;_i++){_slist1[15+_i] = (vol + _i) - _p;  _dlist1[15+_i] = (Dvol + _i) - _p;}
_first = 0;
}
