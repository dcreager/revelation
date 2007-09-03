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

import gettext

from . import info
from .shinygnome import ui as shinyui

_ = gettext.gettext


ErrorDialog	= shinyui.dialog.ErrorMessageDialog


class AboutDialog(shinyui.dialog.AboutDialog):
	"An about dialog"

	def __init__(self, parent):
		shinyui.dialog.AboutDialog.__init__(self, parent)

		self.set_name(info.NAME)
		self.set_version(info.VERSION)
		self.set_copyright(info.COPYRIGHT)
		self.set_comments(('"%s"\n\n%s' % ( info.RELEASENAME, info.DESCRIPTION )))
		self.set_license(info.LICENSE)
		self.set_website(info.WEBSITE)
		self.set_authors(info.AUTHORS)
		self.set_artists(info.ARTISTS)
		self.set_translator_credits(_('translator-credits'))

