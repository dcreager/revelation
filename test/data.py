#!/usr/bin/env python

#
# Revelation 0.3.3 - a password manager for GNOME 2
# http://oss.codepoet.no/revelation/
# $Id: datahandler.py 168 2004-10-22 18:17:27Z erikg $
#
# Unit tests for data module
#
#
# Copyright (c) 2003-2004 Erik Grinaker
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

import gobject, unittest

from revelation import data, entry



class EntrySearch__init(unittest.TestCase):
	"EntrySearch.__init__()"

	def test_attrs(self):
		"EntrySearch.__init__() sets required attributes"

		entrysearch = data.EntrySearch(data.EntryStore())
		self.assertEquals(hasattr(entrysearch, "folders"), True)


	def test_defaults(self):
		"EntrySearch.__init__() sets proper defaults"

		entrysearch = data.EntrySearch(data.EntryStore())
		self.assertEquals(entrysearch.folders, True)
		self.assertEquals(entrysearch.namedesconly, False)
		self.assertEquals(entrysearch.casesensitive, False)



class EntrySearch_find(unittest.TestCase):
	"EntrySearch.find()"


	def setUp(self):
		"Sets up an entrystore for testing"

		self.entrystore = data.EntryStore()
		self.entrysearch = data.EntrySearch(self.entrystore)

		e = entry.GenericEntry()
		e.name = "entry0"
		self.entrystore.add_entry(e)

		e = entry.FolderEntry()
		e.name = "folder0"
		parent = self.entrystore.add_entry(e)

		e = entry.GenericEntry()
		e.name = "entry1"
		self.entrystore.add_entry(e, parent)

		e = entry.GenericEntry()
		e.name = "entry2"
		self.entrystore.add_entry(e)


	def test_direction(self):
		"EntrySearch.find() uses direction correctly"

		iter = self.entrysearch.find("entry")
		self.assertEquals(self.entrystore.get_path(iter), (0, ))

		iter = self.entrysearch.find("entry", None, None, data.SEARCH_PREV)
		self.assertEquals(self.entrystore.get_path(iter), (2, ))


	def test_find(self):
		"EntrySearch.find() returns correct entry"

		iter = self.entrysearch.find("entry1")
		self.assertEquals(self.entrystore.get_path(iter), (1, 0))


	def test_nomatch(self):
		"EntrySearch.find() returns None on no match"

		iter = self.entrysearch.find("test123")
		self.assertEquals(iter, None)


	def test_offset(self):
		"EntrySearch.find() finds next match after offset"

		offset = self.entrystore.get_iter((1, 0))
		iter = self.entrysearch.find("entry", None, offset)

		self.assertEquals(self.entrystore.get_path(iter), (2, ))


	def test_offset_wrap(self):
		"EntrySearch.find() wraps around"

		offset = self.entrystore.get_iter((2, ))
		iter = self.entrysearch.find("entry", None, offset)

		self.assertEquals(self.entrystore.get_path(iter), (0, ))

	def test_offset_nomatch(self):
		"EntrySearch.find() returns None if no match other than offset"

		offset = self.entrystore.get_iter((1, ))
		iter = self.entrysearch.find("folder", None, offset)

		self.assertEquals(iter, None)



class EntrySearch_match(unittest.TestCase):
	"EntrySearch.match()"

	def setUp(self):
		"Sets up an entrystore and entrysearch for testing"

		self.entrystore = data.EntryStore()
		self.entrysearch = data.EntrySearch(self.entrystore)

		e = entry.GenericEntry()
		e.name = "name"
		e.description = "description"
		e[entry.HostnameField] = "hostname"
		e[entry.UsernameField] = "username"
		e[entry.PasswordField] = "password"

		self.iter = self.entrystore.add_entry(e)

		e = entry.FolderEntry()
		e.name = "folder"
		self.folderiter = self.entrystore.add_entry(e)


	def test_blank(self):
		"EntrySearch.match() matches on blank string"

		self.assertEquals(self.entrysearch.match(self.iter, ""), True)


	def test_casesensitive(self):
		"EntrySearch.match() uses casesensitive attribute correctly"

		self.entrysearch.casesensitive = True
		self.assertEquals(self.entrysearch.match(self.iter, "NamE"), False)

		self.entrysearch.casesensitive = False
		self.assertEquals(self.entrysearch.match(self.iter, "NamE"), True)


	def test_folder(self):
		"EntrySearch.match() uses folders attribute correctly"

		self.entrysearch.folders = False
		self.assertEquals(self.entrysearch.match(self.folderiter, ""), False)

		self.entrysearch.folders = True
		self.assertEquals(self.entrysearch.match(self.folderiter, ""), True)


	def test_namedesconly(self):
		"EntrySearch.match() uses namedesconly attribute correctly"

		self.entrysearch.namedesconly = True
		self.assertEquals(self.entrysearch.match(self.iter, "username"), False)

		self.entrysearch.namedesconly = False
		self.assertEquals(self.entrysearch.match(self.iter, "username"), True)


	def test_none(self):
		"EntrySearch.match() returns False on None"

		self.assertEquals(self.entrysearch.match(None, "test"), False)


	def test_string(self):
		"EntrySearch.match() matches on string"

		self.assertEquals(self.entrysearch.match(self.iter, "test"), False)
		self.assertEquals(self.entrysearch.match(self.iter, "name"), True)
		self.assertEquals(self.entrysearch.match(self.iter, "ript"), True)


	def test_type(self):
		"EntrySearch.match() matches on entry type"

		self.assertEquals(self.entrysearch.match(self.iter, "name", entry.GenericEntry), True)
		self.assertEquals(self.entrysearch.match(self.iter, "name", entry.WebEntry), False)



class EntryStore__init(unittest.TestCase):
	"EntryStore.__init__()"

	def test_changed(self):
		"EntryStore.__init__() sets .changed to False"

		e = data.EntryStore()
		self.assertEquals(e.changed, False)


	def test_columns(self):
		"EntryStore.__init__() sets up correct columns"

		e = data.EntryStore()

		self.assertEquals(e.get_n_columns(), 3)
		self.assertEquals(e.get_column_type(0), gobject.TYPE_STRING)
		self.assertEquals(e.get_column_type(1), gobject.TYPE_STRING)
		self.assertEquals(e.get_column_type(2), gobject.TYPE_PYOBJECT)



class EntryStore_add_entry(unittest.TestCase):
	"EntryStore.add_entry()"

	def test_add(self):
		"EntryStore.add_entry() adds an iter"

		entrystore = data.EntryStore()
		e = entry.GenericEntry()

		entrystore.add_entry(e)

		self.assertEquals(entrystore.iter_n_children(None), 1)


	def test_changed(self):
		"EntryStore.add_entry() sets .changed to True"

		entrystore = data.EntryStore()
		e = entry.GenericEntry()

		self.assertEquals(entrystore.changed, False)
		entrystore.add_entry(e)
		self.assertEquals(entrystore.changed, True)


	def test_copy(self):
		"EntryStore.add_entry() stores a copy of the entry"

		entrystore = data.EntryStore()

		e = entry.GenericEntry()
		e.name = "test123"

		iter = entrystore.add_entry(e)

		e.name = "changed"

		self.assertEquals(entrystore.get_value(iter, 2).name, "test123")


	def test_data(self):
		"EntryStore.add_entry() stores all data"

		entrystore = data.EntryStore()

		e = entry.GenericEntry()
		e.name = "name"
		e.description = "description"
		e.updated = 1
		e.get_field(entry.HostnameField).value = "hostname"
		e.get_field(entry.UsernameField).value = "username"
		e.get_field(entry.PasswordField).value = "password"

		iter = entrystore.add_entry(e)

		self.assertEquals(entrystore.get_value(iter, 0), "name")
		self.assertEquals(entrystore.get_value(iter, 1), e.icon)

		ce = entrystore.get_value(iter, 2)
		self.assertEquals(e.name, ce.name)
		self.assertEquals(e.description, ce.description)
		self.assertEquals(e.updated, ce.updated)
		self.assertEquals(e[entry.HostnameField], ce[entry.HostnameField])
		self.assertEquals(e[entry.UsernameField], ce[entry.UsernameField])
		self.assertEquals(e[entry.PasswordField], ce[entry.PasswordField])


	def test_parent(self):
		"EntryStore.add_entry() adds below parent folder"

		entrystore = data.EntryStore()
		parent = entrystore.add_entry(entry.FolderEntry())
		iter = entrystore.add_entry(entry.GenericEntry(), parent)

		self.assertNotEquals(parent, None)
		self.assertEquals(entrystore.iter_n_children(None), 1)
		self.assertEquals(entrystore.iter_n_children(parent), 1)


	def test_parent_notfolder(self):
		"EntryStore.add_entry() appends to root if parent is not folder"

		entrystore = data.EntryStore()
		parent = entrystore.add_entry(entry.GenericEntry())
		iter = entrystore.add_entry(entry.GenericEntry(), parent)

		self.assertNotEquals(parent, None)
		self.assertEquals(entrystore.iter_n_children(None), 2)
		self.assertEquals(entrystore.iter_n_children(parent), 0)


	def test_sibling(self):
		"EntryStore.add_entry() adds before sibling"

		entrystore = data.EntryStore()

		p = entry.FolderEntry()
		p.name = "folder"
		parent = entrystore.add_entry(p)

		s = entry.GenericEntry()
		s.name = "sibling"
		sibling = entrystore.add_entry(s, parent)

		e = entry.GenericEntry()
		e.name = "test123"
		entrystore.add_entry(e, parent, sibling)

		self.assertEquals(entrystore.get_entry(entrystore.iter_nth_child(parent, 0)).name, "test123")
		self.assertEquals(entrystore.get_entry(entrystore.iter_nth_child(parent, 1)).name, "sibling")



class EntryStore_clear(unittest.TestCase):
	"EntryStore.clear()"

	def test_changed(self):
		"EntryStore.clear() sets .changed to False"

		entrystore = data.EntryStore()
		entrystore.add_entry(entry.GenericEntry())
		entrystore.add_entry(entry.GenericEntry())

		self.assertEquals(entrystore.changed, True)
		entrystore.clear()
		self.assertEquals(entrystore.changed, False)


	def test_clear(self):
		"EntryStore.clear() removes all entries"

		entrystore = data.EntryStore()
		entrystore.add_entry(entry.GenericEntry())
		entrystore.add_entry(entry.GenericEntry())

		self.assertEquals(entrystore.iter_n_children(None), 2)
		entrystore.clear()
		self.assertEquals(entrystore.iter_n_children(None), 0)



class EntryStore_get_entry(unittest.TestCase):
	"EntryStore.get_entry()"

	def test_copy(self):
		"EntryStore.get_entry() returns a copy of the entry"

		entrystore = data.EntryStore()

		e = entry.GenericEntry()
		e.name = "test123"
		iter = entrystore.add_entry(e)

		e = entrystore.get_entry(iter)
		e.name = "changed"

		self.assertEquals(entrystore.get_entry(iter).name, "test123")


	def test_data(self):
		"EntryStore.get_entry() returns all entry data"

		entrystore = data.EntryStore()

		e = entry.GenericEntry()
		e.name = "name"
		e.description = "description"
		e.updated = 1
		e.get_field(entry.HostnameField).value = "hostname"
		e.get_field(entry.UsernameField).value = "username"
		e.get_field(entry.PasswordField).value = "password"

		iter = entrystore.add_entry(e)

		ce = entrystore.get_entry(iter)
		self.assertEquals(e.name, ce.name)
		self.assertEquals(e.description, ce.description)
		self.assertEquals(e.updated, ce.updated)
		self.assertEquals(e[entry.HostnameField], ce[entry.HostnameField])
		self.assertEquals(e[entry.UsernameField], ce[entry.UsernameField])
		self.assertEquals(e[entry.PasswordField], ce[entry.PasswordField])


	def test_none(self):
		"EntryStore.get_entry() returns None on no iter"

		entrystore = data.EntryStore()
		self.assertEquals(entrystore.get_entry(None), None)



class EntryStore_get_iter(unittest.TestCase):
	"EntryStore.get_iter()"

	def test_inv(self):
		"EntryStore.get_iter() returns None on invalid path"

		self.assertEquals(data.EntryStore().get_iter((0,)), None)


	def test_iter(self):
		"EntryStore.get_iter() returns iter"

		entrystore = data.EntryStore()

		e = entry.GenericEntry()
		e.name = "test123"

		entrystore.add_entry(e)
		iter = entrystore.get_iter((0,))

		self.assertEquals(e.name, entrystore.get_entry(iter).name)


	def test_none(self):
		"EntryStore.get_iter() handles None and variations"

		entrystore = data.EntryStore()
		self.assertEquals(entrystore.get_iter(None), None)
		self.assertEquals(entrystore.get_iter(""), None)
		self.assertEquals(entrystore.get_iter(()), None)
		self.assertEquals(entrystore.get_iter([]), None)



class EntryStore_get_path(unittest.TestCase):
	"EntryStore.get_path()"

	def test_none(self):
		"EntryStore.get_path() handles None"

		self.assertEquals(data.EntryStore().get_path(None), None)


	def test_path(self):
		"EntryStore.get_path() returns a path"

		entrystore = data.EntryStore()
		parent = entrystore.add_entry(entry.FolderEntry())
		entrystore.add_entry(entry.GenericEntry(), parent)
		iter = entrystore.add_entry(entry.GenericEntry(), parent)

		self.assertEquals(entrystore.get_path(iter), (0, 1))



class EntryStore_iter_traverse_prev(unittest.TestCase):
	"EntryStore.iter_traverse_prev()"

	def setUp(self):
		"Set up the entrystore"

		self.entrystore = data.EntryStore()

		e = entry.GenericEntry()
		e.name = "entry0"
		self.entrystore.add_entry(e)

		e = entry.FolderEntry()
		e.name = "folder0"
		parent = self.entrystore.add_entry(e)

		e = entry.GenericEntry()
		e.name = "entry1"
		self.entrystore.add_entry(e, parent)

		e = entry.GenericEntry()
		e.name = "entry2"
		self.entrystore.add_entry(e, parent)

		e = entry.FolderEntry()
		e.name = "folder1"
		parent2 = self.entrystore.add_entry(e, parent)

		e = entry.GenericEntry()
		e.name = "entry3"
		self.entrystore.add_entry(e, parent2)

		e = entry.GenericEntry()
		e.name = "entry4"
		self.entrystore.add_entry(e, parent)

		e = entry.GenericEntry()
		e.name = "entry5"
		self.entrystore.add_entry(e)
	
		e = entry.FolderEntry()
		e.name = "folder2"
		parent = self.entrystore.add_entry(e)

		e = entry.GenericEntry()
		e.name = "entry6"
		self.entrystore.add_entry(e, parent)


	def test_none(self):
		"EntryStore.iter_traverse_prev() returns last node on None"

		iter = self.entrystore.iter_traverse_prev(None)
		self.assertEquals(self.entrystore.get_entry(iter).name, "entry6")


	def test_traverse(self):
		"EntryStore.iter_traverse_prev() uses correct traversal"

		order = (
			"entry6",
			"folder2",
			"entry5",
			"entry4",
			"entry3",
			"folder1",
			"entry2",
			"entry1",
			"folder0",
			"entry0"
		)

		iter = None

		for name in order:
			iter = self.entrystore.iter_traverse_prev(iter)
			self.assertEquals(self.entrystore.get_entry(iter).name, name)



class EntryStore_iter_traverse_next(unittest.TestCase):
	"EntryStore.iter_traverse_next()"

	def setUp(self):
		"Set up the entrystore"

		self.entrystore = data.EntryStore()

		e = entry.GenericEntry()
		e.name = "entry0"
		self.entrystore.add_entry(e)

		e = entry.FolderEntry()
		e.name = "folder0"
		parent = self.entrystore.add_entry(e)

		e = entry.GenericEntry()
		e.name = "entry1"
		self.entrystore.add_entry(e, parent)

		e = entry.GenericEntry()
		e.name = "entry2"
		self.entrystore.add_entry(e, parent)

		e = entry.FolderEntry()
		e.name = "folder1"
		parent2 = self.entrystore.add_entry(e, parent)

		e = entry.GenericEntry()
		e.name = "entry3"
		self.entrystore.add_entry(e, parent2)

		e = entry.GenericEntry()
		e.name = "entry4"
		self.entrystore.add_entry(e, parent)

		e = entry.GenericEntry()
		e.name = "entry5"
		self.entrystore.add_entry(e)
	
		e = entry.FolderEntry()
		e.name = "folder2"
		parent = self.entrystore.add_entry(e)

		e = entry.GenericEntry()
		e.name = "entry6"
		self.entrystore.add_entry(e, parent)


	def test_none(self):
		"EntryStore.iter_traverse_next() returns first node on None"

		iter = self.entrystore.iter_traverse_next(None)
		self.assertEquals(self.entrystore.get_entry(iter).name, "entry0")


	def test_traverse(self):
		"EntryStore.iter_traverse_next() uses correct traversal"

		order = (
			"entry0",
			"folder0",
			"entry1",
			"entry2",
			"folder1",
			"entry3",
			"entry4",
			"entry5",
			"folder2",
			"entry6"
		)

		iter = None

		for name in order:
			iter = self.entrystore.iter_traverse_next(iter)
			self.assertEquals(self.entrystore.get_entry(iter).name, name)



class EntryStore_remove_entry(unittest.TestCase):
	"EntryStore.remove_entry()"

	def test_none(self):
		"EntryStore.remove_entry() handles None"

		data.EntryStore().remove_entry(None)


	def test_remove(self):
		"EntryStore.remove_entry() removes entry"

		entrystore = data.EntryStore()
		iter = entrystore.add_entry(entry.GenericEntry())

		self.assertEquals(entrystore.iter_n_children(None), 1)
		entrystore.remove_entry(iter)
		self.assertEquals(entrystore.iter_n_children(None), 0)

	

class EntryStore_update_entry(unittest.TestCase):
	"EntryStore.update_entry()"

	def test_changed(self):
		"EntryStore.update_entry() sets .changed to True"

		entrystore = data.EntryStore()

		e = entry.GenericEntry()
		iter = entrystore.add_entry(e)
		entrystore.changed = False

		e.name = "test"
		entrystore.update_entry(iter, e)
		self.assertEquals(entrystore.changed, True)


	def test_data(self):
		"EntryStore.update_entry() updates all data"

		entrystore = data.EntryStore()

		e = entry.GenericEntry()
		iter = entrystore.add_entry(e)

		e.name = "name"
		e.description = "description"
		e.updated = 1
		e.get_field(entry.HostnameField).value = "hostname"
		e.get_field(entry.UsernameField).value = "username"
		e.get_field(entry.PasswordField).value = "password"

		entrystore.update_entry(iter, e)

		ce = entrystore.get_entry(iter)
		self.assertEquals(entrystore.get_value(iter, 0), e.name)
		self.assertEquals(entrystore.get_value(iter, 1), e.icon)
		self.assertEquals(e.name, ce.name)
		self.assertEquals(e.description, ce.description)
		self.assertEquals(e.updated, ce.updated)
		self.assertEquals(e[entry.HostnameField], ce[entry.HostnameField])
		self.assertEquals(e[entry.UsernameField], ce[entry.UsernameField])
		self.assertEquals(e[entry.PasswordField], ce[entry.PasswordField])


	def test_none(self):
		"EntryStore.update_entry() accepts None iter"

		entrystore = data.EntryStore()
		entrystore.update_entry(None, None)



class UndoQueue_add_action(unittest.TestCase):
	"UndoQueue.add_action()"

	def test_add(self):
		"UndoQueue.add_action() adds an action"

		undoqueue = data.UndoQueue()
		undoqueue.add_action("test", None, None, {})

		self.assertEquals(undoqueue.can_undo(), True)
		self.assertEquals(undoqueue.can_redo(), False)

		self.assertEquals(undoqueue.get_undo_action(), ( None, "test", {} ))


	def test_inject(self):
		"UndoQueue.add_action() removes actions later in the queue"

		undoqueue = data.UndoQueue()
		undoqueue.add_action("test0", lambda n,d: 1, lambda n,d: 1, {})
		undoqueue.add_action("test1", lambda n,d: 1, lambda n,d: 1, {})
		undoqueue.add_action("test2", lambda n,d: 1, lambda n,d: 1, {})
		undoqueue.add_action("test3", lambda n,d: 1, lambda n,d: 1, {})

		undoqueue.undo()
		undoqueue.undo()

		undoqueue.add_action("test4", lambda n,d: 1, lambda n,d: 1, {})

		self.assertEquals(undoqueue.can_redo(), False)
		self.assertEquals(undoqueue.get_undo_action()[1], "test4")
		undoqueue.undo()
		self.assertEquals(undoqueue.get_undo_action()[1], "test1")



class UndoQueue_can_redo(unittest.TestCase):
	"UndoQueue.can_redo()"

	def test_can_redo(self):
		"UndoQueue.can_redo() returns correct values"

		undoqueue = data.UndoQueue()
		self.assertEquals(undoqueue.can_redo(), False)

		undoqueue.add_action("test", lambda n,d: 1, lambda n,d: 1, None)
		self.assertEquals(undoqueue.can_redo(), False)

		undoqueue.add_action("test", lambda n,d: 1, lambda n,d: 1, None)
		self.assertEquals(undoqueue.can_redo(), False)

		undoqueue.undo()
		self.assertEquals(undoqueue.can_redo(), True)

		undoqueue.undo()
		self.assertEquals(undoqueue.can_redo(), True)

		undoqueue.redo()
		self.assertEquals(undoqueue.can_redo(), True)

		undoqueue.redo()
		self.assertEquals(undoqueue.can_redo(), False)



class UndoQueue_can_undo(unittest.TestCase):
	"UndoQueue.can_undo()"

	def test_can_undo(self):
		"UndoQueue.can_undo() returns correct values"

		undoqueue = data.UndoQueue()
		self.assertEquals(undoqueue.can_undo(), False)

		undoqueue.add_action("test", lambda n,d: 1, lambda n,d: 1, None)
		self.assertEquals(undoqueue.can_undo(), True)

		undoqueue.add_action("test", lambda n,d: 1, lambda n,d: 1, None)
		self.assertEquals(undoqueue.can_undo(), True)

		undoqueue.undo()
		self.assertEquals(undoqueue.can_undo(), True)

		undoqueue.undo()
		self.assertEquals(undoqueue.can_undo(), False)



class UndoQueue_clear(unittest.TestCase):
	"UndoQueue.clear()"

	def test_clear(self):
		"UndoQueue.clear() clears the queue"

		undoqueue = data.UndoQueue()
		undoqueue.add_action("test", lambda n,d: 1, lambda n,d: 1, None)
		undoqueue.add_action("test", lambda n,d: 1, lambda n,d: 1, None)
		undoqueue.undo()

		self.assertEquals(undoqueue.can_redo(), True)
		self.assertEquals(undoqueue.can_undo(), True)

		undoqueue.clear()
		self.assertEquals(undoqueue.can_redo(), False)
		self.assertEquals(undoqueue.can_undo(), False)



class UndoQueue_get_redo_action(unittest.TestCase):
	"UndoQueue.get_redo_action()"

	def test_data(self):
		"UndoQueue.get_redo_action() returns correct data"

		undoqueue = data.UndoQueue()
		undoqueue.add_action("name", lambda n,d: 1, None, [])
		undoqueue.undo()

		self.assertEquals(undoqueue.get_redo_action(), ( None, "name", [] ))


	def test_order(self):
		"UndoQueue.get_redo_action() returns the correct action"

		undoqueue = data.UndoQueue()
		undoqueue.add_action("name0", lambda n,d: 1, None, [])
		undoqueue.add_action("name1", lambda n,d: 1, None, [])
		undoqueue.add_action("name2", lambda n,d: 1, None, [])
		undoqueue.undo()
		undoqueue.undo()

		self.assertEquals(undoqueue.get_redo_action(), ( None, "name1", [] ))



class UndoQueue_get_undo_action(unittest.TestCase):
	"UndoQueue.get_undo_action()"

	def test_data(self):
		"UndoQueue.get_undo_action() returns correct data"

		undoqueue = data.UndoQueue()
		undoqueue.add_action("name", None, lambda n,d: 1, [])
		self.assertEquals(undoqueue.get_undo_action(), ( None, "name", [] ))


	def test_order(self):
		"UndoQueue.get_undo_action() returns the correct action"

		undoqueue = data.UndoQueue()
		undoqueue.add_action("name0", lambda n,d: 1, None, [])
		undoqueue.add_action("name1", lambda n,d: 1, None, [])
		undoqueue.add_action("name2", lambda n,d: 1, None, [])
		undoqueue.undo()
		undoqueue.undo()

		self.assertEquals(undoqueue.get_undo_action()[1], "name0" )




class UndoQueue_redo(unittest.TestCase):
	"UndoQueue.redo()"

	def test_callback(self):
		"UndoQueue.redo() correctly calls the callback"

		global called
		called = False

		def cb(name, actiondata):
			global called
			called = True

			self.assertEquals(name, "name")
			self.assertEquals(actiondata, "data")

		undoqueue = data.UndoQueue()
		undoqueue.add_action("name", lambda n,d: 1, cb, "data")
		undoqueue.undo()
		undoqueue.redo()

		self.assertEquals(called, True)


	def test_increment(self):
		"UndoQueue.redo() increments the action pointer"

		undoqueue = data.UndoQueue()
		undoqueue.add_action("action0", lambda n,d: 1, lambda n,d: 1, None)
		undoqueue.add_action("action1", lambda n,d: 1, lambda n,d: 1, None)
		undoqueue.add_action("action2", lambda n,d: 1, lambda n,d: 1, None)

		undoqueue.undo()
		undoqueue.undo()
		undoqueue.undo()

		self.assertEquals(undoqueue.get_redo_action()[1], "action0")
		undoqueue.redo()
		self.assertEquals(undoqueue.get_redo_action()[1], "action1")
		undoqueue.redo()
		self.assertEquals(undoqueue.get_redo_action()[1], "action2")
		undoqueue.redo()
		self.assertEquals(undoqueue.get_redo_action(), None)


	def test_overflow(self):
		"UndoQueue.redo() doesn't overflow the pointer"

		undoqueue = data.UndoQueue()
		undoqueue.add_action("action0", lambda n,d: 1, lambda n,d: 1, None)
		undoqueue.add_action("action1", lambda n,d: 1, lambda n,d: 1, None)
		undoqueue.add_action("action2", lambda n,d: 1, lambda n,d: 1, None)

		undoqueue.undo()
		undoqueue.undo()
		undoqueue.undo()
		undoqueue.redo()
		undoqueue.redo()
		undoqueue.redo()

		self.assertEquals(undoqueue.get_undo_action()[1], "action2")
		undoqueue.redo()
		self.assertEquals(undoqueue.get_undo_action()[1], "action2")



class UndoQueue_undo(unittest.TestCase):
	"UndoQueue.undo()"

	def test_callback(self):
		"UndoQueue.undo() correctly calls the callback"

		global called
		called = False

		def cb(name, actiondata):
			global called
			called = True

			self.assertEquals(name, "name")
			self.assertEquals(actiondata, "data")

		undoqueue = data.UndoQueue()
		undoqueue.add_action("name", cb, lambda n,d: 1, "data")
		undoqueue.undo()

		self.assertEquals(called, True)


	def test_increment(self):
		"UndoQueue.undo() decrements the action pointer"

		undoqueue = data.UndoQueue()
		undoqueue.add_action("action0", lambda n,d: 1, lambda n,d: 1, None)
		undoqueue.add_action("action1", lambda n,d: 1, lambda n,d: 1, None)
		undoqueue.add_action("action2", lambda n,d: 1, lambda n,d: 1, None)

		self.assertEquals(undoqueue.get_undo_action()[1], "action2")
		undoqueue.undo()

		self.assertEquals(undoqueue.get_undo_action()[1], "action1")
		undoqueue.undo()

		self.assertEquals(undoqueue.get_undo_action()[1], "action0")
		undoqueue.undo()

		self.assertEquals(undoqueue.get_undo_action(), None)


	def test_overflow(self):
		"UndoQueue.undo() doesn't make the pointer negative"

		undoqueue = data.UndoQueue()
		undoqueue.add_action("action0", lambda n,d: 1, lambda n,d: 1, None)
		undoqueue.add_action("action1", lambda n,d: 1, lambda n,d: 1, None)
		undoqueue.add_action("action2", lambda n,d: 1, lambda n,d: 1, None)

		undoqueue.undo()
		undoqueue.undo()

		self.assertEquals(undoqueue.get_undo_action()[1], "action0")

		undoqueue.undo()
		self.assertEquals(undoqueue.get_undo_action(), None)
		self.assertEquals(undoqueue.get_redo_action()[1], "action0")

		undoqueue.undo()
		self.assertEquals(undoqueue.get_undo_action(), None)
		self.assertEquals(undoqueue.get_redo_action()[1], "action0")



if __name__ == "__main__":
	unittest.main()

