!
! Copyright (c) Rep2D v1.2 2012  - Alberto Lorenzo (alorenzo.md@gmail.com)
!
! Distributed under the MIT License.
! (See accompanying file "copying" or copy at
! http://opensource.org/licenses/MIT)
!

module draw

    use dislin
    implicit none

    character(len = 6), parameter :: colors(6) = (/'red   ', 'orange', 'yellow', 'green ', &
        'cyan  ', 'blue  '/)

    integer :: m_draw

    character(len = 3)  :: mode
    real(kind = 8)      :: xmin, xmax, ymin, ymax
    character(len = 65) :: ctitle
    character(len = 15) :: xtitle, ytitle, ztitle
    integer             :: axs = 1

    real(kind = 8), allocatable :: u(:, :)
    integer :: gpx, gpy

    real(kind = 8) :: level(6)
    integer :: checked(6)

    contains

    subroutine draw_screen()

        real(kind = 8) :: xstep, ystep
        real(kind = 8) :: zmin, zmax, zstep

        integer :: i

        xstep = abs(xmax - xmin) / 1d1
        ystep = abs(ymax - ymin) / 1d1
        zmin = 1d0 * int(minval(u(:, :)))
        zmax = 1d0 * nint(maxval(u(:, :)))
        zstep = abs(zmax - zmin) / 1d1

        call metafl('cons')
        call setxid(m_draw, 'widget')
        call page(3000, 3000)
        call scrmod('norev')
        call disini()
        call erase()
        call pagera
        call hwfont()
        call eushft('acute','`')
        call texmod('on')
        call errmod('all', 'off')
        call setvlt('rain')
        call height(40)
        call hname(50)
        if(mode == 'sur') call autres(gpx, gpy)
        if(axs == 1 .and. mode == 'iso' .and. xmin /= 0d0 .and. ymin/= 0d0) then
            call axstyp('cross')
        else
            call axstyp('rect')
        end if
        if(mode == 'iso') then
            call axspos(475, 2600)
            call axslen(2200, 2200)
        else
            call axspos(300, 2600)
            call ax3len(2200, 2200, 2200)
        end if
        call titlin(ctitle, 3)
        call labdig(1, 'xyz')
        call name(xtitle, 'x')
        call name(ytitle, 'y')
        if(mode /= 'iso') then
            call name(ztitle, 'z')
            call shdmod('cell', 'contur')
            call graf3(xmin, xmax, xmin, xstep, ymin, ymax, xmin, ystep, zmin, zmax, zmin, zstep)
            call height(50)
            call title()
            if(mode == 'sur') then
                call crvmat(u(:, :), gpx, gpy, 1, 1)
            elseif(mode == 'int') then
                call crvmat(u(:, :), gpx, gpy, 500 / gpx, 500 / gpy)
            end if
        else
            call messag(ztitle, 2450, 2800)
            call graf(xmin, xmax, xmin, xstep, ymin, ymax, ymin, ystep)
            call solid()
            call thkcrv(2)
            call labdig(1, 'contur')
            call labels('float', 'contur')
            call height(50)
            call title()
            call height(35)
            do i = 1, 6
                if(checked(i) == 1) then
                    call color(colors(i))
                    call conmat(u, gpx, gpy, level(i))
                end if
            end do
            call color ('white')
        end if
        call disfin()

    end subroutine draw_screen

    subroutine export_PDF(cfile)

        character(len = 256), intent(in) :: cfile

        real(kind = 8) :: xstep, ystep
        real(kind = 8) :: zmin, zmax, zstep

        integer :: i

        xstep = abs(xmax - xmin) / 1d1
        ystep = abs(ymax - ymin) / 1d1
        zmin = 1d0 * int(minval(u(:, :)))
        zmax = 1d0 * nint(maxval(u(:, :)))
        zstep = abs(zmax - zmin) / 1d1

        call setfil(cfile)
        call filmod('delete')
        call metafl('pdf')
        call page(3000, 3000)
        call scrmod('revers')
        call disini()
        call erase()
        call pagera
        call hwfont()
        call eushft('acute','`')
        call texmod('on')
        call errmod('all', 'off')
        call setvlt('rain')
        call height(40)
        call hname(50)
        if(mode == 'sur') call autres(gpx, gpy)
        if(axs == 1 .and. mode == 'iso' .and. xmin /= 0d0 .and. ymin/= 0d0) then
            call axstyp('cross')
        else
            call axstyp('rect')
        end if
        if(mode == 'iso') then
            call axspos(475, 2600)
            call axslen(2200, 2200)
        else
            call axspos(300, 2600)
            call ax3len(2200, 2200, 2200)
        end if
        call titlin(ctitle, 3)
        call labdig(1, 'xyz')
        call name(xtitle, 'x')
        call name(ytitle, 'y')
        if(mode /= 'iso') then
            call name(ztitle, 'z')
            call shdmod('cell', 'contur')
            call graf3(xmin, xmax, xmin, xstep, ymin, ymax, ymin, ystep, zmin, zmax, zmin, zstep)
            call height(50)
            call title()
            if(mode == 'sur') then
                call crvmat(u(:, :), gpx, gpy, 1, 1)
            elseif(mode == 'int') then
                call crvmat(u(:, :), gpx, gpy, 550 / (gpx - 1), 550 / (gpy - 1))
            end if
        else
            call messag(ztitle, 2450, 2800)
            call graf(xmin, xmax, xmin, xstep, ymin, ymax, ymin, ystep)
            call solid()
            call thkcrv(2)
            call labdig(1, 'contur')
            call labels('float', 'contur')
            call height(50)
            call title()
            call height(35)
            do i = 1, 6
                if(checked(i) == 1) then
                    call color(colors(i))
                    call conmat(u, gpx, gpy, level(i))
                end if
            end do
            call color ('white')
        end if
        call disfin()

    end subroutine export_PDF

end module draw
