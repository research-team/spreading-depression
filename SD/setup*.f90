!
! setup.f90
!
!----------------------
! Blocking calculations
! Each cell has ncell gridpoints inside it in each direction
! Compute mcell=(ncell-1)/2
! The repeat length between cells is nblock in each direction
! Then the gridpoints number iblock*nblock-mcell to iblock*nblock+mcell
! are within a cell, iblock any integer. Of course, only if all
! three directions concur.
! The fluxes across and within cell boundaries are numbered
! iblock*nblock-mcell to iblock*nblock+mcell (perpendicular)
! iblock*nblock-mcell-1 to iblock*nblock+mcell (parallel)
!
! We assume that all cells are totally contained, so that only ATP
! need a boundary condition at the edge of the model
!----------------------
!-----------------------------
! Set up array of flux factors
!-----------------------------

subroutine SetFlux
use global
implicit none
integer :: ix,iy,iz,jx,jy,jz,mcell
integer :: lowx,lowy,lowz
double precision :: flix,fliy,fliz

flx=diffATP/(deltax*deltax)	! set whole arrays
fly=diffATP/(deltay*deltay)	! from ATP diffusion coefficient
flz=diffATP/(deltaz*deltaz)
flix=diffIP3/(deltax*deltax)	! but prepare to replace some
fliy=diffIP3/(deltay*deltay)	! from the IP3 constant
fliz=diffIP3/(deltaz*deltaz)

!
! We also set the flux to zero across cell boundaries
! and hopefully end up with ATP and IP3 fluxes in the same arrays
!
lowx=-nXsteps
lowy=-nYsteps
lowz=-nZsteps
IF (lxsymm) THEN
	lowx=0
ENDIF
IF (lysymm) THEN
	lowy=0
ENDIF
IF (lzsymm) THEN
	lowz=0
ENDIF
do ix=lowx,nXsteps
	do iy=lowy,nYsteps
  		do iz=lowz,nZsteps
  			if (icell(ix,iy,iz).eq.castgen) then
			    	flx(ix,iy,iz)=flix
			    	fly(ix,iy,iz)=fliy
			    	flz(ix,iy,iz)=fliz
 			endif
 			if (icell(ix,iy,iz).eq.castmem) then
			    	flx(ix,iy,iz)=flix
			    	fly(ix,iy,iz)=fliy
			    	flz(ix,iy,iz)=fliz
				if (icell(ix+1,iy,iz).eq.cextmem) then
					flx(ix,iy,iz)=0.0D0
				endif
				if (icell(ix,iy+1,iz).eq.cextmem) then
					fly(ix,iy,iz)=0.0D0
				endif
				if (icell(ix,iy,iz+1).eq.cextmem) then
					flz(ix,iy,iz)=0.0D0
				endif
 			endif
  			if (icell(ix,iy,iz).eq.cextmem) then
				if (icell(ix+1,iy,iz).eq.castmem) then
					flx(ix,iy,iz)=0.0D0
				endif
				if (icell(ix,iy+1,iz).eq.castmem) then
					fly(ix,iy,iz)=0.0D0
				endif
				if (icell(ix,iy,iz+1).eq.castmem) then
					flz(ix,iy,iz)=0.0D0
				endif
   			endif
 		enddo
	enddo
enddo
IF (lxsymm) THEN
	do iz=lowz,nZsteps
		do iy=lowy,nYsteps
			flx(-1,iy,iz)=flx(0,iy,iz)
		enddo
	enddo
ENDIF
IF (lysymm) THEN
	do iz=lowz,nZsteps
		do ix=lowx,nXsteps
			fly(ix,-1,iz)=fly(ix,0,iz)
		enddo
	enddo
ENDIF
IF (lzsymm) THEN
	do ix=lowx,nXsteps
		do iy=lowy,nYsteps
			flz(ix,iy,-1)=flz(ix,iy,0)
		enddo
	enddo
ENDIF

if (tSetFlux) call TestSetFlux

!
! Set sums
!
do ix=lowx,nXsteps
	do iy=lowy,nYsteps
		do iz=lowz,nZsteps
			sumfl(ix,iy,iz)=0.5D0*			&
			(flx(ix,iy,iz) + flx(ix-1,iy,iz)	&
			+fly(ix,iy,iz) + fly(ix,iy-1,iz)	&
			+flz(ix,iy,iz) + flz(ix,iy,iz-1) )
		enddo
	enddo
enddo
end subroutine SetFlux

!---------------------------------
! INITIALISE THE ATP CONCENTRATION
!---------------------------------
subroutine InitATP(linitial)
use global
implicit none
logical linitial
integer :: ix,iy,iz,mcell,lowx,lowy,lowz,highx,highy

IF (linitial) ATP=ATP0		! Set concentration everywhere to background

! Stimulus at all gridpoints just outside central cell

mcell=(ncell+1)/2
lowx=-mcell
lowy=-mcell
lowz=-mcell
IF (lxsymm) THEN
	lowx=0
ENDIF
IF (lysymm) THEN
	lowy=0
ENDIF
IF (lzsymm) THEN
	lowz=0
ENDIF

! Start at a cell other than central

highx=mcell
highy=mcell
if (startcellx.ne.0) then
	lowx=nblock*startcellx-mcell
	highx=nblock*startcellx+mcell
endif
if (startcelly.ne.0) then
	lowy=nblock*startcelly-mcell
	highy=nblock*startcelly+mcell
endif

!!! Startup Method ATP !!!

if (startup.EQ.'ATP') then
	do ix=lowx,highx
		do iy=lowy,highy
			do iz=lowz,mcell
				if (icell(ix,iy,iz).eq.cextmem) then
		  			ATP(ix,iy,iz)=startATP
	  			endif
			enddo
		enddo
	enddo
endif

! Now apply the symmetry stuff

lowx=-nXsteps
lowy=-nYsteps
lowz=-nZsteps
IF (lxsymm) THEN
	lowx=-1
ENDIF
IF (lysymm) THEN
	lowy=-1
ENDIF
IF (lzsymm) THEN
	lowz=-1
ENDIF

IF (lxsymm) THEN
	do iz=lowz,nZsteps
		do iy=lowy,nYsteps
			ATP(-1,iy,iz)=ATP(1,iy,iz)
		enddo
	enddo
ENDIF
IF (lysymm) THEN
	do iz=lowz,nZsteps
		do ix=lowx,nXsteps
			ATP(ix,-1,iz)=ATP(ix,1,iz)
		enddo
	enddo
ENDIF
IF (lzsymm) THEN
	do ix=lowx,nXsteps
		do iy=lowy,nYsteps
			ATP(ix,iy,-1)=ATP(ix,iy,1)
		enddo
	enddo
ENDIF

if (tATP) call TestATP

end subroutine InitATP

subroutine InitCa
use global
implicit none
integer :: ix,iy,iz,lowx,lowy,lowz,mcell,midx,midy

Ca=0.0D0		! Set concentration everywhere zero
IP3=0.0D0
h=0.0D0
AStore=1.0D0		! and full ATP stores

lowx=-nXsteps		! Now set the interior of the cells
lowy=-nYsteps
lowz=-nZsteps
IF (lxsymm) THEN
	lowx=0
ENDIF
IF (lysymm) THEN
	lowy=0
ENDIF
IF (lzsymm) THEN
	lowz=0
ENDIF

! Start at a cell other than central

midx=0
midy=0
if (startcellx.ne.0) then
	midx=nblock*startcellx
endif
if (startcelly.ne.0) then
	midy=nblock*startcelly
endif

! Set interior of cells

do ix=lowx,nXsteps
	do iy=lowy,nYsteps
  		do iz=lowz,nZsteps
  			if (icell(ix,iy,iz).eq.castgen.OR.icell(ix,iy,iz).eq.castmem) then
	  			Ca(ix,iy,iz)=Ca0
	  			h(ix,iy,iz)=h0
	  			IP3(ix,iy,iz)=cIP30
 			endif
  		enddo
	enddo
enddo

!!! Startup method CASTEP !!!

if (startup.EQ.'CASTEP'.AND..NOT.lusedelta) then
	mcell=(ncell-1)/2
	do ix=MAX(lowx,-mcell+midx),mcell+midx
		do iy=MAX(lowy,-mcell+midy),mcell+midy
  			do iz=MAX(lowz,-mcell),mcell
	  			Ca(ix,iy,iz)=startCa
  			enddo
		enddo
	enddo
endif

!!! Startup method IPSTEP !!!

if (startup.EQ.'IPSTEP'.AND..NOT.lusedelta) then
	mcell=(ncell-1)/2
	do ix=MAX(lowx,-mcell+midx),mcell+midx
		do iy=MAX(lowy,-mcell+midy),mcell+midy
  			do iz=MAX(lowz,-mcell),mcell
	  			IP3(ix,iy,iz)=startIP3
  			enddo
		enddo
	enddo
endif

IF (lxsymm) THEN
	do iz=MIN(lowz,-1),nZsteps
		do iy=MIN(lowy,-1),nYsteps
			Ca(-1,iy,iz)=Ca(1,iy,iz)
			IP3(-1,iy,iz)=IP3(1,iy,iz)
		enddo
	enddo
ENDIF
IF (lysymm) THEN
	do iz=MIN(lowz,-1),nZsteps
		do ix=MIN(lowx,-1),nXsteps
			Ca(ix,-1,iz)=Ca(ix,1,iz)
			IP3(ix,-1,iz)=IP3(ix,1,iz)
		enddo
	enddo
ENDIF
IF (lzsymm) THEN
	do ix=MIN(lowx,-1),nXsteps
		do iy=MIN(lowy,-1),nYsteps
			Ca(ix,iy,-1)=Ca(ix,iy,1)
			IP3(ix,iy,-1)=IP3(ix,iy,1)
		enddo
	enddo
ENDIF

if (tCa) call TestCa

end subroutine InitCa

subroutine ReInitCa
use global
implicit none
integer :: ix,iy,iz,lowx,lowy,lowz,mcell,midx,midy

lowx=-nXsteps
lowy=-nYsteps
lowz=-nZsteps
IF (lxsymm) THEN
	lowx=0
ENDIF
IF (lysymm) THEN
	lowy=0
ENDIF
IF (lzsymm) THEN
	lowz=0
ENDIF

midx=0
if (startcellx.ne.0) then
	midx=nblock*startcellx
endif
midy=0
if (startcelly.ne.0) then
	midy=nblock*startcelly
endif

if (startup.EQ.'CASTEP') then
	mcell=(ncell-1)/2
	do ix=MAX(lowx,-mcell+midx),mcell+midx
		do iy=MAX(lowy,-mcell),mcell
  			do iz=MAX(lowz,-mcell),mcell
	  			Ca(ix,iy,iz)=startCa
  			enddo
		enddo
	enddo
endif
if (startup.EQ.'IPSTEP') then
	mcell=(ncell-1)/2
	do ix=MAX(lowx,-mcell+midx),mcell+midx
		do iy=MAX(lowy,-mcell),mcell
  			do iz=MAX(lowz,-mcell),mcell
	  			IP3(ix,iy,iz)=startIP3
  			enddo
		enddo
	enddo
endif

IF (lxsymm) THEN
	do iz=MIN(lowz,-1),nZsteps
		do iy=MIN(lowy,-1),nYsteps
			Ca(-1,iy,iz)=Ca(1,iy,iz)
			IP3(-1,iy,iz)=IP3(1,iy,iz)
		enddo
	enddo
ENDIF
IF (lysymm) THEN
	do iz=MIN(lowz,-1),nZsteps
		do ix=MIN(lowx,-1),nXsteps
			Ca(ix,-1,iz)=Ca(ix,1,iz)
			IP3(ix,-1,iz)=IP3(ix,1,iz)
		enddo
	enddo
ENDIF
IF (lzsymm) THEN
	do ix=MIN(lowx,-1),nXsteps
		do iy=MIN(lowy,-1),nYsteps
			Ca(ix,iy,-1)=Ca(ix,iy,1)
			IP3(ix,iy,-1)=IP3(ix,iy,1)
		enddo
	enddo
ENDIF
end subroutine ReInitCa

subroutine ExtendStep
use global
implicit none
if (startup.eq.'ATP') THEN
	call InitATP(.FALSE.)
elseif (startup.eq.'VMEM') THEN
	call InitVmem
else
	call ReInitCa
endif
end subroutine ExtendStep

!------------------------------------
! FLAG WHAT HAPPENS AT EACH GRIDPOINT
!------------------------------------
subroutine FlagCells
use global
implicit none
integer :: ix,iy,iz,jx,jy,jz,mcell
integer :: ixb,iyb,izb,jxb,jyb,jzb,nxblock,nyblock,nzblock
integer :: lowx,lowy,lowz,lowjx,lowjy,lowjz

icell=cextgen		! flag all gridpoints as in exterior

nxblock=nXsteps/nblock
nyblock=nYsteps/nblock
nzblock=nZsteps/nblock
mcell=(ncell-1)/2
! If we were to use sealed boundaries then this should read GE
if (nxblock*nblock+mcell+1.GT.nXsteps) nxblock=nxblock-1
if (nyblock*nblock+mcell+1.GT.nYsteps) nyblock=nyblock-1
if (nzblock*nblock+mcell+1.GT.nZsteps) nzblock=nzblock-1
nzblock=0
nyblock=0
lowx=-nxblock
lowy=-nyblock
lowz=-nzblock
IF (lxsymm) THEN
	lowx=0
ENDIF
IF (lysymm) THEN
	lowy=0
ENDIF
IF (lzsymm) THEN
	lowz=0
ENDIF
!
! Loop over possible cells
!
do ixb=lowx,nxblock
	jxb=ixb*nblock
	do iyb=lowy,nyblock
		do izb=lowz,nzblock
			jzb=izb*nblock
!
! Loops to handle one cell
!

! flag gridpoints just outside cell surface

lowjx=-nxsteps-2
lowjy=-nysteps-2
lowjz=-nzsteps-2
if (lxsymm) lowjx=-1
if (lysymm) lowjy=-1
if (lzsymm) lowjz=mcell

do ix = -mcell,mcell
	jx=ix+jxb
	IF (jx.GE.lowjx) THEN
		do iy=-mcell,mcell
			jy=iy+jyb
			IF (jy.GE.lowjy) THEN
				icell(jx,jy,jzb+mcell+1)=cextmem
				IF (jzb.GE.lowjz) THEN
					icell(jx,jy,jzb-mcell-1)=cextmem
				ENDIF
			ENDIF
		enddo
	ENDIF
enddo

if (lzsymm) lowjz=-1
if (lysymm) lowjy=mcell

do ix = -mcell,mcell
	jx=ix+jxb
	IF (jx.GE.lowjx) THEN
		do iz=-mcell,mcell
			jz=iz+jzb
			IF (jz.GE.-1) THEN
				icell(jx,jyb+mcell+1,jz)=cextmem
				IF (jyb.GE.lowjy) THEN
					icell(jx,jyb-mcell-1,jz)=cextmem
				ENDIF
			ENDIF
		enddo
	ENDIF
enddo

if (lxsymm) lowjx=mcell
if (lysymm) lowjy=-1

do iy = -mcell,mcell
	jy=iy+jyb
	IF (jy.GE.lowjy) THEN
		do iz=-mcell,mcell
			jz=iz+jzb
			IF (jz.GE.lowjz) THEN
				icell(jxb+mcell+1,jy,jz)=cextmem
				IF (jxb.GE.lowjx) THEN
					icell(jxb-mcell-1,jy,jz)=cextmem
				ENDIF
			ENDIF
		enddo
	ENDIF
enddo
!
! flag gridpoints within cells
!

if (lxsymm) lowjx=-1

do ix = -mcell,mcell
	jx=ix+jxb
	do iy = -mcell,mcell
		jy=iy+jyb
		do iz = -mcell,mcell
			jz=iz+jzb
			IF (jx.GE.lowjx.AND.jy.GE.lowjy.AND.jz.GE.lowjz) THEN
				icell(jx,jy,jz)=castgen
				IF (ABS(ix).EQ.mcell.OR.ABS(iy).EQ.mcell	&
					.OR.ABS(iz).EQ.mcell)THEN
					icell(jx,jy,jz)=castmem
				ENDIF
			ENDIF
		enddo
	enddo
enddo
!
! End loops for one cell
!
		enddo
	enddo
enddo

if (tFlagCells) call TestFlagCells
end subroutine FlagCells

subroutine TestFlagCells
use global
implicit none
integer :: lowx,lowy,lowz,ix,iy,iz
integer :: mcell,xcmax,ycmax

INTEGER :: ip
CHARACTER*51 :: ppp

lowx=MAX(-25,-nXSteps)
lowy=MAX(-25,-nYSteps)
lowz=MAX(-25,-nZsteps)
IF (lxsymm) THEN
	lowx=-1
ENDIF
IF (lysymm) THEN
	lowy=-1
ENDIF
IF (lzsymm) THEN
	lowz=-1
ENDIF
DO ip=1,51
	ppp(ip:ip)='.'
enddo
DO iz=lowz,MIN(25,nZSteps)
	DO iy=lowy,MIN(25,nYSteps)
		DO ix=lowx,MIN(25,nXSteps)
			ip=ix-lowx+1
			IF (icell(ix,iy,iz).EQ.0) THEN
				ppp(ip:ip)='0'
			ELSEIF (icell(ix,iy,iz).eq.castgen) THEN
				ppp(ip:ip)='1'
			ELSEIF (icell(ix,iy,iz).eq.cextmem) THEN
				ppp(ip:ip)='2'
			ELSEIF (icell(ix,iy,iz).eq.castmem) THEN
				ppp(ip:ip)='3'
			ELSE
				ppp(ip:ip)='X'
			ENDIF
		ENDDO
		write(*,*)ppp
	ENDDO
	write(*,*)
	read(*,*)
ENDDO
write(*,*)

DO ip=1,51
	ppp(ip:ip)='.'
enddo
mcell=(ncell+1)/2
xcmax=int((nxsteps+mcell)/nblock)-1
ycmax=int((nysteps+mcell)/nblock)-1
lowx=-xcmax
lowy=-ycmax
IF (lxsymm) THEN
	lowx=0
ENDIF
IF (lysymm) THEN
	lowy=0
ENDIF
do ix=lowx,xcmax
	do iy=lowy,ycmax
		ip=iy-lowy+1
		IF (icell(ix*nblock,iy*nblock,0).EQ.cextgen) THEN
			ppp(ip:ip)='0'
		ELSEIF (icell(ix*nblock,iy*nblock,0).eq.castgen) THEN
			ppp(ip:ip)='1'
		ELSEIF (icell(ix*nblock,iy*nblock,0).eq.cextmem) THEN
			ppp(ip:ip)='2'
		ELSEIF (icell(ix*nblock,iy*nblock,0).eq.castmem) THEN
			ppp(ip:ip)='3'
		ELSE
			ppp(ip:ip)='X'
		ENDIF
	ENDDO
	write(*,*)ppp
ENDDO
STOP
end subroutine TestFlagCells

subroutine TestSetFlux
use global
implicit none
integer :: lowx,lowy,lowz,ix,iy,iz
double precision :: flix,fliy,fliz,testflix,testfliy,testfliz

INTEGER :: ip
CHARACTER*51 :: ppp

flix=diffIP3/(deltax*deltax)
fliy=diffIP3/(deltay*deltay)
fliz=diffIP3/(deltaz*deltaz)
testflix=0.01D0*flix
testfliy=0.01D0*fliy
testfliz=0.01D0*fliz

lowx=MAX(-25,-nXSteps)
lowy=MAX(-25,-nYSteps)
lowz=MAX(-25,-nZsteps)
IF (lxsymm) THEN
	lowx=0
ENDIF
IF (lysymm) THEN
	lowy=0
ENDIF
IF (lzsymm) THEN
	lowz=0
ENDIF
do ip=1,51
	ppp(ip:ip)='.'
enddo
if (lowz.eq.0) then
	write(*,*)'<<<z=-1>>>'
	DO iy=lowy,MIN(25,nYSteps)
		DO ix=lowx,MIN(25,nXSteps)
			ip=ix-lowx+1
			IF (flz(ix,iy,-1).EQ.0.0D0) THEN
				ppp(ip:ip)='.'
			ELSEIF (flz(ix,iy,-1).EQ.-1.0D0) THEN
				ppp(ip:ip)='-'
			ELSEIF (ABS(fliz-flz(ix,iy,-1)).LT.testfliz) THEN
				ppp(ip:ip)='I'
			ELSE
				ppp(ip:ip)='A'
			ENDIF
		ENDDO
		write(*,*)ppp
	ENDDO
	write(*,*)
	read(*,*)
endif
DO iz=lowz,MIN(25,nZSteps)
	write(*,*)'<<<z=',iz,'>>>'
	DO iy=lowy,MIN(25,nYSteps)
		DO ix=MIN(lowx,-1),MIN(25,nXSteps)
			ip=ix-MIN(lowx,-1)+1
			IF (flx(ix,iy,iz).EQ.0.0D0) THEN
				ppp(ip:ip)='.'
			ELSEIF (flx(ix,iy,iz).EQ.-1.0D0) THEN
				ppp(ip:ip)='-'
			ELSEIF (ABS(flix-flx(ix,iy,iz)).LT.testflix) THEN
				ppp(ip:ip)='I'
			ELSE
				ppp(ip:ip)='A'
			ENDIF
		ENDDO
		write(*,*)ppp
	ENDDO
	write(*,*)
	DO iy=MIN(lowy,-1),MIN(25,nYSteps)
		DO ix=lowx,MIN(25,nXSteps)
			ip=ix-lowx+1
			IF (fly(ix,iy,iz).EQ.0.0D0) THEN
				ppp(ip:ip)='.'
			ELSEIF (fly(ix,iy,iz).EQ.-1.0D0) THEN
				ppp(ip:ip)='-'
			ELSEIF (ABS(fliy-fly(ix,iy,iz)).LT.testfliy) THEN
				ppp(ip:ip)='I'
			ELSE
				ppp(ip:ip)='A'
			ENDIF
		ENDDO
		write(*,*)ppp
	ENDDO
	write(*,*)
	DO iy=lowy,MIN(25,nYSteps)
		DO ix=lowx,MIN(25,nXSteps)
			ip=ix-lowx+1
			IF (flz(ix,iy,iz).EQ.0.0D0) THEN
				ppp(ip:ip)='.'
			ELSEIF (flz(ix,iy,iz).EQ.-1.0D0) THEN
				ppp(ip:ip)='-'
			ELSEIF (ABS(fliz-flz(ix,iy,iz)).LT.testfliz) THEN
				ppp(ip:ip)='I'
			ELSE
				ppp(ip:ip)='A'
			ENDIF
		ENDDO
		write(*,*)ppp
	ENDDO
	write(*,*)
	read(*,*)
ENDDO
STOP
end subroutine TestSetFlux

subroutine TestATP
use global
implicit none
integer :: lowx,lowy,lowz,ix,iy,iz

INTEGER :: ip
CHARACTER*31 :: ppp

lowx=MAX(-15,-nXSteps)
lowy=MAX(-15,-nYSteps)
lowz=MAX(-15,-nZsteps)
IF (lxsymm) THEN
	lowx=-1
ENDIF
IF (lysymm) THEN
	lowy=-1
ENDIF
IF (lzsymm) THEN
	lowz=-1
ENDIF
DO ip=1,15
	ppp(ip:ip)='.'
enddo
DO iz=lowz,MIN(15,nZSteps)
	DO iy=lowy,MIN(15,nYSteps)
		DO ix=lowx,MIN(15,nXSteps)
			ip=ix-lowx+1
			IF (ATP(ix,iy,iz).GT.1.0D-10) THEN
				ppp(ip:ip)='X'
			ELSE
				ppp(ip:ip)='.'
			ENDIF
		ENDDO
		write(*,*)ppp
	ENDDO
	write(*,*)
	read(*,*)
ENDDO
STOP
end subroutine TestATP

subroutine TestCa
use global
implicit none
integer :: lowx,lowy,lowz,ix,iy,iz

INTEGER :: ip
CHARACTER*31 :: ppp

lowx=MAX(-15,-nXSteps)
lowy=MAX(-15,-nYSteps)
lowz=MAX(-15,-nZsteps)
IF (lxsymm) THEN
	lowx=-1
ENDIF
IF (lysymm) THEN
	lowy=-1
ENDIF
IF (lzsymm) THEN
	lowz=-1
ENDIF
DO ip=1,31
	ppp(ip:ip)='.'
enddo
DO iz=lowz,MIN(15,nZSteps)
	DO iy=lowy,MIN(15,nYSteps)
		DO ix=lowx,MIN(15,nXSteps)
			ip=ix-lowx+1
			IF (ABS(Ca(ix,iy,iz)-StartCa).LT.1.0D-10) THEN
				ppp(ip:ip)='S'
			ELSEIF (ABS(Ca(ix,iy,iz)-Ca0).LT.1.0D-10) THEN
				ppp(ip:ip)='O'
			ELSEIF (Ca(ix,iy,iz).GT.1.0D-10) THEN
				ppp(ip:ip)='X'
			ELSE
				ppp(ip:ip)='-'
			ENDIF
		ENDDO
		write(*,*)ppp
	ENDDO
	write(*,*)
	read(*,*)
ENDDO
STOP
end subroutine TestCa

! This routine is just bodge up
! IT WILL NOT WORK IF ATP IS GENERATED FROM G-PROTEIN
! BECAUSE KR IS APPLIED AT THE EXTERIOR GRIDPOINT

subroutine InitvKR
use global
implicit none
integer :: ix,iy,lowx,lowy,mcell,ixc,iyc
double precision :: RAN3

lowx=-nXsteps
lowy=-nYsteps
IF (lxsymm) THEN
	lowx=0
ENDIF
IF (lysymm) THEN
	lowy=0
ENDIF

mcell=(ncell+1)/2

! Set interior of cells

do ix=lowx,nXsteps
	do iy=lowy,nYsteps
		if (icell(ix,iy,mcell-1).eq.castmem) then
			if (ix.lt.0) then
				ixc=-INT((-ix+mcell)/nblock)
			else
				ixc=INT((ix+mcell)/nblock)
			endif
			if (iy.lt.0) then
				iyc=-INT((-iy+mcell)/nblock)
			else
				iyc=INT((iy+mcell)/nblock)
			endif

! (1) KR different at +x and -x

			if (lvaryKR.eq.1) then
				if (ixc.GT.0) THEN
					vKR(ix,iy)=altKR
				else
					vKR(ix,iy)=KR
				endif

! (2) KR randomised

			elseif (lvaryKR.eq.2) then
				vKR(ix,iy)=KR+(altKR-KR)*RAN3(0)
				if (ixc.eq.startcellx) vKR(ix,iy)=KR
			endif
		endif
	enddo
enddo

end subroutine InitvKR
