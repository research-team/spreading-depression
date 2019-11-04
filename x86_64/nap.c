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
 
#define nrn_init _nrn_init__nap
#define _nrn_initial _nrn_initial__nap
#define nrn_cur _nrn_cur__nap
#define _nrn_current _nrn_current__nap
#define nrn_jacob _nrn_jacob__nap
#define nrn_state _nrn_state__nap
#define _net_receive _net_receive__nap 
#define nastate nastate__nap 
 
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
#define gnabar _p[0]
#define ina _p[1]
#define ma _p[2]
#define mb _p[3]
#define ha _p[4]
#define hb _p[5]
#define ena _p[6]
#define nai _p[7]
#define nao _p[8]
#define ko _p[9]
#define Dma _p[10]
#define Dmb _p[11]
#define Dha _p[12]
#define Dhb _p[13]
#define v _p[14]
#define _g _p[15]
#define _ion_ko	*_ppvar[0]._pval
#define _ion_nai	*_ppvar[1]._pval
#define _ion_nao	*_ppvar[2]._pval
#define _ion_ena	*_ppvar[3]._pval
#define _ion_ina	*_ppvar[4]._pval
#define _ion_dinadv	*_ppvar[5]._pval
 
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
 static void _hoc_kdep(void);
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
 "setdata_nap", _hoc_setdata,
 "efun_nap", _hoc_efun,
 "ghk_nap", _hoc_ghk,
 "h_b_nap", _hoc_h_b,
 "h_a_nap", _hoc_h_a,
 "h_inf_nap", _hoc_h_inf,
 "kdep_nap", _hoc_kdep,
 "m_b_nap", _hoc_m_b,
 "m_a_nap", _hoc_m_a,
 "m_inf_nap", _hoc_m_inf,
 0, 0
};
#define _f_h_inf _f_h_inf_nap
#define _f_h_b _f_h_b_nap
#define _f_h_a _f_h_a_nap
#define _f_m_b _f_m_b_nap
#define _f_m_inf _f_m_inf_nap
#define _f_m_a _f_m_a_nap
#define _f_kdep _f_kdep_nap
#define efun efun_nap
#define ghk ghk_nap
#define h_b h_b_nap
#define h_a h_a_nap
#define h_inf h_inf_nap
#define kdep kdep_nap
#define m_b m_b_nap
#define m_a m_a_nap
#define m_inf m_inf_nap
 extern double _f_h_inf( _threadargsprotocomma_ double );
 extern double _f_h_b( _threadargsprotocomma_ double );
 extern double _f_h_a( _threadargsprotocomma_ double );
 extern double _f_m_b( _threadargsprotocomma_ double );
 extern double _f_m_inf( _threadargsprotocomma_ double );
 extern double _f_m_a( _threadargsprotocomma_ double );
 extern double _f_kdep( _threadargsprotocomma_ double );
 extern double efun( _threadargsprotocomma_ double );
 extern double ghk( _threadargsprotocomma_ double , double , double );
 extern double h_b( _threadargsprotocomma_ double );
 extern double h_a( _threadargsprotocomma_ double );
 extern double h_inf( _threadargsprotocomma_ double );
 extern double kdep( _threadargsprotocomma_ double );
 extern double m_b( _threadargsprotocomma_ double );
 extern double m_a( _threadargsprotocomma_ double );
 extern double m_inf( _threadargsprotocomma_ double );
 
static void _check_kdep(double*, Datum*, Datum*, _NrnThread*); 
static void _check_m_a(double*, Datum*, Datum*, _NrnThread*); 
static void _check_m_inf(double*, Datum*, Datum*, _NrnThread*); 
static void _check_m_b(double*, Datum*, Datum*, _NrnThread*); 
static void _check_h_a(double*, Datum*, Datum*, _NrnThread*); 
static void _check_h_b(double*, Datum*, Datum*, _NrnThread*); 
static void _check_h_inf(double*, Datum*, Datum*, _NrnThread*); 
static void _check_table_thread(double* _p, Datum* _ppvar, Datum* _thread, _NrnThread* _nt, int _type) {
   _check_kdep(_p, _ppvar, _thread, _nt);
   _check_m_a(_p, _ppvar, _thread, _nt);
   _check_m_inf(_p, _ppvar, _thread, _nt);
   _check_m_b(_p, _ppvar, _thread, _nt);
   _check_h_a(_p, _ppvar, _thread, _nt);
   _check_h_b(_p, _ppvar, _thread, _nt);
   _check_h_inf(_p, _ppvar, _thread, _nt);
 }
 #define _za1 _thread[2]._pval[0]
 #define _za2 _thread[2]._pval[1]
 #define _zb1 _thread[2]._pval[2]
 #define _zb2 _thread[2]._pval[3]
 /* declare global and static user variables */
#define conc_half conc_half_nap
 double conc_half = 7;
#define helling helling_nap
 double helling = -0.765;
#define ina_p_h ina_p_h_nap
 double ina_p_h = 25000;
#define tau_act tau_act_nap
 double tau_act = 6;
#define usetable usetable_nap
 double usetable = 1;
 /* some parameters have upper and lower limits */
 static HocParmLimits _hoc_parm_limits[] = {
 "usetable_nap", 0, 1,
 0,0,0
};
 static HocParmUnits _hoc_parm_units[] = {
 "helling_nap", "mM",
 "conc_half_nap", "mM",
 "ina_p_h_nap", "ms",
 "tau_act_nap", "ms",
 "gnabar_nap", "mho/cm2",
 "ina_nap", "mA/cm2",
 0,0
};
 static double delta_t = 0.01;
 static double hb0 = 0;
 static double ha0 = 0;
 static double mb0 = 0;
 static double ma0 = 0;
 /* connect global user variables to hoc */
 static DoubScal hoc_scdoub[] = {
 "helling_nap", &helling_nap,
 "conc_half_nap", &conc_half_nap,
 "ina_p_h_nap", &ina_p_h_nap,
 "tau_act_nap", &tau_act_nap,
 "usetable_nap", &usetable_nap,
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
 
#define _cvode_ieq _ppvar[6]._i
 static void _ode_matsol_instance1(_threadargsproto_);
 /* connect range variables in _p that hoc is supposed to know about */
 static const char *_mechanism[] = {
 "7.5.0",
"nap",
 "gnabar_nap",
 0,
 "ina_nap",
 0,
 "ma_nap",
 "mb_nap",
 "ha_nap",
 "hb_nap",
 0,
 0};
 static Symbol* _k_sym;
 static Symbol* _na_sym;
 
extern Prop* need_memb(Symbol*);

static void nrn_alloc(Prop* _prop) {
	Prop *prop_ion;
	double *_p; Datum *_ppvar;
 	_p = nrn_prop_data_alloc(_mechtype, 16, _prop);
 	/*initialize range parameters*/
 	gnabar = 1e-06;
 	_prop->param = _p;
 	_prop->param_size = 16;
 	_ppvar = nrn_prop_datum_alloc(_mechtype, 7, _prop);
 	_prop->dparam = _ppvar;
 	/*connect ionic variables to this model*/
 prop_ion = need_memb(_k_sym);
 nrn_promote(prop_ion, 1, 0);
 	_ppvar[0]._pval = &prop_ion->param[2]; /* ko */
 prop_ion = need_memb(_na_sym);
 nrn_promote(prop_ion, 1, 1);
 	_ppvar[1]._pval = &prop_ion->param[1]; /* nai */
 	_ppvar[2]._pval = &prop_ion->param[2]; /* nao */
 	_ppvar[3]._pval = &prop_ion->param[0]; /* ena */
 	_ppvar[4]._pval = &prop_ion->param[3]; /* ina */
 	_ppvar[5]._pval = &prop_ion->param[4]; /* _ion_dinadv */
 
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

 void _nap_reg() {
	int _vectorized = 1;
  _initlists();
 	ion_reg("k", -10000.);
 	ion_reg("na", -10000.);
 	_k_sym = hoc_lookup("k_ion");
 	_na_sym = hoc_lookup("na_ion");
 	register_mech(_mechanism, nrn_alloc,nrn_cur, nrn_jacob, nrn_state, nrn_init, hoc_nrnpointerindex, 4);
  _extcall_thread = (Datum*)ecalloc(3, sizeof(Datum));
  _thread_mem_init(_extcall_thread);
 _mechtype = nrn_get_mechtype(_mechanism[1]);
     _nrn_setdata_reg(_mechtype, _setdata);
     _nrn_thread_reg(_mechtype, 1, _thread_mem_init);
     _nrn_thread_reg(_mechtype, 0, _thread_cleanup);
     _nrn_thread_reg(_mechtype, 2, _update_ion_pointer);
     _nrn_thread_table_reg(_mechtype, _check_table_thread);
  hoc_register_prop_size(_mechtype, 16, 7);
  hoc_register_dparam_semantics(_mechtype, 0, "k_ion");
  hoc_register_dparam_semantics(_mechtype, 1, "na_ion");
  hoc_register_dparam_semantics(_mechtype, 2, "na_ion");
  hoc_register_dparam_semantics(_mechtype, 3, "na_ion");
  hoc_register_dparam_semantics(_mechtype, 4, "na_ion");
  hoc_register_dparam_semantics(_mechtype, 5, "na_ion");
  hoc_register_dparam_semantics(_mechtype, 6, "cvodeieq");
 	hoc_register_cvode(_mechtype, _ode_count, _ode_map, _ode_spec, _ode_matsol);
 	hoc_register_tolerance(_mechtype, _hoc_state_tol, &_atollist);
 	hoc_register_var(hoc_scdoub, hoc_vdoub, hoc_intfunc);
 	ivoc_help("help ?1 nap /Users/sulgod/spreading-depression/x86_64/nap.mod\n");
 hoc_register_limits(_mechtype, _hoc_parm_limits);
 hoc_register_units(_mechtype, _hoc_parm_units);
 }
 static double FARADAY = 96485.309;
 static double R = 8.3145;
 /*Top LOCAL _za1 , _za2 , _zb1 , _zb2 */
 static double *_t_kdep;
 static double *_t_m_a;
 static double *_t_m_inf;
 static double *_t_m_b;
 static double *_t_h_a;
 static double *_t_h_b;
 static double *_t_h_inf;
static int _reset;
static char *modelname = "nap";

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
 static double _n_m_b(_threadargsprotocomma_ double _lv);
 static double _n_m_inf(_threadargsprotocomma_ double _lv);
 static double _n_m_a(_threadargsprotocomma_ double _lv);
 static double _n_kdep(_threadargsprotocomma_ double _lv);
 static int _slist1[4], _dlist1[4]; static double *_temp1;
 static int nastate();
 
static int nastate (void* _so, double* _rhs, double* _p, Datum* _ppvar, Datum* _thread, _NrnThread* _nt)
 {int _reset=0;
 {
   double b_flux, f_flux, _term; int _i;
 {int _i; double _dt1 = 1.0/dt;
for(_i=2;_i<4;_i++){
  	_RHS1(_i) = -_dt1*(_p[_slist1[_i]] - _p[_dlist1[_i]]);
	_MATELM1(_i, _i) = _dt1;
      
} }
 _za1 = m_a ( _threadargscomma_ v ) ;
   _za2 = m_b ( _threadargscomma_ v ) ;
   _zb1 = h_a ( _threadargscomma_ v ) ;
   _zb2 = h_b ( _threadargscomma_ v ) ;
   /* ~ mb <-> ma ( _za1 , _za2 )*/
 f_flux =  _za1 * mb ;
 b_flux =  _za2 * ma ;
 _RHS1( 3) += (f_flux - b_flux);
 
 _term =  _za1 ;
 _MATELM1( 3 ,1)  -= _term;
 _term =  _za2 ;
 _MATELM1( 3 ,3)  += _term;
 /*REACTION*/
  /* ~ hb <-> ha ( _zb1 , _zb2 )*/
 f_flux =  _zb1 * hb ;
 b_flux =  _zb2 * ha ;
 _RHS1( 2) += (f_flux - b_flux);
 
 _term =  _zb1 ;
 _MATELM1( 2 ,0)  -= _term;
 _term =  _zb2 ;
 _MATELM1( 2 ,2)  += _term;
 /*REACTION*/
   /* ma + mb = 1.0 */
 _RHS1(1) =  1.0;
 _MATELM1(1, 1) = 1;
 _RHS1(1) -= mb ;
 _MATELM1(1, 3) = 1;
 _RHS1(1) -= ma ;
 /*CONSERVATION*/
  /* ha + hb = 1.0 */
 _RHS1(0) =  1.0;
 _MATELM1(0, 0) = 1;
 _RHS1(0) -= hb ;
 _MATELM1(0, 2) = 1;
 _RHS1(0) -= ha ;
 /*CONSERVATION*/
   } return _reset;
 }
 static double _mfac_kdep, _tmin_kdep;
  static void _check_kdep(double* _p, Datum* _ppvar, Datum* _thread, _NrnThread* _nt) {
  static int _maktable=1; int _i, _j, _ix = 0;
  double _xi, _tmax;
  static double _sav_conc_half;
  static double _sav_helling;
  if (!usetable) {return;}
  if (_sav_conc_half != conc_half) { _maktable = 1;}
  if (_sav_helling != helling) { _maktable = 1;}
  if (_maktable) { double _x, _dx; _maktable=0;
   _tmin_kdep =  0.0 ;
   _tmax =  150.0 ;
   _dx = (_tmax - _tmin_kdep)/150.; _mfac_kdep = 1./_dx;
   for (_i=0, _x=_tmin_kdep; _i < 151; _x += _dx, _i++) {
    _t_kdep[_i] = _f_kdep(_p, _ppvar, _thread, _nt, _x);
   }
   _sav_conc_half = conc_half;
   _sav_helling = helling;
  }
 }

 double kdep(double* _p, Datum* _ppvar, Datum* _thread, _NrnThread* _nt, double _lko) { 
#if 0
_check_kdep(_p, _ppvar, _thread, _nt);
#endif
 return _n_kdep(_p, _ppvar, _thread, _nt, _lko);
 }

 static double _n_kdep(double* _p, Datum* _ppvar, Datum* _thread, _NrnThread* _nt, double _lko){ int _i, _j;
 double _xi, _theta;
 if (!usetable) {
 return _f_kdep(_p, _ppvar, _thread, _nt, _lko); 
}
 _xi = _mfac_kdep * (_lko - _tmin_kdep);
 if (isnan(_xi)) {
  return _xi; }
 if (_xi <= 0.) {
 return _t_kdep[0];
 }
 if (_xi >= 150.) {
 return _t_kdep[150];
 }
 _i = (int) _xi;
 return _t_kdep[_i] + (_xi - (double)_i)*(_t_kdep[_i+1] - _t_kdep[_i]);
 }

 
double _f_kdep ( _threadargsprotocomma_ double _lko ) {
   double _lkdep;
 _lkdep = 1.0 + 2.0 / ( 1.0 + exp ( ( _lko - conc_half ) / helling ) ) ;
   
return _lkdep;
 }
 
static void _hoc_kdep(void) {
  double _r;
   double* _p; Datum* _ppvar; Datum* _thread; _NrnThread* _nt;
   if (_extcall_prop) {_p = _extcall_prop->param; _ppvar = _extcall_prop->dparam;}else{ _p = (double*)0; _ppvar = (Datum*)0; }
  _thread = _extcall_thread;
  _nt = nrn_threads;
 
#if 1
 _check_kdep(_p, _ppvar, _thread, _nt);
#endif
 _r =  kdep ( _p, _ppvar, _thread, _nt, *getarg(1) );
 hoc_retpushx(_r);
}
 static double _mfac_m_a, _tmin_m_a;
  static void _check_m_a(double* _p, Datum* _ppvar, Datum* _thread, _NrnThread* _nt) {
  static int _maktable=1; int _i, _j, _ix = 0;
  double _xi, _tmax;
  if (!usetable) {return;}
  if (_maktable) { double _x, _dx; _maktable=0;
   _tmin_m_a =  - 150.0 ;
   _tmax =  150.0 ;
   _dx = (_tmax - _tmin_m_a)/200.; _mfac_m_a = 1./_dx;
   for (_i=0, _x=_tmin_m_a; _i < 201; _x += _dx, _i++) {
    _t_m_a[_i] = _f_m_a(_p, _ppvar, _thread, _nt, _x);
   }
  }
 }

 double m_a(double* _p, Datum* _ppvar, Datum* _thread, _NrnThread* _nt, double _lv) { 
#if 0
_check_m_a(_p, _ppvar, _thread, _nt);
#endif
 return _n_m_a(_p, _ppvar, _thread, _nt, _lv);
 }

 static double _n_m_a(double* _p, Datum* _ppvar, Datum* _thread, _NrnThread* _nt, double _lv){ int _i, _j;
 double _xi, _theta;
 if (!usetable) {
 return _f_m_a(_p, _ppvar, _thread, _nt, _lv); 
}
 _xi = _mfac_m_a * (_lv - _tmin_m_a);
 if (isnan(_xi)) {
  return _xi; }
 if (_xi <= 0.) {
 return _t_m_a[0];
 }
 if (_xi >= 200.) {
 return _t_m_a[200];
 }
 _i = (int) _xi;
 return _t_m_a[_i] + (_xi - (double)_i)*(_t_m_a[_i+1] - _t_m_a[_i]);
 }

 
double _f_m_a ( _threadargsprotocomma_ double _lv ) {
   double _lm_a;
 _lm_a = m_inf ( _threadargscomma_ _lv ) / tau_act ;
   
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
 static double _mfac_m_inf, _tmin_m_inf;
  static void _check_m_inf(double* _p, Datum* _ppvar, Datum* _thread, _NrnThread* _nt) {
  static int _maktable=1; int _i, _j, _ix = 0;
  double _xi, _tmax;
  if (!usetable) {return;}
  if (_maktable) { double _x, _dx; _maktable=0;
   _tmin_m_inf =  - 150.0 ;
   _tmax =  150.0 ;
   _dx = (_tmax - _tmin_m_inf)/200.; _mfac_m_inf = 1./_dx;
   for (_i=0, _x=_tmin_m_inf; _i < 201; _x += _dx, _i++) {
    _t_m_inf[_i] = _f_m_inf(_p, _ppvar, _thread, _nt, _x);
   }
  }
 }

 double m_inf(double* _p, Datum* _ppvar, Datum* _thread, _NrnThread* _nt, double _lv) { 
#if 0
_check_m_inf(_p, _ppvar, _thread, _nt);
#endif
 return _n_m_inf(_p, _ppvar, _thread, _nt, _lv);
 }

 static double _n_m_inf(double* _p, Datum* _ppvar, Datum* _thread, _NrnThread* _nt, double _lv){ int _i, _j;
 double _xi, _theta;
 if (!usetable) {
 return _f_m_inf(_p, _ppvar, _thread, _nt, _lv); 
}
 _xi = _mfac_m_inf * (_lv - _tmin_m_inf);
 if (isnan(_xi)) {
  return _xi; }
 if (_xi <= 0.) {
 return _t_m_inf[0];
 }
 if (_xi >= 200.) {
 return _t_m_inf[200];
 }
 _i = (int) _xi;
 return _t_m_inf[_i] + (_xi - (double)_i)*(_t_m_inf[_i+1] - _t_m_inf[_i]);
 }

 
double _f_m_inf ( _threadargsprotocomma_ double _lv ) {
   double _lm_inf;
 _lm_inf = 1.0 / ( 1.0 + ( exp ( - ( _lv + 39.7 ) / 7.0 ) ) ) ;
   
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
 static double _mfac_m_b, _tmin_m_b;
  static void _check_m_b(double* _p, Datum* _ppvar, Datum* _thread, _NrnThread* _nt) {
  static int _maktable=1; int _i, _j, _ix = 0;
  double _xi, _tmax;
  if (!usetable) {return;}
  if (_maktable) { double _x, _dx; _maktable=0;
   _tmin_m_b =  - 150.0 ;
   _tmax =  150.0 ;
   _dx = (_tmax - _tmin_m_b)/200.; _mfac_m_b = 1./_dx;
   for (_i=0, _x=_tmin_m_b; _i < 201; _x += _dx, _i++) {
    _t_m_b[_i] = _f_m_b(_p, _ppvar, _thread, _nt, _x);
   }
  }
 }

 double m_b(double* _p, Datum* _ppvar, Datum* _thread, _NrnThread* _nt, double _lv) { 
#if 0
_check_m_b(_p, _ppvar, _thread, _nt);
#endif
 return _n_m_b(_p, _ppvar, _thread, _nt, _lv);
 }

 static double _n_m_b(double* _p, Datum* _ppvar, Datum* _thread, _NrnThread* _nt, double _lv){ int _i, _j;
 double _xi, _theta;
 if (!usetable) {
 return _f_m_b(_p, _ppvar, _thread, _nt, _lv); 
}
 _xi = _mfac_m_b * (_lv - _tmin_m_b);
 if (isnan(_xi)) {
  return _xi; }
 if (_xi <= 0.) {
 return _t_m_b[0];
 }
 if (_xi >= 200.) {
 return _t_m_b[200];
 }
 _i = (int) _xi;
 return _t_m_b[_i] + (_xi - (double)_i)*(_t_m_b[_i+1] - _t_m_b[_i]);
 }

 
double _f_m_b ( _threadargsprotocomma_ double _lv ) {
   double _lm_b;
 _lm_b = ( 1.0 - m_inf ( _threadargscomma_ _lv ) ) / tau_act ;
   
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
 static double _mfac_h_a, _tmin_h_a;
  static void _check_h_a(double* _p, Datum* _ppvar, Datum* _thread, _NrnThread* _nt) {
  static int _maktable=1; int _i, _j, _ix = 0;
  double _xi, _tmax;
  if (!usetable) {return;}
  if (_maktable) { double _x, _dx; _maktable=0;
   _tmin_h_a =  - 150.0 ;
   _tmax =  150.0 ;
   _dx = (_tmax - _tmin_h_a)/200.; _mfac_h_a = 1./_dx;
   for (_i=0, _x=_tmin_h_a; _i < 201; _x += _dx, _i++) {
    _t_h_a[_i] = _f_h_a(_p, _ppvar, _thread, _nt, _x);
   }
  }
 }

 double h_a(double* _p, Datum* _ppvar, Datum* _thread, _NrnThread* _nt, double _lv) { 
#if 0
_check_h_a(_p, _ppvar, _thread, _nt);
#endif
 return _n_h_a(_p, _ppvar, _thread, _nt, _lv);
 }

 static double _n_h_a(double* _p, Datum* _ppvar, Datum* _thread, _NrnThread* _nt, double _lv){ int _i, _j;
 double _xi, _theta;
 if (!usetable) {
 return _f_h_a(_p, _ppvar, _thread, _nt, _lv); 
}
 _xi = _mfac_h_a * (_lv - _tmin_h_a);
 if (isnan(_xi)) {
  return _xi; }
 if (_xi <= 0.) {
 return _t_h_a[0];
 }
 if (_xi >= 200.) {
 return _t_h_a[200];
 }
 _i = (int) _xi;
 return _t_h_a[_i] + (_xi - (double)_i)*(_t_h_a[_i+1] - _t_h_a[_i]);
 }

 
double _f_h_a ( _threadargsprotocomma_ double _lv ) {
   double _lh_a;
 _lh_a = ( 1.0 / ina_p_h ) * ( 0.128 * exp ( ( 7.0 - _lv - 70.0 ) / 18.0 ) ) ;
   
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
  if (!usetable) {return;}
  if (_maktable) { double _x, _dx; _maktable=0;
   _tmin_h_b =  - 150.0 ;
   _tmax =  150.0 ;
   _dx = (_tmax - _tmin_h_b)/200.; _mfac_h_b = 1./_dx;
   for (_i=0, _x=_tmin_h_b; _i < 201; _x += _dx, _i++) {
    _t_h_b[_i] = _f_h_b(_p, _ppvar, _thread, _nt, _x);
   }
  }
 }

 double h_b(double* _p, Datum* _ppvar, Datum* _thread, _NrnThread* _nt, double _lv) { 
#if 0
_check_h_b(_p, _ppvar, _thread, _nt);
#endif
 return _n_h_b(_p, _ppvar, _thread, _nt, _lv);
 }

 static double _n_h_b(double* _p, Datum* _ppvar, Datum* _thread, _NrnThread* _nt, double _lv){ int _i, _j;
 double _xi, _theta;
 if (!usetable) {
 return _f_h_b(_p, _ppvar, _thread, _nt, _lv); 
}
 _xi = _mfac_h_b * (_lv - _tmin_h_b);
 if (isnan(_xi)) {
  return _xi; }
 if (_xi <= 0.) {
 return _t_h_b[0];
 }
 if (_xi >= 200.) {
 return _t_h_b[200];
 }
 _i = (int) _xi;
 return _t_h_b[_i] + (_xi - (double)_i)*(_t_h_b[_i+1] - _t_h_b[_i]);
 }

 
double _f_h_b ( _threadargsprotocomma_ double _lv ) {
   double _lh_b;
 _lh_b = ( 1.0 / ina_p_h ) * 4.0 / ( 1.0 + exp ( ( 30.0 - _lv - 70.0 ) / 5.0 ) ) ;
   
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
  if (!usetable) {return;}
  if (_maktable) { double _x, _dx; _maktable=0;
   _tmin_h_inf =  - 150.0 ;
   _tmax =  150.0 ;
   _dx = (_tmax - _tmin_h_inf)/200.; _mfac_h_inf = 1./_dx;
   for (_i=0, _x=_tmin_h_inf; _i < 201; _x += _dx, _i++) {
    _t_h_inf[_i] = _f_h_inf(_p, _ppvar, _thread, _nt, _x);
   }
  }
 }

 double h_inf(double* _p, Datum* _ppvar, Datum* _thread, _NrnThread* _nt, double _lv) { 
#if 0
_check_h_inf(_p, _ppvar, _thread, _nt);
#endif
 return _n_h_inf(_p, _ppvar, _thread, _nt, _lv);
 }

 static double _n_h_inf(double* _p, Datum* _ppvar, Datum* _thread, _NrnThread* _nt, double _lv){ int _i, _j;
 double _xi, _theta;
 if (!usetable) {
 return _f_h_inf(_p, _ppvar, _thread, _nt, _lv); 
}
 _xi = _mfac_h_inf * (_lv - _tmin_h_inf);
 if (isnan(_xi)) {
  return _xi; }
 if (_xi <= 0.) {
 return _t_h_inf[0];
 }
 if (_xi >= 200.) {
 return _t_h_inf[200];
 }
 _i = (int) _xi;
 return _t_h_inf[_i] + (_xi - (double)_i)*(_t_h_inf[_i+1] - _t_h_inf[_i]);
 }

 
double _f_h_inf ( _threadargsprotocomma_ double _lv ) {
   double _lh_inf;
 _lh_inf = h_a ( _threadargscomma_ _lv ) / ( h_a ( _threadargscomma_ _lv ) + h_b ( _threadargscomma_ _lv ) ) ;
   
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
 {int _i; for(_i=0;_i<4;_i++) _p[_dlist1[_i]] = 0.0;}
 _za1 = m_a ( _threadargscomma_ v ) ;
 _za2 = m_b ( _threadargscomma_ v ) ;
 _zb1 = h_a ( _threadargscomma_ v ) ;
 _zb2 = h_b ( _threadargscomma_ v ) ;
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
   /* ma + mb = 1.0 */
 /*CONSERVATION*/
  /* ha + hb = 1.0 */
 /*CONSERVATION*/
   } return _reset;
 }
 
/*CVODE matsol*/
 static int _ode_matsol1(void* _so, double* _rhs, double* _p, Datum* _ppvar, Datum* _thread, _NrnThread* _nt) {int _reset=0;{
 double b_flux, f_flux, _term; int _i;
   b_flux = f_flux = 0.;
 {int _i; double _dt1 = 1.0/dt;
for(_i=0;_i<4;_i++){
  	_RHS1(_i) = _dt1*(_p[_dlist1[_i]]);
	_MATELM1(_i, _i) = _dt1;
      
} }
 _za1 = m_a ( _threadargscomma_ v ) ;
 _za2 = m_b ( _threadargscomma_ v ) ;
 _zb1 = h_a ( _threadargscomma_ v ) ;
 _zb2 = h_b ( _threadargscomma_ v ) ;
 /* ~ mb <-> ma ( _za1 , _za2 )*/
 _term =  _za1 ;
 _MATELM1( 1 ,1)  += _term;
 _MATELM1( 3 ,1)  -= _term;
 _term =  _za2 ;
 _MATELM1( 1 ,3)  -= _term;
 _MATELM1( 3 ,3)  += _term;
 /*REACTION*/
  /* ~ hb <-> ha ( _zb1 , _zb2 )*/
 _term =  _zb1 ;
 _MATELM1( 0 ,0)  += _term;
 _MATELM1( 2 ,0)  -= _term;
 _term =  _zb2 ;
 _MATELM1( 0 ,2)  -= _term;
 _MATELM1( 2 ,2)  += _term;
 /*REACTION*/
   /* ma + mb = 1.0 */
 /*CONSERVATION*/
  /* ha + hb = 1.0 */
 /*CONSERVATION*/
   } return _reset;
 }
 
/*CVODE end*/
 
static int _ode_count(int _type){ return 4;}
 
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
  nai = _ion_nai;
  nao = _ion_nao;
  ena = _ion_ena;
     _ode_spec1 (_p, _ppvar, _thread, _nt);
  }}
 
static void _ode_map(int _ieq, double** _pv, double** _pvdot, double* _pp, Datum* _ppd, double* _atol, int _type) { 
	double* _p; Datum* _ppvar;
 	int _i; _p = _pp; _ppvar = _ppd;
	_cvode_ieq = _ieq;
	for (_i=0; _i < 4; ++_i) {
		_pv[_i] = _pp + _slist1[_i];  _pvdot[_i] = _pp + _dlist1[_i];
		_cvode_abstol(_atollist, _atol, _i);
	}
 }
 
static void _ode_matsol_instance1(_threadargsproto_) {
 _cvode_sparse_thread(&_thread[_cvspth1]._pvoid, 4, _dlist1, _p, _ode_matsol1, _ppvar, _thread, _nt);
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
  nai = _ion_nai;
  nao = _ion_nao;
  ena = _ion_ena;
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
   nrn_update_ion_pointer(_na_sym, _ppvar, 1, 1);
   nrn_update_ion_pointer(_na_sym, _ppvar, 2, 2);
   nrn_update_ion_pointer(_na_sym, _ppvar, 3, 0);
   nrn_update_ion_pointer(_na_sym, _ppvar, 4, 3);
   nrn_update_ion_pointer(_na_sym, _ppvar, 5, 4);
 }

static void initmodel(double* _p, Datum* _ppvar, Datum* _thread, _NrnThread* _nt) {
  int _i; double _save;{
  hb = hb0;
  ha = ha0;
  mb = mb0;
  ma = ma0;
 {
   ma = m_inf ( _threadargscomma_ v ) ;
   mb = 1.0 - ma ;
   ha = h_inf ( _threadargscomma_ v ) ;
   hb = 1.0 - ha ;
   ina = gnabar * ma * ma * ha * kdep ( _threadargscomma_ ko ) * ( v - ena ) ;
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
 _check_kdep(_p, _ppvar, _thread, _nt);
 _check_m_a(_p, _ppvar, _thread, _nt);
 _check_m_inf(_p, _ppvar, _thread, _nt);
 _check_m_b(_p, _ppvar, _thread, _nt);
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
  nai = _ion_nai;
  nao = _ion_nao;
  ena = _ion_ena;
 initmodel(_p, _ppvar, _thread, _nt);
 }
}

static double _nrn_current(double* _p, Datum* _ppvar, Datum* _thread, _NrnThread* _nt, double _v){double _current=0.;v=_v;{ {
   ina = gnabar * ma * ma * ha * kdep ( _threadargscomma_ ko ) * ( v - ena ) ;
   }
 _current += ina;

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
  nai = _ion_nai;
  nao = _ion_nao;
  ena = _ion_ena;
 _g = _nrn_current(_p, _ppvar, _thread, _nt, _v + .001);
 	{ double _dina;
  _dina = ina;
 _rhs = _nrn_current(_p, _ppvar, _thread, _nt, _v);
  _ion_dinadv += (_dina - ina)/.001 ;
 	}
 _g = (_g - _rhs)/.001;
  _ion_ina += ina ;
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
  nai = _ion_nai;
  nao = _ion_nao;
  ena = _ion_ena;
 {  sparse_thread(&_thread[_spth1]._pvoid, 4, _slist1, _dlist1, _p, &t, dt, nastate, _linmat1, _ppvar, _thread, _nt);
     if (secondorder) {
    int _i;
    for (_i = 0; _i < 4; ++_i) {
      _p[_slist1[_i]] += dt*_p[_dlist1[_i]];
    }}
 } }}
 dt = _dtsav;
}

static void terminal(){}

static void _initlists(){
 double _x; double* _p = &_x;
 int _i; static int _first = 1;
  if (!_first) return;
   _t_kdep = makevector(151*sizeof(double));
   _t_m_a = makevector(201*sizeof(double));
   _t_m_inf = makevector(201*sizeof(double));
   _t_m_b = makevector(201*sizeof(double));
   _t_h_a = makevector(201*sizeof(double));
   _t_h_b = makevector(201*sizeof(double));
   _t_h_inf = makevector(201*sizeof(double));
 _slist1[0] = &(hb) - _p;  _dlist1[0] = &(Dhb) - _p;
 _slist1[1] = &(mb) - _p;  _dlist1[1] = &(Dmb) - _p;
 _slist1[2] = &(ha) - _p;  _dlist1[2] = &(Dha) - _p;
 _slist1[3] = &(ma) - _p;  _dlist1[3] = &(Dma) - _p;
_first = 0;
}

#if defined(__cplusplus)
} /* extern "C" */
#endif
