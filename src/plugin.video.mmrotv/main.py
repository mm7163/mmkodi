# -*- coding: utf-8 -*-
# Module: default
# Author: Roman V. M.
# Created on: 28.11.2014
# License: GPL v.3 https://www.gnu.org/copyleft/gpl.html

import sys
from urlparse import parse_qsl
import urllib,urllib2
import xbmcgui
import xbmcplugin

# Get the plugin url in plugin:// notation.
_url = sys.argv[0]
# Get the plugin handle as an integer number.
_handle = int(sys.argv[1])
# Free sample videos are provided by www.vidsplay.com
# Here we use a fixed set of properties simply for demonstrating purposes
# In a "real life" plugin you will need to get info and links to video files/streams
# from some web-site or online service.
VIDEOS = {"RoTV":[{'name': 'Digi24',
                       'thumb': 'https://pbs.twimg.com/profile_images/1857118628/Digi_24_logo_master_01.png',
                       'video': 'http://82.76.40.75/digi24edge/smil:digi24.smil/playlist.m3u8',
                       'genre': 'TV'},
					   {'name': 'TVR1 (seenow.ro)',
                      'thumb': 'http://media.port-network.com/picture/instance_7/1134533_7.gif',
                      'video': 'tvr1',
                      'genre': 'TV'},
					  {'name': 'TVR1 (tvr.ro)',
                      'thumb': 'http://media.port-network.com/picture/instance_7/1134533_7.gif',
                      'video': 'tvr1tvrro',
                      'genre': 'TV'},
					   {'name': 'TVR2 (seenow.ro)',
                      'thumb': 'http://media.port-network.com/picture/instance_7/1106848_7.gif',
                      'video': 'tvr2',
                      'genre': 'TV'},
					   {'name': 'TVR2 (tvr.ro)',
                      'thumb': 'http://media.port-network.com/picture/instance_7/1106848_7.gif',
                      'video': 'tvr2tvrro',
                      'genre': 'TV'},
					   {'name': 'TVR3 (seenow.ro)',
                      'thumb': 'http://media.port-network.com/picture/instance_7/1111092_7.gif',
                      'video': 'tvr3',
                      'genre': 'TV'},
					   {'name': 'TVR3 (tvr.ro)',
                      'thumb': 'http://media.port-network.com/picture/instance_7/1111092_7.gif',
                      'video': 'tvr3tvrro',
                      'genre': 'TV'},
					   {'name': 'TVR International (seenow.ro)',
                      'thumb': 'http://media.port-network.com/picture/instance_7/1070699_7.gif',
                      'video': 'tvri',
                      'genre': 'TV'},
					   {'name': 'TVR International (tvr.ro)',
                      'thumb': 'http://media.port-network.com/picture/instance_7/1070699_7.gif',
                      'video': 'tvritvrro',
                      'genre': 'TV'},
					  {'name': 'TVR Cluj (tvr.ro)',
                      'thumb': 'http://media.port-network.com/picture/instance_7/1070699_7.gif',
                      'video': 'tvrcjtvrro',
                      'genre': 'TV'},
					   {'name': 'TVR HD',
                      'thumb': 'http://media.port-network.com/picture/instance_7/1070699_7.gif',
                      'video': 'tvrhdtvrro',
                      'genre': 'TV'},
					   {'name': 'Romania TV',
                      'thumb': 'http://media.port-network.com/picture/instance_7/1111124_7.gif',
                      'video': 'rtv',
                      'genre': 'TV'},
					   {'name': 'B1 TV',
                      'thumb': 'http://media.port-network.com/picture/instance_7/1149339_7.gif',
                      'video': 'b1',
                      'genre': 'TV'},
					   {'name': 'Realitatea TV',
                      'thumb': 'http://i.imgur.com/iO9cxv7.jpg',
                      'video': 'http://realitatea.m247.ro/hls/live.m3u8',
                      'genre': 'TV'},
					   {'name': 'Rock TV',
                      'thumb': 'http://www.rockfm.ro/assets/layout/logoweb-rocktv.png',
                      'video': 'rocktv',
                      'genre': 'TV'},
					  {'name': 'Magic TV',
                      'thumb': 'http://www.magicfm.ro/provided/images/logoweb-magictv.png',
                      'video': 'magictv',
                      'genre': 'TV'},
					  {'name': 'Music Channel 1',
                      'thumb': 'http://www.livetvswatch.com/uploads/1-music-channel-tv-live-from-romania-1446180705.jpg',
                      'video': 'http://x1-music_channelx.api.channel.livestream.com/3.0/playlist.m3u8',
                      'genre': 'TV'},
					  {'name': 'UTV',
                      'thumb': 'https://upload.wikimedia.org/wikipedia/ro/1/10/U-TV-logo.gif',
                      'video': 'http://81.196.0.126:80/utvedge/utvlive/index.m3u8',
                      'genre': 'TV'},
					  {'name': 'KissTV',
                      'thumb': 'http://i.imgur.com/rFP8ada.jpg',
                      'video': 'kisstv',
                      'genre': 'TV'}
					  ]
			}
		  
def get_categories():
    """
    Get the list of video categories.
    Here you can insert some parsing code that retrieves
    the list of video categories (e.g. 'Movies', 'TV-shows', 'Documentaries' etc.)
    from some site or server.

    :return: list
    """
    return VIDEOS.keys()

def get_rocktv_url(initurl):
	global rocktv_url
	req = urllib2.Request(initurl)
	response = urllib2.urlopen(req)
	the_page = response.read()
	
	marker=the_page.index('file: "http')+7
	the_page=the_page[marker:]
	marker=the_page.index('"')
	the_page=the_page[:marker]
	rocktv_url=the_page.replace('&','??')

def get_seenow_url(id,streamname):
	initurl='http://www.seenow.ro:1937/service3/play/index/id/'+id+'/platform_id/8'
	a='http://fms75.mediadirect.ro:1937/live3/_definst_/'+streamname+'/playlist.m3u8?publisher=22??token='
	#b='??id=114673787??provider=-1??user_id=0&transaction_id=0??p_item_id='+id+'??publisher=22??'
	b='??provider=-1??user_id=0&transaction_id=0??p_item_id='+id+'??publisher=22??'
	
	global seenow_url
	req = urllib2.Request(initurl)
	response = urllib2.urlopen(req)
	the_page = response.read()
	
	marker=the_page.index('"token-high":"')+14
	the_page=the_page[marker:]
	marker=the_page.index('"')
	the_page=a+the_page[:marker]+b
	seenow_url=the_page.replace('&','??')

def get_tvr_url(id,streamname):
	#id='1'
	#streamname='tvr1'
	cookieiniturl='http://www.tvrplus.ro/emisiune-garantat-100-32'
	initurl='http://www.tvrplus.ro/iphone/show/live/id/'+id
	a='http://fms75.mediadirect.ro:1937/live3/_definst_/'+streamname+'/playlist.m3u8?publisher=4??token='
	b='??id=89660754??provider=-1'
	
	global tvr_url
	reqi = urllib2.Request(cookieiniturl)
	response = urllib2.urlopen(reqi)
	cookies=response.info()['Set-Cookie']
	the_page = response.read()
	
	req = urllib2.Request(initurl)
	req.add_header("Cookie", cookies)
	response = urllib2.urlopen(req)
	#cookies=response.info()['Set-Cookie']
	the_page = response.read()
	
	marker=the_page.index('"token-high":"')+14
	the_page=the_page[marker:]
	marker=the_page.index('"')
	the_page=a+the_page[:marker]+b
	tvr_url=the_page.replace('&','??')

def get_videos(category):
    """
    Get the list of videofiles/streams.
    Here you can insert some parsing code that retrieves
    the list of videostreams in a given category from some site or server.

    :param category: str
    :return: list
    """
    return VIDEOS[category]


def list_categories():
    """
    Create the list of video categories in the Kodi interface.
    """
    # Get video categories
    categories = get_categories()
    # Create a list for our items.
    listing = []
    # Iterate through categories
    for category in categories:
        # Create a list item with a text label and a thumbnail image.
        list_item = xbmcgui.ListItem(label=category)
        # Set graphics (thumbnail, fanart, banner, poster, landscape etc.) for the list item.
        # Here we use the same image for all items for simplicity's sake.
        # In a real-life plugin you need to set each image accordingly.
        list_item.setArt({'thumb': 'http://gamesapk.pk/ArticleImages/tv-romania-free.jpg',
                          'icon': 'http://gamesapk.pk/ArticleImages/tv-romania-free.jpg',})
        # Set additional info for the list item.
        # Here we use a category name for both properties for for simplicity's sake.
        # setInfo allows to set various information for an item.
        # For available properties see the following link:
        # http://mirrors.xbmc.org/docs/python-docs/15.x-isengard/xbmcgui.html#ListItem-setInfo
        list_item.setInfo('video', {'title': category, 'genre': category})
        # Create a URL for the plugin recursive callback.
        # Example: plugin://plugin.video.example/?action=listing&category=Animals
        url = '{0}?action=listing&category={1}'.format(_url, category)
        # is_folder = True means that this item opens a sub-list of lower level items.
        is_folder = True
        # Add our item to the listing as a 3-element tuple.
        listing.append((url, list_item, is_folder))
    # Add our listing to Kodi.
    # Large lists and/or slower systems benefit from adding all items at once via addDirectoryItems
    # instead of adding one by ove via addDirectoryItem.
    xbmcplugin.addDirectoryItems(_handle, listing, len(listing))
    # Add a sort method for the virtual folder items (alphabetically, ignore articles)
    xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
    # Finish creating a virtual folder.
    xbmcplugin.endOfDirectory(_handle)


def list_videos(category):
    """
    Create the list of playable videos in the Kodi interface.

    :param category: str
    """
    # Get the list of videos in the category.
    videos = get_videos(category)
    # Create a list for our items.
    listing = []
    # Iterate through videos.
    for video in videos:
        # Create a list item with a text label and a thumbnail image.
        list_item = xbmcgui.ListItem(label=video['name'])
        # Set additional info for the list item.
        list_item.setInfo('video', {'title': video['name'], 'genre': video['genre']})
        # Set graphics (thumbnail, fanart, banner, poster, landscape etc.) for the list item.
        # Here we use the same image for all items for simplicity's sake.
        # In a real-life plugin you need to set each image accordingly.
        # list_item.setArt({'thumb': video['thumb'], 'icon': video['thumb'], 'fanart': video['thumb']})
        list_item.setArt({'thumb': video['thumb'], 'icon': video['thumb']})
		# Set 'IsPlayable' property to 'true'.
        # This is mandatory for playable items!
        list_item.setProperty('IsPlayable', 'true')
        # Create a URL for the plugin recursive callback.
        # Example: plugin://plugin.video.example/?action=play&video=http://www.vidsplay.com/vids/crab.mp4
        url = '{0}?action=play&video="{1}"'.format(_url, video['video'])
        # Add the list item to a virtual Kodi folder.
        # is_folder = False means that this item won't open any sub-list.
        is_folder = False
        # Add our item to the listing as a 3-element tuple.
        listing.append((url, list_item, is_folder))
    # Add our listing to Kodi.
    # Large lists and/or slower systems benefit from adding all items at once via addDirectoryItems
    # instead of adding one by ove via addDirectoryItem.
    xbmcplugin.addDirectoryItems(_handle, listing, len(listing))
    # Add a sort method for the virtual folder items (alphabetically, ignore articles)
    xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
    # Finish creating a virtual folder.
    xbmcplugin.endOfDirectory(_handle)


def play_video(path):
    """
    Play a video by the provided path.

    :param path: str
    """
    # Create a playable item with a path to play.
    play_item = xbmcgui.ListItem(path=path)
    # Pass the item to the Kodi player.
    xbmcplugin.setResolvedUrl(_handle, True, listitem=play_item)


def router(paramstring):
    """
    Router function that calls other functions
    depending on the provided paramstring

    :param paramstring:
    """
    # Parse a URL-encoded paramstring to the dictionary of
    # {<parameter>: <value>} elements
    params = dict(parse_qsl(paramstring))
    # Check the parameters passed to the plugin
    if params:
        if params['action'] == 'listing':
            # Display the list of videos in a provided category.
            list_videos(params['category'])
        elif params['action'] == 'play':
            # Play a video from a provided URL.
			myparams = params['video'].replace('??','&')
			#xbmcgui.Dialog().ok("bla",myparams)
			if myparams == '"rocktv"':
				get_rocktv_url('http://api.rockfm.ro/api/rocktv/embed')
				#xbmcgui.Dialog().ok("bla",rocktv_url[40:])
				play_video(rocktv_url.replace('??','&'))
			elif myparams == '"magictv"':
				get_rocktv_url('http://api.magicfm.ro/api/magictv/embed')
				play_video(rocktv_url.replace('??','&'))
			elif myparams == '"kisstv"':
				get_seenow_url('26180','kiss_low')
				play_video(seenow_url.replace('??','&'))
			elif myparams == '"tvr1"':
				get_seenow_url('207150','tvr1_low')
				play_video(seenow_url.replace('??','&'))
			elif myparams == '"tvr1tvrro"':
				get_tvr_url('1','tvr1')
				play_video(tvr_url.replace('??','&'))
			elif myparams == '"tvr2tvrro"':
				get_tvr_url('2','tvr2')
				play_video(tvr_url.replace('??','&'))
			elif myparams == '"tvr3tvrro"':
				get_tvr_url('5','tvr3')
				play_video(tvr_url.replace('??','&'))
			elif myparams == '"tvritvrro"':
				get_tvr_url('3','tvr')
				play_video(tvr_url.replace('??','&'))
			elif myparams == '"tvrcjtvrro"':
				get_tvr_url('12','tvrcluj')
				play_video(tvr_url.replace('??','&'))
			elif myparams == '"tvrhdtvrro"':
				get_tvr_url('7','tvrhd')
				play_video(tvr_url.replace('??','&'))
			elif myparams == '"tvr2"':
				get_seenow_url('100743','tvr2_low')
				play_video(seenow_url.replace('??','&'))
			elif myparams == '"tvr3"':
				get_seenow_url('5424','tvr3_low')
				play_video(seenow_url.replace('??','&'))
			elif myparams == '"tvri"':
				get_seenow_url('134246','tvr_low')
				play_video(seenow_url.replace('??','&'))
			elif myparams == '"rtv"':
				get_seenow_url('19291','rtv_low')
				play_video(seenow_url.replace('??','&'))
			elif myparams == '"b1"':
				get_seenow_url('25632','b1')
				play_video(seenow_url.replace('??','&'))
			else:
				play_video(myparams[1:-1])		
    else:
        # If the plugin is called from Kodi UI without any parameters,
        # display the list of video categories
        list_categories()


if __name__ == '__main__':
    # Call the router function and pass the plugin call parameters to it.
    # We use string slicing to trim the leading '?' from the plugin call paramstring
    router(sys.argv[2][1:])
