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
 
#define nrn_init _nrn_init__nachan
#define _nrn_initial _nrn_initial__nachan
#define nrn_cur _nrn_cur__nachan
#define _nrn_current _nrn_current__nachan
#define nrn_jacob _nrn_jacob__nachan
#define nrn_state _nrn_state__nachan
#define _net_receive _net_receive__nachan 
#define nastate nastate__nachan 
#define telspike telspike__nachan 
 
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
#define freq _p[2]
#define interval _p[3]
#define n _p[4]
#define firing _p[5]
#define ma _p[6]
#define mb _p[7]
#define ha _p[8]
#define hb _p[9]
#define qna _p[10]
#define ena _p[11]
#define Dma _p[12]
#define Dmb _p[13]
#define Dha _p[14]
#define Dhb _p[15]
#define Dqna _p[16]
#define v _p[17]
#define _g _p[18]
#define _ion_ena	*_ppvar[0]._pval
#define _ion_ina	*_ppvar[1]._pval
#define _ion_dinadv	*_ppvar[2]._pval
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
 static void _hoc_h_b(void);
 static void _hoc_h_a(void);
 static void _hoc_h_inf(void);
 static void _hoc_m_b(void);
 static void _hoc_m_a(void);
 static void _hoc_m_inf(void);
 static void _hoc_telspike(void);
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
 "setdata_nachan", _hoc_setdata,
 "h_b_nachan", _hoc_h_b,
 "h_a_nachan", _hoc_h_a,
 "h_inf_nachan", _hoc_h_inf,
 "m_b_nachan", _hoc_m_b,
 "m_a_nachan", _hoc_m_a,
 "m_inf_nachan", _hoc_m_inf,
 "telspike_nachan", _hoc_telspike,
 "window_nachan", _hoc_window,
 0, 0
};
#define _f_h_b _f_h_b_nachan
#define _f_h_a _f_h_a_nachan
#define _f_m_b _f_m_b_nachan
#define _f_m_a _f_m_a_nachan
#define h_b h_b_nachan
#define h_a h_a_nachan
#define h_inf h_inf_nachan
#define m_b m_b_nachan
#define m_a m_a_nachan
#define m_inf m_inf_nachan
#define window window_nachan
 extern double _f_h_b( _threadargsprotocomma_ double );
 extern double _f_h_a( _threadargsprotocomma_ double );
 extern double _f_m_b( _threadargsprotocomma_ double );
 extern double _f_m_a( _threadargsprotocomma_ double );
 extern double h_b( _threadargsprotocomma_ double );
 extern double h_a( _threadargsprotocomma_ double );
 extern double h_inf( _threadargsprotocomma_ double );
 extern double m_b( _threadargsprotocomma_ double );
 extern double m_a( _threadargsprotocomma_ double );
 extern double m_inf( _threadargsprotocomma_ double );
 extern double window( _threadargsprotocomma_ double );
 
static void _check_m_a(double*, Datum*, Datum*, _NrnThread*); 
static void _check_m_b(double*, Datum*, Datum*, _NrnThread*); 
static void _check_h_a(double*, Datum*, Datum*, _NrnThread*); 
static void _check_h_b(double*, Datum*, Datum*, _NrnThread*); 
static void _check_table_thread(double* _p, Datum* _ppvar, Datum* _thread, _NrnThread* _nt, int _type) {
   _check_m_a(_p, _ppvar, _thread, _nt);
   _check_m_b(_p, _ppvar, _thread, _nt);
   _check_h_a(_p, _ppvar, _thread, _nt);
   _check_h_b(_p, _ppvar, _thread, _nt);
 }
 #define _za1 _thread[2]._pval[0]
 #define _za2 _thread[2]._pval[1]
 #define _zb1 _thread[2]._pval[2]
 #define _zb2 _thread[2]._pval[3]
 /* declare global and static user variables */
#define scaletauh scaletauh_nachan
 double scaletauh = 1;
#define scaletaum scaletaum_nachan
 double scaletaum = 1;
#define shifth shifth_nachan
 double shifth = 0;
#define shiftm shiftm_nachan
 double shiftm = 0;
#define usetable usetable_nachan
 double usetable = 1;
 /* some parameters have upper and lower limits */
 static HocParmLimits _hoc_parm_limits[] = {
 "usetable_nachan", 0, 1,
 0,0,0
};
 static HocParmUnits _hoc_parm_units[] = {
 "shiftm_nachan", "mV",
 "shifth_nachan", "mV",
 "scaletaum_nachan", "mV",
 "scaletauh_nachan", "mV",
 "gnabar_nachan", "mho/cm2",
 "ina_nachan", "mA/cm2",
 0,0
};
 static double delta_t = 0.01;
 static double hb0 = 0;
 static double ha0 = 0;
 static double mb0 = 0;
 static double ma0 = 0;
 static double qna0 = 0;
 /* connect global user variables to hoc */
 static DoubScal hoc_scdoub[] = {
 "shiftm_nachan", &shiftm_nachan,
 "shifth_nachan", &shifth_nachan,
 "scaletaum_nachan", &scaletaum_nachan,
 "scaletauh_nachan", &scaletauh_nachan,
 "usetable_nachan", &usetable_nachan,
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
"nachan",
 "gnabar_nachan",
 0,
 "ina_nachan",
 "freq_nachan",
 "interval_nachan",
 "n_nachan",
 "firing_nachan",
 0,
 "ma_nachan",
 "mb_nachan",
 "ha_nachan",
 "hb_nachan",
 "qna_nachan",
 0,
 0};
 static Symbol* _morphology_sym;
 static Symbol* _na_sym;
 
extern Prop* need_memb(Symbol*);

static void nrn_alloc(Prop* _prop) {
	Prop *prop_ion;
	double *_p; Datum *_ppvar;
 	_p = nrn_prop_data_alloc(_mechtype, 19, _prop);
 	/*initialize range parameters*/
 	gnabar = 0.001;
 	_prop->param = _p;
 	_prop->param_size = 19;
 	_ppvar = nrn_prop_datum_alloc(_mechtype, 5, _prop);
 	_prop->dparam = _ppvar;
 	/*connect ionic variables to this model*/
 prop_ion = need_memb(_morphology_sym);
 	_ppvar[3]._pval = &prop_ion->param[0]; /* diam */
 prop_ion = need_memb(_na_sym);
 nrn_promote(prop_ion, 0, 1);
 	_ppvar[0]._pval = &prop_ion->param[0]; /* ena */
 	_ppvar[1]._pval = &prop_ion->param[3]; /* ina */
 	_ppvar[2]._pval = &prop_ion->param[4]; /* _ion_dinadv */
 
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

 void _na_reg() {
	int _vectorized = 1;
  _initlists();
 	ion_reg("na", -10000.);
 	_morphology_sym = hoc_lookup("morphology");
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
 #if NMODL_TEXT
  hoc_reg_nmodl_text(_mechtype, nmodl_file_text);
  hoc_reg_nmodl_filename(_mechtype, nmodl_filename);
#endif
  hoc_register_prop_size(_mechtype, 19, 5);
  hoc_register_dparam_semantics(_mechtype, 0, "na_ion");
  hoc_register_dparam_semantics(_mechtype, 1, "na_ion");
  hoc_register_dparam_semantics(_mechtype, 2, "na_ion");
  hoc_register_dparam_semantics(_mechtype, 4, "cvodeieq");
  hoc_register_dparam_semantics(_mechtype, 3, "diam");
 	hoc_register_cvode(_mechtype, _ode_count, _ode_map, _ode_spec, _ode_matsol);
 	hoc_register_tolerance(_mechtype, _hoc_state_tol, &_atollist);
 	hoc_register_var(hoc_scdoub, hoc_vdoub, hoc_intfunc);
 	ivoc_help("help ?1 nachan /home/kseniia/Documents/spreadingDepression/spreading-depression/x86_64/na.mod\n");
 hoc_register_limits(_mechtype, _hoc_parm_limits);
 hoc_register_units(_mechtype, _hoc_parm_units);
 }
 static double PI = 3.14159;
 static double FARADAY = 96485.309;
 static double R = 8.3145;
 /*Top LOCAL _za1 , _za2 , _zb1 , _zb2 */
 static double *_t_m_a;
 static double *_t_m_b;
 static double *_t_h_a;
 static double *_t_h_b;
static int _reset;
static char *modelname = "nachan";

static int error;
static int _ninits = 0;
static int _match_recurse=1;
static void _modl_cleanup(){ _match_recurse=1;}
static int telspike(_threadargsproto_);
 extern double *_nrn_thread_getelm();
 
#define _MATELM1(_row,_col) *(_nrn_thread_getelm(_so, _row + 1, _col + 1))
 
#define _RHS1(_arg) _rhs[_arg+1]
  
#define _linmat1  1
 static int _spth1 = 1;
 static int _cvspth1 = 0;
 
static int _ode_spec1(_threadargsproto_);
/*static int _ode_matsol1(_threadargsproto_);*/
 static double _n_h_b(_threadargsprotocomma_ double _lv);
 static double _n_h_a(_threadargsprotocomma_ double _lv);
 static double _n_m_b(_threadargsprotocomma_ double _lv);
 static double _n_m_a(_threadargsprotocomma_ double _lv);
 static int _slist1[5], _dlist1[5]; static double *_temp1;
 static int nastate();
 
static int nastate (void* _so, double* _rhs, double* _p, Datum* _ppvar, Datum* _thread, _NrnThread* _nt)
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
 /* COMPARTMENT diam * diam * PI / 4.0 {
     qna }
   */
 telspike ( _threadargs_ ) ;
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
 /* ~ qna < < ( - ina * PI * diam * ( 1e4 ) / FARADAY )*/
 f_flux = b_flux = 0.;
 _RHS1( 4) += (b_flux =   ( - ina * PI * diam * ( 1e4 ) / FARADAY ) );
 /*FLUX*/
    } return _reset;
 }
 
static int  telspike ( _threadargsproto_ ) {
   if ( ( ma * ma * ma * ha > .01 )  &&  ! firing ) {
     n = n + 1.0 ;
     if ( n > 1.0 ) {
       freq = 1000.0 / interval ;
       }
     firing = 1.0 ;
     interval = 0.0 ;
     }
   if ( ( ma * ma * ma * ha < .01 )  && firing ) {
     firing = 0.0 ;
     }
   interval = interval + dt / 2.0 ;
    return 0; }
 
static void _hoc_telspike(void) {
  double _r;
   double* _p; Datum* _ppvar; Datum* _thread; _NrnThread* _nt;
   if (_extcall_prop) {_p = _extcall_prop->param; _ppvar = _extcall_prop->dparam;}else{ _p = (double*)0; _ppvar = (Datum*)0; }
  _thread = _extcall_thread;
  _nt = nrn_threads;
 _r = 1.;
 telspike ( _p, _ppvar, _thread, _nt );
 hoc_retpushx(_r);
}
 static double _mfac_m_a, _tmin_m_a;
  static void _check_m_a(double* _p, Datum* _ppvar, Datum* _thread, _NrnThread* _nt) {
  static int _maktable=1; int _i, _j, _ix = 0;
  double _xi, _tmax;
  static double _sav_shiftm;
  static double _sav_scaletaum;
  if (!usetable) {return;}
  if (_sav_shiftm != shiftm) { _maktable = 1;}
  if (_sav_scaletaum != scaletaum) { _maktable = 1;}
  if (_maktable) { double _x, _dx; _maktable=0;
   _tmin_m_a =  - 150.0 ;
   _tmax =  150.0 ;
   _dx = (_tmax - _tmin_m_a)/301.; _mfac_m_a = 1./_dx;
   for (_i=0, _x=_tmin_m_a; _i < 302; _x += _dx, _i++) {
    _t_m_a[_i] = _f_m_a(_p, _ppvar, _thread, _nt, _x);
   }
   _sav_shiftm = shiftm;
   _sav_scaletaum = scaletaum;
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
 if (_xi >= 301.) {
 return _t_m_a[301];
 }
 _i = (int) _xi;
 return _t_m_a[_i] + (_xi - (double)_i)*(_t_m_a[_i+1] - _t_m_a[_i]);
 }

 
double _f_m_a ( _threadargsprotocomma_ double _lv ) {
   double _lm_a;
 _lm_a = scaletauh * 0.32 * ( 13.1 - _lv - 70.0 - shiftm ) / ( exp ( ( 13.1 - _lv - 70.0 - shiftm ) / 4.0 ) - 1.0 ) ;
   
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
  static double _sav_shiftm;
  static double _sav_scaletaum;
  if (!usetable) {return;}
  if (_sav_shiftm != shiftm) { _maktable = 1;}
  if (_sav_scaletaum != scaletaum) { _maktable = 1;}
  if (_maktable) { double _x, _dx; _maktable=0;
   _tmin_m_b =  - 150.0 ;
   _tmax =  150.0 ;
   _dx = (_tmax - _tmin_m_b)/301.; _mfac_m_b = 1./_dx;
   for (_i=0, _x=_tmin_m_b; _i < 302; _x += _dx, _i++) {
    _t_m_b[_i] = _f_m_b(_p, _ppvar, _thread, _nt, _x);
   }
   _sav_shiftm = shiftm;
   _sav_scaletaum = scaletaum;
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
 if (_xi >= 301.) {
 return _t_m_b[301];
 }
 _i = (int) _xi;
 return _t_m_b[_i] + (_xi - (double)_i)*(_t_m_b[_i+1] - _t_m_b[_i]);
 }

 
double _f_m_b ( _threadargsprotocomma_ double _lv ) {
   double _lm_b;
 _lm_b = scaletaum * 0.28 * ( _lv - 40.1 + 70.0 + shiftm ) / ( exp ( ( _lv - 40.1 + 70.0 + shiftm ) / 5.0 ) - 1.0 ) ;
   
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
  static double _sav_shifth;
  static double _sav_scaletauh;
  if (!usetable) {return;}
  if (_sav_shifth != shifth) { _maktable = 1;}
  if (_sav_scaletauh != scaletauh) { _maktable = 1;}
  if (_maktable) { double _x, _dx; _maktable=0;
   _tmin_h_a =  - 150.0 ;
   _tmax =  150.0 ;
   _dx = (_tmax - _tmin_h_a)/301.; _mfac_h_a = 1./_dx;
   for (_i=0, _x=_tmin_h_a; _i < 302; _x += _dx, _i++) {
    _t_h_a[_i] = _f_h_a(_p, _ppvar, _thread, _nt, _x);
   }
   _sav_shifth = shifth;
   _sav_scaletauh = scaletauh;
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
 if (_xi >= 301.) {
 return _t_h_a[301];
 }
 _i = (int) _xi;
 return _t_h_a[_i] + (_xi - (double)_i)*(_t_h_a[_i+1] - _t_h_a[_i]);
 }

 
double _f_h_a ( _threadargsprotocomma_ double _lv ) {
   double _lh_a;
 _lh_a = scaletauh * 0.128 * exp ( ( 17.0 - _lv - 70.0 - shifth ) / 18.0 ) ;
   
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
  static double _sav_shifth;
  static double _sav_scaletauh;
  if (!usetable) {return;}
  if (_sav_shifth != shifth) { _maktable = 1;}
  if (_sav_scaletauh != scaletauh) { _maktable = 1;}
  if (_maktable) { double _x, _dx; _maktable=0;
   _tmin_h_b =  - 150.0 ;
   _tmax =  150.0 ;
   _dx = (_tmax - _tmin_h_b)/301.; _mfac_h_b = 1./_dx;
   for (_i=0, _x=_tmin_h_b; _i < 302; _x += _dx, _i++) {
    _t_h_b[_i] = _f_h_b(_p, _ppvar, _thread, _nt, _x);
   }
   _sav_shifth = shifth;
   _sav_scaletauh = scaletauh;
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
 if (_xi >= 301.) {
 return _t_h_b[301];
 }
 _i = (int) _xi;
 return _t_h_b[_i] + (_xi - (double)_i)*(_t_h_b[_i+1] - _t_h_b[_i]);
 }

 
double _f_h_b ( _threadargsprotocomma_ double _lv ) {
   double _lh_b;
 _lh_b = scaletauh * 4.0 / ( 1.0 + exp ( ( 40.0 - _lv - 70.0 - shifth ) / 5.0 ) ) ;
   
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
 
double m_inf ( _threadargsprotocomma_ double _lv ) {
   double _lm_inf;
 _lm_inf = m_a ( _threadargscomma_ _lv ) / ( m_a ( _threadargscomma_ _lv ) + m_b ( _threadargscomma_ _lv ) ) ;
   
return _lm_inf;
 }
 
static void _hoc_m_inf(void) {
  double _r;
   double* _p; Datum* _ppvar; Datum* _thread; _NrnThread* _nt;
   if (_extcall_prop) {_p = _extcall_prop->param; _ppvar = _extcall_prop->dparam;}else{ _p = (double*)0; _ppvar = (Datum*)0; }
  _thread = _extcall_thread;
  _nt = nrn_threads;
 _r =  m_inf ( _p, _ppvar, _thread, _nt, *getarg(1) );
 hoc_retpushx(_r);
}
 
double h_inf ( _threadargsprotocomma_ double _lv ) {
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
 _r =  h_inf ( _p, _ppvar, _thread, _nt, *getarg(1) );
 hoc_retpushx(_r);
}
 
double window ( _threadargsprotocomma_ double _lv ) {
   double _lwindow;
 _lwindow = gnabar * pow( m_inf ( _threadargscomma_ _lv ) , 3.0 ) * h_inf ( _threadargscomma_ _lv ) * ( _lv - ena ) ;
   
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
 
/*CVODE ode begin*/
 static int _ode_spec1(double* _p, Datum* _ppvar, Datum* _thread, _NrnThread* _nt) {int _reset=0;{
 double b_flux, f_flux, _term; int _i;
 {int _i; for(_i=0;_i<5;_i++) _p[_dlist1[_i]] = 0.0;}
 /* COMPARTMENT diam * diam * PI / 4.0 {
   qna }
 */
 telspike ( _threadargs_ ) ;
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
 /* ~ qna < < ( - ina * PI * diam * ( 1e4 ) / FARADAY )*/
 f_flux = b_flux = 0.;
 Dqna += (b_flux =   ( - ina * PI * diam * ( 1e4 ) / FARADAY ) );
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
 /* COMPARTMENT diam * diam * PI / 4.0 {
 qna }
 */
 telspike ( _threadargs_ ) ;
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
 /* ~ qna < < ( - ina * PI * diam * ( 1e4 ) / FARADAY )*/
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
  ena = _ion_ena;
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
   nrn_update_ion_pointer(_na_sym, _ppvar, 0, 0);
   nrn_update_ion_pointer(_na_sym, _ppvar, 1, 3);
   nrn_update_ion_pointer(_na_sym, _ppvar, 2, 4);
 }

static void initmodel(double* _p, Datum* _ppvar, Datum* _thread, _NrnThread* _nt) {
  int _i; double _save;{
  hb = hb0;
  ha = ha0;
  mb = mb0;
  ma = ma0;
  qna = qna0;
 {
   ma = m_inf ( _threadargscomma_ v ) ;
   ha = h_inf ( _threadargscomma_ v ) ;
   mb = 1.0 - ma ;
   hb = 1.0 - ha ;
   freq = 0.0 ;
   n = 0.0 ;
   interval = 0.0 ;
   firing = 0.0 ;
   qna = 0.0 ;
   ina = gnabar * ma * ma * ma * ha * ( v - ena ) ;
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
 _check_h_a(_p, _ppvar, _thread, _nt);
 _check_h_b(_p, _ppvar, _thread, _nt);
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
  ena = _ion_ena;
 initmodel(_p, _ppvar, _thread, _nt);
 }
}

static double _nrn_current(double* _p, Datum* _ppvar, Datum* _thread, _NrnThread* _nt, double _v){double _current=0.;v=_v;{ {
   ina = gnabar * ma * ma * ma * ha * ( v - ena ) ;
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
  ena = _ion_ena;
 {  sparse_thread(&_thread[_spth1]._pvoid, 5, _slist1, _dlist1, _p, &t, dt, nastate, _linmat1, _ppvar, _thread, _nt);
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
   _t_m_a = makevector(302*sizeof(double));
   _t_m_b = makevector(302*sizeof(double));
   _t_h_a = makevector(302*sizeof(double));
   _t_h_b = makevector(302*sizeof(double));
 _slist1[0] = &(hb) - _p;  _dlist1[0] = &(Dhb) - _p;
 _slist1[1] = &(mb) - _p;  _dlist1[1] = &(Dmb) - _p;
 _slist1[2] = &(ha) - _p;  _dlist1[2] = &(Dha) - _p;
 _slist1[3] = &(ma) - _p;  _dlist1[3] = &(Dma) - _p;
 _slist1[4] = &(qna) - _p;  _dlist1[4] = &(Dqna) - _p;
_first = 0;
}

#if defined(__cplusplus)
} /* extern "C" */
#endif

#if NMODL_TEXT
static const char* nmodl_filename = "/home/kseniia/Documents/spreadingDepression/spreading-depression/na.mod";
static const char* nmodl_file_text = 
  "TITLE nachan\n"
  ": 29-07-01 update weer terug naar geleidbaarheden ipv\n"
  ": permeabiliteiten.\n"
  ": Natrium kanaal m^3*h \n"
  ":  \n"
  ": uit: Traub et al.\n"
  ": A branching dendritic model of a rodent CA3\n"
  ": pyramidal neurone.\n"
  "\n"
  "UNITS {\n"
  "	(mV) =	(millivolt)\n"
  "	(mA) =	(milliamp)\n"
  "}\n"
  "\n"
  "INDEPENDENT {t FROM 0 TO 1 WITH 100 (ms)}\n"
  "\n"
  "NEURON {\n"
  "	SUFFIX nachan\n"
  "	USEION na READ ena WRITE ina\n"
  "	RANGE gnabar, ina, interval, freq, n, firing, qna\n"
  "	GLOBAL shiftm, shifth, scaletaum, scaletauh\n"
  "}\n"
  "\n"
  "UNITS {\n"
  "	PI		= (pi) (1)\n"
  "	:FARADAY = 96520 (coul)\n"
  "	:R = 8.3134 (joule/degC)\n"
  "	:FARADAY	= (faraday) (coulomb)\n"
  "	FARADAY		= 96485.309 (coul)\n"
  "	R = (k-mole) (joule/degC)\n"
  "}\n"
  "\n"
  "PARAMETER {\n"
  "	celsius=36	(degC)\n"
  "	gnabar=1e-3	(mho/cm2)	: default max. perm.\n"
  "	shiftm=0	(mV)		: shift activatie\n"
  "	shifth=0	(mV)		: shift inactivatie\n"
  "	scaletaum=1	(mV)\n"
  "	scaletauh=1	(mV)\n"
  "}\n"
  "\n"
  "ASSIGNED { \n"
  "	ina	(mA/cm2)\n"
  "	v	(mV)\n"
  "	ena	(mV)\n"
  "	dt	(ms)\n"
  "	diam	(um)\n"
  "	freq\n"
  "	interval\n"
  "	n\n"
  "	firing\n"
  "}\n"
  "\n"
  "STATE { ma mb ha hb qna }		: fraction of states, ma=fraction in open state.\n"
  "\n"
  "BREAKPOINT {\n"
  "	SOLVE nastate METHOD sparse\n"
  "	ina = gnabar*ma*ma*ma*ha*(v-ena)\n"
  "}\n"
  "\n"
  "INITIAL {\n"
  "	ma=m_inf(v)\n"
  "	ha=h_inf(v)\n"
  "	mb=1-ma\n"
  "	hb=1-ha\n"
  "	freq = 0\n"
  "	n = 0\n"
  "	interval = 0\n"
  "	firing = 0\n"
  "	qna = 0\n"
  "	ina = gnabar*ma*ma*ma*ha*(v-ena)\n"
  "}\n"
  "\n"
  "LOCAL a1,a2,b1,b2\n"
  "\n"
  "KINETIC nastate {\n"
  "	COMPARTMENT diam*diam*PI/4 { qna }\n"
  "\n"
  "	telspike()\n"
  "	a1 = m_a(v)\n"
  "	a2 = m_b(v)\n"
  "	b1 = h_a(v)\n"
  "	b2 = h_b(v)\n"
  "	~ mb <-> ma (a1, a2)\n"
  "	~ hb <-> ha (b1, b2)\n"
  "	CONSERVE ma + mb = 1\n"
  "	CONSERVE ha + hb = 1\n"
  "	~ qna << (-ina*PI*diam*(1e4)/FARADAY)\n"
  "}\n"
  "\n"
  "PROCEDURE telspike() {\n"
  "	if ( (ma*ma*ma*ha >.01) && !firing ) {\n"
  "	  n=n+1\n"
  "	  if (n>1) {\n"
  "	    freq=1000/interval\n"
  "	  }\n"
  "	  firing=1\n"
  "	  interval=0\n"
  "	}\n"
  "	if ( (ma*ma*ma*ha <.01 ) && firing ) {\n"
  "	  firing = 0\n"
  "	}\n"
  "	interval = interval + dt/2\n"
  "}\n"
  "	\n"
  "FUNCTION m_a(v(mV)) {\n"
  "	TABLE DEPEND shiftm, scaletaum FROM -150 TO 150 WITH 301\n"
  "	m_a=scaletauh*0.32*(13.1-v-70-shiftm) / (exp((13.1-v-70-shiftm)/4)-1) :was scaletauh, fout dus\n"
  "}\n"
  "\n"
  "FUNCTION m_b(v(mV)) {\n"
  "	TABLE DEPEND shiftm, scaletaum FROM -150 TO 150 WITH 301\n"
  "	m_b=scaletaum*0.28*(v-40.1+70+shiftm)/(exp((v-40.1+70+shiftm)/5)-1)	\n"
  "}\n"
  "\n"
  "FUNCTION h_a(v(mV)) {\n"
  "	TABLE DEPEND shifth, scaletauh FROM -150 TO 150 WITH 301\n"
  "	h_a = scaletauh*0.128*exp((17-v-70-shifth)/18)\n"
  "}\n"
  "\n"
  "FUNCTION h_b(v(mV)) {\n"
  "	TABLE DEPEND shifth, scaletauh FROM -150 TO 150 WITH 301\n"
  "	h_b = scaletauh*4/(1+exp((40-v-70-shifth)/5))\n"
  "}\n"
  "\n"
  "FUNCTION m_inf(v(mV)) {\n"
  "	m_inf = m_a(v)/(m_a(v)+m_b(v))\n"
  "}\n"
  "\n"
  "FUNCTION h_inf(v(mV)) {\n"
  "	h_inf = h_a(v)/(h_a(v)+h_b(v))\n"
  "}\n"
  "\n"
  "FUNCTION window(v(mV)) {\n"
  "	window=gnabar*m_inf(v)^3*h_inf(v)*(v-ena)\n"
  "}\n"
  ;
#endif
