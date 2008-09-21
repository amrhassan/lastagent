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

import dbus
import os

class DBusPlayer():
	
	def __init__(self, process_name, *dbus_name_path_pairs):
		
		self.process_name = process_name
		
		self.bus = dbus.SessionBus()
		self.pairs = dbus_name_path_pairs
		self.dbus_objects = None
	
	def setup_objects(self):
		self.dbus_objects = []
		
		for pair in self.pairs:
			self.dbus_objects.append(self.bus.get_object(pair[0], pair[1]))
	
	def isRunning(self):
		if os.popen('pidof ' + self.process_name).read().strip():		
			if not self.dbus_objects:
				self.setup_objects()
			
			return True
		else:
			self.player = None
			return False

	def isPlaying(self):
		pass
		# should be overriden
	
	def getArtist(self):
		pass
		# should be overriden
	
	def getTitle(self):
		pass
		# should be overriden
