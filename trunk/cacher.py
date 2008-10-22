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

import urllib
import os
import pylast

class Cacher(pylast.Asynchronizer):
	def __init__(self, cache_dir):
		self.cache_dir = cache_dir
		
		pylast.Asynchronizer.__init__(self)
		
		if not os.path.exists(cache_dir):
			os.mkdir(cache_dir)
	
	def _url2hash(self, url):
		
		i = url.rfind('.')
		name = url[:i]
		ext = url[i:]
		
		name = name[7:]
		
		name = name.replace('/', '-')
		name = name.replace('.', '-')
		
		return ''.join((name, ext))

	def _is_cached(self, url):
		path = os.path.join('/', self.cache_dir, self._url2hash(url))
		
		if os.path.exists(path):
			return path
		else:
			return False
	
	def _download(self, url):
		path = os.path.join('/', self.cache_dir, self._url2hash(url))
		
		urllib.urlretrieve(url, path)
		
		return path

	def get_cached(self, url):
		
		if self._is_cached(url):
			return self._is_cached(url)
		
		return self._download(url)
	
	def async_get_cached(self, url, callback):
		"""The callback function is prototyped as follows callback(sender, file_path)
		sender: This cacher object.
		output: The file path of the cached image.
		"""
		
		self.async_call(call = self.get_cached, callback = callback, call_args = (url,))
