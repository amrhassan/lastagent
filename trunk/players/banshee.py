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

class Banshee():
	
	def __init__(self):
		
		self.player = None
		
		self.bus = dbus.SessionBus()
		
		self.isRunning()	#to set self.player
	
	def isRunning(self):
		if os.popen('pidof banshee-1').read().strip():		
			if not self.player:
				self.player = self.bus.get_object("org.bansheeproject.Banshee", "/org/bansheeproject/Banshee/PlayerEngine")
			return True
		else:
			self.player = None
			return False

	def isPlaying(self):
		return self.player.GetCurrentState() == 'playing'
	
	def getArtist(self):
		if self.isRunning() and self.isPlaying():
			return unicode(self.player.GetCurrentTrack()['artist'])
		else:
			return None
	
	def getTitle(self):
		if self.isRunning() and self.isPlaying():
			return unicode(self.player.GetCurrentTrack()['name'])
		else:
			return None
