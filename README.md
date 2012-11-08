satellite-pies
==============

A hacked up Python version of Satellite Eyes for Windows.

Usage
-----

```
usage: satellite_pies.py [-h] [-t {toner,watercolor,osm,aerial}] [-b URL]
                         [-z level] [-x lat,lon] [-r] [-w minutes]

Satellite pies.

optional arguments:
  -h, --help            show this help message and exit
  -t {toner,watercolor,osm,aerial}, --tile {toner,watercolor,osm,aerial}
                        Type of map tile to use (default: watercolor)
  -b URL, --osm_base URL
                        Base URL for map tiles (use instead of --tile)
                        (default: None)
  -z level, --zoom level
                        Map zoom level (default: None)
  -x lat,lon, --coords lat,lon
                        Instead of your current position, use these
                        coordinates (default: None)
  -r, --repeat          Repeat (default: False)
  -w minutes, --wait minutes
                        Minutes to wait between repeat (default: 5)
```

Examples
--------

Run once with Toner maps at zoom 15:

    satellite_pies.py --tile toner --zoom 15

Update every ten minutes with OpenStreetMap maps:

    satellite_pies.py --tile osm --repeat --wait 10

Run once with an aerial map of a specific location (remembering west is negative):

    satellite_pies.py -x 38.8977,-77.0366 --tile aerial


Prerequisites
-------------

*Python*

 * [PIL](http://www.pythonware.com/products/pil/)
 * [OSM Viz](http://cbick.github.com/osmviz/html/index.html)
 * For --repeat, [Twisted](http://twistedmatrix.com/trac/)

*Optional prerequisite for Windows XP* 

 * Windows XP needs [WirelessNetConsole](http://www.nirsoft.net/utils/wireless_net_console.html) to get a list of nearby wifi networks, otherwise it will be based on your public-facing IP address which is less accurate.

 * For Windows Vista, Windows 7 and Windows Server 2008, nearby wifi networks can be found with `netsh wlan` (not available on XP). Only tested with fake test data on XP, so let me know if it works.
  
Map terms of use
----------------

The map images have the following terms of use. If you 

 * OSM maps: (c) [OpenStreetMap](http://wiki.openstreetmap.org/wiki/Tile_usage_policy) and contributors, [CC-BY-SA](http://creativecommons.org/licenses/by-sa/3.0/).

 * Watercolor and Toner maps: Courtesy of [Stamen Design](http://maps.stamen.com/), and use OpenStreetMap data, (c) [OpenStreetMap](http://wiki.openstreetmap.org/wiki/Tile_usage_policy) and contributors
[CC-BY-SA](http://creativecommons.org/licenses/by-sa/3.0/).

 * MapQuest Open Aerial Tiles: Portions Courtesy NASA/JPL-Caltech and U.S. Depart. of Agriculture, Farm Service Agency. Tiles Courtesy of [MapQuest](http://developer.mapquest.com/web/products/open/map#terms).