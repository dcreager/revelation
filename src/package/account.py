# -*- coding: utf-8 -*-
#
# Account data
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

import gettext

_ = gettext.gettext


class Field(object):
	"Base class for account fields"

	name	= None
	value	= None



class SecretField(Field):
	"Field for secrets (passwords, PIN codes, etc)"

	name	= _('Password')



class URLField(Field):
	"Field for URLs"

	name	= _('URL')



class UserIDField(Field):
	"Field for user IDs (usernames, etc)"

	name	= _('Username')

