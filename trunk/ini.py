# -*- coding: utf-8 -*-
#
# pylast - A Last.fm Music Tracker for Linux.
# Copyright (C) 2008-2009  Amr Hassan
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307
# USA

import os

class INI(object):
	"""An interface to INI files"""
	
	def __init__(self, file_path, default_section = "Main"):
		self.path = file_path
		self.__root = {}
		self._load()
		self.__defaultSection = default_section
	
	def set(self, name, value, section = None, dump = True):
		if not section:
			section = self.__defaultSection
		
		if not section in self.__root:
			self.__root[section] = {}
		self.__root[section][name] = value
		
		if dump:
			self._dump()
	
	def get(self, name, default_value, section = None):
		if not section:
			section = self.__defaultSection
		
		if not section in self.__root or not name in self.__root[section]:
			self.set(name, default_value, section)
		
		return self.__root[section][name]
	
	def _dump(self):
		f = file(self.path, "w")
		
		for section_name in self.__root.keys():
			f.write("[" + section_name + "]" + os.linesep)
			for value_name in self.__root[section_name].keys():
				f.write(value_name + "=" + self.__root[section_name][value_name] + os.linesep)
			
			f.write('\n')
		
		f.close()
	
	def _load(self):
		if not os.path.exists(self.path):
			return
			
		f = file(self.path, "r")
		
		last_section = ""
		for line in f:
			if line.strip() == '':
				continue
				
			if line.startswith("["):
				line = line.replace("[", "").replace("]", "")
				last_section = line.strip()
			else:
				values = line.split("=")
				self.set(values[0].strip(), values[1].strip(), last_section, False)
		
		f.close()
