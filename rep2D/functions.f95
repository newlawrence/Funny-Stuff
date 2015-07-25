!
! Copyright (c) Rep2D v1.2 2012  - Alberto Lorenzo (alorenzo.md@gmail.com)
!
! Distributed under the MIT License.
! (See accompanying file "copying" or copy at
! http://opensource.org/licenses/MIT)
!

module functions

    use dislin
    implicit none

    integer, parameter :: gpmax=40000

    contains

    subroutine guess_dimensions(IDfile, gpx, gpy)

        integer, intent(in) :: IDfile
        integer, intent(out) :: gpx, gpy

        real(kind = 8) :: dum(gpmax)
        integer :: i, IOerror

        gpx = 0
        read(IDfile, *, iostat = IOerror) (dum(i), i = 1, gpmax)
        if(IOerror < 0) then
            gpx = i - 1
        else
            gpx = gpmax
        end if
        rewind(IDfile)
        gpy = 0
        do
            read(IDfile, *, iostat = IOerror) dum(1)
            if(IOerror < 0) exit
            gpy = gpy + 1
        end do
        gpx = gpx / gpy
        rewind(IDfile)

    end subroutine guess_dimensions

end module functions
