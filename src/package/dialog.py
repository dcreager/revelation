# -*- coding: utf-8 -*-
#
# Dialogs
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

from __future__ import absolute_import

from . import config

from .shinygnome import ui as shinyui


class AboutDialog(shinyui.dialog.AboutDialog):
	"An about dialog"

	def __init__(self, parent):
		shinyui.dialog.AboutDialog.__init__(self, parent)

		self.set_name(config.NAME)
		self.set_version(config.VERSION)
		self.set_copyright(config.COPYRIGHT)
		self.set_comments(('"%s"\n\n%s' % ( config.RELEASENAME, config.DESCRIPTION )))
		self.set_license(config.LICENSE)
		self.set_website(config.WEBSITE)
		self.set_authors(config.AUTHORS)
		self.set_artists(config.ARTISTS)

