!
! Copyright (c) SEMEP 2013  - Alberto Lorenzo (alorenzo.md@gmail.com)
!
! Distributed under the MIT License.
! (See accompanying file "copying" or copy at
! http://opensource.org/licenses/MIT)
!

module SEMEP

	use, intrinsic :: iso_c_binding, only: c_ptr

	implicit none

	type, bind(c) :: SEMEP_Expression
		type(c_ptr) :: expression
	end type SEMEP_Expression

	interface
		function SEMEP_wcreate(e, c_s) bind(c, name='SEMEP_create')

			use, intrinsic :: iso_c_binding, only: c_ptr, c_int, c_char

			type, bind(c) :: SEMEP_Expression
				type(c_ptr) :: expression
			end type SEMEP_Expression

			type(SEMEP_Expression), intent(inout) :: e
			character(kind=c_char, len=1), dimension(*), intent(in) :: c_s
			integer(kind=c_int) :: SEMEP_wcreate

		end function SEMEP_wcreate

		subroutine SEMEP_wfree(e) bind(c, name='SEMEP_free')

			use, intrinsic :: iso_c_binding, only: c_ptr

			type, bind(c) :: SEMEP_Expression
				type(c_ptr) :: expression
			end type SEMEP_Expression

			type(SEMEP_Expression), intent(inout) :: e

		end subroutine SEMEP_wfree

		function SEMEP_wfeval(e, r, s, t, u, v, w, x, y, z) &
            bind(c, name='SEMEP_feval')

			use, intrinsic :: iso_c_binding, only: c_ptr, c_double

			type, bind(c) :: SEMEP_Expression
				type(c_ptr) :: expression
			end type SEMEP_Expression

			type(SEMEP_Expression), intent(in), value :: e
			real(kind=c_double), intent(in), value :: r, s, t, u, v, w, x, y, z 
			real(kind=c_double) :: SEMEP_wfeval

		end function SEMEP_wfeval

		subroutine SEMEP_wbuild(e, c_s) bind(c, name='SEMEP_build')

			use, intrinsic :: iso_c_binding, only: c_ptr, c_char

			type, bind(c) :: SEMEP_Expression
				type(c_ptr) :: expression
			end type SEMEP_Expression

			type(SEMEP_Expression), intent(inout) :: e
			character(kind=c_char, len=1), dimension(*), intent(in) :: c_s

		end subroutine SEMEP_wbuild

		subroutine SEMEP_wclear(e) bind(c, name='SEMEP_clear')

			use, intrinsic :: iso_c_binding, only: c_ptr

			type, bind(c) :: SEMEP_Expression
				type(c_ptr) :: expression
			end type SEMEP_Expression

			type(SEMEP_Expression), intent(inout) :: e

		end subroutine SEMEP_wclear

		function SEMEP_wisBuilt(e) bind(c, name='SEMEP_isBuilt')

			use, intrinsic :: iso_c_binding, only: c_ptr, c_int

			type, bind(c) :: SEMEP_Expression
				type(c_ptr) :: expression
			end type SEMEP_Expression

			type(SEMEP_Expression), intent(in), value :: e
			integer(kind=c_int) :: SEMEP_wisBuilt

		end function SEMEP_wisBuilt

		subroutine SEMEP_wgetLiteral(e, c_s) bind(c, name='SEMEP_getLiteral')

			use, intrinsic :: iso_c_binding, only: c_ptr, c_char

			type, bind(c) :: SEMEP_Expression
				type(c_ptr) :: expression
			end type SEMEP_Expression

			type(SEMEP_Expression), intent(in), value :: e
			character(kind=c_char, len=1), dimension(*), intent(out) :: c_s

		end subroutine SEMEP_wgetLiteral

		subroutine SEMEP_wgetVarName(e, c_s, i) &
            bind(c, name='SEMEP_fgetVarName')

			use, intrinsic :: iso_c_binding, only: c_ptr, c_char, c_int

			type, bind(c) :: SEMEP_Expression
				type(c_ptr) :: expression
			end type SEMEP_Expression

			type(SEMEP_Expression), intent(in), value :: e
			character(kind=c_char, len=1), dimension(*), intent(out) :: c_s
			integer(kind=c_int), intent(in), value :: i

		end subroutine SEMEP_wgetVarName

		function SEMEP_wgetVarCount(e) bind(c, name='SEMEP_fgetVarCount')

			use, intrinsic :: iso_c_binding, only: c_ptr, c_int

			type, bind(c) :: SEMEP_Expression
				type(c_ptr) :: expression
			end type SEMEP_Expression

			type(SEMEP_Expression), intent(in), value :: e
			integer(kind=c_int) :: SEMEP_wgetVarCount

		end function SEMEP_wgetVarCount

		function SEMEP_wcheckError(e) bind(c, name='SEMEP_checkError')

			use, intrinsic :: iso_c_binding, only: c_ptr, c_int

			type, bind(c) :: SEMEP_Expression
				type(c_ptr) :: expression
			end type SEMEP_Expression

			type(SEMEP_Expression), intent(in), value :: e
			integer(kind=c_int) :: SEMEP_wcheckError

		end function SEMEP_wcheckError

		subroutine SEMEP_wwhatError(e, c_s) bind(c, name='SEMEP_whatError')

			use, intrinsic :: iso_c_binding, only: c_ptr, c_char

			type, bind(c) :: SEMEP_Expression
				type(c_ptr) :: expression
			end type SEMEP_Expression

			type(SEMEP_Expression), intent(in), value :: e
			character(kind=c_char, len=1), dimension(*), intent(out) :: c_s

		end subroutine SEMEP_wwhatError

		subroutine SEMEP_waddConstant(c_s, x) bind(c, name='SEMEP_addConstant')

			use, intrinsic :: iso_c_binding, only: c_ptr, c_char, c_double

			character(kind=c_char, len=1), dimension(*), intent(in) :: c_s
			real(kind=c_double), intent(in), value :: x

		end subroutine SEMEP_waddConstant

		subroutine SEMEP_waddUnaryOperator(c_s, f) &
            bind(c, name='SEMEP_addUnaryOperator')

			use, intrinsic :: iso_c_binding, only: c_ptr, c_char, c_funptr

			character(kind=c_char, len=1), dimension(*), intent(in) :: c_s
			type(c_funptr), intent(in), value :: f

		end subroutine SEMEP_waddUnaryOperator
	end interface

	contains

	function SEMEP_F2C_string(F_String) result (C_String)

		use, intrinsic :: iso_c_binding, only: c_char, c_null_char

		character(len=*), intent(in)  :: F_String
		character(kind=c_char, len=1), dimension(len(F_String)+1) :: C_String

		integer :: n, i

		n = len(F_String)
		do i = 1, n
			C_String(i) = F_String(i : i)
		end do
		C_String(n + 1) = c_null_char

	end function

	subroutine SEMEP_C2F_string(F_String, C_String)

		use, intrinsic :: iso_c_binding, only: c_char, c_null_char

		character(len=*), intent(out)  :: F_String
		character(kind=c_char, len=1), dimension(*) :: C_String

		integer :: n, i

		n = len(F_String)
		do i = 1, n
			if(C_String(i) /= c_null_char) then
				F_String(i : i) = C_String(i)
			else
				exit
			end if
		end do
		do while(i <= n)
			F_String(i : i) = ' '
			i = i + 1
		end do 

	end subroutine SEMEP_C2F_string
	
	subroutine SEMEP_create(e, f_s, l)

		type(SEMEP_Expression), intent(out) :: e
		character(len=*), intent(in) :: f_s
		logical, intent(out), optional :: l

		integer :: i

		i = SEMEP_wcreate(e, SEMEP_F2C_string(f_s))
		if(present(l)) then
			if(i /= 0) then
				l = .true.
			else
				l = .false.
			end if
		end if

	end subroutine SEMEP_create

	subroutine SEMEP_free(e)

		type(SEMEP_Expression), intent(out) :: e

		call SEMEP_wfree(e)

	end subroutine SEMEP_free

	function SEMEP_eval(e, r, s, t, u, v, w, x, y, z) result (eval)

		type(SEMEP_Expression), intent(in), value :: e
		real(kind=8), intent(in), optional, value :: r, s, t, u, v, w, x, y, z
		real(kind=8) :: eval

		real(kind=8) :: r1 = 0, s1 = 0, t1 = 0, &
		                u1 = 0, v1 = 0, w1 = 0, &
		                x1 = 0, y1 = 0, z1 = 0

		if(present(r)) r1 = r
		if(present(r)) s1 = s
		if(present(r)) t1 = t
		if(present(r)) u1 = u
		if(present(r)) v1 = v
		if(present(r)) w1 = w
		if(present(r)) x1 = x
		if(present(r)) y1 = y
		if(present(r)) z1 = z

		eval = SEMEP_wfeval(e, r1, s1, t1, u1, v1, w1, x1, y1, z1)

	end function SEMEP_eval

	subroutine SEMEP_build(e, f_s)

		type(SEMEP_Expression), intent(out) :: e
		character(len=*), intent(in) :: f_s

		call SEMEP_wbuild(e, SEMEP_F2C_string(f_s))

	end subroutine SEMEP_build

	subroutine SEMEP_clear(e)

		type(SEMEP_Expression), intent(out) :: e

		call SEMEP_wclear(e)

	end subroutine SEMEP_clear

	function SEMEP_isBuilt(e) result(isBuilt)

		type(SEMEP_Expression), intent(in), value :: e
		logical :: isBuilt

		if(SEMEP_wisBuilt(e) /= 0) then
			isBuilt = .true.
		else
			isBuilt = .false.
		end if

	end function SEMEP_isBuilt

	subroutine SEMEP_getLiteral(e, f_s)

		use, intrinsic :: iso_c_binding, only: c_char

		type(SEMEP_Expression), intent(in), value :: e
		character(len=*), intent(out) :: f_s

		character(kind=c_char, len=1), dimension(50) :: c_s

		call SEMEP_wgetLiteral(e, c_s)
		call SEMEP_C2F_string(f_s, c_s)

	end subroutine SEMEP_getLiteral

	subroutine SEMEP_getVarName(e, f_s, i)

		use, intrinsic :: iso_c_binding, only: c_char

		type(SEMEP_Expression), intent(in), value :: e
		character(len=*), intent(out) :: f_s
		integer, intent(in) :: i

		character(kind=c_char, len=1), dimension(50) :: c_s

		call SEMEP_wgetVarName(e, c_s, i)
		call SEMEP_C2F_string(f_s, c_s)

	end subroutine SEMEP_getVarName

	function SEMEP_getVarCount(e) result(varCount)

		type(SEMEP_Expression), intent(in), value :: e
		integer :: varCount

		varCount = SEMEP_wgetVarCount(e)

	end function SEMEP_getVarCount

	function SEMEP_checkError(e) result(checkError)

		type(SEMEP_Expression), intent(in), value :: e
		logical :: checkError

		if(SEMEP_wcheckError(e) /= 0) then
			checkError = .true.
		else
			checkError = .false.
		end if

	end function SEMEP_checkError

	subroutine SEMEP_whatError(e, f_s)

		use, intrinsic :: iso_c_binding, only: c_char

		type(SEMEP_Expression), intent(in), value :: e
		character(len=*), intent(out) :: f_s

		character(kind=c_char, len=1), dimension(50) :: c_s

		call SEMEP_wwhatError(e, c_s)
		call SEMEP_C2F_string(f_s, c_s)

	end subroutine SEMEP_whatError

	subroutine SEMEP_addConstant(f_s, x)

		character(len=*), intent(in) :: f_s
		real(kind=8), intent(in) :: x

		call SEMEP_waddConstant(SEMEP_F2C_string(f_s), x)

	end subroutine SEMEP_addConstant

	subroutine SEMEP_addUnaryOperator(f_s, f)

		use, intrinsic :: iso_c_binding, only: c_double, c_funloc

		character(len=*), intent(in) :: f_s
		interface
			function f(x) bind(c)
				use, intrinsic :: iso_c_binding, only: c_double
				real(kind=c_double), intent(in), value :: x
				real(kind=c_double) :: f
			end function f
		end interface

		call SEMEP_waddUnaryOperator(SEMEP_F2C_string(f_s), c_funloc(f))

	end subroutine SEMEP_addUnaryOperator

end module SEMEP
