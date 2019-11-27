!
! step.f90
!
!--------------------------------------------
! Determine whether an integer is odd or even
!--------------------------------------------
function odd(ii) result (oddresult)
implicit none
integer :: ii
logical :: oddresult

oddresult=mod(ii,2).ne.0
end function odd
!-------------
! RK2 for ODEs
!-------------
subroutine CaODEs(IP3in,CaInOut,hInOut)
use global
implicit none
double precision :: IP3in,CaInOut,hInOut
double precision :: Caprime,hprime,CaMid,hMid

call CaDerivs(IP3in,CaInOut,hInOut,Caprime,hprime)
!call CaDerivs(0.15D0,CaInOut,hInOut,Caprime,hprime)
CaMid=CaInOut+timestep*Caprime
hMid=hInOut+timestep*hprime
call CaDerivs(IP3in,CaMid,hMid,Caprime,hprime)
!call CaDerivs(0.15D0,CaMid,hMid,Caprime,hprime)
CaInOut=CaInOut+twostep*Caprime
hInOut=hInOut+twostep*hprime
end subroutine CaODEs

subroutine CaDerivs(IP3X,CaX,hX,Caprime,hprime)
use global
implicit none
double precision :: IP3X,CaX,hX,Caprime,hprime
double precision :: term1,term2,term3,Jchannel,Jleak,Jpump
term1=IP3X/(IP3X+KI)
term2=CaX/(CaX+Kact)
term3=1.0D0-CaX/CaER
Jchannel=Jmax*(term1*term2*hX)**3*term3
Jleak=ERLeak*term3
Jpump=ERVmax*CaX**2/(CaX**2+Kpump**2)
Caprime=beta*(Jchannel-Jpump+Jleak)
hprime=kon*(Kinh-(CaX+Kinh)*hX)
end subroutine CaDerivs

subroutine RODEs(LossRate,StoreInOut)
use global
implicit none
double precision :: LossRate,StoreInOut
double precision :: Storeprime,StoreMid

call RDerivs(LossRate,StoreInOut,Storeprime)
StoreMid=StoreInOut+timestep*Storeprime
call RDerivs(LossRate,StoreMid,Storeprime)
StoreInOut=StoreInOut+twostep*Storeprime
end subroutine RODEs

subroutine RDerivs(LossRate,StoreX,Storeprime)
use global
implicit none
double precision :: LossRate,StoreX,Storeprime
StorePrime=-LossRate*StoreX*kATPloss
end subroutine RDerivs

!-------------------------------------------------
! Timestep one X/Y plane without assuming symmetry
!-------------------------------------------------
subroutine StepOne (ind, iz)
use global
implicit none
integer :: ind, iz
integer :: ix, iy, minx, lowx, lowy, ixgap
logical :: odd
double precision :: source,fracbound,storeloss,GlutBX,gapterm
double precision :: zrelrate,setAGain1,setAGain2,setALoss1,setALoss2
double precision :: zrelrated
logical :: llvaryKR

llvaryKR=lvaryKR.GT.0
ixgap=nblock-ncell+1

lowx=-nXsteps
if (lxsymm) then
	lowx=0
endif

lowy=-nYsteps
if (lysymm) then
	lowy=0
endif

! prepare gap junctions

gapterm=0.0D0
if (gapIP3.GT.0.0D0) then
	do iy=lowy,nYsteps
		if (odd(nXsteps+ind+iy)) THEN
			minx = lowx+1
		else
			minx = lowx
		endif
		do ix = minx,nXsteps,2
			IF (icell(ix,iy,iz).eq.castmem) THEN
				IF (icell(ix+1,iy,iz).eq.cextmem) THEN
					IF ((ix+nblock).LT.nXSteps) THEN
			gapterm(ix,iy)=gapIP3*(IP3(ix+ixgap,iy,iz)-IP3(ix,iy,iz))
					ENDIF
				ENDIF
				IF (icell(ix-1,iy,iz).eq.cextmem) THEN
					IF ((ix-nblock).GT.-nXsteps) THEN
			gapterm(ix,iy)=gapIP3*(IP3(ix-ixgap,iy,iz)-IP3(ix,iy,iz))
					ENDIF
				ENDIF
			ENDIF
		enddo
	enddo
endif

! main loop

do iy=lowy,nYsteps
	if (odd(nXsteps+ind+iy)) THEN
		minx = lowx+1
	else
		minx = lowx
	endif
	do ix = minx,nXsteps,2

! ATP production term
! Usually only one gridpoint will contribute, two if cells are close together

		source=0.0D0
		IF (icell(ix,iy,iz).eq.cextmem) THEN
			IF (icell(ix+1,iy,iz).eq.castmem) then
				source=source+setAGain1(ix+1,iy,iz)
			endif
			IF (icell(ix-1,iy,iz).eq.castmem) then
				source=source+setAGain1(ix-1,iy,iz)
			endif
			IF (icell(ix,iy+1,iz).eq.castmem) then
				source=source+setAGain1(ix,iy+1,iz)
			endif
			IF (icell(ix,iy-1,iz).eq.castmem) then
				source=source+setAGain1(ix,iy-1,iz)
			endif
			IF (icell(ix,iy,iz+1).eq.castmem) then
				source=source+setAGain1(ix,iy,iz+1)
			endif
			IF (icell(ix,iy,iz-1).eq.castmem) then
				source=source+setAGain1(ix,iy,iz-1)
			endif
			source=setAGain2(source,ix,iy,iz)
		ENDIF

! Simulate ATPase

		source=source-VATPase*ATP(ix,iy,iz)/(KATPase+ATP(ix,iy,iz))

! Step ATP, including diffusion

		ATP(ix,iy,iz) = ( source					&
			+ ATP(ix,  iy  ,iz  )*(timebit-sumfl(ix,iy,iz))	&
	 		+ ATP(ix+1,iy  ,iz  )*flx(ix,  iy,  iz)		&
			+ ATP(ix-1,iy  ,iz  )*flx(ix-1,iy,  iz)		&
			+ ATP(ix,  iy+1,iz  )*fly(ix,  iy,  iz)		&
			+ ATP(ix,  iy-1,iz  )*fly(ix,  iy-1,iz)		&
			+ ATP(ix,  iy  ,iz+1)*flz(ix,  iy,  iz)		&
			+ ATP(ix,  iy  ,iz-1)*flz(ix,  iy,  iz-1)		&
			)/(timebit+sumfl(ix,iy,iz))

! Step calcium and channel fraction

		IF (icell(ix,iy,iz).eq.castgen.OR.icell(ix,iy,iz).eq.castmem) THEN
			call CaODEs(IP3(ix,iy,iz),Ca(ix,iy,iz),h(ix,iy,iz))

! Simulate IP3 hydrolysis

			if (lusedelta) then
				source=-kdeg*IP3(ix,iy,iz)
			else
				source=-kdeg*(IP3(ix,iy,iz)-cIP30)
			endif

! IP3 production term and ATP store loss term
! 2 or 3 terms may contribute at corners

			IF (icell(ix,iy,iz).eq.castmem) THEN
				zrelrate=0.0D0
				zrelrated=0.0D0
				storeloss=0.0D0
				IF (llvaryKR) KR=vKR(ix,iy)
				IF (icell(ix+1,iy,iz).eq.cextmem) THEN
					fracbound=ATP(ix+1,iy,iz)/(KR+ATP(ix+1,iy,iz))+delta
					zrelrate=zrelrate+fracbound/(KG+fracbound)
					storeloss=storeloss+setALoss1(ix+1,iy,iz)
					zrelrated=zrelrated+1.0D0
				ENDIF
				IF (icell(ix-1,iy,iz).eq.cextmem) THEN
					fracbound=ATP(ix-1,iy,iz)/(KR+ATP(ix-1,iy,iz))+delta
					zrelrate=zrelrate+fracbound/(KG+fracbound)
					storeloss=storeloss+setALoss1(ix-1,iy,iz)
					zrelrated=zrelrated+1.0D0
				ENDIF
				IF (icell(ix,iy+1,iz).eq.cextmem) THEN
					fracbound=ATP(ix,iy+1,iz)/(KR+ATP(ix,iy+1,iz))+delta
					zrelrate=zrelrate+fracbound/(KG+fracbound)
					storeloss=storeloss+setALoss1(ix,iy+1,iz)
					zrelrated=zrelrated+1.0D0
				ENDIF
				IF (icell(ix,iy-1,iz).eq.cextmem) THEN
					fracbound=ATP(ix,iy-1,iz)/(KR+ATP(ix,iy-1,iz))+delta
					zrelrate=zrelrate+fracbound/(KG+fracbound)
					storeloss=storeloss+setALoss1(ix,iy-1,iz)
					zrelrated=zrelrated+1.0D0
				ENDIF
				IF (icell(ix,iy,iz+1).eq.cextmem) THEN
					fracbound=ATP(ix,iy,iz+1)/(KR+ATP(ix,iy,iz+1))+delta
					zrelrate=zrelrate+fracbound/(KG+fracbound)
					storeloss=storeloss+setALoss1(ix,iy,iz+1)
					zrelrated=zrelrated+1.0D0
				ENDIF
				IF (icell(ix,iy,iz-1).eq.cextmem) THEN
					fracbound=ATP(ix,iy,iz-1)/(KR+ATP(ix,iy,iz-1))+delta
					zrelrate=zrelrate+fracbound/(KG+fracbound)
					storeloss=storeloss+setALoss1(ix,iy,iz-1)
					zrelrated=zrelrated+1.0D0
				ENDIF

! Include glutamate response

				call GetGlutB(ix,iy,iz,GlutBX)
				fracbound=GlutBX/(KRg+GlutBX)
				zrelrate=zrelrate+fracbound/(KG+fracbound)

				if (luseCa) zrelrate=zrelrate*Ca(ix,iy,iz)/(Kc+Ca(ix,iy,iz))

				zrelrated=zrelrated*Ca(ix,iy,iz)**2/(Kcd**2+Ca(ix,iy,iz)**2)
				source=source+zrelrate*rh+gapterm(ix,iy)+zrelrated*rhd

! Step ATP store fraction

				storeloss=setALoss2(storeloss,ix,iy,iz)
				call RODEs(storeloss,AStore(ix,iy,iz))
			ENDIF

! Step IP3, including diffusion

			IP3(ix,iy,iz) = ( source					&
				+ IP3(ix,  iy  ,iz)*(timebit-sumfl(ix,iy,iz))	&
	 			+ IP3(ix+1,iy  ,iz)*flx(ix,  iy,  iz)		&
				+ IP3(ix-1,iy  ,iz)*flx(ix-1,iy,  iz)		&
				+ IP3(ix,  iy+1,iz)*fly(ix,  iy,  iz)		&
				+ IP3(ix,  iy-1,iz)*fly(ix,  iy-1,iz)		&
				+ IP3(ix,  iy  ,iz+1)*flz(ix,  iy,  iz)		&
				+ IP3(ix,  iy  ,iz-1)*flz(ix,  iy,  iz-1)		&
				)/(timebit+sumfl(ix,iy,iz))
		ENDIF
	enddo

	if (lxsymm) then
		ATP(-1,iy,iz)=ATP(1,iy,iz)
		IP3(-1,iy,iz)=IP3(1,iy,iz)
		AStore(-1,iy,iz)=AStore(1,iy,iz)
		Ca(-1,iy,iz)=Ca(1,iy,iz)
	endif
enddo

if (lysymm) then
	do ix=lowx,nXsteps
		ATP(ix,-1,iz)=ATP(ix,1,iz)
		IP3(ix,-1,iz)=IP3(ix,1,iz)
		AStore(ix,-1,iz)=AStore(ix,1,iz)
		Ca(ix,-1,iz)=Ca(ix,1,iz)
	enddo
endif
end subroutine StepOne

! Contribution  to ATP production from one of six adjacent cells

function setAGain1(ix,iy,iz) result (gainresult)
use global
implicit none
integer :: ix,iy,iz
double precision :: gainresult,fracbound
IF (latp.LT.4) THEN		! ATP from ATP
	gainresult=AStore(ix,iy,iz)
ELSEIF (latp.eq.4) THEN		! ATP from IP3
	IF (IP3(ix,iy,iz).GT.IP300) THEN
		gainresult=AStore(ix,iy,iz)*(IP3(ix,iy,iz)-IP300)/(KRel+IP3(ix,iy,iz))
	ELSE
		gainresult=0.0D0
	ENDIF
ELSE				! ATP from G-protein
	gainresult=AStore(ix,iy,iz)
ENDIF
end function setAGain1

! Final calculation of ATP production

function setAGain2(insource,ix,iy,iz) result (outsource)
use global
implicit none
integer :: ix,iy,iz
double precision :: insource,outsource,fracbound
IF (latp.eq.1) THEN
	outsource=insource*vmax*ATP(ix,iy,iz)/(KRel+ATP(ix,iy,iz))
ELSEIF (latp.eq.2) THEN
	outsource=insource*vmax*ATP(ix,iy,iz)**2/(KRel**2+ATP(ix,iy,iz)**2)
ELSEIF (latp.eq.3) THEN
	IF (ATP(ix,iy,iz).GT.ATP00) THEN
		outsource=insource*vmax*(ATP(ix,iy,iz)-ATP00)/(KRel+(ATP(ix,iy,iz)))
	ELSE
		outsource=0.0D0
	ENDIF
ELSEIF (latp.eq.4) THEN
	outsource=insource*vmax
ELSEIF (latp.eq.5) THEN
	fracbound=ATP(ix,iy,iz)/(KR+ATP(ix,iy,iz))+delta
	fracbound=fracbound/(KG+fracbound)
	IF (fracbound.GT.GFrac0) THEN
		outsource=insource*vmax*(fracbound-GFrac0)
	ELSE
		outsource=0.0D0
	ENDIF
ELSE
	fracbound=ATP(ix,iy,iz)/(KR+ATP(ix,iy,iz))
	fracbound=fracbound/(KG+fracbound)
	IF (fracbound.GT.GFrac0) THEN
		outsource=insource*vmax*(fracbound-GFrac0)
	ELSE
		outsource=0.0D0
	ENDIF
ENDIF
end function setAGain2

! Contribution to ATP loss from store from one of six adjacent cells

function setALoss1(ix,iy,iz) result (lossresult)
use global
implicit none
integer :: ix,iy,iz
double precision :: lossresult,fracbound
IF (latp.eq.1) THEN
	lossresult=ATP(ix,iy,iz)/(KRel+ATP(ix,iy,iz))
ELSEIF (latp.eq.2) THEN
	lossresult=ATP(ix,iy,iz)**2/(KRel**2+ATP(ix,iy,iz)**2)
ELSEIF (latp.eq.3) THEN
	IF (ATP(ix,iy,iz).GT.ATP00) THEN
		lossresult=(ATP(ix,iy,iz)-ATP00)/(KRel+ATP(ix,iy,iz))
	ELSE
		lossresult=0.0D0
	ENDIF
ELSEIF (latp.eq.4) THEN
	lossresult=1.0D0
ELSEIF (latp.eq.5) THEN
	fracbound=ATP(ix,iy,iz)/(KR+ATP(ix,iy,iz))+delta
	fracbound=fracbound/(KG+fracbound)
	IF (fracbound.GT.GFrac0) THEN
		lossresult=(fracbound-GFrac0)
	ELSE
		lossresult=0.0D0
	ENDIF
ELSE
	fracbound=ATP(ix,iy,iz)/(KR+ATP(ix,iy,iz))
	fracbound=fracbound/(KG+fracbound)
	IF (fracbound.GT.GFrac0) THEN
		lossresult=(fracbound-GFrac0)
	ELSE
		lossresult=0.0D0
	ENDIF
ENDIF
end function setALoss1

! Final calculation of ATP loss from store

function setALoss2(insource,ix,iy,iz) result (outsource)
use global
implicit none
integer :: ix,iy,iz
double precision :: insource,outsource
IF (latp.lt.4) THEN
	outsource=insource
ELSEIF (latp.eq.4) THEN
	IF (IP3(ix,iy,iz).GT.IP300) THEN
		outsource=insource*(IP3(ix,iy,iz)-IP300)/(KRel+IP3(ix,iy,iz))
	ELSE
		outsource=0.0D0
	ENDIF
ELSE
	outsource=insource
ENDIF
end function setALoss2

!
! Master timestepping routine, looping over Z
! ind flags whether odd or even timestep
!
subroutine StepAll(ind)
use global
implicit none
integer :: ind,jnd,iz,ix,iy,lowx,lowy,lowz

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

jnd=ind
do iz=lowz,nZSteps
	jnd=3-jnd
	call StepOne(jnd, iz)
enddo

if (lzsymm) then
	do iy=lowY,nYSteps
		do ix=lowx,nXSteps
			ATP(ix,iy,-1)=ATP(ix,iy,1)
			IP3(ix,iy,-1)=IP3(ix,iy,1)
			AStore(ix,iy,-1)=AStore(ix,iy,1)
			Ca(ix,iy,-1)=Ca(ix,iy,1)
		enddo
	enddo
endif
end subroutine StepAll
