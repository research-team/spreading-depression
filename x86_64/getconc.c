/* Created by Language version: 7.7.0 */
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
 
#if METHOD3
extern int _method3;
#endif

#if !NRNGPU
#undef exp
#define exp hoc_Exp
extern double hoc_Exp(double);
#endif
 
#define nrn_init _nrn_init__getconc
#define _nrn_initial _nrn_initial__getconc
#define nrn_cur _nrn_cur__getconc
#define _nrn_current _nrn_current__getconc
#define nrn_jacob _nrn_jacob__getconc
#define nrn_state _nrn_state__getconc
#define _net_receive _net_receive__getconc 
 
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
#define nai _p[0]
#define Dnai _p[1]
#define nao _p[2]
#define Dnao _p[3]
#define ki _p[4]
#define Dki _p[5]
#define ko _p[6]
#define Dko _p[7]
#define cli _p[8]
#define Dcli _p[9]
#define clo _p[10]
#define Dclo _p[11]
#define ai _p[12]
#define Dai _p[13]
#define ao _p[14]
#define Dao _p[15]
#define _g _p[16]
#define _ion_nai	*_ppvar[0]._pval
#define _ion_nao	*_ppvar[1]._pval
#define _style_na	*((int*)_ppvar[2]._pvoid)
#define _ion_ki	*_ppvar[3]._pval
#define _ion_ko	*_ppvar[4]._pval
#define _style_k	*((int*)_ppvar[5]._pvoid)
#define _ion_cli	*_ppvar[6]._pval
#define _ion_clo	*_ppvar[7]._pval
#define _style_cl	*((int*)_ppvar[8]._pvoid)
#define _ion_ai	*_ppvar[9]._pval
#define _ion_ao	*_ppvar[10]._pval
#define _style_a	*((int*)_ppvar[11]._pvoid)
#define naig	*_ppvar[12]._pval
#define _p_naig	_ppvar[12]._pval
#define naog	*_ppvar[13]._pval
#define _p_naog	_ppvar[13]._pval
#define kig	*_ppvar[14]._pval
#define _p_kig	_ppvar[14]._pval
#define kog	*_ppvar[15]._pval
#define _p_kog	_ppvar[15]._pval
#define clig	*_ppvar[16]._pval
#define _p_clig	_ppvar[16]._pval
#define clog	*_ppvar[17]._pval
#define _p_clog	_ppvar[17]._pval
#define aig	*_ppvar[18]._pval
#define _p_aig	_ppvar[18]._pval
#define aog	*_ppvar[19]._pval
#define _p_aog	_ppvar[19]._pval
 
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
 static int hoc_nrnpointerindex =  12;
 /* external NEURON variables */
 /* declaration of user functions */
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
 "setdata_getconc", _hoc_setdata,
 0, 0
};
 /* declare global and static user variables */
 /* some parameters have upper and lower limits */
 static HocParmLimits _hoc_parm_limits[] = {
 0,0,0
};
 static HocParmUnits _hoc_parm_units[] = {
 0,0
};
 static double ao0 = 0;
 static double ai0 = 0;
 static double clo0 = 0;
 static double cli0 = 0;
 static double ko0 = 0;
 static double ki0 = 0;
 static double nao0 = 0;
 static double nai0 = 0;
 static double v = 0;
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
 /* connect range variables in _p that hoc is supposed to know about */
 static const char *_mechanism[] = {
 "7.7.0",
"getconc",
 0,
 0,
 0,
 "naig_getconc",
 "naog_getconc",
 "kig_getconc",
 "kog_getconc",
 "clig_getconc",
 "clog_getconc",
 "aig_getconc",
 "aog_getconc",
 0};
 static Symbol* _na_sym;
 static Symbol* _k_sym;
 static Symbol* _cl_sym;
 static Symbol* _a_sym;
 
extern Prop* need_memb(Symbol*);

static void nrn_alloc(Prop* _prop) {
	Prop *prop_ion;
	double *_p; Datum *_ppvar;
 	_p = nrn_prop_data_alloc(_mechtype, 17, _prop);
 	/*initialize range parameters*/
 	_prop->param = _p;
 	_prop->param_size = 17;
 	_ppvar = nrn_prop_datum_alloc(_mechtype, 20, _prop);
 	_prop->dparam = _ppvar;
 	/*connect ionic variables to this model*/
 prop_ion = need_memb(_na_sym);
 nrn_check_conc_write(_prop, prop_ion, 1);
 nrn_check_conc_write(_prop, prop_ion, 0);
 nrn_promote(prop_ion, 3, 0);
 	_ppvar[0]._pval = &prop_ion->param[1]; /* nai */
 	_ppvar[1]._pval = &prop_ion->param[2]; /* nao */
 	_ppvar[2]._pvoid = (void*)(&(prop_ion->dparam[0]._i)); /* iontype for na */
 prop_ion = need_memb(_k_sym);
 nrn_check_conc_write(_prop, prop_ion, 1);
 nrn_check_conc_write(_prop, prop_ion, 0);
 nrn_promote(prop_ion, 3, 0);
 	_ppvar[3]._pval = &prop_ion->param[1]; /* ki */
 	_ppvar[4]._pval = &prop_ion->param[2]; /* ko */
 	_ppvar[5]._pvoid = (void*)(&(prop_ion->dparam[0]._i)); /* iontype for k */
 prop_ion = need_memb(_cl_sym);
 nrn_check_conc_write(_prop, prop_ion, 1);
 nrn_check_conc_write(_prop, prop_ion, 0);
 nrn_promote(prop_ion, 3, 0);
 	_ppvar[6]._pval = &prop_ion->param[1]; /* cli */
 	_ppvar[7]._pval = &prop_ion->param[2]; /* clo */
 	_ppvar[8]._pvoid = (void*)(&(prop_ion->dparam[0]._i)); /* iontype for cl */
 prop_ion = need_memb(_a_sym);
 nrn_check_conc_write(_prop, prop_ion, 1);
 nrn_check_conc_write(_prop, prop_ion, 0);
 nrn_promote(prop_ion, 3, 0);
 	_ppvar[9]._pval = &prop_ion->param[1]; /* ai */
 	_ppvar[10]._pval = &prop_ion->param[2]; /* ao */
 	_ppvar[11]._pvoid = (void*)(&(prop_ion->dparam[0]._i)); /* iontype for a */
 
}
 static void _initlists();
 static void _update_ion_pointer(Datum*);
 extern Symbol* hoc_lookup(const char*);
extern void _nrn_thread_reg(int, int, void(*)(Datum*));
extern void _nrn_thread_table_reg(int, void(*)(double*, Datum*, Datum*, _NrnThread*, int));
extern void hoc_register_tolerance(int, HocStateTolerance*, Symbol***);
extern void _cvode_abstol( Symbol**, double*, int);

 void _getconc_reg() {
	int _vectorized = 0;
  _initlists();
 	ion_reg("na", -10000.);
 	ion_reg("k", -10000.);
 	ion_reg("cl", -10000.);
 	ion_reg("a", -10000.);
 	_na_sym = hoc_lookup("na_ion");
 	_k_sym = hoc_lookup("k_ion");
 	_cl_sym = hoc_lookup("cl_ion");
 	_a_sym = hoc_lookup("a_ion");
 	register_mech(_mechanism, nrn_alloc,nrn_cur, nrn_jacob, nrn_state, nrn_init, hoc_nrnpointerindex, 0);
 _mechtype = nrn_get_mechtype(_mechanism[1]);
     _nrn_setdata_reg(_mechtype, _setdata);
     _nrn_thread_reg(_mechtype, 2, _update_ion_pointer);
 #if NMODL_TEXT
  hoc_reg_nmodl_text(_mechtype, nmodl_file_text);
  hoc_reg_nmodl_filename(_mechtype, nmodl_filename);
#endif
  hoc_register_prop_size(_mechtype, 17, 20);
  hoc_register_dparam_semantics(_mechtype, 0, "na_ion");
  hoc_register_dparam_semantics(_mechtype, 1, "na_ion");
  hoc_register_dparam_semantics(_mechtype, 2, "#na_ion");
  hoc_register_dparam_semantics(_mechtype, 3, "k_ion");
  hoc_register_dparam_semantics(_mechtype, 4, "k_ion");
  hoc_register_dparam_semantics(_mechtype, 5, "#k_ion");
  hoc_register_dparam_semantics(_mechtype, 6, "cl_ion");
  hoc_register_dparam_semantics(_mechtype, 7, "cl_ion");
  hoc_register_dparam_semantics(_mechtype, 8, "#cl_ion");
  hoc_register_dparam_semantics(_mechtype, 9, "a_ion");
  hoc_register_dparam_semantics(_mechtype, 10, "a_ion");
  hoc_register_dparam_semantics(_mechtype, 11, "#a_ion");
  hoc_register_dparam_semantics(_mechtype, 12, "pointer");
  hoc_register_dparam_semantics(_mechtype, 13, "pointer");
  hoc_register_dparam_semantics(_mechtype, 14, "pointer");
  hoc_register_dparam_semantics(_mechtype, 15, "pointer");
  hoc_register_dparam_semantics(_mechtype, 16, "pointer");
  hoc_register_dparam_semantics(_mechtype, 17, "pointer");
  hoc_register_dparam_semantics(_mechtype, 18, "pointer");
  hoc_register_dparam_semantics(_mechtype, 19, "pointer");
 	nrn_writes_conc(_mechtype, 0);
 	hoc_register_var(hoc_scdoub, hoc_vdoub, hoc_intfunc);
 	ivoc_help("help ?1 getconc /home/kseniia/Documents/spreadingDepression/spreading-depression/x86_64/getconc.mod\n");
 hoc_register_limits(_mechtype, _hoc_parm_limits);
 hoc_register_units(_mechtype, _hoc_parm_units);
 }
static int _reset;
static char *modelname = "";

static int error;
static int _ninits = 0;
static int _match_recurse=1;
static void _modl_cleanup(){ _match_recurse=1;}
 extern void nrn_update_ion_pointer(Symbol*, Datum*, int, int);
 static void _update_ion_pointer(Datum* _ppvar) {
   nrn_update_ion_pointer(_na_sym, _ppvar, 0, 1);
   nrn_update_ion_pointer(_na_sym, _ppvar, 1, 2);
   nrn_update_ion_pointer(_k_sym, _ppvar, 3, 1);
   nrn_update_ion_pointer(_k_sym, _ppvar, 4, 2);
   nrn_update_ion_pointer(_cl_sym, _ppvar, 6, 1);
   nrn_update_ion_pointer(_cl_sym, _ppvar, 7, 2);
   nrn_update_ion_pointer(_a_sym, _ppvar, 9, 1);
   nrn_update_ion_pointer(_a_sym, _ppvar, 10, 2);
 }

static void initmodel() {
  int _i; double _save;_ninits++;
{
 {
   at_time ( nrn_threads, t ) ;
   {
     nai = naig ;
     nao = naog ;
     ki = kig ;
     ko = kog ;
     cli = clig ;
     clo = clog ;
     ai = aig ;
     ao = aog ;
     }
   }

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
  nai = _ion_nai;
  nao = _ion_nao;
  ki = _ion_ki;
  ko = _ion_ko;
  cli = _ion_cli;
  clo = _ion_clo;
  ai = _ion_ai;
  ao = _ion_ao;
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
}}

static double _nrn_current(double _v){double _current=0.;v=_v;{
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
  nai = _ion_nai;
  nao = _ion_nao;
  ki = _ion_ki;
  ko = _ion_ko;
  cli = _ion_cli;
  clo = _ion_clo;
  ai = _ion_ai;
  ao = _ion_ao;
 {
   nai = naig ;
   nao = naog ;
   ki = kig ;
   ko = kog ;
   cli = clig ;
   clo = clog ;
   ai = aig ;
   ao = aog ;
   }
  _ion_nai = nai;
  _ion_nao = nao;
  _ion_ki = ki;
  _ion_ko = ko;
  _ion_cli = cli;
  _ion_clo = clo;
  _ion_ai = ai;
  _ion_ao = ao;
}}

}

static void terminal(){}

static void _initlists() {
 int _i; static int _first = 1;
  if (!_first) return;
_first = 0;
}

#if NMODL_TEXT
static const char* nmodl_filename = "/home/kseniia/Documents/spreadingDepression/spreading-depression/getconc.mod";
static const char* nmodl_file_text = 
  "NEURON {\n"
  "	SUFFIX getconc\n"
  "	USEION na WRITE nai, nao\n"
  "	USEION  k WRITE  ki,  ko\n"
  "	USEION cl WRITE cli, clo\n"
  "	USEION  a WRITE  ai,  ao\n"
  "	POINTER naig, naog, kig, kog, clig, clog, aig, aog\n"
  "}\n"
  "\n"
  "ASSIGNED {\n"
  "	naig naog kig kog clig clog aig aog\n"
  "}\n"
  "\n"
  "STATE { nai nao ki ko cli clo ai ao }\n"
  "\n"
  "BREAKPOINT {\n"
  "	:at_time(t) {\n"
  "	  nai=naig nao=naog ki=kig ko=kog\n"
  "	  cli=clig clo=clog ai=aig ao=aog\n"
  "	:}\n"
  "\n"
  "}\n"
  "INITIAL {\n"
  "	at_time(t) {\n"
  "	  nai=naig nao=naog ki=kig ko=kog\n"
  "	  cli=clig clo=clog ai=aig ao=aog\n"
  "	}\n"
  "}\n"
  ;
#endif
