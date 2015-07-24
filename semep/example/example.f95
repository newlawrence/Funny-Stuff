! *****************************************************************************
! * This is SEMEP (Simple & Extensible Math Expression Parser), lets see a    *
! * brief example as an introduction to the library.                          *
! *****************************************************************************

program main

	use SEMEP

	implicit none

	real(kind=8), parameter :: PI = 3.1415926535
	type(SEMEP_Expression) :: A
	character(len=50) :: string  ! Minimum size to show complete error messages
	integer :: i

	print *,
	print '(A)', '*** Demonstration of what SEMEP can do ***'

    ! Example of how not to create an instance
	print *,
	print '(A)', 'This will be wrong: call SEMEP_create(A, "sin(x)")'
	call SEMEP_create(A, 'sin(x)')
	print '(A,F5.3)', 'sin(PI/2) = ', SEMEP_eval(A, PI/2d0)
	call SEMEP_whatError(A, string)
	print '(A)', "Let's check it out what happened:"
	if(SEMEP_checkError(A)) &
        print '(A)', string
	print *,
	print '(A)', 'SEMEP must know x is a variable!!!'

    ! Example of a proper instanciation
	print *,
	print '(A)', 'The proper way: call SEMEP_build(A,"sin(x),x")'
	call SEMEP_build(A, 'sin(x),x')
	print '(A,F5.3)', 'sin(PI/2) = ', SEMEP_eval(A, PI/2d0)
	print '(A)', 'This time is OK'

    ! Check if an expression is built	
	print *,
	print '(A)', 'With SEMEP_isBuilt you can check if an expression is ' // &
                 'evaluable'
	if(SEMEP_isBuilt(A)) &
        print '(A)', 'After SEMEP_build(A, "..."): Expression is built'
	call SEMEP_clear(A)
	if(.not. SEMEP_isBuilt(A)) &
        print '(A)', 'After SEMEP_clear(A):        Expression is not built'

    ! Demonstration of error checking	
	print *,
	print '(A)', "Don't forget to check for errors with " // &
                 "'SEMEP_checkError & SEMEP_whatError:"
	print '(A)', 'call SEMEP_build(A, "(4+5")'
	call SEMEP_build(A, '(4+5')
	call SEMEP_whatError(A, string)
	print '(A)', string

    ! Custom variables
	print *,
	print '(A)', 'In Fortran95 you can create expressions up to 9 variables'
	print '(A)', 'call SEMEP_build(A, "Albert*(John-Thomas),' // &
                 'Thomas,Albert,John")'
	call SEMEP_build(A, 'Albert*(John-Thomas),Thomas,Albert,John')
	print '(A,F5.3)', 'SEMEP_eval(A, 2.0, 7.0, 3.1) = ', &
                      SEMEP_eval(A, 2d0, 7d0, 31d-1)
	print '(A)', 'In SEMEP, variables are stored in alphabetic order'

    ! Demonstration of inquiry functions	
	print *,
	print '(A)', "Let's check it with inquiry functions:"
	call SEMEP_getLiteral(A, string)
	print '(A,A)', 'Your expression was: ', string
	print '(A)', 'List of variables as stored in memory'
	do i = 1, SEMEP_getVarCount(A)
		call SEMEP_getVarName(A, string, i)
		print '(A,I1,A,A)', 'Variable ', i, ' = ', string
	end do

    ! Constant expressions
	print *,
	print '(A)', 'Returning constants is allowed:'
	call SEMEP_build(A, '3.56')
	print '(A,F5.3)', 'SEMEP_eval(A) = ', SEMEP_Eval(A)

    ! Other stuff
	print *,
	print '(A)', 'And at last, you can define your own constants and ' // &
                 'single variable functions'
	call SEMEP_addConstant('LM', 7891d-3)
	print '(A)', 'call SEMEP_addConstant("LM", 7.891)'
	call SEMEP_addUnaryOperator('foo', foo)
	print '(A)', 'call SEMEP_addUnaryOperator("foo",foo)'
	call SEMEP_build(A, 'LM*foo(x),x')
	print '(A)', 'call SEMEP_build(A, "LM*foo(x),x")'
	print '(A,F7.3)', 'SEMEP_eval(A, 2.7) = ', SEMEP_eval(A, 27d-1)

    ! End
	print *,
	print '(A)', "That's all folks!!!"

	print *,
	call SEMEP_free(A)  ! Expression deletion

	contains

	! Since SEMEP is coded in C++, extension functions must be provided as
    ! interoperable with C

	function foo(x) result(f) bind(c)

		use, intrinsic :: iso_c_binding, only: c_double

		real(kind=c_double), intent(in), value :: x
		real(kind=c_double) :: f

		f = 1d0 + 2d0 * x

	end function foo

end program main
