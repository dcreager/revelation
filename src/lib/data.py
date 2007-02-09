#
# Revelation - a password manager for GNOME 2
# http://oss.codepoet.no/revelation/
# $Id$
#
# Module containing data-related functionality
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

import datahandler, entry, shinygnome.ui

import gobject, gtk, gtk.gdk, time



COLUMN_NAME	= 0
COLUMN_ICON	= 1
COLUMN_ENTRY	= 2

SEARCH_NEXT	= "next"
SEARCH_PREVIOUS	= "prev"


Timer		= shinygnome.ui.Timer
UndoQueue	= shinygnome.ui.UndoQueue



class Clipboard(gobject.GObject):
	"A normal text-clipboard"

	def __init__(self):
		gobject.GObject.__init__(self)

		self.clip_clipboard	= gtk.clipboard_get("CLIPBOARD")
		self.clip_primary	= gtk.clipboard_get("PRIMARY")

		self.cleartimer		= Timer(10)
		self.cleartimeout	= 60
		self.cleartimer.connect("ring", self.__cb_clear_ring)

		self.content		= None
		self.contentpointer	= 0


	def __cb_clear(self, clipboard, data = None):
		"Clears the clipboard data"

		return


	def __cb_clear_ring(self, widget):
		"Handles cleartimer rings"

		self.content		= None
		self.contentpointer	= 0


	def __cb_get(self, clipboard, selectiondata, info, data):
		"Returns text for clipboard requests"

		if self.content == None:
			text = ""

		elif type(self.content) == list:

			if len(self.content) == 0:
				text = ""

			else:
				text = self.content[self.contentpointer]

			if self.contentpointer < len(self.content) - 1:
				self.contentpointer += 1

		else:
			text = str(self.content)

		selectiondata.set_text(text, len(text))


	def clear(self):
		"Clears the clipboard"

		self.clip_clipboard.clear()
		self.clip_primary.clear()


	def get(self):
		"Fetches text from the clipboard"

		text = self.clip_clipboard.wait_for_text()

		if text is None:
			text = ""

		return text


	def has_contents(self):
		"Checks if the clipboard has any contents"

		return self.clip_clipboard.wait_is_text_available()


	def set(self, content, secret = False):
		"Copies text to the clipboard"

		self.content		= content
		self.contentpointer	= 0

		targets = (
			( "text/plain",		0,	0 ),
			( "STRING",		0,	0 ),
			( "TEXT",		0,	0 ),
			( "COMPOUND_TEXT",	0,	0 ),
			( "UTF8_STRING",	0,	0 )
		)

		self.clip_clipboard.set_with_data(targets, self.__cb_get, self.__cb_clear, None)
		self.clip_primary.set_with_data(targets, self.__cb_get, self.__cb_clear, None)

		if secret == True:
			self.cleartimer.start(self.cleartimeout)

		else:
			self.cleartimer.stop()



class EntryClipboard(gobject.GObject):
	"A clipboard for entries"

	def __init__(self):
		gobject.GObject.__init__(self)

		self.clipboard = gtk.Clipboard(gtk.gdk.display_get_default(), "_REVELATION_ENTRY")
		self.__has_contents = False

		gobject.timeout_add(500, lambda: self.__check_contents())


	def __check_contents(self):
		"Callback which check the clipboard"

		state = self.has_contents()

		if state != self.__has_contents:
			self.emit("content-toggled", state)
			self.__has_contents = state

		return True


	def clear(self):
		"Clears the clipboard"

		self.clipboard.clear()
		self.__check_contents()


	def get(self):
		"Fetches entries from the clipboard"

		try:
			xml = self.clipboard.wait_for_text()

			if xml in ( None, "" ):
				return None

			handler = datahandler.RevelationXML()
			entrystore = handler.import_data(xml)

			return entrystore

		except datahandler.HandlerError:
			return None


	def has_contents(self):
		"Checks if the clipboard has any contents"

		return self.clipboard.wait_for_text() is not None


	def set(self, entrystore, iters):
		"Copies entries from an entrystore to the clipboard"

		copystore = EntryStore()

		for iter in entrystore.filter_parents(iters):
			copystore.import_entry(entrystore, iter)

		xml = datahandler.RevelationXML().export_data(copystore)
		self.clipboard.set_text(xml)

		self.__check_contents()


gobject.signal_new("content-toggled", EntryClipboard, gobject.SIGNAL_ACTION, gobject.TYPE_BOOLEAN, ( gobject.TYPE_BOOLEAN, ))



class EntrySearch(gobject.GObject):
	"Handles searching in an EntryStore"

	def __init__(self, entrystore):
		gobject.GObject.__init__(self)
		self.entrystore	= entrystore

		self.folders		= True
		self.namedesconly	= False
		self.casesensitive	= False


	def find(self, string, entrytype = None, offset = None, direction = SEARCH_NEXT):
		"Searches for an entry, starting at the given offset"

		iter = offset

		while 1:

			if direction == SEARCH_NEXT:
				iter = self.entrystore.iter_traverse_next(iter)

			else:
				iter = self.entrystore.iter_traverse_prev(iter)

			# if we've wrapped around, return None
			if self.entrystore.get_path(iter) == self.entrystore.get_path(offset):
				return None

			if self.match(iter, string, entrytype) == True:
				return iter


	def find_all(self, string, entrytype = None):
		"Searches for all entries matching a term"

		matches = []
		iter = self.entrystore.iter_children(None)

		while iter != None:

			if self.match(iter, string, entrytype) == True:
				matches.append(iter)

			iter = self.entrystore.iter_traverse_next(iter)

		return matches


	def match(self, iter, string, entrytype = None):
		"Check if an entry matches the search criteria"

		if iter is None:
			return False

		e = self.entrystore.get_entry(iter)


		# check entry type
		if type(e) == entry.FolderEntry and self.folders == False:
			return False

		if entrytype is not None and type(e) not in ( entrytype, entry.FolderEntry ):
			return False


		# check entry fields
		items = [ e.name, e.description ]

		if self.namedesconly == False:
			items.extend([ field.value for field in e.fields if field.value != "" ])


		# run the search
		for item in items:
			if self.casesensitive == True and string in item:
				return True

			elif self.casesensitive == False and string.decode("utf-8").lower() in item.decode("utf-8").lower():
				return True

		return False



class EntryStore(shinygnome.ui.TreeStore):
	"A data structure for storing entries"

	def __init__(self):
		shinygnome.ui.TreeStore.__init__(
			self,
			gobject.TYPE_STRING,	# name
			gobject.TYPE_STRING,	# icon
			gobject.TYPE_PYOBJECT	# entry
		)

		self.connect("row-has-child-toggled", self.__cb_iter_has_child)


	def __cb_iter_has_child(self, widget, path, iter):
		"Callback for iters having children"

		if self.iter_n_children(iter) == 0:
			self.folder_expanded(iter, False)


	def add_entry(self, e, parent = None, sibling = None):
		"Adds an entry"

		# place after parent if it's not a folder
		if parent is not None and type(self.get_entry(parent)) != entry.FolderEntry:
			iter = self.insert_after(self.iter_parent(parent), parent)

		# place before sibling, if given
		elif sibling is not None:
			iter = self.insert_before(parent, sibling)

		# otherwise, append to parent
		else:
			iter = self.append(parent)

		self.update_entry(iter, e)

		return iter


	def copy_entry(self, iter, parent = None, sibling = None):
		"Copies an entry recursively"

		newiter = self.add_entry(self.get_entry(iter), parent, sibling)

		for i in range(self.iter_n_children(iter)):
			child = self.iter_nth_child(iter, i)
			self.copy_entry(child, newiter)

		return newiter


	def filter_parents(self, iters):
		"Removes all descendants from the list of iters"

		parents = []

		for child in iters:
			for parent in iters:
				if self.is_ancestor(parent, child):
					break

			else:
				parents.append(child)

		return parents


	def folder_expanded(self, iter, expanded):
		"Sets the expanded state of an entry"

		e = self.get_entry(iter)

		if e == None or type(e) != entry.FolderEntry:
			return

		elif expanded == True:
			self.set_value(iter, COLUMN_ICON, e.openicon)

		else:
			self.set_value(iter, COLUMN_ICON, e.icon)


	def get_entry(self, iter):
		"Fetches data for an entry"

		if iter is None:
			return None

		e = self.get_value(iter, COLUMN_ENTRY)

		if e is None:
			return None

		else:
			return e.copy()


	def get_popular_values(self, fieldtype, threshold = 3):
		"Gets popular values for a field type"

		valuecount = {}
		iter = self.iter_nth_child(None, 0)

		while iter is not None:
			e = self.get_entry(iter)

			if e.has_field(fieldtype) == False:
				iter = self.iter_traverse_next(iter)
				continue

			value = e[fieldtype].strip()

			if value != "":
				if valuecount.has_key(value) == False:
					valuecount[value] = 0

				valuecount[value] += 1

			iter = self.iter_traverse_next(iter)

		popular = [ value for value, count in valuecount.items() if count >= threshold ]
		popular.sort()

		return popular


	def import_entry(self, source, iter, parent = None, sibling = None):
		"Recursively copies an entry from a different entrystore"

		if iter is not None:
			copy = self.add_entry(source.get_entry(iter), parent, sibling)
			parent, sibling = copy, None

		else:
			copy = None

		newiters = []
		for i in range(source.iter_n_children(iter)):
			child = source.iter_nth_child(iter, i)
			newiter = self.import_entry(source, child, parent, sibling)
			newiters.append(newiter)

		return copy is not None and copy or newiters


	def move_entry(self, iter, parent = None, sibling = None):
		"Moves an entry"

		newiter = self.copy_entry(iter, parent, sibling)
		self.remove_entry(iter)

		return newiter


	def remove_entry(self, iter):
		"Removes an entry, and its children if any"

		self.remove(iter)


	def update_entry(self, iter, e):
		"Updates an entry"

		if None in ( iter, e):
			return None

		self.set_value(iter, COLUMN_NAME, e.name)
		self.set_value(iter, COLUMN_ICON, e.icon)
		self.set_value(iter, COLUMN_ENTRY, e.copy())

