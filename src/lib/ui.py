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

import config, data, dialog, entry, io, stock, shinygnome.ui, util

import bonobo.ui, gettext, gobject, gtk, gtk.gdk, gnome.ui, time

_ = gettext.gettext


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



##### TOOLBARS #####
SeparatorToolItem	= shinygnome.ui.SeparatorToolItem
Toolbar			= shinygnome.ui.Toolbar
ToolButton		= shinygnome.ui.ToolButton
ToolItem		= shinygnome.ui.ToolItem



class Searchbar(Toolbar):
	"A toolbar for easy searching"

	def __init__(self):
		Toolbar.__init__(self)

		self.label		= Label("  " + _('  Find:') + " ")
		self.entry		= Entry()
		self.dropdown		= EntryDropDown()
		self.dropdown.insert_item(0, _('Any type'), "gnome-stock-about")
		self.button_next	= ToolButton(stock.STOCK_NEXT, important = True)
		self.button_prev	= ToolButton(stock.STOCK_PREVIOUS, important = True)

		self.append(ToolItem(self.label))
		self.append(ToolItem(self.entry), _('Text to search for'))
		self.append(ToolItem(EventBox(self.dropdown)), _('The type of account to search for'))
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



##### DISPLAY WIDGETS #####

Image		= shinygnome.ui.Image
Label		= shinygnome.ui.Label
Statusbar	= shinygnome.ui.Statusbar
TextView	= shinygnome.ui.TextView

class ImageLabel(HBox):
	"A label with an image"

	def __init__(self, text = None, stock = None, size = gtk.ICON_SIZE_MENU):
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

			menuitem = ImageMenuItem(gtk.stock.STOCK_COPY, _('Copy password'))
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
			menuitem.connect("activate", lambda w: self.clipboard.set(self.get_text(), True))

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
			cr.set_fixed_size(gtk.icon_size_lookup(gtk.ICON_SIZE_SMALL_TOOLBAR)[0] + 5, -1)
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
		cr.set_property("stock-size", gtk.ICON_SIZE_MENU)

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
			self.statusbar.set(item.tooltip)

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
			e.icon, gtk.ICON_SIZE_LARGE_TOOLBAR
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

