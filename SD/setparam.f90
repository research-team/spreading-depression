! setparam.f90

!----------------------------------
! set default values for parameters
!----------------------------------

subroutine SetDefaults

use global
implicit none

tSetFlux=.FALSE.
tATP=.FALSE.
tCa=.FALSE.
tFlagCells=.FALSE.
lusedelta=.TRUE.
luseCa=.TRUE.
latp=1
lvaryKR=0

irunno=0
npresteps=500
npreca=1000
npreiter=1
startup='ATP'
startATP=500.0D0
startCa=-1.0D0
startIP3=0.0D0
startVmem=-1.0D0
startperiod=-1.0D0
startcellx=0
startcelly=0

nxsteps=9
nysteps=9
nzsteps=9
deltax=5.0D0
deltay=5.0D0
deltaz=5.0D0
ncell=3
nblock=10
diffATP=300.0D0
vmaxraw=1D-16
Krel=0.2D0
ATP0=0.0D0
VATPase=100.0D0
KATPase=100.0D0
kATPloss=0.3D0
Ca00=0.05D0		! same as background
IP300=0.01D0		! ditto
ATP00=0.0D0		! ditto
GFrac0=0.0D0
timestep = 0.01D0
endtime = 10.0D0
movietime=-1.0D0

! IP3 generation

Kc=0.4D0		! Lemon value
cIP30=0.01D0		! Lemon/Fink value
diffIP3=280.0D0		! Hoefer
kdeg=1.25D0		! Lemon value
!rhraw=7.7D-16		! Deduced from Lemon...
rhraw=7.7D-11		! ...and corrected because I left out G0
KG=8.82D0		! Deduced from Lemon
KR=5.0D0		! Lemon value
altKR=5.0D0
KRg=5.0D0		! for the sake of argument
gapIP3=0.0D0	! for backwards compatibility
rhrawd=0.0D0	! for backwards compatibility
			! but my estimate from Hoefer is 1.25D-16
Kcd=0.3D0		! Ca dissociation constant

! calcium release from E.R.

Ca0=0.05D0
CaER=400.0D0		! Fink value
B_over_K=40.0D0		! Fink value
KI=0.03D0		! Fink value
Kact=0.17D0		! Fink value
Jmax=2880.0D0		! Fink value
ERVmax=10.0D0		! Bill value; Fink value=5.85
Kpump=0.24D0		! Fink value
Kinh=0.1D0		! Fink value
kon=2.0D0		! Bill value; Fink value=8.0

call ISetDefaults
end subroutine SetDefaults

!---------------------------------------------------
! read in override values and do some precomputation
!---------------------------------------------------

subroutine NextBatch
use global
use ionglob
implicit none
integer :: MallocError,lowx,lowy,lowz,mcell
double precision :: term1,term2,term3,Jchannel,Jpump,multdelta
logical :: odd

namelist/IN/irunno,npresteps,npreca,npreiter,tSetFlux,tATP,tCa,tFlagCells,	&
	lusedelta,luseCa,kATPloss,latp,lvaryKR,altKR,KRg,	&
	deltax,deltay,deltaz,timestep,endtime,movietime,iontimeratio,	&
	nxsteps,nysteps,nzsteps,ncell,nblock,	&
	diffATP,VATPase,KATPase,vmaxraw,Krel,	&
	Ca0,CaER,B_over_K,KI,Kact,Jmax,ERVmax,Kpump,	&
	Kinh,kon,Kc,cIP30,diffIP3,kdeg,rhraw,gapIP3,rhrawd,Kcd,	&
	KG,KR,Ca00,IP300,ATP00,ATP0,GFrac0, &
	startup,startATP,startCa,startVmem,startIP3, &
	startperiod,startcellx,startcelly,	&
	glut0,neuglurate,astglurate,gluuptrate,	&
	Cmem,Rmem,epsA,epsN,volareaA,volareaN,CaBuffFact,	&
	KA0,KN0,KI0,NaA0,NaN0,NaI0,CaA0,CaN0,CaI0,ClA0,ClN0,ClI0,VmA0,VmN0,	&
	gKDRA,gBKA,gKirA,gKAA,gKMA,gSKA,gIKA,gNaFA,gNaPA,gCaLVAA,gCaHVAA,	&
	gKDRN,gBKN,      gKAN,gKMN,gSKN,gIKN,gNaFN,gNaPN,gCaLVAN,gCaHVAN,	&
	NMDAopen,NMDAclose,gKNaCaN,	&
	rClA,rCaA,rNaKA,rNaCaA,gKClA,gNaKClA,	&
	rClN,rCaN,rNaKN,rNaCaN,gKClN,multdelta

multdelta=1.0D0

read(10,IN)

nTsteps = int(endtime / (2.0D0 * timestep))
timebit=0.5D0/timestep
twostep=2.0D0*timestep

! For the moment we have only one layout

lxsymm=.FALSE.	! because of asymmetry of neuronal glutamate release/reception
lysymm=.TRUE.
lzsymm=.TRUE.
startcelly=0;

if (lvaryKR.and.latp.GT.4) THEN
	write(*,*)'Bodged vKR will not work'
	stop
elseif (lvaryKR.GT.2) THEN
	write(*,*)'Bad lvaryKR:',lvaryKR
	stop
endif

rh=rhraw*1D15/deltax		! assume deltax=deltay for moment
vmax=vmaxraw*1D15/deltax
rhd=rhrawd*1D15/deltax

if (lusedelta) then
	delta=(kdeg*cIP30-rhd*Ca0**2/(Kcd**2+Ca0**2))/rh
	if (luseCa) delta=delta*(Kc+Ca0)/Ca0
	delta=delta*ncell/6

delta=delta*multdelta

!would have been better delta=delta*(ncell/6)/(1-2/ncell)
!or delta=delta*ncell/(6-12/ncell+8/(ncell*ncell))

	delta=KG*delta/(1.0D0-delta)	! multiplier 0.975D0?
	if (delta.lt.0.0D0) then
		write(*,*)'Bad delta',delta
		stop
	else
		write(*,*)'delta=',delta
		write(*,*)'G*0=',delta/(KG+delta)

	endif
else
	delta=0.0D0
endif

! allocate arrays
! Note anything contributing to ATP release must exist at N+1
! to prevent errors. This includes AStore, Ca, IP3.
!
! AStore	-nxsteps-1:nxsteps+1	-nysteps-1:nysteps+1	-nzsteps-1:nzsteps+1
! ATP		-1:nxsteps+1		-1:nysteps+1		-1:nzsteps+1
! IP3
! Ca
! icell
! PeakCa
! PeakTime
!
! flx		-nxsteps-1:nxsteps	-nysteps:nysteps		-nzsteps:nzsteps
!		-1:nxsteps			0:nysteps			0:nzsteps
!
! fly		-nxsteps:nxsteps		-nysteps-1:nysteps	-nzsteps:nzsteps
!		0:nxsteps			-1:nysteps			0:nzsteps
!
! flz		-nxsteps:nxsteps		-nysteps:nysteps		-nzsteps-1:nzsteps
!		0:nxsteps			0:nysteps			-1:nzsteps+1
!
! sumfl		-nxsteps:nxsteps		-nysteps:nysteps		-nzsteps:nzsteps
! H		0:nxsteps			0:nysteps			0:nzsteps

mcell=(ncell-1)/2
lowx=-nxsteps
lowy=-nysteps
lowz=-nzsteps

if (lxsymm) then
	lowx=0
endif
if (lysymm) then
	lowy=0
endif
if (lzsymm) then
	lowz=0
endif

allocate (AStore(lowx-1:nxsteps+1,lowy-1:nysteps+1,lowz-1:nzsteps+1),STAT=MAllocError)
call testalloc(MAllocError)
allocate (ATP(lowx-1:nxsteps+1,lowy-1:nysteps+1,lowz-1:nzsteps+1),STAT=MAllocError)
call testalloc(MAllocError)
allocate (IP3(lowx-1:nxsteps+1,lowy-1:nysteps+1,lowz-1:nzsteps+1),STAT=MAllocError)
call testalloc(MAllocError)
allocate (flx(lowx-1:nxsteps,lowy:nysteps,lowz:nzsteps),STAT=MAllocError)
call testalloc(MAllocError)
allocate (fly(lowx:nxsteps,lowy-1:nysteps,lowz:nzsteps),STAT=MAllocError)
call testalloc(MAllocError)
allocate (flz(lowx:nxsteps,lowy:nysteps,lowz-1:nzsteps),STAT=MAllocError)
call testalloc(MAllocError)
allocate (sumfl(lowx:nxsteps,lowy:nysteps,lowz:nzsteps),STAT=MAllocError)
call testalloc(MAllocError)
allocate (Ca(lowx-1:nxsteps+1,lowy-1:nysteps+1,lowz-1:nzsteps+1),STAT=MAllocError)
call testalloc(MAllocError)
allocate (H(lowx:nxsteps,lowy:nysteps,lowz:nzsteps),STAT=MAllocError)
call testalloc(MAllocError)
allocate (icell(lowx-1:nxsteps+1,lowy-1:nysteps+1,lowz-1:nzsteps+1),STAT=MAllocError)
call testalloc(MAllocError)

if (lvaryKR.GT.0) then
	allocate (vKR(lowx:nxsteps,lowy:nysteps),STAT=MAllocError)
	call testalloc(MAllocError)
endif
allocate (gapterm(lowx-1:nxsteps+1,lowy-1:nysteps+1),STAT=MAllocError)
call testalloc(MAllocError)

! calcium-related

h0=Kinh/(Ca0+Kinh)

term1=cIP30/(cIP30+KI)
term2=Ca0/(Ca0+Kact)
term3=1.0D0-Ca0/CaER
Jchannel=Jmax*(term1*term2*h0)**3*term3	! initial IP3 channel release rate
Jpump=ERVmax*Ca0**2/(Ca0**2+Kpump**2);	! initial ER pumping rate
ERLeak=(Jpump-Jchannel)/term3;		! leak rate constant
if (ERLeak.LT.0.0D0) THEN
	write(*,*)'Bad leak rate:',ERLeak
	stop
endif

beta=1.0D0/(1.0D0+B_over_K)

call INextBatch
end subroutine NextBatch

!--------------------------------------------------------
! Error reporting routine after dynamic memory allocation
!--------------------------------------------------------

subroutine testalloc(MAllocError)

implicit none
integer :: MAllocError
if (MAllocError>0) then
   write(*,*)'Error in memory allocation to array.'
   stop
endif

end subroutine testalloc

!-------------------------------
! Deallocate memory between runs
!-------------------------------
subroutine EndBatch
use global
implicit none
deallocate (AStore)
deallocate (ATP)
deallocate (IP3)
deallocate (flx)
deallocate (fly)
deallocate (flz)
deallocate (sumfl)
deallocate (Ca)
deallocate (H)
deallocate (icell)

if (lvaryKR.GT.0) then
	deallocate (vKR)
endif
deallocate (gapterm)

call IEndBatch
endsubroutine EndBatch

