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

STOCK_LOVE = 'lastagent-love-icon'
STOCK_SHARE = 'lastagent-share-icon'
STOCK_TAG = 'lastagent-tag-icon'
STOCK_NETWORK = 'lastagent-network-icon'
STOCK_IDLE_NETWORK = 'lastagent-idle-network-icon'
STOCK_ARTIST = 'lastagent-artist-icon'
STOCK_ALBUM = 'lastagent-album-icon'
STOCK_USER = 'lastagent-user-icon'
STOCK_PLAYLIST = 'lastagent-playlist-icon'
STOCK_AMAROK = 'player-amarok-icon'
STOCK_BANSHEE = 'player-banshee-icon'
STOCK_AUDACIOUS = 'player-audacious-icon'
STOCK_RHYTHMBOX = 'player-rhythmbox-icon'

def get_factory():
	
	icons = [
		(STOCK_LOVE, 'gui/images/love.png'),
		(STOCK_TAG, 'gui/images/tag.png'),
		(STOCK_SHARE, 'gui/images/share.png'),
		(STOCK_NETWORK, 'gui/images/network.ico'),
		(STOCK_IDLE_NETWORK, 'gui/images/network-idle.png'),
		(STOCK_ALBUM, 'gui/images/album.png'),
		(STOCK_USER, 'gui/images/user.png'),
		(STOCK_ARTIST, 'gui/images/artist.png'),
		(STOCK_PLAYLIST, 'gui/images/playlist.png'),
		(STOCK_AMAROK, 'gui/images/amarok.png'),
		(STOCK_BANSHEE, 'gui/images/banshee.png'),
		(STOCK_AUDACIOUS, 'gui/images/audacious.png'),
		(STOCK_RHYTHMBOX, 'gui/images/rhythmbox.png'),
		]
	
	factory = gtk.IconFactory()
	
	for stock_id, file in icons:
		pixbuf = gtk.gdk.pixbuf_new_from_file(file)
		iconset = gtk.IconSet(pixbuf)
		factory.add(stock_id, iconset)
	
	return factory
