#
# Revelation - a password manager for GNOME 2
# http://oss.codepoet.no/revelation/
# $Id$
#
# Module with dialogs
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

import config, datahandler, entry, io, stock, ui, util
import shinygnome.ui, shinygnome.util

import gettext, gnome.ui, gobject, gtk, urllib

_ = gettext.gettext


EVENT_FILTER		= None
UNIQUE_DIALOGS		= {}


##### EXCEPTIONS #####

class CancelError(Exception):
	"Exception for dialog cancellations"
	pass



##### BASE DIALOGS #####

Dialog 			= shinygnome.ui.Dialog
FileChooserDialog	= shinygnome.ui.FileChooserDialog
Message			= shinygnome.ui.MessageDialog
Error			= shinygnome.ui.ErrorMessageDialog
Info			= shinygnome.ui.InfoMessageDialog
Question		= shinygnome.ui.QuestionMessageDialog
Warning			= shinygnome.ui.WarningMessageDialog


class Popup(gtk.Window):
	"Base class for popup (frameless) dialogs"

	def __init__(self, widget = None):
		gtk.Window.__init__(self)
		self.set_decorated(False)

		self.border = gtk.Frame()
		self.border.set_shadow_type(gtk.SHADOW_OUT)
		gtk.Window.add(self, self.border)

		if widget != None:
			self.add(widget)

		self.connect("key-press-event", self.__cb_keypress)


	def __cb_keypress(self, widget, data):
		"Callback for key presses"

		if data.keyval == 65307:
			self.close()


	def add(self, widget):
		"Adds a widget to the window"

		self.border.add(widget)


	def close(self):
		"Closes the dialog"

		self.hide()
		self.emit("closed")
		self.destroy()


	def realize(self):
		"Realizes the popup and displays children"

		gtk.Window.realize(self)

		for child in self.get_children():
			child.show_all()


	def show(self, x = None, y = None):
		"Show the dialog"

		if x != None and y != None:
			self.move(x, y)

		self.show_all()


gobject.signal_new("closed", Popup, gobject.SIGNAL_ACTION, gobject.TYPE_BOOLEAN, ())



class Utility(Dialog):
	"A utility dialog"

	def __init__(self, parent, title, buttons = ( ( gtk.STOCK_CLOSE, gtk.RESPONSE_CLOSE ), ), default = None):
		Dialog.__init__(self, parent, title, buttons, default)

		self.set_border_width(12)
		self.vbox.set_spacing(18)

		self.sizegroup	= ui.SizeGroup()
		self.tooltips	= gtk.Tooltips()


	def add_inputbox(self, title):
		"Adds an inputbox to the dialog"

		inputbox = ui.InputBox(title, self.sizegroup)
		self.vbox.pack_start(inputbox)

		return inputbox



##### QUESTION DIALOGS #####

class FileChanged(Warning):
	"Notifies about changed file"

	def __init__(self, parent, filename):
		Warning.__init__(
			self, parent, _('File has changed'), _('The current file \'%s\' has changed. Do you want to reload it?') % filename,
			( ( gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL ), ( stock.STOCK_RELOAD, gtk.RESPONSE_OK ) )
		)


	def run(self):
		"Displays the dialog"

		if Warning.run(self) == gtk.RESPONSE_OK:
			return True

		else:
			raise CancelError


class FileChanges(Warning):
	"Asks to save changes before proceeding"

	def __init__(self, parent, title, text):
		Warning.__init__(
			self, parent, title, text,
			( ( stock.STOCK_DISCARD, gtk.RESPONSE_ACCEPT ), ( gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL ), ( gtk.STOCK_SAVE, gtk.RESPONSE_OK ) )
		)


	def run(self):
		"Displays the dialog"

		response = Warning.run(self)

		if response == gtk.RESPONSE_OK:	
			return True

		elif response == gtk.RESPONSE_ACCEPT:
			return False

		elif response in ( gtk.RESPONSE_CANCEL, gtk.RESPONSE_CLOSE ):
			raise CancelError



class FileChangesNew(FileChanges):
	"Asks the user to save changes when creating a new file"

	def __init__(self, parent):
		FileChanges.__init__(
			self, parent, _('Save changes to current file?'),
			_('You have made changes which have not been saved. If you create a new file without saving then these changes will be lost.')
		)



class FileChangesOpen(FileChanges):
	"Asks the user to save changes when opening a different file"

	def __init__(self, parent):
		FileChanges.__init__(
			self, parent, _('Save changes before opening?'),
			_('You have made changes which have not been saved. If you open a different file without saving then these changes will be lost.')
		)



class FileChangesQuit(FileChanges):
	"Asks the user to save changes when quitting"

	def __init__(self, parent):
		FileChanges.__init__(
			self, parent, _('Save changes before quitting?'),
			_('You have made changes which have not been saved. If you quit without saving, then these changes will be lost.')
		)



class FileReplace(Warning):
	"Asks for confirmation when replacing a file"

	def __init__(self, parent, file):
		Warning.__init__(
			self, parent, _('Replace existing file?'),
			_('The file \'%s\' already exists - do you wish to replace this file?') % file,
			( ( gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL ), ( stock.STOCK_REPLACE, gtk.RESPONSE_OK ) ),
			gtk.RESPONSE_CANCEL
		)


	def run(self):
		"Displays the dialog"

		if Warning.run(self) == gtk.RESPONSE_OK:
			return True

		else:
			raise CancelError



class FileSaveInsecure(Warning):
	"Asks for confirmation when exporting to insecure file"

	def __init__(self, parent):
		Warning.__init__(
			self, parent, _('Save to insecure file?'),
			_('You have chosen to save your passwords to an insecure (unencrypted) file format - if anyone has access to this file, they will be able to see your passwords.'),
			( ( gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL ), ( gtk.STOCK_SAVE, gtk.RESPONSE_OK ) ), 0
		)


	def run(self):
		"Runs the dialog"

		if Warning.run(self) == gtk.RESPONSE_OK:
			return True

		else:
			raise CancelError



##### FILE SELECTION DIALOGS #####

class FileSelector(FileChooserDialog):
	"A normal file selector"

	def __init__(self, parent, title = None, action = gtk.FILE_CHOOSER_ACTION_OPEN, stockbutton = None):
		if stockbutton is None:
			if action == gtk.FILE_CHOOSER_ACTION_OPEN:
				stockbutton = gtk.STOCK_OPEN

			elif action == gtk.FILE_CHOOSER_ACTION_SAVE:
				stockbutton = gtk.STOCK_SAVE

		FileChooserDialog.__init__(
			self, title, parent, action,
			( gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, stockbutton, gtk.RESPONSE_OK )
		)

		self.set_default_response(gtk.RESPONSE_OK)


	def run(self):
		"Displays and runs the file selector, returns the filename"

		response = FileChooserDialog.run(self)
		filename = self.get_path()
		self.destroy()

		if response == gtk.RESPONSE_OK:
			return filename

		else:
			raise CancelError



class ExportFileSelector(FileSelector):
	"A file selector for exporting files"

	def __init__(self, parent):
		FileSelector.__init__(
			self, parent, _('Select File to Export to'),
			gtk.FILE_CHOOSER_ACTION_SAVE, stock.STOCK_EXPORT
		)

		# set up filetype dropdown
		self.dropdown = ui.SimpleComboBox()
		self.add_widget(self.dropdown, _('Filetype'))

		for handler in datahandler.get_export_handlers():
			self.dropdown.append_item(handler.name, None, handler)

		for index in range(self.dropdown.get_size()):
			if self.dropdown.get_item(index)[2] == datahandler.RevelationXML:
				self.dropdown.set_active(index)


	def run(self):
		"Displays the dialog"

		self.show_all()
		self.inputbox.show_all()

		if gtk.FileSelection.run(self) == gtk.RESPONSE_OK:
			filename = self.get_path()
			handler = self.dropdown.get_active_item()[2]
			self.destroy()

			return filename, handler

		else:
			self.destroy()
			raise CancelError



class ImportFileSelector(FileSelector):
	"A file selector for importing files"

	def __init__(self, parent):
		FileSelector.__init__(
			self, parent, _('Select File to Import'),
			gtk.FILE_CHOOSER_ACTION_OPEN, stock.STOCK_IMPORT
		)

		# set up filetype dropdown
		self.dropdown = ui.SimpleComboBox()
		self.add_widget(self.dropdown, _('Filetype'))

		self.dropdown.append_item(_('Automatically detect'))

		for handler in datahandler.get_import_handlers():
			self.dropdown.append_item(handler.name, None, handler)


	def run(self):
		"Displays the dialog"

		self.show_all()
		self.inputbox.show_all()

		if gtk.FileSelection.run(self) == gtk.RESPONSE_OK:
			filename = self.get_path()
			handler = self.dropdown.get_active_item()[2]
			self.destroy()

			return filename, handler

		else:
			self.destroy()
			raise CancelError



class OpenFileSelector(FileSelector):
	"A file selector for opening files"

	def __init__(self, parent):
		FileSelector.__init__(
			self, parent, _('Select File to Open'),
			gtk.FILE_CHOOSER_ACTION_OPEN, gtk.STOCK_OPEN
		)

		filter = gtk.FileFilter()
		filter.set_name(_('Revelation files'))
		filter.add_mime_type("application/x-revelation")
		self.add_filter(filter)

		filter = gtk.FileFilter()
		filter.set_name(_('All files'))
		filter.add_pattern("*")
		self.add_filter(filter)



class SaveFileSelector(FileSelector):
	"A file selector for saving files"

	def __init__(self, parent):
		FileSelector.__init__(
			self, parent, _('Select File to Save to'),
			gtk.FILE_CHOOSER_ACTION_SAVE, gtk.STOCK_SAVE
		)

		filter = gtk.FileFilter()
		filter.set_name(_('Revelation files'))
		filter.add_mime_type("application/x-revelation")
		self.add_filter(filter)

		filter = gtk.FileFilter()
		filter.set_name(_('All files'))
		filter.add_pattern("*")
		self.add_filter(filter)

		self.set_do_overwrite_confirmation(True)
		self.connect("confirm-overwrite", self.__cb_confirm_overwrite)


	def __cb_confirm_overwrite(self, widget, data = None):
		"Handles confirm-overwrite signals"

		try:
			FileReplace(self, shinygnome.util.path.normalize(self.get_uri())).run()

		except CancelError:
			return gtk.FILE_CHOOSER_CONFIRMATION_SELECT_AGAIN

		else:
			return gtk.FILE_CHOOSER_CONFIRMATION_ACCEPT_FILENAME



##### PASSWORD DIALOGS #####

class Password(Message):
	"A base dialog for asking for passwords"

	def __init__(self, parent, title, text, stock = gtk.STOCK_OK):
		Message.__init__(
			self, parent, title, text, gtk.STOCK_DIALOG_AUTHENTICATION,
			( ( gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL ), ( stock, gtk.RESPONSE_OK ))
		)

		self.entries = []

		self.inputbox_passwords = ui.InputBox()
		self.add(self.inputbox_passwords)


	def add_entry(self, name, entry = None):
		"Adds a password entry to the dialog"

		if entry == None:
			entry = ui.Entry()
			entry.set_visibility(False)

		self.inputbox_passwords.add(entry, name)
		self.entries.append(entry)

		return entry


	def run(self):
		"Displays the dialog"

		self.show_all()

		if len(self.entries) > 0:
			self.entries[0].grab_focus()

		return gtk.Dialog.run(self)



class PasswordChange(Password):
	"A dialog for changing the password"

	def __init__(self, parent, password = None):
		Password.__init__(
			self, parent, _('Enter new password'),
			_('Enter a new password for the current data file. The file must be saved before the new password is applied.'),
			stock.STOCK_PASSWORD_CHANGE
		)

		self.password = password

		if password is not None:
			self.entry_current = self.add_entry(_('Current password'))

		self.entry_new		= self.add_entry(_('New password'), ui.PasswordEntry())
		self.entry_confirm	= self.add_entry(_('Confirm password'))
		self.entry_confirm.autocheck = False


	def run(self):
		"Displays the dialog"

		while 1:
			if Password.run(self) != gtk.RESPONSE_OK:
				self.destroy()
				raise CancelError

			elif self.password is not None and self.entry_current.get_text() != self.password:
				Error(self, _('Incorrect password'), _('The password you entered as the current file password is incorrect.')).run()

			elif self.entry_new.get_text() != self.entry_confirm.get_text():
				Error(self, _('Passwords don\'t match'), _('The password and password confirmation you entered does not match.')).run()

			else:
				password = self.entry_new.get_text()

				try:
					util.check_password(password)

				except ValueError, res:
					response = Warning(
						self, _('Use insecure password?'),
						_('The password you entered is not secure; %s. Are you sure you want to use it?') % str(res).lower(),
						( ( gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL ), ( gtk.STOCK_OK, gtk.RESPONSE_OK ) ), gtk.RESPONSE_CANCEL
					).run()

					if response != gtk.RESPONSE_OK:
						continue

				self.destroy()
				return password



class PasswordLock(Password):
	"Asks for a password when the file is locked"

	def __init__(self, parent, password):
		Password.__init__(
			self, parent, _('Enter password to unlock file'),
			_('The current file has been locked, please enter the file password to unlock it.'),
			stock.STOCK_UNLOCK
		)

		self.get_response_widget(gtk.RESPONSE_CANCEL).set_label(gtk.STOCK_QUIT)

		self.password = password
		self.entry_password = self.add_entry(_('Password'))


	def run(self):
		"Displays the dialog"

		while 1:
			try:
				response = Password.run(self)

				if response == gtk.RESPONSE_CANCEL:
					raise CancelError

				elif response != gtk.RESPONSE_OK:
					continue

				elif self.entry_password.get_text() == self.password:
					break

				else:
					Error(self, _('Incorrect password'), _('The password you entered was not correct, please try again.')).run()

			except CancelError:
				if self.get_response_widget(gtk.RESPONSE_CANCEL).get_property("sensitive") == True:
					self.destroy()
					raise

				else:
					continue

		self.destroy()



class PasswordOpen(Password):
	"Password dialog for opening files"

	def __init__(self, parent, filename):
		Password.__init__(
			self, parent, _('Enter file password'),
			_('The file \'%s\' is encrypted. Please enter the file password to open it.') % filename,
			gtk.STOCK_OPEN
		)

		self.entry_password = self.add_entry(_('Password'))


	def run(self):
		"Displays the dialog"

		response = Password.run(self)
		password = self.entry_password.get_text()
		self.destroy()

		if response == gtk.RESPONSE_OK:
			return password

		else:
			raise CancelError



class PasswordSave(Password):
	"Password dialog for saving data"

	def __init__(self, parent, filename):
		Password.__init__(
			self, parent, _('Enter password for file'),
			_('Please enter a password for the file \'%s\'. You will need this password to open the file at a later time.') % filename,
			gtk.STOCK_SAVE
		)

		self.entry_new		= self.add_entry(_('New password'), ui.PasswordEntry())
		self.entry_confirm	= self.add_entry(_('Confirm password'))
		self.entry_confirm.autocheck = False


	def run(self):
		"Displays the dialog"

		while 1:
			if Password.run(self) != gtk.RESPONSE_OK:
				self.destroy()
				raise CancelError

			elif self.entry_new.get_text() != self.entry_confirm.get_text():
				Error(self, _('Passwords don\'t match'), _('The passwords you entered does not match.')).run()

			elif len(self.entry_new.get_text()) == 0:
				Error(self, _('No password entered'), _('You must enter a password for the new data file.')).run()

			else:
				password = self.entry_new.get_text()

				try:
					util.check_password(password)

				except ValueError, res:
					response = Warning(
						self, _('Use insecure password?'),
						_('The password you entered is not secure; %s. Are you sure you want to use it?') % str(res).lower(),
						( ( gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL ), ( gtk.STOCK_OK, gtk.RESPONSE_OK ) ), gtk.RESPONSE_CANCEL
					).run()

					if response != gtk.RESPONSE_OK:
						continue

				self.destroy()
				return password



##### ENTRY DIALOGS #####

class EntryEdit(Utility):
	"A dialog for editing entries"

	def __init__(self, parent, title, e = None, cfg = None, clipboard = None):
		Utility.__init__(
			self, parent, title,
			(
				( gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL ),
				( e is None and stock.STOCK_NEW_ENTRY or stock.STOCK_UPDATE, gtk.RESPONSE_OK )
			)
		)

		self.config		= cfg
		self.clipboard		= clipboard
		self.entry_field	= {}
		self.fielddata		= {}
		self.widgetdata		= {}

		# set up the ui
		self.input_meta		= self.add_inputbox(title)
		self.input_fields	= self.add_inputbox(_('Account Data'))

		self.entry_name = ui.Entry()
		self.entry_name.set_width_chars(50)
		self.tooltips.set_tip(self.entry_name, _('The name of the entry'))
		self.input_meta.add(self.entry_name, _('Name'))

		self.entry_desc = ui.Entry()
		self.tooltips.set_tip(self.entry_desc, _('A description of the entry'))
		self.input_meta.add(self.entry_desc, _('Description'))

		self.dropdown = ui.EntryDropDown()
		self.dropdown.connect("changed", lambda w: self.__setup_fieldsect(self.dropdown.get_active_type()().fields))
		eventbox = ui.EventBox(self.dropdown)
		self.tooltips.set_tip(eventbox, _('The type of entry'))
		self.input_meta.add(eventbox, _('Type'))

		# populate the dialog with data
		self.set_entry(e)


	def __setup_fieldsect(self, fields):
		"Generates a field section based on a field list"

		# store current field values
		for fieldtype, fieldentry in self.entry_field.items():
			self.fielddata[fieldtype] = fieldentry.get_text()

		self.entry_field = {}
		self.input_fields.clear()

		# generate field entries
		for field in fields:

			if self.widgetdata.has_key(type(field)):
				userdata = self.widgetdata[type(field)]

			elif field.datatype == entry.DATATYPE_PASSWORD:
				userdata = self.clipboard

			else:
				userdata = None

			fieldentry = ui.generate_field_edit_widget(field, self.config, userdata)
			self.entry_field[type(field)] = fieldentry

			if self.fielddata.has_key(type(field)):
				fieldentry.set_text(self.fielddata[type(field)])

			if (fieldentry.flags() & gtk.NO_WINDOW) != gtk.NO_WINDOW:
				self.tooltips.set_tip(fieldentry, field.description)

			elif hasattr(fieldentry, "entry") == True:
				self.tooltips.set_tip(fieldentry.entry, field.description)

			self.input_fields.add(fieldentry, field.name)


		# show widgets
		self.input_fields.show_all()


	def get_entry(self):
		"Generates an entry from the dialog contents"

		e = self.dropdown.get_active_type()()

		e.name = self.entry_name.get_text()
		e.description = self.entry_desc.get_text()

		for field in e.fields:
			field.value = self.entry_field[type(field)].get_text()

		return e


	def run(self):
		"Displays the dialog"

		while 1:
			self.show_all()

			if Utility.run(self) == gtk.RESPONSE_OK:
				e = self.get_entry()

				if e.name == "":
					Error(self, _('Name not entered'), _('You must enter a name for the account')).run()
					continue

				self.destroy()
				return e

			else:
				self.destroy()
				raise CancelError


	def set_entry(self, e):
		"Sets an entry for the dialog"

		e = e is not None and e.copy() or entry.GenericEntry()

		self.entry_name.set_text(e.name)
		self.entry_desc.set_text(e.description)
		self.dropdown.set_active_type(type(e))

		for field in e.fields:
			self.entry_field[type(field)].set_text(field.value)


	def set_fieldwidget_data(self, fieldtype, userdata):
		"Sets user data for fieldwidget"

		self.widgetdata[fieldtype] = userdata

		if fieldtype == entry.UsernameField and self.entry_field.has_key(entry.UsernameField):
			self.entry_field[entry.UsernameField].set_items(userdata)



class EntryRemove(Warning):
	"Asks for confirmation when removing entries"

	def __init__(self, parent, entries):

		if len(entries) > 1:
			title	= _('Really remove the %i selected entries?') % len(entries)
			text	= _('By removing these entries you will also remove any entries they may contain.')

		elif type(entries[0]) == entry.FolderEntry:
			title	= _('Really remove folder \'%s\'?') % entries[0].name
			text	= _('By removing this folder you will also remove all accounts and folders it contains.')

		else:
			title	= _('Really remove account \'%s\'?') % entries[0].name
			text	= _('Please confirm that you wish to remove this account.')


		Warning.__init__(
			self, parent, title, text,
			( ( gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL ), ( stock.STOCK_REMOVE, gtk.RESPONSE_OK ) ),
			0
		)


	def run(self):
		"Displays the dialog"

		if Warning.run(self) == gtk.RESPONSE_OK:
			return True

		else:
			raise CancelError



class FolderEdit(Utility):
	"Dialog for editing a folder"

	def __init__(self, parent, title, e = None):
		Utility.__init__(
			self, parent, title,
			(
				( gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL ),
				( e == None and stock.STOCK_NEW_FOLDER or stock.STOCK_UPDATE, gtk.RESPONSE_OK )
			)
		)

		# set up the ui
		self.inputbox_folder	= self.add_inputbox(title)

		self.entry_name = ui.Entry()
		self.entry_name.set_width_chars(25)
		self.tooltips.set_tip(self.entry_name, _('The name of the folder'))
		self.inputbox_folder.add(self.entry_name, _('Name'))

		self.entry_desc = ui.Entry()
		self.tooltips.set_tip(self.entry_desc, _('A description of the folder'))
		self.inputbox_folder.add(self.entry_desc, _('Description'))

		# populate the dialog with data
		self.set_entry(e)


	def get_entry(self):
		"Generates an entry from the dialog contents"

		e = entry.FolderEntry()
		e.name = self.entry_name.get_text()
		e.description = self.entry_desc.get_text()

		return e


	def run(self):
		"Displays the dialog"

		while 1:
			self.show_all()

			if Utility.run(self) == gtk.RESPONSE_OK:
				e = self.get_entry()

				if e.name == "":
					Error(self, _('Name not entered'), _('You must enter a name for the folder')).run()
					continue

				self.destroy()
				return e

			else:
				self.destroy()
				raise CancelError


	def set_entry(self, e):
		"Sets an entry for the dialog"

		if e is None:
			return

		self.entry_name.set_text(e.name)
		self.entry_desc.set_text(e.description)



##### MISCELLANEOUS DIALOGS #####

class About(shinygnome.ui.AboutDialog):
	"About dialog"

	def __init__(self, parent):
		shinygnome.ui.AboutDialog.__init__(self, parent)

		self.set_name(config.APPNAME)
		self.set_version(config.VERSION)
		self.set_copyright(config.COPYRIGHT)
		self.set_comments(('"%s"\n\n' + _('A password manager for the GNOME desktop')) % config.RELNAME)
		self.set_license(config.LICENSE)
		self.set_website(config.URL)
		self.set_authors(config.AUTHORS)
		self.set_artists(config.ARTISTS)
		self.set_logo(parent.render_icon(stock.STOCK_REVELATION, gtk.ICON_SIZE_DIALOG))



class Exception(Error):
	"Displays a traceback for an unhandled exception"

	def __init__(self, parent, traceback):
		Error.__init__(
			self, parent, _('Unknown error'),
			_('An unknown error occured. Please report the text below to the Revelation developers, along with what you were doing that may have caused the error. You may attempt to continue running Revelation, but it may behave unexpectedly.'),
			( ( gtk.STOCK_QUIT, gtk.RESPONSE_CANCEL ), ( stock.STOCK_CONTINUE, gtk.RESPONSE_OK ) )
		)

		textview = ui.TextView(None, traceback)
		scrolledwindow = ui.ScrolledWindow(textview)
		scrolledwindow.set_size_request(-1, 120)

		self.add(scrolledwindow)


	def run(self):
		"Runs the dialog"

		return Error.run(self) == gtk.RESPONSE_OK



class PasswordChecker(Utility):
	"A password checker dialog"

	def __init__(self, parent, cfg = None, clipboard = None):
		Utility.__init__(
			self, parent, _('Password Checker'),
			( ( gtk.STOCK_CLOSE, gtk.RESPONSE_CLOSE ), )
		)

		self.cfg = cfg
		self.set_modal(False)
		self.set_size_request(300, -1)

		self.inputbox = self.add_inputbox(_('Password Checker'))

		self.entry = ui.PasswordEntry(None, cfg, clipboard)
		self.entry.autocheck = False
		self.entry.set_width_chars(40)
		self.entry.connect("changed", self.__cb_changed)
		self.tooltips.set_tip(self.entry, _('Enter a password to check'))
		self.inputbox.add(self.entry, _('Password'))

		self.result = ui.ImageLabel(_('Enter a password to check'), stock.STOCK_UNKNOWN, ui.ICON_SIZE_HEADLINE)
		self.tooltips.set_tip(self.result, _('The result of the check'))
		self.inputbox.add(self.result)

		self.connect("response", self.__cb_response)


	def __cb_changed(self, widget, data = None):
		"Callback for entry changes"

		password = self.entry.get_text()

		try:
			if len(password) == 0:
				icon	= stock.STOCK_UNKNOWN
				result	= _('Enter a password to check')

			else:
				util.check_password(password)
				icon	= stock.STOCK_PASSWORD_STRONG
				result	= _('The password seems good')

		except ValueError, result:
			icon	= stock.STOCK_PASSWORD_WEAK
			result = _('The password %s') % str(result)

		self.result.set_text(result)
		self.result.set_stock(icon, ui.ICON_SIZE_HEADLINE)


	def __cb_response(self, widget, response):
		"Callback for response"

		self.destroy()


	def run(self):
		"Displays the dialog"

		self.show_all()

		if EVENT_FILTER != None:
			self.window.add_filter(EVENT_FILTER)

		# for some reason, gtk crashes on close-by-escape
		# if we don't do this
		self.get_response_widget(gtk.RESPONSE_CLOSE).grab_focus()
		self.entry.grab_focus()



class PasswordGenerator(Utility):
	"A password generator dialog"

	def __init__(self, parent, cfg, clipboard = None):
		Utility.__init__(
			self, parent, _('Password Generator'),
			( ( gtk.STOCK_CLOSE, gtk.RESPONSE_CLOSE ), ( stock.STOCK_GENERATE, gtk.RESPONSE_OK ) )
		)

		self.config = cfg
		self.set_modal(False)

		self.inputbox = self.add_inputbox(_('Password Generator'))

		self.entry = ui.PasswordEntry(None, cfg, clipboard)
		self.entry.autocheck = False
		self.entry.set_editable(False)
		self.tooltips.set_tip(self.entry, _('The generated password'))
		self.inputbox.add(self.entry, _('Password'))

		self.spin_pwlen = ui.SpinButton()
		self.spin_pwlen.set_range(4, 256)
		self.spin_pwlen.set_value(self.config.get("passwordgen/length"))
		self.tooltips.set_tip(self.spin_pwlen, ('The number of characters in generated passwords - 8 or more are recommended'))
		self.inputbox.add(self.spin_pwlen, _('Length'))

		self.connect("response", self.__cb_response)


	def __cb_response(self, widget, response):
		"Callback for dialog responses"

		if response == gtk.RESPONSE_OK:
			self.entry.set_text(util.generate_password(self.spin_pwlen.get_value()))

		else:
			self.destroy()


	def run(self):
		"Displays the dialog"

		self.show_all()
		self.get_response_widget(gtk.RESPONSE_CLOSE).grab_focus()

		if EVENT_FILTER != None:
			self.window.add_filter(EVENT_FILTER)



##### FUNCTIONS #####

def create_unique(dialog, *args):
	"Creates a unique dialog"

	if present_unique(dialog) == True:
		return get_unique(dialog)

	else:
		UNIQUE_DIALOGS[dialog] = dialog(*args)
		UNIQUE_DIALOGS[dialog].connect("destroy", lambda w: remove_unique(dialog))

		return UNIQUE_DIALOGS[dialog]


def get_unique(dialog):
	"Returns a unique dialog"

	if unique_exists(dialog) == True:
		return UNIQUE_DIALOGS[dialog]

	else:
		return None


def present_unique(dialog):
	"Presents a unique dialog, if it exists"

	if unique_exists(dialog) == True:
		get_unique(dialog).present()

		return True

	else:
		return False


def remove_unique(dialog):
	"Removes a unique dialog"

	if unique_exists(dialog):
		UNIQUE_DIALOGS[dialog] = None


def run_unique(dialog, *args):
	"Runs a unique dialog"

	if present_unique(dialog) == True:
		return None

	else:
		d = create_unique(dialog, *args)

		return d.run()


def unique_exists(dialog):
	"Checks if a unique dialog exists"

	return UNIQUE_DIALOGS.has_key(dialog) == True and UNIQUE_DIALOGS[dialog] != None

