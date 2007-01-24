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

import config, data, dialog, entry, io, shinygnome.ui, util

import bonobo.ui, gettext, gobject, gtk, gtk.gdk, gnome.ui, os, pango, pwd, time

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
	( STOCK_REVELATION,		"revelation",			( ICON_SIZE_APPLET, ICON_SIZE_LOGO, gtk.ICON_SIZE_DIALOG, gtk.ICON_SIZE_MENU )),
	( STOCK_REVELATION_LOCKED,	"revelation-locked",		( ICON_SIZE_APPLET, ICON_SIZE_LOGO, gtk.ICON_SIZE_DIALOG, gtk.ICON_SIZE_MENU )),
	( STOCK_ENTRY_CREDITCARD,	"stock_creditcard",		( ICON_SIZE_DATAVIEW, ICON_SIZE_DROPDOWN, ICON_SIZE_ENTRY, ICON_SIZE_TREEVIEW )),
	( STOCK_ENTRY_CRYPTOKEY,	"stock_keyring",		( ICON_SIZE_DATAVIEW, ICON_SIZE_DROPDOWN, ICON_SIZE_ENTRY, ICON_SIZE_TREEVIEW )),
	( STOCK_ENTRY_DATABASE,		"stock_data-sources",		( ICON_SIZE_DATAVIEW, ICON_SIZE_DROPDOWN, ICON_SIZE_ENTRY, ICON_SIZE_TREEVIEW )),
	( STOCK_ENTRY_DOOR,		"stock_exit",			( ICON_SIZE_DATAVIEW, ICON_SIZE_DROPDOWN, ICON_SIZE_ENTRY, ICON_SIZE_TREEVIEW )),
	( STOCK_ENTRY_EMAIL,		"stock_mail",			( ICON_SIZE_DATAVIEW, ICON_SIZE_DROPDOWN, ICON_SIZE_ENTRY, ICON_SIZE_TREEVIEW )),
	( STOCK_ENTRY_FTP,		"system-file-manager",		( ICON_SIZE_DATAVIEW, ICON_SIZE_DROPDOWN, ICON_SIZE_ENTRY, ICON_SIZE_TREEVIEW )),
	( STOCK_ENTRY_GENERIC,		"stock_lock",			( ICON_SIZE_DATAVIEW, ICON_SIZE_DROPDOWN, ICON_SIZE_ENTRY, ICON_SIZE_TREEVIEW )),
	( STOCK_ENTRY_PHONE,		"stock_cell-phone",		( ICON_SIZE_DATAVIEW, ICON_SIZE_DROPDOWN, ICON_SIZE_ENTRY, ICON_SIZE_TREEVIEW )),
	( STOCK_ENTRY_SHELL,		"gnome-terminal",		( ICON_SIZE_DATAVIEW, ICON_SIZE_DROPDOWN, ICON_SIZE_ENTRY, ICON_SIZE_TREEVIEW )),
	( STOCK_ENTRY_WEBSITE,		"stock_hyperlink-toolbar",	( ICON_SIZE_DATAVIEW, ICON_SIZE_DROPDOWN, ICON_SIZE_ENTRY, ICON_SIZE_TREEVIEW )),
	( STOCK_ENTRY_FOLDER,		"stock_folder",			( ICON_SIZE_DATAVIEW, ICON_SIZE_DROPDOWN, ICON_SIZE_ENTRY, ICON_SIZE_TREEVIEW )),
	( STOCK_ENTRY_FOLDER_OPEN,	"stock_folder",			( ICON_SIZE_DATAVIEW, ICON_SIZE_DROPDOWN, ICON_SIZE_ENTRY, ICON_SIZE_TREEVIEW )),
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



##### FUNCTIONS #####

def generate_field_display_widget(field, cfg = None, userdata = None):
	"Generates a widget for displaying a field value"

	if field.datatype == entry.DATATYPE_EMAIL:
		widget = LinkButton("mailto:%s" % field.value, util.escape_markup(field.value))

	elif field.datatype == entry.DATATYPE_PASSWORD:
		widget = PasswordLabel(util.escape_markup(field.value), cfg, userdata)

	elif field.datatype == entry.DATATYPE_URL:
		widget = LinkButton(field.value, util.escape_markup(field.value))

	else:
		widget = Label(util.escape_markup(field.value))
		widget.set_selectable(True)

	return widget


def generate_field_edit_widget(field, cfg = None, userdata = None):
	"Generates a widget for editing a field"

	if type(field) == entry.PasswordField:
		widget = PasswordEntryGenerate(None, cfg, userdata)

	elif type(field) == entry.UsernameField:
		widget = ComboBoxEntry(userdata)

	elif field.datatype == entry.DATATYPE_FILE:
		widget = FileEntry()

	elif field.datatype == entry.DATATYPE_PASSWORD:
		widget = PasswordEntry(None, cfg, userdata)

	else:
		widget = Entry()

	widget.set_text(field.value)

	return widget



##### CONTAINERS #####

Alignment	= shinygnome.ui.Alignment
EventBox	= shinygnome.ui.EventBox
HBox		= shinygnome.ui.HBox
HButtonBox	= shinygnome.ui.HButtonBox
HPaned		= shinygnome.ui.HPaned
Notebook	= shinygnome.ui.Notebook
ScrolledWindow	= shinygnome.ui.ScrolledWindow
Table		= shinygnome.ui.Table
VBox		= shinygnome.ui.VBox


class NotebookPage(VBox):
	"A notebook page"

	def __init__(self):
		VBox.__init__(self)

		self.sizegroup = gtk.SizeGroup(gtk.SIZE_GROUP_HORIZONTAL)
		self.set_border_width(12)
		self.set_spacing(18)


	def add_section(self, title, description = None):
		"Adds an input section to the notebook"

		section = InputSection(title, description, self.sizegroup)
		self.pack_start(section, False, False)

		return section



class Toolbar(gtk.Toolbar):
	"A Toolbar subclass"

	def __init__(self):
		gtk.Toolbar.__init__(self)

		self.tooltips	= gtk.Tooltips()


	def append_space(self):
		"Appends a space to the toolbar"

		space = gtk.SeparatorToolItem()
		space.set_draw(False)

		self.insert(space, -1)


	def append_widget(self, widget, tooltip = None):
		"Appends a widget to the toolbar"

		toolitem = gtk.ToolItem()
		toolitem.add(widget)

		if tooltip != None:
			toolitem.set_tooltip(self.tooltips, tooltip)

		self.insert(toolitem, -1)



class InputSection(VBox):
	"A section of input fields"

	def __init__(self, title = None, description = None, sizegroup = None):
		VBox.__init__(self)

		self.title	= None
		self.desc	= None
		self.sizegroup	= sizegroup

		if title is not None:
			self.title = Label("<span weight=\"bold\">%s</span>" % util.escape_markup(title))
			self.pack_start(self.title, False)

		if description is not None:
			self.desc = Label(util.escape_markup(description))
			self.pack_start(self.desc, False)

		if sizegroup is None:
			self.sizegroup = gtk.SizeGroup(gtk.SIZE_GROUP_HORIZONTAL)


	def append_widget(self, title, widget, indent = True):
		"Adds a widget to the section"

		row = HBox()
		row.set_spacing(12)
		self.pack_start(row, False, False)

		if self.title is not None and indent == True:
			row.pack_start(Label(""), False, False)

		if title is not None:
			label = Label("%s:" % util.escape_markup(title))
			self.sizegroup.add_widget(label)
			row.pack_start(label, False, False)

		row.pack_start(widget)


	def clear(self):
		"Removes all widgets"

		for child in self.get_children():
			if child not in ( self.title, self.desc ):
				child.destroy()



##### DISPLAY WIDGETS #####

Image		= shinygnome.ui.Image
Label		= shinygnome.ui.Label
TextView	= shinygnome.ui.TextView

class ImageLabel(HBox):
	"A label with an image"

	def __init__(self, text = None, stock = None, size = ICON_SIZE_LABEL):
		HBox.__init__(self)

		self.image = Image()
		self.pack_start(self.image, False, True)

		self.label = Label(text)
		self.pack_start(self.label)

		if text != None:
			self.set_text(text)

		if stock != None:
			self.set_stock(stock, size)


	def set_ellipsize(self, ellipsize):
		"Sets label ellisization"

		self.label.set_ellipsize(ellipsize)


	def set_stock(self, stock, size):
		"Sets the image"

		self.image.set_from_stock(stock, size)


	def set_text(self, text):
		"Sets the label text"

		self.label.set_text(text)



class PasswordLabel(EventBox):
	"A label for displaying passwords"

	def __init__(self, password = "", cfg = None, clipboard = None, justify = gtk.JUSTIFY_LEFT):
		EventBox.__init__(self)

		self.password	= util.unescape_markup(password)
		self.config	= cfg
		self.clipboard	= clipboard

		self.label = Label(util.escape_markup(self.password), justify)
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

			menuitem = ImageMenuItem(gtk.STOCK_COPY, _('Copy password'))
			menuitem.connect("activate", lambda w: self.clipboard.set(self.password, True))
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
			self.label.set_text(util.escape_markup(self.password))
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



##### TEXT ENTRIES #####

Entry		= shinygnome.ui.Entry
IconEntry	= shinygnome.ui.IconEntry
SpinButton	= shinygnome.ui.SpinButton


class ComboBoxEntry(gtk.ComboBoxEntry):
	"An entry with a combo box list"

	def __init__(self, list = []):
		gtk.ComboBoxEntry.__init__(self)

		self.entry = self.child
		self.entry.set_activates_default(True)

		self.model = gtk.ListStore(gobject.TYPE_STRING)
		self.set_model(self.model)
		self.set_text_column(0)

		self.completion = gtk.EntryCompletion()
		self.completion.set_model(self.model)
		self.completion.set_text_column(0)
		self.completion.set_minimum_key_length(1)
		self.entry.set_completion(self.completion)

		if list is not None:
			self.set_values(list)


	def get_text(self):
		"Returns the text of the entry"

		return self.entry.get_text()


	def set_text(self, text):
		"Sets the text of the entry"

		if text is None:
			self.entry.set_text("")

		else:
			self.entry.set_text(text)


	def set_values(self, list):
		"Sets the values for the dropdown"

		self.model.clear()

		for item in list:
			self.model.append((item,))



class FileEntry(HBox):
	"A file entry"

	def __init__(self, title = None, file = None, type = gtk.FILE_CHOOSER_ACTION_OPEN):
		HBox.__init__(self)

		self.title = title is not None and title or _('Select File')
		self.type = type

		self.entry = Entry()
		self.entry.connect("changed", lambda w: self.emit("changed"))
		self.pack_start(self.entry)

		self.button = Button(_('Browse...'), self.__cb_filesel)
		self.pack_start(self.button, False, False)

		if file is not None:
			self.set_filename(file)


	def __cb_filesel(self, widget, data = None):
		"Displays a file selector when Browse is pressed"

		try:
			fsel = dialog.FileSelector(None, self.title, self.type)
			file = self.get_filename()

			if file != None:
				fsel.set_filename(file)

			self.set_filename(fsel.run())

		except dialog.CancelError:
			pass


	def get_filename(self):
		"Gets the current filename"

		return io.file_normpath(self.entry.get_text())


	def get_text(self):
		"Wrapper to emulate Entry"

		return self.entry.get_text()


	def set_filename(self, filename):
		"Sets the current filename"

		self.entry.set_text(io.file_normpath(filename))
		self.entry.set_position(-1)


	def set_text(self, text):
		"Wrapper to emulate Entry"

		self.entry.set_text(text)


gobject.type_register(FileEntry)
gobject.signal_new("changed", FileEntry, gobject.SIGNAL_ACTION, gobject.TYPE_BOOLEAN, ())



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
			menuitem = ImageMenuItem(gtk.STOCK_COPY, _('Copy password'))
			menuitem.connect("activate", lambda w: self.clipboard.set(self.get_text(), True))

			menu.insert(menuitem, 2)

		menu.show_all()


	def set_password_strong(self, strong, reason = ""):
		"Sets whether the password is strong or not"

		self.set_icon(strong == True and STOCK_PASSWORD_STRONG or STOCK_PASSWORD_WEAK, reason)



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



##### BUTTONS #####

Button		= shinygnome.ui.Button
CheckButton	= shinygnome.ui.CheckButton
RadioButton	= shinygnome.ui.RadioButton


class DropDown(gtk.ComboBox):
	"A dropdown button"

	def __init__(self, icons = False):
		gtk.ComboBox.__init__(self)

		self.model = gtk.ListStore(gobject.TYPE_STRING, gobject.TYPE_STRING, gobject.TYPE_PYOBJECT)
		self.set_model(self.model)

		if icons == True:
			cr = gtk.CellRendererPixbuf()
			cr.set_fixed_size(gtk.icon_size_lookup(ICON_SIZE_DROPDOWN)[0] + 5, -1)
			self.pack_start(cr, False)
			self.add_attribute(cr, "stock-id", 1)

		cr = gtk.CellRendererText()
		self.pack_start(cr, True)
		self.add_attribute(cr, "text", 0)

		self.connect("realize", self.__cb_show)


	def __cb_show(self, widget, data = None):
		"Callback for when widget is shown"

		if self.get_active() == -1:
			self.set_active(0)


	def append_item(self, text, stock = None, data = None):
		"Appends an item to the dropdown"

		self.model.append( ( text, stock, data ) )


	def delete_item(self, index):
		"Removes an item from the dropdown"

		if self.model.iter_n_children(None) > index:
			iter = self.model.iter_nth_child(None, index)
			self.model.remove(iter)


	def get_active_item(self):
		"Returns a tuple with data for the current item"

		iter = self.model.iter_nth_child(None, self.get_active())
		return self.model.get(iter, 0, 1, 2)


	def get_item(self, index):
		"Returns data for an item"

		return self.model.get(self.model.iter_nth_child(None, index), 0, 1, 2)


	def get_num_items(self):
		"Returns the number of items in the dropdown"

		return self.model.iter_n_children(None)


	def insert_item(self, index, text, stock = None, data = None):
		"Inserts an item in the dropdown"

		self.model.insert(index, ( text, stock, data ) )



class EntryDropDown(DropDown):
	"An entry type dropdown"

	def __init__(self):
		DropDown.__init__(self, True)

		for e in entry.ENTRYLIST:
			if e != entry.FolderEntry:
				self.append_item(e().typename, e().icon, e)


	def get_active_type(self):
		"Get the currently active type"

		item = self.get_active_item()

		if item is not None:
			return item[2]


	def set_active_type(self, entrytype):
		"Set the active type"

		for i in range(self.model.iter_n_children(None)):
			iter = self.model.iter_nth_child(None, i)

			if self.model.get_value(iter, 2) == entrytype:
				self.set_active(i)


class FileButton(gtk.FileChooserButton):
	"A file chooser button"

	def __init__(self, title = None, file = None, type = gtk.FILE_CHOOSER_ACTION_OPEN):
		gtk.FileChooserButton.__init__(self, title)
		self.set_action(type)
		self.set_local_only(False)

		if file != None:
			self.set_filename(file)


	def get_filename(self):
		"Gets the filename"

		return io.file_normpath(self.get_uri())


	def set_filename(self, filename):
		"Sets the filename"

		filename = io.file_normpath(filename)

		if filename != io.file_normpath(self.get_filename()):
			gtk.FileChooserButton.set_filename(self, filename)



class LinkButton(gnome.ui.HRef):
	"A link button"

	def __init__(self, url, label):
		gnome.ui.HRef.__init__(self, url, label)
		self.set_alignment(0, 0.5)

		self.label = self.get_children()[0]


	def set_ellipsize(self, ellipsize):
		"Sets ellipsize for label"

		self.label.set_ellipsize(ellipsize)


	def set_justify(self, justify):
		"Sets justify for label"

		self.label.set_justify(justify)



##### MENUS AND MENU ITEMS #####

ImageMenuItem	= shinygnome.ui.ImageMenuItem
Menu		= shinygnome.ui.Menu



##### MISCELLANEOUS WIDGETS #####

TreeView	= shinygnome.ui.TreeView


class EntryTree(TreeView):
	"An entry tree"

	def __init__(self, entrystore):
		TreeView.__init__(self, entrystore)

		column = gtk.TreeViewColumn()
		self.append_column(column)

		cr = gtk.CellRendererPixbuf()
		column.pack_start(cr, False) 
		column.add_attribute(cr, "stock-id", data.COLUMN_ICON)
		cr.set_property("stock-size", ICON_SIZE_TREEVIEW)

		cr = gtk.CellRendererText()
		column.pack_start(cr, True)
		column.add_attribute(cr, "text", data.COLUMN_NAME)

		self.connect("doubleclick", self.__cb_doubleclick)
		self.connect("row-expanded", self.__cb_row_expanded)
		self.connect("row-collapsed", self.__cb_row_collapsed)


	def __cb_doubleclick(self, widget, iter):
		"Stop doubleclick emission on folder"

		if type(self.model.get_entry(iter)) == entry.FolderEntry:
			self.stop_emission("doubleclick")


	def __cb_row_collapsed(self, object, iter, extra):
		"Updates folder icons when collapsed"

		self.model.folder_expanded(iter, False)


	def __cb_row_expanded(self, object, iter, extra):
		"Updates folder icons when expanded"

		# make sure all children are collapsed (some may have lingering expand icons)
		for i in range(self.model.iter_n_children(iter)):
			child = self.model.iter_nth_child(iter, i)

			if self.row_expanded(self.model.get_path(child)) == False:
				self.model.folder_expanded(child, False)

		self.model.folder_expanded(iter, True)


	def set_model(self, model):
		"Sets the model displayed by the tree view"

		TreeView.set_model(self, model)

		if model is None:
			return

		for i in range(model.iter_n_children(None)):
			model.folder_expanded(model.iter_nth_child(None, i), False)



class Statusbar(gtk.Statusbar):
	"An application statusbar"

	def __init__(self):
		gtk.Statusbar.__init__(self)
		self.contextid = self.get_context_id("statusbar")


	def clear(self):
		"Clears the statusbar"

		self.pop(self.contextid)


	def set_status(self, text):
		"Displays a text in the statusbar"

		self.clear()
		self.push(self.contextid, text)



##### FACTORIES AND MANAGERS #####

class ItemFactory(gtk.IconFactory):
	"A stock item factory"

	def __init__(self, parent):
		gtk.IconFactory.__init__(self)
		self.add_default()

		self.parent	= parent
		self.theme	= gtk.icon_theme_get_default()

		if config.DIR_ICONS not in self.theme.get_search_path():
			self.theme.append_search_path(config.DIR_ICONS)

		self.__init_icons()
		self.__init_items()

		self.theme.connect("changed", self.__cb_theme_changed)


	def __init_icons(self):
		"Loads stock icons"

		for id, icon, sizes in STOCK_ICONS:
			self.create_stock_icon(id, icon, sizes)


	def __init_items(self):
		"Creates stock items"

		for id, name, icon in STOCK_ITEMS:
			self.create_stock_item(id, name, icon)


	def __cb_theme_changed(self, widget, data = None):
		"Callback for changed theme"

		self.__init_icons()
		self.__init_items()


	def create_stock_icon(self, id, icon, sizes):
		"Creates a stock icon from a different stock icon"

		iconset = gtk.IconSet()
		self.add(id, iconset)

		if self.theme.has_icon(icon) == False:
			return

		# load icons (the dict.fromkeys() thing is to remove duplicates)
		for size in dict.fromkeys(sizes).keys():
			source = self.get_iconsource(icon, size)

			if source != None:
				iconset.add_source(source)


		# load fallback icon if none were found
		if len(iconset.get_sizes()) == 0:
			source = self.get_iconsource(icon, ICON_SIZE_FALLBACK, True)

			if source != None:
				iconset.add_source(source)


	def create_stock_item(self, id, name, icon = None):
		"Creates a stock item"

		gtk.stock_add(((id, name, 0, 0, None), ))

		if icon is None:
			pass

		elif gtk.stock_lookup(icon) is not None:
			self.add(id, self.parent.get_style().lookup_icon_set(icon))

		else:
			self.create_stock_icon(id, icon, ( gtk.ICON_SIZE_SMALL_TOOLBAR, gtk.ICON_SIZE_LARGE_TOOLBAR, gtk.ICON_SIZE_MENU, gtk.ICON_SIZE_BUTTON, gtk.ICON_SIZE_DIALOG, ICON_SIZE_LABEL, ICON_SIZE_HEADLINE ))


	def get_iconsource(self, id, size, wildcard = False):
		"Loads an icon as an iconsource"

		width, height	= gtk.icon_size_lookup(size)
		pixbuf		= self.get_pixbuf(id, width)

		if pixbuf == None:
			return

		# reject icons more than 4 pixels away from requested size if not wildcard
		elif wildcard == False and not width - 4 <= pixbuf.get_property("width") <= width + 4:
			return

		elif wildcard == False and not height - 4 <= pixbuf.get_property("height") <= height + 4:
			return

		source = gtk.IconSource()
		source.set_pixbuf(pixbuf)
		source.set_size(size)
		source.set_size_wildcarded(wildcard)

		return source


	def get_pixbuf(self, id, size):
		"Loads an icon as a pixbuf"

		if self.theme.has_icon(id) == False:
			return None

		try:
			return self.theme.load_icon(id, size, 0)

		except gobject.GError:
			return None



##### ACTION HANDLING #####

Action		= shinygnome.ui.Action
ActionGroup	= shinygnome.ui.ActionGroup
ToggleAction	= shinygnome.ui.ToggleAction
UIManager	= shinygnome.ui.UIManager



##### APPLICATION COMPONENTS #####

class App(gnome.ui.App):
	"An application window"

	def __init__(self, appname):
		gnome.ui.App.__init__(self, appname, appname)

		self.statusbar = Statusbar()
		self.set_statusbar(self.statusbar)

		self.uimanager = UIManager()
		self.add_accel_group(self.uimanager.get_accel_group())


	def __connect_menu_statusbar(self, menu):
		"Connects a menus items to the statusbar"

		for item in menu.get_children():
			if isinstance(item, gtk.MenuItem) == True:
				item.connect("select", self.cb_menudesc, True)
				item.connect("deselect", self.cb_menudesc, False)


	def cb_menudesc(self, item, show):
		"Displays menu descriptions in the statusbar"

		if show == True:
			self.statusbar.set_status(item.tooltip)

		else:
			self.statusbar.clear()


	def __cb_toolbar_hide(self, widget, name):
		"Hides the toolbar dock when the toolbar is hidden"

		self.get_dock_item_by_name(name).hide()


	def __cb_toolbar_show(self, widget, name):
		"Shows the toolbar dock when the toolbar is shown"

		self.get_dock_item_by_name(name).show()


	def add_toolbar(self, toolbar, name, band, detachable):
		"Adds a toolbar"

		behavior = bonobo.ui.DOCK_ITEM_BEH_EXCLUSIVE

		if detachable == False:
			behavior |= bonobo.ui.DOCK_ITEM_BEH_LOCKED

		gnome.ui.App.add_toolbar(self, toolbar, name, behavior, 0, band, 0, 0)

		toolbar.connect("show", self.__cb_toolbar_show, name)
		toolbar.connect("hide", self.__cb_toolbar_hide, name)

		toolbar.show_all()


	def get_title(self):
		"Returns the app title"

		title = gnome.ui.App.get_title(self)

		return title.replace(" - " + config.APPNAME, "")


	def popup(self, menu, button, time):
		"Displays a popup menu"

		self.__connect_menu_statusbar(menu)
		menu.popup(None, None, None, button, time)


	def run(self):
		"Runs the application"

		self.show_all()
		gtk.main()


	def set_menus(self, menubar):
		"Sets the menubar for the application"

		for item in menubar.get_children():
			self.__connect_menu_statusbar(item.get_submenu())

		gnome.ui.App.set_menus(self, menubar)


	def set_title(self, title):
		"Sets the window title"

		gnome.ui.App.set_title(self, title + " - " + config.APPNAME)


	def set_toolbar(self, toolbar):
		"Sets the application toolbar"

		gnome.ui.App.set_toolbar(self, toolbar)
		toolbar.connect("show", self.__cb_toolbar_show, "Toolbar")
		toolbar.connect("hide", self.__cb_toolbar_hide, "Toolbar")



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
			"<span size=\"large\" weight=\"bold\">%s</span>" % util.escape_markup(e.name),
			e.icon, ICON_SIZE_DATAVIEW
		)
		metabox.pack_start(Alignment(label, 0.5, 0.5, 0, 0))

		label = Label("<span weight=\"bold\">%s</span>%s" % ( e.typename + (e.description != "" and ": " or ""), util.escape_markup(e.description) ), gtk.JUSTIFY_CENTER)
		metabox.pack_start(label)

		# set up field list
		fields = [ field for field in e.fields if field.value != "" ]

		if len(fields) > 0:
			table = Table(2, len(fields))
			self.pack_start(table)

			for rowindex, field in zip(range(len(fields)), fields):
				label = Label("<span weight=\"bold\">%s:</span>" % util.escape_markup(field.name))
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
		self.dropdown		= EntryDropDown()
		self.dropdown.insert_item(0, _('Any type'), "gnome-stock-about")
		self.button_next	= Button(STOCK_NEXT)
		self.button_prev	= Button(STOCK_PREVIOUS)

		self.append_widget(self.label)
		self.append_widget(self.entry, _('Text to search for'))
		self.append_widget(EventBox(self.dropdown), _('The type of account to search for'))
		self.append_space()
		self.append_widget(self.button_next, _('Find the next match'))
		self.append_widget(self.button_prev, _('Find the previous match'))

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

		self.entry.select_region(0, -1)
		self.entry.grab_focus()

