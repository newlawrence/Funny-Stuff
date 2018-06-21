!
! Copyright (c) Rep2D v1.2 2012  - Alberto Lorenzo (alorenzo.md@gmail.com)
!
! Distributed under the MIT License.
! (See accompanying file "copying" or copy at
! http://opensource.org/licenses/MIT)
!

module callback

    use functions
    use draw
    implicit none

    integer :: m
    integer :: m_fil, m_fil_opn, m_fil_pdf
    integer :: m_vis, m_vis_lev, m_vis_sur, m_vis_int
    integer :: m_prop, m_prop_edt, m_prop_inv
    integer :: m_help, m_help_abt

    contains

    subroutine load_matrix(id)

        integer, intent(in) :: id

        character(len = 256) :: cfile

        integer :: i
        integer :: IDfile, IOerror

        if(allocated(u)) deallocate(u)
        cfile = ''
        call dwgfil('Seleccionar fichero de datos', cfile, '*.dat')
        if(cfile /= 'none') then
            IDfile = 100
            open(unit = IDfile, file = cfile, status = 'old', action = 'read', iostat = IOerror)
            if(IOerror == 0) then
                call guess_dimensions(IDfile, gpx, gpy)
                allocate(u(0 : gpx - 1, 0 : gpy - 1), stat = IOerror)
                if(IOerror > 0) then
                    call dwgmsg('Error: memoria insuficiente')
                else
                    do i = gpy - 1, 0, -1
                        read(IDfile, *) u(:, i)
                    end do
                end if
                close(IDfile)
            end if
        end if
        if(allocated(u)) call draw_screen()

    end subroutine load_matrix

    subroutine export_matrix(id)

        integer, intent(in) :: id

        character(len = 256) :: cfile
        if(allocated(u)) then
            cfile = ''
            call dwgfil('Exportar como PDF', cfile, '*.pdf')
            call export_PDF(cfile)
        end if

    end subroutine export_matrix

    subroutine view_levels(id)

        integer, intent(in) :: id

        integer :: t
        integer :: t_bas1, t_chk1, t_lvl1
        integer :: t_bas2, t_chk2, t_lvl2
        integer :: t_bas3, t_chk3, t_lvl3
        integer :: t_bas4, t_chk4, t_lvl4
        integer :: t_bas5, t_chk5, t_lvl5
        integer :: t_bas6, t_chk6, t_lvl6

        character(len = 8) :: cnumber

        mode = 'iso'
        call swgatt(m, 'inactive', 'status')
        call swgtit('Curvas de nivel')
        call swgwth(-8)
        call wgini('vert', t)
        call wgbas(t, 'hori', t_bas1)
        call wgbut(t_bas1, 'Rojo', checked(1), t_chk1)
        write(cnumber, '(F8.1)'), level(1)
        call wgltxt(t_bas1, 'Valor:', cnumber, 70, t_lvl1)
        call wgbas(t, 'hori', t_bas2)
        call wgbut(t_bas2, 'Naranja', checked(2), t_chk2)
        write(cnumber, '(F8.1)'), level(2)
        call wgltxt(t_bas2, 'Valor:', cnumber, 70, t_lvl2)
        call wgbas(t, 'hori', t_bas3)
        call wgbut(t_bas3, 'Amarillo', checked(3), t_chk3)
        write(cnumber, '(F8.1)'), level(3)
        call wgltxt(t_bas3, 'Valor:', cnumber, 70, t_lvl3)
        call wgbas(t, 'hori', t_bas4)
        call wgbut(t_bas4, 'Verde', checked(4), t_chk4)
        write(cnumber, '(F8.1)'), level(4)
        call wgltxt(t_bas4, 'Valor:', cnumber, 70, t_lvl4)
        call wgbas(t, 'hori', t_bas5)
        call wgbut(t_bas5, 'Cyan', checked(5), t_chk5)
        write(cnumber, '(F8.1)'), level(5)
        call wgltxt(t_bas5, 'Valor:', cnumber, 70, t_lvl5)
        call wgbas(t, 'hori', t_bas6)
        call wgbut(t_bas6, 'Azul', checked(6), t_chk6)
        write(cnumber, '(F8.1)'), level(6)
        call wgltxt(t_bas6, 'Valor:', cnumber, 70, t_lvl6)

        call swgcbk(t_chk1, change_chk1)
        call swgcbk(t_lvl1, change_lvl1)
        call swgcbk(t_chk2, change_chk2)
        call swgcbk(t_lvl2, change_lvl2)
        call swgcbk(t_chk3, change_chk3)
        call swgcbk(t_lvl3, change_lvl3)
        call swgcbk(t_chk4, change_chk4)
        call swgcbk(t_lvl4, change_lvl4)
        call swgcbk(t_chk5, change_chk5)
        call swgcbk(t_lvl5, change_lvl5)
        call swgcbk(t_chk6, change_chk6)
        call swgcbk(t_lvl6, change_lvl6)

        call wgfin()
        call swgatt(m, 'active', 'status')
        if(allocated(u)) call draw_screen()

    end subroutine view_levels

    subroutine view_surface(id)

        integer, intent(in) :: id

        mode = 'sur'
        if(allocated(u)) call draw_screen()

    end subroutine view_surface

    subroutine view_interpolation(id)

        integer, intent(in) :: id

        mode = 'int'
        if(allocated(u)) call draw_screen()

    end subroutine view_interpolation

    subroutine change_properties(id)

        integer, intent(in) :: id

        integer :: p
        integer :: p_title
        integer :: p_ztitle, p_xtitle, p_ytitle
        integer :: p_xmin, p_xmax
        integer :: p_ymin, p_ymax
        integer :: p_axs

        character(len = 8) :: cnumber

        call swgatt(m, 'inactive', 'status')
        call swgtit('Propiedades')
        call swgwth(-15)
        call wgini('vert', p)
        call wgltxt(p, 'Título:', ctitle, 75, p_title)
        call wgltxt(p, 'Título eje z:', ztitle, 50, p_ztitle)
        call wgltxt(p, 'Título eje x:', xtitle, 50, p_xtitle)
        call wgltxt(p, 'Título eje y:', ytitle, 50, p_ytitle)
        write(cnumber, '(F8.1)'), xmin
        call wgltxt(p, 'x min:', cnumber, 25, p_xmin)
        write(cnumber, '(F8.1)'), xmax
        call wgltxt(p, 'x max:', cnumber, 25, p_xmax)
        write(cnumber, '(F8.1)'), ymin
        call wgltxt(p, 'y min:', cnumber, 25, p_ymin)
        write(cnumber, '(F8.1)'), ymax
        call wgltxt(p, 'y max:', cnumber, 25, p_ymax)
        call wgbox(p, 'Ejes centrados en orígen|Ejes localizados en contorno', axs, p_axs)

        call swgcbk(p_title, change_title)
        call swgcbk(p_ztitle, change_ztitle)
        call swgcbk(p_xtitle, change_xtitle)
        call swgcbk(p_ytitle, change_ytitle)
        call swgcbk(p_xmin, change_xmin)
        call swgcbk(p_xmax, change_xmax)
        call swgcbk(p_ymin, change_ymin)
        call swgcbk(p_ymax, change_ymax)
        call swgcbk(p_axs, change_axs)

        call wgfin()
        call swgatt(m, 'active', 'status')

        if(allocated(u)) call draw_screen()

    end subroutine change_properties

    subroutine invert_matrix(id)

        integer, intent(in) :: id

        integer :: i
        integer :: IOerror

        real(kind = 8), allocatable :: t(:, :)

        if(allocated(u)) then
            allocate(t(0 : gpx - 1, 0 : gpy - 1), stat = IOerror)
            if(IOerror > 0) then
                call dwgmsg('Error: memoria insuficiente')
            else
                do i = 0, gpy - 1
                    t(:, i) = u(:, gpy - 1 - i)
                end do
                u = t
                deallocate(t)
            end if
            call draw_screen()
        end if

    end subroutine invert_matrix

    subroutine about(id)

        integer, intent(in) :: id

        call dwgmsg('...........................Rep2D versión 1.2...| &
        Año 2012 por Alberto Lorenzo||Correo:   alorenzo.md@gmail.com')

    end subroutine about

    subroutine change_chk1(id)

        integer, intent(in) :: id

        call gwgbut(id, checked(1))

    end subroutine change_chk1

    subroutine change_lvl1(id)

        integer, intent(in) :: id
        character(len = 8) :: cnumber
        integer :: IOerror

        call gwgtxt(id, cnumber)
        read(cnumber, *, iostat = IOerror) level(1)
        if(IOerror /= 0) level(1) =0d0

    end subroutine change_lvl1

    subroutine change_chk2(id)

        integer, intent(in) :: id

        call gwgbut(id, checked(2))

    end subroutine change_chk2

    subroutine change_lvl2(id)

        integer, intent(in) :: id
        character(len = 8) :: cnumber
        integer :: IOerror

        call gwgtxt(id, cnumber)
        read(cnumber, *, iostat = IOerror) level(2)
        if(IOerror /= 0) level(2) =0d0

    end subroutine change_lvl2

    subroutine change_chk3(id)

        integer, intent(in) :: id

        call gwgbut(id, checked(3))

    end subroutine change_chk3

    subroutine change_lvl3(id)

        integer, intent(in) :: id
        character(len = 8) :: cnumber
        integer :: IOerror

        call gwgtxt(id, cnumber)
        read(cnumber, *, iostat = IOerror) level(3)
        if(IOerror /= 0) level(3) =0d0

    end subroutine change_lvl3

    subroutine change_chk4(id)

        integer, intent(in) :: id

        call gwgbut(id, checked(4))

    end subroutine change_chk4

    subroutine change_lvl4(id)

        integer, intent(in) :: id
        character(len = 8) :: cnumber
        integer :: IOerror

        call gwgtxt(id, cnumber)
        read(cnumber, *, iostat = IOerror) level(4)
        if(IOerror /= 0) level(4) =0d0

    end subroutine change_lvl4

    subroutine change_chk5(id)

        integer, intent(in) :: id

        call gwgbut(id, checked(5))

    end subroutine change_chk5

    subroutine change_lvl5(id)

        integer, intent(in) :: id
        character(len = 8) :: cnumber
        integer :: IOerror

        call gwgtxt(id, cnumber)
        read(cnumber, *, iostat = IOerror) level(5)
        if(IOerror /= 0) level(5) =0d0

    end subroutine change_lvl5

    subroutine change_chk6(id)

        integer, intent(in) :: id

        call gwgbut(id, checked(6))

    end subroutine change_chk6

    subroutine change_lvl6(id)

        integer, intent(in) :: id
        character(len = 8) :: cnumber
        integer :: IOerror

        call gwgtxt(id, cnumber)
        read(cnumber, *, iostat = IOerror) level(6)
        if(IOerror /= 0) level(6) =0d0

    end subroutine change_lvl6

    subroutine change_title(id)

        integer, intent(in) :: id

        call gwgtxt(id, ctitle)

    end subroutine change_title

    subroutine change_ztitle(id)

        integer, intent(in) :: id

        call gwgtxt(id, ztitle)

    end subroutine change_ztitle

    subroutine change_xtitle(id)

        integer, intent(in) :: id

        call gwgtxt(id, xtitle)

    end subroutine change_xtitle

    subroutine change_ytitle(id)

        integer, intent(in) :: id

        call gwgtxt(id, ytitle)

    end subroutine change_ytitle

    subroutine change_xmin(id)

        integer, intent(in) :: id
        character(len = 8) :: cnumber
        integer :: IOerror

        call gwgtxt(id, cnumber)
        read(cnumber, *, iostat = IOerror) xmin
        if(IOerror /= 0) xmin =0d0

    end subroutine change_xmin

        subroutine change_xmax(id)

        integer, intent(in) :: id
        character(len = 8) :: cnumber
        integer :: IOerror

        call gwgtxt(id, cnumber)
        read(cnumber, *, iostat = IOerror) xmax
        if(IOerror /= 0) xmax =0d0

    end subroutine change_xmax

    subroutine change_ymin(id)

        integer, intent(in) :: id
        character(len = 8) :: cnumber
        integer :: IOerror

        call gwgtxt(id, cnumber)
        read(cnumber, *, iostat = IOerror) ymin
        if(IOerror /= 0) ymin =0d0

    end subroutine change_ymin

    subroutine change_ymax(id)

        integer, intent(in) :: id
        character(len = 8) :: cnumber
        integer :: IOerror

        call gwgtxt(id, cnumber)
        read(cnumber, *, iostat = IOerror) ymax
        if(IOerror /= 0) ymax =0d0

    end subroutine change_ymax

    subroutine change_axs(id)

        integer, intent(in) :: id

        call gwgbox(id, axs)

    end subroutine change_axs

end module callback
