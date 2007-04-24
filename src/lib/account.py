#
# Revelation - a password manager for GNOME 2
# http://oss.codepoet.no/revelation/
# $Id$
#
# Module containing account classes
#
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

import time
import shinygnome.ui


DATATYPE_DATE		= "date"
DATATYPE_DATETIME	= "datetime"
DATATYPE_FILE		= "file"
DATATYPE_EMAIL		= "email"
DATATYPE_HOSTNAME	= "hostname"
DATATYPE_INTEGER	= "integer"
DATATYPE_PATH		= "path"
DATATYPE_SECRET		= "secret"
DATATYPE_STRING		= "string"
DATATYPE_URL		= "url"
DATATYPE_USERID		= "userid"



class Account(object):
	"An account"

	def __init__(self, accounttype):
		self.id			= None
		self.accounttype	= accounttype
		self.modified		= time.time()

		self.name		= ""
		self.description	= ""
		self.tags		= TagList()
		self.launcher		= ""
		self.note		= ""

		self.fields		= []



class AccountStore(shinygnome.ui.ListStore):
	"An account store"

	def __init__(self):
		shinygnome.ui.ListStore.__init__(
			self,
			str,		# icon
			str,		# name
			object		# account
		)


	def add_account(self, account):
		"Adds an account"

		if account == None:
			return

		iter = self.append([ account.accounttype.icon, account.name, account ])


	def get_account(self, iter):
		"Fetches an account"

		if iter:
			return self.get_value(iter, 2)


	def remove_account(self, iter):
		"Removes an entry"

		self.remove(iter)


	def update_account(self, iter, account):
		"Updates an account"

		if iter == None or account == None:
			return

		self.set_value(iter,	0,	account.accounttype.icon)
		self.set_value(iter,	1,	account.name)
		self.set_value(iter,	2,	account)



class Field(object):
	"An account data field"

	def __init__(self, name, value = "", datatype = DATATYPE_STRING, description = ""):
		self.name		= name
		self.description	= description
		self.datatype		= datatype
		self.value		= value


	def __setattr__(self, name, value):
		"Custom attribute setting"

		if name == "value":
			value = value.strip()

		object.__setattr__(self, name, value)


	def get_display_widget(self):
		"Returns a widget for displaying the field"

		import ui

		if self.datatype == DATATYPE_EMAIL:
			return ui.LinkButton("mailto:%s" % value, shinygnome.util.text.escape_markup(self.value))

		elif self.datatype == DATATYPE_SECRET:
			return ui.PasswordLabel(shinygnome.util.text.escape_markup(self.value))

		elif self.datatype == DATATYPE_URL:
			return ui.LinkButton(self.value, shinygnome.util.text.escape_markup(self.value))

		else:
			label = ui.Label(shinygnome.util.text.escape_markup(self.value))
			label.set_selectable(True)

			return label


	def get_edit_widget(self):
		"Returns a widget for editing the field"

		import ui

		if self.datatype == DATATYPE_SECRET:
			editor = ui.PasswordEntryGenerate()

		elif self.datatype == DATATYPE_USERID:
			editor = ui.SimpleComboBoxEntry()

		else:
			editor = ui.Entry()


		if self.value:
			editor.set_text(self.value)

		return editor



class TagList(list):
	"A tag list"

	def clear(self):
		"Clears the tag list"

		while len(self):
			self.remove(0)


	def from_string(self, string):
		"Sets the tags list from a comma-separated string"

		self.clear()

		for tag in [ tag.strip() for tag in string.split(",") if tag.strip() != "" ]:
			self.append(tag)



class Type(object):
	"An account type"

	def __init__(self, id, name, icon, description = "", launcher = ""):
		self.id			= id
		self.name		= name
		self.icon		= icon
		self.description	= description
		self.launcher		= launcher
		self.fields		= []



class Types(list):
	"A collection of account types"
	pass

