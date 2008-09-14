
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
		
		self.async_call(callback, self.get_cached, url)
		
		self.start()
