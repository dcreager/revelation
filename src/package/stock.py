# -*- coding: utf-8 -*-
#
# Stock items
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

import gtk

from .shinygnome import ui as shinyui


STOCK_ABOUT		= gtk.STOCK_ABOUT
STOCK_CLOSE		= gtk.STOCK_CLOSE
STOCK_QUIT		= gtk.STOCK_QUIT
STOCK_REVELATION	= "revelation-revelation"


class StockFactory(shinyui.icon.StockFactory):
	"A stock item factory"

	icons	= (
		( STOCK_REVELATION,		"revelation" ),
	)

	def __init__(self, parent, searchpath = None):
		shinyui.icon.StockFactory.__init__(self, parent, searchpath)

		# load icons
		for id, icon in self.icons:
			self.copy(id, icon)

