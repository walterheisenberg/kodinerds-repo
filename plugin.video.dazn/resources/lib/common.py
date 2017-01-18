# -*- coding: utf-8 -*-

import json,os,sys,urllib,urlparse
import time,datetime,random,re
import xbmc,xbmcaddon,xbmcgui,xbmcplugin

from uuid import getnode as uuid_node
from hashlib import md5

addon_handle = int(sys.argv[1])
addon        = xbmcaddon.Addon()
dialog       = xbmcgui.Dialog()
addon_id     = addon.getAddonInfo('id')
version      = addon.getAddonInfo('version')
icon         = addon.getAddonInfo('icon')
fanart       = addon.getAddonInfo('fanart')
content      = addon.getSetting('content')
view_id      = addon.getSetting('view_id')
force_view   = addon.getSetting('force_view') == 'true'
email        = addon.getSetting('email')
password     = addon.getSetting('password')
token        = addon.getSetting('token')
language     = addon.getSetting('language')
country      = addon.getSetting('country')
device_id    = addon.getSetting('device_id')
cdn          = int(addon.getSetting('server'))

base_url     = 'https://isl.dazn.com'
api_base     = base_url+'/isl/api/v1/dataservice/'

time_format  = '%Y-%m-%dT%H:%M:%SZ'

def log(msg):
    xbmc.log(str(msg), xbmc.LOGNOTICE)
    
def getString(id):
    return addon.getLocalizedString(id)

def build_url(query):
    return sys.argv[0] + '?' + urllib.urlencode(query)
    
def utfenc(str):
    try:
        str = str.encode('utf-8')
    except:
        pass
    return str

def timedelta_total_seconds(timedelta):
    return (
        timedelta.microseconds + 0.0 +
        (timedelta.seconds + timedelta.days * 24 * 3600) * 10 ** 6) / 10 ** 6

def utc2local(date_string):
    if date_string:
        utc = datetime.datetime(*(time.strptime(date_string, time_format)[0:6]))
        epoch = time.mktime(utc.timetuple())
        offset = datetime.datetime.fromtimestamp(epoch) - datetime.datetime.utcfromtimestamp(epoch)
        return (utc + offset).strftime(time_format)
        
def uniq_id(mac_addr):
    if mac_addr:
        return mac_addr
    else:
        mac_addr = xbmc.getInfoLabel('Network.MacAddress')
    if not ":" in mac_addr: mac_addr = xbmc.getInfoLabel('Network.MacAddress')
    # hack response busy
    if not ":" in mac_addr:
        time.sleep(2)
        mac_addr = xbmc.getInfoLabel('Network.MacAddress')
    if ":" in mac_addr:
        mac_addr = md5(str(mac_addr.decode("utf-8"))).hexdigest()
    else:
        mac_addr = md5(str(uuid_node())).hexdigest()
    addon.setSetting('device_id', mac_addr)
    return mac_addr
    
def days(title, now, start):
    today = datetime.date.today()
    if start and not title == 'Live':
        if now[:10] == start[:10]:
            return 'Today'
        elif str(today + datetime.timedelta(days=1)) == start[:10]:
            return 'Tomorrow'
        elif str(today + datetime.timedelta(days=2)) == start[:10]:
            return (today + datetime.timedelta(days=2)).strftime('%A')
        elif str(today + datetime.timedelta(days=3)) == start[:10]:
            return (today + datetime.timedelta(days=3)).strftime('%A')
        elif str(today + datetime.timedelta(days=4)) == start[:10]:
            return (today + datetime.timedelta(days=4)).strftime('%A')
        elif str(today + datetime.timedelta(days=5)) == start[:10]:
            return (today + datetime.timedelta(days=5)).strftime('%A')
        elif str(today + datetime.timedelta(days=6)) == start[:10]:
            return (today + datetime.timedelta(days=6)).strftime('%A')
        elif str(today + datetime.timedelta(days=7)) == start[:10]:
            return (today + datetime.timedelta(days=7)).strftime('%A')
        elif str(today + datetime.timedelta(days=8)) == start[:10]:
            return (today + datetime.timedelta(days=8)).strftime('%A')
    return title