! ionglob.f90

module ionglob

implicit none

! special timestepping for ion equations

integer :: iontimeratio	! ratio standard time-step/ion time-step
double precision :: itimestep	! in seconds (computed)
double precision :: itwostep	! time-step times two (computed)

! Physical constants

double precision :: RTF		! (mv)

! Volume ratios

double precision :: epsA	! astrocyte/interstitial
double precision :: epsN	! neuron/interstitial

! Volume/membrane area

double precision :: volareaA	! astrocyte (um)
double precision :: volareaN	! neuron (um)

! conversion factors from currents to concentration changes

double precision :: ConvNaA,ConvKA,ConvClA,ConvCaA
double precision :: ConvNaN,ConvKN,ConvClN,ConvCaN

! Ca buffering factor (**** CHECK ***)

double precision :: CaBuffFact

! initial concentrations

double precision :: KA0, KN0, KI0		! potassium (mM)
double precision :: NaA0, NaN0, NaI0	! sodium (mM)
double precision :: CaA0, CaN0, CaI0	! calcium (mM)
double precision :: ClA0, ClN0, ClI0		! chlorine (mM)

! initial membrane potentials

double precision :: VmA0, VmN0	! (mV)

! Potassium delayed rectifier channel

double precision :: gKDRA,gKDRN	! (nS/um^2)

! Potassium BK channel

double precision :: gBKA,gBKN	! (nS/um^2)

! Potassium inward rectifier channel

double precision :: gKirA	! (nS/um^2)

! Potassium A channel

double precision :: gKAA,gKAN	! (nS/um^2)

! Potassium M channel

double precision :: gKMA,gKMN	! (nS/um^2)

! Potassium SK channel

double precision :: gSKA,gSKN	! (nS/um^2)

! Potassium IK channel

double precision :: gIKA,gIKN	! (nS/um^2)

! Sodium transient current

double precision :: gNaFA,gNaFN	! (nS/um^2)

! Sodium persistent current

double precision :: gNaPA,gNaPN	! (nS/um^2)

! Calcium low-voltage-activated

double precision :: gCaLVAA,gCaLVAN	! (nS/um^2)

! Calcium high-voltage-activated

double precision :: gCaHVAA,gCaHVAN	! (nS/um^2)

! NMDA receptor

double precision :: gKNaCaN	! dimensionless
double precision :: NMDAKfac,NMDANafac,NMDACafac	! calculated quantities
double precision :: NMDAopen	! channel opening (/mM/s)
double precision :: NMDAclose	! channel closing (/s)

! Chloride pump

double precision :: rClA,rClN	! (pA/um2)

! Calcium pump

double precision :: rCaA,rCaN	! (pA/um2)

! Sodium/potassium pump

double precision :: rNaKA,rNaKN	! (pA/um2)

! Sodium/calcium exchanger

double precision :: rNaCaA,rNaCaN	! (pA/um2)

! Potassium/chloride transporter

double precision :: gKClA,gKClN	! (nS/um^2)

! Sodium/potassium/chloride transporter

double precision :: gNaKClA	! (nS/um^2)

! Leaks (set from initial balance)

double precision :: gKLeakN,gKLeakA
double precision :: gNaLeakN,gNaLeakA
double precision :: gCaLeakN,gCaLeakA
double precision :: gClLeakN,gClLeakA

!---------------------
! glutamate production
!---------------------

double precision :: glut0	! background level of glut, mM

double precision :: neuglurate	! glutamate production rate (mM/s)
double precision :: astglurate	! glutamate production rate (mM/s)
double precision :: gluuptrate	! glutamate uptake rate (/s)

!! NMDA receptor (superseded, but I'm keeping it for reference

!!double precision :: Mg0		! extracellular Mg (mM)
!!double precision :: NMDAopen	! opening rate (Bill's r1) (/mM/s)
!!double precision :: NMDAclose	! closing rate (Bill's r2) (/s)
!!double precision :: VNMDArev		! reversal potential (mV)
!!double precision :: gcondmaxNMDA	! maximum whole cell conductance (ohm^-1)

!-------------------
! Membrane potential
!-------------------

double precision :: Cmem	! membrane capacitance (F/cm^2)
double precision :: Rmem	! membrane resistance (ohm cm^2)

! Computed data

double precision :: Tmem	! membrane time constant (/s)
double precision :: QCmem	! roughly 1/Cmem ( (Gohm/s)(um^2))

!--------------------------
! Allocatable arrays
!--------------------------

double precision, dimension(:), allocatable :: KA	! astrocyte K+ concentration
double precision, dimension(:), allocatable :: KN	! neuron K+ concentration
double precision, dimension(:), allocatable :: KJ	! interstitial K+ concn
double precision, dimension(:), allocatable :: NaA	! astrocyte Na+ concentration
double precision, dimension(:), allocatable :: NaN	! neuron Na+ concentration
double precision, dimension(:), allocatable :: NaI	! interstitial Na+ concn
double precision, dimension(:), allocatable :: CaA	! astrocyte Ca2+ concentration
double precision, dimension(:), allocatable :: CaN	! neuron Ca2+ concentration
double precision, dimension(:), allocatable :: CaI	! interstitial Ca2+ concn
double precision, dimension(:), allocatable :: ClA	! astrocyte Cl- concentration
double precision, dimension(:), allocatable :: ClN	! neuron Cl- concentration
double precision, dimension(:), allocatable :: ClI	! interstitial Cl- concn
double precision, dimension(:), allocatable :: VmA	! astrocyte membrane potential
double precision, dimension(:), allocatable :: VmN	! neuron membrane potential

double precision, dimension(:), allocatable :: glutA	! glutamate A concentration
double precision, dimension(:), allocatable :: glutB	! glutamate B concentration
double precision, dimension(:), allocatable :: NMDAy	! open probability

end module ionglob
