!-------------------------------------------------
! Timestep one X/Y plane without assuming symmetry
!-------------------------------------------------
subroutine IP3One (ind, iz)
use global
implicit none
integer :: ind, iz
integer :: ix, iy, minx, lowx, lowy
logical :: odd
double precision :: source,zrelrate,zrelrated

lowx=-nXsteps
if (lxsymm) then
	lowx=0
endif

lowy=-nYsteps
if (lysymm) then
	lowy=0
endif

do iy=lowy,nYsteps
	if (odd(nXsteps+ind+iy)) THEN
		minx = lowx+1
	else
		minx = lowx
	endif
	do ix = minx,nXsteps,2
		IF (icell(ix,iy,iz).eq.castgen.OR.icell(ix,iy,iz).eq.castmem) THEN

			source=-kdeg*IP3(ix,iy,iz)

			IF (icell(ix,iy,iz).eq.castmem) THEN
				zrelrate=0.0D0
				zrelrated=0.0D0
				IF (icell(ix+1,iy,iz).eq.cextmem) THEN
					zrelrate=zrelrate+delta/(KG+delta)
					zrelrated=zrelrated+1.0D0
				ENDIF
				IF (icell(ix-1,iy,iz).eq.cextmem) THEN
					zrelrate=zrelrate+delta/(KG+delta)
					zrelrated=zrelrated+1.0D0
				ENDIF
				IF (icell(ix,iy+1,iz).eq.cextmem) THEN
					zrelrate=zrelrate+delta/(KG+delta)
					zrelrated=zrelrated+1.0D0
				ENDIF
				IF (icell(ix,iy-1,iz).eq.cextmem) THEN
					zrelrate=zrelrate+delta/(KG+delta)
					zrelrated=zrelrated+1.0D0
				ENDIF
				IF (icell(ix,iy,iz+1).eq.cextmem) THEN
					zrelrate=zrelrate+delta/(KG+delta)
					zrelrated=zrelrated+1.0D0
				ENDIF
				IF (icell(ix,iy,iz-1).eq.cextmem) THEN
					zrelrate=zrelrate+delta/(KG+delta)
					zrelrated=zrelrated+1.0D0
				ENDIF
				if (luseCa) zrelrate=zrelrate*Ca(ix,iy,iz)/(Kc+Ca(ix,iy,iz))
				zrelrated=zrelrated*Ca(ix,iy,iz)**2/(Kcd**2+Ca(ix,iy,iz)**2)
				source=source+zrelrate*rh+zrelrated*rhd
			ENDIF

			IP3(ix,iy,iz) = ( source					&
				+ IP3(ix,  iy,  iz  )*(timebit-sumfl(ix,iy,iz))	&
	 			+ IP3(ix+1,iy,  iz  )*flx(ix,  iy,  iz)		&
				+ IP3(ix-1,iy,  iz  )*flx(ix-1,iy,  iz)		&
				+ IP3(ix,  iy+1,iz  )*fly(ix,  iy,  iz)		&
				+ IP3(ix,  iy-1,iz  )*fly(ix,  iy-1,iz)		&
				+ IP3(ix,  iy,  iz+1)*flz(ix,  iy,  iz)		&
				+ IP3(ix,  iy,  iz-1)*flz(ix,  iy,  iz-1)	&
				)/(timebit+sumfl(ix,iy,iz))
		ENDIF
	enddo
	if (lxsymm) then
		IP3(-1,iy,iz)=IP3(1,iy,iz)
	endif
enddo
if (lysymm) then
	do ix=lowx,nXsteps
		IP3(ix,-1,iz)=IP3(ix,1,iz)
	enddo
endif
end subroutine IP3One

subroutine IP3All(ind)
use global
implicit none
integer :: ind,jnd,iz,ix,iy,lowx,lowy,lowz

jnd=ind
lowx=-nXsteps
if (lxsymm) then
	lowx=0
endif

lowy=-nYsteps
if (lysymm) then
	lowy=0
endif

lowz=-nZsteps
if (lzsymm) then
	lowz=0
endif

do iz=lowz,nZSteps
	jnd=3-jnd
	call IP3One(jnd,iz)
enddo

if (lzsymm) then
	do iy=lowy,nYSteps
		do ix=lowx,nXSteps
			IP3(ix,iy,-1)=IP3(ix,iy,1)
		enddo
	enddo
endif
end subroutine IP3All
