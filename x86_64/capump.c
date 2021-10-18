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
 
#define nrn_init _nrn_init__capump
#define _nrn_initial _nrn_initial__capump
#define nrn_cur _nrn_cur__capump
#define _nrn_current _nrn_current__capump
#define nrn_jacob _nrn_jacob__capump
#define nrn_state _nrn_state__capump
#define _net_receive _net_receive__capump 
 
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
#define scale _p[0]
#define ica _p[1]
#define cai _p[2]
#define _g _p[3]
#define _ion_cai	*_ppvar[0]._pval
#define _ion_ica	*_ppvar[1]._pval
#define _ion_dicadv	*_ppvar[2]._pval
 
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
 /* external NEURON variables */
 /* declaration of user functions */
 static void _hoc_pumprate(void);
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
 "setdata_capump", _hoc_setdata,
 "pumprate_capump", _hoc_pumprate,
 0, 0
};
#define pumprate pumprate_capump
 extern double pumprate( double );
 /* declare global and static user variables */
#define Km Km_capump
 double Km = 0.0069;
#define Vconv Vconv_capump
 double Vconv = 0;
#define Vmax Vmax_capump
 double Vmax = 352;
#define carest carest_capump
 double carest = 0;
#define hill hill_capump
 double hill = 1;
#define vol_surf_ratio vol_surf_ratio_capump
 double vol_surf_ratio = 1.85;
 /* some parameters have upper and lower limits */
 static HocParmLimits _hoc_parm_limits[] = {
 0,0,0
};
 static HocParmUnits _hoc_parm_units[] = {
 "Vmax_capump", "uM/s",
 "vol_surf_ratio_capump", "um",
 "Km_capump", "mM",
 "ica_capump", "mA/cm2",
 0,0
};
 static double v = 0;
 /* connect global user variables to hoc */
 static DoubScal hoc_scdoub[] = {
 "Vmax_capump", &Vmax_capump,
 "vol_surf_ratio_capump", &vol_surf_ratio_capump,
 "Km_capump", &Km_capump,
 "hill_capump", &hill_capump,
 "Vconv_capump", &Vconv_capump,
 "carest_capump", &carest_capump,
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
"capump",
 "scale_capump",
 0,
 "ica_capump",
 0,
 0,
 0};
 static Symbol* _ca_sym;
 
extern Prop* need_memb(Symbol*);

static void nrn_alloc(Prop* _prop) {
	Prop *prop_ion;
	double *_p; Datum *_ppvar;
 	_p = nrn_prop_data_alloc(_mechtype, 4, _prop);
 	/*initialize range parameters*/
 	scale = 0.0001;
 	_prop->param = _p;
 	_prop->param_size = 4;
 	_ppvar = nrn_prop_datum_alloc(_mechtype, 3, _prop);
 	_prop->dparam = _ppvar;
 	/*connect ionic variables to this model*/
 prop_ion = need_memb(_ca_sym);
 nrn_promote(prop_ion, 1, 0);
 	_ppvar[0]._pval = &prop_ion->param[1]; /* cai */
 	_ppvar[1]._pval = &prop_ion->param[3]; /* ica */
 	_ppvar[2]._pval = &prop_ion->param[4]; /* _ion_dicadv */
 
}
 static void _initlists();
 static void _update_ion_pointer(Datum*);
 extern Symbol* hoc_lookup(const char*);
extern void _nrn_thread_reg(int, int, void(*)(Datum*));
extern void _nrn_thread_table_reg(int, void(*)(double*, Datum*, Datum*, _NrnThread*, int));
extern void hoc_register_tolerance(int, HocStateTolerance*, Symbol***);
extern void _cvode_abstol( Symbol**, double*, int);

 void _capump_reg() {
	int _vectorized = 0;
  _initlists();
 	ion_reg("ca", -10000.);
 	_ca_sym = hoc_lookup("ca_ion");
 	register_mech(_mechanism, nrn_alloc,nrn_cur, nrn_jacob, nrn_state, nrn_init, hoc_nrnpointerindex, 0);
 _mechtype = nrn_get_mechtype(_mechanism[1]);
     _nrn_setdata_reg(_mechtype, _setdata);
     _nrn_thread_reg(_mechtype, 2, _update_ion_pointer);
 #if NMODL_TEXT
  hoc_reg_nmodl_text(_mechtype, nmodl_file_text);
  hoc_reg_nmodl_filename(_mechtype, nmodl_filename);
#endif
  hoc_register_prop_size(_mechtype, 4, 3);
  hoc_register_dparam_semantics(_mechtype, 0, "ca_ion");
  hoc_register_dparam_semantics(_mechtype, 1, "ca_ion");
  hoc_register_dparam_semantics(_mechtype, 2, "ca_ion");
 	hoc_register_var(hoc_scdoub, hoc_vdoub, hoc_intfunc);
 	ivoc_help("help ?1 capump /home/kseniia/Documents/spreadingDepression/spreading-depression/x86_64/capump.mod\n");
 hoc_register_limits(_mechtype, _hoc_parm_limits);
 hoc_register_units(_mechtype, _hoc_parm_units);
 }
 static double FARADAY = 96485.3;
static int _reset;
static char *modelname = "calcium pump ";

static int error;
static int _ninits = 0;
static int _match_recurse=1;
static void _modl_cleanup(){ _match_recurse=1;}
 
double pumprate (  double _lci ) {
   double _lpumprate;
 Vconv = Vmax * vol_surf_ratio * FARADAY * 2.0 * ( 1e-4 ) ;
   if ( fabs ( _lci - carest ) < 1e-7 ) {
     _lpumprate = ( _lci - carest ) * Vconv / Km ;
     }
   else {
     _lpumprate = Vconv / ( 1.0 + Km / ( _lci - carest ) ) ;
     }
   
return _lpumprate;
 }
 
static void _hoc_pumprate(void) {
  double _r;
   _r =  pumprate (  *getarg(1) );
 hoc_retpushx(_r);
}
 extern void nrn_update_ion_pointer(Symbol*, Datum*, int, int);
 static void _update_ion_pointer(Datum* _ppvar) {
   nrn_update_ion_pointer(_ca_sym, _ppvar, 0, 1);
   nrn_update_ion_pointer(_ca_sym, _ppvar, 1, 3);
   nrn_update_ion_pointer(_ca_sym, _ppvar, 2, 4);
 }

static void initmodel() {
  int _i; double _save;_ninits++;
{
 {
   
/*VERBATIM*/
	cai = _ion_cai;
	carest = _ion_cai;
 ica = pumprate ( _threadargscomma_ cai ) * scale ;
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
  cai = _ion_cai;
 initmodel();
 }}

static double _nrn_current(double _v){double _current=0.;v=_v;{ {
   ica = pumprate ( _threadargscomma_ cai ) * scale ;
   }
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
  cai = _ion_cai;
 _g = _nrn_current(_v + .001);
 	{ double _dica;
  _dica = ica;
 _rhs = _nrn_current(_v);
  _ion_dicadv += (_dica - ica)/.001 ;
 	}
 _g = (_g - _rhs)/.001;
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

}

static void terminal(){}

static void _initlists() {
 int _i; static int _first = 1;
  if (!_first) return;
_first = 0;
}

#if NMODL_TEXT
static const char* nmodl_filename = "/home/kseniia/Documents/spreadingDepression/spreading-depression/capump.mod";
static const char* nmodl_file_text = 
  "TITLE calcium pump \n"
  "COMMENT\n"
  "uit aren borgdorff's proefschrift pagina 30:\n"
  "V(ca2+i)=Vmax/(1+Km/Ca2+)^h\n"
  "met Vmax = 352uM/s, Km = 6.9 uM and h=1.1\n"
  "\n"
  "zie parameters ook in PARAMETER-box\n"
  "pomp uit granule cellen met gemiddelde diam= 11.1 +/- 0.15 um\n"
  "Om de granule cel-specifieke waarde Voor Vmax te gebruiken in \n"
  "een CA1 cel moet het omgezet worden in algemenere eenheid, nl.\n"
  "van uM/s naar i/um2:\n"
  "\n"
  "diam was 11.1 um -> r=5.55 um ->\n"
  "opp=387 um en inhoud = 716 um3, -> inhoud/opp = r/3 = 1.85 um\n"
  "\n"
  "\n"
  "\n"
  "ENDCOMMENT\n"
  "\n"
  "NEURON {\n"
  "	SUFFIX capump\n"
  "	USEION ca READ cai WRITE ica	\n"
  "	RANGE ica, scale\n"
  "	GLOBAL Vmax, Km, hill, Vconv, carest\n"
  "}\n"
  "\n"
  "UNITS {\n"
  "	(mA) = (milliamp)\n"
  "	(mV) = (millivolt)\n"
  "	FARADAY = (faraday) (coulombs)\n"
  "\n"
  "}\n"
  "\n"
  "PARAMETER {\n"
  "	Vmax = 352 (uM/s) 		: units of Borgdorff\n"
  "	vol_surf_ratio = 1.85 (um) 	: assume r=5.55 um and sphere\n"
  "	Km = .0069 (mM)			: 6.9 uM\n"
  "	hill = 1			: hill is 1.1, no significant diff from 1\n"
  "	scale = 1e-4\n"
  "}\n"
  "\n"
  "ASSIGNED {\n"
  "	ica (mA/cm2)\n"
  "        cai (mM) \n"
  "	Vconv\n"
  "	carest\n"
  "}\n"
  "\n"
  "INITIAL {\n"
  "	VERBATIM\n"
  "	cai = _ion_cai;\n"
  "	carest = _ion_cai;\n"
  "	ENDVERBATIM\n"
  "	ica =  pumprate(cai)*scale	\n"
  "}\n"
  "\n"
  "BREAKPOINT {\n"
  "	ica =  pumprate(cai)*scale\n"
  "}\n"
  "\n"
  "FUNCTION pumprate (ci) {\n"
  "	Vconv = Vmax*vol_surf_ratio*FARADAY*2*(1e-4)\n"
  "	if (fabs(ci-carest) < 1e-7) {\n"
  "	  pumprate = (ci-carest)*Vconv/Km\n"
  "	}else{\n"
  "	  pumprate = Vconv/(1+Km/(ci-carest))\n"
  "	}\n"
  "}\n"
  ;
#endif
