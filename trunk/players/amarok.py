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

import pydcop
import os

def shell(command):
	return os.popen(command).read().strip()

class Amarok():
	
	def __init__(self):
		
		self.amarok = None
		
		self.isRunning()
	
	def isRunning(self):
		if shell('pidof amarokapp'):
			if not self.amarok:
				self.amarok = pydcop.DCOPApplication('amarok')
			return True
		else:
			self.amarok = None
			return False

	def isPlaying(self):
		return self.amarok.player.isPlaying()
	
	def getArtist(self):
		if self.isRunning() and self.isPlaying():
			return self.amarok.player.artist()
		else:
			return None
	
	def getTitle(self):
		if self.isRunning() and self.isPlaying():
			return self.amarok.player.title()
		else:
			return None
