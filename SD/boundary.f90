!
! boundary.f90
!
! There is no need to set zero concentration on the outer boundaries,
! because the points are set zero initially and stay zero.
! Note however that if we were ever to use sealed boundaries then the
! test for determining the number of astrocytes in FlagCells is not
! correct.
!------------------------
! Apply sealed boundaries
!------------------------
subroutine BoundaryConds
use global
implicit none
integer :: iix,iiy,iiz
integer :: lowx,lowy,lowz
lowx=-nXSteps
lowy=-nYSteps
lowz=-nZSteps
if (lxsymm) then
	lowx=0
endif
if (lysymm) then
	lowy=0
endif
if (lzsymm) then
	lowz=0
endif
do iix = lowx,nXSteps
	do iiy = lowy,nYSteps
		ATP(iix,iiy,nZSteps+1) = ATP(iix,iiy,nZSteps)
		if (.not.lzsymm) then
			ATP(iix,iiy,-nZSteps-1) = ATP(iix,iiy,-nZSteps)
		endif 
	enddo
	do iiz = lowz,nZSteps
		ATP(iix,nYSteps+1,iiz) = ATP(iix,nYSteps,iiz)
		if (.not.lysymm) then
			ATP(iix,-nYSteps-1,iiz) = ATP(iix,-nYSteps,iiz)
		endif
	enddo
enddo
do iiy = lowy,nYSteps
	do iiz = lowz,nZSteps
		ATP(nXSteps+1,iiy,iiz) = ATP(nXSteps,iiy,iiz)
		if (.not.lxsymm) then
			ATP(-nXSteps-1,iiy,iiz) = ATP(-nXSteps,iiy,iiz)
		endif
	enddo
enddo
end subroutine BoundaryConds
