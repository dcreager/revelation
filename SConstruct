#
# Revelation - a password manager for GNOME 2
# http://oss.codepoet.no/revelation/
# $Id$
#
# SConstruct - build configuration for SCons
#
# Copyright (c) 2003-2006 Erik Grinaker
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
#

import sconsent

# set some variables
PACKAGE			= "revelation"
VERSION			= "0.4.9"
RELEASENAME		= "One toke? You poor fool!"

REQ_PKGCONFIG_PACKAGES	= {
	"pygtk-2.0"			: "2.8.0",
	"gnome-python-2.0"		: "2.10.0",
	"gnome-python-desktop-2.0"	: "2.10.0",
	"gnome-python-extras-2.0"	: "2.10.0",
}
REQ_PYTHON_VERSION	= "2.3.0"
REQ_PYTHON_MODULES	= [
	"Crypto",
	"bonobo",
	"gconf",
	"gtk",
	"gnome",
	"gnomeapplet",
	"gnomevfs",
	"gobject",
	"pango",
]

# set up sconsent
sconsent.LoadTool("cracklib", "fdo", "gconf", "groff", "intltool", "pkgconfig", "python", "xsltproc")

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
	conf.CheckFDO()
	conf.CheckCracklib()
	conf.CheckGConf()
	conf.CheckIntlTool()
	conf.CheckXSLTProc()
	conf.CheckPIC2Graph()

	env = conf.Finish()

except sconsent.configure.ConfigureDisabledError:
	pass

except sconsent.configure.ConfigureError, reason:
	env.Error(reason)


# load sconscript files
env.SConscript("data/SConscript", exports = "env", build_dir = "build/data")
env.SConscript("doc/SConscript", exports = "env", build_dir = "build/doc")
env.SConscript("po/SConscript", exports = "env", build_dir = "build/po")
env.SConscript("src/SConscript", exports = "env", build_dir = "build/src")

env.Replace(shinygnome_libdir = env.subst("$python_libdir/$package/shinygnome"))
env.SConscript("src/shinygnome/SConscript", exports = "env", build_dir = "build/src/shinygnome")

