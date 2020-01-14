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
 
#define nrn_init _nrn_init__xiong
#define _nrn_initial _nrn_initial__xiong
#define nrn_cur _nrn_cur__xiong
#define _nrn_current _nrn_current__xiong
#define nrn_jacob _nrn_jacob__xiong
#define nrn_state _nrn_state__xiong
#define _net_receive _net_receive__xiong 
#define gatestate gatestate__xiong 
 
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
#define g _p[0]
#define ina _p[1]
#define ik _p[2]
#define gpresent _p[3]
#define itot _p[4]
#define m _p[5]
#define ena _p[6]
#define ek _p[7]
#define cao _p[8]
#define ki _p[9]
#define ko _p[10]
#define nai _p[11]
#define nao _p[12]
#define Dm _p[13]
#define v _p[14]
#define _g _p[15]
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
#define _ion_cao	*_ppvar[10]._pval
 
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
 static void _hoc_hill(void);
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
 "setdata_xiong", _hoc_setdata,
 "efun_xiong", _hoc_efun,
 "ghk_xiong", _hoc_ghk,
 "hill_xiong", _hoc_hill,
 0, 0
};
#define _f_hill _f_hill_xiong
#define efun efun_xiong
#define ghk ghk_xiong
#define hill hill_xiong
 extern double _f_hill( _threadargsprotocomma_ double );
 extern double efun( _threadargsprotocomma_ double );
 extern double ghk( _threadargsprotocomma_ double , double , double );
 extern double hill( _threadargsprotocomma_ double );
 
static void _check_hill(double*, Datum*, Datum*, _NrnThread*); 
static void _check_table_thread(double* _p, Datum* _ppvar, Datum* _thread, _NrnThread* _nt, int _type) {
   _check_hill(_p, _ppvar, _thread, _nt);
 }
 /* declare global and static user variables */
#define Nh Nh_xiong
 double Nh = 1.4;
#define ec50 ec50_xiong
 double ec50 = 0.145;
#define n n_xiong
 double n = 4;
#define rmax rmax_xiong
 double rmax = 1;
#define tau_act tau_act_xiong
 double tau_act = 992;
#define tau_ina tau_ina_xiong
 double tau_ina = 100;
#define tauavg tauavg_xiong
 double tauavg = 300;
#define usetable usetable_xiong
 double usetable = 1;
 /* some parameters have upper and lower limits */
 static HocParmLimits _hoc_parm_limits[] = {
 "usetable_xiong", 0, 1,
 0,0,0
};
 static HocParmUnits _hoc_parm_units[] = {
 "tau_ina_xiong", "ms",
 "tau_act_xiong", "ms",
 "ec50_xiong", "mM",
 "tauavg_xiong", "ms",
 "g_xiong", "mho/cm2",
 "ina_xiong", "mA/cm2",
 "ik_xiong", "mA/cm2",
 0,0
};
 static double delta_t = 0.01;
 static double m0 = 0;
 /* connect global user variables to hoc */
 static DoubScal hoc_scdoub[] = {
 "tau_ina_xiong", &tau_ina_xiong,
 "tau_act_xiong", &tau_act_xiong,
 "rmax_xiong", &rmax_xiong,
 "ec50_xiong", &ec50_xiong,
 "Nh_xiong", &Nh_xiong,
 "n_xiong", &n_xiong,
 "tauavg_xiong", &tauavg_xiong,
 "usetable_xiong", &usetable_xiong,
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
 
#define _cvode_ieq _ppvar[11]._i
 static void _ode_matsol_instance1(_threadargsproto_);
 /* connect range variables in _p that hoc is supposed to know about */
 static const char *_mechanism[] = {
 "7.7.0",
"xiong",
 "g_xiong",
 0,
 "ina_xiong",
 "ik_xiong",
 "gpresent_xiong",
 "itot_xiong",
 0,
 "m_xiong",
 0,
 0};
 static Symbol* _k_sym;
 static Symbol* _na_sym;
 static Symbol* _ca_sym;
 
extern Prop* need_memb(Symbol*);

static void nrn_alloc(Prop* _prop) {
	Prop *prop_ion;
	double *_p; Datum *_ppvar;
 	_p = nrn_prop_data_alloc(_mechtype, 16, _prop);
 	/*initialize range parameters*/
 	g = 0.001;
 	_prop->param = _p;
 	_prop->param_size = 16;
 	_ppvar = nrn_prop_datum_alloc(_mechtype, 12, _prop);
 	_prop->dparam = _ppvar;
 	/*connect ionic variables to this model*/
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
 nrn_promote(prop_ion, 1, 0);
 	_ppvar[10]._pval = &prop_ion->param[2]; /* cao */
 
}
 static void _initlists();
  /* some states have an absolute tolerance */
 static Symbol** _atollist;
 static HocStateTolerance _hoc_state_tol[] = {
 0,0
};
 static void _update_ion_pointer(Datum*);
 extern Symbol* hoc_lookup(const char*);
extern void _nrn_thread_reg(int, int, void(*)(Datum*));
extern void _nrn_thread_table_reg(int, void(*)(double*, Datum*, Datum*, _NrnThread*, int));
extern void hoc_register_tolerance(int, HocStateTolerance*, Symbol***);
extern void _cvode_abstol( Symbol**, double*, int);

 void _xiong_reg() {
	int _vectorized = 1;
  _initlists();
 	ion_reg("k", -10000.);
 	ion_reg("na", -10000.);
 	ion_reg("ca", -10000.);
 	_k_sym = hoc_lookup("k_ion");
 	_na_sym = hoc_lookup("na_ion");
 	_ca_sym = hoc_lookup("ca_ion");
 	register_mech(_mechanism, nrn_alloc,nrn_cur, nrn_jacob, nrn_state, nrn_init, hoc_nrnpointerindex, 1);
 _mechtype = nrn_get_mechtype(_mechanism[1]);
     _nrn_setdata_reg(_mechtype, _setdata);
     _nrn_thread_reg(_mechtype, 2, _update_ion_pointer);
     _nrn_thread_table_reg(_mechtype, _check_table_thread);
 #if NMODL_TEXT
  hoc_reg_nmodl_text(_mechtype, nmodl_file_text);
  hoc_reg_nmodl_filename(_mechtype, nmodl_filename);
#endif
  hoc_register_prop_size(_mechtype, 16, 12);
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
  hoc_register_dparam_semantics(_mechtype, 11, "cvodeieq");
 	hoc_register_cvode(_mechtype, _ode_count, _ode_map, _ode_spec, _ode_matsol);
 	hoc_register_tolerance(_mechtype, _hoc_state_tol, &_atollist);
 	hoc_register_var(hoc_scdoub, hoc_vdoub, hoc_intfunc);
 	ivoc_help("help ?1 xiong /home/kseniia/Documents/spreadingDepression/spreading-depression/x86_64/xiong.mod\n");
 hoc_register_limits(_mechtype, _hoc_parm_limits);
 hoc_register_units(_mechtype, _hoc_parm_units);
 }
 static double FARADAY = 96485.3;
 static double R = 8.3145;
 static double *_t_hill;
static int _reset;
static char *modelname = "xiong";

static int error;
static int _ninits = 0;
static int _match_recurse=1;
static void _modl_cleanup(){ _match_recurse=1;}
 
static int _ode_spec1(_threadargsproto_);
/*static int _ode_matsol1(_threadargsproto_);*/
 static double _n_hill(_threadargsprotocomma_ double _lv);
 static int _slist1[1], _dlist1[1];
 static int gatestate(_threadargsproto_);
 
/*CVODE*/
 static int _ode_spec1 (double* _p, Datum* _ppvar, Datum* _thread, _NrnThread* _nt) {int _reset = 0; {
   Dm = ( ( hill ( _threadargscomma_ cao ) - m ) / tauavg ) ;
   }
 return _reset;
}
 static int _ode_matsol1 (double* _p, Datum* _ppvar, Datum* _thread, _NrnThread* _nt) {
 Dm = Dm  / (1. - dt*( ( ( ( ( - 1.0 ) ) ) / tauavg ) )) ;
  return 0;
}
 /*END CVODE*/
 static int gatestate (double* _p, Datum* _ppvar, Datum* _thread, _NrnThread* _nt) { {
    m = m + (1. - exp(dt*(( ( ( ( - 1.0 ) ) ) / tauavg ))))*(- ( ( ( ( hill ( _threadargscomma_ cao ) ) ) / tauavg ) ) / ( ( ( ( ( - 1.0 ) ) ) / tauavg ) ) - m) ;
   }
  return 0;
}
 static double _mfac_hill, _tmin_hill;
  static void _check_hill(double* _p, Datum* _ppvar, Datum* _thread, _NrnThread* _nt) {
  static int _maktable=1; int _i, _j, _ix = 0;
  double _xi, _tmax;
  static double _sav_rmax;
  static double _sav_ec50;
  static double _sav_Nh;
  static double _sav_n;
  if (!usetable) {return;}
  if (_sav_rmax != rmax) { _maktable = 1;}
  if (_sav_ec50 != ec50) { _maktable = 1;}
  if (_sav_Nh != Nh) { _maktable = 1;}
  if (_sav_n != n) { _maktable = 1;}
  if (_maktable) { double _x, _dx; _maktable=0;
   _tmin_hill =  0.0 ;
   _tmax =  15.0 ;
   _dx = (_tmax - _tmin_hill)/150.; _mfac_hill = 1./_dx;
   for (_i=0, _x=_tmin_hill; _i < 151; _x += _dx, _i++) {
    _t_hill[_i] = _f_hill(_p, _ppvar, _thread, _nt, _x);
   }
   _sav_rmax = rmax;
   _sav_ec50 = ec50;
   _sav_Nh = Nh;
   _sav_n = n;
  }
 }

 double hill(double* _p, Datum* _ppvar, Datum* _thread, _NrnThread* _nt, double _lco) { 
#if 0
_check_hill(_p, _ppvar, _thread, _nt);
#endif
 return _n_hill(_p, _ppvar, _thread, _nt, _lco);
 }

 static double _n_hill(double* _p, Datum* _ppvar, Datum* _thread, _NrnThread* _nt, double _lco){ int _i, _j;
 double _xi, _theta;
 if (!usetable) {
 return _f_hill(_p, _ppvar, _thread, _nt, _lco); 
}
 _xi = _mfac_hill * (_lco - _tmin_hill);
 if (isnan(_xi)) {
  return _xi; }
 if (_xi <= 0.) {
 return _t_hill[0];
 }
 if (_xi >= 150.) {
 return _t_hill[150];
 }
 _i = (int) _xi;
 return _t_hill[_i] + (_xi - (double)_i)*(_t_hill[_i+1] - _t_hill[_i]);
 }

 
double _f_hill ( _threadargsprotocomma_ double _lco ) {
   double _lhill;
 _lhill = pow( ( rmax / ( 1.0 + pow( ( _lco / ec50 ) , Nh ) ) ) , ( 1.0 / n ) ) ;
   
return _lhill;
 }
 
static void _hoc_hill(void) {
  double _r;
   double* _p; Datum* _ppvar; Datum* _thread; _NrnThread* _nt;
   if (_extcall_prop) {_p = _extcall_prop->param; _ppvar = _extcall_prop->dparam;}else{ _p = (double*)0; _ppvar = (Datum*)0; }
  _thread = _extcall_thread;
  _nt = nrn_threads;
 
#if 1
 _check_hill(_p, _ppvar, _thread, _nt);
#endif
 _r =  hill ( _p, _ppvar, _thread, _nt, *getarg(1) );
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
 
static int _ode_count(int _type){ return 1;}
 
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
  cao = _ion_cao;
     _ode_spec1 (_p, _ppvar, _thread, _nt);
   }}
 
static void _ode_map(int _ieq, double** _pv, double** _pvdot, double* _pp, Datum* _ppd, double* _atol, int _type) { 
	double* _p; Datum* _ppvar;
 	int _i; _p = _pp; _ppvar = _ppd;
	_cvode_ieq = _ieq;
	for (_i=0; _i < 1; ++_i) {
		_pv[_i] = _pp + _slist1[_i];  _pvdot[_i] = _pp + _dlist1[_i];
		_cvode_abstol(_atollist, _atol, _i);
	}
 }
 
static void _ode_matsol_instance1(_threadargsproto_) {
 _ode_matsol1 (_p, _ppvar, _thread, _nt);
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
  cao = _ion_cao;
 _ode_matsol_instance1(_threadargs_);
 }}
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
   nrn_update_ion_pointer(_ca_sym, _ppvar, 10, 2);
 }

static void initmodel(double* _p, Datum* _ppvar, Datum* _thread, _NrnThread* _nt) {
  int _i; double _save;{
  m = m0;
 {
   m = hill ( _threadargscomma_ cao ) ;
   gpresent = g * pow( m , n ) ;
   ina = gpresent * ( v - ena ) ;
   ik = gpresent * ( v - ek ) ;
   itot = ik + ina ;
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
 _check_hill(_p, _ppvar, _thread, _nt);
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
  cao = _ion_cao;
 initmodel(_p, _ppvar, _thread, _nt);
  }
}

static double _nrn_current(double* _p, Datum* _ppvar, Datum* _thread, _NrnThread* _nt, double _v){double _current=0.;v=_v;{ {
   gpresent = g * pow( m , n ) ;
   ina = gpresent * ( v - ena ) ;
   ik = gpresent * ( v - ek ) ;
   itot = ik + ina ;
   }
 _current += ik;
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
  ki = _ion_ki;
  ek = _ion_ek;
  nai = _ion_nai;
  nao = _ion_nao;
  ena = _ion_ena;
  cao = _ion_cao;
 _g = _nrn_current(_p, _ppvar, _thread, _nt, _v + .001);
 	{ double _dina;
 double _dik;
  _dik = ik;
  _dina = ina;
 _rhs = _nrn_current(_p, _ppvar, _thread, _nt, _v);
  _ion_dikdv += (_dik - ik)/.001 ;
  _ion_dinadv += (_dina - ina)/.001 ;
 	}
 _g = (_g - _rhs)/.001;
  _ion_ik += ik ;
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
  cao = _ion_cao;
 {   gatestate(_p, _ppvar, _thread, _nt);
  }  }}

}

static void terminal(){}

static void _initlists(){
 double _x; double* _p = &_x;
 int _i; static int _first = 1;
  if (!_first) return;
 _slist1[0] = &(m) - _p;  _dlist1[0] = &(Dm) - _p;
   _t_hill = makevector(151*sizeof(double));
_first = 0;
}

#if defined(__cplusplus)
} /* extern "C" */
#endif

#if NMODL_TEXT
static const char* nmodl_filename = "/home/kseniia/Documents/spreadingDepression/spreading-depression/xiong.mod";
static const char* nmodl_file_text = 
  "TITLE xiong\n"
  "\n"
  "COMMENT\n"
  "Extracellular concentrations of Ca21 change\n"
  "rapidly and transiently in the brain during excitatory synaptic\n"
  "activity. To test whether such changes in Ca21 can play a\n"
  "signaling role we examined the effects of rapidly lowering\n"
  "Ca21 on the excitability of acutely isolated CA1 and cultured\n"
  "hippocampal neurons. Reducing Ca21 excited and depolarized\n"
  "neurons by activating a previously undescribed nonselective\n"
  "cation channel. This channel had a single-channel conductance\n"
  "of 36 pS, and its frequency of opening was inversely\n"
  "proportional to the concentration of Ca21. The inhibition of\n"
  "gating of this channel was sensitive to ionic strength but\n"
  "independent of membrane potential. The ability of this channel\n"
  "to sense Ca21 provides a novel mechanism whereby\n"
  "neurons can respond to alterations in the extracellular concentration\n"
  "of this key signaling ion.\n"
  "uit: \n"
  "Proc. Natl. Acad. Sci. USA\n"
  "Vol. 94, pp. 7012 7017, June 1997\n"
  "Neurobiology\n"
  "Extracellular calcium sensed by a novel cation channel in\n"
  "hippocampal neurons\n"
  "Z.-G. XIONG, W.-Y. LU, AND J. F. MACDONALD\n"
  "\n"
  "ENDCOMMENT\n"
  "\n"
  "NEURON {\n"
  "	SUFFIX xiong\n"
  "	USEION k READ ko, ki, ek WRITE ik\n"
  "	USEION na READ nai, nao, ena WRITE ina\n"
  "	USEION ca READ cao\n"
  "	GLOBAL tauavg, rmax, ec50, Nh, n\n"
  "	RANGE ik, ina, g, gpresent, itot\n"
  "}\n"
  "\n"
  "UNITS {\n"
  "	(molar) = 	(1/liter)\n"
  "	(mV) =	(millivolt)\n"
  "	(mA) =	(milliamp)\n"
  "	(mM) =	(millimolar)\n"
  "	FARADAY	= (faraday) (coulomb)\n"
  "	:FARADAY		= 96485.309 (coul)\n"
  "	R = (k-mole) (joule/degC)\n"
  "}\n"
  "\n"
  ":INDEPENDENT {t FROM 0 TO 1 WITH 100 (ms)}\n"
  "\n"
  "PARAMETER {\n"
  "	celsius		(degC)\n"
  "	g=1e-3	(mho/cm2)\n"
  "	tau_ina=100	(ms)\n"
  "	tau_act=992	(ms)\n"
  "	rmax=1\n"
  "	ec50=.145	(mM) : 1/2 - max. dosage: was .39 in eerste artikel xiong. deze waarde komt uit vervolg studie met lamotrigine uit 2001\n"
  "	Nh=1.4		: hill coefficient\n"
  "	n=4		: gates voor asymmetrie in tau's\n"
  "	tauavg=300	(ms) : jbf-tau, ziet er aardig uit.\n"
  "}\n"
  "\n"
  "ASSIGNED { \n"
  "	v	(mV)	\n"
  "	ina	(mA/cm2)\n"
  "	ik	(mA/cm2)\n"
  "	ena	(mV)\n"
  "	ek	(mV)\n"
  "	cao	(mM)\n"
  "	ki\n"
  "	ko\n"
  "	nai\n"
  "	nao\n"
  "	gpresent\n"
  "	itot\n"
  "}\n"
  "\n"
  "STATE { m }\n"
  "\n"
  "BREAKPOINT {\n"
  "	SOLVE gatestate METHOD cnexp\n"
  "	gpresent=g*m^n\n"
  "	ina = gpresent*(v-ena)\n"
  "	ik = gpresent*(v-ek)\n"
  "	itot=ik+ina\n"
  "}\n"
  "\n"
  "INITIAL {\n"
  "	m=hill(cao)\n"
  "	gpresent=g*m^n\n"
  "	ina = gpresent*(v-ena)\n"
  "	ik = gpresent*(v-ek)\n"
  "	itot=ik+ina\n"
  "}\n"
  "\n"
  "DERIVATIVE gatestate {\n"
  "	m' = ( (hill(cao)-m)/tauavg )\n"
  "}\n"
  "\n"
  "FUNCTION hill(co) {\n"
  "	TABLE DEPEND rmax, ec50, Nh, n FROM 0 TO 15 WITH 150\n"
  "	hill = (rmax/(1+(co/ec50)^Nh))^(1/n)\n"
  "}\n"
  "\n"
  "FUNCTION ghk(v(mV), ci(mM), co(mM)) (.001 coul/cm3) {\n"
  "	LOCAL z, eci, eco\n"
  "	z = (1e-3)*1*FARADAY*v/(R*(celsius+273.11247574))\n"
  "	eco = co*efun(z)\n"
  "	eci = ci*efun(-z)\n"
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
