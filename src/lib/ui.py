#
# Revelation - a password manager for GNOME 2
# http://oss.codepoet.no/revelation/
# $Id$
#
# Module for UI functionality
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

import account, config, data, entry, io, stock, shinygnome.ui, shinygnome.util, util

import gettext, gtk, gtk.gdk, time

_ = gettext.gettext


##### SHINYGNOME WIDGETS #####

Action			= shinygnome.ui.Action
ActionGroup		= shinygnome.ui.ActionGroup
Alignment		= shinygnome.ui.Alignment
App			= shinygnome.ui.App
Button			= shinygnome.ui.Button
CheckButton		= shinygnome.ui.CheckButton
ComboBox		= shinygnome.ui.ComboBox
ComboBoxEntry		= shinygnome.ui.ComboBoxEntry
Entry			= shinygnome.ui.Entry
EventBox		= shinygnome.ui.EventBox
FileChooserButton	= shinygnome.ui.FileChooserButton
HBox			= shinygnome.ui.HBox
HButtonBox		= shinygnome.ui.HButtonBox
HPaned			= shinygnome.ui.HPaned
IconEntry		= shinygnome.ui.IconEntry
Image			= shinygnome.ui.Image
ImageLabel		= shinygnome.ui.ImageLabel
ImageMenuItem		= shinygnome.ui.ImageMenuItem
InputBox		= shinygnome.ui.InputBox
Label			= shinygnome.ui.Label
LinkButton		= shinygnome.ui.LinkButton
Menu			= shinygnome.ui.Menu
Notebook		= shinygnome.ui.Notebook
NotebookPage		= shinygnome.ui.NotebookPage
RadioButton		= shinygnome.ui.RadioButton
ScrolledWindow		= shinygnome.ui.ScrolledWindow
SeparatorToolItem	= shinygnome.ui.SeparatorToolItem
SimpleComboBox		= shinygnome.ui.SimpleComboBox
SimpleComboBoxEntry	= shinygnome.ui.SimpleComboBoxEntry
SizeGroup		= shinygnome.ui.SizeGroup
SpinButton		= shinygnome.ui.SpinButton
Statusbar		= shinygnome.ui.Statusbar
Table			= shinygnome.ui.Table
TextView		= shinygnome.ui.TextView
ToggleAction		= shinygnome.ui.ToggleAction
Toolbar			= shinygnome.ui.Toolbar
ToolButton		= shinygnome.ui.ToolButton
ToolItem		= shinygnome.ui.ToolItem
TreeView		= shinygnome.ui.TreeView
UIManager		= shinygnome.ui.UIManager
VBox			= shinygnome.ui.VBox



##### PASSWORD WIDGETS #####

class PasswordEntry(IconEntry):
	"An entry for editing a password (follows the 'show passwords' preference)"

	def __init__(self, password = None, cfg = None, clipboard = None):
		IconEntry.__init__(self, password)
		self.set_visibility(False)

		self.autocheck	= True
		self.config	= cfg
		self.clipboard	= clipboard

		self.connect("changed", self.__cb_check_password)
		self.connect("populate-popup", self.__cb_popup)

		if cfg != None:
			self.config.monitor("view/passwords", lambda k,v,d: self.set_visibility(v))


	def __cb_check_password(self, widget, data = None):
		"Callback for changed, checks the password"

		if self.autocheck == False:
			return

		password = self.get_text()

		if len(password) == 0:
			self.remove_icon()

		else:
			try:
				util.check_password(password)

			except ValueError, reason:
				self.set_password_strong(False, _('The password %s') % str(reason))

			else:
				self.set_password_strong(True, _('The password seems good'))


	def __cb_popup(self, widget, menu):
		"Populates the popup menu"

		if self.clipboard != None:
			menuitem = ImageMenuItem(gtk.stock.STOCK_COPY, _('Copy password'))
			menuitem.connect("activate", lambda w: self.clipboard.set_text(self.get_text(), True))

			menu.insert(menuitem, 2)

		menu.show_all()


	def set_password_strong(self, strong, reason = ""):
		"Sets whether the password is strong or not"

		self.set_icon(strong == True and stock.STOCK_PASSWORD_STRONG or stock.STOCK_PASSWORD_WEAK, reason)



class PasswordEntryGenerate(HBox):
	"A password entry with a generator button"

	def __init__(self, password = None, cfg = None, clipboard = None):
		HBox.__init__(self)
		self.config = cfg

		self.pwentry = PasswordEntry(password, cfg, clipboard)
		self.pack_start(self.pwentry)

		self.button = Button(_('Generate'), lambda w: self.generate())
		self.pack_start(self.button, False, False)

		self.entry = self.pwentry.entry


	def generate(self):
		"Generates a password for the entry"

		password = util.generate_password(self.config.get("passwordgen/length"))
		self.pwentry.set_text(password)


	def get_text(self):
		"Wrapper for the entry"

		return self.pwentry.get_text()


	def set_text(self, text):
		"Wrapper for the entry"

		self.pwentry.set_text(text)



class PasswordLabel(EventBox):
	"A label for displaying passwords"

	def __init__(self, password = "", cfg = None, clipboard = None, justify = gtk.JUSTIFY_LEFT):
		EventBox.__init__(self)

		self.password	= shinygnome.util.text.unescape_markup(password)
		self.config	= cfg
		self.clipboard	= clipboard

		self.label = Label(shinygnome.util.text.escape_markup(self.password), justify)
		self.label.set_selectable(True)
		self.add(self.label)

		if self.config is not None:
			try:
				self.config.monitor("view/passwords", lambda k,v,d: self.show_password(v))

			except config.ConfigError:
				self.config.monitor("show_passwords", lambda k,v,d: self.show_password(v))

		self.connect("button-press-event", self.__cb_button_press)
		self.connect("drag-data-get", self.__cb_drag_data_get)


	def __cb_drag_data_get(self, widget, context, selection, info, timestamp, data = None):
		"Provides data for a drag operation"

		selection.set_text(self.password, -1)


	def __cb_button_press(self, widget, data = None):
		"Populates the popup menu"

		if self.label.get_selectable() == True:
			return False

		elif data.button == 3:
			menu = Menu()

			menuitem = ImageMenuItem(gtk.stock.STOCK_COPY, _('Copy password'))
			menuitem.connect("activate", lambda w: self.clipboard.set_text(self.password, True))
			menu.append(menuitem)

			menu.show_all()
			menu.popup(None, None, None, data.button, data.time)

			return True


	def set_ellipsize(self, ellipsize):
		"Sets ellipsize for the label"

		self.label.set_ellipsize(ellipsize)


	def show_password(self, show = True):
		"Sets whether to display the password"

		if show == True:
			self.label.set_text(shinygnome.util.text.escape_markup(self.password))
			self.label.set_selectable(True)
			self.drag_source_unset()

		else:
			self.label.set_text("******")
			self.label.set_selectable(False)

			self.drag_source_set(
				gtk.gdk.BUTTON1_MASK,
				(
					("text/plain", 0, 0),
					("TEXT", 0, 1),
					("STRING", 0, 2),
					("COMPOUND TEXT", 0, 3),
					("UTF8_STRING", 0, 4),
				),
				gtk.gdk.ACTION_COPY
			)



##### ACCOUNT WIDGETS #####

class AccountList(shinygnome.ui.TreeView):
	"An account list"

	def __init__(self, accountstore):
		shinygnome.ui.TreeView.__init__(self, accountstore)

		cr_icon	= shinygnome.ui.CellRendererPixbuf(stock_size = gtk.ICON_SIZE_MENU)
		cr_name	= shinygnome.ui.CellRendererText()

		column = shinygnome.ui.TreeViewColumn(None)
		column.pack_start(cr_icon, False)
		column.pack_start(cr_name)
		column.add_attribute(cr_icon, "stock-id", 0)
		column.add_attribute(cr_name, "text", 1)
		self.append_column(column)



class AccountTypeDropdown(shinygnome.ui.SimpleComboBox):
	"An account type dropdown"

	def __init__(self, accounttypes):
		shinygnome.ui.SimpleComboBox.__init__(self, True)

		for accounttype in accounttypes:
			self.append_item(accounttype.name, accounttype.icon, accounttype)


	def get_active_accounttype(self):
		"Returns the currently active accounttype"

		item = self.get_active_item()

		if item:
			return item[-1]


	def set_active_accounttype(self, accounttype):
		"Sets the active accounttype"

		for i in range(self.model.iter_n_children(None)):
			iter = self.model.iter_nth_child(None, i)

			if self.model.get_value(iter, 2) == accounttype:
				self.set_active(i)



class AccountView(VBox):
	"An account display widget"

	def __init__(self, account = None):
		VBox.__init__(self)
		self.set_spacing(12)
		self.set_border_width(12)

		self.account = None

		if account:
			self.display(account)


	def clear(self):
		"Clears the account view"

		self.account = None

		VBox.clear(self)


	def display(self, acct):
		"Displays an account"

		self.clear()

		if not acct:
			return

		self.account = acct

		# set up metadata display
		metabox = VBox(
			Alignment(ImageLabel(
				"<span size=\"large\" weight=\"bold\">%s</span>" % shinygnome.util.text.escape_markup(acct.name),
				acct.accounttype.icon, gtk.ICON_SIZE_LARGE_TOOLBAR
			)),
			Label(
				"<span weight=\"bold\">%s%s</span>%s" % (
					shinygnome.util.text.escape_markup(acct.accounttype.name),
					acct.description != "" and ": " or "",
					shinygnome.util.text.escape_markup(acct.description)
				), gtk.JUSTIFY_CENTER
			)
		)

		self.pack_start(Alignment(metabox), False, False)

		# set up field display
		fields = [ field for field in acct.fields if field.value != "" ]

		if fields:
			table = Table(2, len(fields))
			self.pack_start(Alignment(table))

			for rowindex, field in zip(range(len(fields)), fields):
				table.attach(Label("<span weight=\"bold\">%s:</span>" % shinygnome.util.text.escape_markup(field.name)), 0, rowindex)
				table.attach(field.get_display_widget(), 1, rowindex)

		# display modified time
		self.pack_start(Alignment(Label(
			_("Updated %s ago\n%s") % (
				util.time_period_rough(acct.modified, time.time()),
				time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(acct.modified))
			), gtk.JUSTIFY_CENTER
		)))

		self.show_all()



##### ENTRY WIDGETS #####

class EntryView(VBox):
	"A component for displaying an entry"

	def __init__(self, cfg = None, clipboard = None):
		VBox.__init__(self)
		self.set_spacing(12)
		self.set_border_width(12)

		self.config		= cfg
		self.clipboard		= clipboard
		self.entry		= None


	def clear(self, force = False):
		"Clears the data view"

		self.entry = None

		for child in self.get_children():
			child.destroy()


	def display_entry(self, e):
		"Displays info about an entry"

		self.clear()
		self.entry = e

		if self.entry == None:
			return

		# set up metadata display
		metabox = VBox()
		self.pack_start(metabox)

		label = ImageLabel(
			"<span size=\"large\" weight=\"bold\">%s</span>" % shinygnome.util.text.escape_markup(e.name),
			e.icon, gtk.ICON_SIZE_LARGE_TOOLBAR
		)
		metabox.pack_start(Alignment(label, 0.5, 0.5, 0, 0))

		label = Label("<span weight=\"bold\">%s</span>%s" % ( e.typename + (e.description != "" and ": " or ""), shinygnome.util.text.escape_markup(e.description) ), gtk.JUSTIFY_CENTER)
		metabox.pack_start(label)

		# set up field list
		fields = [ field for field in e.fields if field.value != "" ]

		if len(fields) > 0:
			table = Table(2, len(fields))
			self.pack_start(table)

			for rowindex, field in zip(range(len(fields)), fields):
				label = Label("<span weight=\"bold\">%s:</span>" % shinygnome.util.text.escape_markup(field.name))
				table.attach(label, 0, rowindex)

				widget = generate_field_display_widget(field, self.config, self.clipboard)
				table.attach(widget, 1, rowindex)

		# display updatetime
		if type(e) != entry.FolderEntry:
			label = Label((_('Updated %s ago') + "\n%s") % ( util.time_period_rough(e.updated, time.time()), time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(e.updated)) ), gtk.JUSTIFY_CENTER)
			self.pack_start(label)

		self.show_all()


	def pack_start(self, widget):
		"Adds a widget to the data view"

		alignment = Alignment(widget, 0.5, 0.5, 0, 0)
		VBox.pack_start(self, alignment, False, False)



class Searchbar(Toolbar):
	"A toolbar for easy searching"

	def __init__(self):
		Toolbar.__init__(self)

		self.label		= Label("  " + _('  Find:') + " ")
		self.entry		= Entry()
		#self.dropdown		= EntryDropDown()
		#self.dropdown.insert_item(0, _('Any type'), "gnome-stock-about")
		self.button_next	= ToolButton(stock.STOCK_NEXT, important = True)
		self.button_prev	= ToolButton(stock.STOCK_PREVIOUS, important = True)

		self.append(ToolItem(self.label))
		self.append(ToolItem(self.entry), _('Text to search for'))
		#self.append(ToolItem(EventBox(self.dropdown)), _('The type of account to search for'))
		self.append(SeparatorToolItem())
		self.append(self.button_next, _('Find the next match'))
		self.append(self.button_prev, _('Find the previous match'))

		self.connect("show", self.__cb_show)

		self.entry.connect("changed", self.__cb_entry_changed)
		self.entry.connect("key-press-event", self.__cb_key_press)

		self.button_next.set_sensitive(False)
		self.button_prev.set_sensitive(False)


	def __cb_entry_changed(self, widget, data = None):
		"Callback for entry changes"

		s = self.entry.get_text() != ""

		self.button_next.set_sensitive(s)
		self.button_prev.set_sensitive(s)


	def __cb_key_press(self, widget, data = None):
		"Callback for key presses"

		# return
		if data.keyval == 65293 and widget.get_text() != "":
			if data.state & gtk.gdk.SHIFT_MASK == gtk.gdk.SHIFT_MASK:
				self.button_prev.activate()

			else:
				self.button_next.activate()

			return True


	def __cb_show(self, widget, data = None):
		"Callback for widget display"

		self.set_style(gtk.TOOLBAR_BOTH_HORIZ)
		self.entry.select_region(0, -1)
		self.entry.grab_focus()

