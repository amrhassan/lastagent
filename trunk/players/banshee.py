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

from dbusplayer import DBusPlayer

class Banshee(DBusPlayer):
	
	def __init__(self):
		
		DBusPlayer.__init__(self, 'banshee-1', ('org.bansheeproject.Banshee', '/org/bansheeproject/Banshee/PlayerEngine'))
	
	def isPlaying(self):
		return self.dbus_objects[0].GetCurrentState() == 'playing'
	
	def getArtist(self):
		try:
			return unicode(self.dbus_objects[0].GetCurrentTrack()['artist'])
		except:
			return None
	
	def getTitle(self):
		try:
			return unicode(self.dbus_objects[0].GetCurrentTrack()['name'])
		except:
			return None
