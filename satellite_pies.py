import argparse
import ctypes
import math
import os
from PIL import Image, ImageOps
import platform
import re
import socket
from subprocess import Popen, PIPE
import sys
import tempfile
import urllib

# Prerequisites: PIL and OSM Viz
# Prerequisites: For --repeat, twisted.internet

# Optional: For a more accurate location based on nearby wifi networks, WirelessNetConsole [1] is needed, otherwise maps will be based on your public IP address which is less accurate.
# [1] http://www.nirsoft.net/utils/wireless_net_console.html

# TODO Error handling: no wifi, no internet...
# TODO Where available (Windows but not XP), get wifi network list with `netsh wlan show networks mode=bssid` instead of WirelessNetConsole
# TODO Linux
# TODO Use higher zoom aerial maps than MapQuest Open Aerial

try:
    from osmviz.manager import PILImageManager, OSMManager
except ImportError, e:
    sys.exit("ImportError: %s.\n"
              "OSM Viz module needed, available from\n"
              "http://cbick.github.com/osmviz/\n\n" % str(e))

last_pos_id = [] # Can be a list of wifis or an IP address. Used to check if user is in the same place.
last_coords = None,None

def get_wifi_geolocation():
    """
    Get the computer's geolocation using the nearest wifi networks. Should be very accurate. Required WirelessNetConsole.exe.
    """
    print "Get wifi geolocation"
    global last_pos_id
    cmd = 'WirelessNetConsole'
    try:
        p = Popen(cmd, stdout=PIPE, stderr=PIPE)
        stdout, stderr = p.communicate()
        # for line in stdout.split("\n"):
            # print line
        ssids = re.compile('SSID                          :  (.*)\r\r').findall(stdout)
        macs = re.compile('MAC Address                   :  (.*)\r\r').findall(stdout)
        rssis = re.compile('RSSI                          :  (.*)\r\r').findall(stdout)

        number_same = len(set(last_pos_id) & set(macs))
        if number_same > 1:
            print number_same, "same wifi networks found. Probably same place, don't update"
            return None, False
        else:
            last_pos_id = macs
        
        geourl = 'https://maps.googleapis.com/maps/api/browserlocation/json?browser=firefox&sensor=true'
        for i,ssid in enumerate(ssids):
            print macs[i], ssid, rssis[i]
            geourl += '&wifi=mac:%s%%7Cssid:%s%%7Css:%s' % (macs[i], ssid.replace(" ", "%20"), rssis[i])
        # Look up lat/lon from Google Maps API
        html = urllib.urlopen(geourl).read()
        lat = re.compile('"lat" : (.+),').findall(html)[0]
        lon = re.compile('"lng" : (.+)').findall(html)[0]
        print "Latitude:", lat
        print "Longitude:", lon
        return (lat, lon), True
    except:
        return None, False
    
def get_ip():
    """
    Get the computer's public-facing IP address.
    """
    print "Get public-facing IP address"
    ip = urllib.urlopen('http://automation.whatismyip.com/n09230945.asp').read()
    print "IP:", ip
    return ip

def get_geolocation(ip):
    """
    Get the computer's geolocation from its public-facing IP address. May not be very accurate, may even be in the wrong city or country.
    """
    print "Get IP geolocation"
    url = 'http://api.hostip.info/get_html.php?ip=%s&position=true' % ip
    print url
    response = urllib.urlopen(url).read()
    print(response)
    lines = response.split('\n')
    lat = re.compile('Latitude: ([0-9\.]*)').search(response).group(1)
    lon = re.compile('Longitude: ([0-9\.]*)').search(response).group(1)
    # city = re.compile('City: (.*)').search(response).group(1)
    # country = re.compile('Country: (.*)').search(response).group(1)
    print "Latitude: ", lat
    print "Longitude:", lon
    # print "City:", city
    # print "Country:", country
    return (lat, lon)

def get_desktop_size():
    """
    Return computer's desktop screen size.
    """
    user32 = ctypes.windll.user32
    screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
    print "Desktop size:", screensize
    return (screensize)

def get_metres_per_pixel(lat, zoom):
    """
    For a given latitude and OSM zoom level, return approximate number of metres each pixel represents.
    """
    metres_per_pixel = 156543.04 * math.cos(lat*(math.pi/180)) / math.pow(2, zoom)
    return metres_per_pixel
    
    
def get_bounding_box((lat, lon), (height_in_metres, width_in_metres)):
    """
    Give central coordinates and the required height/width of the screen in metres, return a bounding box of min_lat, max_lat, min_lon, max_lon.
    """
    # Earth's radius in metres, sphere
    R = 6378137
    
    # Offsets from centre to edge, in metres
    dn = height_in_metres/2
    de = width_in_metres/2
 
    # Coordinate offsets in radians
    dLat = dn/R
    dLon = de/(R*math.cos(math.pi*lat/180))

    # Convert back to degrees
    dLat *= 180/math.pi
    dLon *= 180/math.pi

    # Finally, offset positions in decimal degrees
    min_lat = lat - dLat
    max_lat = lat + dLat
    min_lon = lon - dLon
    max_lon = lon + dLon

    # print min_lat, max_lat, min_lon, max_lon
    return (min_lat, max_lat, min_lon, max_lon)

def get_osm_image((lat, lon), screensize, zoom):
    """
    Create, crop and save a PIL image of OSM tiles patched together.
    """
    lat, lon = float(lat), float(lon)
    metres_per_pixel = get_metres_per_pixel(lat, zoom)
    width_in_metres = screensize[0] * metres_per_pixel
    height_in_metres = screensize[1] * metres_per_pixel
    print "bbox (metres):", width_in_metres, height_in_metres
    bbox = get_bounding_box((lat, lon), (height_in_metres, width_in_metres))
    
    osm = OSMManager(image_manager=PILImageManager('RGB'),
                     server=args.osm_base)
    img, bnds = osm.createOSMImage(bbox, zoom)
    print "Pre-crop size: ", img.size
    img = ImageOps.fit(img, screensize, Image.ANTIALIAS)
    print "Post-crop size:", img.size
    # outfile = os.path.join(tempfile.gettempdir(), "satellite_pies.bmp") 
    img.save(outfile)
    return outfile

def set_wallpaper(filename):
    """
    Set an image as wallpaper.
    """
    if filename != None:
        print filename
        SPI_SETDESKWALLPAPER = 20
        ctypes.windll.user32.SystemParametersInfoA(SPI_SETDESKWALLPAPER, 0, filename, 0)

def print_terms_of_use():
    """
    Show terms of use for the map images.
    """
    print "\nTerms of Use:"
    print "\n * OSM maps: (c) OpenStreetMap and contributors, CC-BY-SA."
    print "\n * Watercolor and Toner maps: Courtesy of Stamen Design, and use OpenStreetMap data, (c) OpenStreetMap and contributors CC-BY-SA."
    print "\n * MapQuest Open Aerial Tiles: Portions Courtesy NASA/JPL-Caltech and U.S. Depart. of Agriculture, Farm Service Agency. Tiles Courtesy of MapQuest."
    
def do_work():
    """
    This gets the computer's location, fetches the correct-sized map and sets it as wallpaper.
    """
    latlon, changed = get_wifi_geolocation()
    if not changed:
        return
    if latlon:
        if not args.zoom:
            args.zoom = 17 # http://wiki.openstreetmap.org/wiki/Zoom_levels
    else:
        ip = get_ip()
        if last_pos_id == ip:
            print "Same place, don't update"
            return
        else:
            last_pos_id = ip

        latlon = get_geolocation(ip)

        if not args.zoom:
            args.zoom = 10 # less zoom for less accurate IP-based geolocation

    global last_coords
    if last_coords == latlon:
        print last_coords, "Same lat/lon coordinates as last time, don't update"
        return
    else:
        last_coords = latlon

    if args.tile == "aerial" and args.zoom > 11:
        # args.zoom = 11 # Levels 12+ are provided only in the US
        print "Warning: MapQuest Open Aerial zoom levels 12+ are provided only in the US"

    print "Zoom level:", args.zoom
    filename = get_osm_image(latlon, get_desktop_size(), args.zoom)
    set_wallpaper(filename)
    print_terms_of_use()

if __name__ == '__main__':
    if platform.system() != "Windows":
        sys.exit("Currently only implemented for Windows")

    parser = argparse.ArgumentParser(description='Satellite pies.', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-t', '--tile', default='watercolor', 
        choices=('toner', 'watercolor', 'osm', 'aerial'), 
        help='Type of map tile to use')
    parser.add_argument('-b', '--osm_base', metavar='URL', 
        help='Base URL for map tiles (use instead of --tile)')
    parser.add_argument('-z', '--zoom', metavar='level', type=int,
        help='Map zoom level')
    
    parser.add_argument('-r', '--repeat', action='store_true',
        help='Repeat')
    parser.add_argument('-w', '--wait', metavar='minutes', type=int, 
        help='Minutes to wait between repeat', default=5)

    args = parser.parse_args()
    print args

    if not args.osm_base:
        if args.tile == 'watercolor':
            args.osm_base = "http://b.tile.stamen.com/watercolor"
        elif args.tile == 'toner':
            args.osm_base = "http://b.tile.stamen.com/toner"
        elif args.tile == 'osm':
            args.osm_base = "http://tile.openstreetmap.org"
        elif args.tile == 'aerial':
            args.osm_base = "http://oatile1.mqcdn.com/tiles/1.0.0/sat"

    outfile = os.path.join(tempfile.gettempdir(), "satellite_pies.bmp") 
    set_wallpaper(outfile)
    
    if args.repeat:
        from twisted.internet import reactor, task
        loop = task.LoopingCall(do_work)
        loop.start(args.wait * 60) # seconds
        reactor.run()
    else:
        do_work() # run once

# End of file
