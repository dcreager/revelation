## Process this file with automake to produce Makefile.in
#
# src/Makefile.am
#
# $Id$
#

SUBDIRS		= bundle lib wrap
bin_SCRIPTS	= revelation
libexec_SCRIPTS	= revelation-applet
EXTRA_DIST	= revelation.in revelation-applet.in
CLEANFILES	= revelation revelation-applet


revelation: revelation.in
	sed \
		-e "s|\@pyexecdir\@|$(pyexecdir)|" \
		revelation.in > revelation

revelation-applet: revelation-applet.in
	sed \
		-e "s|\@pyexecdir\@|$(pyexecdir)|" \
		-e "s|\@bindir\@|$(bindir)|" \
		revelation-applet.in > revelation-applet

