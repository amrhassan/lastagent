import os

class INI(object):
	"""An interface to INI files"""
	
	def __init__(self, file_path, default_section = "Main"):
		self.path = file_path
		self.__root = {}
		self._load()
		self.__defaultSection = default_section
	
	def set(self, name, value, section = -1, dump = True):
		if section == -1:
			section = self.__defaultSection
		
		if not section in self.__root:
			self.__root[section] = {}
		self.__root[section][name] = value
		
		if dump:
			self._dump()
	
	def get(self, name, default_value, section = -1):
		if section == -1:
			section = self.__defaultSection
		
		if not section in self.__root:
			return default_value
		if not name in self.__root[section]:
			return default_value
		
		return self.__root[section][name]
	
	def _dump(self):
		f = file(self.path, "w")
		
		for section_name in self.__root.keys():
			f.write("[" + section_name + "]" + os.linesep)
			for value_name in self.__root[section_name].keys():
				f.write(value_name + "=" + self.__root[section_name][value_name] + os.linesep)
		
		f.close()
	
	def _load(self):
		if not os.path.exists(self.path):
			return
			
		f = file(self.path, "r")
		
		last_section = ""
		for line in f:
			if line.startswith("["):
				line = line.replace("[", "").replace("]", "")
				last_section = line.strip()
			else:
				values = line.split("=")
				self.set(values[0].strip(), values[1].strip(), last_section, False)
		
		f.close()
