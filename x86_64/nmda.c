/* Created by Language version: 7.5.0 */
/* VECTORIZED */
#define NRN_VECTORIZED 1
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
 
#if METHOD3
extern int _method3;
#endif

#if !NRNGPU
#undef exp
#define exp hoc_Exp
extern double hoc_Exp(double);
#endif
 
#define nrn_init _nrn_init__nmda
#define _nrn_initial _nrn_initial__nmda
#define nrn_cur _nrn_cur__nmda
#define _nrn_current _nrn_current__nmda
#define nrn_jacob _nrn_jacob__nmda
#define nrn_state _nrn_state__nmda
#define _net_receive _net_receive__nmda 
#define synstate synstate__nmda 
 
#define _threadargscomma_ _p, _ppvar, _thread, _nt,
#define _threadargsprotocomma_ double* _p, Datum* _ppvar, Datum* _thread, _NrnThread* _nt,
#define _threadargs_ _p, _ppvar, _thread, _nt
#define _threadargsproto_ double* _p, Datum* _ppvar, Datum* _thread, _NrnThread* _nt
 	/*SUPPRESS 761*/
	/*SUPPRESS 762*/
	/*SUPPRESS 763*/
	/*SUPPRESS 765*/
	 extern double *getarg();
 /* Thread safe. No static _p or _ppvar. */
 
#define t _nt->_t
#define dt _nt->_dt
#define itot _p[0]
#define ik _p[1]
#define ina _p[2]
#define ica _p[3]
#define ma _p[4]
#define mb _p[5]
#define ha _p[6]
#define hb _p[7]
#define qna _p[8]
#define qk _p[9]
#define ki _p[10]
#define ko _p[11]
#define ek _p[12]
#define nai _p[13]
#define nao _p[14]
#define ena _p[15]
#define cai _p[16]
#define cao _p[17]
#define eca _p[18]
#define Dma _p[19]
#define Dmb _p[20]
#define Dha _p[21]
#define Dhb _p[22]
#define Dqna _p[23]
#define Dqk _p[24]
#define v _p[25]
#define _g _p[26]
#define _ion_ko	*_ppvar[0]._pval
#define _ion_ki	*_ppvar[1]._pval
#define _ion_ek	*_ppvar[2]._pval
#define _ion_ik	*_ppvar[3]._pval
#define _ion_dikdv	*_ppvar[4]._pval
#define _ion_nai	*_ppvar[5]._pval
#define _ion_nao	*_ppvar[6]._pval
#define _ion_ena	*_ppvar[7]._pval
#define _ion_ina	*_ppvar[8]._pval
#define _ion_dinadv	*_ppvar[9]._pval
#define _ion_cai	*_ppvar[10]._pval
#define _ion_cao	*_ppvar[11]._pval
#define _ion_eca	*_ppvar[12]._pval
#define _ion_ica	*_ppvar[13]._pval
#define _ion_dicadv	*_ppvar[14]._pval
#define diam	*_ppvar[15]._pval
 
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
 static int hoc_nrnpointerindex =  -1;
 static Datum* _extcall_thread;
 static Prop* _extcall_prop;
 /* external NEURON variables */
 extern double celsius;
 /* declaration of user functions */
 static void _hoc_efun(void);
 static void _hoc_ghk(void);
 static void _hoc_h_b(void);
 static void _hoc_h_a(void);
 static void _hoc_h_inf(void);
 static void _hoc_m_b(void);
 static void _hoc_m_a(void);
 static void _hoc_m_inf(void);
 static int _mechtype;
extern void _nrn_cacheloop_reg(int, int);
extern void hoc_register_prop_size(int, int, int);
extern void hoc_register_limits(int, HocParmLimits*);
extern void hoc_register_units(int, HocParmUnits*);
extern void nrn_promote(Prop*, int, int);
extern Memb_func* memb_func;
 extern void _nrn_setdata_reg(int, void(*)(Prop*));
 static void _setdata(Prop* _prop) {
 _extcall_prop = _prop;
 }
 static void _hoc_setdata() {
 Prop *_prop, *hoc_getdata_range(int);
 _prop = hoc_getdata_range(_mechtype);
   _setdata(_prop);
 hoc_retpushx(1.);
}
 /* connect user functions to hoc names */
 static VoidFunc hoc_intfunc[] = {
 "setdata_nmda", _hoc_setdata,
 "efun_nmda", _hoc_efun,
 "ghk_nmda", _hoc_ghk,
 "h_b_nmda", _hoc_h_b,
 "h_a_nmda", _hoc_h_a,
 "h_inf_nmda", _hoc_h_inf,
 "m_b_nmda", _hoc_m_b,
 "m_a_nmda", _hoc_m_a,
 "m_inf_nmda", _hoc_m_inf,
 0, 0
};
#define _f_h_inf _f_h_inf_nmda
#define _f_h_b _f_h_b_nmda
#define _f_h_a _f_h_a_nmda
#define _f_m_inf _f_m_inf_nmda
#define _f_m_b _f_m_b_nmda
#define _f_m_a _f_m_a_nmda
#define efun efun_nmda
#define ghk ghk_nmda
#define h_b h_b_nmda
#define h_a h_a_nmda
#define h_inf h_inf_nmda
#define m_b m_b_nmda
#define m_a m_a_nmda
#define m_inf m_inf_nmda
 extern double _f_h_inf( _threadargsprotocomma_ double );
 extern double _f_h_b( _threadargsprotocomma_ double );
 extern double _f_h_a( _threadargsprotocomma_ double );
 extern double _f_m_inf( _threadargsprotocomma_ double );
 extern double _f_m_b( _threadargsprotocomma_ double );
 extern double _f_m_a( _threadargsprotocomma_ double );
 extern double efun( _threadargsprotocomma_ double );
 extern double ghk( _threadargsprotocomma_ double , double , double );
 extern double h_b( _threadargsprotocomma_ double );
 extern double h_a( _threadargsprotocomma_ double );
 extern double h_inf( _threadargsprotocomma_ double );
 extern double m_b( _threadargsprotocomma_ double );
 extern double m_a( _threadargsprotocomma_ double );
 extern double m_inf( _threadargsprotocomma_ double );
 
static void _check_m_a(double*, Datum*, Datum*, _NrnThread*); 
static void _check_m_b(double*, Datum*, Datum*, _NrnThread*); 
static void _check_m_inf(double*, Datum*, Datum*, _NrnThread*); 
static void _check_h_a(double*, Datum*, Datum*, _NrnThread*); 
static void _check_h_b(double*, Datum*, Datum*, _NrnThread*); 
static void _check_h_inf(double*, Datum*, Datum*, _NrnThread*); 
static void _check_table_thread(double* _p, Datum* _ppvar, Datum* _thread, _NrnThread* _nt, int _type) {
   _check_m_a(_p, _ppvar, _thread, _nt);
   _check_m_b(_p, _ppvar, _thread, _nt);
   _check_m_inf(_p, _ppvar, _thread, _nt);
   _check_h_a(_p, _ppvar, _thread, _nt);
   _check_h_b(_p, _ppvar, _thread, _nt);
   _check_h_inf(_p, _ppvar, _thread, _nt);
 }
 #define _za1 _thread[2]._pval[0]
 #define _za2 _thread[2]._pval[1]
 #define _zb1 _thread[2]._pval[2]
 #define _zb2 _thread[2]._pval[3]
 /* declare global and static user variables */
#define act_01 act_01_nmda
 double act_01 = 10;
#define act_99 act_99_nmda
 double act_99 = 20;
#define gbar gbar_nmda
 double gbar = 0.001;
#define ina_01 ina_01_nmda
 double ina_01 = 10;
#define ina_99 ina_99_nmda
 double ina_99 = 3.5;
#define mg mg_nmda
 double mg = 1.2;
#define scaleca scaleca_nmda
 double scaleca = 1;
#define tau_act tau_act_nmda
 double tau_act = 2;
#define tau_ina tau_ina_nmda
 double tau_ina = 2000;
#define usetable usetable_nmda
 double usetable = 1;
 /* some parameters have upper and lower limits */
 static HocParmLimits _hoc_parm_limits[] = {
 "usetable_nmda", 0, 1,
 0,0,0
};
 static HocParmUnits _hoc_parm_units[] = {
 "gbar_nmda", "mho/cm2",
 "tau_ina_nmda", "ms",
 "tau_act_nmda", "ms",
 "act_99_nmda", "mM",
 "act_01_nmda", "mM",
 "ina_99_nmda", "mM",
 "ina_01_nmda", "mM",
 "mg_nmda", "mM",
 "itot_nmda", "mA/cm2",
 "ik_nmda", "mA/cm2",
 "ina_nmda", "mA/cm2",
 "ica_nmda", "mA/cm2",
 0,0
};
 static double delta_t = 0.01;
 static double hb0 = 0;
 static double ha0 = 0;
 static double mb0 = 0;
 static double ma0 = 0;
 static double qk0 = 0;
 static double qna0 = 0;
 /* connect global user variables to hoc */
 static DoubScal hoc_scdoub[] = {
 "gbar_nmda", &gbar_nmda,
 "tau_ina_nmda", &tau_ina_nmda,
 "tau_act_nmda", &tau_act_nmda,
 "act_99_nmda", &act_99_nmda,
 "act_01_nmda", &act_01_nmda,
 "ina_99_nmda", &ina_99_nmda,
 "ina_01_nmda", &ina_01_nmda,
 "mg_nmda", &mg_nmda,
 "scaleca_nmda", &scaleca_nmda,
 "usetable_nmda", &usetable_nmda,
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
 
#define _cvode_ieq _ppvar[16]._i
 static void _ode_matsol_instance1(_threadargsproto_);
 /* connect range variables in _p that hoc is supposed to know about */
 static const char *_mechanism[] = {
 "7.5.0",
"nmda",
 0,
 "itot_nmda",
 "ik_nmda",
 "ina_nmda",
 "ica_nmda",
 0,
 "ma_nmda",
 "mb_nmda",
 "ha_nmda",
 "hb_nmda",
 "qna_nmda",
 "qk_nmda",
 0,
 0};
 static Symbol* _morphology_sym;
 static Symbol* _k_sym;
 static Symbol* _na_sym;
 static Symbol* _ca_sym;
 
extern Prop* need_memb(Symbol*);

static void nrn_alloc(Prop* _prop) {
	Prop *prop_ion;
	double *_p; Datum *_ppvar;
 	_p = nrn_prop_data_alloc(_mechtype, 27, _prop);
 	/*initialize range parameters*/
 	_prop->param = _p;
 	_prop->param_size = 27;
 	_ppvar = nrn_prop_datum_alloc(_mechtype, 17, _prop);
 	_prop->dparam = _ppvar;
 	/*connect ionic variables to this model*/
 prop_ion = need_memb(_morphology_sym);
 	_ppvar[15]._pval = &prop_ion->param[0]; /* diam */
 prop_ion = need_memb(_k_sym);
 nrn_promote(prop_ion, 1, 1);
 	_ppvar[0]._pval = &prop_ion->param[2]; /* ko */
 	_ppvar[1]._pval = &prop_ion->param[1]; /* ki */
 	_ppvar[2]._pval = &prop_ion->param[0]; /* ek */
 	_ppvar[3]._pval = &prop_ion->param[3]; /* ik */
 	_ppvar[4]._pval = &prop_ion->param[4]; /* _ion_dikdv */
 prop_ion = need_memb(_na_sym);
 nrn_promote(prop_ion, 1, 1);
 	_ppvar[5]._pval = &prop_ion->param[1]; /* nai */
 	_ppvar[6]._pval = &prop_ion->param[2]; /* nao */
 	_ppvar[7]._pval = &prop_ion->param[0]; /* ena */
 	_ppvar[8]._pval = &prop_ion->param[3]; /* ina */
 	_ppvar[9]._pval = &prop_ion->param[4]; /* _ion_dinadv */
 prop_ion = need_memb(_ca_sym);
 nrn_promote(prop_ion, 1, 1);
 	_ppvar[10]._pval = &prop_ion->param[1]; /* cai */
 	_ppvar[11]._pval = &prop_ion->param[2]; /* cao */
 	_ppvar[12]._pval = &prop_ion->param[0]; /* eca */
 	_ppvar[13]._pval = &prop_ion->param[3]; /* ica */
 	_ppvar[14]._pval = &prop_ion->param[4]; /* _ion_dicadv */
 
}
 static void _initlists();
  /* some states have an absolute tolerance */
 static Symbol** _atollist;
 static HocStateTolerance _hoc_state_tol[] = {
 0,0
};
 static void _thread_mem_init(Datum*);
 static void _thread_cleanup(Datum*);
 static void _update_ion_pointer(Datum*);
 extern Symbol* hoc_lookup(const char*);
extern void _nrn_thread_reg(int, int, void(*)(Datum*));
extern void _nrn_thread_table_reg(int, void(*)(double*, Datum*, Datum*, _NrnThread*, int));
extern void hoc_register_tolerance(int, HocStateTolerance*, Symbol***);
extern void _cvode_abstol( Symbol**, double*, int);

 void _nmda_reg() {
	int _vectorized = 1;
  _initlists();
 	ion_reg("k", -10000.);
 	ion_reg("na", -10000.);
 	ion_reg("ca", 2.0);
 	_morphology_sym = hoc_lookup("morphology");
 	_k_sym = hoc_lookup("k_ion");
 	_na_sym = hoc_lookup("na_ion");
 	_ca_sym = hoc_lookup("ca_ion");
 	register_mech(_mechanism, nrn_alloc,nrn_cur, nrn_jacob, nrn_state, nrn_init, hoc_nrnpointerindex, 4);
  _extcall_thread = (Datum*)ecalloc(3, sizeof(Datum));
  _thread_mem_init(_extcall_thread);
 _mechtype = nrn_get_mechtype(_mechanism[1]);
     _nrn_setdata_reg(_mechtype, _setdata);
     _nrn_thread_reg(_mechtype, 1, _thread_mem_init);
     _nrn_thread_reg(_mechtype, 0, _thread_cleanup);
     _nrn_thread_reg(_mechtype, 2, _update_ion_pointer);
     _nrn_thread_table_reg(_mechtype, _check_table_thread);
  hoc_register_prop_size(_mechtype, 27, 17);
  hoc_register_dparam_semantics(_mechtype, 0, "k_ion");
  hoc_register_dparam_semantics(_mechtype, 1, "k_ion");
  hoc_register_dparam_semantics(_mechtype, 2, "k_ion");
  hoc_register_dparam_semantics(_mechtype, 3, "k_ion");
  hoc_register_dparam_semantics(_mechtype, 4, "k_ion");
  hoc_register_dparam_semantics(_mechtype, 5, "na_ion");
  hoc_register_dparam_semantics(_mechtype, 6, "na_ion");
  hoc_register_dparam_semantics(_mechtype, 7, "na_ion");
  hoc_register_dparam_semantics(_mechtype, 8, "na_ion");
  hoc_register_dparam_semantics(_mechtype, 9, "na_ion");
  hoc_register_dparam_semantics(_mechtype, 10, "ca_ion");
  hoc_register_dparam_semantics(_mechtype, 11, "ca_ion");
  hoc_register_dparam_semantics(_mechtype, 12, "ca_ion");
  hoc_register_dparam_semantics(_mechtype, 13, "ca_ion");
  hoc_register_dparam_semantics(_mechtype, 14, "ca_ion");
  hoc_register_dparam_semantics(_mechtype, 16, "cvodeieq");
  hoc_register_dparam_semantics(_mechtype, 15, "diam");
 	hoc_register_cvode(_mechtype, _ode_count, _ode_map, _ode_spec, _ode_matsol);
 	hoc_register_tolerance(_mechtype, _hoc_state_tol, &_atollist);
 	hoc_register_var(hoc_scdoub, hoc_vdoub, hoc_intfunc);
 	ivoc_help("help ?1 nmda /Users/sulgod/spreading-depression/x86_64/nmda.mod\n");
 hoc_register_limits(_mechtype, _hoc_parm_limits);
 hoc_register_units(_mechtype, _hoc_parm_units);
 }
 static double FARADAY = 96485.309;
 static double R = 8.3145;
 static double PI = 3.14159;
 /*Top LOCAL _za1 , _za2 , _zb1 , _zb2 */
 static double *_t_m_a;
 static double *_t_m_b;
 static double *_t_m_inf;
 static double *_t_h_a;
 static double *_t_h_b;
 static double *_t_h_inf;
static int _reset;
static char *modelname = "nmda";

static int error;
static int _ninits = 0;
static int _match_recurse=1;
static void _modl_cleanup(){ _match_recurse=1;}
 extern double *_nrn_thread_getelm();
 
#define _MATELM1(_row,_col) *(_nrn_thread_getelm(_so, _row + 1, _col + 1))
 
#define _RHS1(_arg) _rhs[_arg+1]
  
#define _linmat1  1
 static int _spth1 = 1;
 static int _cvspth1 = 0;
 
static int _ode_spec1(_threadargsproto_);
/*static int _ode_matsol1(_threadargsproto_);*/
 static double _n_h_inf(_threadargsprotocomma_ double _lv);
 static double _n_h_b(_threadargsprotocomma_ double _lv);
 static double _n_h_a(_threadargsprotocomma_ double _lv);
 static double _n_m_inf(_threadargsprotocomma_ double _lv);
 static double _n_m_b(_threadargsprotocomma_ double _lv);
 static double _n_m_a(_threadargsprotocomma_ double _lv);
 static int _slist1[6], _dlist1[6]; static double *_temp1;
 static int synstate();
 
static int synstate (void* _so, double* _rhs, double* _p, Datum* _ppvar, Datum* _thread, _NrnThread* _nt)
 {int _reset=0;
 {
   double b_flux, f_flux, _term; int _i;
 {int _i; double _dt1 = 1.0/dt;
for(_i=0;_i<6;_i++){
  	_RHS1(_i) = -_dt1*(_p[_slist1[_i]] - _p[_dlist1[_i]]);
	_MATELM1(_i, _i) = _dt1;
      
}  
_RHS1(4) *= ( diam * diam * PI / 4.0) ;
_MATELM1(4, 4) *= ( diam * diam * PI / 4.0); 
_RHS1(5) *= ( diam * diam * PI / 4.0) ;
_MATELM1(5, 5) *= ( diam * diam * PI / 4.0);  }
 _za1 = m_a ( _threadargscomma_ ko ) ;
   _za2 = m_b ( _threadargscomma_ ko ) ;
   _zb1 = h_a ( _threadargscomma_ ko ) ;
   _zb2 = h_b ( _threadargscomma_ ko ) ;
   /* ~ mb <-> ma ( _za1 , _za2 )*/
 f_flux =  _za1 * mb ;
 b_flux =  _za2 * ma ;
 _RHS1( 2) -= (f_flux - b_flux);
 _RHS1( 3) += (f_flux - b_flux);
 
 _term =  _za1 ;
 _MATELM1( 2 ,2)  += _term;
 _MATELM1( 3 ,2)  -= _term;
 _term =  _za2 ;
 _MATELM1( 2 ,3)  -= _term;
 _MATELM1( 3 ,3)  += _term;
 /*REACTION*/
  /* ~ hb <-> ha ( _zb1 , _zb2 )*/
 f_flux =  _zb1 * hb ;
 b_flux =  _zb2 * ha ;
 _RHS1( 0) -= (f_flux - b_flux);
 _RHS1( 1) += (f_flux - b_flux);
 
 _term =  _zb1 ;
 _MATELM1( 0 ,0)  += _term;
 _MATELM1( 1 ,0)  -= _term;
 _term =  _zb2 ;
 _MATELM1( 0 ,1)  -= _term;
 _MATELM1( 1 ,1)  += _term;
 /*REACTION*/
  /* COMPARTMENT diam * diam * PI / 4.0 {
     qna qk }
   */
 /* ~ qna < < ( - ina * PI * diam * ( 1e4 ) / FARADAY )*/
 f_flux = b_flux = 0.;
 _RHS1( 5) += (b_flux =   ( - ina * PI * diam * ( 1e4 ) / FARADAY ) );
 /*FLUX*/
  /* ~ qk < < ( - ik * PI * diam * ( 1e4 ) / FARADAY )*/
 f_flux = b_flux = 0.;
 _RHS1( 4) += (b_flux =   ( - ik * PI * diam * ( 1e4 ) / FARADAY ) );
 /*FLUX*/
    } return _reset;
 }
 static double _mfac_m_a, _tmin_m_a;
  static void _check_m_a(double* _p, Datum* _ppvar, Datum* _thread, _NrnThread* _nt) {
  static int _maktable=1; int _i, _j, _ix = 0;
  double _xi, _tmax;
  static double _sav_act_99;
  static double _sav_act_01;
  static double _sav_tau_act;
  if (!usetable) {return;}
  if (_sav_act_99 != act_99) { _maktable = 1;}
  if (_sav_act_01 != act_01) { _maktable = 1;}
  if (_sav_tau_act != tau_act) { _maktable = 1;}
  if (_maktable) { double _x, _dx; _maktable=0;
   _tmin_m_a =  0.0 ;
   _tmax =  150.0 ;
   _dx = (_tmax - _tmin_m_a)/150.; _mfac_m_a = 1./_dx;
   for (_i=0, _x=_tmin_m_a; _i < 151; _x += _dx, _i++) {
    _t_m_a[_i] = _f_m_a(_p, _ppvar, _thread, _nt, _x);
   }
   _sav_act_99 = act_99;
   _sav_act_01 = act_01;
   _sav_tau_act = tau_act;
  }
 }

 double m_a(double* _p, Datum* _ppvar, Datum* _thread, _NrnThread* _nt, double _lko) { 
#if 0
_check_m_a(_p, _ppvar, _thread, _nt);
#endif
 return _n_m_a(_p, _ppvar, _thread, _nt, _lko);
 }

 static double _n_m_a(double* _p, Datum* _ppvar, Datum* _thread, _NrnThread* _nt, double _lko){ int _i, _j;
 double _xi, _theta;
 if (!usetable) {
 return _f_m_a(_p, _ppvar, _thread, _nt, _lko); 
}
 _xi = _mfac_m_a * (_lko - _tmin_m_a);
 if (isnan(_xi)) {
  return _xi; }
 if (_xi <= 0.) {
 return _t_m_a[0];
 }
 if (_xi >= 150.) {
 return _t_m_a[150];
 }
 _i = (int) _xi;
 return _t_m_a[_i] + (_xi - (double)_i)*(_t_m_a[_i+1] - _t_m_a[_i]);
 }

 
double _f_m_a ( _threadargsprotocomma_ double _lko ) {
   double _lm_a;
 _lm_a = m_inf ( _threadargscomma_ _lko ) / tau_act ;
   
return _lm_a;
 }
 
static void _hoc_m_a(void) {
  double _r;
   double* _p; Datum* _ppvar; Datum* _thread; _NrnThread* _nt;
   if (_extcall_prop) {_p = _extcall_prop->param; _ppvar = _extcall_prop->dparam;}else{ _p = (double*)0; _ppvar = (Datum*)0; }
  _thread = _extcall_thread;
  _nt = nrn_threads;
 
#if 1
 _check_m_a(_p, _ppvar, _thread, _nt);
#endif
 _r =  m_a ( _p, _ppvar, _thread, _nt, *getarg(1) );
 hoc_retpushx(_r);
}
 static double _mfac_m_b, _tmin_m_b;
  static void _check_m_b(double* _p, Datum* _ppvar, Datum* _thread, _NrnThread* _nt) {
  static int _maktable=1; int _i, _j, _ix = 0;
  double _xi, _tmax;
  static double _sav_act_99;
  static double _sav_act_01;
  static double _sav_tau_act;
  if (!usetable) {return;}
  if (_sav_act_99 != act_99) { _maktable = 1;}
  if (_sav_act_01 != act_01) { _maktable = 1;}
  if (_sav_tau_act != tau_act) { _maktable = 1;}
  if (_maktable) { double _x, _dx; _maktable=0;
   _tmin_m_b =  0.0 ;
   _tmax =  150.0 ;
   _dx = (_tmax - _tmin_m_b)/150.; _mfac_m_b = 1./_dx;
   for (_i=0, _x=_tmin_m_b; _i < 151; _x += _dx, _i++) {
    _t_m_b[_i] = _f_m_b(_p, _ppvar, _thread, _nt, _x);
   }
   _sav_act_99 = act_99;
   _sav_act_01 = act_01;
   _sav_tau_act = tau_act;
  }
 }

 double m_b(double* _p, Datum* _ppvar, Datum* _thread, _NrnThread* _nt, double _lko) { 
#if 0
_check_m_b(_p, _ppvar, _thread, _nt);
#endif
 return _n_m_b(_p, _ppvar, _thread, _nt, _lko);
 }

 static double _n_m_b(double* _p, Datum* _ppvar, Datum* _thread, _NrnThread* _nt, double _lko){ int _i, _j;
 double _xi, _theta;
 if (!usetable) {
 return _f_m_b(_p, _ppvar, _thread, _nt, _lko); 
}
 _xi = _mfac_m_b * (_lko - _tmin_m_b);
 if (isnan(_xi)) {
  return _xi; }
 if (_xi <= 0.) {
 return _t_m_b[0];
 }
 if (_xi >= 150.) {
 return _t_m_b[150];
 }
 _i = (int) _xi;
 return _t_m_b[_i] + (_xi - (double)_i)*(_t_m_b[_i+1] - _t_m_b[_i]);
 }

 
double _f_m_b ( _threadargsprotocomma_ double _lko ) {
   double _lm_b;
 _lm_b = ( 1.0 - m_inf ( _threadargscomma_ _lko ) ) / tau_act ;
   
return _lm_b;
 }
 
static void _hoc_m_b(void) {
  double _r;
   double* _p; Datum* _ppvar; Datum* _thread; _NrnThread* _nt;
   if (_extcall_prop) {_p = _extcall_prop->param; _ppvar = _extcall_prop->dparam;}else{ _p = (double*)0; _ppvar = (Datum*)0; }
  _thread = _extcall_thread;
  _nt = nrn_threads;
 
#if 1
 _check_m_b(_p, _ppvar, _thread, _nt);
#endif
 _r =  m_b ( _p, _ppvar, _thread, _nt, *getarg(1) );
 hoc_retpushx(_r);
}
 static double _mfac_m_inf, _tmin_m_inf;
  static void _check_m_inf(double* _p, Datum* _ppvar, Datum* _thread, _NrnThread* _nt) {
  static int _maktable=1; int _i, _j, _ix = 0;
  double _xi, _tmax;
  static double _sav_act_99;
  static double _sav_act_01;
  static double _sav_tau_act;
  if (!usetable) {return;}
  if (_sav_act_99 != act_99) { _maktable = 1;}
  if (_sav_act_01 != act_01) { _maktable = 1;}
  if (_sav_tau_act != tau_act) { _maktable = 1;}
  if (_maktable) { double _x, _dx; _maktable=0;
   _tmin_m_inf =  0.0 ;
   _tmax =  150.0 ;
   _dx = (_tmax - _tmin_m_inf)/150.; _mfac_m_inf = 1./_dx;
   for (_i=0, _x=_tmin_m_inf; _i < 151; _x += _dx, _i++) {
    _t_m_inf[_i] = _f_m_inf(_p, _ppvar, _thread, _nt, _x);
   }
   _sav_act_99 = act_99;
   _sav_act_01 = act_01;
   _sav_tau_act = tau_act;
  }
 }

 double m_inf(double* _p, Datum* _ppvar, Datum* _thread, _NrnThread* _nt, double _lko) { 
#if 0
_check_m_inf(_p, _ppvar, _thread, _nt);
#endif
 return _n_m_inf(_p, _ppvar, _thread, _nt, _lko);
 }

 static double _n_m_inf(double* _p, Datum* _ppvar, Datum* _thread, _NrnThread* _nt, double _lko){ int _i, _j;
 double _xi, _theta;
 if (!usetable) {
 return _f_m_inf(_p, _ppvar, _thread, _nt, _lko); 
}
 _xi = _mfac_m_inf * (_lko - _tmin_m_inf);
 if (isnan(_xi)) {
  return _xi; }
 if (_xi <= 0.) {
 return _t_m_inf[0];
 }
 if (_xi >= 150.) {
 return _t_m_inf[150];
 }
 _i = (int) _xi;
 return _t_m_inf[_i] + (_xi - (double)_i)*(_t_m_inf[_i+1] - _t_m_inf[_i]);
 }

 
double _f_m_inf ( _threadargsprotocomma_ double _lko ) {
   double _lm_inf;
 double _lkh , _lh ;
 _lkh = ( act_99 + act_01 ) / 2.0 ;
   _lh = - ( _lkh - act_99 ) / 4.59 ;
   _lm_inf = 1.0 / ( 1.0 + ( exp ( ( _lkh - _lko ) / _lh ) ) ) ;
   
return _lm_inf;
 }
 
static void _hoc_m_inf(void) {
  double _r;
   double* _p; Datum* _ppvar; Datum* _thread; _NrnThread* _nt;
   if (_extcall_prop) {_p = _extcall_prop->param; _ppvar = _extcall_prop->dparam;}else{ _p = (double*)0; _ppvar = (Datum*)0; }
  _thread = _extcall_thread;
  _nt = nrn_threads;
 
#if 1
 _check_m_inf(_p, _ppvar, _thread, _nt);
#endif
 _r =  m_inf ( _p, _ppvar, _thread, _nt, *getarg(1) );
 hoc_retpushx(_r);
}
 static double _mfac_h_a, _tmin_h_a;
  static void _check_h_a(double* _p, Datum* _ppvar, Datum* _thread, _NrnThread* _nt) {
  static int _maktable=1; int _i, _j, _ix = 0;
  double _xi, _tmax;
  static double _sav_ina_99;
  static double _sav_ina_01;
  static double _sav_tau_ina;
  if (!usetable) {return;}
  if (_sav_ina_99 != ina_99) { _maktable = 1;}
  if (_sav_ina_01 != ina_01) { _maktable = 1;}
  if (_sav_tau_ina != tau_ina) { _maktable = 1;}
  if (_maktable) { double _x, _dx; _maktable=0;
   _tmin_h_a =  0.0 ;
   _tmax =  150.0 ;
   _dx = (_tmax - _tmin_h_a)/150.; _mfac_h_a = 1./_dx;
   for (_i=0, _x=_tmin_h_a; _i < 151; _x += _dx, _i++) {
    _t_h_a[_i] = _f_h_a(_p, _ppvar, _thread, _nt, _x);
   }
   _sav_ina_99 = ina_99;
   _sav_ina_01 = ina_01;
   _sav_tau_ina = tau_ina;
  }
 }

 double h_a(double* _p, Datum* _ppvar, Datum* _thread, _NrnThread* _nt, double _lko) { 
#if 0
_check_h_a(_p, _ppvar, _thread, _nt);
#endif
 return _n_h_a(_p, _ppvar, _thread, _nt, _lko);
 }

 static double _n_h_a(double* _p, Datum* _ppvar, Datum* _thread, _NrnThread* _nt, double _lko){ int _i, _j;
 double _xi, _theta;
 if (!usetable) {
 return _f_h_a(_p, _ppvar, _thread, _nt, _lko); 
}
 _xi = _mfac_h_a * (_lko - _tmin_h_a);
 if (isnan(_xi)) {
  return _xi; }
 if (_xi <= 0.) {
 return _t_h_a[0];
 }
 if (_xi >= 150.) {
 return _t_h_a[150];
 }
 _i = (int) _xi;
 return _t_h_a[_i] + (_xi - (double)_i)*(_t_h_a[_i+1] - _t_h_a[_i]);
 }

 
double _f_h_a ( _threadargsprotocomma_ double _lko ) {
   double _lh_a;
 _lh_a = h_inf ( _threadargscomma_ _lko ) / tau_ina ;
   
return _lh_a;
 }
 
static void _hoc_h_a(void) {
  double _r;
   double* _p; Datum* _ppvar; Datum* _thread; _NrnThread* _nt;
   if (_extcall_prop) {_p = _extcall_prop->param; _ppvar = _extcall_prop->dparam;}else{ _p = (double*)0; _ppvar = (Datum*)0; }
  _thread = _extcall_thread;
  _nt = nrn_threads;
 
#if 1
 _check_h_a(_p, _ppvar, _thread, _nt);
#endif
 _r =  h_a ( _p, _ppvar, _thread, _nt, *getarg(1) );
 hoc_retpushx(_r);
}
 static double _mfac_h_b, _tmin_h_b;
  static void _check_h_b(double* _p, Datum* _ppvar, Datum* _thread, _NrnThread* _nt) {
  static int _maktable=1; int _i, _j, _ix = 0;
  double _xi, _tmax;
  static double _sav_ina_99;
  static double _sav_ina_01;
  static double _sav_tau_ina;
  if (!usetable) {return;}
  if (_sav_ina_99 != ina_99) { _maktable = 1;}
  if (_sav_ina_01 != ina_01) { _maktable = 1;}
  if (_sav_tau_ina != tau_ina) { _maktable = 1;}
  if (_maktable) { double _x, _dx; _maktable=0;
   _tmin_h_b =  0.0 ;
   _tmax =  150.0 ;
   _dx = (_tmax - _tmin_h_b)/150.; _mfac_h_b = 1./_dx;
   for (_i=0, _x=_tmin_h_b; _i < 151; _x += _dx, _i++) {
    _t_h_b[_i] = _f_h_b(_p, _ppvar, _thread, _nt, _x);
   }
   _sav_ina_99 = ina_99;
   _sav_ina_01 = ina_01;
   _sav_tau_ina = tau_ina;
  }
 }

 double h_b(double* _p, Datum* _ppvar, Datum* _thread, _NrnThread* _nt, double _lko) { 
#if 0
_check_h_b(_p, _ppvar, _thread, _nt);
#endif
 return _n_h_b(_p, _ppvar, _thread, _nt, _lko);
 }

 static double _n_h_b(double* _p, Datum* _ppvar, Datum* _thread, _NrnThread* _nt, double _lko){ int _i, _j;
 double _xi, _theta;
 if (!usetable) {
 return _f_h_b(_p, _ppvar, _thread, _nt, _lko); 
}
 _xi = _mfac_h_b * (_lko - _tmin_h_b);
 if (isnan(_xi)) {
  return _xi; }
 if (_xi <= 0.) {
 return _t_h_b[0];
 }
 if (_xi >= 150.) {
 return _t_h_b[150];
 }
 _i = (int) _xi;
 return _t_h_b[_i] + (_xi - (double)_i)*(_t_h_b[_i+1] - _t_h_b[_i]);
 }

 
double _f_h_b ( _threadargsprotocomma_ double _lko ) {
   double _lh_b;
 _lh_b = ( 1.0 - h_inf ( _threadargscomma_ _lko ) ) / tau_ina ;
   
return _lh_b;
 }
 
static void _hoc_h_b(void) {
  double _r;
   double* _p; Datum* _ppvar; Datum* _thread; _NrnThread* _nt;
   if (_extcall_prop) {_p = _extcall_prop->param; _ppvar = _extcall_prop->dparam;}else{ _p = (double*)0; _ppvar = (Datum*)0; }
  _thread = _extcall_thread;
  _nt = nrn_threads;
 
#if 1
 _check_h_b(_p, _ppvar, _thread, _nt);
#endif
 _r =  h_b ( _p, _ppvar, _thread, _nt, *getarg(1) );
 hoc_retpushx(_r);
}
 static double _mfac_h_inf, _tmin_h_inf;
  static void _check_h_inf(double* _p, Datum* _ppvar, Datum* _thread, _NrnThread* _nt) {
  static int _maktable=1; int _i, _j, _ix = 0;
  double _xi, _tmax;
  static double _sav_ina_99;
  static double _sav_ina_01;
  static double _sav_tau_ina;
  if (!usetable) {return;}
  if (_sav_ina_99 != ina_99) { _maktable = 1;}
  if (_sav_ina_01 != ina_01) { _maktable = 1;}
  if (_sav_tau_ina != tau_ina) { _maktable = 1;}
  if (_maktable) { double _x, _dx; _maktable=0;
   _tmin_h_inf =  0.0 ;
   _tmax =  150.0 ;
   _dx = (_tmax - _tmin_h_inf)/150.; _mfac_h_inf = 1./_dx;
   for (_i=0, _x=_tmin_h_inf; _i < 151; _x += _dx, _i++) {
    _t_h_inf[_i] = _f_h_inf(_p, _ppvar, _thread, _nt, _x);
   }
   _sav_ina_99 = ina_99;
   _sav_ina_01 = ina_01;
   _sav_tau_ina = tau_ina;
  }
 }

 double h_inf(double* _p, Datum* _ppvar, Datum* _thread, _NrnThread* _nt, double _lko) { 
#if 0
_check_h_inf(_p, _ppvar, _thread, _nt);
#endif
 return _n_h_inf(_p, _ppvar, _thread, _nt, _lko);
 }

 static double _n_h_inf(double* _p, Datum* _ppvar, Datum* _thread, _NrnThread* _nt, double _lko){ int _i, _j;
 double _xi, _theta;
 if (!usetable) {
 return _f_h_inf(_p, _ppvar, _thread, _nt, _lko); 
}
 _xi = _mfac_h_inf * (_lko - _tmin_h_inf);
 if (isnan(_xi)) {
  return _xi; }
 if (_xi <= 0.) {
 return _t_h_inf[0];
 }
 if (_xi >= 150.) {
 return _t_h_inf[150];
 }
 _i = (int) _xi;
 return _t_h_inf[_i] + (_xi - (double)_i)*(_t_h_inf[_i+1] - _t_h_inf[_i]);
 }

 
double _f_h_inf ( _threadargsprotocomma_ double _lko ) {
   double _lh_inf;
 double _lkh , _lh ;
 _lkh = ( ina_99 + ina_01 ) / 2.0 ;
   _lh = - ( ina_99 - _lkh ) / 4.59 ;
   _lh_inf = 1.0 / ( 1.0 + ( exp ( ( _lko - _lkh ) / _lh ) ) ) ;
   
return _lh_inf;
 }
 
static void _hoc_h_inf(void) {
  double _r;
   double* _p; Datum* _ppvar; Datum* _thread; _NrnThread* _nt;
   if (_extcall_prop) {_p = _extcall_prop->param; _ppvar = _extcall_prop->dparam;}else{ _p = (double*)0; _ppvar = (Datum*)0; }
  _thread = _extcall_thread;
  _nt = nrn_threads;
 
#if 1
 _check_h_inf(_p, _ppvar, _thread, _nt);
#endif
 _r =  h_inf ( _p, _ppvar, _thread, _nt, *getarg(1) );
 hoc_retpushx(_r);
}
 
double ghk ( _threadargsprotocomma_ double _lv , double _lci , double _lco ) {
   double _lghk;
 double _lz , _leci , _leco ;
 _lz = ( 1e-3 ) * 1.0 * FARADAY * _lv / ( R * ( celsius + 273.11247574 ) ) ;
   _leco = _lco * efun ( _threadargscomma_ _lz ) ;
   _leci = _lci * efun ( _threadargscomma_ - _lz ) ;
   _lghk = ( .001 ) * 1.0 * FARADAY * ( _leci - _leco ) ;
   
return _lghk;
 }
 
static void _hoc_ghk(void) {
  double _r;
   double* _p; Datum* _ppvar; Datum* _thread; _NrnThread* _nt;
   if (_extcall_prop) {_p = _extcall_prop->param; _ppvar = _extcall_prop->dparam;}else{ _p = (double*)0; _ppvar = (Datum*)0; }
  _thread = _extcall_thread;
  _nt = nrn_threads;
 _r =  ghk ( _p, _ppvar, _thread, _nt, *getarg(1) , *getarg(2) , *getarg(3) );
 hoc_retpushx(_r);
}
 
double efun ( _threadargsprotocomma_ double _lz ) {
   double _lefun;
 if ( fabs ( _lz ) < 1e-4 ) {
     _lefun = 1.0 - _lz / 2.0 ;
     }
   else {
     _lefun = _lz / ( exp ( _lz ) - 1.0 ) ;
     }
   
return _lefun;
 }
 
static void _hoc_efun(void) {
  double _r;
   double* _p; Datum* _ppvar; Datum* _thread; _NrnThread* _nt;
   if (_extcall_prop) {_p = _extcall_prop->param; _ppvar = _extcall_prop->dparam;}else{ _p = (double*)0; _ppvar = (Datum*)0; }
  _thread = _extcall_thread;
  _nt = nrn_threads;
 _r =  efun ( _p, _ppvar, _thread, _nt, *getarg(1) );
 hoc_retpushx(_r);
}
 
/*CVODE ode begin*/
 static int _ode_spec1(double* _p, Datum* _ppvar, Datum* _thread, _NrnThread* _nt) {int _reset=0;{
 double b_flux, f_flux, _term; int _i;
 {int _i; for(_i=0;_i<6;_i++) _p[_dlist1[_i]] = 0.0;}
 _za1 = m_a ( _threadargscomma_ ko ) ;
 _za2 = m_b ( _threadargscomma_ ko ) ;
 _zb1 = h_a ( _threadargscomma_ ko ) ;
 _zb2 = h_b ( _threadargscomma_ ko ) ;
 /* ~ mb <-> ma ( _za1 , _za2 )*/
 f_flux =  _za1 * mb ;
 b_flux =  _za2 * ma ;
 Dmb -= (f_flux - b_flux);
 Dma += (f_flux - b_flux);
 
 /*REACTION*/
  /* ~ hb <-> ha ( _zb1 , _zb2 )*/
 f_flux =  _zb1 * hb ;
 b_flux =  _zb2 * ha ;
 Dhb -= (f_flux - b_flux);
 Dha += (f_flux - b_flux);
 
 /*REACTION*/
  /* COMPARTMENT diam * diam * PI / 4.0 {
   qna qk }
 */
 /* ~ qna < < ( - ina * PI * diam * ( 1e4 ) / FARADAY )*/
 f_flux = b_flux = 0.;
 Dqna += (b_flux =   ( - ina * PI * diam * ( 1e4 ) / FARADAY ) );
 /*FLUX*/
  /* ~ qk < < ( - ik * PI * diam * ( 1e4 ) / FARADAY )*/
 f_flux = b_flux = 0.;
 Dqk += (b_flux =   ( - ik * PI * diam * ( 1e4 ) / FARADAY ) );
 /*FLUX*/
  _p[_dlist1[4]] /= ( diam * diam * PI / 4.0);
 _p[_dlist1[5]] /= ( diam * diam * PI / 4.0);
   } return _reset;
 }
 
/*CVODE matsol*/
 static int _ode_matsol1(void* _so, double* _rhs, double* _p, Datum* _ppvar, Datum* _thread, _NrnThread* _nt) {int _reset=0;{
 double b_flux, f_flux, _term; int _i;
   b_flux = f_flux = 0.;
 {int _i; double _dt1 = 1.0/dt;
for(_i=0;_i<6;_i++){
  	_RHS1(_i) = _dt1*(_p[_dlist1[_i]]);
	_MATELM1(_i, _i) = _dt1;
      
}  
_RHS1(4) *= ( diam * diam * PI / 4.0) ;
_MATELM1(4, 4) *= ( diam * diam * PI / 4.0); 
_RHS1(5) *= ( diam * diam * PI / 4.0) ;
_MATELM1(5, 5) *= ( diam * diam * PI / 4.0);  }
 _za1 = m_a ( _threadargscomma_ ko ) ;
 _za2 = m_b ( _threadargscomma_ ko ) ;
 _zb1 = h_a ( _threadargscomma_ ko ) ;
 _zb2 = h_b ( _threadargscomma_ ko ) ;
 /* ~ mb <-> ma ( _za1 , _za2 )*/
 _term =  _za1 ;
 _MATELM1( 2 ,2)  += _term;
 _MATELM1( 3 ,2)  -= _term;
 _term =  _za2 ;
 _MATELM1( 2 ,3)  -= _term;
 _MATELM1( 3 ,3)  += _term;
 /*REACTION*/
  /* ~ hb <-> ha ( _zb1 , _zb2 )*/
 _term =  _zb1 ;
 _MATELM1( 0 ,0)  += _term;
 _MATELM1( 1 ,0)  -= _term;
 _term =  _zb2 ;
 _MATELM1( 0 ,1)  -= _term;
 _MATELM1( 1 ,1)  += _term;
 /*REACTION*/
  /* COMPARTMENT diam * diam * PI / 4.0 {
 qna qk }
 */
 /* ~ qna < < ( - ina * PI * diam * ( 1e4 ) / FARADAY )*/
 /*FLUX*/
  /* ~ qk < < ( - ik * PI * diam * ( 1e4 ) / FARADAY )*/
 /*FLUX*/
    } return _reset;
 }
 
/*CVODE end*/
 
static int _ode_count(int _type){ return 6;}
 
static void _ode_spec(_NrnThread* _nt, _Memb_list* _ml, int _type) {
   double* _p; Datum* _ppvar; Datum* _thread;
   Node* _nd; double _v; int _iml, _cntml;
  _cntml = _ml->_nodecount;
  _thread = _ml->_thread;
  for (_iml = 0; _iml < _cntml; ++_iml) {
    _p = _ml->_data[_iml]; _ppvar = _ml->_pdata[_iml];
    _nd = _ml->_nodelist[_iml];
    v = NODEV(_nd);
  ko = _ion_ko;
  ki = _ion_ki;
  ek = _ion_ek;
  nai = _ion_nai;
  nao = _ion_nao;
  ena = _ion_ena;
  cai = _ion_cai;
  cao = _ion_cao;
  eca = _ion_eca;
     _ode_spec1 (_p, _ppvar, _thread, _nt);
    }}
 
static void _ode_map(int _ieq, double** _pv, double** _pvdot, double* _pp, Datum* _ppd, double* _atol, int _type) { 
	double* _p; Datum* _ppvar;
 	int _i; _p = _pp; _ppvar = _ppd;
	_cvode_ieq = _ieq;
	for (_i=0; _i < 6; ++_i) {
		_pv[_i] = _pp + _slist1[_i];  _pvdot[_i] = _pp + _dlist1[_i];
		_cvode_abstol(_atollist, _atol, _i);
	}
 }
 
static void _ode_matsol_instance1(_threadargsproto_) {
 _cvode_sparse_thread(&_thread[_cvspth1]._pvoid, 6, _dlist1, _p, _ode_matsol1, _ppvar, _thread, _nt);
 }
 
static void _ode_matsol(_NrnThread* _nt, _Memb_list* _ml, int _type) {
   double* _p; Datum* _ppvar; Datum* _thread;
   Node* _nd; double _v; int _iml, _cntml;
  _cntml = _ml->_nodecount;
  _thread = _ml->_thread;
  for (_iml = 0; _iml < _cntml; ++_iml) {
    _p = _ml->_data[_iml]; _ppvar = _ml->_pdata[_iml];
    _nd = _ml->_nodelist[_iml];
    v = NODEV(_nd);
  ko = _ion_ko;
  ki = _ion_ki;
  ek = _ion_ek;
  nai = _ion_nai;
  nao = _ion_nao;
  ena = _ion_ena;
  cai = _ion_cai;
  cao = _ion_cao;
  eca = _ion_eca;
 _ode_matsol_instance1(_threadargs_);
 }}
 
static void _thread_mem_init(Datum* _thread) {
   _thread[2]._pval = (double*)ecalloc(4, sizeof(double));
 }
 
static void _thread_cleanup(Datum* _thread) {
   _nrn_destroy_sparseobj_thread(_thread[_cvspth1]._pvoid);
   _nrn_destroy_sparseobj_thread(_thread[_spth1]._pvoid);
   free((void*)(_thread[2]._pval));
 }
 extern void nrn_update_ion_pointer(Symbol*, Datum*, int, int);
 static void _update_ion_pointer(Datum* _ppvar) {
   nrn_update_ion_pointer(_k_sym, _ppvar, 0, 2);
   nrn_update_ion_pointer(_k_sym, _ppvar, 1, 1);
   nrn_update_ion_pointer(_k_sym, _ppvar, 2, 0);
   nrn_update_ion_pointer(_k_sym, _ppvar, 3, 3);
   nrn_update_ion_pointer(_k_sym, _ppvar, 4, 4);
   nrn_update_ion_pointer(_na_sym, _ppvar, 5, 1);
   nrn_update_ion_pointer(_na_sym, _ppvar, 6, 2);
   nrn_update_ion_pointer(_na_sym, _ppvar, 7, 0);
   nrn_update_ion_pointer(_na_sym, _ppvar, 8, 3);
   nrn_update_ion_pointer(_na_sym, _ppvar, 9, 4);
   nrn_update_ion_pointer(_ca_sym, _ppvar, 10, 1);
   nrn_update_ion_pointer(_ca_sym, _ppvar, 11, 2);
   nrn_update_ion_pointer(_ca_sym, _ppvar, 12, 0);
   nrn_update_ion_pointer(_ca_sym, _ppvar, 13, 3);
   nrn_update_ion_pointer(_ca_sym, _ppvar, 14, 4);
 }

static void initmodel(double* _p, Datum* _ppvar, Datum* _thread, _NrnThread* _nt) {
  int _i; double _save;{
  hb = hb0;
  ha = ha0;
  mb = mb0;
  ma = ma0;
  qk = qk0;
  qna = qna0;
 {
   ma = m_inf ( _threadargscomma_ ko ) ;
   mb = 1.0 - ma ;
   ha = h_inf ( _threadargscomma_ ko ) ;
   hb = 1.0 - ha ;
   qna = 0.0 ;
   qk = 0.0 ;
   ina = gbar * ma * ha * ( v - ena ) / ( 1.0 + ( mg / 3.0 ) * exp ( - .07 * ( 70.0 + v - 60.0 ) ) ) ;
   ik = gbar * ma * ha * ( v - ek ) / ( 1.0 + ( mg / 3.0 ) * exp ( - .07 * ( 70.0 + v - 60.0 ) ) ) ;
   ica = gbar * scaleca * ma * ha * ( v - eca ) / ( 1.0 + ( mg / 3.0 ) * exp ( - .07 * ( 70.0 + v - 60.0 ) ) ) ;
   itot = ina + ik + ica ;
   }
 
}
}

static void nrn_init(_NrnThread* _nt, _Memb_list* _ml, int _type){
double* _p; Datum* _ppvar; Datum* _thread;
Node *_nd; double _v; int* _ni; int _iml, _cntml;
#if CACHEVEC
    _ni = _ml->_nodeindices;
#endif
_cntml = _ml->_nodecount;
_thread = _ml->_thread;
for (_iml = 0; _iml < _cntml; ++_iml) {
 _p = _ml->_data[_iml]; _ppvar = _ml->_pdata[_iml];

#if 0
 _check_m_a(_p, _ppvar, _thread, _nt);
 _check_m_b(_p, _ppvar, _thread, _nt);
 _check_m_inf(_p, _ppvar, _thread, _nt);
 _check_h_a(_p, _ppvar, _thread, _nt);
 _check_h_b(_p, _ppvar, _thread, _nt);
 _check_h_inf(_p, _ppvar, _thread, _nt);
#endif
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
  ko = _ion_ko;
  ki = _ion_ki;
  ek = _ion_ek;
  nai = _ion_nai;
  nao = _ion_nao;
  ena = _ion_ena;
  cai = _ion_cai;
  cao = _ion_cao;
  eca = _ion_eca;
 initmodel(_p, _ppvar, _thread, _nt);
   }
}

static double _nrn_current(double* _p, Datum* _ppvar, Datum* _thread, _NrnThread* _nt, double _v){double _current=0.;v=_v;{ {
   ina = gbar * ma * ha * ( v - ena ) / ( 1.0 + ( mg / 3.0 ) * exp ( - .07 * ( 70.0 + v - 60.0 ) ) ) ;
   ik = gbar * ma * ha * ( v - ek ) / ( 1.0 + ( mg / 3.0 ) * exp ( - .07 * ( 70.0 + v - 60.0 ) ) ) ;
   ica = gbar * scaleca * ma * ha * ( v - eca ) / ( 1.0 + ( mg / 3.0 ) * exp ( - .07 * ( 70.0 + v - 60.0 ) ) ) ;
   itot = ina + ik + ica ;
   }
 _current += ik;
 _current += ina;
 _current += ica;

} return _current;
}

static void nrn_cur(_NrnThread* _nt, _Memb_list* _ml, int _type) {
double* _p; Datum* _ppvar; Datum* _thread;
Node *_nd; int* _ni; double _rhs, _v; int _iml, _cntml;
#if CACHEVEC
    _ni = _ml->_nodeindices;
#endif
_cntml = _ml->_nodecount;
_thread = _ml->_thread;
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
  ko = _ion_ko;
  ki = _ion_ki;
  ek = _ion_ek;
  nai = _ion_nai;
  nao = _ion_nao;
  ena = _ion_ena;
  cai = _ion_cai;
  cao = _ion_cao;
  eca = _ion_eca;
 _g = _nrn_current(_p, _ppvar, _thread, _nt, _v + .001);
 	{ double _dica;
 double _dina;
 double _dik;
  _dik = ik;
  _dina = ina;
  _dica = ica;
 _rhs = _nrn_current(_p, _ppvar, _thread, _nt, _v);
  _ion_dikdv += (_dik - ik)/.001 ;
  _ion_dinadv += (_dina - ina)/.001 ;
  _ion_dicadv += (_dica - ica)/.001 ;
 	}
 _g = (_g - _rhs)/.001;
  _ion_ik += ik ;
  _ion_ina += ina ;
  _ion_ica += ica ;
#if CACHEVEC
  if (use_cachevec) {
	VEC_RHS(_ni[_iml]) -= _rhs;
  }else
#endif
  {
	NODERHS(_nd) -= _rhs;
  }
 
}
 
}

static void nrn_jacob(_NrnThread* _nt, _Memb_list* _ml, int _type) {
double* _p; Datum* _ppvar; Datum* _thread;
Node *_nd; int* _ni; int _iml, _cntml;
#if CACHEVEC
    _ni = _ml->_nodeindices;
#endif
_cntml = _ml->_nodecount;
_thread = _ml->_thread;
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
 
}
 
}

static void nrn_state(_NrnThread* _nt, _Memb_list* _ml, int _type) {
double* _p; Datum* _ppvar; Datum* _thread;
Node *_nd; double _v = 0.0; int* _ni; int _iml, _cntml;
double _dtsav = dt;
if (secondorder) { dt *= 0.5; }
#if CACHEVEC
    _ni = _ml->_nodeindices;
#endif
_cntml = _ml->_nodecount;
_thread = _ml->_thread;
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
  ko = _ion_ko;
  ki = _ion_ki;
  ek = _ion_ek;
  nai = _ion_nai;
  nao = _ion_nao;
  ena = _ion_ena;
  cai = _ion_cai;
  cao = _ion_cao;
  eca = _ion_eca;
 {  sparse_thread(&_thread[_spth1]._pvoid, 6, _slist1, _dlist1, _p, &t, dt, synstate, _linmat1, _ppvar, _thread, _nt);
     if (secondorder) {
    int _i;
    for (_i = 0; _i < 6; ++_i) {
      _p[_slist1[_i]] += dt*_p[_dlist1[_i]];
    }}
 }   }}
 dt = _dtsav;
}

static void terminal(){}

static void _initlists(){
 double _x; double* _p = &_x;
 int _i; static int _first = 1;
  if (!_first) return;
   _t_m_a = makevector(151*sizeof(double));
   _t_m_b = makevector(151*sizeof(double));
   _t_m_inf = makevector(151*sizeof(double));
   _t_h_a = makevector(151*sizeof(double));
   _t_h_b = makevector(151*sizeof(double));
   _t_h_inf = makevector(151*sizeof(double));
 _slist1[0] = &(hb) - _p;  _dlist1[0] = &(Dhb) - _p;
 _slist1[1] = &(ha) - _p;  _dlist1[1] = &(Dha) - _p;
 _slist1[2] = &(mb) - _p;  _dlist1[2] = &(Dmb) - _p;
 _slist1[3] = &(ma) - _p;  _dlist1[3] = &(Dma) - _p;
 _slist1[4] = &(qk) - _p;  _dlist1[4] = &(Dqk) - _p;
 _slist1[5] = &(qna) - _p;  _dlist1[5] = &(Dqna) - _p;
_first = 0;
}

#if defined(__cplusplus)
} /* extern "C" */
#endif
