# -*- coding: utf-8 -*-
#
# SCons build script
# $Id$
#
# Copyright ©2003-2007 Erik Grinaker <erikg@codepoet.no>
#
# This file is part of Revelation.
#
# Revelation is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# Revelation is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import sconsent


# set some variables
PACKAGE			= "revelation"
VERSION			= "0.5.0"
RELEASENAME		= "Unnamed"

REQ_PYTHON_VERSION	= "2.5.0"
REQ_PYTHON_MODULES	= [ "bonobo", "gtk", "gnome", "gobject", "pango" ]
REQ_PKGCONFIG_PACKAGES	= {
	"pygtk-2.0"			: "2.8.0",
	"gnome-python-2.0"		: "2.10.0",
	"gnome-python-desktop-2.0"	: "2.10.0",
	"gnome-python-extras-2.0"	: "2.10.0",
}


# set up sconsent
sconsent.LoadTool("groff", "pkgconfig", "python", "xsltproc")

# set up environment
options = sconsent.option.Options(args = ARGUMENTS)

env = sconsent.InitEnv(
	Environment(options = options),
	PACKAGE, VERSION,
	options = options,
	releasename = RELEASENAME
)


# run configuration checks
try:
	conf = env.Configure()

	conf.CheckPKGConfig(REQ_PKGCONFIG_PACKAGES)
	conf.CheckPython(REQ_PYTHON_VERSION, REQ_PYTHON_MODULES)
	conf.CheckXSLTProc()
	conf.CheckDocbookXSL()
	conf.CheckPIC2Graph()

	env = conf.Finish()


except sconsent.configure.ConfigureDisabledError:
	pass

except sconsent.config.ConfigureError, error:
	env.Error(error)


# load sconscript files
env.SConscript("data/SConscript", exports = "env", build_dir = "build/data")
env.SConscript("docs/SConscript", exports = "env", build_dir = "build/docs")
env.SConscript("src/SConscript", exports = "env", build_dir = "build/src")

# build shinygnome
env.Replace(shinygnome_libdir = env.subst("$python_libdir/$package/shinygnome"))
env.SConscript("src/shinygnome/SConscript", exports = "env", build_dir = "build/src/shinygnome")
