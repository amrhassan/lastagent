# -*- coding: utf-8 -*-

import gtk
import pylast
from pylast import Track
from cacher import Cacher
import os
import sys
import players.current
import threading
from share_dialog import ShareDialog
from tag_dialog import TagDialog
from custom_labels import *
from image_store import *
from stock_setup import *
from about_dialog import AboutApp
from custom_widgets import *
from add_dialog import *

PLAYBACK_CHECKING_INTERVAL = 2.0	#in seconds

PROCESS_TAG = 0
PROCESS_LOVE = 1
PROCESS_SHARE = 2
PROCESS_ADD = 3

class MainWindow(gtk.Window):
	
	def __init__(self, application):
		gtk.Window.__init__(self, gtk.WINDOW_TOPLEVEL)
		
		self.shown_track = None
		self.shown_artist = None
		self.shown_album = None
		
		self.app = application
		
		self.hidden = False
		self.art_store = ImageStore()
		
		get_factory().add_default()
		
		self.setup()
		
		self.show_track()
	
	def setup(self):
		#declarations
		self.main_box = gtk.VBox()
		self.content_box = gtk.HBox(False, 10)
		self.art = gtk.Image()
		self.art_box = gtk.VBox()
		self.track_box = gtk.VBox()
		self.title_label = TitleLabel()
		self.title_box = gtk.HBox()
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
		self.playlist_image = gtk.Image()
		self.share_button = gtk.Button()
		self.tag_button = gtk.Button()
		self.playlist_add_button = gtk.Button()
		self.status_bar = StatusBar()
		self.status_icon = gtk.StatusIcon()
		self.album_label = AlbumLabel()
		self.album_box = gtk.HBox()
		self.waiting_animation = gtk.gdk.PixbufAnimation('gui/images/waiting1.gif')
		self.quit_action = gtk.Action('quit', '_Quit', 'Exit', gtk.STOCK_QUIT)
		self.about_action = gtk.Action('about', '_About', 'About', gtk.STOCK_ABOUT)
		self.love_track_action = gtk.Action('love-track', '_Love', 'Love the currently playing track', STOCK_LOVE)
		self.tag_track_action = gtk.Action('tag-track', '_Tag...', 'Tag the currently playing track', STOCK_TAG)
		self.share_track_action = gtk.Action('share-track', '_Share...', 'Share the currently playing track', STOCK_SHARE)
		self.tag_artist_action = gtk.Action('tag-artist', '_Tag...', 'Tag the artist', STOCK_TAG)
		self.share_artist_action = gtk.Action('share-artist', '_Share...', 'Share the artist', STOCK_SHARE)
		self.tag_album_action = gtk.Action('tag-album', '_Tag...', 'Tag the album', STOCK_TAG)
		self.share_album_action = gtk.Action('share-album', '_Share...', 'Share an album', STOCK_SHARE)
		self.playlist_add_action = gtk.Action('playlist-add', '_Add...', 'Add to playlist', STOCK_PLAYLIST)
		
		
		#self
		self.resize(350, 100)
		self.set_title('%s: %s' %(self.app.name, self.app.current_user.getName()))
		self.set_position(gtk.WIN_POS_CENTER)
		self.add(self.main_box)
		self.connect('delete_event', self.on_self_delete)
		self.connect('show', self.on_self_show)
		self.connect('hide', self.on_self_hide)
		self.set_icon(self.app.pixbuf_icon)
		self.deletable = False
		if self.app.settings.get('main_keep_above', '1', 'display') == '1':
			self.set_keep_above(True)
		if self.app.settings.get('main_skip_taskbar', '0', 'display') == '1':
			self.set_property('skip-taskbar-hint', True)
		if self.app.settings.get('main_resizable', '0', 'display') == '0':
			self.set_resizable(False)
		self.show()
		
		#status_icon
		self.status_icon.set_from_stock(STOCK_LASTAGENT)
		self.status_icon.set_visible(True)
		self.status_icon.set_tooltip(self.get_title())
		self.status_icon.connect('activate', self.on_status_icon_activate)
		self.status_icon.connect('popup-menu', self.on_status_icon_popup)
		
		#main_box
		self.main_box.pack_start(self.content_box)
		self.main_box.pack_end(self.status_bar, False)
		self.main_box.show()
		
		#content_box
		self.content_box.pack_start(self.art_box, False, False)
		self.content_box.pack_start(self.track_pane_box)
		self.content_box.set_border_width(10)
		self.content_box.show()
		
		#art_box
		self.art_box.pack_start(self.art, False)
		self.art_box.show()
		
		#art
		self.art.show()
		
		#artist_label
		self.artist_label.set_tag_action(self.tag_artist_action)
		self.artist_label.set_share_action(self.share_artist_action)
		self.artist_label.show()
		
		#title_box
		self.title_box.pack_start(self.title_label, False, False)
		self.title_box.show()
		
		#title_label
		self.title_label.show()
		self.title_label.set_alignment(0, 0.5)
		self.title_label.set_love_action(self.love_track_action)
		self.title_label.set_tag_action(self.tag_track_action)
		self.title_label.set_share_action(self.share_track_action)
		self.title_label.set_add_action(self.playlist_add_action)
		
		#by_label
		self.by_label.set_markup('<b>by </b>')
		self.by_label.show()
		
		#artist_box
		self.artist_box.pack_start(self.by_label, False, False)
		self.artist_box.pack_start(self.artist_label, False, False)
		self.artist_box.show()
		
		#track_box
		self.track_box.pack_start(self.title_box, False, False)
		self.track_box.pack_start(self.artist_box, False, False)
		self.track_box.pack_start(self.album_box, False, False)
		self.track_box.show()
		
		#not_playing_label
		self.not_playing_label.set_markup('<big><b>Not Playing</b></big>')
		self.not_playing_label.set_sensitive(False)
		
		#status_bar
		self.status_bar.set_default_icon_from_stock(STOCK_NETWORK)
		self.status_bar.set_default_status('Ready.')
		self.status_bar.reset_to_default(0)
		self.status_bar.show_all()
		
		#love_image
		self.love_image.set_from_stock(STOCK_LOVE, gtk.ICON_SIZE_BUTTON)
		self.love_image.show()
		
		#tag_image
		self.tag_image.set_from_stock(STOCK_TAG, gtk.ICON_SIZE_BUTTON)
		self.tag_image.show()
		
		#share_image
		self.share_image.set_from_stock(STOCK_SHARE, gtk.ICON_SIZE_BUTTON)
		self.share_image.show()
		
		#playlist_image
		self.playlist_image.set_from_stock(STOCK_PLAYLIST, gtk.ICON_SIZE_BUTTON)
		self.playlist_image.show()
		
		#tag_button
		##self.tag_button.set_tooltip_text('Tag...')
		self.tag_button.set_label('_Tag')
		self.tag_button.set_image(self.tag_image)
		self.tag_button.set_size_request(75, -1)
		self.tag_button.connect_object('clicked', gtk.Action.activate, self.tag_track_action)
		##self.tag_button.set_relief(gtk.RELIEF_NONE)
		self.tag_button.set_focus_on_click(False)
		self.tag_button.show()
		
		#share_button
		##self.share_button.set_tooltip_text('Share...')
		self.share_button.set_label('_Share')
		self.share_button.set_image(self.share_image)
		self.share_button.set_size_request(75, -1)
		self.share_button.connect_object('clicked', gtk.Action.activate, self.share_track_action)
		##self.share_button.set_relief(gtk.RELIEF_NONE)
		self.share_button.set_focus_on_click(False)
		self.share_button.show()
		
		#playlist_add_button
		##self.playlist_add_button.set_tooltip_text('Add to a playlist...')
		self.playlist_add_button.set_label('_Add')
		self.playlist_add_button.set_image(self.playlist_image)
		self.playlist_add_button.set_size_request(75, -1)
		self.playlist_add_button.connect_object('clicked', gtk.Action.activate, self.playlist_add_action)
		##self.playlist_add_button.set_relief(gtk.RELIEF_NONE)
		self.playlist_add_button.set_focus_on_click(False)
		self.playlist_add_button.show()
		
		#love_button
		##self.love_button.set_tooltip_text("Love")
		self.love_button.set_label("_Love")
		self.love_button.set_image(self.love_image)
		self.love_button.set_size_request(75, -1)
		self.love_button.connect_object('clicked', gtk.Action.activate, self.love_track_action)
		##self.love_button.set_relief(gtk.RELIEF_NONE)
		self.love_button.set_focus_on_click(False)
		self.love_button.show()
		
		#track_buttons_box
		self.track_buttons_box.pack_end(self.share_button, False, False, 2)
		self.track_buttons_box.pack_end(self.playlist_add_button, False, False, 2)
		self.track_buttons_box.pack_end(self.tag_button, False, False, 2)
		self.track_buttons_box.pack_end(self.love_button, False, False, 2)
		self.track_buttons_box.show()
		
		#album_box
		self.album_box.pack_start(self.album_label, False, False)
		self.album_box.show()
		
		#album_label
		self.album_label.set_alignment(0, 0.5)
		self.album_label.set_tag_action(self.tag_album_action)
		self.album_label.set_share_action(self.share_album_action)
		
		#track_pane_box
		self.track_pane_box.pack_start(self.track_box, False, False)
		self.track_pane_box.pack_start(self.not_playing_label)
		self.track_pane_box.pack_end(self.track_buttons_box, False)
		self.track_pane_box.show()
		
		#quit_action
		self.quit_action.connect('activate', self.on_quit_action_activate)
		
		#about_action
		self.about_action.connect('activate', self.on_about_action_activate)
		
		#love_track_action
		self.love_track_action.connect('activate', self.on_love_track_action_activate)
		
		#tag_track_action
		self.tag_track_action.connect('activate', self.on_tag_track_action_activate)
		
		#share_track_action
		self.share_track_action.connect('activate', self.on_share_track_action_activate)
		
		#tag_artist_action
		self.tag_artist_action.connect('activate', self.on_tag_artist_action_activate)
		
		#share_artist_action
		self.share_artist_action.connect('activate', self.on_share_artist_action_activate)
		
		#tag_album_action
		self.tag_album_action.connect('activate', self.on_tag_album_action_activate)
		
		#share_album_action
		self.share_album_action.connect('activate', self.on_share_album_action_activate)
		
		#playlist_add_action
		self.playlist_add_action.connect('activate', self.on_playlist_add_action_activate)
	
	def _create_tray_menu(self):
		menu = gtk.Menu()
		
		#track menu
		if self.shown_track:
			track_item = gtk.ImageMenuItem(self.shown_track.toStr())
			
			size = int(self.app.settings.get('menu_track_art_size', '50', 'display'))
			
			track_item.set_image(gtk.image_new_from_pixbuf(self.art_store.get_image(self.current_art_filename, size)))
			track_item.show()
			menu.append(track_item)
			
			menu.append(self.love_track_action.create_menu_item())
			menu.append(self.tag_track_action.create_menu_item())
			menu.append(self.playlist_add_action.create_menu_item())
			menu.append(self.share_track_action.create_menu_item())
			
			track_item.connect('button-press-event', self.on_track_menuitem_pressed)
			
			menu.append(gtk.SeparatorMenuItem())
			
			artist_menu = gtk.Menu()
			artist_menu.append(self.tag_artist_action.create_menu_item())
			artist_menu.append(self.share_artist_action.create_menu_item())
			
			artist_item = gtk.ImageMenuItem('A_rtist')
			artist_item.set_image(gtk.image_new_from_stock(STOCK_ARTIST, gtk.ICON_SIZE_MENU))
			artist_item.set_submenu(artist_menu)
			menu.append(artist_item)
			
			if self.shown_album:
				#menu.append(gtk.SeparatorMenuItem())
				
				album_item = gtk.ImageMenuItem('A_lbum')
				album_item.set_image(gtk.image_new_from_stock(STOCK_ALBUM, gtk.ICON_SIZE_MENU))
				
				album_menu = gtk.Menu()
				album_menu.append(self.tag_album_action.create_menu_item())
				album_menu.append(self.share_album_action.create_menu_item())
				
				album_item.set_submenu(album_menu)
				
				menu.append(album_item)
				
			menu.append(gtk.SeparatorMenuItem())
			
		menu.append(self.about_action.create_menu_item())
		menu.append(self.quit_action.create_menu_item())
		
		#menu.set_border_width(3)
		menu.show_all()
		
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
			self.status_bar.set_icon_from_stock(STOCK_IDLE_NETWORK)
		else:
			self.not_playing_label.hide()
			self.track_box.show()
			self.track_buttons_box.set_sensitive(True)
			self.status_bar.set_icon_from_stock(STOCK_NETWORK)
		
		self.set_art()
	
	def set_art(self, image_filepath = None):
		if not image_filepath:
			image_filepath = 'gui/images/album.png'
		
		dimension = int(self.app.settings.get('main_art_dimension', '174', 'display'))
		image_pixbuf = self.art_store.get_image(image_filepath, dimension)
		
		self.current_art_filename = image_filepath
		
		self.art.set_from_pixbuf(image_pixbuf)
		
		##width = int(self.app.settings.get('main_default_width', '500', 'display'))
		##self.resize(width, 1)

	def show_track(self):
		
		self.restart_timer()
		track = self.get_playing_track()
		
		if not track:
			self.show_not_playing()
			self.shown_track = None
			self.shown_album = None
			self.shown_artist = None
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
		
		artist = track.getArtist()
		
		self.shown_track = track
		self.shown_artist = artist
		self.shown_album = None
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
			self.shown_album = sender.getAlbum()
			self.album_label.set_album(self.shown_album)
		
		#get cached image
		cacher = Cacher(self.app.cache_dir)
		cacher.async_get_cached(url, self._set_art_callback)
	
	def set_status_working(self, process, object):
		
		if process == PROCESS_LOVE:
			text = 'Loving ' + object.toStr() + '...'
		elif process == PROCESS_TAG:
			text = 'Tagging ' + object.toStr() + '...'
		elif process == PROCESS_SHARE:
			text = 'Sharing ' + object.toStr() + '...'
		elif process == PROCESS_ADD:
			text = 'Adding ' + object.toStr() + ' to a playlist...'
		
		self.status_bar.set_status(text)
		self.status_bar.set_icon_from_animation(self.waiting_animation)
	
	def set_status_success(self, process, object):
		
		if process == PROCESS_LOVE:
			name = 'loved'
		elif process == PROCESS_TAG:
			name = 'tagged'
		elif process == PROCESS_SHARE:
			name = 'shared'
		elif process == PROCESS_ADD:
			name = 'added'
		
		self.status_bar.set_status('%s was %s successfully.' %(object.toStr(), name), 5.0)
		self.status_bar.set_icon_from_stock(gtk.STOCK_APPLY)
	
	def set_status_error(self, process, object):
		
		if process == PROCESS_LOVE:
			action = 'loved'
		elif process == PROCESS_TAG:
			action = 'tagged'
		elif process == PROCESS_SHARE:
			action = 'shared'
		elif process == PROCESS_ADD:
			action = 'added'
			
		self.status_bar.set_status('%s could not be added.' %object.toStr(), 5.0)
		self.status_bar.set_icon_from_stock(gtk.STOCK_DIALOG_ERROR)
		
		message = 'An error has occured and %s was not %s.\n\nDetails:\n%s' \
		%(object.toStr(), action, object.last_error().__str__())
		
		mb = MessageBox("Error", message, gtk.STOCK_DIALOG_ERROR, self)
		mb.show()

	def love_callback(self, sender, output):
		if sender.last_error():
			self.set_status_error(PROCESS_LOVE, sender)
		else:
			self.set_status_success(PROCESS_LOVE, sender)
	
	def on_love_track_action_activate(self, sender):
		target = self.shown_track
		
		self.set_status_working(PROCESS_LOVE, target)
		
		target.async_call(self.love_callback, target.love)
		target.start()
	
	def on_share_track_action_activate(self, sender):
		
		self.share(self.shown_track)
	
	def share(self, target):
		
		d = ShareDialog(self, self.app, target)
		
		output = d.get_recipients()
		
		if output:
			self.set_status_working(PROCESS_SHARE, target)
			target.async_call(self.share_callback, target.share, output[0], output[1])
			target.start()
	
	def tag_callback(self, sender, output):
		if sender.last_error():
			self.set_status_error(PROCESS_TAG, sender)
		else:
			self.set_status_success(PROCESS_TAG, sender)
	
	def share_callback(self, sender, output):
		if sender.last_error():
			self.set_status_error(PROCESS_SHARE, sender)
		else:
			self.set_status_success(PROCESS_SHARE, sender)
	
	def on_tag_track_action_activate(self, sender):
		
		self.tag(self.shown_track)
	
	def on_tag_artist_action_activate(self, sender):
		self.tag(self.shown_track.getArtist())
	
	def on_share_artist_action_activate(self, sender):
		self.share(self.shown_track.getArtist())
	
	def on_tag_album_action_activate(self, sender):
		if self.shown_album:
			self.tag(self.shown_album)
	
	def on_share_album_action_activate(self, sender):
		if self.shown_album:
			self.share(self.shown_album)
	
	def tag(self, target):
		#target is Track, Artist or Album
		
		td = TagDialog(self, self.app, target)
		
		tag_names = td.get_tags()
		
		if tag_names != None:
			self.set_status_working(PROCESS_TAG, target)
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
	
	def on_playlist_add_action_activate(self, sender):
		target = self.shown_track
		
		ad = AddDialog(self, self.app, target)
		
		output = ad.get_playlist_id()
		
		if output:
			self.playlist_add(output, target)
	
	def playlist_add(self, playlist_id, track):
		self.set_status_working(PROCESS_ADD, track)
		track.async_call(self.playlist_add_callback, track.addToPlaylist, playlist_id)
		track.start()
	
	def playlist_add_callback(self, sender, output):
		
		if sender.last_error():
			if not int(sender.last_error().getID()) == int(pylast.STATUS_INVALID_PARAMS):
				self.set_status_error(PROCESS_ADD, sender)
				return
		
		self.set_status_success(PROCESS_ADD, sender)
	
	def fire_up(self):
		self.show()
		
		if '--hidden' in sys.argv:
			self.toggle_iconified()
