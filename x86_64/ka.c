/* Created by Language version: 7.7.0 */
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
 
#define nrn_init _nrn_init__ka
#define _nrn_initial _nrn_initial__ka
#define nrn_cur _nrn_cur__ka
#define _nrn_current _nrn_current__ka
#define nrn_jacob _nrn_jacob__ka
#define nrn_state _nrn_state__ka
#define _net_receive _net_receive__ka 
#define kstate kstate__ka 
 
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
#define gkbar _p[0]
#define ik _p[1]
#define am _p[2]
#define ac _p[3]
#define bm _p[4]
#define bc _p[5]
#define qk _p[6]
#define ek _p[7]
#define Dam _p[8]
#define Dac _p[9]
#define Dbm _p[10]
#define Dbc _p[11]
#define Dqk _p[12]
#define v _p[13]
#define _g _p[14]
#define _ion_ek	*_ppvar[0]._pval
#define _ion_ik	*_ppvar[1]._pval
#define _ion_dikdv	*_ppvar[2]._pval
#define diam	*_ppvar[3]._pval
 
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
 static void _hoc_a_c(void);
 static void _hoc_a_m(void);
 static void _hoc_a_inf(void);
 static void _hoc_b_c(void);
 static void _hoc_b_m(void);
 static void _hoc_b_inf(void);
 static void _hoc_efun(void);
 static void _hoc_ghk(void);
 static void _hoc_window(void);
 static int _mechtype;
extern void _nrn_cacheloop_reg(int, int);
extern void hoc_register_prop_size(int, int, int);
extern void hoc_register_limits(int, HocParmLimits*);
extern void hoc_register_units(int, HocParmUnits*);
extern void nrn_promote(Prop*, int, int);
extern Memb_func* memb_func;
 
#define NMODL_TEXT 1
#if NMODL_TEXT
static const char* nmodl_file_text;
static const char* nmodl_filename;
extern void hoc_reg_nmodl_text(int, const char*);
extern void hoc_reg_nmodl_filename(int, const char*);
#endif

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
 "setdata_ka", _hoc_setdata,
 "a_c_ka", _hoc_a_c,
 "a_m_ka", _hoc_a_m,
 "a_inf_ka", _hoc_a_inf,
 "b_c_ka", _hoc_b_c,
 "b_m_ka", _hoc_b_m,
 "b_inf_ka", _hoc_b_inf,
 "efun_ka", _hoc_efun,
 "ghk_ka", _hoc_ghk,
 "window_ka", _hoc_window,
 0, 0
};
#define _f_b_c _f_b_c_ka
#define _f_b_m _f_b_m_ka
#define _f_a_c _f_a_c_ka
#define _f_a_m _f_a_m_ka
#define a_c a_c_ka
#define a_m a_m_ka
#define a_inf a_inf_ka
#define b_c b_c_ka
#define b_m b_m_ka
#define b_inf b_inf_ka
#define efun efun_ka
#define ghk ghk_ka
#define window window_ka
 extern double _f_b_c( _threadargsprotocomma_ double );
 extern double _f_b_m( _threadargsprotocomma_ double );
 extern double _f_a_c( _threadargsprotocomma_ double );
 extern double _f_a_m( _threadargsprotocomma_ double );
 extern double a_c( _threadargsprotocomma_ double );
 extern double a_m( _threadargsprotocomma_ double );
 extern double a_inf( _threadargsprotocomma_ double );
 extern double b_c( _threadargsprotocomma_ double );
 extern double b_m( _threadargsprotocomma_ double );
 extern double b_inf( _threadargsprotocomma_ double );
 extern double efun( _threadargsprotocomma_ double );
 extern double ghk( _threadargsprotocomma_ double , double , double );
 extern double window( _threadargsprotocomma_ double );
 
static void _check_a_m(double*, Datum*, Datum*, _NrnThread*); 
static void _check_a_c(double*, Datum*, Datum*, _NrnThread*); 
static void _check_b_m(double*, Datum*, Datum*, _NrnThread*); 
static void _check_b_c(double*, Datum*, Datum*, _NrnThread*); 
static void _check_table_thread(double* _p, Datum* _ppvar, Datum* _thread, _NrnThread* _nt, int _type) {
   _check_a_m(_p, _ppvar, _thread, _nt);
   _check_a_c(_p, _ppvar, _thread, _nt);
   _check_b_m(_p, _ppvar, _thread, _nt);
   _check_b_c(_p, _ppvar, _thread, _nt);
 }
 #define _za1 _thread[2]._pval[0]
 #define _za2 _thread[2]._pval[1]
 #define _zb1 _thread[2]._pval[2]
 #define _zb2 _thread[2]._pval[3]
 /* declare global and static user variables */
#define shifth shifth_ka
 double shifth = 0;
#define shiftm shiftm_ka
 double shiftm = 0;
#define usetable usetable_ka
 double usetable = 1;
 /* some parameters have upper and lower limits */
 static HocParmLimits _hoc_parm_limits[] = {
 "usetable_ka", 0, 1,
 0,0,0
};
 static HocParmUnits _hoc_parm_units[] = {
 "shiftm_ka", "mV",
 "shifth_ka", "mV",
 "gkbar_ka", "cm/s",
 "ik_ka", "mA/cm2",
 0,0
};
 static double ac0 = 0;
 static double am0 = 0;
 static double bc0 = 0;
 static double bm0 = 0;
 static double delta_t = 0.01;
 static double qk0 = 0;
 /* connect global user variables to hoc */
 static DoubScal hoc_scdoub[] = {
 "shiftm_ka", &shiftm_ka,
 "shifth_ka", &shifth_ka,
 "usetable_ka", &usetable_ka,
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
 
#define _cvode_ieq _ppvar[4]._i
 static void _ode_matsol_instance1(_threadargsproto_);
 /* connect range variables in _p that hoc is supposed to know about */
 static const char *_mechanism[] = {
 "7.7.0",
"ka",
 "gkbar_ka",
 0,
 "ik_ka",
 0,
 "am_ka",
 "ac_ka",
 "bm_ka",
 "bc_ka",
 "qk_ka",
 0,
 0};
 static Symbol* _morphology_sym;
 static Symbol* _k_sym;
 
extern Prop* need_memb(Symbol*);

static void nrn_alloc(Prop* _prop) {
	Prop *prop_ion;
	double *_p; Datum *_ppvar;
 	_p = nrn_prop_data_alloc(_mechtype, 15, _prop);
 	/*initialize range parameters*/
 	gkbar = 0.001;
 	_prop->param = _p;
 	_prop->param_size = 15;
 	_ppvar = nrn_prop_datum_alloc(_mechtype, 5, _prop);
 	_prop->dparam = _ppvar;
 	/*connect ionic variables to this model*/
 prop_ion = need_memb(_morphology_sym);
 	_ppvar[3]._pval = &prop_ion->param[0]; /* diam */
 prop_ion = need_memb(_k_sym);
 nrn_promote(prop_ion, 0, 1);
 	_ppvar[0]._pval = &prop_ion->param[0]; /* ek */
 	_ppvar[1]._pval = &prop_ion->param[3]; /* ik */
 	_ppvar[2]._pval = &prop_ion->param[4]; /* _ion_dikdv */
 
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

 void _ka_reg() {
	int _vectorized = 1;
  _initlists();
 	ion_reg("k", -10000.);
 	_morphology_sym = hoc_lookup("morphology");
 	_k_sym = hoc_lookup("k_ion");
 	register_mech(_mechanism, nrn_alloc,nrn_cur, nrn_jacob, nrn_state, nrn_init, hoc_nrnpointerindex, 4);
  _extcall_thread = (Datum*)ecalloc(3, sizeof(Datum));
  _thread_mem_init(_extcall_thread);
 _mechtype = nrn_get_mechtype(_mechanism[1]);
     _nrn_setdata_reg(_mechtype, _setdata);
     _nrn_thread_reg(_mechtype, 1, _thread_mem_init);
     _nrn_thread_reg(_mechtype, 0, _thread_cleanup);
     _nrn_thread_reg(_mechtype, 2, _update_ion_pointer);
     _nrn_thread_table_reg(_mechtype, _check_table_thread);
 #if NMODL_TEXT
  hoc_reg_nmodl_text(_mechtype, nmodl_file_text);
  hoc_reg_nmodl_filename(_mechtype, nmodl_filename);
#endif
  hoc_register_prop_size(_mechtype, 15, 5);
  hoc_register_dparam_semantics(_mechtype, 0, "k_ion");
  hoc_register_dparam_semantics(_mechtype, 1, "k_ion");
  hoc_register_dparam_semantics(_mechtype, 2, "k_ion");
  hoc_register_dparam_semantics(_mechtype, 4, "cvodeieq");
  hoc_register_dparam_semantics(_mechtype, 3, "diam");
 	hoc_register_cvode(_mechtype, _ode_count, _ode_map, _ode_spec, _ode_matsol);
 	hoc_register_tolerance(_mechtype, _hoc_state_tol, &_atollist);
 	hoc_register_var(hoc_scdoub, hoc_vdoub, hoc_intfunc);
 	ivoc_help("help ?1 ka /home/kseniia/Documents/spreadingDepression/spreading-depression/x86_64/ka.mod\n");
 hoc_register_limits(_mechtype, _hoc_parm_limits);
 hoc_register_units(_mechtype, _hoc_parm_units);
 }
 static double PI = 3.14159;
 static double FARADAY = 96485.309;
 static double R = 8.3145;
 /*Top LOCAL _za1 , _za2 , _zb1 , _zb2 */
 static double *_t_a_m;
 static double *_t_a_c;
 static double *_t_b_m;
 static double *_t_b_c;
static int _reset;
static char *modelname = "ka";

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
 static double _n_b_c(_threadargsprotocomma_ double _lv);
 static double _n_b_m(_threadargsprotocomma_ double _lv);
 static double _n_a_c(_threadargsprotocomma_ double _lv);
 static double _n_a_m(_threadargsprotocomma_ double _lv);
 static int _slist1[5], _dlist1[5]; static double *_temp1;
 static int kstate();
 
static int kstate (void* _so, double* _rhs, double* _p, Datum* _ppvar, Datum* _thread, _NrnThread* _nt)
 {int _reset=0;
 {
   double b_flux, f_flux, _term; int _i;
 {int _i; double _dt1 = 1.0/dt;
for(_i=2;_i<5;_i++){
  	_RHS1(_i) = -_dt1*(_p[_slist1[_i]] - _p[_dlist1[_i]]);
	_MATELM1(_i, _i) = _dt1;
      
}  
_RHS1(4) *= ( diam * diam * PI / 4.0) ;
_MATELM1(4, 4) *= ( diam * diam * PI / 4.0);  }
 _za1 = a_m ( _threadargscomma_ v ) ;
   _za2 = a_c ( _threadargscomma_ v ) ;
   _zb1 = b_m ( _threadargscomma_ v ) ;
   _zb2 = b_c ( _threadargscomma_ v ) ;
   /* ~ ac <-> am ( _za1 , _za2 )*/
 f_flux =  _za1 * ac ;
 b_flux =  _za2 * am ;
 _RHS1( 2) += (f_flux - b_flux);
 
 _term =  _za1 ;
 _MATELM1( 2 ,1)  -= _term;
 _term =  _za2 ;
 _MATELM1( 2 ,2)  += _term;
 /*REACTION*/
  /* ~ bc <-> bm ( _zb1 , _zb2 )*/
 f_flux =  _zb1 * bc ;
 b_flux =  _zb2 * bm ;
 _RHS1( 3) += (f_flux - b_flux);
 
 _term =  _zb1 ;
 _MATELM1( 3 ,0)  -= _term;
 _term =  _zb2 ;
 _MATELM1( 3 ,3)  += _term;
 /*REACTION*/
   /* am + ac = 1.0 */
 _RHS1(1) =  1.0;
 _MATELM1(1, 1) = 1;
 _RHS1(1) -= ac ;
 _MATELM1(1, 2) = 1;
 _RHS1(1) -= am ;
 /*CONSERVATION*/
  /* bm + bc = 1.0 */
 _RHS1(0) =  1.0;
 _MATELM1(0, 0) = 1;
 _RHS1(0) -= bc ;
 _MATELM1(0, 3) = 1;
 _RHS1(0) -= bm ;
 /*CONSERVATION*/
 /* COMPARTMENT diam * diam * PI / 4.0 {
     qk }
   */
 /* ~ qk < < ( ( - ik * diam ) * PI * ( 1e4 ) / FARADAY )*/
 f_flux = b_flux = 0.;
 _RHS1( 4) += (b_flux =   ( ( - ik * diam ) * PI * ( 1e4 ) / FARADAY ) );
 /*FLUX*/
    } return _reset;
 }
 static double _mfac_a_m, _tmin_a_m;
  static void _check_a_m(double* _p, Datum* _ppvar, Datum* _thread, _NrnThread* _nt) {
  static int _maktable=1; int _i, _j, _ix = 0;
  double _xi, _tmax;
  static double _sav_shiftm;
  if (!usetable) {return;}
  if (_sav_shiftm != shiftm) { _maktable = 1;}
  if (_maktable) { double _x, _dx; _maktable=0;
   _tmin_a_m =  - 150.0 ;
   _tmax =  150.0 ;
   _dx = (_tmax - _tmin_a_m)/200.; _mfac_a_m = 1./_dx;
   for (_i=0, _x=_tmin_a_m; _i < 201; _x += _dx, _i++) {
    _t_a_m[_i] = _f_a_m(_p, _ppvar, _thread, _nt, _x);
   }
   _sav_shiftm = shiftm;
  }
 }

 double a_m(double* _p, Datum* _ppvar, Datum* _thread, _NrnThread* _nt, double _lv) { 
#if 0
_check_a_m(_p, _ppvar, _thread, _nt);
#endif
 return _n_a_m(_p, _ppvar, _thread, _nt, _lv);
 }

 static double _n_a_m(double* _p, Datum* _ppvar, Datum* _thread, _NrnThread* _nt, double _lv){ int _i, _j;
 double _xi, _theta;
 if (!usetable) {
 return _f_a_m(_p, _ppvar, _thread, _nt, _lv); 
}
 _xi = _mfac_a_m * (_lv - _tmin_a_m);
 if (isnan(_xi)) {
  return _xi; }
 if (_xi <= 0.) {
 return _t_a_m[0];
 }
 if (_xi >= 200.) {
 return _t_a_m[200];
 }
 _i = (int) _xi;
 return _t_a_m[_i] + (_xi - (double)_i)*(_t_a_m[_i+1] - _t_a_m[_i]);
 }

 
double _f_a_m ( _threadargsprotocomma_ double _lv ) {
   double _la_m;
 double _lshift ;
 _lshift = - 30.0 + shiftm ;
   _la_m = 0.02 * ( 13.1 - _lv - 70.0 - _lshift ) / ( exp ( ( 13.1 - _lv - 70.0 - _lshift ) / 10.0 ) - 1.0 ) ;
   
return _la_m;
 }
 
static void _hoc_a_m(void) {
  double _r;
   double* _p; Datum* _ppvar; Datum* _thread; _NrnThread* _nt;
   if (_extcall_prop) {_p = _extcall_prop->param; _ppvar = _extcall_prop->dparam;}else{ _p = (double*)0; _ppvar = (Datum*)0; }
  _thread = _extcall_thread;
  _nt = nrn_threads;
 
#if 1
 _check_a_m(_p, _ppvar, _thread, _nt);
#endif
 _r =  a_m ( _p, _ppvar, _thread, _nt, *getarg(1) );
 hoc_retpushx(_r);
}
 static double _mfac_a_c, _tmin_a_c;
  static void _check_a_c(double* _p, Datum* _ppvar, Datum* _thread, _NrnThread* _nt) {
  static int _maktable=1; int _i, _j, _ix = 0;
  double _xi, _tmax;
  static double _sav_shiftm;
  if (!usetable) {return;}
  if (_sav_shiftm != shiftm) { _maktable = 1;}
  if (_maktable) { double _x, _dx; _maktable=0;
   _tmin_a_c =  - 150.0 ;
   _tmax =  150.0 ;
   _dx = (_tmax - _tmin_a_c)/200.; _mfac_a_c = 1./_dx;
   for (_i=0, _x=_tmin_a_c; _i < 201; _x += _dx, _i++) {
    _t_a_c[_i] = _f_a_c(_p, _ppvar, _thread, _nt, _x);
   }
   _sav_shiftm = shiftm;
  }
 }

 double a_c(double* _p, Datum* _ppvar, Datum* _thread, _NrnThread* _nt, double _lv) { 
#if 0
_check_a_c(_p, _ppvar, _thread, _nt);
#endif
 return _n_a_c(_p, _ppvar, _thread, _nt, _lv);
 }

 static double _n_a_c(double* _p, Datum* _ppvar, Datum* _thread, _NrnThread* _nt, double _lv){ int _i, _j;
 double _xi, _theta;
 if (!usetable) {
 return _f_a_c(_p, _ppvar, _thread, _nt, _lv); 
}
 _xi = _mfac_a_c * (_lv - _tmin_a_c);
 if (isnan(_xi)) {
  return _xi; }
 if (_xi <= 0.) {
 return _t_a_c[0];
 }
 if (_xi >= 200.) {
 return _t_a_c[200];
 }
 _i = (int) _xi;
 return _t_a_c[_i] + (_xi - (double)_i)*(_t_a_c[_i+1] - _t_a_c[_i]);
 }

 
double _f_a_c ( _threadargsprotocomma_ double _lv ) {
   double _la_c;
 double _lshift ;
 _lshift = - 30.0 + shiftm ;
   _la_c = 0.0175 * ( _lv - 40.1 + 70.0 + _lshift ) / ( exp ( ( _lv - 40.1 + 70.0 + _lshift ) / 10.0 ) - 1.0 ) ;
   
return _la_c;
 }
 
static void _hoc_a_c(void) {
  double _r;
   double* _p; Datum* _ppvar; Datum* _thread; _NrnThread* _nt;
   if (_extcall_prop) {_p = _extcall_prop->param; _ppvar = _extcall_prop->dparam;}else{ _p = (double*)0; _ppvar = (Datum*)0; }
  _thread = _extcall_thread;
  _nt = nrn_threads;
 
#if 1
 _check_a_c(_p, _ppvar, _thread, _nt);
#endif
 _r =  a_c ( _p, _ppvar, _thread, _nt, *getarg(1) );
 hoc_retpushx(_r);
}
 static double _mfac_b_m, _tmin_b_m;
  static void _check_b_m(double* _p, Datum* _ppvar, Datum* _thread, _NrnThread* _nt) {
  static int _maktable=1; int _i, _j, _ix = 0;
  double _xi, _tmax;
  static double _sav_shifth;
  if (!usetable) {return;}
  if (_sav_shifth != shifth) { _maktable = 1;}
  if (_maktable) { double _x, _dx; _maktable=0;
   _tmin_b_m =  - 150.0 ;
   _tmax =  150.0 ;
   _dx = (_tmax - _tmin_b_m)/200.; _mfac_b_m = 1./_dx;
   for (_i=0, _x=_tmin_b_m; _i < 201; _x += _dx, _i++) {
    _t_b_m[_i] = _f_b_m(_p, _ppvar, _thread, _nt, _x);
   }
   _sav_shifth = shifth;
  }
 }

 double b_m(double* _p, Datum* _ppvar, Datum* _thread, _NrnThread* _nt, double _lv) { 
#if 0
_check_b_m(_p, _ppvar, _thread, _nt);
#endif
 return _n_b_m(_p, _ppvar, _thread, _nt, _lv);
 }

 static double _n_b_m(double* _p, Datum* _ppvar, Datum* _thread, _NrnThread* _nt, double _lv){ int _i, _j;
 double _xi, _theta;
 if (!usetable) {
 return _f_b_m(_p, _ppvar, _thread, _nt, _lv); 
}
 _xi = _mfac_b_m * (_lv - _tmin_b_m);
 if (isnan(_xi)) {
  return _xi; }
 if (_xi <= 0.) {
 return _t_b_m[0];
 }
 if (_xi >= 200.) {
 return _t_b_m[200];
 }
 _i = (int) _xi;
 return _t_b_m[_i] + (_xi - (double)_i)*(_t_b_m[_i+1] - _t_b_m[_i]);
 }

 
double _f_b_m ( _threadargsprotocomma_ double _lv ) {
   double _lb_m;
 _lb_m = 0.016 * exp ( ( - 13.0 - _lv - 70.0 - shifth ) / 18.0 ) ;
   
return _lb_m;
 }
 
static void _hoc_b_m(void) {
  double _r;
   double* _p; Datum* _ppvar; Datum* _thread; _NrnThread* _nt;
   if (_extcall_prop) {_p = _extcall_prop->param; _ppvar = _extcall_prop->dparam;}else{ _p = (double*)0; _ppvar = (Datum*)0; }
  _thread = _extcall_thread;
  _nt = nrn_threads;
 
#if 1
 _check_b_m(_p, _ppvar, _thread, _nt);
#endif
 _r =  b_m ( _p, _ppvar, _thread, _nt, *getarg(1) );
 hoc_retpushx(_r);
}
 static double _mfac_b_c, _tmin_b_c;
  static void _check_b_c(double* _p, Datum* _ppvar, Datum* _thread, _NrnThread* _nt) {
  static int _maktable=1; int _i, _j, _ix = 0;
  double _xi, _tmax;
  static double _sav_shifth;
  if (!usetable) {return;}
  if (_sav_shifth != shifth) { _maktable = 1;}
  if (_maktable) { double _x, _dx; _maktable=0;
   _tmin_b_c =  - 150.0 ;
   _tmax =  150.0 ;
   _dx = (_tmax - _tmin_b_c)/200.; _mfac_b_c = 1./_dx;
   for (_i=0, _x=_tmin_b_c; _i < 201; _x += _dx, _i++) {
    _t_b_c[_i] = _f_b_c(_p, _ppvar, _thread, _nt, _x);
   }
   _sav_shifth = shifth;
  }
 }

 double b_c(double* _p, Datum* _ppvar, Datum* _thread, _NrnThread* _nt, double _lv) { 
#if 0
_check_b_c(_p, _ppvar, _thread, _nt);
#endif
 return _n_b_c(_p, _ppvar, _thread, _nt, _lv);
 }

 static double _n_b_c(double* _p, Datum* _ppvar, Datum* _thread, _NrnThread* _nt, double _lv){ int _i, _j;
 double _xi, _theta;
 if (!usetable) {
 return _f_b_c(_p, _ppvar, _thread, _nt, _lv); 
}
 _xi = _mfac_b_c * (_lv - _tmin_b_c);
 if (isnan(_xi)) {
  return _xi; }
 if (_xi <= 0.) {
 return _t_b_c[0];
 }
 if (_xi >= 200.) {
 return _t_b_c[200];
 }
 _i = (int) _xi;
 return _t_b_c[_i] + (_xi - (double)_i)*(_t_b_c[_i+1] - _t_b_c[_i]);
 }

 
double _f_b_c ( _threadargsprotocomma_ double _lv ) {
   double _lb_c;
 _lb_c = 0.5 / ( 1.0 + exp ( ( 10.1 - _lv - 70.0 - shifth ) / 5.0 ) ) ;
   
return _lb_c;
 }
 
static void _hoc_b_c(void) {
  double _r;
   double* _p; Datum* _ppvar; Datum* _thread; _NrnThread* _nt;
   if (_extcall_prop) {_p = _extcall_prop->param; _ppvar = _extcall_prop->dparam;}else{ _p = (double*)0; _ppvar = (Datum*)0; }
  _thread = _extcall_thread;
  _nt = nrn_threads;
 
#if 1
 _check_b_c(_p, _ppvar, _thread, _nt);
#endif
 _r =  b_c ( _p, _ppvar, _thread, _nt, *getarg(1) );
 hoc_retpushx(_r);
}
 
double a_inf ( _threadargsprotocomma_ double _lv ) {
   double _la_inf;
 _la_inf = a_m ( _threadargscomma_ _lv ) / ( a_m ( _threadargscomma_ _lv ) + a_c ( _threadargscomma_ _lv ) ) ;
   
return _la_inf;
 }
 
static void _hoc_a_inf(void) {
  double _r;
   double* _p; Datum* _ppvar; Datum* _thread; _NrnThread* _nt;
   if (_extcall_prop) {_p = _extcall_prop->param; _ppvar = _extcall_prop->dparam;}else{ _p = (double*)0; _ppvar = (Datum*)0; }
  _thread = _extcall_thread;
  _nt = nrn_threads;
 _r =  a_inf ( _p, _ppvar, _thread, _nt, *getarg(1) );
 hoc_retpushx(_r);
}
 
double b_inf ( _threadargsprotocomma_ double _lv ) {
   double _lb_inf;
 _lb_inf = b_m ( _threadargscomma_ _lv ) / ( b_m ( _threadargscomma_ _lv ) + b_c ( _threadargscomma_ _lv ) ) ;
   
return _lb_inf;
 }
 
static void _hoc_b_inf(void) {
  double _r;
   double* _p; Datum* _ppvar; Datum* _thread; _NrnThread* _nt;
   if (_extcall_prop) {_p = _extcall_prop->param; _ppvar = _extcall_prop->dparam;}else{ _p = (double*)0; _ppvar = (Datum*)0; }
  _thread = _extcall_thread;
  _nt = nrn_threads;
 _r =  b_inf ( _p, _ppvar, _thread, _nt, *getarg(1) );
 hoc_retpushx(_r);
}
 
double window ( _threadargsprotocomma_ double _lv ) {
   double _lwindow;
 _lwindow = gkbar * a_inf ( _threadargscomma_ _lv ) * a_inf ( _threadargscomma_ _lv ) * b_inf ( _threadargscomma_ _lv ) * ( _lv - ek ) ;
   
return _lwindow;
 }
 
static void _hoc_window(void) {
  double _r;
   double* _p; Datum* _ppvar; Datum* _thread; _NrnThread* _nt;
   if (_extcall_prop) {_p = _extcall_prop->param; _ppvar = _extcall_prop->dparam;}else{ _p = (double*)0; _ppvar = (Datum*)0; }
  _thread = _extcall_thread;
  _nt = nrn_threads;
 _r =  window ( _p, _ppvar, _thread, _nt, *getarg(1) );
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
 {int _i; for(_i=0;_i<5;_i++) _p[_dlist1[_i]] = 0.0;}
 _za1 = a_m ( _threadargscomma_ v ) ;
 _za2 = a_c ( _threadargscomma_ v ) ;
 _zb1 = b_m ( _threadargscomma_ v ) ;
 _zb2 = b_c ( _threadargscomma_ v ) ;
 /* ~ ac <-> am ( _za1 , _za2 )*/
 f_flux =  _za1 * ac ;
 b_flux =  _za2 * am ;
 Dac -= (f_flux - b_flux);
 Dam += (f_flux - b_flux);
 
 /*REACTION*/
  /* ~ bc <-> bm ( _zb1 , _zb2 )*/
 f_flux =  _zb1 * bc ;
 b_flux =  _zb2 * bm ;
 Dbc -= (f_flux - b_flux);
 Dbm += (f_flux - b_flux);
 
 /*REACTION*/
   /* am + ac = 1.0 */
 /*CONSERVATION*/
  /* bm + bc = 1.0 */
 /*CONSERVATION*/
 /* COMPARTMENT diam * diam * PI / 4.0 {
   qk }
 */
 /* ~ qk < < ( ( - ik * diam ) * PI * ( 1e4 ) / FARADAY )*/
 f_flux = b_flux = 0.;
 Dqk += (b_flux =   ( ( - ik * diam ) * PI * ( 1e4 ) / FARADAY ) );
 /*FLUX*/
  _p[_dlist1[4]] /= ( diam * diam * PI / 4.0);
   } return _reset;
 }
 
/*CVODE matsol*/
 static int _ode_matsol1(void* _so, double* _rhs, double* _p, Datum* _ppvar, Datum* _thread, _NrnThread* _nt) {int _reset=0;{
 double b_flux, f_flux, _term; int _i;
   b_flux = f_flux = 0.;
 {int _i; double _dt1 = 1.0/dt;
for(_i=0;_i<5;_i++){
  	_RHS1(_i) = _dt1*(_p[_dlist1[_i]]);
	_MATELM1(_i, _i) = _dt1;
      
}  
_RHS1(4) *= ( diam * diam * PI / 4.0) ;
_MATELM1(4, 4) *= ( diam * diam * PI / 4.0);  }
 _za1 = a_m ( _threadargscomma_ v ) ;
 _za2 = a_c ( _threadargscomma_ v ) ;
 _zb1 = b_m ( _threadargscomma_ v ) ;
 _zb2 = b_c ( _threadargscomma_ v ) ;
 /* ~ ac <-> am ( _za1 , _za2 )*/
 _term =  _za1 ;
 _MATELM1( 1 ,1)  += _term;
 _MATELM1( 2 ,1)  -= _term;
 _term =  _za2 ;
 _MATELM1( 1 ,2)  -= _term;
 _MATELM1( 2 ,2)  += _term;
 /*REACTION*/
  /* ~ bc <-> bm ( _zb1 , _zb2 )*/
 _term =  _zb1 ;
 _MATELM1( 0 ,0)  += _term;
 _MATELM1( 3 ,0)  -= _term;
 _term =  _zb2 ;
 _MATELM1( 0 ,3)  -= _term;
 _MATELM1( 3 ,3)  += _term;
 /*REACTION*/
   /* am + ac = 1.0 */
 /*CONSERVATION*/
  /* bm + bc = 1.0 */
 /*CONSERVATION*/
 /* COMPARTMENT diam * diam * PI / 4.0 {
 qk }
 */
 /* ~ qk < < ( ( - ik * diam ) * PI * ( 1e4 ) / FARADAY )*/
 /*FLUX*/
    } return _reset;
 }
 
/*CVODE end*/
 
static int _ode_count(int _type){ return 5;}
 
static void _ode_spec(_NrnThread* _nt, _Memb_list* _ml, int _type) {
   double* _p; Datum* _ppvar; Datum* _thread;
   Node* _nd; double _v; int _iml, _cntml;
  _cntml = _ml->_nodecount;
  _thread = _ml->_thread;
  for (_iml = 0; _iml < _cntml; ++_iml) {
    _p = _ml->_data[_iml]; _ppvar = _ml->_pdata[_iml];
    _nd = _ml->_nodelist[_iml];
    v = NODEV(_nd);
  ek = _ion_ek;
     _ode_spec1 (_p, _ppvar, _thread, _nt);
  }}
 
static void _ode_map(int _ieq, double** _pv, double** _pvdot, double* _pp, Datum* _ppd, double* _atol, int _type) { 
	double* _p; Datum* _ppvar;
 	int _i; _p = _pp; _ppvar = _ppd;
	_cvode_ieq = _ieq;
	for (_i=0; _i < 5; ++_i) {
		_pv[_i] = _pp + _slist1[_i];  _pvdot[_i] = _pp + _dlist1[_i];
		_cvode_abstol(_atollist, _atol, _i);
	}
 }
 
static void _ode_matsol_instance1(_threadargsproto_) {
 _cvode_sparse_thread(&_thread[_cvspth1]._pvoid, 5, _dlist1, _p, _ode_matsol1, _ppvar, _thread, _nt);
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
  ek = _ion_ek;
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
   nrn_update_ion_pointer(_k_sym, _ppvar, 0, 0);
   nrn_update_ion_pointer(_k_sym, _ppvar, 1, 3);
   nrn_update_ion_pointer(_k_sym, _ppvar, 2, 4);
 }

static void initmodel(double* _p, Datum* _ppvar, Datum* _thread, _NrnThread* _nt) {
  int _i; double _save;{
  ac = ac0;
  am = am0;
  bc = bc0;
  bm = bm0;
  qk = qk0;
 {
   am = a_inf ( _threadargscomma_ v ) ;
   ac = 1.0 - am ;
   bm = b_inf ( _threadargscomma_ v ) ;
   bc = 1.0 - bm ;
   qk = 0.0 ;
   ik = gkbar * am * am * bm * ( v - ek ) ;
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
 _check_a_m(_p, _ppvar, _thread, _nt);
 _check_a_c(_p, _ppvar, _thread, _nt);
 _check_b_m(_p, _ppvar, _thread, _nt);
 _check_b_c(_p, _ppvar, _thread, _nt);
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
  ek = _ion_ek;
 initmodel(_p, _ppvar, _thread, _nt);
 }
}

static double _nrn_current(double* _p, Datum* _ppvar, Datum* _thread, _NrnThread* _nt, double _v){double _current=0.;v=_v;{ {
   ik = gkbar * am * am * bm * ( v - ek ) ;
   }
 _current += ik;

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
  ek = _ion_ek;
 _g = _nrn_current(_p, _ppvar, _thread, _nt, _v + .001);
 	{ double _dik;
  _dik = ik;
 _rhs = _nrn_current(_p, _ppvar, _thread, _nt, _v);
  _ion_dikdv += (_dik - ik)/.001 ;
 	}
 _g = (_g - _rhs)/.001;
  _ion_ik += ik ;
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
  ek = _ion_ek;
 {  sparse_thread(&_thread[_spth1]._pvoid, 5, _slist1, _dlist1, _p, &t, dt, kstate, _linmat1, _ppvar, _thread, _nt);
     if (secondorder) {
    int _i;
    for (_i = 0; _i < 5; ++_i) {
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
   _t_a_m = makevector(201*sizeof(double));
   _t_a_c = makevector(201*sizeof(double));
   _t_b_m = makevector(201*sizeof(double));
   _t_b_c = makevector(201*sizeof(double));
 _slist1[0] = &(bc) - _p;  _dlist1[0] = &(Dbc) - _p;
 _slist1[1] = &(ac) - _p;  _dlist1[1] = &(Dac) - _p;
 _slist1[2] = &(am) - _p;  _dlist1[2] = &(Dam) - _p;
 _slist1[3] = &(bm) - _p;  _dlist1[3] = &(Dbm) - _p;
 _slist1[4] = &(qk) - _p;  _dlist1[4] = &(Dqk) - _p;
_first = 0;
}

#if defined(__cplusplus)
} /* extern "C" */
#endif

#if NMODL_TEXT
static const char* nmodl_filename = "/home/kseniia/Documents/spreadingDepression/spreading-depression/ka.mod";
static const char* nmodl_file_text = 
  "TITLE ka\n"
  ": Kalium stroom type A \n"
  ": twee gates met elk twee toestanden: open of dicht\n"
  ": \n"
  ": uit: Traub et al.\n"
  ": A branching dendritic model of a rodent CA3\n"
  ": pyramidal neurone.\n"
  "\n"
  "\n"
  "\n"
  "UNITS {\n"
  "	(molar) = (1/liter)\n"
  "	(mV) =	(millivolt)\n"
  "	(mA) =	(milliamp)\n"
  "	(mM) =	(millimolar)\n"
  "}\n"
  "\n"
  "INDEPENDENT {t FROM 0 TO 1 WITH 100 (ms)}\n"
  "\n"
  "NEURON {\n"
  "	SUFFIX ka\n"
  "	USEION k READ ek WRITE ik\n"
  "	RANGE gkbar, ik, qk\n"
  "	GLOBAL shiftm, shifth\n"
  "}\n"
  "\n"
  "UNITS {\n"
  "	PI		= (pi) (1)\n"
  "	FARADAY		= 96485.309 (coul)\n"
  "	R = (k-mole) (joule/degC)\n"
  "}\n"
  "\n"
  "PARAMETER {\n"
  "	celsius		(degC)\n"
  "	gkbar=1e-3	(cm/s)		: Maximum Permeability .2e-3*5 hans\n"
  "	shiftm = 0	(mV)\n"
  "	shifth = 0	(mV)\n"
  "}\n"
  "\n"
  "ASSIGNED { \n"
  "	ik	(mA/cm2)\n"
  "	v	(mV)	\n"
  "	ek	(mV)\n"
  "	diam	(um)\n"
  "}\n"
  "\n"
  "STATE { am ac bm bc qk }			: fraction of states, m=fraction in open state.\n"
  "\n"
  "BREAKPOINT {\n"
  "	SOLVE kstate METHOD sparse\n"
  "	ik = gkbar*am*am*bm*(v-ek)\n"
  "}\n"
  "\n"
  "INITIAL {\n"
  "	am=a_inf(v)\n"
  "	ac=1-am\n"
  "	bm=b_inf(v)\n"
  "	bc=1-bm\n"
  "	qk=0\n"
  "	ik = gkbar*am*am*bm*(v-ek)\n"
  "\n"
  "}\n"
  "\n"
  "LOCAL a1,a2,b1,b2\n"
  "\n"
  "KINETIC kstate {\n"
  "	a1 = a_m(v)\n"
  "	a2 = a_c(v)\n"
  "	b1 = b_m(v)\n"
  "	b2 = b_c(v)\n"
  "	~ ac <-> am (a1, a2)\n"
  "	~ bc <-> bm (b1, b2)\n"
  "	\n"
  "	CONSERVE am + ac = 1\n"
  "	CONSERVE bm + bc = 1\n"
  "	\n"
  "	COMPARTMENT diam*diam*PI/4 { qk }\n"
  "	~ qk << ((-ik*diam )*PI*(1e4)/FARADAY )\n"
  "}\n"
  "\n"
  "FUNCTION a_m(v(mV)) {\n"
  "	LOCAL shift\n"
  "	TABLE DEPEND shiftm FROM -150 TO 150 WITH 200\n"
  "	shift=-30+shiftm\n"
  "	a_m=0.02*(13.1-v-70-shift)/(exp((13.1-v-70-shift)/10)-1)\n"
  "}\n"
  "\n"
  "FUNCTION a_c(v(mV)) {\n"
  "	LOCAL shift\n"
  "	TABLE DEPEND shiftm FROM -150 TO 150 WITH 200\n"
  "	shift=-30+shiftm\n"
  "	a_c=0.0175*(v-40.1+70+shift)/(exp((v-40.1+70+shift)/10)-1)	\n"
  "}\n"
  "\n"
  "FUNCTION b_m(v(mV)) {\n"
  "	TABLE DEPEND shifth FROM -150 TO 150 WITH 200\n"
  "	b_m = 0.016*exp((-13-v-70-shifth)/18)\n"
  "}\n"
  "\n"
  "FUNCTION b_c(v(mV)) {\n"
  "	TABLE DEPEND shifth FROM -150 TO 150 WITH 200\n"
  "	b_c = 0.5/(1+exp((10.1-v-70-shifth)/5))\n"
  "}\n"
  "\n"
  "FUNCTION a_inf(v(mV)) {\n"
  "        a_inf = a_m(v) / ( a_m(v) + a_c(v) )\n"
  "}\n"
  "\n"
  "FUNCTION b_inf(v(mV)) {\n"
  "        b_inf = b_m(v) / ( b_m(v) + b_c(v) )\n"
  "}\n"
  "\n"
  "FUNCTION window(v(mV)) {\n"
  "	window=gkbar*a_inf(v)*a_inf(v)*b_inf(v)*(v-ek)\n"
  "}\n"
  "\n"
  "FUNCTION ghk(v(mV), ci(mM), co(mM)) (.001 coul/cm3) {\n"
  "	LOCAL z, eci, eco\n"
  "	z = (1e-3)*1*FARADAY*v/(R*(celsius+273.11247574))\n"
  "	eco = co*efun(z)\n"
  "	eci = ci*efun(-z)\n"
  "	:high kao charge moves inward, mogelijke fouten vanwege oorsprong Ca(2+)!\n"
  "	:negative potential charge moves inward\n"
  "	ghk = (.001)*1*FARADAY*(eci - eco)\n"
  "}\n"
  "\n"
  "FUNCTION efun(z) {\n"
  "	if (fabs(z) < 1e-4) {\n"
  "		efun = 1 - z/2\n"
  "	}else{\n"
  "		efun = z/(exp(z) - 1)\n"
  "	}\n"
  "}\n"
  ;
#endif
