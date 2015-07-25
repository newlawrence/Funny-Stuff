program heat

    implicit none


    ! ***********************
    ! ***  Declaraciones  ***
    ! ***********************

    integer, parameter :: gp = 50          ! Los puntos de la malla
    integer, parameter :: n = 10 * gp ** 2 ! El número de iteraciones en el tiempo

    ! Párametros de la sustancia escogida (arena en mi caso) y condiciones de contorno
    real(kind = 8), parameter :: us = 15.0    ! Temperatura del suelo en ºC
    real(kind = 8), parameter :: ue = 0.0     ! Temperatura del exterior en ºC
    real(kind = 8), parameter :: uf = 50.0    ! Temperatura de la fuente de calor en ºC
    real(kind = 8), parameter :: l = 6.0      ! El lado del cuadrado a estudiar en m
    real(kind = 8), parameter :: kappa = 0.58 ! Coeficiente de conductividad térmica en W/(m*K)
    real(kind = 8), parameter :: c = 795.0    ! Calor específico en J/(kg*K)
    real(kind = 8), parameter :: rho = 1400.0 ! Densidad en kg/m**3
    real(kind = 8), parameter :: h = 12.0     ! Coeficiente de convección del aire W/(K*m**2)

    ! Coeficiente de difusión térmica y términos para simplificar las ecuaciones (se calculan en el programa)
    real(kind = 8) :: alpha, A, B, t

    real(kind = 8) :: u(0 : gp, 0 : gp, 0 : n) ! Matriz que guarda las temperaturas
    real(kind = 8) :: dx, dy, dt

    ! Celdas que delimitan los extremos de la fuente de calor (1/6 de l en mi caso)
    integer :: i1, i2, j1

    integer :: i, j, k
    integer :: IDfile
    character(len = 12) :: fil


    ! ************************
    ! ***  Puesta a punto  ***
    ! ************************

    print *, 'Instante de tiempo a representar (en dias):'
    read *, t

    ! Cálculo de las variables que intervienen en las cuentas
    print *, 'Preparando problema...'
    t = t * 86400.0 ! Pasamos los días a segundos
    dx = 1.0 / gp
    dy = 1.0 / gp
    A = (h * l) / kappa
    B = 1.0 / (2.0 * A * dy)
    alpha = kappa / (c * rho)
    dt = (alpha * t) / (n * l ** 2)

    ! Recinto de la fuente de calor
    i1 = int((5.0 * gp)/ 12.0)
    i2 = int((7.0 * gp)/ 12.0) + 1
    j1 = int((10.0 * gp)/ 12.0) + 1


    ! *************************************************************
    ! ***  Resolución del problema en variables adimensionales  ***
    ! *************************************************************

    print *, 'Calculando...'

    ! Condiciones iniciales (la temperatura se distribuye de forma uniforme hacia abajo)
    do j = 0, gp
        u(:, j, 0) = (us - ue) * (1 - j * dy) / (uf - ue)
    end do

    ! Condiciones de contorno
    u(:, 0,  1 :) = (us - ue) / (uf - ue)  ! Zona A
    u(i1 + 1 : i2 - 1, j1 : gp, 1 :) = 1   ! Zona B

    ! Bucle temporal
    do k = 0, n - 1
        ! Zona C
        do i = 1, gp - 1
            do j = 1, j1 - 1
                u(i, j, k + 1) = u(i, j, k) + dt * &
                (((u(i + 1, j, k) - 2 * u(i, j, k) + u(i - 1, j, k)) / dx ** 2) + &
                ((u(i, j + 1, k) - 2 * u(i, j, k) + u(i, j - 1, k)) / dy ** 2))
            end do
        end do
        ! Zona D
        do i = 1, i1 - 1
            do j = j1, gp - 1
                u(i, j, k + 1) = u(i, j, k) + dt * &
                (((u(i + 1, j, k) - 2 * u(i, j, k) + u(i - 1, j, k)) / dx ** 2) + &
                ((u(i, j + 1, k) - 2 * u(i, j, k) + u(i, j - 1, k)) / dy ** 2))
            end do
        end do
        ! Zona E
         do i = i2, gp - 1
            do j = j1, gp - 1
                u(i, j, k + 1) = u(i, j, k) + dt * &
                (((u(i + 1, j, k) - 2 * u(i, j, k) + u(i - 1, j, k)) / dx ** 2) + &
                ((u(i, j + 1, k) - 2 * u(i, j, k) + u(i, j - 1, k)) / dy ** 2))
            end do
        end do
        ! Zona F
        do i = 1, i1 - 1
            u(i, gp, k + 1) = (B * (4.0 * u(i, gp - 1, k + 1) - u(i, gp - 2, k + 1))) / (3.0 * B + 1.0)
        end do
        ! Zona G
        do i = i2 + 1, gp - 1
            u(i, gp, k + 1) = (B * (4.0 * u(i, gp - 1, k + 1) - u(i, gp - 2, k + 1))) / (3.0 * B + 1.0)
        end do
        ! Zona H
        do j = 1, gp
            u(0, j, k + 1) = (4.0 * u(1, j, k + 1) - u(2, j, k + 1)) / 3.0
        end do
        ! Zona I
        do j = j1, gp
            u(i1, j, k + 1) = (4.0 * u(i1 - 1, j, k + 1) - u(i1 - 2, j, k + 1)) / 3.0
        end do
        ! Zona J
        do j = j1, gp
            u(i2, j, k + 1) = (4.0 * u(i2 + 1, j, k + 1) - u(i2 + 2, j, k + 1)) / 3.0
        end do
        ! Zona K
        do j = 1, gp
            u(gp, j, k + 1) = (4.0 * u(gp - 1, j, k + 1) - u(gp - 2, j, k + 1)) / 3.0
        end do
    end do


    ! ******************************************
    ! ***  Vuelta a variables dimensionales  ***
    ! ******************************************

    u(:, :, :) = (u(:, :, :) * (uf - ue)) + ue


    ! ******************************************
    ! ***  Generación de fichero con matriz  ***
    ! ******************************************

    print *, 'Guardando fichero...'

    write(fil, '(A,I3.3,A)') 'heat_', nint(t / 86400.0), '.dat'
    open(unit = IDfile, file = fil, status = 'unknown', action = 'write')
        do j = gp, 0, -1
            write(IDfile, '(100(F18.12))') u(:, j, n)
        end do
    close(IDfile)

    print *, 'Finalizado.'

end program heat
