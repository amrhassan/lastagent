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

class Rhythmbox(DBusPlayer):
	
	def __init__(self):
		
		DBusPlayer.__init__(self, 'rhythmbox', ('org.gnome.Rhythmbox', '/org/gnome/Rhythmbox/Player'), ('org.gnome.Rhythmbox', '/org/gnome/Rhythmbox/Shell'))
		
	
	def isPlaying(self):
		return int(self.dbus_objects[0].getPlaying()) == 1
	
	def getArtist(self):
		if self.isRunning() and self.isPlaying():
			uri = self.dbus_objects[0].getPlayingUri()
			props = self.dbus_objects[1].getSongProperties(uri)
			
			return unicode(props['artist'])
		else:
			return None
	
	def getTitle(self):
		if self.isRunning() and self.isPlaying():
			uri = self.dbus_objects[0].getPlayingUri()
			props = self.dbus_objects[1].getSongProperties(uri)
			
			return unicode(props['title'])
		else:
			return None
