#
# Revelation - a password manager for GNOME 2
# http://oss.codepoet.no/revelation/
# $Id$
#
# Module for importing data from CSV files.
#
# Copyright (c) 2006 Devan Goodwin <dgoodwin@dangerouslyinc.com>
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

import csv, time

import base
from revelation import data, entry


class SplashIDCSV(base.DataHandler):
	"""
	Data handler for CSV files generated by SplashID.

	While SplashID CSV files were used as the basis for this parser,
	by arranging data in the format similar to what SplashID generates
	(i.e. use a spreadsheet and export a CSV with the proper format)
	one should be able to import any CSV file.

	SplashID's CSV data looks like the following:

	Type,Field 1,Field 2,Field 3,Field 4,Field 5,Field 6,Notes,Category

	The mapping to a Revelation generic entry takes place as follows:

	Type: 		Ignored
	Field 1:	Name
	Field 2:	Username
	Field 3:	Password
	Field 4:	Hostname
	Field 5:	Added to Description
	Field 6:	Added to Description
	Notes:		Added to Description
	Category:	Folder
	"""

	name		= "SplashID CSV"
	importer	= True
	exporter	= False
	encryption	= False

	def import_data(self, input, password):
		" Import data from a file into the entry store"

		# Replace any vertical tabs with spaces, SplashID seems to use
		# these to seperate lines within a Notes field:
		if input.count('\x0b'):
			input = input.replace('\x0b', ' ')

		entrystore = data.EntryStore()

		# Maintain a hash of folder names to folder entries so we
		# can use each category encountered to create a new folder
		# by that name, or use an existing one if we've already
		# created it:
		folders = {}

		for line in input.splitlines():
			for row in csv.reader([line]):

				# Raise FormatError if we don't have all 9 fields
				if len(row) != 9:
					raise base.FormatError

				# Import the entry
				e			= entry.GenericEntry()
				e.name			= row[1]
				e.description		= " / ".join([ desc.strip() for desc in row[5:8] if desc.strip() != "" ])
				e.updated		= time.time()

				e[entry.UsernameField]	= row[2]
				e[entry.PasswordField]	= row[3]
				e[entry.HostnameField]	= row[4]

				# Create and/or add to folder based on category:
				if folders.has_key(row[8]):
					parent = folders[category]

				else:
					folder		= entry.FolderEntry()
					folder.name	= category
					parent		= entrystore.add_entry(new_folder)
					folders[row[8]]	= parent

				# Add the entry
				entrystore.add_entry(e, parent)

		return entrystore
