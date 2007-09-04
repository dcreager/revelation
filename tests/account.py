# -*- coding: utf-8 -*-
#
# Unit-tests for account package
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

from package import account

from . import testutil


class TestSuite(testutil.TestSuite):
	"Account test suite"

	def __init__(self):
		testutil.TestSuite.__init__(self, [
			Account,
			Field,
			SecretField,
			URLField,
			UserIDField,
		])



class Account(testutil.TestCase):
	"Unit tests for Account"

	def setUp(self):
		self.account = account.Account()


	def test__attr_changed(self):
		"Account.changed exists"

		self.assertAttr(self.account, "changed")


	def test__attr_description(self):
		"Account.description exists"

		self.assertAttr(self.account, "description")


	def test__attr_name(self):
		"Account.name exists"

		self.assertAttr(self.account, "name")


	def test__attr_note(self):
		"Account.note exists"

		self.assertAttr(self.account, "note")



class Field(testutil.TestCase):
	"Unit tests for Field"

	def setUp(self):
		self.field = account.Field


	def test__attr_name(self):
		"Field.name exists"

		self.assertAttr(self.field, "name")


	def test__attr_value(self):
		"Field.value exists"

		self.assertAttr(self.field, "value")



class SecretField(testutil.TestCase):
	"Unit tests for SecretField"

	def test__subclass(self):
		"SecretField is Field subclass"

		self.assertSubclass(account.SecretField, account.Field)



class URLField(testutil.TestCase):
	"Unit tests for URLField"

	def test__subclass(self):
		"URLField is Field subclass"

		self.assertSubclass(account.URLField, account.Field)



class UserIDField(testutil.TestCase):
	"Unit tests for UserIDField"

	def test__subclass(self):
		"UserIDField is Field subclass"

		self.assertSubclass(account.UserIDField, account.Field)

