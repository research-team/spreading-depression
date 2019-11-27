!
! file.f90
!

! If a run number is given
!	Atime.999		Aspace.txt		Asection.txt
!	Ctime.999		Cspace.txt		Csection.txt
!	Cpeak.999
!	Cpeaktime.999
!	Itime.999
!	Ptime.999
!				total.txt
! This gives a set of time series identified by the run number and
! more or less meaningless sections at the end

! If movies are required
!	Atime.txt		Aspace.txt (reset)	Asection.0 (reset .1, .2 etc)
!	Ctime.txt		Cspace.txt (reset)	Csection.0 (reset .1, .2 etc)
!	Cpeak.txt (reset)
!	Cpeaktime.txt (reset)
!	Itime.txt
!	Ptime.txt
!				total.txt
! This gives a set of time series for one run, with cross sections at
! sundry times

! If neither
!	Atime.txt		Aspace.txt		Asection.txt
!	Ctime.txt		Cspace.txt		Csection.txt
!	Cpeak.txt
!	Cpeaktime.txt
!	Itime.txt
!	Ptime.txt
!				total.txt
! This gives a set of time series for one run, with cross sections at the end

! If both
!	Atime.999		Aspace.txt (reset)	Asection.0 (reset .1, .2 etc)
!	Ctime.999		Cspace.txt (reset)	Csection.0 (reset .1, .2 etc)
!	Cpeak.999 (reset as Cpeak.txt)
!	Cpeaktime.999 (reset as Cpeak.txt)
!	Itime.999
!	Ptime.999
!				total.txt
! This is pointless since sections for only one run result


!------------------
! Open output files
!------------------
subroutine OpenOutput
use global
implicit none
character*9 :: fname
fname='Atime.txt'
IF (irunno.GT.0) THEN
	IF (irunno.LT.10) THEN
		fname(7:7)=char(irunno+ichar('0'))
		fname(8:8)=' '
		fname(9:9)=' '
	ELSEIF (irunno.LT.100) THEN
		fname(7:7)=char(irunno/10+ichar('0'))
		fname(8:8)=char(mod(irunno,10)+ichar('0'))
		fname(9:9)=' '
	ELSE
		fname(7:7)=char(irunno/100+ichar('0'))
		fname(8:8)=char(mod(irunno,100)/10+ichar('0'))
		fname(9:9)=char(mod(irunno,10)+ichar('0'))
	ENDIF
ENDIF
!
! ATP
!
open(11, file=fname)	! ie Atime.nnn
if (movietime.GT.0.0D0) then
	open(13, file='Asection.0')
else
	open(13, file='Asection.txt')
endif
!
! Ca
!
fname(1:1)='C'
open(21, file=fname)	! ie Ctime.nnn
if (movietime.GT.0.0D0) then
	open(23, file='Csection.0')
else
	open(23, file='Csection.txt')
endif
!
! IP3
!
fname(1:5)='Itime'
open(31, file=fname)	! ie Itime.nnn
!
! Desensitisation
!
fname(1:1)='P'
open(41, file=fname)	! ie Ptime.nnn
!
! Ion files
!
call IOpenOutput(fname)
!
! Supplementary files
!
fname(5:5)='2'
fname(1:1)='A'
open(16, file=fname)	! ie Atim2.nnn
fname(1:1)='C'
open(26, file=fname)	! ie Ctim2.nnn
fname(1:1)='I'
open(36, file=fname)	! ie Itim2.nnn
fname(1:1)='P'
open(46, file=fname)	! ie Ptim2.nnn
end subroutine OpenOutput
!-------------------
! Close output files
!-------------------
subroutine CloseOutput
implicit none
close(11)
close(13)
close(21)
close(23)
close(31)
close(41)
close(16)
close(26)
close(36)
close(46)
call ICloseOutput
end subroutine CloseOutput
!------------------
! Reset output file
! This only happens if we are generating a movie. If so,
! then the file naming scheme is incompatible with that used for
! numbering different runs, so movie data files must not do 
! multiple runs
!------------------
subroutine ResetOutput(iitime)
implicit none
integer :: iitime
character*12 :: fname
close(23)
fname='Csection.???'
IF (iitime.LT.10) THEN
	fname(10:10)=char(iitime+ichar('0'))
	fname(11:11)=' '
	fname(12:12)=' '
ELSEIF (iitime.LT.100) THEN
	fname(10:10)=char(iitime/10+ichar('0'))
	fname(11:11)=char(mod(iitime,10)+ichar('0'))
	fname(12:12)=' '
ELSE
	fname(10:10)=char(iitime/100+ichar('0'))
	fname(11:11)=char(mod(iitime,100)/10+ichar('0'))
	fname(12:12)=char(mod(iitime,10)+ichar('0'))
ENDIF
open(23, file=fname)
close(13)
fname(1:1)='A'
open(13, file=fname)
end subroutine ResetOutput
!-----------------
! Save time series
!-----------------
subroutine SaveResults
use global
implicit none
integer :: mcell,xAM,yAM
integer :: ix,iy,iz,xtest
double precision :: fixout
integer :: pickset,pp,pq,pr

! ATP time series just outside astrocytes

xtest=(ncell+1)/2
xAM=0
yAM=(ncell+1)/2
IF (startcellx.LT.0) then
	XAM=XAM+startcellx*nblock
	xtest=xtest+startcellx*nblock
ENDIF
DO pickset=1,2
IF (pickset.eq.1) THEN
	pp=11
ELSE
	pp=16
ENDIF
IF (xtest.GT.nxSteps) THEN	! this is only for pickset=2
ELSEIF (xtest+nblock.GT.nXSteps) THEN
	write(pp,'(2E15.7)')t,fixout(ATP(xAM,yAM,0))
ELSEIF (xtest+2*nblock.GT.nXSteps) THEN
	write(pp,'(3E15.7)')t,fixout(ATP(xAM,yAM,0)),	&
		fixout(ATP(nblock+xAM,yAM,0))
ELSEIF (xtest+3*nblock.GT.nXSteps) THEN
	write(pp,'(4E15.7)')t,fixout(ATP(xAM,yAM,0)),	&
		fixout(ATP(nblock+xAM,yAM,0)),fixout(ATP(2*nblock+xAM,yAM,0))
ELSEIF (xtest+4*nblock.GT.nXSteps) THEN
	write(pp,'(5E15.7)')t,fixout(ATP(xAM,yAM,0)),	&
		fixout(ATP(nblock+xAM,yAM,0)),fixout(ATP(2*nblock+xAM,yAM,0)),	&
		fixout(ATP(3*nblock+xAM,yAM,0))
ELSEIF (xtest+5*nblock.GT.nXSteps) THEN
	write(pp,'(6E15.7)')t,fixout(ATP(xAM,yAM,0)),	&
		fixout(ATP(nblock+xAM,yAM,0)),fixout(ATP(2*nblock+xAM,yAM,0)),	&
		fixout(ATP(3*nblock+xAM,yAM,0)),fixout(ATP(4*nblock+xAM,yAM,0))
ELSEIF (xtest+6*nblock.GT.nXSteps) THEN
	write(pp,'(7E15.7)')t,fixout(ATP(xAM,yAM,0)),	&
		fixout(ATP(nblock+xAM,yAM,0)),fixout(ATP(2*nblock+xAM,yAM,0)),	&
		fixout(ATP(3*nblock+xAM,yAM,0)),fixout(ATP(4*nblock+xAM,yAM,0)),&
		fixout(ATP(5*nblock+xAM,yAM,0))
ELSEIF (xtest+7*nblock.GT.nXSteps) THEN
	write(pp,'(8E15.7)')t,fixout(ATP(xAM,yAM,0)),	&
		fixout(ATP(nblock+xAM,yAM,0)),fixout(ATP(2*nblock+xAM,yAM,0)),	&
		fixout(ATP(3*nblock+xAM,yAM,0)),fixout(ATP(4*nblock+xAM,yAM,0)),&
		fixout(ATP(5*nblock+xAM,yAM,0)),fixout(ATP(6*nblock+xAM,yAM,0))
ELSE
	write(pp,'(9E15.7)')t,fixout(ATP(xAM,yAM,0)),	&
		fixout(ATP(nblock+xAM,yAM,0)),fixout(ATP(2*nblock+xAM,yAM,0)),	&
		fixout(ATP(3*nblock+xAM,yAM,0)),fixout(ATP(4*nblock+xAM,yAM,0)),&
		fixout(ATP(5*nblock+xAM,yAM,0)),fixout(ATP(6*nblock+xAM,yAM,0)),&
		fixout(ATP(7*nblock+xAM,yAM,0))
ENDIF

! Ca time series just inside astrocytes

yAM=yAM-1
IF (pickset.eq.1) THEN
	pp=21
	pq=31
	pr=41
ELSE
	pp=26
	pq=36
	pr=46
ENDIF
IF (xtest.GT.nxSteps) THEN	! this is only for pickset=2
ELSEIF (xtest+nblock.GT.nXSteps) THEN
	write(pp,'(2E15.7)')t,Ca(xAM,yAM,0)
	write(pq,'(2E15.7)')t,IP3(xAM,yAM,0)
	write(pr,'(2E15.7)')t,AStore(xAM,yAM,0)
ELSEIF (xtest+2*nblock.GT.nXSteps) THEN
	write(pp,'(3E15.7)')t,Ca(xAM,yAM,0),Ca(xAM+nblock,yAM,0)
	write(pq,'(3E15.7)')t,IP3(xAM,yAM,0),IP3(xAM+nblock,yAM,0)
	write(pr,'(3E15.7)')t,AStore(xAM,yAM,0),AStore(xAM+nblock,yAM,0)
ELSEIF (xtest+3*nblock.GT.nXSteps) THEN
	write(pp,'(4E15.7)')t,Ca(xAM,yAM,0),Ca(xAM+nblock,yAM,0),	&
		Ca(xAM+2*nblock,yAM,0)
	write(pq,'(4E15.7)')t,IP3(xAM,yAM,0),IP3(xAM+nblock,yAM,0),	&
		IP3(xAM+2*nblock,yAM,0)
	write(pr,'(4E15.7)')t,AStore(xAM,yAM,0),AStore(xAM+nblock,yAM,0),	&
		AStore(xAM+2*nblock,yAM,0)
ELSEIF (xtest+4*nblock.GT.nXSteps) THEN
	write(pp,'(5E15.7)')t,Ca(xAM,yAM,0),Ca(xAM+nblock,yAM,0),	&
		Ca(xAM+2*nblock,yAM,0),Ca(xAM+3*nblock,yAM,0)
	write(pq,'(5E15.7)')t,IP3(xAM,yAM,0),IP3(xAM+nblock,yAM,0),	&
		IP3(xAM+2*nblock,yAM,0),IP3(xAM+3*nblock,yAM,0)
	write(pr,'(5E15.7)')t,AStore(xAM,yAM,0),AStore(xAM+nblock,yAM,0),	&
		AStore(xAM+2*nblock,yAM,0),AStore(xAM+3*nblock,yAM,0)
ELSEIF (xtest+5*nblock.GT.nXSteps) THEN
	write(pp,'(6E15.7)')t,Ca(xAM,yAM,0),Ca(xAM+nblock,yAM,0),	&
		Ca(xAM+2*nblock,yAM,0),Ca(xAM+3*nblock,yAM,0),	&
		Ca(xAM+4*nblock,yAM,0)
	write(pq,'(6E15.7)')t,IP3(xAM,yAM,0),IP3(xAM+nblock,yAM,0),	&
		IP3(xAM+2*nblock,yAM,0),IP3(xAM+3*nblock,yAM,0),	&
		IP3(xAM+xAM+4*nblock,yAM,0)
	write(pr,'(6E15.7)')t,AStore(xAM,yAM,0),AStore(xAM+nblock,yAM,0),	&
		AStore(xAM+2*nblock,yAM,0),AStore(xAM+3*nblock,yAM,0),	&
		AStore(xAM+4*nblock,yAM,0)
ELSEIF (xtest+6*nblock.GT.nXSteps) THEN
	write(pp,'(7E15.7)')t,Ca(xAM,yAM,0),Ca(xAM+nblock,yAM,0),	&
		Ca(xAM+2*nblock,yAM,0),Ca(xAM+3*nblock,yAM,0),	&
		Ca(xAM+4*nblock,yAM,0),Ca(xAM+5*nblock,yAM,0)
	write(pq,'(7E15.7)')t,IP3(xAM,yAM,0),IP3(xAM+nblock,yAM,0),	&
		IP3(xAM+2*nblock,yAM,0),IP3(xAM+3*nblock,yAM,0),	&
		IP3(xAM+xAM+4*nblock,yAM,0),IP3(xAM+xAM+5*nblock,yAM,0)
	write(pr,'(7E15.7)')t,AStore(xAM,yAM,0),AStore(xAM+nblock,yAM,0),	&
		AStore(xAM+2*nblock,yAM,0),AStore(xAM+3*nblock,yAM,0),	&
		AStore(xAM+4*nblock,yAM,0),AStore(xAM+5*nblock,yAM,0)
ELSEIF (xtest+7*nblock.GT.nXSteps) THEN
	write(pp,'(8E15.7)')t,Ca(xAM,yAM,0),Ca(xAM+nblock,yAM,0),	&
		Ca(xAM+2*nblock,yAM,0),Ca(xAM+3*nblock,yAM,0),	&
		Ca(xAM+4*nblock,yAM,0),Ca(xAM+5*nblock,yAM,0),	&
		Ca(xAM+6*nblock,yAM,0)
	write(pq,'(8E15.7)')t,IP3(xAM,yAM,0),IP3(xAM+nblock,yAM,0),	&
		IP3(xAM+2*nblock,yAM,0),IP3(xAM+3*nblock,yAM,0),	&
		IP3(xAM+4*nblock,yAM,0),IP3(xAM+5*nblock,yAM,0),	&
		IP3(xAM+6*nblock,yAM,0)
	write(pr,'(8E15.7)')t,AStore(xAM,yAM,0),AStore(xAM+nblock,yAM,0),	&
		AStore(xAM+2*nblock,yAM,0),AStore(xAM+3*nblock,yAM,0),	&
		AStore(xAM+4*nblock,yAM,0),AStore(xAM+5*nblock,yAM,0),	&
		AStore(xAM+6*nblock,yAM,0)
ELSE
	write(pp,'(9E15.7)')t,Ca(xAM,yAM,0),Ca(xAM+nblock,yAM,0),	&
		Ca(xAM+2*nblock,yAM,0),Ca(xAM+3*nblock,yAM,0),	&
		Ca(xAM+4*nblock,yAM,0),Ca(xAM+5*nblock,yAM,0),	&
		Ca(xAM+6*nblock,yAM,0),Ca(xAM+7*nblock,yAM,0)
	write(pq,'(9E15.7)')t,IP3(xAM,yAM,0),IP3(xAM+nblock,yAM,0),	&
		IP3(xAM+2*nblock,yAM,0),IP3(xAM+3*nblock,yAM,0),	&
		IP3(xAM+4*nblock,yAM,0),IP3(xAM+5*nblock,yAM,0),	&
		IP3(xAM+6*nblock,yAM,0),IP3(xAM+7*nblock,yAM,0)
	write(pr,'(9E15.7)')t,AStore(xAM,yAM,0),AStore(xAM+nblock,yAM,0),	&
		AStore(xAM+2*nblock,yAM,0),AStore(xAM+3*nblock,yAM,0),	&
		AStore(xAM+4*nblock,yAM,0),AStore(xAM+5*nblock,yAM,0),	&
		AStore(xAM+6*nblock,yAM,0),AStore(xAM+7*nblock,yAM,0)
ENDIF
yAM=yAM+1
xtest=xtest+8*nblock
xAM=xAM+8*nblock;
ENDDO
call ISaveResults
end subroutine SaveResults

!------------------------
! Save spatial variations
!------------------------
subroutine SaveFinal
use global
implicit none
integer :: ix,iy,lowx,lowy,mcell
double precision :: fixout

lowx=-nXsteps
lowy=-nYsteps
if (lxsymm) lowx=0

mcell=(ncell-1)/2

! Section through centre

if (lxsymm) then
	if (lysymm) then
		do iy=nYsteps,0,-1
			write(13,'(E15.7)')(fixout(ATP(ix,iy,0)),ix=nXSteps,0,-1)
			write(13,'(E15.7)')(fixout(ATP(ix,iy,0)),ix=1,nXSteps)
			write(23,'(E15.7)')(Ca(ix,iy,0),ix=nXSteps,0,-1)
			write(23,'(E15.7)')(Ca(ix,iy,0),ix=1,nXSteps)
		enddo
		do iy=1,nYsteps
			write(13,'(E15.7)')(fixout(ATP(ix,iy,0)),ix=nXSteps,0,-1)
			write(13,'(E15.7)')(fixout(ATP(ix,iy,0)),ix=1,nXSteps)
			write(23,'(E15.7)')(Ca(ix,iy,0),ix=nXSteps,0,-1)
			write(23,'(E15.7)')(Ca(ix,iy,0),ix=1,nXSteps)
		enddo
	else
		do iy=-nYsteps,nYsteps
			write(13,'(E15.7)')(fixout(ATP(ix,iy,0)),ix=nXSteps,0,-1)
			write(13,'(E15.7)')(fixout(ATP(ix,iy,0)),ix=1,nXSteps)
			write(23,'(E15.7)')(Ca(ix,iy,0),ix=nXSteps,0,-1)
			write(23,'(E15.7)')(Ca(ix,iy,0),ix=1,nXSteps)
		enddo
	endif
else if (lysymm) then
	write(13,'(E15.7)')((fixout(ATP(ix,iy,0)),ix=-nXSteps,nXSteps),	&
		iy=nYSteps,0,-1)
	write(13,'(E15.7)')((fixout(ATP(ix,iy,0)),ix=-nXSteps,nXSteps),	&
		iy=1,nYSteps)
	write(23,'(E15.7)')((Ca(ix,iy,0),ix=-nXSteps,nXSteps),	&
		iy=nYSteps,0,-1)
	write(23,'(E15.7)')((Ca(ix,iy,0),ix=-nXSteps,nXSteps),	&
		iy=1,nYSteps)
else
	write(13,'(E15.7)')((fixout(ATP(ix,iy,0)),ix=-nXSteps,nXSteps),	&
		iy=-nYSteps,nYSteps)
	write(23,'(E15.7)')((Ca(ix,iy,0),ix=-nXSteps,nXSteps),	&
		iy=-nYSteps,nYSteps)
endif
end subroutine SaveFinal

function fixout(valin) result (valout)
implicit none
double precision :: valin,valout

if (abs(valin).GT.1d-99) then
	valout=valin
else
	valout=1d-99
endif
end function fixout
