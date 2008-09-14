import gtk
import webbrowser
import pango

class LinkLabel(gtk.EventBox):
	def __init__(self):
		gtk.EventBox.__init__(self)
		
		self.label = gtk.Label()
		self.add(self.label)
		self.label.show()
		self.text = ''
		
		self.connect('button-press-event', self.on_clicked)
		self.connect('enter-notify-event', self.on_mouse_enter)
		self.connect('leave-notify-event', self.on_mouse_leave)
	
	def set_alignment(self, xalign, yalign):
		self.label.set_alignment(xalign, yalign)
	
	def reset_text(self):
		self._set_markup(self.text)
	
	def enable_underline(self):
		self._set_markup('<u>' + self.text + '</u>')
	
	def enable_bold(self):
		self._set_markup('<b>' + self.text + '</b>')
	
	def enable_big(self):
		self._set_markup('<big>' + self.text + '</big>')
	
	def set_text(self, text):
		self.text = text
		self._set_markup(text)
		self.set_tooltip_text(self.label.get_text())
	
	def _set_markup(self, markup):
		markup = markup.replace('&', '&amp;')
		self.label.set_markup(markup)
	
	def set_url(self, url):
		self.url = url
		
		self.window.set_cursor(gtk.gdk.Cursor(gtk.gdk.HAND2))
	
	def on_clicked(self, sender, event):
		if event.button == 1:
			webbrowser.open(self.url)
	
	def on_mouse_enter(self, sender, event):
		self.enable_underline()
	
	def on_mouse_leave(self, sender, event):
		self.reset_text()

class AlbumLabel(LinkLabel):
	def __init__(self):
		LinkLabel.__init__(self)
	
	def set_album(self, album):
		self.set_text(album.getTitle())
		self.set_url(album.getURL())
		
		#self.label.set_ellipsize(pango.ELLIPSIZE_END)

class TitleLabel(LinkLabel):
	def __init__(self):
		LinkLabel.__init__(self)
	
	def set_track(self, track):
		self.set_text('<b><big>' + track.getTitle() + '</big></b>')
		self.set_url(track.getURL())

class ArtistLabel(LinkLabel):
	def __init__(self):
		LinkLabel.__init__(self)
	
	def set_artist(self, artist):
		self.set_text(artist.toStr())
		self.set_url(artist.getURL())
