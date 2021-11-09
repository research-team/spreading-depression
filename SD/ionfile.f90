subroutine IOpenOutput(fname)
use global
implicit none
character*9 :: fname
character*10 :: gname1,gname2,gname3
gname1(3:10)=fname(2:9)
gname2(3:10)=fname(2:9)
gname3(3:10)=fname(2:9)
gname1(2:2)='I'
gname2(2:2)='A'
gname3(2:2)='N'
!
! potassium
!
gname1(1:1)='K'
gname2(1:1)='K'
gname3(1:1)='K'
open(51, file=gname1)	! ie KItime.nnn
open(61, file=gname2)	! ie KAtime.nnn
open(71, file=gname3)	! ie KNtime.nnn
!
! sodium
!
gname1(1:1)='N'
gname2(1:1)='N'
gname3(1:1)='N'
open(52, file=gname1)	! ie NItime.nnn
open(62, file=gname2)	! ie NAtime.nnn
open(72, file=gname3)	! ie NNtime.nnn
!
! calcium
!
gname1(1:1)='D'
gname2(1:1)='D'
gname3(1:1)='D'
open(53, file=gname1)	! ie DItime.nnn
open(63, file=gname2)	! ie DAtime.nnn
open(73, file=gname3)	! ie DNtime.nnn
!
! chlorine
!
gname1(1:1)='L'
gname2(1:1)='L'
gname3(1:1)='L'
open(54, file=gname1)	! ie LItime.nnn
open(64, file=gname2)	! ie LAtime.nnn
open(74, file=gname3)	! ie LNtime.nnn
!
! membrane potential
!
gname2(1:1)='V'
gname3(1:1)='V'
open(65, file=gname2)	! ie VAtime.nnn
open(75, file=gname3)	! ie VNtime.nnn
!
! glutamate
!
fname(1:1)='G'
open(56, file=fname)	! ie Gtime.nnn
fname(1:1)='H'
open(57, file=fname)	! ie HTime.nnn
end subroutine IOpenOutput

subroutine ICloseOutput
implicit none
close(51)
close(52)
close(53)
close(54)
close(56)
close(57)
close(61)
close(62)
close(63)
close(64)
close(65)
close(71)
close(72)
close(73)
close(74)
close(75)
end subroutine ICloseOutput

subroutine ISaveResults
use global
use ionglob
implicit none
integer ix,lowx,highx,nxblock,mcell
double precision :: fixout

nxblock=nXsteps/nblock
mcell=(ncell-1)/2
! If we were to use sealed boundaries then this should read GE
if (nxblock*nblock+mcell+1.GT.nXsteps) nxblock=nxblock-1
lowx=-nxblock
IF (lxsymm) THEN
	lowx=0
ENDIF
if (lowx.lt.startcellx) lowx=startcellx

highx=lowx+7
if (highx.gt.nxblock) highx=nxblock

write(51,'(9E15.7)')t,(KJ(ix),ix=lowx,highx)
write(52,'(9E15.7)')t,(NaI(ix),ix=lowx,highx)
write(53,'(9E15.7)')t,(CaI(ix),ix=lowx,highx)
write(54,'(9E15.7)')t,(ClI(ix),ix=lowx,highx)
write(56,'(9E15.7)')t,(fixout(GlutA(ix)),ix=lowx,highx)
write(57,'(9E15.7)')t,(fixout(GlutB(ix)),ix=lowx,highx)
write(61,'(9E15.7)')t,(KA(ix),ix=lowx,highx)
write(62,'(9E15.7)')t,(NaA(ix),ix=lowx,highx)
write(63,'(9E15.7)')t,(CaA(ix),ix=lowx,highx)
write(64,'(9E15.7)')t,(ClA(ix),ix=lowx,highx)
write(65,'(9E15.7)')t,(VmA(ix),ix=lowx,highx)
write(71,'(9E15.7)')t,(KN(ix),ix=lowx,highx)
write(72,'(9E15.7)')t,(NaN(ix),ix=lowx,highx)
write(73,'(9E15.7)')t,(CaN(ix),ix=lowx,highx)
write(74,'(9E15.7)')t,(ClN(ix),ix=lowx,highx)
write(75,'(9E15.7)')t,(VmN(ix),ix=lowx,highx)
end subroutine ISaveResults
