import gtk
import webbrowser

class AboutApp(gtk.AboutDialog):
	def __init__(self, app):
		
		gtk.AboutDialog.__init__(self)
		
		gtk.about_dialog_set_url_hook(self.on_click_url, None)
		
		self.set_name(app.name)
		self.set_version(app.version)
		self.set_copyright(app.author)
		self.set_comments(app.comment)
		self.set_license(open('LICENSE').read())
		self.set_wrap_license(True)
		self.set_website('http://lastagent.googlecode.com/')
		self.set_authors(('* Amr Hassan (amr.hassan@gmail.com)',))
		self.set_artists(('* http://www.gorvan.com (Application icon taken from the "Last.fm icons 2" set)', '', '* Last.fm web site and official client icon designers (The rest of the icons)'))
		self.set_logo(app.pixbuf_icon)
		self.set_icon(app.pixbuf_icon)
		self.connect('response', self.on_response)
		

	
	def on_response(self, sender, response):
		sender.destroy()
	
	def on_click_url(self, sender, url, data):
		webbrowser.open(url)

