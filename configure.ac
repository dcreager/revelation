dnl initialize autoconf/automake
AC_PREREQ(2.53)
AC_INIT(src/revelation.in)
AM_INIT_AUTOMAKE(revelation, 0.4.0-pre2)


dnl some macros
AC_DEFUN(AC_CRACKLIB_DICTPATH,
[
	AC_MSG_CHECKING([cracklib dictionary database])
	AC_ARG_WITH(cracklib-dict, [  --with-cracklib-dict=PATH  path to cracklib dictionary database], CRACK_DICTPATH=$withval)

	if test -z "$CRACK_DICTPATH"; then
		cat > dictpath-test.c << EOF
#include <crack.h>

int main()
{
	printf(CRACKLIB_DICTPATH);
	return 0;
}
EOF

		${CC-cc} -o dictpath-test $CFLAGS dictpath-test.c >/dev/null 2>&1

		if test -e dictpath-test; then
			CRACK_DICTPATH=`./dictpath-test`
			AC_MSG_RESULT($CRACK_DICTPATH)
		else
			CRACK_DICTPATH="$datadir/revelation/pwdict"
			AC_MSG_RESULT(using builtin)
		fi

		rm -f dictpath-test* core core.dictpath-test
	else
		AC_MSG_RESULT($CRACK_DICTPATH)
	fi

	AC_SUBST(CRACK_DICTPATH)
])

AC_DEFUN([AC_PYTHON_MODULE],[
	AC_MSG_CHECKING(python module: $1)
	python -c "import $1" 2>/dev/null

	if test $? -eq 0; then
		AC_MSG_RESULT(yes)
		eval AS_TR_CPP(HAVE_PYMOD_$1)=yes
	else
		AC_MSG_RESULT(no)
		eval AS_TR_CPP(HAVE_PYMOD_$1)=no

		if test -n "$2"; then
			AC_MSG_ERROR(failed to find required module $1)
			exit 1
		fi
	fi
])

AC_DEFUN(PFK_PYTHON_PATH,[
	AC_MSG_CHECKING(Python include path)
	AC_ARG_WITH(python-include, [  --with-python-include=PATH  path to where Python.h lives], PY_INCLUDE=$withval )

	if test -z "$PY_INCLUDE" ; then
		PY_INCLUDE=$PYTHON
		pfk_py_include_path=`echo $PY_INCLUDE | sed -e "s/bin/include/"`
		pfk_py_version="`$PYTHON -c "import sys; print sys.version[[0:3]]"`";
		PY_INCLUDE="$pfk_py_include_path$pfk_py_version"
	fi

	AC_MSG_RESULT($PY_INCLUDE)
	AC_SUBST(PY_INCLUDE)
])



dnl check for dependencies
AC_PROG_CC()

AM_PATH_PYTHON(2.3)
PFK_PYTHON_PATH()
PKG_CHECK_MODULES(PYGTK, pygtk-2.0 >= 2.3.90)
PKG_CHECK_MODULES(GNOME_PYTHON, gnome-python-2.0 >= 2.5.90)
AC_PYTHON_MODULE(Crypto, yes)

AC_CHECK_LIB(crack, FascistCheck, [], AC_MSG_ERROR(cracklib2 not found))
AC_CRACKLIB_DICTPATH
AC_PATH_PROG(CRACK_MKDICT, mkdict, no)
if test x"$CRACK_MKDICT" = xno; then
	AC_MSG_ERROR([mkdict executable from cracklib not found in your path])
fi
AC_PATH_PROG(CRACK_PACKER, packer, no)
if test x"$CRACK_PACKER" = xno; then
	AC_MSG_ERROR([packer executable from cracklib not found in your path])
fi

AC_PATH_PROG(GCONFTOOL, gconftool-2, no)
if test x"$GCONFTOOL" = xno; then
	AC_MSG_ERROR([gconftool-2 executable not found in your path - should be installed with GConf])
fi
AM_GCONF_SOURCE_2

AC_PATH_PROG(UPDATE_MIME_DATABASE, update-mime-database, no)
AC_PATH_PROG(UPDATE_DESKTOP_DATABASE, update-desktop-database, no)

AM_CONDITIONAL(FDO_MIME, test x$UPDATE_MIME_DATABASE != xno -a x$UPDATE_DESKTOP_DATABASE != xno)



dnl output files
AC_OUTPUT([
	Makefile
	data/Makefile
	data/icons/Makefile
	data/icons/16x16/Makefile
	data/icons/24x24/Makefile
	data/icons/32x32/Makefile
	data/icons/48x48/Makefile
	data/mime/Makefile
	data/ui/Makefile
	src/Makefile
	src/lib/Makefile
	src/lib/datahandler/Makefile
	test/Makefile
	wrap/Makefile
	wrap/authmanager/Makefile
	wrap/crack/Makefile
])

