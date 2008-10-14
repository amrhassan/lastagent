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

from dbusplayer import *
import os


def shell(command):
	return unicode(os.popen(command).read().strip().encode('utf-8'))

class Audacious(DBusPlayer):
	
	def __init__(self):
		DBusPlayer.__init__(self, 'audacious', ('org.atheme.audacious', '/org/atheme/audacious'), ('org.atheme.audacious', '/org/atheme/audacious/player'))

	def isPlaying(self):
		return (self.dbus_objects[0].Status() == 'playing')
	
	def getArtist(self):
		try:
			return unicode(self.dbus_objects[0].SongTuple(self.dbus_objects[0].Position(), 'artist'))
		except:
			return None
	
	def getTitle(self):
		try:
			return unicode(self.dbus_objects[0].SongTuple(self.dbus_objects[0].Position(), 'title'))
		except:
			return None

	def getName(self):
		return "Audacious"
	
	def getIconStackName(self):
		return 'player-audacious-icon'
	
	def hasControls(self):
		return True
	
	def next(self):
		shell('audtool playlist-advance')
	
	def prev(self):
		shell('audtool playlist-reverse')
	
	def play(self):
		shell('audtool playback-playpause')
	
	def pause(self):
		shell('audtool playback-playpause')
