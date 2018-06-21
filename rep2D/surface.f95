!
! Copyright (c) Rep2D v1.2 2012  - Alberto Lorenzo (alorenzo.md@gmail.com)
!
! Distributed under the MIT License.
! (See accompanying file "copying" or copy at
! http://opensource.org/licenses/MIT)
!

program surface

    use callback
    implicit none

    mode = 'sur'
    level = 0d0
    checked = 0
    xmin = 0d0
    xmax = 1d0
    ymin = 0d0
    ymax = 1d0
    ctitle = 'Modifica los valores por defecto en "Propiedades>Representaci`on"'
    xtitle = 'x'
    ytitle = 'y'
    ztitle = 'z'
    axs = 2

    call swgtit('Representación 2D')
    call swgopt('ok', 'close')
    call swgwth(-45)
    call swgpop('nook')
    call swgpop('noquit')
    call swgpop('nohelp')
    call swgfnt('Microsoft Sans Serif', 15)
    call swgopt('change', 'callback')
    call wgini('vert', m)
    call wgpop(m, 'Archivo', m_fil)
    call wgapp(m_fil, 'Cargar matriz', m_fil_opn)
    call wgapp(m_fil, 'Exportar PDF', m_fil_pdf)
    call wgpop(m, 'Visualizar', m_vis)
    call wgapp(m_vis, 'Mapa de curvas de nivel', m_vis_lev)
    call wgapp(m_vis, 'Superficie discretizada', m_vis_sur)
    call wgapp(m_vis, 'Superficie interpolada', m_vis_int)
    call wgpop(m, 'Propiedades', m_prop)
    call wgapp(m_prop, 'Representación', m_prop_edt)
    call wgapp(m_prop, 'Invertir mapeado', m_prop_inv)
    call wgpop(m, 'Ayuda', m_help)
    call wgapp(m_help, 'Acerca de', m_help_abt)
    call page(1900, 1900)
    call wgdraw(m, m_draw)

    call swgcbk(m_fil_opn, load_matrix)
    call swgcbk(m_fil_pdf, export_matrix)
    call swgcbk(m_vis_lev, view_levels)
    call swgcbk(m_vis_sur, view_surface)
    call swgcbk(m_vis_int, view_interpolation)
    call swgcbk(m_prop_edt, change_properties)
    call swgcbk(m_prop_inv, invert_matrix)
    call swgcbk(m_help_abt, about)

    call wgfin()
    if(allocated(u)) deallocate(u)

end program surface
