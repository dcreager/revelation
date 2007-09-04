# -*- coding: utf-8 -*-
#
# Module with base unit test classes
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

import unittest


class TestCase(unittest.TestCase):
	"Base class for unit tests"

	def assertAttr(self, object, attr, value = None):
		"Checks that an object has an attribute, and optionally the value of the attribute"

		self.assert_(hasattr(object, attr))

		if value is not None:
			self.assertEqual(getattr(object, attr), value)


	def assertContains(self, container, contents):
		"Checks if an item exist within another item"

		self.assert_(contents in container)


	def assertSubclass(self, subclass, superclass):
		"Checks that a class is a subclass of another class"

		self.assert_(issubclass(subclass, superclass))


	def assertType(self, object, objecttype):
		"Checks that an object is of a given type"

		self.assertEqual(type(object), objecttype)



class TestSuite(unittest.TestSuite):
	"Base class for test suites"

	def __init__(self, testcases):
		unittest.TestSuite.__init__(self)

		for testcase in testcases:
			self.addTests((
				issubclass(testcase, unittest.TestSuite) and testcase() or unittest.makeSuite(testcase),
			))


	def execute(self):
		"Runs the test suite"

		unittest.TextTestRunner(verbosity = 2).run(self)

