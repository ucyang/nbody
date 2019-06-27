program nbody_serial
implicit none
    integer(kind = 8) :: nsteps
    integer(kind = 8) :: nparticles

    real(kind = 8), dimension(:), allocatable :: m
    real(kind = 8), dimension(:), allocatable :: x, y, z
    real(kind = 8), dimension(:), allocatable :: x_tmp, y_tmp, z_tmp
    real(kind = 8), dimension(:), allocatable :: vx, vy, vz

    real(kind = 8) :: G
    real(kind = 8) :: dt
    real(kind = 8) :: dx, dy, dz
    real(kind = 8) :: r, a
    real(kind = 8) :: softening

    integer(kind = 8) :: n, i, j

    character(len = 1024) :: arg
    character(len = 1024) :: param_file

    integer :: ios

    do i = 1, 5
        call get_command_argument(int(i), arg)
        if (len_trim(arg) == 0) then
            print *, "Please specify arguments correctly." // achar(10)
            print *, "Usage: nbody <nsteps> <dt> <G> <softening> " &
                // "<PARAMETERS_FILE>" // achar(10)
            print *, "PARAMETERS_FILE format:"
            print *, " nparticles (on the first line)"
            print *, " m x y z vx vy vz (on each line after the first line)"
            stop
        end if

        select case (i)
        case (1)
            read(arg, *) nsteps
        case (2)
            read(arg, *) dt
        case (3)
            read(arg, *) G
        case (4)
            read(arg, *) softening
        case (5)
            read(arg, "(a)") param_file
        end select
    end do

    open(1, file = param_file, iostat = ios, status = "old")
    if (ios /= 0) then
        print *, "Can't open the PARAMETERS_FILE:", param_file
        stop
    end if

    read(1, *) nparticles
    allocate(m(0:nparticles - 1))
    allocate(x(0:nparticles - 1))
    allocate(y(0:nparticles - 1))
    allocate(z(0:nparticles - 1))
    allocate(x_tmp(0:nparticles - 1))
    allocate(y_tmp(0:nparticles - 1))
    allocate(z_tmp(0:nparticles - 1))
    allocate(vx(0:nparticles - 1))
    allocate(vy(0:nparticles - 1))
    allocate(vz(0:nparticles - 1))

    print *, "Initial parameters:"
    do i = 0, nparticles - 1
        read(1, *) m(i), x(i), y(i), z(i), vx(i), vy(i), vz(i)
        print *, i, ": m =", m(i), "x =", x(i), "y =", y(i), "z =", z(i), &
            "vx =", vx(i), "vy =", vy(i), "vz =", vz(i)
    end do

    close(1)

    print *, "n =", 0_8
    do i = 0, nparticles - 1
        print *, i, ":", x(i), y(i), z(i)
    end do

    do n = 1, nsteps
        x_tmp = x + vx * dt
        y_tmp = y + vy * dt
        z_tmp = z + vz * dt

        do i = 0, nparticles - 1
            do j = 0, nparticles - 1
                dx = x(j) - x(i)
                dy = y(j) - y(i)
                dz = z(j) - z(i)

                r = sqrt(dx ** 2 + dy ** 2 + dz ** 2 + softening)
                a = G * m(j) / r ** 3 * dt

                vx(i) = vx(i) + a * dx
                vy(i) = vy(i) + a * dy
                vz(i) = vz(i) + a * dz
            end do
        end do

        x = x_tmp
        y = y_tmp
        z = z_tmp

        print *, "n =", n
        do i = 0, nparticles - 1
            print *, i, ":", x(i), y(i), z(i)
        end do
    end do

    deallocate(m)
    deallocate(x)
    deallocate(y)
    deallocate(z)
    deallocate(x_tmp)
    deallocate(y_tmp)
    deallocate(z_tmp)
    deallocate(vx)
    deallocate(vy)
    deallocate(vz)
end program
