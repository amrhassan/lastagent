# -*- coding: utf-8 -*-

import gtk
import pylast
from pylast import Track
from cacher import Cacher
import os
import players.current
import threading
from share_dialog import ShareDialog
from tag_dialog import TagDialog
from custom_labels import *
from image_store import *
from stock_setup import *
from about_dialog import AboutApp

PLAYBACK_CHECKING_INTERVAL = 2.0	#in seconds

class MainWindow(gtk.Window):
	
	def __init__(self, application):
		gtk.Window.__init__(self, gtk.WINDOW_TOPLEVEL)
		
		self.shown_track = None
		self.app = application
		
		self.hidden = False
		self.art_store = ImageStore()
		
		get_factory().add_default()
		
		self.setup()
		
		self.show_track()
		
		self.set_status()
	
	def setup(self):
		#declarations
		self.main_box = gtk.VBox()
		self.content_box = gtk.HBox(False, 10)
		self.art = gtk.Image()
		self.art_box = gtk.VBox()
		self.track_box = gtk.VBox()
		self.title_label = TitleLabel()
		self.artist_label = ArtistLabel()
		self.artist_box = gtk.HBox()
		self.by_label = gtk.Label()
		self.not_playing_label = gtk.Label()
		self.track_pane_box = gtk.VBox()
		self.love_button = gtk.Button()
		self.share_button = gtk.Button()
		self.tag_button = gtk.Button()
		self.track_buttons_box = gtk.HBox()
		self.main_buttons_box = gtk.HBox()
		self.love_image = gtk.Image()
		self.share_image = gtk.Image()
		self.tag_image = gtk.Image()
		self.share_button = gtk.Button()
		self.tag_button = gtk.Button()
		self.status_bar = gtk.Statusbar()
		self.status_icon = gtk.StatusIcon()
		self.album_label = AlbumLabel()
		self.quit_action = gtk.Action('quit', '_Quit', 'Exit', gtk.STOCK_QUIT)
		self.about_action = gtk.Action('about', '_About', 'About', gtk.STOCK_ABOUT)
		self.love_action = gtk.Action('love', '_Love', 'Love the currently playing track', STOCK_LOVE)
		self.tag_action = gtk.Action('tag', '_Tag', 'Tag the currently playing track', STOCK_TAG)
		self.share_action = gtk.Action('share', '_Share', 'Share the currently playing track', STOCK_SHARE)
		
		#self
		self.resize(350, 100)
		self.set_title('%s: %s' %(self.app.name, self.app.current_user.getName()))
		self.set_position(gtk.WIN_POS_CENTER)
		self.add(self.main_box)
		self.connect('delete_event', self.on_self_delete)
		self.connect('show', self.on_self_show)
		self.connect('hide', self.on_self_hide)
		self.set_icon(self.app.pixbuf_icon)
		#self.set_property('skip-taskbar-hint', True)
		self.set_keep_above(True)
		self.deletable = False
		self.resizable = False
		self.show()
		
		#status_icon
		self.status_icon.set_from_stock(STOCK_LASTAGENT)
		self.status_icon.set_visible(True)
		self.status_icon.set_tooltip(self.get_title())
		self.status_icon.connect('activate', self.on_status_icon_activate)
		self.status_icon.connect('popup-menu', self.on_status_icon_popup)
		
		#main_box
		self.main_box.pack_start(self.content_box, False, False)
		self.main_box.pack_end(self.status_bar, False)
		self.main_box.show()
		
		#content_box
		self.content_box.pack_start(self.art_box, False, False)
		self.content_box.pack_start(self.track_pane_box, False, False)
		self.content_box.set_border_width(10)
		self.content_box.show()
		
		#art_box
		self.art_box.pack_start(self.art, False)
		self.art_box.show()
		
		#art
		self.art.show()
		
		#artist_label
		self.artist_label.show()
		
		#title_label
		self.title_label.show()
		self.title_label.set_alignment(0, 0.5)
		
		#by_label
		self.by_label.set_text('by ')
		self.by_label.show()
		
		#artist_box
		self.artist_box.pack_start(self.by_label, False, False)
		self.artist_box.pack_start(self.artist_label, False, False)
		self.artist_box.show()
		
		#track_box
		self.track_box.pack_start(self.title_label, False, False)
		self.track_box.pack_start(self.artist_box, False, False)
		self.track_box.pack_start(self.album_label, False, False)
		self.track_box.show()
		
		#not_playing_label
		self.not_playing_label.set_markup('<big><b>Not Playing</b></big>')
		self.not_playing_label.set_sensitive(False)
		
		#status_bar
		self.status_bar.set_has_resize_grip(False)
		self.status_bar.show()
		
		#love_image
		self.love_image.set_from_stock(STOCK_LOVE, gtk.ICON_SIZE_BUTTON)
		self.love_image.show()
		
		#tag_image
		self.tag_image.set_from_stock(STOCK_TAG, gtk.ICON_SIZE_BUTTON)
		self.tag_image.show()
		
		#share_image
		self.share_image.set_from_stock(STOCK_SHARE, gtk.ICON_SIZE_BUTTON)
		self.share_image.show()
		
		#tag_button
		self.tag_button.set_label('_Tag')
		self.tag_button.set_image(self.tag_image)
		self.tag_button.set_size_request(75, -1)
		self.tag_button.connect_object('clicked', gtk.Action.activate, self.tag_action)
		self.tag_button.show()
		
		#share_button
		self.share_button.set_label('_Share')
		self.share_button.set_image(self.share_image)
		self.share_button.set_size_request(75, -1)
		self.share_button.connect_object('clicked', gtk.Action.activate, self.share_action)
		self.share_button.show()
		
		#love_button
		self.love_button.set_label("_Love")
		self.love_button.set_image(self.love_image)
		self.love_button.set_size_request(75, -1)
		self.love_button.connect_object('clicked', gtk.Action.activate, self.love_action)
		self.love_button.show()
		
		#track_buttons_box
		self.track_buttons_box.pack_end(self.share_button, False, False, 2)
		self.track_buttons_box.pack_end(self.tag_button, False, False, 2)
		self.track_buttons_box.pack_end(self.love_button, False, False, 2)
		self.track_buttons_box.show()
		
		#album_label
		self.album_label.set_alignment(0, 0.5)
		
		#track_pane_box
		self.track_pane_box.pack_start(self.track_box, False, False)
		self.track_pane_box.pack_start(self.not_playing_label)
		self.track_pane_box.pack_end(self.track_buttons_box, False)
		self.track_pane_box.show()
		
		#quit_action
		self.quit_action.connect('activate', self.on_quit_action_activate)
		
		#about_action
		self.about_action.connect('activate', self.on_about_action_activate)
		
		#love_action
		self.love_action.connect('activate', self.on_love_action_activate)
		
		#tag_action
		self.tag_action.connect('activate', self.on_tag_action_activate)
		
		#share_action
		self.share_action.connect('activate', self.on_share_action_activate)
		
	
	def _create_tray_menu(self):
		menu = gtk.Menu()
		
		#track menu
		if self.shown_track:
			track_item = gtk.ImageMenuItem(self.shown_track.toStr())
			track_item.set_image(gtk.image_new_from_pixbuf(self.art_store.get_image(self.current_art_filename, 50)))
			track_item.show()
			menu.append(track_item)
			
			submenu = menu
			submenu.append(self.love_action.create_menu_item())
			submenu.append(self.tag_action.create_menu_item())
			submenu.append(self.share_action.create_menu_item())
			
			#submenu.show()
			
			#track_item.set_submenu(submenu)
			
			track_item.connect('button-press-event', self.on_track_menuitem_pressed)
			
			sep = gtk.SeparatorMenuItem()
			sep.show()
			
			menu.append(sep)
		
		menu.append(self.about_action.create_menu_item())
		menu.append(self.quit_action.create_menu_item())
		
		#menu.set_border_width(3)
		menu.show()
		
		return menu
	
	def get_playing_track(self):
		player = players.current.getRunning()
		
		if player:
			return Track(player.getArtist(), player.getTitle(), *self.app.auth_data)
		
		return None
	
	def show_not_playing(self, not_playing = True):
		
		if not_playing:
			self.not_playing_label.show()
			self.track_box.hide()
			self.track_buttons_box.set_sensitive(False)
			self.album_label.hide()
			self.status_icon.set_tooltip(self.get_title())
		else:
			self.not_playing_label.hide()
			self.track_box.show()
			self.track_buttons_box.set_sensitive(True)
		
		self.set_art()
	
	def set_art(self, image_filepath = None):
		if not image_filepath:
			image_filepath = 'gui/images/no_cover.png'
		
		image_pixbuf = self.art_store.get_image(image_filepath, 174)
		
		self.current_art_filename = image_filepath
		
		self.art.clear()
		self.art.set_from_pixbuf(image_pixbuf)
		self.resize(1, 1)

	def show_track(self):
		
		self.restart_timer()
		track = self.get_playing_track()
		
		if not track:
			self.show_not_playing()
			self.shown_track = None
			return
		
		if self.shown_track and track._hash() == self.shown_track._hash():
			return
		
		self.album_label.hide()
		self.show_not_playing(not_playing = False)
		
		self.artist_label.set_artist(track.getArtist())
		self.title_label.set_track(track)
		self.set_art()
		
		track.async_call(self._get_image_callback, track.getImage, pylast.IMAGE_LARGE, True)
		track.start()
		
		self.shown_track = track
		self.status_icon.set_tooltip(track.toStr())
	
	def restart_timer(self):
		
		self.timer = threading.Timer(PLAYBACK_CHECKING_INTERVAL, self.show_track)
		self.timer.start()
	
	def _set_art_callback(self, sender, file_path):
		self.set_art(file_path)
	
	def _get_image_callback(self, sender, url):
		
		#show album
		if sender.getAlbum().getTitle():
			self.album_label.show()
			self.album_label.set_album(sender.getAlbum())
		
		#get cached image
		cacher = Cacher(self.app.cache_dir)
		cacher.async_get_cached(url, self._set_art_callback)
	
	def set_ready_status_in(self, seconds):
		
		timer = threading.Timer(seconds, self.set_status)
		timer.start()
	
	def set_status(self, message = 'Ready.'):
		
		id = self.status_bar.get_context_id(message)
		self.status_bar.push(id, message)
	
	def love_callback(self, sender, output):
		if sender.last_error():
			self.set_status(sender.last_error().__str__())
		else:
			self.set_status(sender.toStr() + ' was loved successfully.')
			self.set_ready_status_in(3.0)
	
	def on_love_action_activate(self, sender):
		self.set_status('Loving ' + self.shown_track.toStr() + '...')
		
		self.shown_track.async_call(self.love_callback, self.shown_track.love)
		self.shown_track.start()
	
	def on_share_action_activate(self, sender):
		
		self.share(self.shown_track)
	
	def share(self, target):
		
		d = ShareDialog(self, self.app, target)
		
		output = d.get_recipients()
		
		if output:
			self.set_status('Sharing ' + target.toStr() + '...')
			target.async_call(self.share_callback, target.share, output[0], output[1])
			target.start()
	
	def tag_callback(self, sender, output):
		if sender.last_error():
			self.set_status(sender.last_error().__str__())
			self.set_ready_status_in(10.0)
		else:
			self.set_status(sender.toStr() + ' was tagged successfully.')
			self.set_ready_status_in(3.0)
	
	def share_callback(self, sender, output):
		if sender.last_error():
			self.set_status(sender.last_error().__str__())
			self.set_ready_status_in(10.0)
		else:
			self.set_status(sender.toStr() + ' was shared successfully.')
			self.set_ready_status_in(3.0)
	
	def on_tag_action_activate(self, sender):
		
		self.tag(self.shown_track)

	
	def tag(self, target):
		#target is Track, Artist or Album
		
		td = TagDialog(self, self.app, target)
		
		tag_names = td.get_tags()
		
		if tag_names:
			self.set_status('Tagging ' + target.toStr() + '...')
			target.async_call(self.tag_callback, target.setTags, *tag_names)
			target.start()
	
	def on_status_icon_activate(self, sender):
		self.toggle_iconified()
	
	def toggle_iconified(self):
		if self.hidden:
			self.show()
			self.present()
		else:
			self.hide()
	
	def on_status_icon_popup(self, statusicon, button, time):
		self._create_tray_menu().popup(None, None, None, button, time)
	
	def on_quit_action_activate(self, sender):
		quit()
	
	def on_self_delete(self, sender, event):
		self.toggle_iconified()
		return True

	def on_about_action_activate(self, sender):
		d = AboutApp(self.app)
		d.run()

	def on_track_menuitem_pressed(self, sender, event):
		self.present()
	
	def on_self_hide(self, sender):
		self.hidden = True
	
	def on_self_show(self, sender):
		self.hidden = False
