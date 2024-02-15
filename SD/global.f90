! global.f90

module global

implicit none

! define cell characteristics

integer (kind=1), parameter :: cextgen=0	! general exterior
integer (kind=1), parameter :: cextmem=2	! exterior adjacent to membrane
integer (kind=1), parameter :: castgen=1	! general astrocyte interior
integer (kind=1), parameter :: castmem=3	! interior adjacent to membrane

logical :: lxsymm	! x direction mirror symmetric
logical :: lysymm	! y direction mirror symmetric
logical :: lzsymm	! z direction mirror symmetric

integer :: irunno ! run number for multiple runs
logical :: tSetFlux, tATP, tCa, tFlagCells	! debugging flags
integer :: npresteps	! iterations to set up IP3 field
integer :: npreca	! iterations to set up Ca field
integer :: npreiter	! number of cycles of setup phase
logical :: lusedelta, luseCa	! options to control IP3 cycle
integer :: latp		! option to control ATP release mechanism
integer :: lvaryKR	! option to vary KR between cells (bodgy)

! start-up data

character*10 startup
! Define the following methods
! ATP - set ATP to startATP in cells adjacent to the centre cell
! CASTEP - set Ca to startCa in central cell
! IPSTEP - set IP3 to startIP3 in central cell
! VMEM - set membrane potential to startVmem at first neuron
! in all cases ATP is mostly set to ATP0, calcium to Ca0, and IP3 to cIP30

double precision :: startATP	! initial concentration of ATP near centre cell, uM
double precision :: startCa	! initial concentration of Ca in centre cell, uM
double precision :: startIP3	! initial concentration of IP3 in centre cell, uM
double precision :: startVmem	! initial membrane potential centre cell, mV
double precision :: startperiod	! duration of step function, s
integer :: startcellx,startcelly	! offset of starting point (number of cells in x/y

! Geometry

integer :: nxsteps,nysteps,nzsteps	! nodes in system
double precision :: deltax,deltay,deltaz	! grid size (um)
integer :: ncell	! number of gridpoints per cell
integer :: nblock	! number of gridpoints per repeat

! Time

double precision :: timestep,endtime,movietime	! in seconds

! Physical constants

double precision :: diffATP	! diffusion constant, um^2/s
double precision :: vmaxraw	! release rate, umol/um^2 /s
double precision :: Krel	! constant for release uM
double precision :: VATPase	! maximum rate of ATP breakdown uM/s
double precision :: KATPase	! Michaelis constant for ATP breakdown uM
double precision :: ATP0	! background level of ATP, uM
double precision :: kATPloss	! ATP store depletion rate, /s
double precision :: Ca00,IP300,ATP00,GFrac0	! lowest level for ATP production

! Computed data

double precision :: t		! current time (s)
double precision :: timebit	! time-step factor in stepping
integer :: nTsteps		! number of timesteps
double precision :: vmax	! vmax converted to uM/s
double precision :: twostep	! time-step times two

!---------------
! IP3 generation
!---------------

double precision :: Kc		! Ca binding to PLC
double precision :: cIP30	! initial [IP3] (uM)
double precision :: diffIP3	! diffusion constant, um^2/s
double precision :: kdeg	! IP3 hydrolysis rate (/s)
double precision :: rhraw	! IP3 production rate (umol/s/um^2)
double precision :: KG		! G protein activation constant
double precision :: KR		! Receptor binding constant (uM)
double precision :: altKR	! alternate for variable KR setup
double precision :: KRg		! Glut receptor binding constant (uM? mM?)
double precision :: gapIP3	! transfer through gap junctions, (/s)

! extra stuff for PLC-delta

double precision :: rhrawd	! IP3 production rate (umol/s/um^2)
double precision :: Kcd		! Ca dissociation constant (uM)

! Computed data

double precision :: rh		! IP3 production rate (uM/s)
double precision :: delta	! G protein spontaneous activation parameter
double precision :: rhd		! IP3 production rate (uM/s)

!--------------------------
! Calcium release from E.R.
!--------------------------

double precision :: Ca0		! Initial cytoplasmic [Ca] (uM)
double precision :: CaER	! Effective [Ca] in ER (uM)
double precision :: B_over_K	! Endogenous buffer (dimensionless)

! IP3-induced Ca release from the ER

double precision :: KI		! IP3 binding site (uM)
double precision :: Kact	! Ca-activation site (uM)
double precision :: Jmax	! Maximum release rate (uM/s)

! Ca pump into the ER

double precision :: ERVmax	! Maximum pump rate (uM/s)
double precision :: Kpump	! Pump dissocation constant (uM)

! Channel opening

double precision :: Kinh	! Ca-inhibitory site (uM)
double precision :: kon		! Site on rate (/uM/s)

! Computed data

double precision :: beta	! Buffering parameter
double precision :: ERLeak	! Leak rate (uM/s)
double precision :: h0		! Channel open fraction

!--------------------------
! Allocatable arrays
!--------------------------

double precision, dimension(:,:,:), allocatable :: flx,fly,flz	! flux factors
double precision, dimension(:,:,:), allocatable :: sumfl	!
double precision, dimension(:,:,:), allocatable :: ATP		! ATP concentration
double precision, dimension(:,:,:), allocatable :: Ca,H		! Ca concentration and fraction open channels
double precision, dimension(:,:,:), allocatable :: IP3		! IP3 concentration
double precision, dimension(:,:,:), allocatable :: AStore	! fraction ATP store not released
integer (kind=1), dimension(:,:,:), allocatable :: icell	! flag gridpoints

double precision, dimension(:,:), allocatable :: vKR		! bodgy variable KR
double precision, dimension(:,:), allocatable :: gapterm	! gap junctions
end module global
