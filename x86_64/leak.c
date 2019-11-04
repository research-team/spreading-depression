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
 
#define nrn_init _nrn_init__leak
#define _nrn_initial _nrn_initial__leak
#define nrn_cur _nrn_cur__leak
#define _nrn_current _nrn_current__leak
#define nrn_jacob _nrn_jacob__leak
#define nrn_state _nrn_state__leak
#define _net_receive _net_receive__leak 
#define integreer integreer__leak 
#define stromen stromen__leak 
 
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
#define gk _p[0]
#define gna _p[1]
#define gcl _p[2]
#define ga _p[3]
#define ik _p[4]
#define ina _p[5]
#define icl _p[6]
#define ia _p[7]
#define qk _p[8]
#define qna _p[9]
#define qcl _p[10]
#define qa _p[11]
#define ek _p[12]
#define ena _p[13]
#define ecl _p[14]
#define ea _p[15]
#define Dqk _p[16]
#define Dqna _p[17]
#define Dqcl _p[18]
#define Dqa _p[19]
#define v _p[20]
#define _g _p[21]
#define _ion_ek	*_ppvar[0]._pval
#define _ion_ik	*_ppvar[1]._pval
#define _ion_dikdv	*_ppvar[2]._pval
#define _ion_ena	*_ppvar[3]._pval
#define _ion_ina	*_ppvar[4]._pval
#define _ion_dinadv	*_ppvar[5]._pval
#define _ion_ecl	*_ppvar[6]._pval
#define _ion_icl	*_ppvar[7]._pval
#define _ion_dicldv	*_ppvar[8]._pval
#define _ion_ea	*_ppvar[9]._pval
#define _ion_ia	*_ppvar[10]._pval
#define _ion_diadv	*_ppvar[11]._pval
#define diam	*_ppvar[12]._pval
 
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
 /* declaration of user functions */
 static void _hoc_itot(void);
 static void _hoc_stromen(void);
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
 "setdata_leak", _hoc_setdata,
 "itot_leak", _hoc_itot,
 "stromen_leak", _hoc_stromen,
 0, 0
};
#define itot itot_leak
 extern double itot( _threadargsprotocomma_ double );
 /* declare global and static user variables */
 /* some parameters have upper and lower limits */
 static HocParmLimits _hoc_parm_limits[] = {
 0,0,0
};
 static HocParmUnits _hoc_parm_units[] = {
 "gk_leak", "mho/cm2",
 "gna_leak", "mho/cm2",
 "gcl_leak", "mho/cm2",
 "ga_leak", "mho/cm2",
 "ik_leak", "mA/cm2",
 "ina_leak", "mA/cm2",
 "icl_leak", "mA/cm2",
 "ia_leak", "mA/cm2",
 0,0
};
 static double delta_t = 0.01;
 static double qa0 = 0;
 static double qcl0 = 0;
 static double qna0 = 0;
 static double qk0 = 0;
 /* connect global user variables to hoc */
 static DoubScal hoc_scdoub[] = {
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
 
#define _cvode_ieq _ppvar[13]._i
 static void _ode_matsol_instance1(_threadargsproto_);
 /* connect range variables in _p that hoc is supposed to know about */
 static const char *_mechanism[] = {
 "7.5.0",
"leak",
 "gk_leak",
 "gna_leak",
 "gcl_leak",
 "ga_leak",
 0,
 "ik_leak",
 "ina_leak",
 "icl_leak",
 "ia_leak",
 0,
 "qk_leak",
 "qna_leak",
 "qcl_leak",
 "qa_leak",
 0,
 0};
 static Symbol* _morphology_sym;
 static Symbol* _k_sym;
 static Symbol* _na_sym;
 static Symbol* _cl_sym;
 static Symbol* _a_sym;
 
extern Prop* need_memb(Symbol*);

static void nrn_alloc(Prop* _prop) {
	Prop *prop_ion;
	double *_p; Datum *_ppvar;
 	_p = nrn_prop_data_alloc(_mechtype, 22, _prop);
 	/*initialize range parameters*/
 	gk = 1e-05;
 	gna = 1e-05;
 	gcl = 0.0001;
 	ga = 0;
 	_prop->param = _p;
 	_prop->param_size = 22;
 	_ppvar = nrn_prop_datum_alloc(_mechtype, 14, _prop);
 	_prop->dparam = _ppvar;
 	/*connect ionic variables to this model*/
 prop_ion = need_memb(_morphology_sym);
 	_ppvar[12]._pval = &prop_ion->param[0]; /* diam */
 prop_ion = need_memb(_k_sym);
 nrn_promote(prop_ion, 0, 1);
 	_ppvar[0]._pval = &prop_ion->param[0]; /* ek */
 	_ppvar[1]._pval = &prop_ion->param[3]; /* ik */
 	_ppvar[2]._pval = &prop_ion->param[4]; /* _ion_dikdv */
 prop_ion = need_memb(_na_sym);
 nrn_promote(prop_ion, 0, 1);
 	_ppvar[3]._pval = &prop_ion->param[0]; /* ena */
 	_ppvar[4]._pval = &prop_ion->param[3]; /* ina */
 	_ppvar[5]._pval = &prop_ion->param[4]; /* _ion_dinadv */
 prop_ion = need_memb(_cl_sym);
 nrn_promote(prop_ion, 0, 1);
 	_ppvar[6]._pval = &prop_ion->param[0]; /* ecl */
 	_ppvar[7]._pval = &prop_ion->param[3]; /* icl */
 	_ppvar[8]._pval = &prop_ion->param[4]; /* _ion_dicldv */
 prop_ion = need_memb(_a_sym);
 nrn_promote(prop_ion, 0, 1);
 	_ppvar[9]._pval = &prop_ion->param[0]; /* ea */
 	_ppvar[10]._pval = &prop_ion->param[3]; /* ia */
 	_ppvar[11]._pval = &prop_ion->param[4]; /* _ion_diadv */
 
}
 static void _initlists();
  /* some states have an absolute tolerance */
 static Symbol** _atollist;
 static HocStateTolerance _hoc_state_tol[] = {
 0,0
};
 static void _thread_cleanup(Datum*);
 static void _update_ion_pointer(Datum*);
 extern Symbol* hoc_lookup(const char*);
extern void _nrn_thread_reg(int, int, void(*)(Datum*));
extern void _nrn_thread_table_reg(int, void(*)(double*, Datum*, Datum*, _NrnThread*, int));
extern void hoc_register_tolerance(int, HocStateTolerance*, Symbol***);
extern void _cvode_abstol( Symbol**, double*, int);

 void _leak_reg() {
	int _vectorized = 1;
  _initlists();
 	ion_reg("k", -10000.);
 	ion_reg("na", -10000.);
 	ion_reg("cl", -1.0);
 	ion_reg("a", -1.0);
 	_morphology_sym = hoc_lookup("morphology");
 	_k_sym = hoc_lookup("k_ion");
 	_na_sym = hoc_lookup("na_ion");
 	_cl_sym = hoc_lookup("cl_ion");
 	_a_sym = hoc_lookup("a_ion");
 	register_mech(_mechanism, nrn_alloc,nrn_cur, nrn_jacob, nrn_state, nrn_init, hoc_nrnpointerindex, 3);
  _extcall_thread = (Datum*)ecalloc(2, sizeof(Datum));
 _mechtype = nrn_get_mechtype(_mechanism[1]);
     _nrn_setdata_reg(_mechtype, _setdata);
     _nrn_thread_reg(_mechtype, 0, _thread_cleanup);
     _nrn_thread_reg(_mechtype, 2, _update_ion_pointer);
  hoc_register_prop_size(_mechtype, 22, 14);
  hoc_register_dparam_semantics(_mechtype, 0, "k_ion");
  hoc_register_dparam_semantics(_mechtype, 1, "k_ion");
  hoc_register_dparam_semantics(_mechtype, 2, "k_ion");
  hoc_register_dparam_semantics(_mechtype, 3, "na_ion");
  hoc_register_dparam_semantics(_mechtype, 4, "na_ion");
  hoc_register_dparam_semantics(_mechtype, 5, "na_ion");
  hoc_register_dparam_semantics(_mechtype, 6, "cl_ion");
  hoc_register_dparam_semantics(_mechtype, 7, "cl_ion");
  hoc_register_dparam_semantics(_mechtype, 8, "cl_ion");
  hoc_register_dparam_semantics(_mechtype, 9, "a_ion");
  hoc_register_dparam_semantics(_mechtype, 10, "a_ion");
  hoc_register_dparam_semantics(_mechtype, 11, "a_ion");
  hoc_register_dparam_semantics(_mechtype, 13, "cvodeieq");
  hoc_register_dparam_semantics(_mechtype, 12, "diam");
 	hoc_register_cvode(_mechtype, _ode_count, _ode_map, _ode_spec, _ode_matsol);
 	hoc_register_tolerance(_mechtype, _hoc_state_tol, &_atollist);
 	hoc_register_var(hoc_scdoub, hoc_vdoub, hoc_intfunc);
 	ivoc_help("help ?1 leak /Users/sulgod/spreading-depression/x86_64/leak.mod\n");
 hoc_register_limits(_mechtype, _hoc_parm_limits);
 hoc_register_units(_mechtype, _hoc_parm_units);
 }
 static double PI = 3.14159;
 static double FARADAY = 96485.309;
static int _reset;
static char *modelname = "leak";

static int error;
static int _ninits = 0;
static int _match_recurse=1;
static void _modl_cleanup(){ _match_recurse=1;}
static int stromen(_threadargsproto_);
 extern double *_nrn_thread_getelm();
 
#define _MATELM1(_row,_col) *(_nrn_thread_getelm(_so, _row + 1, _col + 1))
 
#define _RHS1(_arg) _rhs[_arg+1]
  
#define _linmat1  1
 static int _spth1 = 1;
 static int _cvspth1 = 0;
 
static int _ode_spec1(_threadargsproto_);
/*static int _ode_matsol1(_threadargsproto_);*/
 static int _slist1[4], _dlist1[4]; static double *_temp1;
 static int integreer();
 
static int integreer (void* _so, double* _rhs, double* _p, Datum* _ppvar, Datum* _thread, _NrnThread* _nt)
 {int _reset=0;
 {
   double b_flux, f_flux, _term; int _i;
 {int _i; double _dt1 = 1.0/dt;
for(_i=0;_i<4;_i++){
  	_RHS1(_i) = -_dt1*(_p[_slist1[_i]] - _p[_dlist1[_i]]);
	_MATELM1(_i, _i) = _dt1;
      
}  
_RHS1(0) *= ( diam * diam * PI / 4.0) ;
_MATELM1(0, 0) *= ( diam * diam * PI / 4.0); 
_RHS1(1) *= ( diam * diam * PI / 4.0) ;
_MATELM1(1, 1) *= ( diam * diam * PI / 4.0); 
_RHS1(2) *= ( diam * diam * PI / 4.0) ;
_MATELM1(2, 2) *= ( diam * diam * PI / 4.0); 
_RHS1(3) *= ( diam * diam * PI / 4.0) ;
_MATELM1(3, 3) *= ( diam * diam * PI / 4.0);  }
 /* COMPARTMENT diam * diam * PI / 4.0 {
     qna qk qcl qa }
   */
 /* ~ qna < < ( ( - ina * diam ) * PI * ( 1e4 ) / FARADAY )*/
 f_flux = b_flux = 0.;
 _RHS1( 2) += (b_flux =   ( ( - ina * diam ) * PI * ( 1e4 ) / FARADAY ) );
 /*FLUX*/
  /* ~ qk < < ( ( - ik * diam ) * PI * ( 1e4 ) / FARADAY )*/
 f_flux = b_flux = 0.;
 _RHS1( 3) += (b_flux =   ( ( - ik * diam ) * PI * ( 1e4 ) / FARADAY ) );
 /*FLUX*/
  /* ~ qcl < < ( ( - icl * diam ) * PI * ( 1e4 ) / FARADAY )*/
 f_flux = b_flux = 0.;
 _RHS1( 1) += (b_flux =   ( ( - icl * diam ) * PI * ( 1e4 ) / FARADAY ) );
 /*FLUX*/
  /* ~ qa < < ( ( - ia * diam ) * PI * ( 1e4 ) / FARADAY )*/
 f_flux = b_flux = 0.;
 _RHS1( 0) += (b_flux =   ( ( - ia * diam ) * PI * ( 1e4 ) / FARADAY ) );
 /*FLUX*/
    } return _reset;
 }
 
double itot ( _threadargsprotocomma_ double _lv ) {
   double _litot;
 _litot = gk * ( _lv - ek ) + gna * ( _lv - ena ) + gcl * ( _lv - ecl ) + ga * ( _lv - ea ) ;
   
return _litot;
 }
 
static void _hoc_itot(void) {
  double _r;
   double* _p; Datum* _ppvar; Datum* _thread; _NrnThread* _nt;
   if (_extcall_prop) {_p = _extcall_prop->param; _ppvar = _extcall_prop->dparam;}else{ _p = (double*)0; _ppvar = (Datum*)0; }
  _thread = _extcall_thread;
  _nt = nrn_threads;
 _r =  itot ( _p, _ppvar, _thread, _nt, *getarg(1) );
 hoc_retpushx(_r);
}
 
static int  stromen ( _threadargsproto_ ) {
    return 0; }
 
static void _hoc_stromen(void) {
  double _r;
   double* _p; Datum* _ppvar; Datum* _thread; _NrnThread* _nt;
   if (_extcall_prop) {_p = _extcall_prop->param; _ppvar = _extcall_prop->dparam;}else{ _p = (double*)0; _ppvar = (Datum*)0; }
  _thread = _extcall_thread;
  _nt = nrn_threads;
 _r = 1.;
 stromen ( _p, _ppvar, _thread, _nt );
 hoc_retpushx(_r);
}
 
/*CVODE ode begin*/
 static int _ode_spec1(double* _p, Datum* _ppvar, Datum* _thread, _NrnThread* _nt) {int _reset=0;{
 double b_flux, f_flux, _term; int _i;
 {int _i; for(_i=0;_i<4;_i++) _p[_dlist1[_i]] = 0.0;}
 /* COMPARTMENT diam * diam * PI / 4.0 {
   qna qk qcl qa }
 */
 /* ~ qna < < ( ( - ina * diam ) * PI * ( 1e4 ) / FARADAY )*/
 f_flux = b_flux = 0.;
 Dqna += (b_flux =   ( ( - ina * diam ) * PI * ( 1e4 ) / FARADAY ) );
 /*FLUX*/
  /* ~ qk < < ( ( - ik * diam ) * PI * ( 1e4 ) / FARADAY )*/
 f_flux = b_flux = 0.;
 Dqk += (b_flux =   ( ( - ik * diam ) * PI * ( 1e4 ) / FARADAY ) );
 /*FLUX*/
  /* ~ qcl < < ( ( - icl * diam ) * PI * ( 1e4 ) / FARADAY )*/
 f_flux = b_flux = 0.;
 Dqcl += (b_flux =   ( ( - icl * diam ) * PI * ( 1e4 ) / FARADAY ) );
 /*FLUX*/
  /* ~ qa < < ( ( - ia * diam ) * PI * ( 1e4 ) / FARADAY )*/
 f_flux = b_flux = 0.;
 Dqa += (b_flux =   ( ( - ia * diam ) * PI * ( 1e4 ) / FARADAY ) );
 /*FLUX*/
  _p[_dlist1[0]] /= ( diam * diam * PI / 4.0);
 _p[_dlist1[1]] /= ( diam * diam * PI / 4.0);
 _p[_dlist1[2]] /= ( diam * diam * PI / 4.0);
 _p[_dlist1[3]] /= ( diam * diam * PI / 4.0);
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
      
}  
_RHS1(0) *= ( diam * diam * PI / 4.0) ;
_MATELM1(0, 0) *= ( diam * diam * PI / 4.0); 
_RHS1(1) *= ( diam * diam * PI / 4.0) ;
_MATELM1(1, 1) *= ( diam * diam * PI / 4.0); 
_RHS1(2) *= ( diam * diam * PI / 4.0) ;
_MATELM1(2, 2) *= ( diam * diam * PI / 4.0); 
_RHS1(3) *= ( diam * diam * PI / 4.0) ;
_MATELM1(3, 3) *= ( diam * diam * PI / 4.0);  }
 /* COMPARTMENT diam * diam * PI / 4.0 {
 qna qk qcl qa }
 */
 /* ~ qna < < ( ( - ina * diam ) * PI * ( 1e4 ) / FARADAY )*/
 /*FLUX*/
  /* ~ qk < < ( ( - ik * diam ) * PI * ( 1e4 ) / FARADAY )*/
 /*FLUX*/
  /* ~ qcl < < ( ( - icl * diam ) * PI * ( 1e4 ) / FARADAY )*/
 /*FLUX*/
  /* ~ qa < < ( ( - ia * diam ) * PI * ( 1e4 ) / FARADAY )*/
 /*FLUX*/
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
  ek = _ion_ek;
  ena = _ion_ena;
  ecl = _ion_ecl;
  ea = _ion_ea;
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
  ek = _ion_ek;
  ena = _ion_ena;
  ecl = _ion_ecl;
  ea = _ion_ea;
 _ode_matsol_instance1(_threadargs_);
 }}
 
static void _thread_cleanup(Datum* _thread) {
   _nrn_destroy_sparseobj_thread(_thread[_cvspth1]._pvoid);
   _nrn_destroy_sparseobj_thread(_thread[_spth1]._pvoid);
 }
 extern void nrn_update_ion_pointer(Symbol*, Datum*, int, int);
 static void _update_ion_pointer(Datum* _ppvar) {
   nrn_update_ion_pointer(_k_sym, _ppvar, 0, 0);
   nrn_update_ion_pointer(_k_sym, _ppvar, 1, 3);
   nrn_update_ion_pointer(_k_sym, _ppvar, 2, 4);
   nrn_update_ion_pointer(_na_sym, _ppvar, 3, 0);
   nrn_update_ion_pointer(_na_sym, _ppvar, 4, 3);
   nrn_update_ion_pointer(_na_sym, _ppvar, 5, 4);
   nrn_update_ion_pointer(_cl_sym, _ppvar, 6, 0);
   nrn_update_ion_pointer(_cl_sym, _ppvar, 7, 3);
   nrn_update_ion_pointer(_cl_sym, _ppvar, 8, 4);
   nrn_update_ion_pointer(_a_sym, _ppvar, 9, 0);
   nrn_update_ion_pointer(_a_sym, _ppvar, 10, 3);
   nrn_update_ion_pointer(_a_sym, _ppvar, 11, 4);
 }

static void initmodel(double* _p, Datum* _ppvar, Datum* _thread, _NrnThread* _nt) {
  int _i; double _save;{
  qa = qa0;
  qcl = qcl0;
  qna = qna0;
  qk = qk0;
 {
   ik = gk * ( v - ek ) ;
   ina = gna * ( v - ena ) ;
   icl = gcl * ( v - ecl ) ;
   ia = ga * ( v - ea ) ;
   qk = 0.0 ;
   qna = 0.0 ;
   qcl = 0.0 ;
   qa = 0.0 ;
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
  ena = _ion_ena;
  ecl = _ion_ecl;
  ea = _ion_ea;
 initmodel(_p, _ppvar, _thread, _nt);
    }
}

static double _nrn_current(double* _p, Datum* _ppvar, Datum* _thread, _NrnThread* _nt, double _v){double _current=0.;v=_v;{ {
   ik = gk * ( v - ek ) ;
   ina = gna * ( v - ena ) ;
   icl = gcl * ( v - ecl ) ;
   ia = ga * ( v - ea ) ;
   }
 _current += ik;
 _current += ina;
 _current += icl;
 _current += ia;

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
  ena = _ion_ena;
  ecl = _ion_ecl;
  ea = _ion_ea;
 _g = _nrn_current(_p, _ppvar, _thread, _nt, _v + .001);
 	{ double _dia;
 double _dicl;
 double _dina;
 double _dik;
  _dik = ik;
  _dina = ina;
  _dicl = icl;
  _dia = ia;
 _rhs = _nrn_current(_p, _ppvar, _thread, _nt, _v);
  _ion_dikdv += (_dik - ik)/.001 ;
  _ion_dinadv += (_dina - ina)/.001 ;
  _ion_dicldv += (_dicl - icl)/.001 ;
  _ion_diadv += (_dia - ia)/.001 ;
 	}
 _g = (_g - _rhs)/.001;
  _ion_ik += ik ;
  _ion_ina += ina ;
  _ion_icl += icl ;
  _ion_ia += ia ;
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
  ena = _ion_ena;
  ecl = _ion_ecl;
  ea = _ion_ea;
 {  sparse_thread(&_thread[_spth1]._pvoid, 4, _slist1, _dlist1, _p, &t, dt, integreer, _linmat1, _ppvar, _thread, _nt);
     if (secondorder) {
    int _i;
    for (_i = 0; _i < 4; ++_i) {
      _p[_slist1[_i]] += dt*_p[_dlist1[_i]];
    }}
 }    }}
 dt = _dtsav;
}

static void terminal(){}

static void _initlists(){
 double _x; double* _p = &_x;
 int _i; static int _first = 1;
  if (!_first) return;
 _slist1[0] = &(qa) - _p;  _dlist1[0] = &(Dqa) - _p;
 _slist1[1] = &(qcl) - _p;  _dlist1[1] = &(Dqcl) - _p;
 _slist1[2] = &(qna) - _p;  _dlist1[2] = &(Dqna) - _p;
 _slist1[3] = &(qk) - _p;  _dlist1[3] = &(Dqk) - _p;
_first = 0;
}

#if defined(__cplusplus)
} /* extern "C" */
#endif
