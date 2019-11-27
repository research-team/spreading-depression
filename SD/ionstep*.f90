!-------------
! RK2 for ODEs
!-------------
subroutine IonODEs(NaIinout,NaAinout,NaNinout, KIinout,KNinout,KAinout,	&
	ClIinout,ClAinout,ClNinout, CaAinout,CaIinout,CaNinout, VmAinout,VmNinout,	&
	GlutAinout,GlutBinout,NMDAyInOut,ATPIn)
use ionglob
use global
implicit none
double precision :: NaIinout,NaAinout,NaNinout, KIinout,KNinout,KAinout
double precision :: ClIinout,ClAinout,ClNinout, CaAinout,CaIinout,CaNinout
double precision :: VmAinout,VmNinout,GlutAInout,GlutBInout,NMDAyInOut,ATPIn
double precision :: NaImid,NaAmid,NaNmid, KImid,KNmid,KAmid
double precision :: ClImid,ClAmid,ClNmid, CaAmid,CaImid,CaNmid
double precision :: VmAmid,VmNmid,GlutAmid,GlutBmid,NMDAymid
double precision :: NaIprime,NaAprime,NaNprime, KIprime,KNprime,KAprime
double precision :: ClIprime,ClAprime,ClNprime, CaAprime,CaIprime,CaNprime
double precision :: VmAprime,VmNprime,GlutAprime,GlutBprime,NMDAyprime

call IonDerivs(NaIinout,NaAinout,NaNinout, KIinout,KNinout,KAinout, &
	ClIinout,ClAinout,ClNinout, CaAinout,CaIinout,CaNinout,	&
	VmAinout,VmNinout,GlutAinout,GlutBinout,NMDAyInOut,ATPIn, 	&
	NaIprime,NaAprime,NaNprime, KIprime,KNprime,KAprime, &
	ClIprime,ClAprime,ClNprime, CaAprime,CaIprime,CaNprime, &
	VmAprime,VmNprime,GlutAprime,GlutBprime,NMDAyprime)
NaImid=NaIinout+itimestep*NaIprime
NaAmid=NaAinout+itimestep*NaAprime
NaNmid=NaNinout+itimestep*NaNprime
KImid=KIinout+itimestep*KIprime
KAmid=KAinout+itimestep*KAprime
KNmid=KNinout+itimestep*KNprime
CaImid=CaIinout+itimestep*CaIprime
CaAmid=CaAinout+itimestep*CaAprime
CaNmid=CaNinout+itimestep*CaNprime
ClImid=ClIinout+itimestep*ClIprime
ClAmid=ClAinout+itimestep*ClAprime
ClNmid=ClNinout+itimestep*ClNprime
VmAmid=VmAinout+itimestep*VmAprime
VmNmid=VmNinout+itimestep*VmNprime
GlutAmid=GlutAinout+itimestep*GlutAprime
GlutBmid=GlutBinout+itimestep*GlutBprime
NMDAyMid=NMDAyInOut+timestep*NMDAyprime

call IonDerivs(NaImid,NaAmid, NaNmid, KImid,KNmid,KAmid, &
	ClImid,ClAmid,ClNmid, CaAmid,CaImid,CaNmid,	&
	VmAmid,VmNmid,GlutAmid,GlutBmid,NMDAyMid,ATPIn, 	&
	NaIprime,NaAprime,NaNprime, KIprime,KNprime,KAprime, &
	ClIprime,ClAprime,ClNprime, CaAprime,CaIprime,CaNprime, &
	VmAprime,VmNprime,GlutAprime,GlutBprime,NMDAyprime)
NaIinout=NaIinout+itwostep*NaIprime
NaAinout=NaAinout+itwostep*NaAprime
NaNinout=NaNinout+itwostep*NaNprime
KIinout=KIinout+itwostep*KIprime
KAinout=KAinout+itwostep*KAprime
KNinout=KNinout+itwostep*KNprime
CaIinout=CaIinout+itwostep*CaIprime
CaAinout=CaAinout+itwostep*CaAprime
CaNinout=CaNinout+itwostep*CaNprime
ClIinout=ClIinout+itwostep*ClIprime
ClAinout=ClAinout+itwostep*ClAprime
ClNinout=ClNinout+itwostep*ClNprime
VmAinout=VmAinout+itwostep*VmAprime
VmNinout=VmNinout+itwostep*VmNprime
GlutAInOut=GlutAInOut+itwostep*GlutAprime
GlutBInOut=GlutBInOut+itwostep*GlutBprime
NMDAyInOut=NMDAyInOut+twostep*NMDAyprime
end subroutine IonODEs

subroutine IonDerivs(NaIX,NaAX,NaNX, KIX,KNX,KAX, ClIX,ClAX,ClNX, CaAX,CaIX,CaNX,	&
	VmAZ,VmNX,GlutAX,GlutBX,NMDAyX,ATPIn, 	&
	NaIprime,NaAprime,NaNprime, KIprime,KNprime,KAprime, &
	ClIprime,ClAprime,ClNprime, CaAprime,CaIprime,CaNprime,VmAprime,VmNprime, &
	GlutAprime,GlutBprime,NMDAyprime)
use ionglob
implicit none

! inputs

double precision :: NaIX,NaAX,NaNX, KIX,KNX,KAX, ClIX,ClAX,ClNX, CaAX,CaIX,CaNX
double precision :: VmAZ,VmNX,GlutAX,GlutBX,NMDAyX
double precision :: NaIprime,NaAprime,NaNprime, KIprime,KNprime,KAprime
double precision :: ClIprime,ClAprime,ClNprime, CaAprime,CaIprime,CaNprime
double precision :: VmAprime,VmNprime,GlutAprime,GlutBprime,NMDAyprime
double precision :: ATPIn

! local

double precision :: phi,dV,hinf,minf,alpha,beta,A,B,ABphi
double precision :: numerator,denominator
double precision :: EKA,ENaA,ECaA,EClA, EKN,ENaN,ECaN,EClN
double precision :: IKDRA,IKDRN, IBKA,IBKN, IKirA, IKAN,IKAA, IKMN,IKMA
double precision :: ISKA, ISKN, IIKA,IIKN
double precision :: INaFA,INaFN, INaPA,INaPN
double precision :: ICaLVAA,ICaLVAN,ICaHVAA,ICaHVAN
double precision :: IKNMDAN,INaNMDAN,ICaNMDAN
double precision :: IClpumpA,iClpumpN,ICapumpA,ICapumpN
double precision :: IKpumpA,INapumpA,IKpumpN,INapumpN
double precision :: ICaantA,INaantA,ICaantN,INaantN
double precision :: IKexchN,IClexchN,IKexchA,IClexchA
double precision :: IKastroA,INaastroA,IClastroA
double precision :: INaTotalA,IKTotalA,ICaTotalA,IClTotalA
double precision :: INaTotalN,IKTotalN,ICaTotalN,IClTotalN
double precision :: IKLeakN,INaLeakN,ICaLeakN,IClLeakN
double precision :: IKLeakA,INaLeakA,ICaLeakA,IClLeakA

! Nernst potentials

EKA=RTF*log(KIX/KAX)
ENaA=RTF*log(NaIX/NaAX)
ECaA=0.5D0*RTF*log(CaIX/CaAX);
EClA=-RTF*log(ClIX/ClAX);
EKN=RTF*log(KIX/KNX)
ENaN=RTF*log(NaIX/NaNX)
ECaN=0.5D0*RTF*log(CaIX/CaNX);
EClN=-RTF*log(ClIX/ClNX);

! K delayed rectifier

dV=VmAZ-20D0
alpha=0.0047D0*(dV+12D0)/(1D0-exp(-(dV+12D0)/12D0))
beta=exp(-(dV+147D0)/30D0)
hinf=1D0/(1D0+exp(VmAZ+25D0)/4D0)
minf=alpha/(alpha+beta)
IKDRA=gKDRA*minf*minf*hinf*(VmAZ-EKA)

dV=VmNX-20D0
alpha=0.0047D0*(dV+12D0)/(1D0-exp(-(dV+12D0)/12D0))
beta=exp(-(dV+147D0)/30D0)
hinf=1D0/(1D0+exp(VmNX+25D0)/4D0)
minf=alpha/(alpha+beta)
IKDRN=gKDRN*minf*minf*hinf*(VmNX-EKN)

! K BK channel (Ca dependent)

minf=250D0*CaNX*exp(VmNX/24)
minf=minf/(minf+0.1D0*exp(-VmNX/24D0))
IBKN=gBKN*minf*(VmNX-EKN)

minf=250D0*CaAX*exp(VmAZ/24)
minf=minf/(minf+0.1D0*exp(-VmAZ/24D0))
IBKA=gBKA*minf*(VmAZ-EKA)

! K inward rectifier (astrocyte only)

!minf=1D0/(2D0+exp((1.62D0/RTF)*(VmAZ-EKA)))
!IKirA=gKirA*minf*(KIX/(KIX+13D0))*(VmAZ-EKA)
IKirA=0D0

! K A-channel (transient outward)

!minf=1D0/(1D0+exp(-(VmNX+42D0)/13D0))
!hinf=1D0/(1D0+exp((VmNX+110D0)/18D0))
!IKAN=gKAN*minf*hinf*(VmNX-EKN)
IKAN=0D0

!minf=1D0/(1D0+exp(-(VmAZ+42D0)/13D0))
!hinf=1D0/(1D0+exp((VmAZ+110D0)/18D0))
!IKAA=gKAA*minf*hinf*(VmAZ-EKA)
IKAA=0D0

! K M-channel (non-inactivating muscarinic)

minf=1D0/(1D0+exp(-(VmNX+35D0)/10D0))
IKMN=gKMN*minf*(VmNX-EKN)

minf=1D0/(1D0+exp(-(VmAZ+35D0)/10D0))
IKMA=gKMA*minf*(VmAZ-EKA)

! K SK-channel (voltage-independent Ca-activated)

alpha=1.25D8*CaNX**2
beta=2.5D0
minf=alpha/(alpha+beta)
ISKN=gSKN*minf*minf*(VmNX-EKN)

alpha=1.25D8*CaAX**2
beta=2.5D0
minf=alpha/(alpha+beta)
ISKA=gSKA*minf*minf*(VmAZ-EKA)

! K IK-channel (K2 Ca-activated)

alpha=25D0
beta=0.075D0*exp(-(VmNX+5D0)/10D0)
minf=alpha/(alpha+beta)
IIKN=gIKN*minf*(VmNX-EKN)/(1D0+0.0002D0/CaNX)**2

alpha=25D0
beta=0.075D0*exp(-(VmAZ+5D0)/10D0)
minf=alpha/(alpha+beta)
IIKA=gIKA*minf*(VmAZ-EKA)/(1D0+0.0002D0/CaAX)**2

! Na transient (fast)

alpha=35D0*exp((VmNX+5D0)/10D0)
beta=7D0*exp(-(VmNX+65D0)/20D0)
minf=alpha/(alpha+beta)
alpha=0.225D0/(1D0+exp((VmNX+80D0)/10D0))
beta=7.5D0*exp((VmNX-3D0)/18D0)
hinf=alpha/(alpha+beta)
INaFN=gNaFN*minf**3*hinf*(VmNX-ENaN)

alpha=35D0*exp((VmAZ+5D0)/10D0)
beta=7D0*exp(-(VmAZ+65D0)/20D0)
minf=alpha/(alpha+beta)
alpha=0.225D0/(1+exp((VmAZ+80D0)/10D0))
beta=7.5D0*exp((VmAZ-3D0)/18D0)
hinf=alpha/(alpha+beta)
INaFA=gNaFA*minf**3*hinf*(VmAZ-ENaA)

! Na persistent current

alpha=200D0/(1D0+exp(-(VmAZ-18D0)/16D0))
beta=25D0/(1D0+exp((VmAZ+58D0)/8D0))
minf=alpha/(alpha+beta)
INaPA=gNaPA*minf**3*(VmAZ-ENaA)

alpha=200D0/(1+exp(-(VmNX-18D0)/16D0))
beta=25D0/(1+exp((VmNX+58D0)/8D0))
minf=alpha/(alpha+beta)
INaPN=gNaPN*minf**3*(VmNX-ENaN)

! Ca high voltage activated (P-type)

alpha=8.5D0/(1D0+exp(-(VmAZ-8D0)/12.5D0))
beta=35D0/(1D0+exp((VmAZ+74D0)/14.5D0))
minf=alpha/(alpha+beta)
alpha=0.0015D0/(1D0+exp((VmAZ+29D0)/8D0))
beta=0.0055D0/(1D0+exp(-(VmAZ+23D0)/8D0))
hinf=alpha/(alpha+beta)
ICaHVAA=gCaHVAA*minf*hinf*(VmAZ-ECaA)

alpha=8.5D0/(1+exp(-(VmNX-8D0)/12.5D0))
beta=35D0/(1+exp((VmNX+74D0)/14.5D0))
minf=alpha/(alpha+beta)
alpha=0.0015D0/(1D0+exp((VmNX+29D0)/8D0))
beta=0.0055D0/(1D0+exp(-(VmNX+23D0)/8D0))
hinf=alpha/(alpha+beta)
ICaHVAN=gCaHVAN*minf*hinf*(VmNX-ECaN)

! Ca low voltage activated (T-type)

!alpha=2.6D0/(1D0+exp(-(VmNX+21D0)/8D0))
!beta=0.018D0/(1D0+exp((VmNX+40D0)/4D0))
!minf=alpha/(alpha+beta)
!alpha=0.0025D0/(1D0+exp((VmNX+40D0)/8D0))
!beta=0.19D0/(1D0+exp(-(VmNX+50D0)/10D0))
!hinf=alpha/(alpha+beta)
!ICaLVAN=gCaLVAN*minf*hinf*(VmNX-ECaN)
ICaLVAN=0

!alpha=2.6D0/(1D0+exp(-(VmAZ+21D0)/8D0))
!beta=0.018D0/(1D0+exp((VmAZ+40D0)/4D0))
!minf=alpha/(alpha+beta)
!alpha=0.0025D0/(1D0+exp((VmAZ+40D0)/8D0))
!beta=0.19D0/(1D0+exp(-(VmAZ+50D0)/10D0))
!hinf=alpha/(alpha+beta)
!ICaLVAA=gCaLVAA*minf*hinf*(VmAZ-ECaA)
ICaLVAA=0

! NMDA receptor

NMDAyPrime=NMDAopen*GlutAX*(1.0D0-NMDAyX)-NMDAclose*NMDAyX
!A=72D0*GlutAX/(72D0*GlutAX+6.6D0)
A=NMDAyX
B=1D0/(1D0+0.28D0*exp(-0.062D0*VmNX))
phi=VmNX/RTF
ABphi=A*B*phi
IKNMDAN=NMDAKfac*ABphi*(KNX*exp(phi)-KIX)/(exp(phi)-1D0)
INaNMDAN=NMDANafac*ABphi*(NaNX*exp(phi)-NaIX)/(exp(phi)-1D0)
ICaNMDAN=NMDACafac*ABphi*(CaNX*exp(2D0*phi)-CaIX)/(exp(2D0*phi)-1D0)

! Cl pump

IClpumpA=-rClA*ClAX/(ClAX+25D0)
IClpumpN=-rClN*ClNX/(ClNX+25D0)

! Ca pump

ICapumpA=rCaA*CaAX/(CaAX+0.0002D0)
ICapumpN=rCaN*CaNX/(CaNX+0.0002D0)

! K/Na exchange

phi=(VmAZ+176.5D0)/RTF
phi=0.052D0*sinh(phi)/(0.026D0*exp(phi)+22.5D0*exp(-phi))
IKpumpA=-rNaKA*(KIX/(KIX+3.7D0))**2*(NaAX/(NaAX+0.6D0))**3*phi
INapumpA=-1.5D0*IKpumpA

phi=(VmNX+176.5D0)/RTF
phi=0.052D0*sinh(phi)/(0.026D0*exp(phi)+22.5D0*exp(-phi))
IKpumpN=-rNaKN*(KIX/(KIX+3.7D0))**2*(NaNX/(NaNX+0.6D0))**3*phi
INapumpN=-1.5D0*IKpumpN

! Na/Ca exchanger

phi=VmNX/RTF
numerator=(NaNX**3*CaIX*exp(0.35D0*phi)-NaIX**3*CaNX*2.5D0*exp(-0.65D0*phi))
denominator=(87.5D0**3+NaIX**3)*(1.38D0+CaIX)*(1D0+0.1D0*exp(-0.65D0*phi))
ICaantN=-rNaCaN*numerator/denominator
INaantN=-1.5D0*ICaantN

phi=VmAZ/RTF
numerator=(NaAX**3*CaIX*exp(0.35D0*phi)-NaIX**3*CaAX*2.5D0*exp(-0.65D0*phi))
denominator=(87.5D0**3+NaIX**3)*(1.38D0+CaIX)*(1D0+0.1D0*exp(-0.65D0*phi))
ICaantA=-rNaCaA*numerator/denominator
INaantA=-1.5D0*ICaantA

! K/Cl transporter

IKexchN=gKClN*RTF*log((KNX/KIX)*(ClNX/ClIX))
IClexchN=-IKexchN

IKexchA=gKClA*RTF*log((KAX/KIX)*(ClAX/ClIX))
IClexchA=-IKexchA

! Na/K/Cl transporter

IKastroA=-gNaKClA*RTF*log((NaIX/NaAX)*(KIX/KAX)*(ClIX/ClAX)**2)
INaastroA=IKastroA
IClastroA=-2D0*IKastroA

! ==== leaks ====

IKLeakN=gKLeakN*(VmNX-EKN)
INaLeakN=gNaLeakN*(VmNX-ENaN)
ICaLeakN=gCaLeakN*(VmNX-ECaN)
IClLeakN=gClLeakN*(VmNX-EClN)
IKLeakA=gKLeakA*(VmAZ-EKA)
INaLeakA=gNaLeakA*(VmAZ-ENaA)
ICaLeakA=gCaLeakA*(VmAZ-ECaA)
IClLeakA=gClLeakA*(VmAZ-EClA)

! Total currents - these to be in pA/um2

IKTotalN=IKLeakN+IKDRN+IBKN+IKAN+IKMN+ISKN+IIKN+IKNMDAN+IKpumpN+IKexchN
INaTotalN=INaLeakN+INaFN+INaPN+INaNMDAN+INapumpN+INaantN
ICaTotalN=ICaLeakN+ICaHVAN+ICaLVAN+ICaNMDAN+ICapumpN+ICaantN
IClTotalN=IClLeakN+IClpumpN+IClexchN
IKTotalA=IKLeakA+IKDRA+IBKA+IKirA+IKAA+IKMA+ISKA+IIKA+IKpumpA+IKexchA+IKastroA
INaTotalA=INaLeakA+INaFA+INaPA+INapumpA+INaantA+INaastroA
ICaTotalA=ICaLeakA+ICaHVAA+ICaLVAA+ICapumpA+ICaantA
IClTotalA=IClLeakA+IClpumpA+IClexchA+IClastroA

! Derivatives

KNprime=IKTotalN*ConvKN
NaNprime=INaTotalN*ConvNaN
CaNprime=ICaTotalN*ConvCaN
ClNprime=IClTotalN*ConvClN
KAprime=IKTotalA*ConvKA
NaAprime=INaTotalA*ConvNaA
CaAprime=ICaTotalA*ConvCaA
ClAprime=IClTotalA*ConvClA
KIprime=-(KNprime*epsN+KAprime*epsA)
NaIprime=-(NaAprime*epsA+NaNprime*epsN)
CaIprime=-(CaAprime*epsA+CaNprime*epsN)
ClIprime=-(ClAprime*epsA+ClNprime*epsN)

VmAprime=-(INaTotalA+IKTotalA+ICaTotalA+IClTotalA)*QCmem
VmNprime=-(INaTotalN+IKTotalN+ICaTotalN+IClTotalN)*QCmem

CaNprime=CaNprime*CaBuffFact
CaAprime=CaAprime*CaBuffFact

GlutAPrime=astglurate/(1.0D0+7.0036D0*ATPIn**(-0.9828))	&
	-GluUptRate*GlutAX
GlutBPrime=neuglurate*exp(-0.0044D0*(VmNX-8.6573D0)**2)-GluUptRate*GlutBX
end subroutine IonDerivs

!-------------
! Loop over series of compartments
!-------------
! Note: this doesn't properly interface the stepping because of the backward spatial
! reference to GlutB. I'm leaving this alone for the moment because there are other
! comparable errors in linking all this to the ATP story.

subroutine StepIons
use ionglob
use global
implicit none
integer :: i,lowx,mcell,nxblock
integer :: ition	! time counter
double precision :: ATPX

nxblock=nXsteps/nblock
mcell=(ncell-1)/2
if (nxblock*nblock+mcell+1.GT.nXsteps) nxblock=nxblock-1
lowx=-nxblock
IF (lxsymm) THEN
	lowx=0
ENDIF

do ition=1,iontimeratio
	do i=lowx,nxblock
		call GetATP(i,ATPX)
		call IonODEs(NaI(i),NaA(i),NaN(i), KJ(i),KN(i),KA(i),	&
		ClI(i),ClA(i),ClN(i), CaA(i),CaI(i),CaN(i), VmA(i),VmN(i),	&
		GlutA(i),GlutB(i),NMDAy(i),ATPX)
	enddo
enddo
end subroutine StepIons

!-------------
! Average the local ATP concentration around the astrocyte
!-------------

subroutine GetATP(iastro,ATPX)
use global
implicit none
integer :: iastro,ixcentre
integer :: ix,iy,iz,mcell,countATP,jx,jy,jz
double precision :: ATPX,sumATP

ixcentre=iastro*nblock
mcell=(ncell+1)/2
sumATP=0.0D0
countATP=0
do ix=ixcentre-mcell,ixcentre+mcell
	jx=ix
	if (lxsymm) jx=abs(jx)
	do iy=-mcell,mcell
		jy=iy
		if (lysymm) jy=abs(jy)
		do iz=-mcell,mcell
			jz=iz
			if (lzsymm) jz=abs(jz)
			if (icell(jx,jy,jz).eq.cextmem) then
				sumATP=sumATP+ATP(jx,jy,jz)
				countATP=countATP+1
			endif
		enddo
	enddo
enddo
ATPX=sumATP/countATP
end subroutine GetATP

!-------------
! Retrieve the glutamate concentration near the astrocyte
! This is used inside step.f90
!-------------

subroutine GetGlutB(ix,iy,iz,GlutBX)
use ionglob
use global
implicit none
integer :: ix,iy,iz,iastro
double precision :: GlutBX

iastro=int(anint(real(ix)/nblock))
if (lxsymm) iastro=abs(iastro)
GlutBX=GlutB(iastro)
end subroutine GetGlutB
