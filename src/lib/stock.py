#
# Revelation - a password manager for GNOME 2
# http://oss.codepoet.no/revelation/
# $Id$
#
# Module for stock items
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

import shinygnome.ui

import gettext, gtk

_ = gettext.gettext


STOCK_CONTINUE			= "revelation-continue"
STOCK_DISCARD			= "revelation-discard"
STOCK_EDIT			= "revelation-edit"
STOCK_EXPORT			= "revelation-export"
STOCK_FOLDER			= "revelation-folder"
STOCK_GENERATE			= "revelation-generate"
STOCK_IMPORT			= "revelation-import"
STOCK_GOTO			= "revelation-goto"
STOCK_LOCK			= "revelation-lock"
STOCK_NEW_ENTRY			= "revelation-new-entry"
STOCK_NEW_FOLDER		= "revelation-new-folder"
STOCK_NEXT			= "revelation-next"
STOCK_PASSWORD_CHANGE		= "revelation-password-change"
STOCK_PASSWORD_CHECK		= "revelation-password-check"
STOCK_PASSWORD_STRONG		= "revelation-password-strong"
STOCK_PASSWORD_WEAK		= "revelation-password-weak"
STOCK_PREVIOUS			= "revelation-previous"
STOCK_RELOAD			= "revelation-reload"
STOCK_REMOVE			= "revelation-remove"
STOCK_REPLACE			= "revelation-replace"
STOCK_UNKNOWN			= "revelation-unknown"
STOCK_UNLOCK			= "revelation-unlock"
STOCK_UPDATE			= "revelation-update"
STOCK_WARNING			= "revelation-warning"


STOCK_ENTRY_FOLDER		= "revelation-account-folder"
STOCK_ENTRY_FOLDER_OPEN		= "revelation-account-folder-open"
STOCK_ENTRY_CREDITCARD		= "revelation-account-creditcard"
STOCK_ENTRY_CRYPTOKEY		= "revelation-account-cryptokey"
STOCK_ENTRY_DATABASE		= "revelation-account-database"
STOCK_ENTRY_DOOR		= "revelation-account-door"
STOCK_ENTRY_EMAIL		= "revelation-account-email"
STOCK_ENTRY_FTP			= "revelation-account-ftp"
STOCK_ENTRY_GENERIC		= "revelation-account-generic"
STOCK_ENTRY_PHONE		= "revelation-account-phone"
STOCK_ENTRY_SHELL		= "revelation-account-shell"
STOCK_ENTRY_WEBSITE		= "revelation-account-website"

STOCK_REVELATION		= "revelation-revelation"
STOCK_REVELATION_LOCKED		= "revelation-revelation-locked"


ICON_SIZE_APPLET		= gtk.ICON_SIZE_LARGE_TOOLBAR
ICON_SIZE_DATAVIEW		= gtk.ICON_SIZE_LARGE_TOOLBAR
ICON_SIZE_DROPDOWN		= gtk.ICON_SIZE_SMALL_TOOLBAR
ICON_SIZE_ENTRY			= gtk.ICON_SIZE_MENU
ICON_SIZE_FALLBACK		= gtk.ICON_SIZE_LARGE_TOOLBAR
ICON_SIZE_HEADLINE		= gtk.ICON_SIZE_LARGE_TOOLBAR
ICON_SIZE_LABEL			= gtk.ICON_SIZE_MENU
ICON_SIZE_LOGO			= gtk.ICON_SIZE_DND
ICON_SIZE_TREEVIEW		= gtk.ICON_SIZE_MENU

STOCK_ICONS			= (
	( STOCK_REVELATION,		"revelation" ),
	( STOCK_REVELATION_LOCKED,	"revelation-locked" ),
	( STOCK_ENTRY_CREDITCARD,	"stock_creditcard" ),
	( STOCK_ENTRY_CRYPTOKEY,	"stock_keyring" ),
	( STOCK_ENTRY_DATABASE,		"stock_data-sources" ),
	( STOCK_ENTRY_DOOR,		"stock_exit" ),
	( STOCK_ENTRY_EMAIL,		"stock_mail" ),
	( STOCK_ENTRY_FTP,		"system-file-manager" ),
	( STOCK_ENTRY_GENERIC,		"stock_lock" ),
	( STOCK_ENTRY_PHONE,		"stock_cell-phone" ),
	( STOCK_ENTRY_SHELL,		"gnome-terminal" ),
	( STOCK_ENTRY_WEBSITE,		"stock_hyperlink-toolbar" ),
	( STOCK_ENTRY_FOLDER,		"stock_folder" ),
	( STOCK_ENTRY_FOLDER_OPEN,	"stock_folder" ),
)

STOCK_ITEMS = (
	( STOCK_CONTINUE,		_('_Continue'),			"stock_test-mode" ),
	( STOCK_DISCARD,		_('_Discard'),			gtk.STOCK_DELETE ),
	( STOCK_EDIT,			_('_Edit'),			"stock_edit" ),
	( STOCK_EXPORT,			_('_Export'),			gtk.STOCK_EXECUTE ),
	( STOCK_FOLDER,			'',				"stock_folder" ),
	( STOCK_GENERATE,		_('_Generate'),			gtk.STOCK_EXECUTE ),
	( STOCK_GOTO,			_('_Go to'),			gtk.STOCK_JUMP_TO ),
	( STOCK_IMPORT,			_('_Import'),			gtk.STOCK_CONVERT ),
	( STOCK_LOCK,			_('_Lock'),			"stock_lock" ),
	( STOCK_NEW_ENTRY,		_('_Add Entry'),		gtk.STOCK_ADD ),
	( STOCK_NEW_FOLDER,		_('_Add Folder'),		"stock_folder" ),
	( STOCK_NEXT,			_('Next'),			gtk.STOCK_GO_DOWN ),
	( STOCK_PASSWORD_CHANGE,	_('_Change'),			"stock_lock-ok" ),
	( STOCK_PASSWORD_CHECK,		_('_Check'),			"stock_lock-ok" ),
	( STOCK_PASSWORD_STRONG,	'',				"stock_lock-ok" ),
	( STOCK_PASSWORD_WEAK,		'',				"stock_lock-broken" ),
	( STOCK_PREVIOUS,		_('Previous'),			gtk.STOCK_GO_UP ),
	( STOCK_RELOAD,			_('_Reload'),			gtk.STOCK_REFRESH ),
	( STOCK_REMOVE,			_('Re_move'),			gtk.STOCK_DELETE ),
	( STOCK_REPLACE,		_('_Replace'),			gtk.STOCK_SAVE_AS ),
	( STOCK_UNKNOWN,		_('Unknown'),			gtk.STOCK_DIALOG_QUESTION ),
	( STOCK_UNLOCK,			_('_Unlock'),			"stock_lock-open" ),
	( STOCK_UPDATE,			_('_Update'),			"stock_edit" ),
	( STOCK_WARNING,		'',				"stock_dialog-warning" ),
)

class StockFactory(shinygnome.ui.StockFactory):
	"A stock item factory"

	def __init__(self, parent, searchpath = None):
		shinygnome.ui.StockFactory.__init__(self, parent, searchpath)

		# load icons
		for id, icon in STOCK_ICONS:
			self.copy(id, icon)

		# load items
		for id, name, icon in STOCK_ITEMS:
			self.add_item(id, name, icon)

