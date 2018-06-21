program stab

    ! Zona de estabilidad absoluta para el Adams Bashford de orden 2

    implicit none

    integer, parameter :: gpx = 50, gpy = 50

    real(kind = 8), parameter :: xmax = 1d0, xmin = -1d0
    real(kind = 8), parameter :: ymax = 1d0, ymin = -1d0

    complex(kind = 8) :: w(0: gpx, 0: gpy)
    real(kind = 8)    :: dx, dy

    complex(kind = 8) :: r1, r2
    real(kind = 8)    :: rho(0 : gpx, 0 : gpy)

    integer :: i, j
    integer :: IDfile

    dx = abs(xmax - xmin) / gpx
    dy = abs(ymax - ymin) / gpy
    do i = 0, gpx
        do j = 0, gpy
            w(i, j) = cmplx(xmin + i * dx, ymin + j * dy)
            r1 = (3d0 * w(i, j) + 2d0) / 4d0 + &
            (((3d0 * w(i, j) + 2d0)**2 / 4d0 - 2d0 * w(i, j)) ** 5d-1) * 5d-1
            r2 = (3d0 * w(i, j) + 2d0) / 4d0 - &
            (((3d0 * w(i, j) + 2d0)**2 / 4d0 - 2d0 * w(i, j)) ** 5d-1) * 5d-1
            rho(i, j) = max(abs(r1), abs(r2))
        end do
    end do

    IDfile = 100
    open(unit = IDfile, file = 'stab.dat', status = 'unknown', action = 'write')
        do j = gpy, 0, -1
            write(IDfile, '(100(F18.12))') rho(:, j)
        end do
    close(IDfile)

end program stab
