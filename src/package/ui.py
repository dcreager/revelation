# -*- coding: utf-8 -*-
#
# User interface classes
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

from . import stock

from .shinygnome import ui as shinyui


# these widgets are just used as-is from shinygnome
ActionGroup	= shinyui.uimanager.ActionGroup
Alignment	= shinyui.container.Alignment
App		= shinyui.window.App
HPaned		= shinyui.container.HPaned
ScrolledWindow	= shinyui.container.ScrolledWindow
VBox		= shinyui.container.VBox


class AccountList(shinyui.tree.TreeView):
	"Displays the account list"

	def __init__(self, accountstore = None):
		shinyui.tree.TreeView.__init__(self, accountstore)

		cr_icon	= shinyui.display.CellRendererPixbuf(stock_size = stock.ICON_SIZE_LIST)
		cr_name	= shinyui.display.CellRendererText()

		column = shinyui.tree.TreeViewColumn(None)
		column.pack_start(cr_icon, False)
		column.pack_start(cr_name)
		column.add_attribute(cr_icon, "stock-id", 0)
		column.add_attribute(cr_name, "text", 1)
		self.append_column(column)



class AccountView(VBox):
	"An account display widget"

	def __init__(self, account = None):
		VBox.__init__(self)
		self.set_spacing(12)
		self.set_border_width(12)

