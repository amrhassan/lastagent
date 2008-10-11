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
import gtk
from logger import *

MAX_ART_AGE = 20	#after nth step, the objects get released for garbage collecting.

class ImageStore(object):
	def __init__(self):
		self.images = {}	#gtk.Image objects per file_name
		self.cache = {}		#scaled gtk.gdk.Pixbuf objects per max_dimension
		self.stats = {}		#int statistic per file_name
	
	def get_image(self, file_name, max_dimension):
		"""Returns a scaled pixbuf from a local cache."""
		
		if not file_name in self.images.keys():
			image = gtk.image_new_from_file(file_name)
			
			#a work around to delete the corrupted images
			try:
				buf = image.get_pixbuf()
			except:
				log_debug(self, 'Removed corrupted image at' + file_name + '.')
				os.remove(file_name)
				return None
			
			self.images[file_name] = image
			self.cache[file_name] = {}
			self.stats[file_name] = 0
		
		if not max_dimension in self.cache[file_name].keys():
			self.cache[file_name][max_dimension] = self._scale_image(self.images[file_name], max_dimension)
		
		self._step_stat(file_name)
		return self.cache[file_name][max_dimension]
	
	def _scale_image(self, image, max_dimension):
		"""Returns a scaled pixbuf."""
		
		pixbuf = image.get_pixbuf()
		
		width = pixbuf.get_width()
		height = pixbuf.get_height()
		
		if width > height:		
			n_width = max_dimension
			n_height = (height * max_dimension) / width
		else:
			n_height = max_dimension
			n_width = (width * max_dimension) / height
		
		return pixbuf.scale_simple(n_width, n_height, gtk.gdk.INTERP_BILINEAR)
	
	def _step_stat(self, file_name):
		
		self.stats[file_name] = 0
		
		for fn in self.images.keys():
			self.stats[fn] += 1
			
			if self.stats[fn] >= MAX_ART_AGE:
				for pixbuf in self.cache[fn]:
					del pixbuf
				del self.images[fn]
				del self.stats[fn]
