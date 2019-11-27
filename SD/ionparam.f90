! ionparam.f90

!----------------------------------
! set default values for parameters
!----------------------------------

subroutine ISetDefaults

use ionglob
implicit none
double precision :: xR,xT,xF,xxx

iontimeratio=100

xR=8.3145D0		! gas constant (J/mol/K)
xT=310.15D0		! temperature (K)
xF=96480.0D0	! Faraday constant (C/mol)

RTF=xR*xT/xF	! J/C = V
RTF=RTF*1000.0D0	! mV

! volume ratios

epsA=1.5D0
epsN=2.5D0
volareaA=3.59D0	! Dronne
volareaN=5.56D0	! Dronne

! conversion factors from currents to concentration changes
! We assume currents in pA/um2 and concentration changes in mM/s

xxx=-1D6/xF

ConvNaA=xxx/volareaA
ConvKA=xxx/volareaA
ConvClA=-xxx/volareaA
ConvCaA=0.5D0*xxx/volareaA
ConvNaN=xxx/volareaN
ConvKN=xxx/volareaN
ConvClN=-xxx/volareaN
ConvCaN=0.5D0*xxx/volareaN

! Ca buffering factor (**** CHECK ***)

CaBuffFact=1.0D0/40.0D0

! initial concentrations

KA0=130D0
KN0=130D0
KI0=3.5D0
NaA0=10D0
NaN0=10D0
NaI0=140D0
CaA0=0.0001D0
CaN0=0.0001D0
CaI0=2D0
ClA0=7D0
ClN0=10D0
ClI0=140D0

! initial membrane potentials

VmA0=-85D0
VmN0=-70D0

! Channel parameters

gKDRA=35D0
gKDRN=2D0
gBKA=0.1D0
gBKN=0.1D0
!gKirA=???
!gKAA=???
!gKAN=???
gKMA=0.01D0
gKMN=0.01D0
gSKA=0.005D0
gSKN=0.005D0
gIKA=0.004D0
gIKN=0.004D0
gNaFA=60D0
gNaFN=60D0
gNaPA=0.002D0
gNaPN=0.002D0
!gCaLVAA=???
!gCaLVAN=???
gCaHVAA=0.02D0
gCaHVAN=0.02D0
gKNaCaN=0.01D0
NMDAopen=72.0D0	! Destexhe et al
NMDAclose=6.6D0	! ditto
rClA=0.02D0
rClN=0.02D0
rCaA=0.001D0
rCaN=0.001D0
rNaKA=0.015D0
rNaKN=0.015D0
rNaCaA=10D0
rNaCaN=10D0
gKClA=0.00005D0
gKClN=0.00005D0
gNaKClA=0.00002D0

! glutamate production

glut0=0.0D0
neuglurate=0.7592D0		! Destexhe et al
astglurate=6.0D00	! estimate from previous work, must find correct value
gluuptrate=1.0	! must find correct value

!! NMDA receptor (superseded, but I'm keeping it for reference

!!Mg0=1.0D0	! Jahr & Stevens, Destexhe et al
!!NMDAopen=72.0D0	! Destexhe et al
!!NMDAclose=6.6D0	! ditto
!!VNMDArev=0.0D0	! Jahr & Stevens
!!gcondmaxNMDA=1.0D-9	! must find correct value

! membrane potential

Cmem=1.0d-6		! typical, see Bill's notes
Rmem=1.0d4		! typical, see Bill's notes

end subroutine ISetDefaults

!---------------------------------------------------
! read in override values and do some precomputation
!---------------------------------------------------

subroutine INextBatch
use global
use ionglob
implicit none
integer :: MallocError,lowx,mcell,nxblock

itimestep=timestep/iontimeratio
itwostep=twostep/iontimeratio

if (startVmem.lt.-999.0D0) startVmem=VmN0

Tmem=Rmem*Cmem
QCmem=0.1D0/Cmem

! allocate arrays

nxblock=nXsteps/nblock
mcell=(ncell-1)/2
! If we were to use sealed boundaries then this should read GE
if (nxblock*nblock+mcell+1.GT.nXsteps) nxblock=nxblock-1
lowx=-nxblock
IF (lxsymm) THEN
	lowx=0
ENDIF
allocate (KA(lowx:nxblock),STAT=MAllocError)
call testalloc(MAllocError)
allocate (KJ(lowx:nxblock),STAT=MAllocError)
call testalloc(MAllocError)
allocate (KN(lowx:nxblock),STAT=MAllocError)
call testalloc(MAllocError)
allocate (NaA(lowx:nxblock),STAT=MAllocError)
call testalloc(MAllocError)
allocate (NaI(lowx:nxblock),STAT=MAllocError)
call testalloc(MAllocError)
allocate (NaN(lowx:nxblock),STAT=MAllocError)
call testalloc(MAllocError)
allocate (CaA(lowx:nxblock),STAT=MAllocError)
call testalloc(MAllocError)
allocate (CaI(lowx:nxblock),STAT=MAllocError)
call testalloc(MAllocError)
allocate (CaN(lowx:nxblock),STAT=MAllocError)
call testalloc(MAllocError)
allocate (ClA(lowx:nxblock),STAT=MAllocError)
call testalloc(MAllocError)
allocate (ClI(lowx:nxblock),STAT=MAllocError)
call testalloc(MAllocError)
allocate (ClN(lowx:nxblock),STAT=MAllocError)
call testalloc(MAllocError)
allocate (VmA(lowx:nxblock),STAT=MAllocError)
call testalloc(MAllocError)
allocate (VmN(lowx:nxblock),STAT=MAllocError)
call testalloc(MAllocError)

allocate (glutA(lowx:nxblock),STAT=MAllocError)
call testalloc(MAllocError)
allocate (glutB(lowx:nxblock),STAT=MAllocError)
call testalloc(MAllocError)
allocate (NMDAy(lowx:nxblock),STAT=MAllocError)
call testalloc(MAllocError)
end subroutine INextBatch

!-------------------------------
! Deallocate memory between runs
!-------------------------------
subroutine IEndBatch
use ionglob
implicit none
deallocate (KA)
deallocate (KN)
deallocate (KJ)
deallocate (NaA)
deallocate (NaN)
deallocate (NaI)
deallocate (CaA)
deallocate (CaN)
deallocate (CaI)
deallocate (ClA)
deallocate (ClN)
deallocate (ClI)
deallocate (VmA)
deallocate (VmN)

deallocate (glutA)
deallocate (glutB)
deallocate (NMDAy)
endsubroutine IEndBatch
