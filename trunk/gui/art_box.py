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

import gtk
import threading
from cacher import *
from image_store import *
import pylast

class ArtBox(gtk.Image):
	def __init__(self, app):
		gtk.Image.__init__(self)
		
		self.cache_dir = app.cache_dir
		self.store = ImageStore()
		self.app = app
		
		self.default_image_path = 'gui/images/album.png'
		
		self.image_path = self.default_image_path
		
		self.image_size = 1
	
	def set_size(self, size):
		self.image_size = size
	
	def _get_url_callback(self, sender, url):
		self.set_art(url)
	
	def set_art(self, image_url):
		cacher = Cacher(self.cache_dir)
		cacher.async_get_cached(image_url, self._get_path_callback)
	
	def _get_path_callback(self, sender, path):
		gtk.gdk.threads_enter()
		self._set_image(path)
		gtk.gdk.threads_leave()
	
	def _set_image(self, image_path):
		
		self.image_path = image_path
		self.set_from_pixbuf(self.store.get_image(image_path, self.image_size))
		
	
	def get_pixbuf_resized(self, size):
		return self.store.get_image(self.image_path, size)
	
	def get_image_resized(self, size):
		return gtk.image_new_from_pixbuf(self.get_pixbuf_resized(size))
	
	def show_default(self):
		gtk.gdk.threads_enter()
		self._set_image(self.default_image_path)
		gtk.gdk.threads_leave()
	
	def reset(self):
		self._set_image(self.image_path)
	
	def disable(self):
		self.set_sensitive(False)
	
	def enable(self):
		self.set_sensitive(True)
