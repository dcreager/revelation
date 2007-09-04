# -*- coding: utf-8 -*-
#
# Test suite for Revelation
# $Id$
#
# Copyright ©2006-2007 Erik Grinaker <erikg@codepoet.no>
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

from . import account
from . import testutil



class TestSuite(testutil.TestSuite):
	"Main test suite"

	def __init__(self):
		testutil.TestSuite.__init__(self, [
			account.TestSuite,
		])

