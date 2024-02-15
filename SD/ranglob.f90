! ranglob.f90

module ranglob

implicit none

integer :: iff=0	! set to 1 when generator is seeded
integer :: inext,inextp
integer, dimension(55) :: ma

integer, parameter :: mbig=1000000000
integer, parameter :: mseed=161803398
integer, parameter :: mz=0
double precision, parameter :: fac=1.0D0/mbig

end module ranglob
