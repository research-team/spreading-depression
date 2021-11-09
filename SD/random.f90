! Randomisation routines
!
! Initialisation
!
subroutine InitRAN3(lunit)
use ranglob
implicit none

! if lunit>0, read randomisation data from that unit
integer :: lunit
integer :: kran
double precision :: ran3,dummy

namelist/RAN/kran
namelist/INRAN/ma,iff,inext,inextp

iff=0
kran=0
if (lunit.GT.0) then
	read(lunit,RAN)
	if (kran.GT.0) then	! if kran>0 change the seed
		dummy=RAN3(kran)
	elseif (kran.LT.0) then	! if kran<0 read dumped data
		read(lunit,INRAN)
	endif
endif
end subroutine InitRAN3
!
! Save data (for restoration with kran<0)
!
subroutine SaveRAN3(lunit)
use ranglob
implicit none
integer :: lunit
namelist/OUTRAN/ma,iff,inext,inextp
write(lunit,OUTRAN)
end subroutine SaveRan3
!
! Function to return uniform random deviate - see Numerical Recipes
! The parameter idum should be set to 0, except for the very first
! call, when it may be used to set the seed.
! If idum is set to a negative integer, this indicates reseeding.
!
function RAN3(idum) result (ranno)
use ranglob
implicit none
integer :: idum
double precision :: ranno

integer :: mk,k,i,ii,mj

if (idum.lt.0.or.iff.eq.0) then
	iff=1	! flag generator seeded
	mj=mseed-iabs(idum)
	mj=mod(mj,mbig)
	ma(55)=mj
	mk=1
	do i=1,54
		ii=mod(21*i,55)
		ma(ii)=mk
		mk=mj-mk
		if (mk.lt.mz) mk=mk+mbig
		mj=ma(ii)
	enddo
	do k=1,4
		do i=1,55
			ma(i)=ma(i)-ma(1+mod(i+30,55))
			if (ma(i).lt.mz) ma(i)=ma(i)+mbig
		enddo
	enddo
	inext=0
	inextp=31
endif

inext=inext+1
if (inext.eq.56)inext=1
inextp=inextp+1
if (inextp.eq.56)inextp=1
mj=ma(inext)-ma(inextp)
if (mj.lt.mz)mj=mj+mbig
ma(inext)=mj
ranno=mj*fac
end function RAN3
