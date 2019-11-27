!
! castep.f90
!
!-------------
! RK2 for ODEs
!-------------
subroutine XCaODEs(IP3in,CaInOut,hInOut)
use global
implicit none
double precision :: IP3in,CaInOut,hInOut
double precision :: Caprime,CaMid,hMid

call XCaDerivs(IP3in,CaInOut,hInOut,Caprime)
CaMid=CaInOut+timestep*Caprime
hMid=Kinh/(CaMid+Kinh)
call XCaDerivs(IP3in,CaMid,hMid,Caprime)
CaInOut=CaInOut+twostep*Caprime
hInOut=Kinh/(CaInOut+Kinh)
end subroutine XCaODEs

subroutine XCaDerivs(IP3X,CaX,hX,Caprime)
use global
implicit none
double precision :: IP3X,CaX,hX,Caprime
double precision :: term1,term2,term3,Jchannel,Jleak,Jpump
term1=IP3X/(IP3X+KI)
term2=CaX/(CaX+Kact)
term3=1.0D0-CaX/CaER
Jchannel=Jmax*(term1*term2*hX)**3*term3
Jleak=ERLeak*term3
Jpump=ERVmax*CaX**2/(CaX**2+Kpump**2)
Caprime=beta*(Jchannel-Jpump+Jleak)
end subroutine XCaDerivs

!subroutine XCaODEs(IP3in,CaInOut,hInOut)
!use global
!implicit none
!double precision :: IP3in,CaInOut,hInOut
!double precision :: Caprime,hprime,CaMid,hMid

!call XCaDerivs(IP3in,CaInOut,hInOut,Caprime,hprime)
!CaMid=CaInOut+timestep*Caprime
!hMid=hInOut+timestep*hprime
!call XCaDerivs(IP3in,CaMid,hMid,Caprime,hprime)
!CaInOut=CaInOut+twostep*Caprime
!hInOut=hInOut+twostep*hprime
!end subroutine XCaODEs

!subroutine XCaDerivs(IP3X,CaX,hX,Caprime,hprime)
!use global
!implicit none
!double precision :: IP3X,CaX,hX,Caprime,hprime
!double precision :: term1,term2,term3,Jchannel,Jleak,Jpump
!term1=IP3X/(IP3X+KI)
!term2=CaX/(CaX+Kact)
!term3=1.0D0-CaX/CaER
!Jchannel=Jmax*(term1*term2*hX)**3*term3
!Jleak=ERLeak*term3
!Jpump=ERVmax*CaX**2/(CaX**2+Kpump**2)
!Caprime=beta*(Jchannel-Jpump+Jleak)
!hprime=kon*(Kinh-(CaX+Kinh)*hX)
!end subroutine XCaDerivs

!-----------------------
! Timestep one X/Y plane
!-----------------------
subroutine CaOne (iz)
use global
implicit none
integer :: ix, iy, iz, lowx, lowy

lowx=-nXsteps
if (lxsymm) then
	lowx=0
endif
lowy=-nYsteps
if (lysymm) then
	lowy=0
endif

do iy=lowy,nYsteps
	do ix = lowx,nXsteps
		IF (icell(ix,iy,iz).eq.castgen.OR.icell(ix,iy,iz).eq.castmem) THEN
			call XCaODEs(IP3(ix,iy,iz),Ca(ix,iy,iz),h(ix,iy,iz))
		endif
	enddo
	if (lxsymm) then
		Ca(-1,iy,iz)=Ca(1,iy,iz)
	endif
enddo
if (lysymm) then
	do ix=lowx,nXsteps
		Ca(ix,-1,iz)=Ca(ix,1,iz)
	enddo
endif
end subroutine CaOne

!
! Master timestepping routine, looping over Z
! ind flags whether odd or even timestep
!
subroutine CaAll
use global
implicit none
integer :: iz,ix,iy,lowx,lowy,lowz

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
	call CaOne(iz)
enddo

if (lzsymm) then
	do iy=lowy,nYSteps
		do ix=lowx,nXSteps
			Ca(ix,iy,-1)=Ca(ix,iy,1)
		enddo
	enddo
endif

end subroutine CaAll
